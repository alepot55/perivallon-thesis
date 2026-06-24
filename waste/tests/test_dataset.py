"""Smoke tests for AerialWaste dataset and DataModule."""

from __future__ import annotations

from pathlib import Path

import pytest
import torch
from torchvision import transforms as T

from waste_detection.data.aerialwaste_dataset import AerialWasteDataset, NUM_CATEGORIES
from waste_detection.data.aerialwaste_dm import AerialWasteDataModule


class TestAerialWasteDataset:
    def test_load_train_split(self, synthetic_dataset: Path) -> None:
        ds = AerialWasteDataset(root=synthetic_dataset, split="train")
        assert len(ds) == 14

    def test_load_test_split(self, synthetic_dataset: Path) -> None:
        ds = AerialWasteDataset(root=synthetic_dataset, split="test")
        assert len(ds) == 6

    def test_getitem_returns_expected_keys(self, synthetic_dataset: Path) -> None:
        ds = AerialWasteDataset(root=synthetic_dataset, split="train")
        sample = ds[0]
        assert "image" in sample
        assert "label" in sample
        assert "file_name" in sample
        assert isinstance(sample["image"], torch.Tensor)
        assert sample["image"].shape[0] == 3  # RGB

    def test_binary_label_values(self, synthetic_dataset: Path) -> None:
        ds = AerialWasteDataset(root=synthetic_dataset, split="train")
        labels = [ds[i]["label"].item() for i in range(len(ds))]
        assert set(labels) == {0.0, 1.0}

    def test_multiclass_labels(self, synthetic_dataset: Path) -> None:
        ds = AerialWasteDataset(root=synthetic_dataset, split="train", multiclass=True)
        sample = ds[0]  # first positive with categories
        assert "multi_label" in sample
        assert sample["multi_label"].shape == (NUM_CATEGORIES,)
        assert sample["multi_label"].sum() > 0  # has some categories

    def test_class_distribution(self, synthetic_dataset: Path) -> None:
        ds = AerialWasteDataset(root=synthetic_dataset, split="train")
        dist = ds.get_class_distribution()
        assert "waste" in dist
        assert "no_waste" in dist
        assert dist["waste"] + dist["no_waste"] == len(ds)

    def test_transform_applied(self, synthetic_dataset: Path) -> None:
        transform = T.Compose([T.Resize((224, 224)), T.ToTensor()])
        ds = AerialWasteDataset(root=synthetic_dataset, split="train", transform=transform)
        sample = ds[0]
        assert sample["image"].shape == (3, 224, 224)

    def test_missing_json_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            AerialWasteDataset(root=tmp_path, split="train")


class TestAerialWasteDataModule:
    def test_setup_fit(self, synthetic_dataset: Path) -> None:
        dm = AerialWasteDataModule(
            root=synthetic_dataset,
            image_size=224,
            target_gsd=None,  # no filtering for synthetic data
            batch_size=4,
            num_workers=0,
            val_fraction=0.2,
        )
        dm.setup(stage="fit")
        assert dm.train_dataset is not None
        assert dm.val_dataset is not None

    def test_setup_test(self, synthetic_dataset: Path) -> None:
        dm = AerialWasteDataModule(
            root=synthetic_dataset,
            image_size=224,
            target_gsd=None,
            batch_size=4,
            num_workers=0,
        )
        dm.setup(stage="test")
        assert dm.test_dataset is not None

    def test_train_dataloader_batches(self, synthetic_dataset: Path) -> None:
        dm = AerialWasteDataModule(
            root=synthetic_dataset,
            image_size=224,
            target_gsd=None,
            batch_size=4,
            num_workers=0,
            val_fraction=0.2,
        )
        dm.setup(stage="fit")
        batch = next(iter(dm.train_dataloader()))
        assert batch["image"].shape == (4, 3, 224, 224)
        assert batch["label"].shape == (4,)
