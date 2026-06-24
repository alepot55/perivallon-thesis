"""Multispectral DataModule for WorldView-3 imagery.

Extends the AerialWaste RGB pipeline to support multi-band TIF images
(e.g., 8-band WorldView-3 multispectral) with configurable band selection
and per-channel normalization.

WorldView-3 multispectral bands (8 bands at ~1.24m GSD):
  0: Coastal Blue  (400-450 nm)
  1: Blue          (450-510 nm)
  2: Green         (510-580 nm)
  3: Yellow        (585-625 nm)
  4: Red           (630-690 nm)
  5: Red-Edge      (705-745 nm)
  6: NIR1          (770-895 nm)
  7: NIR2          (860-1040 nm)

.. note::
    The actual WV-3 dataset is not yet available. The dataset class
    raises ``NotImplementedError`` at load time. Once integrated,
    replace the placeholder with real TIF loading logic.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader, Dataset, Subset

from waste_detection.data.aerialwaste_dm import AerialWasteDataModule

logger = logging.getLogger(__name__)

# WorldView-3 multispectral band names (8-band configuration)
WV3_BAND_NAMES: list[str] = [
    "Coastal Blue",
    "Blue",
    "Green",
    "Yellow",
    "Red",
    "Red-Edge",
    "NIR1",
    "NIR2",
]

# Placeholder per-channel normalization statistics for WV-3 8-band imagery.
# TODO: Compute real statistics from the WV-3 dataset once available.
# These values are approximate reflectance-based estimates (0-1 range)
# derived from typical urban/peri-urban land cover in WorldView-3 scenes.
WV3_DEFAULT_MEAN: tuple[float, ...] = (
    0.28, 0.30, 0.32, 0.31, 0.30, 0.33, 0.38, 0.36,
)
WV3_DEFAULT_STD: tuple[float, ...] = (
    0.17, 0.18, 0.17, 0.16, 0.18, 0.19, 0.22, 0.21,
)

_PROXY_VAL_FRACTION = 0.10


class MultispectralDataModule(pl.LightningDataModule):
    """Lightning DataModule for multispectral waste classification.

    Mirrors the train/val/test split logic from :class:`AerialWasteDataModule`
    but handles multi-band TIF images instead of RGB PNGs.

    Args:
        root: Dataset root path containing TIF imagery and metadata.
        channels: List of band indices to use (0-indexed). Defaults to
            all 8 WV-3 bands ``[0, 1, 2, 3, 4, 5, 6, 7]``.
        image_size: Resize target in pixels.
        batch_size: Batch size for data loaders.
        num_workers: Number of DataLoader workers.
        val_fraction: Fraction of training data for validation split.
            0.0 = proxy val mode (train on everything, 10% proxy for monitoring).
        mean: Per-channel mean for normalization. Length must match ``channels``.
        std: Per-channel std for normalization. Length must match ``channels``.
        seed: Random seed for reproducible train/val split.
    """

    def __init__(
        self,
        root: str | Path = "data/wv3",
        channels: list[int] | None = None,
        image_size: int = 224,
        batch_size: int = 32,
        num_workers: int = 4,
        val_fraction: float = 0.15,
        mean: tuple[float, ...] | list[float] | None = None,
        std: tuple[float, ...] | list[float] | None = None,
        seed: int = 42,
    ) -> None:
        super().__init__()

        # Default: all 8 WV-3 bands
        if channels is None:
            channels = list(range(8))
        self.channels = channels
        self.n_channels = len(channels)

        # Validate and set normalization stats
        if mean is None:
            mean = tuple(WV3_DEFAULT_MEAN[c] for c in channels)
        if std is None:
            std = tuple(WV3_DEFAULT_STD[c] for c in channels)

        if len(mean) != self.n_channels:
            raise ValueError(
                f"mean has {len(mean)} values but {self.n_channels} channels selected"
            )
        if len(std) != self.n_channels:
            raise ValueError(
                f"std has {len(std)} values but {self.n_channels} channels selected"
            )

        self.save_hyperparameters()
        self.root = Path(root)
        self.image_size = image_size
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.val_fraction = val_fraction
        self.mean = tuple(mean)
        self.std = tuple(std)
        self.seed = seed

        self.train_dataset: Dataset | None = None
        self.val_dataset: Dataset | None = None
        self.test_dataset: Dataset | None = None

        logger.info(
            "MultispectralDataModule: %d channels %s, image_size=%d",
            self.n_channels,
            [WV3_BAND_NAMES[c] for c in channels if c < len(WV3_BAND_NAMES)],
            image_size,
        )

    def _normalize(self, tensor: torch.Tensor) -> torch.Tensor:
        """Apply per-channel normalization to a (C, H, W) tensor."""
        for c in range(tensor.shape[0]):
            tensor[c] = (tensor[c] - self.mean[c]) / self.std[c]
        return tensor

    def setup(self, stage: str | None = None) -> None:
        """Set up train/val/test datasets.

        .. note::
            Currently raises ``NotImplementedError`` because the WV-3
            multispectral dataset class is not yet implemented. Replace
            ``_load_ms_dataset()`` with real TIF loading once the data
            is available.
        """
        if stage in ("fit", None):
            full_train = self._load_ms_dataset(split="train")

            if self.val_fraction > 0:
                n_val = int(len(full_train) * self.val_fraction)
                n_train = len(full_train) - n_val
                generator = torch.Generator().manual_seed(self.seed)
                train_subset, val_subset = torch.utils.data.random_split(
                    full_train, [n_train, n_val], generator=generator,
                )
                self.train_dataset = train_subset
                self.val_dataset = val_subset
            else:
                # Proxy val: train on ALL data, 10% proxy for monitoring
                n_proxy = int(len(full_train) * _PROXY_VAL_FRACTION)
                generator = torch.Generator().manual_seed(self.seed)
                indices = torch.randperm(len(full_train), generator=generator)
                proxy_indices = indices[:n_proxy].tolist()

                self.train_dataset = full_train
                self.val_dataset = Subset(full_train, proxy_indices)

        if stage in ("test", None):
            self.test_dataset = self._load_ms_dataset(split="test")

    def _load_ms_dataset(self, split: str) -> Dataset:
        """Load a multispectral dataset for the given split.

        Args:
            split: One of ``"train"`` or ``"test"``.

        Returns:
            A :class:`torch.utils.data.Dataset` yielding dicts with keys
            ``"image"`` (Tensor of shape ``(n_channels, H, W)``) and
            ``"label"`` (scalar Tensor).

        Raises:
            NotImplementedError: The WV-3 multispectral dataset is not yet
                available. Implement this method to load multi-band TIF
                images, select the configured channels, resize to
                ``image_size``, and apply per-channel normalization.

        .. todo::
            Implementation outline for when WV-3 data is available:

            1. Parse COCO-style JSON metadata (same format as AerialWaste v3).
            2. For each sample, load the multi-band TIF using rasterio::

                   import rasterio
                   with rasterio.open(tif_path) as src:
                       bands = src.read(self.channels)  # (C, H, W)

            3. Resize to ``(image_size, image_size)`` with bilinear interpolation.
            4. Apply per-channel normalization using ``self.mean`` / ``self.std``.
            5. Apply data augmentation (random flips, rotations) for train split.
            6. Return dict with ``"image"``, ``"label"``, ``"file_name"``.
        """
        raise NotImplementedError(
            f"WorldView-3 multispectral dataset loading is not yet implemented. "
            f"Requested split='{split}', root='{self.root}', "
            f"channels={self.channels}. "
            f"Implement TIF loading with rasterio once the WV-3 data is available."
        )

    def train_dataloader(self) -> DataLoader:
        """Training DataLoader with shuffling and pin_memory."""
        assert self.train_dataset is not None, "Call setup('fit') first"
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True,
            drop_last=True,
        )

    def val_dataloader(self) -> DataLoader:
        """Validation DataLoader (no shuffling)."""
        assert self.val_dataset is not None, "Call setup('fit') first"
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
        )

    def test_dataloader(self) -> DataLoader:
        """Test DataLoader (no shuffling)."""
        assert self.test_dataset is not None, "Call setup('test') first"
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
        )
