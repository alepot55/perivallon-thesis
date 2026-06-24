"""Smoke tests for the Swin-T RSP model and Lightning module."""

from __future__ import annotations

import pytest
import torch

from waste_detection.models.swin_rsp_baseline import SwinRSPClassifier
from waste_detection.training.lightning_module import WasteClassifierModule


class TestSwinRSPClassifier:
    def test_forward_shape(self) -> None:
        model = SwinRSPClassifier(pretrained_imagenet=False, num_classes=1)
        x = torch.randn(2, 3, 224, 224)
        out = model(x)
        assert out.shape == (2, 1)

    def test_forward_500px(self) -> None:
        """Test with actual training image size (500×500)."""
        model = SwinRSPClassifier(pretrained_imagenet=False, num_classes=1, image_size=500)
        x = torch.randn(1, 3, 500, 500)
        out = model(x)
        assert out.shape == (1, 1)

    def test_freeze_backbone(self) -> None:
        model = SwinRSPClassifier(pretrained_imagenet=False, freeze_backbone=True)
        backbone_grads = [p.requires_grad for p in model.backbone.parameters()]
        head_grads = [p.requires_grad for p in model.head.parameters()]
        assert not any(backbone_grads), "Backbone should be frozen"
        assert all(head_grads), "Head should be trainable"

    def test_unfreeze_last_stage(self) -> None:
        model = SwinRSPClassifier(
            pretrained_imagenet=False,
            freeze_backbone=True,
            unfreeze_last_stage=True,
        )
        # Last stage (layers.3) should be unfrozen
        stage3_grads = []
        other_grads = []
        for name, p in model.backbone.named_parameters():
            if "layers.3" in name or "norm" in name:
                stage3_grads.append(p.requires_grad)
            else:
                other_grads.append(p.requires_grad)
        assert all(stage3_grads), "Last stage should be unfrozen"
        assert not any(other_grads), "Other stages should be frozen"

    def test_get_trainable_params(self) -> None:
        model = SwinRSPClassifier(pretrained_imagenet=False, freeze_backbone=True)
        groups = model.get_trainable_params()
        # Only head should be trainable when backbone is frozen
        assert len(groups) == 1
        assert groups[0]["name"] == "head"

    def test_get_trainable_params_ft(self) -> None:
        model = SwinRSPClassifier(
            pretrained_imagenet=False,
            freeze_backbone=True,
            unfreeze_last_stage=True,
        )
        groups = model.get_trainable_params()
        assert len(groups) == 2  # backbone (stage 4) + head
        names = {g["name"] for g in groups}
        assert names == {"backbone", "head"}


class TestWasteClassifierModule:
    def test_training_step(self) -> None:
        module = WasteClassifierModule(
            model_cfg={"pretrained_imagenet": False},
            lr=1e-3,
            training_phase="tl",
        )
        batch = {
            "image": torch.randn(2, 3, 224, 224),
            "label": torch.tensor([0.0, 1.0]),
        }
        loss = module.training_step(batch, 0)
        assert loss.ndim == 0  # scalar
        assert loss.item() > 0

    def test_validation_step(self) -> None:
        module = WasteClassifierModule(
            model_cfg={"pretrained_imagenet": False},
            training_phase="tl",
        )
        batch = {
            "image": torch.randn(2, 3, 224, 224),
            "label": torch.tensor([0.0, 1.0]),
        }
        module.validation_step(batch, 0)

    def test_switch_to_finetune(self) -> None:
        module = WasteClassifierModule(
            model_cfg={"pretrained_imagenet": False},
            lr=1e-3,
            training_phase="tl",
        )
        module.switch_to_finetune(lr=1e-4)
        assert module.hparams.training_phase == "ft"
        assert module.hparams.lr == 1e-4

        # Check that last stage is unfrozen
        for name, p in module.model.backbone.named_parameters():
            if "layers.3" in name:
                assert p.requires_grad
