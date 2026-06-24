"""Generate synthetic 13-band multispectral patches for pipeline validation.

Creates N patches at 64×64 pixels, 13 bands (Sentinel-2 layout), float32.
Statistical structure approximates real spectral signatures:
  - VIS (B2-B4): from AerialWaste RGB channel stats
  - Red Edge (B5-B7): VIS * (1.1 + 0.2 * noise)
  - NIR (B8, B8A): spectrally coherent with vegetation/soil response
  - Water vapor (B9), Cirrus (B10): near-zero + high noise
  - SWIR1 (B11): key discriminator (waste: 0.25±0.05, no-waste: 0.12±0.04)
  - SWIR2 (B12): 0.85 * B11 + noise

Binary label: positive if B11_mean > 0.18 (~35% positive rate).
22-class label: assigned proportionally to AerialWaste class distribution.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_bounds

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# AerialWaste RGB stats (from dataset_stats.json)
RGB_MEAN = [0.320, 0.336, 0.280]
RGB_STD = [0.188, 0.167, 0.166]

# AerialWaste 22-class distribution (from training.json, normalized)
CLASS_DISTRIBUTION = {
    1: 228, 2: 242, 3: 135, 4: 140, 5: 102, 6: 27, 7: 32,
    8: 19, 9: 21, 10: 15, 11: 8, 12: 12, 13: 9, 14: 10,
    15: 6, 16: 355, 17: 113, 18: 31, 19: 43, 20: 38, 21: 26, 22: 16,
}

CLASS_NAMES = {
    1: "Rubble/excavated earth and rocks", 2: "Bulky items",
    3: "Fire Wood", 4: "Scrap", 5: "Plastic", 6: "Vehicles",
    7: "Tires", 8: "Domestic appliances", 9: "Paper",
    10: "Sludge-Zootechnical waste-Manure", 11: "Foundry waste",
    12: "Stone/marble processing waste", 13: "Asphalt milling",
    14: "Corrugated sheets (asbestos-cement)", 15: "Glass",
    16: "Heaps not delimited", 17: "Full container", 18: "Big bags",
    19: "Full pallets", 20: "Delimited heaps", 21: "Cisterns",
    22: "Drums bins",
}


def generate_patch(
    rng: np.random.Generator,
    is_waste: bool,
    h: int = 64,
    w: int = 64,
) -> np.ndarray:
    """Generate a single 13-band patch.

    Returns array of shape (13, h, w) in float32.
    """
    patch = np.zeros((13, h, w), dtype=np.float32)

    # B1 (Coastal aerosol, 443nm) — low signal
    patch[0] = rng.normal(0.05, 0.02, (h, w))

    # B2 (Blue, 490nm), B3 (Green, 560nm), B4 (Red, 665nm)
    for i, (mu, sigma) in enumerate(zip(RGB_MEAN, RGB_STD)):
        patch[i + 1] = rng.normal(mu, sigma, (h, w))

    # B5-B7 (Red Edge, 705-783nm): VIS_red * scale
    for i in range(4, 7):
        scale = 1.1 + 0.2 * rng.standard_normal((h, w))
        patch[i] = patch[3] * scale  # scale from B4 (Red)

    # B8 (NIR, 842nm), B8A (NIR narrow, 865nm)
    if is_waste:
        nir_scale = 1.2 + 0.3 * rng.standard_normal((h, w))
    else:
        nir_scale = 2.0 + 0.5 * rng.standard_normal((h, w))
    patch[7] = patch[3] * nir_scale
    patch[8] = patch[7] * (1.0 + 0.05 * rng.standard_normal((h, w)))

    # B9 (Water vapour, 940nm) — near zero
    patch[9] = rng.normal(0.01, 0.005, (h, w))

    # B10 (Cirrus, 1375nm) — near zero
    patch[10] = rng.normal(0.005, 0.003, (h, w))

    # B11 (SWIR1, 1610nm) — KEY DISCRIMINATOR
    if is_waste:
        patch[11] = rng.normal(0.25, 0.05, (h, w))
    else:
        patch[11] = rng.normal(0.12, 0.04, (h, w))

    # B12 (SWIR2, 2190nm): correlated with B11
    patch[12] = 0.85 * patch[11] + rng.normal(0.0, 0.02, (h, w))

    # Clamp to valid reflectance range
    return np.clip(patch, 0.0, 1.0)


def generate_dataset(
    output_dir: str | Path,
    n_samples: int = 1000,
    seed: int = 42,
) -> None:
    """Generate the full synthetic MS dataset."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(seed)

    # Compute class probabilities from AerialWaste distribution
    total_cat = sum(CLASS_DISTRIBUTION.values())
    class_probs = {k: v / total_cat for k, v in CLASS_DISTRIBUTION.items()}
    cat_ids = list(class_probs.keys())
    cat_weights = [class_probs[k] for k in cat_ids]

    # Target ~35% waste positive rate
    labels = []
    for i in range(n_samples):
        patch_b11_mean_target = rng.normal(
            0.25 if rng.random() < 0.35 else 0.12,
            0.02,
        )
        is_waste = patch_b11_mean_target > 0.18

        patch = generate_patch(rng, is_waste)

        # Save as GeoTIFF (synthetic coords around 0,0)
        tif_path = output_dir / f"{i:05d}_bands.tif"
        transform = from_bounds(0, 0, 640, 640, 64, 64)
        with rasterio.open(
            tif_path, "w",
            driver="GTiff",
            height=64, width=64, count=13,
            dtype="float32",
            crs="EPSG:32632",
            transform=transform,
        ) as dst:
            for band in range(13):
                dst.write(patch[band], band + 1)

        # Assign multi-class label
        if is_waste:
            category_id = rng.choice(cat_ids, p=cat_weights)
            category_name = CLASS_NAMES[category_id]
        else:
            category_id = 0
            category_name = "no_waste"

        label_data = {
            "binary": int(is_waste),
            "category_id": int(category_id),
            "category": category_name,
        }
        label_path = output_dir / f"{i:05d}_label.json"
        with open(label_path, "w") as f:
            json.dump(label_data, f)

        labels.append(label_data)

    # Summary
    n_pos = sum(1 for l in labels if l["binary"] == 1)
    n_neg = n_samples - n_pos
    logger.info(
        "Generated %d synthetic patches: %d positive (%.1f%%), %d negative",
        n_samples, n_pos, 100 * n_pos / n_samples, n_neg,
    )

    # Save manifest
    manifest = {
        "n_samples": n_samples,
        "n_positive": n_pos,
        "n_negative": n_neg,
        "bands": 13,
        "height": 64,
        "width": 64,
        "seed": seed,
    }
    with open(output_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    logger.info("Saved manifest to %s", output_dir / "manifest.json")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate synthetic MS patches")
    parser.add_argument("--output-dir", default="data/synthetic_ms", help="Output directory")
    parser.add_argument("--n-samples", type=int, default=1000, help="Number of patches")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    generate_dataset(args.output_dir, args.n_samples, args.seed)
