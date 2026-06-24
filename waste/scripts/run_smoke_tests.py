"""End-to-end smoke tests for multispectral foundation models.

Runs 3 epochs (phase 1 only) for each model/band/data combination:

  Model             | Bands        | Data
  ------------------|--------------|------------------
  SSL4EOClassifier  | all 13       | synthetic_ms
  SSL4EOClassifier  | [3,2,1]      | synthetic_ms (RGB-equiv)
  DOFAClassifier    | all 13       | synthetic_ms
  SwinRSP (existing)| 3            | real AerialWaste RGB

Success criteria:
  - No runtime errors
  - val/F1 > 0.50 after 3 epochs
  - 13-band SSL4EO val/F1 > RGB-equiv SSL4EO
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import pytorch_lightning as pl
import torch

from waste_detection.data.synthetic_ms_dm import SyntheticMSDataModule
from waste_detection.models.ssl4eo_classifier import SSL4EOClassifier
from waste_detection.models.dofa_classifier import DOFAClassifier, S2_ALL_WAVELENGTHS
from waste_detection.training.ms_module import MSClassifierModule

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s][%(levelname)s] - %(message)s",
)
logger = logging.getLogger(__name__)


def run_ssl4eo_smoke(
    band_indices: list[int] | None,
    label: str,
    dm: SyntheticMSDataModule,
    max_epochs: int = 3,
) -> dict:
    """Run SSL4EO smoke test."""
    logger.info("=== %s ===", label)
    n_bands = len(band_indices) if band_indices is not None else 13

    model = SSL4EOClassifier(
        n_classes=1,  # binary
        band_indices=band_indices,
        freeze_backbone=False,  # unfreeze for smoke test (3 epochs)
        drop_head=0.1,
        pretrained=True,
    )

    module = MSClassifierModule(
        model=model,
        n_classes=2,  # binary internally
        lr=1e-3,
        training_phase="tl",
    )

    trainer = pl.Trainer(
        max_epochs=max_epochs,
        accelerator="gpu" if torch.cuda.is_available() else "cpu",
        devices=1,
        precision="16-mixed" if torch.cuda.is_available() else 32,
        enable_checkpointing=False,
        enable_model_summary=False,
        logger=False,
    )

    t0 = time.time()
    trainer.fit(module, dm)
    elapsed = time.time() - t0

    # Get final val metrics
    val_results = trainer.callback_metrics
    val_f1 = val_results.get("val/f1", torch.tensor(0)).item()
    val_acc = val_results.get("val/acc", torch.tensor(0)).item()

    result = {
        "model": "SSL4EOClassifier",
        "label": label,
        "bands": n_bands,
        "band_indices": band_indices,
        "val_f1": round(val_f1, 4),
        "val_acc": round(val_acc, 4),
        "elapsed_s": round(elapsed, 1),
        "pass": val_f1 > 0.50,
    }
    logger.info(
        "✓ %s — val/F1=%.2f%%  val/Acc=%.2f%%  (%.1fs)",
        label, val_f1 * 100, val_acc * 100, elapsed,
    )
    return result


def run_dofa_smoke(
    dm: SyntheticMSDataModule,
    max_epochs: int = 3,
) -> dict:
    """Run DOFA smoke test."""
    label = "DOFA_all13"
    logger.info("=== %s ===", label)

    model = DOFAClassifier(
        n_classes=1,  # binary
        wavelengths=[float(w) for w in S2_ALL_WAVELENGTHS],
        freeze_backbone=False,  # unfreeze for smoke test
        drop_head=0.1,
        pretrained=True,
    )

    module = MSClassifierModule(
        model=model,
        n_classes=2,
        lr=1e-3,
        training_phase="tl",
        wavelengths=[float(w) for w in S2_ALL_WAVELENGTHS],
    )

    # DOFA + AMP causes NaN — use fp32
    trainer = pl.Trainer(
        max_epochs=max_epochs,
        accelerator="gpu" if torch.cuda.is_available() else "cpu",
        devices=1,
        precision=32,
        enable_checkpointing=False,
        enable_model_summary=False,
        logger=False,
    )

    t0 = time.time()
    trainer.fit(module, dm)
    elapsed = time.time() - t0

    val_results = trainer.callback_metrics
    val_f1 = val_results.get("val/f1", torch.tensor(0)).item()
    val_acc = val_results.get("val/acc", torch.tensor(0)).item()

    result = {
        "model": "DOFAClassifier",
        "label": label,
        "bands": 13,
        "wavelengths": S2_ALL_WAVELENGTHS,
        "val_f1": round(val_f1, 4),
        "val_acc": round(val_acc, 4),
        "elapsed_s": round(elapsed, 1),
        "pass": val_f1 > 0.50,
    }
    logger.info(
        "✓ %s — val/F1=%.2f%%  val/Acc=%.2f%%  (%.1fs)",
        label, val_f1 * 100, val_acc * 100, elapsed,
    )
    return result


def run_swin_rsp_smoke(max_epochs: int = 3) -> dict:
    """Run existing SwinRSP on real AerialWaste RGB."""
    from waste_detection.data.aerialwaste_dm import AerialWasteDataModule
    from waste_detection.training.lightning_module import WasteClassifierModule

    label = "SwinRSP_RGB_real"
    logger.info("=== %s ===", label)

    dm = AerialWasteDataModule(
        root="data/raw",
        image_size=224,  # smaller for smoke test speed
        target_gsd=None,  # skip GSD normalization for speed
        batch_size=32,
        num_workers=4,
        val_fraction=0.15,
    )

    module = WasteClassifierModule(
        model_cfg={
            "pretrained_imagenet": True,
            "num_classes": 1,
            "image_size": 224,
            "freeze_backbone": True,
            "drop_rate": 0.1,
        },
        lr=1e-3,
        training_phase="tl",
    )

    trainer = pl.Trainer(
        max_epochs=max_epochs,
        accelerator="gpu" if torch.cuda.is_available() else "cpu",
        devices=1,
        precision="16-mixed" if torch.cuda.is_available() else 32,
        enable_checkpointing=False,
        enable_model_summary=False,
        logger=False,
    )

    t0 = time.time()
    trainer.fit(module, dm)
    elapsed = time.time() - t0

    val_results = trainer.callback_metrics
    val_f1 = val_results.get("val/f1", torch.tensor(0)).item()
    val_acc = val_results.get("val/acc", torch.tensor(0)).item()

    result = {
        "model": "SwinRSP",
        "label": label,
        "bands": 3,
        "data": "AerialWaste_RGB",
        "val_f1": round(val_f1, 4),
        "val_acc": round(val_acc, 4),
        "elapsed_s": round(elapsed, 1),
        "pass": val_f1 > 0.50,
    }
    logger.info(
        "✓ %s — val/F1=%.2f%%  val/Acc=%.2f%%  (%.1fs)",
        label, val_f1 * 100, val_acc * 100, elapsed,
    )
    return result


def main() -> None:
    results = []

    # Setup synthetic data modules
    dm_all13 = SyntheticMSDataModule(
        root="data/synthetic_ms",
        band_indices=None,
        img_size=224,
        batch_size=32,
        num_workers=4,
    )
    dm_all13.setup()

    dm_rgb = SyntheticMSDataModule(
        root="data/synthetic_ms",
        band_indices=[3, 2, 1],
        img_size=224,
        batch_size=32,
        num_workers=4,
    )
    dm_rgb.setup()

    # 1. SSL4EO all 13 bands
    results.append(run_ssl4eo_smoke(None, "SSL4EO_all13", dm_all13))

    # 2. SSL4EO RGB equivalent
    results.append(run_ssl4eo_smoke([3, 2, 1], "SSL4EO_RGB", dm_rgb))

    # 3. DOFA all 13 bands
    results.append(run_dofa_smoke(dm_all13))

    # 4. SwinRSP on real AerialWaste RGB
    results.append(run_swin_rsp_smoke())

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("SMOKE TEST RESULTS")
    logger.info("=" * 70)
    all_pass = True
    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        if not r["pass"]:
            all_pass = False
        logger.info(
            "  %-25s %dch  val/F1=%.2f%%  %s  (%.1fs)",
            r["label"], r["bands"], r["val_f1"] * 100, status, r["elapsed_s"],
        )

    # Check: 13-band SSL4EO > RGB SSL4EO
    ssl4eo_all = next(r for r in results if r["label"] == "SSL4EO_all13")
    ssl4eo_rgb = next(r for r in results if r["label"] == "SSL4EO_RGB")
    ms_gt_rgb = ssl4eo_all["val_f1"] > ssl4eo_rgb["val_f1"]
    logger.info(
        "\n  13-band > RGB: %s (%.2f%% vs %.2f%%)",
        "YES" if ms_gt_rgb else "NO",
        ssl4eo_all["val_f1"] * 100,
        ssl4eo_rgb["val_f1"] * 100,
    )

    # Save results
    output_path = Path("data/processed/smoke_test_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    logger.info("\nResults saved to %s", output_path)

    if all_pass:
        logger.info("All smoke tests PASSED!")
    else:
        logger.warning("Some smoke tests FAILED!")


if __name__ == "__main__":
    main()
