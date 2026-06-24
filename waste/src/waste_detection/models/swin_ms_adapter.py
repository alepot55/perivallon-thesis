"""Multispectral adaptation strategies for Swin-T backbone.

Adapts a pretrained 3-channel Swin-T (from SwinRSPClassifier) to accept
N-channel multispectral input (e.g., 8-band WorldView-3) using one of
three strategies:

1. **WeightInflation**: Replicate the 3-channel patch_embed conv weights
   across all input channels, scaling by 3/C_in to preserve activation
   magnitude. Simple, preserves pretrained features.

2. **RandomInitExtra**: Keep the original 3 RGB conv weights unchanged,
   add Kaiming-initialized weights for extra channels via concatenation
   along the channel dimension.

3. **LateFusion**: Two separate Swin-T backbones (RGB + extra channels).
   The RGB backbone retains pretrained weights; the extra-channels backbone
   gets a randomly initialized patch_embed. Features are fused before the
   classification head.

All strategies are accessible through the unified :func:`adapt_patch_embed`
entry point, or via the :class:`LateFusionClassifier` wrapper for the
late fusion approach.

Reference:
    - WorldView-3: 8 multispectral bands (Coastal, Blue, Green, Yellow,
      Red, Red-Edge, NIR1, NIR2) at ~1.24m GSD.
"""

from __future__ import annotations

import copy
import logging
import math
from typing import Any

import torch
import torch.nn as nn

from waste_detection.models.swin_rsp_baseline import SwinRSPClassifier

logger = logging.getLogger(__name__)


def adapt_patch_embed(
    model: SwinRSPClassifier,
    in_channels: int = 8,
    strategy: str = "weight_inflation",
) -> SwinRSPClassifier | LateFusionClassifier:
    """Adapt a pretrained 3-channel SwinRSPClassifier for multispectral input.

    This is the main entry point for all adaptation strategies.

    Args:
        model: A pre-configured :class:`SwinRSPClassifier` (with pretrained
            weights already loaded).
        in_channels: Total number of input channels (default 8 for WV-3).
            Must be >= 3.
        strategy: One of ``"weight_inflation"``, ``"random_init_extra"``,
            or ``"late_fusion"``.

    Returns:
        For ``weight_inflation`` and ``random_init_extra``: the modified
        :class:`SwinRSPClassifier` (deep-copied, original untouched).
        For ``late_fusion``: a :class:`LateFusionClassifier` wrapper.

    Raises:
        ValueError: If strategy is unknown or in_channels < 3.
    """
    valid_strategies = ("weight_inflation", "random_init_extra", "late_fusion")
    if strategy not in valid_strategies:
        raise ValueError(
            f"Unknown strategy '{strategy}'. Choose from: {valid_strategies}"
        )
    if in_channels < 3:
        raise ValueError(f"in_channels must be >= 3, got {in_channels}")

    if strategy == "weight_inflation":
        return _apply_weight_inflation(model, in_channels)
    elif strategy == "random_init_extra":
        return _apply_random_init_extra(model, in_channels)
    elif strategy == "late_fusion":
        return LateFusionClassifier(model, in_channels=in_channels)

    # Unreachable, but keeps type checkers happy
    raise RuntimeError(f"Unhandled strategy: {strategy}")  # pragma: no cover


# ---------------------------------------------------------------------------
# Strategy 1: Weight Inflation
# ---------------------------------------------------------------------------


def _apply_weight_inflation(
    model: SwinRSPClassifier,
    in_channels: int,
) -> SwinRSPClassifier:
    """Replicate patch_embed conv weights across all input channels.

    The original 3-channel weights are copied to channels 0-2.
    Extra channels (3+) receive the mean of the RGB weights.
    The entire kernel is then scaled by ``3 / in_channels`` so the output
    activation magnitude is approximately preserved.

    Args:
        model: Base model (will be deep-copied).
        in_channels: Target number of input channels.

    Returns:
        Modified :class:`SwinRSPClassifier` with inflated patch_embed.
    """
    adapted = copy.deepcopy(model)
    old_proj = adapted.backbone.patch_embed.proj
    assert isinstance(old_proj, nn.Conv2d), f"Expected Conv2d, got {type(old_proj)}"

    old_weight = old_proj.weight.data  # (out_ch, 3, kH, kW)
    old_bias = old_proj.bias

    out_channels = old_weight.shape[0]
    kernel_size = old_proj.kernel_size
    stride = old_proj.stride
    padding = old_proj.padding

    new_proj = nn.Conv2d(
        in_channels, out_channels,
        kernel_size=kernel_size, stride=stride, padding=padding,
        bias=old_bias is not None,
    )

    # Build inflated weight tensor
    new_weight = torch.zeros(
        out_channels, in_channels, *kernel_size,
        dtype=old_weight.dtype,
    )
    # Copy original RGB weights
    new_weight[:, :3, :, :] = old_weight
    # Extra channels: use mean of RGB weights as initialization
    rgb_mean = old_weight.mean(dim=1, keepdim=True)  # (out_ch, 1, kH, kW)
    for c in range(3, in_channels):
        new_weight[:, c : c + 1, :, :] = rgb_mean

    # Scale to preserve activation magnitude: sum over input channels
    # produces similar output as original 3-channel conv
    new_weight *= 3.0 / in_channels

    new_proj.weight.data = new_weight
    if old_bias is not None:
        new_proj.bias.data = old_bias.data.clone()

    adapted.backbone.patch_embed.proj = new_proj
    logger.info(
        "WeightInflation: patch_embed.proj inflated from 3 -> %d channels "
        "(scale=%.4f)",
        in_channels,
        3.0 / in_channels,
    )
    return adapted


# ---------------------------------------------------------------------------
# Strategy 2: Random Init Extra Channels
# ---------------------------------------------------------------------------


def _apply_random_init_extra(
    model: SwinRSPClassifier,
    in_channels: int,
) -> SwinRSPClassifier:
    """Keep original RGB weights, add Kaiming-initialized extra channels.

    Channels 0-2 retain the exact pretrained weights. Channels 3+ are
    randomly initialized with Kaiming uniform (fan_in mode), matching
    PyTorch's default Conv2d initialization.

    Args:
        model: Base model (will be deep-copied).
        in_channels: Target number of input channels.

    Returns:
        Modified :class:`SwinRSPClassifier` with extended patch_embed.
    """
    adapted = copy.deepcopy(model)
    old_proj = adapted.backbone.patch_embed.proj
    assert isinstance(old_proj, nn.Conv2d), f"Expected Conv2d, got {type(old_proj)}"

    old_weight = old_proj.weight.data  # (out_ch, 3, kH, kW)
    old_bias = old_proj.bias

    out_channels = old_weight.shape[0]
    kernel_size = old_proj.kernel_size
    stride = old_proj.stride
    padding = old_proj.padding

    n_extra = in_channels - 3

    # Kaiming uniform init for extra channels
    extra_weight = torch.empty(
        out_channels, n_extra, *kernel_size,
        dtype=old_weight.dtype,
    )
    fan_in = n_extra * kernel_size[0] * kernel_size[1]
    bound = math.sqrt(6.0 / fan_in)  # Kaiming uniform, ReLU gain=1
    extra_weight.uniform_(-bound, bound)

    # Concatenate: [pretrained_RGB | random_extra]
    new_weight = torch.cat([old_weight, extra_weight], dim=1)

    new_proj = nn.Conv2d(
        in_channels, out_channels,
        kernel_size=kernel_size, stride=stride, padding=padding,
        bias=old_bias is not None,
    )
    new_proj.weight = nn.Parameter(new_weight)
    if old_bias is not None:
        new_proj.bias = nn.Parameter(old_bias.data.clone())

    adapted.backbone.patch_embed.proj = new_proj
    logger.info(
        "RandomInitExtra: patch_embed.proj extended to %d channels "
        "(RGB preserved, %d extra with Kaiming init)",
        in_channels,
        n_extra,
    )
    return adapted


# ---------------------------------------------------------------------------
# Strategy 3: Late Fusion
# ---------------------------------------------------------------------------


class LateFusionClassifier(nn.Module):
    """Two-branch late fusion classifier for multispectral input.

    Uses two separate Swin-T backbones:
      - **RGB branch**: channels 0-2, initialized from the pretrained model.
      - **Extra branch**: channels 3+, with a randomly initialized patch_embed
        and the rest of the Swin architecture also deep-copied (but effectively
        randomly initialized for the extra bands).

    Features from both branches are concatenated and projected through a
    fusion layer before the classification head.

    Args:
        base_model: A pre-configured :class:`SwinRSPClassifier` with pretrained
            weights loaded.
        in_channels: Total number of input channels (default 8 for WV-3).
            Must be > 3.
    """

    def __init__(
        self,
        base_model: SwinRSPClassifier,
        in_channels: int = 8,
    ) -> None:
        super().__init__()

        n_extra = in_channels - 3
        if n_extra <= 0:
            raise ValueError(
                f"LateFusion requires in_channels > 3, got {in_channels}"
            )

        self.in_channels = in_channels
        self._n_extra = n_extra

        # RGB branch: pretrained backbone (deep copy)
        self.rgb_backbone = copy.deepcopy(base_model.backbone)
        embed_dim = self.rgb_backbone.num_features  # 768 for Swin-T

        # Extra-channels branch: separate Swin-T backbone with randomly
        # initialized patch_embed for n_extra input channels.
        self.extra_backbone = copy.deepcopy(base_model.backbone)
        self._reinit_patch_embed(self.extra_backbone, n_extra)

        # Fusion: concatenated features (2 * embed_dim) -> embed_dim
        self.fusion = nn.Sequential(
            nn.Linear(2 * embed_dim, embed_dim),
            nn.GELU(),
            nn.Dropout(p=0.1),
        )

        # Classification head (deep copy from base model)
        self.head = copy.deepcopy(base_model.head)

        logger.info(
            "LateFusion: RGB branch (3ch, pretrained) + extra branch (%dch, "
            "random patch_embed) -> fusion -> head",
            n_extra,
        )

    @staticmethod
    def _reinit_patch_embed(backbone: nn.Module, n_channels: int) -> None:
        """Replace patch_embed.proj with a randomly initialized Conv2d.

        Args:
            backbone: Swin-T backbone to modify in-place.
            n_channels: Number of input channels for the new projection.
        """
        old_proj = backbone.patch_embed.proj
        assert isinstance(old_proj, nn.Conv2d)

        new_proj = nn.Conv2d(
            n_channels,
            old_proj.out_channels,
            kernel_size=old_proj.kernel_size,
            stride=old_proj.stride,
            padding=old_proj.padding,
            bias=old_proj.bias is not None,
        )
        # Default PyTorch init (Kaiming uniform) is applied automatically
        backbone.patch_embed.proj = new_proj

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through both branches with late fusion.

        Args:
            x: Input tensor of shape ``(B, in_channels, H, W)``.

        Returns:
            Logits tensor of shape ``(B, num_classes)`` (pre-sigmoid).
        """
        rgb = x[:, :3, :, :]
        extra = x[:, 3:, :, :]

        rgb_feat = self.rgb_backbone(rgb)        # (B, embed_dim)
        extra_feat = self.extra_backbone(extra)  # (B, embed_dim)

        fused = torch.cat([rgb_feat, extra_feat], dim=1)  # (B, 2*embed_dim)
        fused = self.fusion(fused)                          # (B, embed_dim)
        return self.head(fused)                             # (B, num_classes)

    def get_trainable_params(self) -> list[dict[str, Any]]:
        """Return parameter groups for differential learning rates.

        Groups:
          - ``rgb_backbone``: pretrained RGB branch (recommended: low LR).
          - ``extra_backbone``: randomly initialized extra branch (high LR).
          - ``fusion``: fusion layer (high LR).
          - ``head``: classification head (high LR).
        """
        rgb_params = [p for p in self.rgb_backbone.parameters() if p.requires_grad]
        extra_params = list(self.extra_backbone.parameters())
        fusion_params = list(self.fusion.parameters())
        head_params = list(self.head.parameters())

        groups = []
        if rgb_params:
            groups.append({"params": rgb_params, "name": "rgb_backbone"})
        groups.append({"params": extra_params, "name": "extra_backbone"})
        groups.append({"params": fusion_params, "name": "fusion"})
        groups.append({"params": head_params, "name": "head"})
        return groups
