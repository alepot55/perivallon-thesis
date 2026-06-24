#!/usr/bin/env python3
"""Download and validate the AerialWaste v3 dataset from Zenodo.

Zenodo record: https://zenodo.org/records/7034382
DOI: 10.5281/zenodo.7034382

Downloads ~18 GB of imagery (6 zip files) plus metadata JSONs.
After download, validates file integrity and computes dataset statistics.

Usage:
    python scripts/download_data.py [--output-dir data/raw] [--skip-images]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

ZENODO_RECORD = "7034382"
BASE_URL = f"https://zenodo.org/api/records/{ZENODO_RECORD}/files"

FILES = {
    "training.json": {"md5": "18b32c383683d194177a36a51b8e236b", "size": 2_928_668},
    "testing.json": {"md5": "6af2da456dbd6232c9051b2d15dd4cca", "size": 1_696_233},
    "images0.zip": {"md5": "99a48ac4a23b58266d8ec678bc587077", "size": 3_001_893_566},
    "images1.zip": {"md5": "0f9bb21f6b19e0a05638ac42f5e49fab", "size": 3_020_482_162},
    "images2.zip": {"md5": "768a21b031bed9f521372eb17152fb39", "size": 3_023_663_123},
    "images3.zip": {"md5": "c59f2bc03be6912ddf2f1bad0b6c3c39", "size": 3_017_472_956},
    "images4.zip": {"md5": "9ab464610b6a807a16148122c82fdc9d", "size": 3_030_975_980},
    "images5.zip": {"md5": "24d66b1c156610baedd092bb24766380", "size": 2_988_101_490},
}

# RSP Swin-T checkpoint
RSP_GDRIVE_ID = "1G5wjbjIHepmT6VVOuW03bWmyvrhcfe1F"
RSP_FILENAME = "rsp_swin_t_e300.pth"


def md5sum(filepath: Path, chunk_size: int = 8192) -> str:
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def download_progress(block_num: int, block_size: int, total_size: int) -> None:
    downloaded = block_num * block_size
    if total_size > 0:
        pct = min(100.0, downloaded / total_size * 100)
        mb = downloaded / 1e6
        total_mb = total_size / 1e6
        print(f"\r  {mb:.1f}/{total_mb:.1f} MB ({pct:.1f}%)", end="", flush=True)


def download_file(name: str, output_dir: Path) -> Path:
    url = f"{BASE_URL}/{name}/content"
    dest = output_dir / name
    if dest.exists() and dest.stat().st_size == FILES[name]["size"]:
        logger.info("Skipping %s (already exists with correct size)", name)
        return dest
    logger.info("Downloading %s ...", name)
    urlretrieve(url, dest, reporthook=download_progress)
    print()  # newline after progress
    return dest


def validate_file(filepath: Path, expected_md5: str) -> bool:
    actual = md5sum(filepath)
    if actual != expected_md5:
        logger.error("MD5 mismatch for %s: expected %s, got %s", filepath.name, expected_md5, actual)
        return False
    logger.info("MD5 OK: %s", filepath.name)
    return True


def extract_images(output_dir: Path) -> None:
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)
    for name in sorted(FILES):
        if not name.endswith(".zip"):
            continue
        zip_path = output_dir / name
        logger.info("Extracting %s ...", name)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(images_dir)
    logger.info("All images extracted to %s", images_dir)


def compute_dataset_stats(output_dir: Path, processed_dir: Path) -> dict:
    """Compute and save dataset statistics."""
    stats: dict = {"splits": {}}

    for split_name, json_name in [("train", "training.json"), ("test", "testing.json")]:
        json_path = output_dir / json_name
        with open(json_path) as f:
            metadata = json.load(f)

        items = metadata.get("images", metadata) if isinstance(metadata, dict) else metadata
        total = len(items)
        positives = sum(1 for it in items if it.get("is_candidate_location", 0) == 1)
        negatives = total - positives

        # Source distribution (using img_source field)
        sources: dict[str, int] = {}
        for it in items:
            src = it.get("img_source", "unknown")
            sources[src] = sources.get(src, 0) + 1

        # Build category ID→name mapping from JSON
        cat_map = {}
        if isinstance(metadata, dict) and "categories" in metadata:
            for c in metadata["categories"]:
                cat_map[c["id"]] = c["name"]

        # Multi-class distribution (categories are integer IDs)
        category_counts: dict[str, int] = {}
        for it in items:
            for cat_id in it.get("categories", []):
                cat_name = cat_map.get(cat_id, f"unknown_{cat_id}")
                category_counts[cat_name] = category_counts.get(cat_name, 0) + 1

        stats["splits"][split_name] = {
            "total": total,
            "positive": positives,
            "negative": negatives,
            "ratio_neg_pos": round(negatives / max(positives, 1), 2),
            "sources": sources,
            "category_counts": dict(sorted(category_counts.items(), key=lambda x: -x[1])),
        }

    stats["total_images"] = sum(s["total"] for s in stats["splits"].values())

    # Compute channel stats if images are available
    images_dir = output_dir / "images"
    if images_dir.exists() and any(images_dir.iterdir()):
        logger.info("Computing per-channel statistics (sampling up to 2000 images)...")
        stats["channel_stats"] = _compute_channel_stats(output_dir, max_samples=2000)
    else:
        logger.warning("Images not found — skipping channel statistics")
        stats["channel_stats"] = None

    processed_dir.mkdir(parents=True, exist_ok=True)
    stats_path = processed_dir / "dataset_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    logger.info("Dataset stats saved to %s", stats_path)

    return stats


def _compute_channel_stats(output_dir: Path, max_samples: int = 2000) -> dict:
    """Compute RGB mean/std by iterating over dataset images."""
    from PIL import Image

    json_path = output_dir / "training.json"
    with open(json_path) as f:
        metadata = json.load(f)
    items = metadata.get("images", metadata) if isinstance(metadata, dict) else metadata

    rng = np.random.default_rng(42)
    indices = rng.choice(len(items), size=min(max_samples, len(items)), replace=False)

    channel_sum = np.zeros(3, dtype=np.float64)
    channel_sq_sum = np.zeros(3, dtype=np.float64)
    pixel_count = 0
    corrupt_files: list[str] = []

    images_dir = output_dir / "images"
    for i in indices:
        img_path = images_dir / items[i]["file_name"]
        try:
            img = Image.open(img_path).convert("RGB")
            arr = np.asarray(img, dtype=np.float64) / 255.0  # [H, W, 3]
            channel_sum += arr.sum(axis=(0, 1))
            channel_sq_sum += (arr**2).sum(axis=(0, 1))
            pixel_count += arr.shape[0] * arr.shape[1]

            # Check for zero-variance (corrupt) images
            if arr.std() < 1e-6:
                corrupt_files.append(items[i]["file_name"])
        except Exception as e:
            corrupt_files.append(f"{items[i]['file_name']} (error: {e})")

    mean = channel_sum / pixel_count
    std = np.sqrt(channel_sq_sum / pixel_count - mean**2)

    return {
        "mean": mean.tolist(),
        "std": std.tolist(),
        "sampled_images": int(len(indices)),
        "corrupt_or_zero_variance": corrupt_files,
    }


def download_rsp_checkpoint(output_dir: Path) -> None:
    """Download RSP Swin-T checkpoint from Google Drive."""
    dest = output_dir / RSP_FILENAME
    if dest.exists():
        logger.info("RSP checkpoint already exists: %s", dest)
        return

    logger.info("Downloading RSP Swin-T checkpoint from Google Drive...")
    # gdown handles Google Drive large files with confirmation
    try:
        import gdown
        gdown.download(id=RSP_GDRIVE_ID, output=str(dest), quiet=False)
    except ImportError:
        url = f"https://drive.google.com/uc?id={RSP_GDRIVE_ID}&export=download"
        logger.warning(
            "gdown not installed. Download RSP weights manually:\n"
            "  pip install gdown && gdown %s -O %s\n"
            "  Or download from: %s",
            RSP_GDRIVE_ID, dest, url,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Download AerialWaste v3 dataset")
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--checkpoint-dir", type=Path, default=Path("checkpoints"))
    parser.add_argument("--skip-images", action="store_true", help="Download only metadata JSONs")
    parser.add_argument("--skip-extract", action="store_true", help="Skip zip extraction")
    parser.add_argument("--skip-validate", action="store_true", help="Skip MD5 validation")
    parser.add_argument("--download-rsp", action="store_true", help="Also download RSP weights")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # Download files
    for name, info in FILES.items():
        if args.skip_images and name.endswith(".zip"):
            continue
        filepath = download_file(name, args.output_dir)
        if not args.skip_validate:
            validate_file(filepath, info["md5"])

    # Extract
    if not args.skip_images and not args.skip_extract:
        extract_images(args.output_dir)

    # Compute stats
    stats = compute_dataset_stats(args.output_dir, args.processed_dir)

    # Print summary
    for split_name, split_stats in stats["splits"].items():
        logger.info(
            "%s: %d total (%d pos, %d neg, ratio %.1f:1)",
            split_name,
            split_stats["total"],
            split_stats["positive"],
            split_stats["negative"],
            split_stats["ratio_neg_pos"],
        )

    # RSP checkpoint
    if args.download_rsp:
        download_rsp_checkpoint(args.checkpoint_dir)

    logger.info("Done!")


if __name__ == "__main__":
    main()
