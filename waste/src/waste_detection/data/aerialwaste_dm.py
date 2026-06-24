"""PyTorch Lightning DataModule for AerialWaste v3."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader, Subset
from torchvision import transforms as T

from waste_detection.data.aerialwaste_dataset import AerialWasteDataset

_PROXY_VAL_FRACTION = 0.10  # fraction of train data used as proxy val


class AerialWasteDataModule(pl.LightningDataModule):
    """Lightning DataModule wrapping AerialWaste v3.

    When ``val_fraction > 0``, carves out an exclusive validation set from
    training data.  When ``val_fraction == 0``, trains on the **full**
    training split and uses a 10 % proxy subset (overlapping with training)
    for early-stopping / checkpoint monitoring only.

    Args:
        root: Dataset root path.
        image_size: Resize target (pixels).  500 for 20 cm/px @ 100 m context.
        target_gsd: Optional GSD filter (20, 30, or 50).
        batch_size: Batch size for data loaders.
        num_workers: DataLoader workers.
        val_fraction: Fraction of training data used for validation.
            0.0 = proxy val mode (train on everything).
        mean: Per-channel mean for normalization.
        std: Per-channel std for normalization.
        seed: Random seed for train/val split.
    """

    def __init__(
        self,
        root: str | Path = "data/raw",
        image_size: int = 500,
        target_gsd: int | None = 20,
        batch_size: int = 32,
        num_workers: int = 4,
        val_fraction: float = 0.15,
        mean: tuple[float, ...] = (0.485, 0.456, 0.406),
        std: tuple[float, ...] = (0.229, 0.224, 0.225),
        seed: int = 42,
    ) -> None:
        super().__init__()
        self.save_hyperparameters()
        self.root = Path(root)
        self.image_size = image_size
        self.target_gsd = target_gsd
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.val_fraction = val_fraction
        self.mean = mean
        self.std = std
        self.seed = seed

        self.train_dataset: Any = None
        self.val_dataset: Any = None
        self.test_dataset: AerialWasteDataset | None = None

    @property
    def train_transform(self) -> T.Compose:
        return T.Compose([
            T.Resize((self.image_size, self.image_size)),
            T.RandomHorizontalFlip(p=0.5),
            T.RandomVerticalFlip(p=0.5),
            T.RandomRotation(degrees=90, expand=False),
            T.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1, hue=0.05),
            T.ToTensor(),
            T.Normalize(mean=self.mean, std=self.std),
            T.RandomErasing(p=0.1, scale=(0.02, 0.1)),
        ])

    @property
    def eval_transform(self) -> T.Compose:
        return T.Compose([
            T.Resize((self.image_size, self.image_size)),
            T.ToTensor(),
            T.Normalize(mean=self.mean, std=self.std),
        ])

    def setup(self, stage: str | None = None) -> None:
        if stage in ("fit", None):
            full_train = AerialWasteDataset(
                root=self.root,
                split="train",
                transform=None,  # applied per-subset via _TransformSubset
                target_gsd=self.target_gsd,
            )

            if self.val_fraction > 0:
                # Exclusive split: remove val data from training
                n_val = int(len(full_train) * self.val_fraction)
                n_train = len(full_train) - n_val
                generator = torch.Generator().manual_seed(self.seed)
                train_subset, val_subset = torch.utils.data.random_split(
                    full_train, [n_train, n_val], generator=generator,
                )
                self.train_dataset = _TransformSubset(train_subset, self.train_transform)
                self.val_dataset = _TransformSubset(val_subset, self.eval_transform)
            else:
                # Proxy val: train on ALL data; 10% proxy for monitoring
                n_proxy = int(len(full_train) * _PROXY_VAL_FRACTION)
                generator = torch.Generator().manual_seed(self.seed)
                indices = torch.randperm(len(full_train), generator=generator)
                proxy_indices = indices[:n_proxy].tolist()

                self.train_dataset = _TransformSubset(full_train, self.train_transform)
                proxy_subset = Subset(full_train, proxy_indices)
                self.val_dataset = _TransformSubset(proxy_subset, self.eval_transform)

        if stage in ("test", None):
            self.test_dataset = AerialWasteDataset(
                root=self.root,
                split="test",
                transform=self.eval_transform,
                target_gsd=self.target_gsd,
            )

    def train_dataloader(self) -> DataLoader:
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True,
            drop_last=True,
        )

    def val_dataloader(self) -> DataLoader:
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
        )

    def test_dataloader(self) -> DataLoader:
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
        )


class _TransformSubset:
    """Wrapper that applies a transform to a Dataset/Subset's items."""

    def __init__(self, subset: Any, transform: Any) -> None:
        self.subset = subset
        self.transform = transform

    def __len__(self) -> int:
        return len(self.subset)

    def __getitem__(self, idx: int) -> dict:
        sample = self.subset[idx]
        if self.transform is not None:
            from torchvision.transforms.functional import to_pil_image
            img = sample["image"]
            if isinstance(img, torch.Tensor):
                img = to_pil_image(img)
            sample["image"] = self.transform(img)
        return sample
