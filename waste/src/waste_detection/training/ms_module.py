"""Lightning module for multispectral foundation model training.

Unified module for SSL4EOClassifier, DOFAClassifier, and any future
backbone that follows the same interface (forward, phase1, phase2,
get_trainable_params).

Supports both binary (BCE) and multi-class (CE/Focal) classification.
"""

from __future__ import annotations

import logging
from typing import Any

import pytorch_lightning as pl
import torch
import torch.nn as nn
from torchmetrics.classification import (
    BinaryAccuracy,
    BinaryConfusionMatrix,
    BinaryF1Score,
    BinaryPrecision,
    BinaryRecall,
    MulticlassAccuracy,
    MulticlassConfusionMatrix,
    MulticlassF1Score,
    MulticlassPrecision,
    MulticlassRecall,
)

logger = logging.getLogger(__name__)


class MSClassifierModule(pl.LightningModule):
    """Lightning module for multispectral scene classification.

    Works with any model that has:
      - forward(x) -> logits or forward(x, wavelengths) -> logits
      - phase1() / phase2() for training phase control
      - get_trainable_params() -> list of param groups

    Args:
        model: Classification model (SSL4EOClassifier, DOFAClassifier, etc.).
        n_classes: Number of classes (1 for binary BCE, >=2 for multi-class CE).
        lr: Learning rate.
        training_phase: ``"tl"`` for transfer learning, ``"ft"`` for fine-tuning.
        weight_decay: Weight decay for AdamW.
        criterion: Loss function (if None, auto-selects BCE or CE).
        wavelengths: Wavelengths to pass to DOFA forward (None for non-DOFA).
    """

    def __init__(
        self,
        model: nn.Module,
        n_classes: int = 2,
        lr: float = 1e-3,
        training_phase: str = "tl",
        weight_decay: float = 0.05,
        criterion: nn.Module | None = None,
        wavelengths: list[float] | None = None,
    ) -> None:
        super().__init__()
        self.save_hyperparameters(ignore=["model", "criterion"])
        self.model = model
        self.wavelengths = wavelengths

        # Determine task type
        self.is_binary = n_classes <= 2
        self._out_classes = 1 if (n_classes == 2 and self.is_binary) else n_classes

        # Loss
        if criterion is not None:
            self.criterion = criterion
        elif self.is_binary:
            self.criterion = nn.BCEWithLogitsLoss()
        else:
            self.criterion = nn.CrossEntropyLoss()

        # Metrics
        if self.is_binary:
            self.train_acc = BinaryAccuracy()
            self.train_f1 = BinaryF1Score()
            self.val_acc = BinaryAccuracy()
            self.val_f1 = BinaryF1Score()
            self.val_precision = BinaryPrecision()
            self.val_recall = BinaryRecall()
            self.test_acc = BinaryAccuracy()
            self.test_f1 = BinaryF1Score()
            self.test_precision = BinaryPrecision()
            self.test_recall = BinaryRecall()
            self.test_cm = BinaryConfusionMatrix()
        else:
            mk: dict[str, Any] = {"num_classes": n_classes}
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
            self.test_cm = MulticlassConfusionMatrix(**mk)

    def _forward(self, x: torch.Tensor) -> torch.Tensor:
        """Call model forward, passing wavelengths if needed (DOFA)."""
        if self.wavelengths is not None:
            return self.model(x, self.wavelengths)
        return self.model(x)

    def _shared_step(
        self, batch: dict[str, Any],
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        images = batch["image"]
        labels = batch["label"]
        logits = self._forward(images)

        if self.is_binary:
            logits = logits.squeeze(-1)
            labels = labels.float()
            loss = self.criterion(logits, labels)
            preds = torch.sigmoid(logits)
        else:
            labels = labels.long()
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
        self.test_cm(preds, labels)
        self.log("test/loss", loss)
        self.log("test/acc", self.test_acc, on_step=False, on_epoch=True)
        self.log("test/f1", self.test_f1, on_step=False, on_epoch=True)
        self.log("test/precision", self.test_precision, on_step=False, on_epoch=True)
        self.log("test/recall", self.test_recall, on_step=False, on_epoch=True)

    def on_test_epoch_end(self) -> None:
        cm = self.test_cm.compute()
        if self.is_binary:
            tn, fp, fn, tp = cm.flatten().int().tolist()
            logger.info("Test CM: TN=%d FP=%d FN=%d TP=%d", tn, fp, fn, tp)
        else:
            logger.info("Test Confusion Matrix:\n%s", cm.int())

    def configure_optimizers(self) -> dict[str, Any]:
        if hasattr(self.model, "get_trainable_params"):
            param_groups = self.model.get_trainable_params()
        else:
            param_groups = [{"params": [p for p in self.model.parameters() if p.requires_grad]}]

        optimizer = torch.optim.AdamW(
            param_groups, lr=self.hparams.lr, weight_decay=self.hparams.weight_decay,
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

    def switch_to_finetune(self, lr: float = 1e-4, n_blocks: int = 4) -> None:
        """Switch from TL to FT phase."""
        if hasattr(self.model, "phase2"):
            self.model.phase2(n_blocks=n_blocks)
        self.hparams.lr = lr
        self.hparams.training_phase = "ft"
