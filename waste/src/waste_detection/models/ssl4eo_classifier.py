"""SSL4EO-S12 ViT classifier with spectral band selection.

Uses a ViT-Small/16 pretrained on Sentinel-2 (all 13 bands) via MoCo-v3
from the SSL4EO-S12 dataset (Wang et al., 2022). Loaded via TorchGeo.

Band selection is achieved by slicing the pretrained patch embedding weight
matrix along the input channel dimension, preserving spectral alignment.

Reference:
    - SSL4EO-S12: https://arxiv.org/abs/2211.07044
    - TorchGeo: https://torchgeo.readthedocs.io/
"""

from __future__ import annotations

import logging
from typing import Any

import torch
import torch.nn as nn
from torchgeo.models import vit_small_patch16_224, ViTSmall16_Weights

logger = logging.getLogger(__name__)

# Sentinel-2 band ordering in SSL4EO-S12 pretrained weights
S2_BANDS = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B8a", "B9", "B10", "B11", "B12"]
S2_BAND_INDEX = {name: i for i, name in enumerate(S2_BANDS)}

# Common band presets (indices into the 13-band S2 ordering)
BAND_PRESETS = {
    "rgb": [3, 2, 1],          # B4(Red), B3(Green), B2(Blue)
    "rgbn": [3, 2, 1, 7],     # + B8(NIR)
    "ms6": [3, 2, 1, 7, 11, 12],  # + B11(SWIR1), B12(SWIR2)
    "ms10": [1, 2, 3, 4, 5, 6, 7, 8, 11, 12],  # 10 bands (skip B1, B9, B10)
    "all13": None,             # All 13 bands
}


class SSL4EOClassifier(nn.Module):
    """ViT-Small/16 classifier with SSL4EO-S12 Sentinel-2 pretraining.

    Args:
        n_classes: Number of output classes (1 for binary with BCE, >1 for CE).
        band_indices: Indices into the 13 S2 bands to use. ``None`` = all 13.
            E.g., ``[3, 2, 1]`` for RGB (B4, B3, B2).
        freeze_backbone: If True, freeze the entire backbone.
        drop_head: Dropout rate before classification head.
        pretrained: Load SSL4EO-S12 MoCo pretrained weights.
    """

    def __init__(
        self,
        n_classes: int = 2,
        band_indices: list[int] | None = None,
        freeze_backbone: bool = True,
        drop_head: float = 0.1,
        pretrained: bool = True,
    ) -> None:
        super().__init__()

        self.band_indices = band_indices
        self.n_bands = len(band_indices) if band_indices is not None else 13

        # Load backbone from TorchGeo
        weights = ViTSmall16_Weights.SENTINEL2_ALL_MOCO if pretrained else None
        self.backbone = vit_small_patch16_224(weights=weights, num_classes=0)
        self.embed_dim = self.backbone.embed_dim  # 384

        # Adapt patch embedding if using a band subset
        if band_indices is not None:
            self._slice_patch_embed(band_indices)

        # Classification head
        self.head = nn.Sequential(
            nn.Dropout(p=drop_head),
            nn.Linear(self.embed_dim, n_classes),
        )

        # Freeze control
        if freeze_backbone:
            self.freeze_backbone()

        n_params = sum(p.numel() for p in self.parameters())
        n_trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        logger.info(
            "SSL4EOClassifier: %d bands, embed_dim=%d, params=%.1fM (trainable=%.1fM)",
            self.n_bands, self.embed_dim, n_params / 1e6, n_trainable / 1e6,
        )

    def _slice_patch_embed(self, band_indices: list[int]) -> None:
        """Slice the pretrained patch embedding to selected bands.

        Extracts the corresponding columns from the [embed_dim, 13, 16, 16]
        weight tensor, preserving spectral alignment with pretrained features.
        """
        proj = self.backbone.patch_embed.proj
        assert isinstance(proj, nn.Conv2d)

        old_weight = proj.weight.data  # [embed_dim, 13, 16, 16]
        old_bias = proj.bias

        new_weight = old_weight[:, band_indices, :, :]  # [embed_dim, n_bands, 16, 16]

        new_proj = nn.Conv2d(
            len(band_indices), old_weight.shape[0],
            kernel_size=proj.kernel_size, stride=proj.stride, padding=proj.padding,
            bias=old_bias is not None,
        )
        new_proj.weight = nn.Parameter(new_weight)
        if old_bias is not None:
            new_proj.bias = nn.Parameter(old_bias.data.clone())

        self.backbone.patch_embed.proj = new_proj
        band_names = [S2_BANDS[i] for i in band_indices]
        logger.info(
            "Sliced patch_embed: 13 -> %d bands %s",
            len(band_indices), band_names,
        )

    def freeze_backbone(self) -> None:
        """Freeze all backbone parameters (phase 1: train head only)."""
        for param in self.backbone.parameters():
            param.requires_grad = False
        logger.info("Backbone frozen — only head is trainable")

    def phase1(self) -> None:
        """Phase 1: freeze backbone, train head only."""
        self.freeze_backbone()

    def phase2(self, n_blocks: int = 4) -> None:
        """Phase 2: unfreeze last n transformer blocks for fine-tuning."""
        # Unfreeze last n blocks
        total_blocks = len(self.backbone.blocks)
        start = max(0, total_blocks - n_blocks)
        for i in range(start, total_blocks):
            for param in self.backbone.blocks[i].parameters():
                param.requires_grad = True
        # Also unfreeze final norm
        if hasattr(self.backbone, "norm"):
            for param in self.backbone.norm.parameters():
                param.requires_grad = True

        n_trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        logger.info(
            "Phase 2: unfrozen blocks[%d:%d] + norm — trainable=%.1fM",
            start, total_blocks, n_trainable / 1e6,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Args:
            x: Input tensor [B, n_bands, 224, 224].

        Returns:
            Logits [B, n_classes].
        """
        features = self.backbone(x)  # [B, embed_dim]
        return self.head(features)   # [B, n_classes]

    def get_trainable_params(self) -> list[dict[str, Any]]:
        """Return parameter groups for optimizer (differential LR)."""
        head_params = list(self.head.parameters())
        head_ids = {id(p) for p in head_params}
        backbone_params = [
            p for p in self.backbone.parameters()
            if p.requires_grad and id(p) not in head_ids
        ]

        groups = []
        if backbone_params:
            groups.append({"params": backbone_params, "name": "backbone"})
        groups.append({"params": head_params, "name": "head"})
        return groups
