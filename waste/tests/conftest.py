"""Shared test fixtures — synthetic data for smoke tests without full dataset."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import numpy as np
import pytest
from PIL import Image


@pytest.fixture
def synthetic_dataset(tmp_path: Path) -> Path:
    """Create a minimal synthetic AerialWaste-like dataset for smoke tests.

    Returns the dataset root path.
    """
    images_dir = tmp_path / "images"
    images_dir.mkdir()

    rng = np.random.default_rng(42)
    samples = []

    for i in range(20):
        is_positive = i < 7  # ~1:2 ratio
        fname = f"agea_tile_{i:04d}.png"

        # Create random RGB image (varying sizes like real dataset)
        h, w = int(rng.integers(200, 600)), int(rng.integers(200, 600))
        arr = rng.integers(0, 255, size=(h, w, 3), dtype=np.uint8)
        if not is_positive:
            # Negative images tend to be more uniform (fields, etc.)
            arr = (arr * 0.3 + 128).astype(np.uint8)

        img = Image.fromarray(arr)
        img.save(images_dir / fname)

        sample = {
            "id": i,
            "file_name": fname,
            "is_candidate_location": 1 if is_positive else 0,
            "width": int(w),
            "height": int(h),
        }
        if is_positive and i < 3:
            # Categories are integer IDs (1-indexed, matching COCO style)
            sample["categories"] = [1, 2, 16]  # Rubble, Bulky items, Heaps not delimited
        samples.append(sample)

    # Split: 14 train, 6 test
    train_samples = {"images": samples[:14]}
    test_samples = {"images": samples[14:]}

    with open(tmp_path / "training.json", "w") as f:
        json.dump(train_samples, f)
    with open(tmp_path / "testing.json", "w") as f:
        json.dump(test_samples, f)

    return tmp_path
