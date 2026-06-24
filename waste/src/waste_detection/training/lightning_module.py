"""PyTorch Lightning module for waste classification training.

Implements the two-step training procedure from Gibellini et al. (2025):
  Step 1 — Transfer Learning: backbone frozen, train head only (LR=1e-3)
  Step 2 — Fine-Tuning: unfreeze last stage, train with lower LR (LR=1e-4)
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
)

from waste_detection.models.swin_rsp_baseline import SwinRSPClassifier

logger = logging.getLogger(__name__)


class WasteClassifierModule(pl.LightningModule):
    """Lightning module for binary waste scene classification.

    Args:
        model_cfg: Dict with SwinRSPClassifier constructor args.
        lr: Learning rate.
        training_phase: ``"tl"`` for Transfer Learning, ``"ft"`` for Fine-Tuning.
        threshold: Classification threshold for metrics.
        weight_decay: Weight decay for optimizer.
    """

    def __init__(
        self,
        model_cfg: dict[str, Any] | None = None,
        lr: float = 1e-3,
        training_phase: str = "tl",
        threshold: float = 0.5,
        weight_decay: float = 0.05,
    ) -> None:
        super().__init__()
        self.save_hyperparameters()

        model_cfg = model_cfg or {}
        if training_phase == "tl":
            model_cfg.setdefault("freeze_backbone", True)
            model_cfg.setdefault("unfreeze_last_stage", False)
        elif training_phase == "ft":
            model_cfg.setdefault("freeze_backbone", True)
            model_cfg.setdefault("unfreeze_last_stage", True)

        self.model = SwinRSPClassifier(**model_cfg)
        self.criterion = nn.BCEWithLogitsLoss()
        self.threshold = threshold

        # Metrics
        metrics_kwargs: dict[str, Any] = {"threshold": threshold}
        self.train_acc = BinaryAccuracy(**metrics_kwargs)
        self.train_f1 = BinaryF1Score(**metrics_kwargs)
        self.val_acc = BinaryAccuracy(**metrics_kwargs)
        self.val_f1 = BinaryF1Score(**metrics_kwargs)
        self.val_precision = BinaryPrecision(**metrics_kwargs)
        self.val_recall = BinaryRecall(**metrics_kwargs)
        self.test_acc = BinaryAccuracy(**metrics_kwargs)
        self.test_f1 = BinaryF1Score(**metrics_kwargs)
        self.test_precision = BinaryPrecision(**metrics_kwargs)
        self.test_recall = BinaryRecall(**metrics_kwargs)
        self.test_cm = BinaryConfusionMatrix()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def _shared_step(self, batch: dict[str, Any]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        images = batch["image"]
        labels = batch["label"]
        logits = self(images).squeeze(-1)
        loss = self.criterion(logits, labels)
        preds = torch.sigmoid(logits)
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
        tn, fp, fn, tp = cm.flatten().int().tolist()
        logger.info("Confusion Matrix (test set):")
        logger.info("  Predicted →  Neg    Pos")
        logger.info("  Actual Neg   %5d  %5d", tn, fp)
        logger.info("  Actual Pos   %5d  %5d", fn, tp)
        logger.info("  TN=%d FP=%d FN=%d TP=%d", tn, fp, fn, tp)

    def configure_optimizers(self) -> dict[str, Any]:
        param_groups = self.model.get_trainable_params()
        optimizer = torch.optim.AdamW(
            param_groups,
            lr=self.hparams.lr,
            weight_decay=self.hparams.weight_decay,
        )

        if self.hparams.training_phase == "ft":
            # CosineAnnealingLR for fine-tuning phase
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=self.trainer.max_epochs,
            )
            return {
                "optimizer": optimizer,
                "lr_scheduler": {
                    "scheduler": scheduler,
                    "interval": "epoch",
                },
            }
        else:
            # ReduceLROnPlateau for transfer learning phase
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer, mode="min", factor=0.5, patience=5,
            )
            return {
                "optimizer": optimizer,
                "lr_scheduler": {
                    "scheduler": scheduler,
                    "monitor": "val/loss",
                },
            }

    def switch_to_finetune(self, lr: float = 1e-4) -> None:
        """Switch from Transfer Learning to Fine-Tuning phase.

        Call this between training phases to unfreeze the last backbone stage
        and lower the learning rate.
        """
        self.model.unfreeze_last_stage()
        self.hparams.lr = lr
        self.hparams.training_phase = "ft"
