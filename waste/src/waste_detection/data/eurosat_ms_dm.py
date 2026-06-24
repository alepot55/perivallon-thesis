"""EuroSAT multispectral DataModule for band ablation study.

Wraps torchgeo's EuroSAT 13-band Sentinel-2 dataset with configurable
band selection, normalization, and augmentation.

Note: RGB channels are always placed first (indices 0-2) to ensure
compatibility with the MSAdapter strategies that assume [R, G, B, ...] order.
"""

from __future__ import annotations

import logging
from typing import Any

import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchgeo.datasets import EuroSAT

logger = logging.getLogger(__name__)

# Pre-computed per-band statistics (torchgeo, EuroSAT training split)
BAND_MEAN: dict[str, float] = {
    "B01": 1354.41, "B02": 1118.24, "B03": 1042.93, "B04": 947.63,
    "B05": 1199.47, "B06": 1999.79, "B07": 2369.22, "B08": 2296.83,
    "B09": 732.08,  "B10": 12.11,   "B11": 1819.01, "B12": 1118.92,
    "B8A": 2594.14,
}
BAND_STD: dict[str, float] = {
    "B01": 245.72, "B02": 333.01, "B03": 395.09, "B04": 593.75,
    "B05": 566.42, "B06": 861.18, "B07": 1086.63, "B08": 1117.98,
    "B09": 404.92, "B10": 4.78,   "B11": 1002.59, "B12": 761.30,
    "B8A": 1231.59,
}

# Band presets — RGB always first for adapter compatibility
BAND_PRESETS: dict[str, tuple[str, ...]] = {
    "RGB":  ("B04", "B03", "B02"),
    "RGBN": ("B04", "B03", "B02", "B08"),
    "MS6":  ("B04", "B03", "B02", "B08", "B12", "B8A"),
    "MS10": ("B04", "B03", "B02", "B05", "B06", "B07", "B08", "B11", "B12", "B8A"),
    "MS13": ("B04", "B03", "B02", "B01", "B05", "B06", "B07", "B08", "B09", "B10", "B11", "B12", "B8A"),
}

EUROSAT_CLASSES: list[str] = [
    "AnnualCrop", "Forest", "HerbaceousVegetation", "Highway",
    "Industrial", "Pasture", "PermanentCrop", "Residential",
    "River", "SeaLake",
]


class _EuroSATTransform:
    """Resize + normalize + augment EuroSAT samples (tensor-based)."""

    def __init__(
        self,
        bands: tuple[str, ...],
        image_size: int = 224,
        augment: bool = False,
    ) -> None:
        self.mean = torch.tensor([BAND_MEAN[b] for b in bands]).view(-1, 1, 1)
        self.std = torch.tensor([BAND_STD[b] for b in bands]).view(-1, 1, 1)
        self.image_size = image_size
        self.augment = augment

    def __call__(self, sample: dict[str, Any]) -> dict[str, Any]:
        image = sample["image"].float()  # (C, H, W)

        # Resize
        if image.shape[-2:] != (self.image_size, self.image_size):
            image = F.interpolate(
                image.unsqueeze(0),
                size=(self.image_size, self.image_size),
                mode="bilinear",
                align_corners=False,
            ).squeeze(0)

        # Normalize
        image = (image - self.mean) / self.std

        # Augmentation
        if self.augment:
            if torch.rand(1).item() > 0.5:
                image = image.flip(-1)
            if torch.rand(1).item() > 0.5:
                image = image.flip(-2)
            k = torch.randint(0, 4, (1,)).item()
            if k > 0:
                image = torch.rot90(image, k, [-2, -1])

        sample["image"] = image
        return sample


class EuroSATMultispectralDM(pl.LightningDataModule):
    """Lightning DataModule for EuroSAT 13-band multispectral data.

    Uses torchgeo's EuroSAT with pre-defined train/val/test splits (60/20/20).
    Supports band presets: RGB (3ch), RGBN (4ch), MS6, MS10, MS13.

    Args:
        root: Directory for EuroSAT data.
        bands_preset: Band configuration name.
        image_size: Target image size (224 for Swin-T).
        batch_size: Batch size.
        num_workers: DataLoader workers.
        download: Auto-download from HuggingFace.
    """

    def __init__(
        self,
        root: str = "data/eurosat",
        bands_preset: str = "RGB",
        image_size: int = 224,
        batch_size: int = 32,
        num_workers: int = 4,
        download: bool = True,
    ) -> None:
        super().__init__()
        if bands_preset not in BAND_PRESETS:
            raise ValueError(f"Unknown preset '{bands_preset}'. Choose from: {list(BAND_PRESETS)}")

        self.bands = BAND_PRESETS[bands_preset]
        self.save_hyperparameters()
        self.root = root
        self.bands_preset = bands_preset
        self.n_channels = len(self.bands)
        self.image_size = image_size
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.download = download

        self.train_dataset: Any = None
        self.val_dataset: Any = None
        self.test_dataset: Any = None

    def setup(self, stage: str | None = None) -> None:
        if stage in ("fit", None):
            self.train_dataset = EuroSAT(
                root=self.root, split="train", bands=self.bands,
                transforms=_EuroSATTransform(self.bands, self.image_size, augment=True),
                download=self.download,
            )
            self.val_dataset = EuroSAT(
                root=self.root, split="val", bands=self.bands,
                transforms=_EuroSATTransform(self.bands, self.image_size, augment=False),
                download=self.download,
            )
        if stage in ("test", None):
            self.test_dataset = EuroSAT(
                root=self.root, split="test", bands=self.bands,
                transforms=_EuroSATTransform(self.bands, self.image_size, augment=False),
                download=self.download,
            )

    def train_dataloader(self) -> DataLoader:
        return DataLoader(
            self.train_dataset, batch_size=self.batch_size, shuffle=True,
            num_workers=self.num_workers, pin_memory=True, drop_last=True,
        )

    def val_dataloader(self) -> DataLoader:
        return DataLoader(
            self.val_dataset, batch_size=self.batch_size, shuffle=False,
            num_workers=self.num_workers, pin_memory=True,
        )

    def test_dataloader(self) -> DataLoader:
        return DataLoader(
            self.test_dataset, batch_size=self.batch_size, shuffle=False,
            num_workers=self.num_workers, pin_memory=True,
        )
