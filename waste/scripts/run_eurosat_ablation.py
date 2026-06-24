#!/usr/bin/env python3
"""EuroSAT band ablation study.

Runs 10 configurations (1 RGB baseline + 3 strategies x 3 band configs)
to evaluate multispectral adaptation strategies for Swin-T with RSP weights.

Usage:
    python scripts/run_eurosat_ablation.py

Results saved to data/processed/eurosat_ablation_results.json with
crash-resilient per-run saving (can restart to continue from last run).
"""

from __future__ import annotations

import csv
import json
import logging
import time
from pathlib import Path

import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint, RichProgressBar
from pytorch_lightning.loggers import CSVLogger

from waste_detection.data.eurosat_ms_dm import (
    BAND_PRESETS,
    EUROSAT_CLASSES,
    EuroSATMultispectralDM,
)
from waste_detection.models.swin_ms_adapter import LateFusionClassifier, adapt_patch_embed
from waste_detection.models.swin_rsp_baseline import SwinRSPClassifier
from waste_detection.training.multiclass_module import MultiClassModule

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s][%(levelname)s] - %(message)s",
)
logger = logging.getLogger(__name__)

# ─── Configuration ──────────────────────────────────────────────────────────

RSP_CHECKPOINT = "checkpoints/rsp_swin_t_e300.pth"
IMAGE_SIZE = 224
NUM_CLASSES = 10
BATCH_SIZE = 32
NUM_WORKERS = 4
SEED = 42

TL_EPOCHS = 10
FT_EPOCHS = 15
LR_TL = 1e-3
LR_FT = 1e-4
WEIGHT_DECAY = 0.05
PATIENCE = 5

EUROSAT_ROOT = "data/eurosat"
RESULTS_PATH = Path("data/processed/eurosat_ablation_results.json")

# ─── Run definitions ────────────────────────────────────────────────────────

RUNS: list[dict] = [
    {"name": "RGB_baseline",            "band_config": "RGB",  "strategy": None},
    {"name": "RGBN_weight_inflation",   "band_config": "RGBN", "strategy": "weight_inflation"},
    {"name": "RGBN_random_init_extra",  "band_config": "RGBN", "strategy": "random_init_extra"},
    {"name": "RGBN_late_fusion",        "band_config": "RGBN", "strategy": "late_fusion"},
    {"name": "MS6_weight_inflation",    "band_config": "MS6",  "strategy": "weight_inflation"},
    {"name": "MS6_random_init_extra",   "band_config": "MS6",  "strategy": "random_init_extra"},
    {"name": "MS6_late_fusion",         "band_config": "MS6",  "strategy": "late_fusion"},
    {"name": "MS10_weight_inflation",   "band_config": "MS10", "strategy": "weight_inflation"},
    {"name": "MS10_random_init_extra",  "band_config": "MS10", "strategy": "random_init_extra"},
    {"name": "MS10_late_fusion",        "band_config": "MS10", "strategy": "late_fusion"},
]


# ─── Helpers ────────────────────────────────────────────────────────────────


def create_model(band_config: str, strategy: str | None) -> torch.nn.Module:
    """Create and adapt a Swin-T model for the given configuration."""
    n_channels = len(BAND_PRESETS[band_config])

    # Base model: RSP pretrained, backbone frozen (TL phase)
    base = SwinRSPClassifier(
        rsp_checkpoint_path=RSP_CHECKPOINT,
        num_classes=NUM_CLASSES,
        image_size=IMAGE_SIZE,
        freeze_backbone=True,
        unfreeze_last_stage=False,
    )

    if strategy is None:
        return base

    # Adapt for multispectral input
    # Note: adapt_patch_embed deep-copies the model, so `base` is untouched.
    # The new patch_embed.proj has requires_grad=True by default (new Conv2d),
    # so it will be trainable even though the rest of the backbone is frozen.
    model = adapt_patch_embed(base, in_channels=n_channels, strategy=strategy)

    # For LateFusion: both backbones are deep-copied from the frozen base,
    # so transformer layers are already frozen. The new patch_embed in the
    # extra_backbone has requires_grad=True. fusion + head are trainable.
    return model


def build_trainer(phase: str, run_name: str, max_epochs: int) -> pl.Trainer:
    """Create a fresh Trainer for a training phase."""
    ckpt_dir = Path(f"checkpoints/eurosat_ablation/{run_name}/{phase}")
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    return pl.Trainer(
        max_epochs=max_epochs,
        accelerator="auto",
        devices=1,
        precision="16-mixed",
        log_every_n_steps=10,
        deterministic=False,
        logger=CSVLogger(save_dir="logs/eurosat_ablation", name=f"{run_name}_{phase}"),
        callbacks=[
            ModelCheckpoint(
                dirpath=str(ckpt_dir),
                filename="{epoch:02d}-{val/f1:.4f}",
                monitor="val/f1",
                mode="max",
                save_top_k=1,
            ),
            EarlyStopping(
                monitor="val/f1",
                patience=PATIENCE,
                min_delta=0.001,
                mode="max",
            ),
            RichProgressBar(),
        ],
        default_root_dir=f"outputs/eurosat_ablation/{run_name}/{phase}",
    )


def parse_csv_history(csv_dir: str | Path) -> list[dict]:
    """Extract per-epoch metrics from CSVLogger output."""
    metrics_file = Path(csv_dir) / "metrics.csv"
    if not metrics_file.exists():
        return []

    epoch_data: dict[int, dict] = {}
    with open(metrics_file) as f:
        for row in csv.DictReader(f):
            epoch = int(row.get("epoch", -1))
            if epoch < 0:
                continue
            if epoch not in epoch_data:
                epoch_data[epoch] = {}
            for k, v in row.items():
                if v and k not in ("epoch", "step"):
                    try:
                        epoch_data[epoch][k] = float(v)
                    except ValueError:
                        pass

    return [{"epoch": e, **epoch_data[e]} for e in sorted(epoch_data)]


def count_trainable(model: torch.nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


# ─── Main experiment loop ───────────────────────────────────────────────────


def run_single_experiment(run_cfg: dict) -> dict:
    """Run one ablation experiment: TL → FT → test."""
    name = run_cfg["name"]
    band_config = run_cfg["band_config"]
    strategy = run_cfg["strategy"]
    n_channels = len(BAND_PRESETS[band_config])

    logger.info("=" * 60)
    logger.info("RUN: %s  (bands=%s, n_ch=%d, strategy=%s)", name, band_config, n_channels, strategy)
    logger.info("=" * 60)

    start = time.time()
    pl.seed_everything(SEED, workers=True)
    torch.set_float32_matmul_precision("high")

    # Model
    model = create_model(band_config, strategy)
    logger.info("Trainable params (TL): %s", f"{count_trainable(model):,}")

    # Data
    dm = EuroSATMultispectralDM(
        root=EUROSAT_ROOT,
        bands_preset=band_config,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        download=True,
    )

    # ── Phase 1: Transfer Learning ──────────────────────────────────────
    module = MultiClassModule(
        model=model, num_classes=NUM_CLASSES,
        lr=LR_TL, training_phase="tl", weight_decay=WEIGHT_DECAY,
    )

    tl_trainer = build_trainer("tl", name, TL_EPOCHS)
    tl_trainer.fit(module, dm)

    tl_best_f1 = tl_trainer.callback_metrics.get("val/f1", torch.tensor(0.0)).item()
    tl_ckpt = tl_trainer.checkpoint_callback.best_model_path
    logger.info("TL best val/f1: %.4f  ckpt: %s", tl_best_f1, tl_ckpt)

    # Divergence check
    if tl_best_f1 < 0.30:
        logger.warning("DIVERGED in TL (val/f1=%.4f < 0.30). Flagging.", tl_best_f1)
        return {
            "name": name, "band_config": band_config, "strategy": strategy,
            "n_channels": n_channels, "status": "diverged_tl",
            "tl_best_val_f1": tl_best_f1,
        }

    # Load best TL checkpoint
    if tl_ckpt:
        state = torch.load(tl_ckpt, map_location="cpu", weights_only=False)
        module.load_state_dict(state["state_dict"])
        logger.info("Loaded best TL checkpoint")

    # ── Phase 2: Fine-Tuning ────────────────────────────────────────────
    module.switch_to_finetune(lr=LR_FT)
    logger.info("Trainable params (FT): %s", f"{count_trainable(module.model):,}")

    ft_trainer = build_trainer("ft", name, FT_EPOCHS)
    ft_trainer.fit(module, dm)

    ft_ckpt = ft_trainer.checkpoint_callback.best_model_path
    logger.info("FT best ckpt: %s", ft_ckpt)

    # ── Test ────────────────────────────────────────────────────────────
    test_results = ft_trainer.test(module, dm, ckpt_path=ft_ckpt)
    test_metrics = test_results[0] if test_results else {}

    per_class_f1 = module.test_f1_per_class.compute().cpu().tolist()
    per_class_dict = {
        EUROSAT_CLASSES[i]: round(per_class_f1[i], 4)
        for i in range(min(len(EUROSAT_CLASSES), len(per_class_f1)))
    }

    # Training history
    tl_history = parse_csv_history(tl_trainer.logger.log_dir)
    ft_history = parse_csv_history(ft_trainer.logger.log_dir)

    elapsed = time.time() - start
    result = {
        "name": name,
        "band_config": band_config,
        "strategy": strategy,
        "n_channels": n_channels,
        "status": "completed",
        "tl_best_val_f1": round(tl_best_f1, 4),
        "test_f1": round(test_metrics.get("test/f1", 0.0), 4),
        "test_acc": round(test_metrics.get("test/acc", 0.0), 4),
        "test_precision": round(test_metrics.get("test/precision", 0.0), 4),
        "test_recall": round(test_metrics.get("test/recall", 0.0), 4),
        "test_loss": round(test_metrics.get("test/loss", 0.0), 4),
        "per_class_f1": per_class_dict,
        "tl_history": tl_history,
        "ft_history": ft_history,
        "elapsed_seconds": round(elapsed, 1),
    }

    logger.info(
        "✓ %s — test/F1=%.2f%%  test/Acc=%.2f%%  (%.1f min)",
        name, result["test_f1"] * 100, result["test_acc"] * 100, elapsed / 60,
    )
    return result


def main() -> None:
    """Run all ablation experiments with crash-resilient saving."""
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load existing results (restart support)
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH) as f:
            all_results = json.load(f)
        logger.info("Loaded existing results (%d runs)", len(all_results.get("runs", {})))
    else:
        all_results = {
            "config": {
                "seed": SEED, "image_size": IMAGE_SIZE, "batch_size": BATCH_SIZE,
                "tl_epochs": TL_EPOCHS, "ft_epochs": FT_EPOCHS,
                "lr_tl": LR_TL, "lr_ft": LR_FT,
                "weight_decay": WEIGHT_DECAY, "patience": PATIENCE,
                "rsp_checkpoint": RSP_CHECKPOINT,
            },
            "runs": {},
        }

    completed = set(all_results["runs"].keys())
    total_start = time.time()

    # Pre-download EuroSAT
    logger.info("Ensuring EuroSAT data is downloaded...")
    from torchgeo.datasets import EuroSAT as _EuroSAT
    _EuroSAT(root=EUROSAT_ROOT, split="train", download=True)
    logger.info("EuroSAT data ready.")

    for run_cfg in RUNS:
        name = run_cfg["name"]
        if name in completed:
            logger.info("Skipping %s (already completed)", name)
            continue

        try:
            result = run_single_experiment(run_cfg)
            all_results["runs"][name] = result
        except Exception as e:
            logger.error("Run %s FAILED: %s", name, e, exc_info=True)
            all_results["runs"][name] = {
                "name": name, "band_config": run_cfg["band_config"],
                "strategy": run_cfg["strategy"], "status": "failed", "error": str(e),
            }

        # Save after each run
        with open(RESULTS_PATH, "w") as f:
            json.dump(all_results, f, indent=2)
        logger.info("Saved to %s", RESULTS_PATH)

    total_elapsed = time.time() - total_start
    logger.info("All %d runs complete in %.1f hours.", len(RUNS), total_elapsed / 3600)
    logger.info("Results: %s", RESULTS_PATH)


if __name__ == "__main__":
    main()
