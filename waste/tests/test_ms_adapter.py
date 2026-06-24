"""Unit tests for multispectral Swin-T adapter strategies.

Tests the three adaptation strategies (WeightInflation, RandomInitExtra,
LateFusion) and the ``adapt_patch_embed`` entry point for correctness
of output shape, weight initialization, and activation magnitude.
"""

from __future__ import annotations

import pytest
import torch

from waste_detection.models.swin_rsp_baseline import SwinRSPClassifier
from waste_detection.models.swin_ms_adapter import (
    LateFusionClassifier,
    adapt_patch_embed,
)

IMG_SIZE = 224
BATCH_SIZE = 2
N_CHANNELS = 8  # WorldView-3
STRATEGIES = ["weight_inflation", "random_init_extra", "late_fusion"]


@pytest.fixture
def base_model() -> SwinRSPClassifier:
    """Create a base Swin-T classifier (no pretrained weights, for speed)."""
    return SwinRSPClassifier(
        pretrained_imagenet=False,
        num_classes=1,
        image_size=IMG_SIZE,
    )


# ---------------------------------------------------------------------------
# Output shape tests
# ---------------------------------------------------------------------------


class TestOutputShape:
    """Verify that all strategies produce correct output shape [B, 1]."""

    @pytest.mark.parametrize("strategy", STRATEGIES)
    def test_output_shape_8ch(
        self, base_model: SwinRSPClassifier, strategy: str
    ) -> None:
        """Input [B, 8, 224, 224] should produce [B, 1]."""
        adapted = adapt_patch_embed(base_model, in_channels=N_CHANNELS, strategy=strategy)
        x = torch.randn(BATCH_SIZE, N_CHANNELS, IMG_SIZE, IMG_SIZE)
        with torch.no_grad():
            out = adapted(x)
        assert out.shape == (BATCH_SIZE, 1), (
            f"Expected ({BATCH_SIZE}, 1), got {out.shape} for strategy={strategy}"
        )

    @pytest.mark.parametrize("strategy", STRATEGIES)
    @pytest.mark.parametrize("in_channels", [4, 6, 8])
    def test_output_shape_various_channels(
        self,
        base_model: SwinRSPClassifier,
        strategy: str,
        in_channels: int,
    ) -> None:
        """All channel counts >= 3 should produce [B, 1]."""
        adapted = adapt_patch_embed(base_model, in_channels=in_channels, strategy=strategy)
        x = torch.randn(BATCH_SIZE, in_channels, IMG_SIZE, IMG_SIZE)
        with torch.no_grad():
            out = adapted(x)
        assert out.shape == (BATCH_SIZE, 1)


# ---------------------------------------------------------------------------
# WeightInflation tests
# ---------------------------------------------------------------------------


class TestWeightInflation:
    """Verify weight inflation preserves activation magnitude."""

    def test_activation_magnitude_preserved(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """Mean activation of inflated model should be within 2x of RGB model.

        Feeds random input to both the original (3ch) and inflated (8ch) models.
        The scaling factor 3/C_in should keep activation magnitudes comparable.
        """
        torch.manual_seed(42)
        x_rgb = torch.randn(BATCH_SIZE, 3, IMG_SIZE, IMG_SIZE)
        x_ms = torch.randn(BATCH_SIZE, N_CHANNELS, IMG_SIZE, IMG_SIZE)
        # Make RGB channels of MS input match the RGB input
        x_ms[:, :3, :, :] = x_rgb

        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="weight_inflation"
        )

        with torch.no_grad():
            out_rgb = base_model(x_rgb)
            out_ms = adapted(x_ms)

        rgb_mag = out_rgb.abs().mean().item()
        ms_mag = out_ms.abs().mean().item()

        # Allow 2x tolerance (random extra channels add noise)
        assert ms_mag < rgb_mag * 2.0 + 0.5, (
            f"MS activation magnitude ({ms_mag:.4f}) is too large compared "
            f"to RGB ({rgb_mag:.4f}). Weight scaling may be broken."
        )
        assert ms_mag > rgb_mag * 0.01, (
            f"MS activation magnitude ({ms_mag:.6f}) is near zero, "
            f"suggesting weights were zeroed out."
        )

    def test_inflated_weight_shape(self, base_model: SwinRSPClassifier) -> None:
        """Inflated patch_embed should have shape (out_ch, 8, kH, kW)."""
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="weight_inflation"
        )
        weight = adapted.backbone.patch_embed.proj.weight
        assert weight.shape[1] == N_CHANNELS, (
            f"Expected channel dim = {N_CHANNELS}, got {weight.shape[1]}"
        )

    def test_rgb_channels_scaled(self, base_model: SwinRSPClassifier) -> None:
        """RGB channels should be original weights * (3/N)."""
        original_weight = base_model.backbone.patch_embed.proj.weight.data.clone()
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="weight_inflation"
        )
        inflated_weight = adapted.backbone.patch_embed.proj.weight.data
        scale = 3.0 / N_CHANNELS

        expected = original_weight * scale
        actual = inflated_weight[:, :3, :, :]
        assert torch.allclose(actual, expected, atol=1e-6), (
            "Inflated RGB weights should equal original * (3/N)"
        )


# ---------------------------------------------------------------------------
# RandomInitExtra tests
# ---------------------------------------------------------------------------


class TestRandomInitExtra:
    """Verify random init keeps original RGB weights and has correct shape."""

    def test_rgb_weights_preserved(self, base_model: SwinRSPClassifier) -> None:
        """Channels 0-2 should retain exact original weights."""
        original_weight = base_model.backbone.patch_embed.proj.weight.data.clone()
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="random_init_extra"
        )
        new_weight = adapted.backbone.patch_embed.proj.weight.data
        rgb_portion = new_weight[:, :3, :, :]
        assert torch.allclose(rgb_portion, original_weight, atol=1e-6), (
            "RGB weights (channels 0-2) should be preserved exactly"
        )

    def test_correct_weight_shape(self, base_model: SwinRSPClassifier) -> None:
        """Weight tensor should have shape (out_ch, 8, kH, kW)."""
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="random_init_extra"
        )
        weight = adapted.backbone.patch_embed.proj.weight
        assert weight.shape[1] == N_CHANNELS, (
            f"Expected channel dim = {N_CHANNELS}, got {weight.shape[1]}"
        )

    def test_extra_channels_nonzero(self, base_model: SwinRSPClassifier) -> None:
        """Extra channels should have non-zero Kaiming-initialized weights."""
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="random_init_extra"
        )
        extra = adapted.backbone.patch_embed.proj.weight.data[:, 3:, :, :]
        assert extra.abs().sum() > 0, "Extra channel weights should be non-zero"

    def test_extra_channels_differ_from_rgb(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """Extra channels should NOT be copies of RGB weights."""
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="random_init_extra"
        )
        weight = adapted.backbone.patch_embed.proj.weight.data
        rgb_mean = weight[:, :3, :, :].mean(dim=1, keepdim=True)
        for c in range(3, N_CHANNELS):
            assert not torch.allclose(weight[:, c : c + 1, :, :], rgb_mean, atol=1e-4), (
                f"Extra channel {c} should differ from RGB mean"
            )


# ---------------------------------------------------------------------------
# LateFusionClassifier tests
# ---------------------------------------------------------------------------


class TestLateFusionClassifier:
    """Verify LateFusionClassifier architecture and forward pass."""

    def test_forward_pass(self, base_model: SwinRSPClassifier) -> None:
        """LateFusionClassifier should accept [B, 8, H, W] and produce [B, 1]."""
        model = LateFusionClassifier(base_model, in_channels=N_CHANNELS)
        x = torch.randn(BATCH_SIZE, N_CHANNELS, IMG_SIZE, IMG_SIZE)
        with torch.no_grad():
            out = model(x)
        assert out.shape == (BATCH_SIZE, 1)

    def test_has_two_backbones(self, base_model: SwinRSPClassifier) -> None:
        """Should have separate RGB and extra-bands Swin backbones."""
        model = LateFusionClassifier(base_model, in_channels=N_CHANNELS)
        assert hasattr(model, "rgb_backbone"), "Missing RGB backbone"
        assert hasattr(model, "extra_backbone"), "Missing extra-bands backbone"
        assert hasattr(model, "fusion"), "Missing fusion layer"
        assert hasattr(model, "head"), "Missing classification head"

    def test_rgb_backbone_preserves_weights(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """RGB backbone should retain original pretrained weights."""
        original_weight = base_model.backbone.patch_embed.proj.weight.data.clone()
        model = LateFusionClassifier(base_model, in_channels=N_CHANNELS)
        rgb_weight = model.rgb_backbone.patch_embed.proj.weight.data
        assert torch.allclose(rgb_weight, original_weight, atol=1e-6), (
            "RGB backbone should preserve original weights"
        )

    def test_extra_backbone_has_correct_channels(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """Extra backbone patch_embed should accept n_extra channels."""
        n_extra = N_CHANNELS - 3
        model = LateFusionClassifier(base_model, in_channels=N_CHANNELS)
        extra_proj = model.extra_backbone.patch_embed.proj
        assert extra_proj.in_channels == n_extra, (
            f"Extra backbone should accept {n_extra} channels, "
            f"got {extra_proj.in_channels}"
        )

    def test_param_groups(self, base_model: SwinRSPClassifier) -> None:
        """Should expose parameter groups for differential LR."""
        model = LateFusionClassifier(base_model, in_channels=N_CHANNELS)
        groups = model.get_trainable_params()
        names = {g["name"] for g in groups}
        assert "rgb_backbone" in names
        assert "extra_backbone" in names
        assert "head" in names

    def test_requires_more_than_3_channels(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """LateFusion with in_channels=3 should raise ValueError."""
        with pytest.raises(ValueError, match="in_channels > 3"):
            LateFusionClassifier(base_model, in_channels=3)


# ---------------------------------------------------------------------------
# adapt_patch_embed entry point tests
# ---------------------------------------------------------------------------


class TestAdaptPatchEmbed:
    """Verify the unified entry point."""

    @pytest.mark.parametrize("strategy", STRATEGIES)
    def test_entry_point(
        self, base_model: SwinRSPClassifier, strategy: str
    ) -> None:
        """adapt_patch_embed should return a working model for each strategy."""
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy=strategy
        )
        x = torch.randn(BATCH_SIZE, N_CHANNELS, IMG_SIZE, IMG_SIZE)
        with torch.no_grad():
            out = adapted(x)
        assert out.shape == (BATCH_SIZE, 1)

    def test_returns_swin_for_weight_inflation(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """weight_inflation should return a SwinRSPClassifier."""
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="weight_inflation"
        )
        assert isinstance(adapted, SwinRSPClassifier)

    def test_returns_swin_for_random_init(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """random_init_extra should return a SwinRSPClassifier."""
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="random_init_extra"
        )
        assert isinstance(adapted, SwinRSPClassifier)

    def test_returns_late_fusion_for_late_fusion(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """late_fusion should return a LateFusionClassifier."""
        adapted = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="late_fusion"
        )
        assert isinstance(adapted, LateFusionClassifier)

    def test_invalid_strategy(self, base_model: SwinRSPClassifier) -> None:
        """Unknown strategy should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown strategy"):
            adapt_patch_embed(base_model, in_channels=N_CHANNELS, strategy="invalid")

    def test_in_channels_too_low(self, base_model: SwinRSPClassifier) -> None:
        """in_channels < 3 should raise ValueError."""
        with pytest.raises(ValueError, match="in_channels must be >= 3"):
            adapt_patch_embed(
                base_model, in_channels=2, strategy="weight_inflation"
            )

    def test_does_not_modify_original(
        self, base_model: SwinRSPClassifier
    ) -> None:
        """adapt_patch_embed should deep-copy; original model stays untouched."""
        original_weight = base_model.backbone.patch_embed.proj.weight.data.clone()
        _ = adapt_patch_embed(
            base_model, in_channels=N_CHANNELS, strategy="weight_inflation"
        )
        current_weight = base_model.backbone.patch_embed.proj.weight.data
        assert torch.allclose(current_weight, original_weight, atol=1e-6), (
            "adapt_patch_embed should not modify the original model"
        )


# ---------------------------------------------------------------------------
# CUDA tests (skipped if no GPU)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
class TestCUDA:
    """Verify models work on GPU."""

    @pytest.mark.parametrize("strategy", STRATEGIES)
    def test_forward_on_cuda(self, strategy: str) -> None:
        """Forward pass should work on CUDA device."""
        base = SwinRSPClassifier(
            pretrained_imagenet=False, num_classes=1, image_size=IMG_SIZE
        )
        adapted = adapt_patch_embed(base, in_channels=N_CHANNELS, strategy=strategy)
        adapted = adapted.cuda()
        x = torch.randn(1, N_CHANNELS, IMG_SIZE, IMG_SIZE, device="cuda")
        with torch.no_grad():
            out = adapted(x)
        assert out.shape == (1, 1)
        assert out.device.type == "cuda"
