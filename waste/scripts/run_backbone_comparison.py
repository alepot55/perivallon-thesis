"""Experiment A — Backbone comparison on AerialWaste binary classification.

Compares three pretrained backbones on waste/no-waste task:
  A1. Swin-T RSP (ImageNet → Million-AID RSP)
  A2. SSL4EO ViT-S/16 (Sentinel-2 MoCo, RGB bands)
  A3. DOFA ViT-B/16 (wavelength-conditioned MAE, RGB wavelengths)

Same training protocol for all:
  Phase 1: 10 epochs, frozen backbone, lr=1e-3
  Phase 2: 15 epochs, unfreeze last blocks, lr=1e-4, CosineAnnealing
  AdamW, wd=0.05, batch_size=32, val_fraction=0.15, seed=42, early_stop=7
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint

from waste_detection.data.aerialwaste_dm import AerialWasteDataModule
from waste_detection.models.swin_rsp_baseline import SwinRSPClassifier
from waste_detection.models.ssl4eo_classifier import SSL4EOClassifier
from waste_detection.models.dofa_classifier import DOFAClassifier, S2_ALL_WAVELENGTHS
from waste_detection.training.ms_module import MSClassifierModule
from waste_detection.training.lightning_module import WasteClassifierModule

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s][%(levelname)s] - %(message)s",
)
logger = logging.getLogger(__name__)

# AerialWaste RGB stats (from dataset_stats.json, [0,1] scale)
AW_MEAN = (0.3201, 0.3358, 0.2801)
AW_STD = (0.1878, 0.1666, 0.1664)

CKPT_DIR = Path("checkpoints/backbone_comparison")
RESULTS_PATH = Path("data/processed/backbone_comparison_results.json")


def make_datamodule(image_size: int = 224, batch_size: int = 32) -> AerialWasteDataModule:
    """Create AerialWaste DataModule with consistent settings."""
    return AerialWasteDataModule(
        root="data/raw",
        image_size=image_size,
        target_gsd=None,  # all sources
        batch_size=batch_size,
        num_workers=4,
        val_fraction=0.15,
        mean=AW_MEAN,
        std=AW_STD,
        seed=42,
    )


def measure_inference_time(
    model: torch.nn.Module,
    input_shape: tuple,
    device: str = "cuda",
    n_warmup: int = 10,
    n_runs: int = 50,
    wavelengths: list[float] | None = None,
) -> float:
    """Measure average inference time per batch in ms."""
    model.eval()
    model.to(device)
    x = torch.randn(*input_shape, device=device)

    # Warmup
    with torch.no_grad():
        for _ in range(n_warmup):
            if wavelengths is not None:
                model(x, wavelengths)
            else:
                model(x)

    torch.cuda.synchronize()
    t0 = time.perf_counter()
    with torch.no_grad():
        for _ in range(n_runs):
            if wavelengths is not None:
                model(x, wavelengths)
            else:
                model(x)
    torch.cuda.synchronize()
    elapsed = (time.perf_counter() - t0) / n_runs * 1000  # ms
    return elapsed


def train_two_phase(
    module: pl.LightningModule,
    dm: AerialWasteDataModule,
    label: str,
    precision: int | str = "16-mixed",
    phase1_epochs: int = 10,
    phase2_epochs: int = 15,
    patience: int = 7,
) -> dict:
    """Run two-phase training and return results.

    Phase 1: fixed epochs (no early stopping) — head only.
    Phase 2: up to phase2_epochs with early stopping — last blocks unfrozen.
    """
    ckpt_dir = CKPT_DIR / label
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    csv_logger = pl.loggers.CSVLogger("logs", name=label)

    # Phase 1: frozen backbone, fixed epochs
    logger.info("=== %s Phase 1 (TL, %d epochs) ===", label, phase1_epochs)
    ckpt_p1 = ModelCheckpoint(
        dirpath=str(ckpt_dir),
        filename="p1-{epoch:02d}-{val/f1:.4f}",
        monitor="val/f1", mode="max", save_top_k=1,
    )

    trainer_p1 = pl.Trainer(
        max_epochs=phase1_epochs,
        accelerator="gpu",
        devices=1,
        precision=precision,
        callbacks=[ckpt_p1],
        logger=csv_logger,
        enable_model_summary=False,
    )

    t0 = time.time()
    trainer_p1.fit(module, dm)
    p1_time = time.time() - t0

    best_p1_f1 = trainer_p1.callback_metrics.get("val/f1", torch.tensor(0)).item()
    logger.info(
        "%s Phase 1 done: val/F1=%.2f%% (%.1f min)",
        label, best_p1_f1 * 100, p1_time / 60,
    )

    # Load best Phase 1 checkpoint before switching to FT
    if ckpt_p1.best_model_path:
        ckpt_data = torch.load(ckpt_p1.best_model_path, map_location="cpu")
        module.load_state_dict(ckpt_data["state_dict"])
        logger.info("Loaded best P1 checkpoint: %s", ckpt_p1.best_model_path)

    # Phase 2: unfreeze last blocks
    logger.info("=== %s Phase 2 (FT, up to %d epochs) ===", label, phase2_epochs)
    if hasattr(module, "switch_to_finetune"):
        if isinstance(module, MSClassifierModule):
            module.switch_to_finetune(lr=1e-4, n_blocks=4)
        else:
            module.switch_to_finetune(lr=1e-4)

    ckpt_p2 = ModelCheckpoint(
        dirpath=str(ckpt_dir),
        filename="p2-{epoch:02d}-{val/f1:.4f}",
        monitor="val/f1", mode="max", save_top_k=1,
    )
    early_stop = EarlyStopping(
        monitor="val/f1", mode="max", patience=patience,
    )

    trainer_p2 = pl.Trainer(
        max_epochs=phase2_epochs,
        accelerator="gpu",
        devices=1,
        precision=precision,
        callbacks=[ckpt_p2, early_stop],
        logger=csv_logger,
        enable_model_summary=False,
    )

    t1 = time.time()
    trainer_p2.fit(module, dm)
    p2_time = time.time() - t1

    total_time = p1_time + p2_time
    best_ckpt = ckpt_p2.best_model_path or ckpt_p1.best_model_path
    logger.info(
        "%s Phase 2 done: best_ckpt=%s (%.1f min total)",
        label, best_ckpt, total_time / 60,
    )

    # Test evaluation from best checkpoint
    logger.info("=== %s Test Evaluation ===", label)
    test_results = trainer_p2.test(module, dm, ckpt_path=best_ckpt)
    test_metrics = test_results[0] if test_results else {}

    return {
        "label": label,
        "best_checkpoint": str(best_ckpt),
        "p1_time_min": round(p1_time / 60, 1),
        "p2_time_min": round(p2_time / 60, 1),
        "total_time_min": round(total_time / 60, 1),
        "best_epoch_p1": ckpt_p1.best_model_path,
        "best_epoch_p2": ckpt_p2.best_model_path,
        "test/f1": round(test_metrics.get("test/f1", 0), 4),
        "test/acc": round(test_metrics.get("test/acc", 0), 4),
        "test/precision": round(test_metrics.get("test/precision", 0), 4),
        "test/recall": round(test_metrics.get("test/recall", 0), 4),
    }


def run_swin_rsp(dm: AerialWasteDataModule) -> dict:
    """A1: Swin-T RSP baseline."""
    label = "SwinT_RSP"

    module = WasteClassifierModule(
        model_cfg={
            "rsp_checkpoint_path": "checkpoints/rsp_swin_t_e300.pth",
            "num_classes": 1,
            "image_size": 224,
            "freeze_backbone": True,
            "drop_rate": 0.1,
        },
        lr=1e-3,
        training_phase="tl",
        weight_decay=0.05,
    )

    result = train_two_phase(module, dm, label, precision="16-mixed")

    # Inference time
    model = module.model
    infer_ms = measure_inference_time(model, (32, 3, 224, 224))
    n_params = sum(p.numel() for p in model.parameters())

    result["params_M"] = round(n_params / 1e6, 1)
    result["infer_ms"] = round(infer_ms, 1)
    result["precision"] = "16-mixed"
    return result


def run_ssl4eo(dm: AerialWasteDataModule) -> dict:
    """A2: SSL4EO ViT-S/16 with RGB bands."""
    label = "SSL4EO_ViTS16"

    model = SSL4EOClassifier(
        n_classes=1,
        band_indices=[3, 2, 1],  # B4(R), B3(G), B2(B)
        freeze_backbone=True,
        drop_head=0.1,
        pretrained=True,
    )

    module = MSClassifierModule(
        model=model,
        n_classes=2,
        lr=1e-3,
        training_phase="tl",
        weight_decay=0.05,
    )

    result = train_two_phase(module, dm, label, precision="16-mixed")

    # Inference time
    infer_ms = measure_inference_time(model, (32, 3, 224, 224))
    n_params = sum(p.numel() for p in model.parameters())

    result["params_M"] = round(n_params / 1e6, 1)
    result["infer_ms"] = round(infer_ms, 1)
    result["precision"] = "16-mixed"
    return result


def run_dofa(dm: AerialWasteDataModule) -> dict:
    """A3: DOFA ViT-B/16 with RGB wavelengths."""
    label = "DOFA_ViTB16"
    rgb_wavelengths = [665.0, 560.0, 490.0]

    model = DOFAClassifier(
        n_classes=1,
        wavelengths=rgb_wavelengths,
        freeze_backbone=True,
        drop_head=0.1,
        pretrained=True,
    )

    module = MSClassifierModule(
        model=model,
        n_classes=2,
        lr=1e-3,
        training_phase="tl",
        weight_decay=0.05,
        wavelengths=rgb_wavelengths,
    )

    # DOFA + AMP = NaN, use fp32
    result = train_two_phase(module, dm, label, precision=32)

    # Inference time (fp32)
    infer_ms = measure_inference_time(
        model, (32, 3, 224, 224), wavelengths=rgb_wavelengths,
    )
    n_params = sum(p.numel() for p in model.parameters())

    result["params_M"] = round(n_params / 1e6, 1)
    result["infer_ms"] = round(infer_ms, 1)
    result["precision"] = "fp32 (DOFA+AMP=NaN)"
    return result


def main() -> None:
    pl.seed_everything(42)

    dm = make_datamodule(image_size=224, batch_size=32)
    dm.setup("fit")
    dm.setup("test")

    logger.info("Dataset: %d train, %d val, %d test",
                len(dm.train_dataset), len(dm.val_dataset), len(dm.test_dataset))

    results = []

    # A1: Swin-T RSP
    try:
        r = run_swin_rsp(dm)
        results.append(r)
        logger.info("A1 done: test/F1=%.2f%%", r["test/f1"] * 100)
    except Exception as e:
        logger.error("A1 Swin-T RSP failed: %s", e, exc_info=True)

    # A2: SSL4EO ViT-S/16
    try:
        r = run_ssl4eo(dm)
        results.append(r)
        logger.info("A2 done: test/F1=%.2f%%", r["test/f1"] * 100)
    except Exception as e:
        logger.error("A2 SSL4EO failed: %s", e, exc_info=True)

    # A3: DOFA ViT-B/16
    try:
        r = run_dofa(dm)
        results.append(r)
        logger.info("A3 done: test/F1=%.2f%%", r["test/f1"] * 100)
    except Exception as e:
        logger.error("A3 DOFA failed: %s", e, exc_info=True)

    # Summary table
    logger.info("\n" + "=" * 80)
    logger.info("BACKBONE COMPARISON RESULTS")
    logger.info("=" * 80)
    logger.info("%-20s %8s %8s %8s %8s %8s %8s",
                "Backbone", "test/F1", "test/Acc", "Prec", "Recall", "Params", "Infer(ms)")
    logger.info("-" * 80)
    for r in results:
        logger.info(
            "%-20s %7.2f%% %7.2f%% %7.2f%% %7.2f%% %7.1fM %7.1fms",
            r["label"],
            r["test/f1"] * 100,
            r["test/acc"] * 100,
            r["test/precision"] * 100,
            r["test/recall"] * 100,
            r["params_M"],
            r["infer_ms"],
        )
    logger.info("=" * 80)

    # Save
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    logger.info("Results saved to %s", RESULTS_PATH)


if __name__ == "__main__":
    main()
