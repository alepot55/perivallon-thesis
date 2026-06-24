#!/usr/bin/env python3
"""Compute per-channel statistics over the AerialWaste v3 training split.

Computes:
  - Per-channel (RGB) mean and std (for normalization)
  - Per-channel 1st and 99th percentiles (for visualization clipping)

Uses rasterio for memory-efficient windowed/tiled reading — images are
processed in tiles rather than loading full images into RAM.

Usage:
    python scripts/compute_channel_stats.py [--data-dir data/raw] [--output data/processed/dataset_stats.json]
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import Window

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TILE_SIZE = 512  # Read images in tiles of this size


def compute_stats(
    data_dir: Path,
    max_samples: int = 0,
    tile_size: int = TILE_SIZE,
    percentile_reservoir_size: int = 5_000_000,
) -> dict:
    """Compute per-channel mean, std, and percentiles over the training split.

    Uses Welford-style online accumulation for mean/std (exact) and
    reservoir sampling for percentiles (approximate but memory-bounded).

    Args:
        data_dir: Path to dataset root (containing training.json and images/).
        max_samples: Max images to process (0 = all).
        tile_size: Tile size for windowed reading.
        percentile_reservoir_size: Max pixels to keep in reservoir for percentile estimation.

    Returns:
        Dict with mean, std, percentiles_1, percentiles_99 (3-element lists for RGB).
    """
    json_path = data_dir / "training.json"
    if not json_path.exists():
        logger.error("training.json not found at %s", json_path)
        sys.exit(1)

    with open(json_path) as f:
        metadata = json.load(f)
    items = metadata.get("images", metadata) if isinstance(metadata, dict) else metadata

    images_dir = data_dir / "images"
    if not images_dir.exists():
        logger.error("Images directory not found at %s", images_dir)
        sys.exit(1)

    rng = np.random.default_rng(42)
    indices = list(range(len(items)))
    if max_samples > 0:
        indices = rng.choice(indices, size=min(max_samples, len(indices)), replace=False).tolist()

    # Accumulators for mean/std (Welford online)
    channel_sum = np.zeros(3, dtype=np.float64)
    channel_sq_sum = np.zeros(3, dtype=np.float64)
    pixel_count = 0

    # Reservoir for percentile estimation
    reservoir = [np.empty(0, dtype=np.float32) for _ in range(3)]
    reservoir_count = 0
    per_channel_reservoir_size = percentile_reservoir_size // 3

    errors: list[str] = []
    n_total = len(indices)

    for progress_idx, i in enumerate(indices):
        item = items[i]
        img_path = images_dir / item["file_name"]

        if progress_idx % 500 == 0:
            logger.info("Processing %d/%d (%.0f%%)", progress_idx, n_total, progress_idx / n_total * 100)

        try:
            with rasterio.open(img_path) as src:
                h, w = src.height, src.width
                n_bands = min(src.count, 3)  # Use first 3 bands (RGB)

                # Process in tiles
                for row_off in range(0, h, tile_size):
                    for col_off in range(0, w, tile_size):
                        win_h = min(tile_size, h - row_off)
                        win_w = min(tile_size, w - col_off)
                        window = Window(col_off, row_off, win_w, win_h)

                        # Read tile: shape (bands, win_h, win_w)
                        tile = src.read(
                            indexes=list(range(1, n_bands + 1)),
                            window=window,
                        ).astype(np.float64) / 255.0

                        n_pixels = win_h * win_w

                        # Accumulate for mean/std
                        for c in range(n_bands):
                            channel_data = tile[c]
                            channel_sum[c] += channel_data.sum()
                            channel_sq_sum[c] += (channel_data ** 2).sum()

                        pixel_count += n_pixels

                        # Reservoir sampling for percentiles
                        for c in range(n_bands):
                            flat = tile[c].ravel().astype(np.float32)
                            if len(reservoir[c]) < per_channel_reservoir_size:
                                reservoir[c] = np.concatenate([reservoir[c], flat])
                                if len(reservoir[c]) > per_channel_reservoir_size:
                                    # Trim to size
                                    idx = rng.choice(len(reservoir[c]), size=per_channel_reservoir_size, replace=False)
                                    reservoir[c] = reservoir[c][idx]
                            else:
                                # Reservoir sampling: replace with decreasing probability
                                reservoir_count_c = len(reservoir[c])
                                for val in flat[rng.choice(len(flat), size=min(100, len(flat)), replace=False)]:
                                    j = rng.integers(0, reservoir_count_c + 1)
                                    if j < per_channel_reservoir_size:
                                        reservoir[c][j] = val

        except Exception as e:
            errors.append(f"{item['file_name']}: {e}")
            continue

    if pixel_count == 0:
        logger.error("No pixels processed — check image paths")
        sys.exit(1)

    # Compute final statistics
    mean = channel_sum / pixel_count
    std = np.sqrt(channel_sq_sum / pixel_count - mean ** 2)

    # Percentiles from reservoir
    percentiles_1 = [float(np.percentile(reservoir[c], 1)) for c in range(3)]
    percentiles_99 = [float(np.percentile(reservoir[c], 99)) for c in range(3)]

    logger.info("Processed %d images, %d total pixels", n_total - len(errors), pixel_count)
    if errors:
        logger.warning("%d errors encountered", len(errors))
        for e in errors[:5]:
            logger.warning("  %s", e)

    return {
        "mean": mean.tolist(),
        "std": std.tolist(),
        "percentiles_1": percentiles_1,
        "percentiles_99": percentiles_99,
        "sampled_images": n_total - len(errors),
        "total_pixels": pixel_count,
        "errors": errors[:10],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute AerialWaste channel statistics")
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/dataset_stats.json"))
    parser.add_argument("--max-samples", type=int, default=0, help="Max images (0=all)")
    parser.add_argument("--tile-size", type=int, default=TILE_SIZE)
    args = parser.parse_args()

    logger.info("Computing channel statistics over training split...")
    stats = compute_stats(args.data_dir, args.max_samples, args.tile_size)

    # Update existing stats file if present
    output_path = args.output
    existing = {}
    if output_path.exists():
        with open(output_path) as f:
            existing = json.load(f)

    existing["channel_stats"] = stats
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(existing, f, indent=2)

    logger.info("Results saved to %s", output_path)
    logger.info("  mean = [%.4f, %.4f, %.4f]", *stats["mean"])
    logger.info("  std  = [%.4f, %.4f, %.4f]", *stats["std"])
    logger.info("  p1   = [%.4f, %.4f, %.4f]", *stats["percentiles_1"])
    logger.info("  p99  = [%.4f, %.4f, %.4f]", *stats["percentiles_99"])


if __name__ == "__main__":
    main()
