"""AerialWaste v3 dataset wrapper compatible with TorchGeo conventions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms as T


# 22 fine-grained waste categories from AerialWaste v3 (COCO-style, 1-indexed)
# Supercategory: Type_of_object (1-15) + Storage_mode (16-22)
WASTE_CATEGORIES: dict[int, str] = {
    1: "Rubble/excavated earth and rocks",
    2: "Bulky items",
    3: "Fire Wood",
    4: "Scrap",
    5: "Plastic",
    6: "Vehicles",
    7: "Tires",
    8: "Domestic appliances",
    9: "Paper",
    10: "Sludge-Zootechnical waste-Manure",
    11: "Foundry waste",
    12: "Stone/marble processing waste",
    13: "Asphalt milling",
    14: "Corrugated sheets (presumed asbestos-cement)",
    15: "Glass",
    16: "Heaps not delimited",
    17: "Full container",
    18: "Big bags",
    19: "Full pallets",
    20: "Delimited heaps (by barriers/walls/etc)",
    21: "Cisterns",
    22: "Drums bins",
}

NUM_CATEGORIES = len(WASTE_CATEGORIES)

# Source → GSD mapping
SOURCE_GSD: dict[str, int] = {
    "AGEA": 20,
    "WV3": 30,
    "GE": 50,
}


class AerialWasteDataset(Dataset):
    """AerialWaste v3 scene classification dataset.

    Loads images and binary labels (waste / no-waste) from the AerialWaste
    COCO-style JSON metadata.  Optionally returns multi-class labels for the
    22 waste categories.

    Args:
        root: Path to the dataset root containing ``images/`` and JSON files.
        split: ``"train"`` or ``"test"``.
        transform: Optional torchvision transform applied to PIL images.
        target_gsd: If set, filter to images from sources matching this GSD
            (20, 30, or 50 cm/px).  ``None`` keeps all sources.
        multiclass: If True, also return a 22-dim multi-label vector.
    """

    def __init__(
        self,
        root: str | Path,
        split: str = "train",
        transform: Any | None = None,
        target_gsd: int | None = None,
        multiclass: bool = False,
    ) -> None:
        self.root = Path(root)
        self.split = split
        self.transform = transform
        self.target_gsd = target_gsd
        self.multiclass = multiclass

        json_name = "training.json" if split == "train" else "testing.json"
        json_path = self.root / json_name
        if not json_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {json_path}")

        with open(json_path) as f:
            metadata = json.load(f)

        # Parse COCO-style category mapping if present
        self.category_map: dict[int, str] = {}
        if isinstance(metadata, dict) and "categories" in metadata:
            for cat in metadata["categories"]:
                self.category_map[cat["id"]] = cat["name"]
        if not self.category_map:
            self.category_map = dict(WASTE_CATEGORIES)

        self.images_dir = self.root / "images"
        self.samples: list[dict] = []

        items = metadata.get("images", metadata) if isinstance(metadata, dict) else metadata
        for item in items:
            if target_gsd is not None:
                source = item.get("img_source", "")
                source_gsd = SOURCE_GSD.get(source)
                if source_gsd is not None and source_gsd != target_gsd:
                    continue
            self.samples.append(item)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> dict[str, Any]:
        item = self.samples[idx]
        img_path = self.images_dir / item["file_name"]
        image = Image.open(img_path).convert("RGB")

        if self.transform is not None:
            image = self.transform(image)
        elif not isinstance(image, torch.Tensor):
            image = T.ToTensor()(image)

        binary_label = torch.tensor(
            item.get("is_candidate_location", 0), dtype=torch.float32
        )

        sample = {
            "image": image,
            "label": binary_label,
            "file_name": item["file_name"],
        }

        if self.multiclass:
            cat_ids = item.get("categories", [])
            multi_label = torch.zeros(NUM_CATEGORIES, dtype=torch.float32)
            for cat_id in cat_ids:
                if isinstance(cat_id, int) and 1 <= cat_id <= NUM_CATEGORIES:
                    multi_label[cat_id - 1] = 1.0  # 1-indexed → 0-indexed
            sample["multi_label"] = multi_label

        return sample

    def get_class_distribution(self) -> dict[str, int]:
        """Count samples per binary class."""
        pos = sum(1 for s in self.samples if s.get("is_candidate_location", 0) == 1)
        return {"waste": pos, "no_waste": len(self.samples) - pos}

    def get_source_distribution(self) -> dict[str, int]:
        """Count samples per image source."""
        sources: dict[str, int] = {}
        for s in self.samples:
            src = s.get("img_source", "unknown")
            sources[src] = sources.get(src, 0) + 1
        return sources

    def get_category_distribution(self) -> dict[str, int]:
        """Count occurrences of each waste category."""
        counts: dict[str, int] = {}
        for s in self.samples:
            for cat_id in s.get("categories", []):
                name = self.category_map.get(cat_id, f"unknown_{cat_id}")
                counts[name] = counts.get(name, 0) + 1
        return dict(sorted(counts.items(), key=lambda x: -x[1]))

    def compute_channel_stats(self, max_samples: int = 0) -> dict[str, list[float]]:
        """Compute per-channel mean and std across the dataset.

        Args:
            max_samples: Max images to sample (0 = all).

        Returns:
            Dict with ``mean`` and ``std`` keys (3-element lists for RGB).
        """
        to_tensor = T.ToTensor()
        indices = list(range(len(self.samples)))
        if max_samples > 0:
            rng = np.random.default_rng(42)
            indices = rng.choice(indices, size=min(max_samples, len(indices)), replace=False)

        channel_sum = torch.zeros(3, dtype=torch.float64)
        channel_sq_sum = torch.zeros(3, dtype=torch.float64)
        pixel_count = 0

        for i in indices:
            img_path = self.images_dir / self.samples[i]["file_name"]
            img = Image.open(img_path).convert("RGB")
            t = to_tensor(img).to(torch.float64)  # [3, H, W]
            channel_sum += t.sum(dim=(1, 2))
            channel_sq_sum += (t**2).sum(dim=(1, 2))
            pixel_count += t.shape[1] * t.shape[2]

        mean = channel_sum / pixel_count
        std = torch.sqrt(channel_sq_sum / pixel_count - mean**2)
        return {"mean": mean.tolist(), "std": std.tolist()}
