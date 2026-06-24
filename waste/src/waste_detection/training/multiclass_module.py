"""Multi-class Lightning module for scene classification.

Supports both SwinRSPClassifier and LateFusionClassifier models.
Uses CrossEntropyLoss and multi-class metrics from torchmetrics.
"""

from __future__ import annotations

import logging
from typing import Any

import pytorch_lightning as pl
import torch
import torch.nn as nn
from torchmetrics.classification import (
    MulticlassAccuracy,
    MulticlassConfusionMatrix,
    MulticlassF1Score,
    MulticlassPrecision,
    MulticlassRecall,
)

from waste_detection.data.eurosat_ms_dm import EUROSAT_CLASSES
from waste_detection.models.swin_ms_adapter import LateFusionClassifier

logger = logging.getLogger(__name__)


class MultiClassModule(pl.LightningModule):
    """Lightning module for multi-class scene classification.

    Works with any model implementing forward(x) -> [B, num_classes].

    Args:
        model: Classification model (SwinRSPClassifier or LateFusionClassifier).
        num_classes: Number of output classes.
        lr: Learning rate.
        training_phase: ``"tl"`` or ``"ft"``.
        weight_decay: Weight decay for AdamW.
    """

    def __init__(
        self,
        model: nn.Module,
        num_classes: int = 10,
        lr: float = 1e-3,
        training_phase: str = "tl",
        weight_decay: float = 0.05,
    ) -> None:
        super().__init__()
        self.save_hyperparameters(ignore=["model"])
        self.model = model
        self.criterion = nn.CrossEntropyLoss()

        mk: dict[str, Any] = {"num_classes": num_classes}
        self.train_acc = MulticlassAccuracy(**mk)
        self.train_f1 = MulticlassF1Score(**mk, average="macro")
        self.val_acc = MulticlassAccuracy(**mk)
        self.val_f1 = MulticlassF1Score(**mk, average="macro")
        self.val_precision = MulticlassPrecision(**mk, average="macro")
        self.val_recall = MulticlassRecall(**mk, average="macro")
        self.test_acc = MulticlassAccuracy(**mk)
        self.test_f1 = MulticlassF1Score(**mk, average="macro")
        self.test_precision = MulticlassPrecision(**mk, average="macro")
        self.test_recall = MulticlassRecall(**mk, average="macro")
        self.test_f1_per_class = MulticlassF1Score(**mk, average="none")
        self.test_cm = MulticlassConfusionMatrix(**mk)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def _shared_step(
        self, batch: dict[str, Any],
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        images = batch["image"]
        labels = batch["label"].long()
        logits = self(images)  # [B, num_classes]
        loss = self.criterion(logits, labels)
        preds = logits.argmax(dim=1)
        return loss, preds, labels

    def training_step(self, batch: dict[str, Any], batch_idx: int) -> torch.Tensor:
        loss, preds, labels = self._shared_step(batch)
        self.train_acc(preds, labels)
        self.train_f1(preds, labels)
        self.log("train/loss", loss, prog_bar=True)
        self.log("train/acc", self.train_acc, on_step=False, on_epoch=True)
        self.log("train/f1", self.train_f1, on_step=False, on_epoch=True)
        return loss

    def validation_step(self, batch: dict[str, Any], batch_idx: int) -> None:
        loss, preds, labels = self._shared_step(batch)
        self.val_acc(preds, labels)
        self.val_f1(preds, labels)
        self.val_precision(preds, labels)
        self.val_recall(preds, labels)
        self.log("val/loss", loss, prog_bar=True)
        self.log("val/acc", self.val_acc, on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/f1", self.val_f1, on_step=False, on_epoch=True, prog_bar=True)
        self.log("val/precision", self.val_precision, on_step=False, on_epoch=True)
        self.log("val/recall", self.val_recall, on_step=False, on_epoch=True)

    def test_step(self, batch: dict[str, Any], batch_idx: int) -> None:
        loss, preds, labels = self._shared_step(batch)
        self.test_acc(preds, labels)
        self.test_f1(preds, labels)
        self.test_precision(preds, labels)
        self.test_recall(preds, labels)
        self.test_f1_per_class(preds, labels)
        self.test_cm(preds, labels)
        self.log("test/loss", loss)
        self.log("test/acc", self.test_acc, on_step=False, on_epoch=True)
        self.log("test/f1", self.test_f1, on_step=False, on_epoch=True)
        self.log("test/precision", self.test_precision, on_step=False, on_epoch=True)
        self.log("test/recall", self.test_recall, on_step=False, on_epoch=True)

    def on_test_epoch_end(self) -> None:
        per_class_f1 = self.test_f1_per_class.compute()
        cm = self.test_cm.compute()
        logger.info("Per-class F1 scores:")
        for i, f1_val in enumerate(per_class_f1):
            name = EUROSAT_CLASSES[i] if i < len(EUROSAT_CLASSES) else f"Class {i}"
            logger.info("  %s: %.4f", name, f1_val.item())
        logger.info("Confusion Matrix:\n%s", cm.int())

    def configure_optimizers(self) -> dict[str, Any]:
        trainable = [p for p in self.model.parameters() if p.requires_grad]
        optimizer = torch.optim.AdamW(
            trainable, lr=self.hparams.lr, weight_decay=self.hparams.weight_decay,
        )
        if self.hparams.training_phase == "ft":
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=self.trainer.max_epochs,
            )
            return {
                "optimizer": optimizer,
                "lr_scheduler": {"scheduler": scheduler, "interval": "epoch"},
            }
        else:
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer, mode="min", factor=0.5, patience=3,
            )
            return {
                "optimizer": optimizer,
                "lr_scheduler": {"scheduler": scheduler, "monitor": "val/loss"},
            }

    def switch_to_finetune(self, lr: float = 1e-4) -> None:
        """Unfreeze last backbone stage and switch to FT phase."""
        if isinstance(self.model, LateFusionClassifier):
            for name, param in self.model.rgb_backbone.named_parameters():
                if "layers.3" in name or "norm" in name:
                    param.requires_grad = True
            for name, param in self.model.extra_backbone.named_parameters():
                if "layers.3" in name or "norm" in name:
                    param.requires_grad = True
            logger.info("LateFusion: unfrozen layers.3 + norm in both backbones")
        elif hasattr(self.model, "unfreeze_last_stage"):
            self.model.unfreeze_last_stage()
        self.hparams.lr = lr
        self.hparams.training_phase = "ft"
