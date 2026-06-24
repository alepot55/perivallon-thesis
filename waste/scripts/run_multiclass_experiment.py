"""Experiment B — 22-class material classification on AerialWaste.

Uses only waste-positive images with category annotations.
Groups classes with <20 samples into "Rare" → 20-class problem.
FocalLoss (gamma=2.0) with class weights from class_weights_22.json.

Training: same two-phase protocol as Experiment A.
"""

from __future__ import annotations

import json
import logging
import time
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn as nn
from PIL import Image
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from torch.utils.data import DataLoader, Dataset
from torchmetrics.classification import (
    MulticlassAccuracy,
    MulticlassConfusionMatrix,
    MulticlassF1Score,
    MulticlassPrecision,
    MulticlassRecall,
)
from torchvision import transforms as T

from waste_detection.data.aerialwaste_dataset import WASTE_CATEGORIES
from waste_detection.models.multiclass_head import FocalLoss

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s][%(levelname)s] - %(message)s",
)
logger = logging.getLogger(__name__)

# AerialWaste RGB stats
AW_MEAN = (0.3201, 0.3358, 0.2801)
AW_STD = (0.1878, 0.1666, 0.1664)

# Classes to group into "Rare" (< 20 total samples across train+test)
RARE_THRESHOLD = 20
RARE_LABEL = "Rare"


def build_class_mapping(
    train_path: str = "data/raw/training.json",
    test_path: str = "data/raw/testing.json",
) -> tuple[dict[int, int], list[str], dict[str, list[str]]]:
    """Build category mapping, grouping rare classes.

    Returns:
        old_to_new: mapping from original cat_id (1-22) to new class index
        class_names: list of new class names (20 classes)
        rare_group: dict mapping "Rare" to list of original category names
    """
    # Count total occurrences across both splits
    total_counts: Counter[int] = Counter()
    for path in [train_path, test_path]:
        with open(path) as f:
            data = json.load(f)
        for img in data["images"]:
            for cat_id in img.get("categories", []):
                total_counts[cat_id] += 1

    # Identify rare classes
    rare_ids = {cid for cid, count in total_counts.items() if count < RARE_THRESHOLD}
    rare_names = [WASTE_CATEGORIES[cid] for cid in sorted(rare_ids)]

    # Build new mapping: non-rare classes keep order, Rare goes last
    new_names = []
    old_to_new = {}
    for cid in range(1, 23):
        if cid in rare_ids:
            continue
        old_to_new[cid] = len(new_names)
        new_names.append(WASTE_CATEGORIES[cid])

    # Add Rare class
    rare_idx = len(new_names)
    new_names.append(RARE_LABEL)
    for cid in rare_ids:
        old_to_new[cid] = rare_idx

    logger.info("Class mapping: %d original → %d classes", 22, len(new_names))
    logger.info("Rare classes (<%d samples): %s", RARE_THRESHOLD, rare_names)
    for i, name in enumerate(new_names):
        logger.info("  %2d: %s", i, name)

    return old_to_new, new_names, {"Rare": rare_names}


class MultiClassWasteDataset(Dataset):
    """AerialWaste dataset for multi-class material classification.

    Only includes images with at least one category annotation.
    Assigns primary label = first listed category.
    """

    def __init__(
        self,
        root: str | Path,
        split: str,
        old_to_new: dict[int, int],
        transform: Any = None,
    ) -> None:
        self.root = Path(root)
        self.images_dir = self.root / "images"
        self.transform = transform
        self.old_to_new = old_to_new

        json_name = "training.json" if split == "train" else "testing.json"
        with open(self.root / json_name) as f:
            data = json.load(f)

        # Filter to images with categories
        self.samples = []
        for img in data["images"]:
            cats = img.get("categories", [])
            if not cats:
                continue
            # Primary label: first category
            primary_cat = cats[0]
            new_label = self.old_to_new.get(primary_cat)
            if new_label is not None:
                self.samples.append({
                    "file_name": img["file_name"],
                    "label": new_label,
                    "all_categories": [self.old_to_new.get(c, -1) for c in cats],
                })

        logger.info(
            "MultiClassWasteDataset (%s): %d images with categories",
            split, len(self.samples),
        )

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        sample = self.samples[idx]
        img_path = self.images_dir / sample["file_name"]
        image = Image.open(img_path).convert("RGB")

        if self.transform is not None:
            image = self.transform(image)
        else:
            image = T.ToTensor()(image)

        return {
            "image": image,
            "label": torch.tensor(sample["label"], dtype=torch.long),
            "file_name": sample["file_name"],
        }


class MultiClassWasteModule(pl.LightningModule):
    """Lightning module for 20-class waste classification with Swin-T RSP."""

    def __init__(
        self,
        num_classes: int = 20,
        lr: float = 1e-3,
        weight_decay: float = 0.05,
        training_phase: str = "tl",
        class_weights: torch.Tensor | None = None,
        focal_gamma: float = 2.0,
        image_size: int = 224,
    ) -> None:
        super().__init__()
        self.save_hyperparameters(ignore=["class_weights"])

        import timm

        self.backbone = timm.create_model(
            "swin_tiny_patch4_window7_224",
            pretrained=True,
            num_classes=0,
            img_size=image_size,
        )
        embed_dim = self.backbone.num_features  # 768

        self.head = nn.Sequential(
            nn.Dropout(p=0.1),
            nn.Linear(embed_dim, num_classes),
        )

        # Freeze backbone for Phase 1
        if training_phase == "tl":
            for p in self.backbone.parameters():
                p.requires_grad = False

        # Focal loss with class weights
        self.criterion = FocalLoss(
            weight=class_weights,
            gamma=focal_gamma,
        )

        mk = {"num_classes": num_classes}
        self.train_acc = MulticlassAccuracy(**mk)
        self.train_f1 = MulticlassF1Score(**mk, average="macro")
        self.val_acc = MulticlassAccuracy(**mk)
        self.val_f1 = MulticlassF1Score(**mk, average="macro")
        self.val_precision = MulticlassPrecision(**mk, average="macro")
        self.val_recall = MulticlassRecall(**mk, average="macro")
        self.test_acc = MulticlassAccuracy(**mk)
        self.test_f1_macro = MulticlassF1Score(**mk, average="macro")
        self.test_f1_weighted = MulticlassF1Score(**mk, average="weighted")
        self.test_f1_per_class = MulticlassF1Score(**mk, average="none")
        self.test_precision = MulticlassPrecision(**mk, average="macro")
        self.test_recall = MulticlassRecall(**mk, average="macro")
        self.test_cm = MulticlassConfusionMatrix(**mk)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.backbone(x)
        return self.head(features)

    def _shared_step(self, batch):
        images = batch["image"]
        labels = batch["label"]
        logits = self(images)
        loss = self.criterion(logits, labels)
        preds = logits.argmax(dim=1)
        return loss, preds, labels

    def training_step(self, batch, batch_idx):
        loss, preds, labels = self._shared_step(batch)
        self.train_acc(preds, labels)
        self.train_f1(preds, labels)
        self.log("train/loss", loss, prog_bar=True)
        self.log("train/acc", self.train_acc, on_step=False, on_epoch=True)
        self.log("train/f1", self.train_f1, on_step=False, on_epoch=True)
        return loss

    def validation_step(self, batch, batch_idx):
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

    def test_step(self, batch, batch_idx):
        loss, preds, labels = self._shared_step(batch)
        self.test_acc(preds, labels)
        self.test_f1_macro(preds, labels)
        self.test_f1_weighted(preds, labels)
        self.test_f1_per_class(preds, labels)
        self.test_precision(preds, labels)
        self.test_recall(preds, labels)
        self.test_cm(preds, labels)
        self.log("test/loss", loss)
        self.log("test/acc", self.test_acc, on_step=False, on_epoch=True)
        self.log("test/f1_macro", self.test_f1_macro, on_step=False, on_epoch=True)
        self.log("test/f1_weighted", self.test_f1_weighted, on_step=False, on_epoch=True)
        self.log("test/precision", self.test_precision, on_step=False, on_epoch=True)
        self.log("test/recall", self.test_recall, on_step=False, on_epoch=True)

    def configure_optimizers(self):
        head_params = list(self.head.parameters())
        head_ids = {id(p) for p in head_params}
        backbone_params = [
            p for p in self.backbone.parameters()
            if p.requires_grad and id(p) not in head_ids
        ]

        groups = []
        if backbone_params:
            groups.append({"params": backbone_params, "name": "backbone"})
        groups.append({"params": head_params, "name": "head"})

        optimizer = torch.optim.AdamW(
            groups, lr=self.hparams.lr, weight_decay=self.hparams.weight_decay,
        )

        if self.hparams.training_phase == "ft":
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=self.trainer.max_epochs,
            )
            return {"optimizer": optimizer, "lr_scheduler": {"scheduler": scheduler, "interval": "epoch"}}
        else:
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer, mode="min", factor=0.5, patience=3,
            )
            return {"optimizer": optimizer, "lr_scheduler": {"scheduler": scheduler, "monitor": "val/loss"}}

    def switch_to_finetune(self, lr: float = 1e-4) -> None:
        # Unfreeze last Swin stage + norm
        for name, param in self.backbone.named_parameters():
            if "layers.3" in name or "norm" in name:
                param.requires_grad = True
        self.hparams.lr = lr
        self.hparams.training_phase = "ft"
        n_trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        logger.info("Phase 2: unfrozen layers.3 + norm — trainable=%d", n_trainable)


def compute_new_class_weights(
    train_ds: MultiClassWasteDataset,
    num_classes: int,
) -> torch.Tensor:
    """Compute inverse-frequency weights from the actual training distribution."""
    counts = torch.zeros(num_classes)
    for sample in train_ds.samples:
        counts[sample["label"]] += 1

    counts = counts.clamp(min=1)
    total = counts.sum()
    weights = total / (num_classes * counts)

    for i in range(num_classes):
        logger.info("  Class %d: count=%d, weight=%.4f", i, int(counts[i]), weights[i])

    return weights


def main() -> None:
    pl.seed_everything(42)

    # Build class mapping
    old_to_new, class_names, rare_group = build_class_mapping()
    num_classes = len(class_names)

    # Transforms
    train_transform = T.Compose([
        T.Resize((224, 224)),
        T.RandomHorizontalFlip(p=0.5),
        T.RandomVerticalFlip(p=0.5),
        T.RandomRotation(degrees=90, expand=False),
        T.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
        T.ToTensor(),
        T.Normalize(mean=AW_MEAN, std=AW_STD),
    ])

    eval_transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=AW_MEAN, std=AW_STD),
    ])

    # Create datasets
    train_ds = MultiClassWasteDataset("data/raw", "train", old_to_new, train_transform)
    test_ds = MultiClassWasteDataset("data/raw", "test", old_to_new, eval_transform)

    # Stratified train/val split
    from torch.utils.data import Subset
    labels = [s["label"] for s in train_ds.samples]
    n_val = int(len(train_ds) * 0.15)

    # Stratified split using sklearn-style approach
    rng = np.random.default_rng(42)
    indices = np.arange(len(train_ds))
    rng.shuffle(indices)

    val_indices = indices[:n_val].tolist()
    train_indices = indices[n_val:].tolist()

    train_subset = Subset(train_ds, train_indices)
    val_ds_tmp = MultiClassWasteDataset("data/raw", "train", old_to_new, eval_transform)
    val_subset = Subset(val_ds_tmp, val_indices)

    logger.info("Split: %d train, %d val, %d test", len(train_subset), len(val_subset), len(test_ds))

    # Class distribution in train
    train_label_counts = Counter()
    for idx in train_indices:
        train_label_counts[train_ds.samples[idx]["label"]] += 1
    for i, name in enumerate(class_names):
        logger.info("  Train class %d (%s): %d", i, name, train_label_counts.get(i, 0))

    # Class weights from train distribution
    weights_tensor = compute_new_class_weights(train_ds, num_classes)

    # DataLoaders
    train_dl = DataLoader(train_subset, batch_size=16, shuffle=True, num_workers=4, pin_memory=True)
    val_dl = DataLoader(val_subset, batch_size=16, shuffle=False, num_workers=4, pin_memory=True)
    test_dl = DataLoader(test_ds, batch_size=16, shuffle=False, num_workers=4, pin_memory=True)

    # Model
    module = MultiClassWasteModule(
        num_classes=num_classes,
        lr=1e-3,
        weight_decay=0.05,
        training_phase="tl",
        class_weights=weights_tensor,
        focal_gamma=2.0,
    )

    ckpt_dir = Path("checkpoints/multiclass_22")
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    csv_logger = pl.loggers.CSVLogger("logs", name="multiclass_22")

    # Phase 1: frozen backbone, 10 epochs
    logger.info("=== Phase 1 (TL) ===")
    ckpt_p1 = ModelCheckpoint(
        dirpath=str(ckpt_dir), filename="p1-{epoch:02d}-{val/f1:.4f}",
        monitor="val/f1", mode="max", save_top_k=1,
    )
    trainer_p1 = pl.Trainer(
        max_epochs=10, accelerator="gpu", devices=1, precision="16-mixed",
        callbacks=[ckpt_p1], logger=csv_logger, enable_model_summary=False,
    )
    t0 = time.time()
    trainer_p1.fit(module, train_dl, val_dl)
    p1_time = time.time() - t0
    logger.info("Phase 1 done (%.1f min)", p1_time / 60)

    # Load best P1 checkpoint
    if ckpt_p1.best_model_path:
        ckpt_data = torch.load(ckpt_p1.best_model_path, map_location="cpu")
        module.load_state_dict(ckpt_data["state_dict"])

    # Phase 2: unfreeze last stage, 15 epochs
    logger.info("=== Phase 2 (FT) ===")
    module.switch_to_finetune(lr=1e-4)

    ckpt_p2 = ModelCheckpoint(
        dirpath=str(ckpt_dir), filename="p2-{epoch:02d}-{val/f1:.4f}",
        monitor="val/f1", mode="max", save_top_k=1,
    )
    early_stop = EarlyStopping(monitor="val/f1", mode="max", patience=7)

    trainer_p2 = pl.Trainer(
        max_epochs=15, accelerator="gpu", devices=1, precision="16-mixed",
        callbacks=[ckpt_p2, early_stop], logger=csv_logger, enable_model_summary=False,
    )
    t1 = time.time()
    trainer_p2.fit(module, train_dl, val_dl)
    p2_time = time.time() - t1
    logger.info("Phase 2 done (%.1f min)", p2_time / 60)

    # Test evaluation
    best_ckpt = ckpt_p2.best_model_path or ckpt_p1.best_model_path
    logger.info("=== Test Evaluation ===")
    test_results = trainer_p2.test(module, test_dl, ckpt_path=best_ckpt)
    test_metrics = test_results[0] if test_results else {}

    # Per-class F1 and confusion matrix
    per_class_f1 = module.test_f1_per_class.compute().cpu()
    cm = module.test_cm.compute().cpu()

    logger.info("\nPer-class F1:")
    per_class_dict = {}
    for i, name in enumerate(class_names):
        f1_val = per_class_f1[i].item()
        per_class_dict[name] = round(f1_val, 4)
        logger.info("  %-45s %.4f", name, f1_val)

    # Save results
    results = {
        "num_classes": num_classes,
        "class_names": class_names,
        "rare_group": rare_group,
        "train_size": len(train_subset),
        "val_size": len(val_subset),
        "test_size": len(test_ds),
        "p1_time_min": round(p1_time / 60, 1),
        "p2_time_min": round(p2_time / 60, 1),
        "total_time_min": round((p1_time + p2_time) / 60, 1),
        "test/f1_macro": round(test_metrics.get("test/f1_macro", 0), 4),
        "test/f1_weighted": round(test_metrics.get("test/f1_weighted", 0), 4),
        "test/acc": round(test_metrics.get("test/acc", 0), 4),
        "test/precision": round(test_metrics.get("test/precision", 0), 4),
        "test/recall": round(test_metrics.get("test/recall", 0), 4),
        "per_class_f1": per_class_dict,
        "best_checkpoint": str(best_ckpt),
    }

    out_path = Path("data/processed/multiclass_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    logger.info("Results saved to %s", out_path)

    # Save confusion matrix as PNG
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    cm_np = cm.numpy().astype(int)
    im = ax.imshow(cm_np, interpolation="nearest", cmap="Blues")
    ax.set_xticks(range(num_classes))
    ax.set_yticks(range(num_classes))
    short_names = [n[:20] for n in class_names]
    ax.set_xticklabels(short_names, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(short_names, fontsize=8)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title(f"22-Class Confusion Matrix (Macro F1={results['test/f1_macro']:.2%})")
    fig.colorbar(im, ax=ax)

    # Annotate cells
    for i in range(num_classes):
        for j in range(num_classes):
            val = cm_np[i, j]
            if val > 0:
                ax.text(j, i, str(val), ha="center", va="center", fontsize=6,
                        color="white" if val > cm_np.max() / 2 else "black")

    fig.tight_layout()
    cm_path = Path("data/processed/confusion_matrix_22class.png")
    fig.savefig(cm_path, dpi=150)
    plt.close(fig)
    logger.info("Confusion matrix saved to %s", cm_path)

    # Summary
    sorted_f1 = sorted(per_class_dict.items(), key=lambda x: x[1], reverse=True)
    logger.info("\nTop-3 classes: %s", sorted_f1[:3])
    logger.info("Bottom-3 classes: %s", sorted_f1[-3:])


if __name__ == "__main__":
    main()
