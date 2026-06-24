"""DOFA (Dynamic One-For-All) classifier with wavelength-conditioned input.

DOFA uses a hypernetwork that generates patch embedding weights conditioned
on input wavelengths, enabling a single pretrained model to handle arbitrary
band configurations without retraining the stem layer.

Loaded via TorchGeo with MAE pretrained weights from SatlasPretrain,
Five-Billion-Pixels, and HySpecNet-11k.

Reference:
    - DOFA: https://arxiv.org/abs/2403.15356
    - TorchGeo: https://torchgeo.readthedocs.io/
"""

from __future__ import annotations

import logging
from typing import Any

import torch
import torch.nn as nn
from torchgeo.models import dofa_base_patch16_224, DOFABase16_Weights

logger = logging.getLogger(__name__)

# Center wavelengths (nm) for Sentinel-2 bands
S2_WAVELENGTHS: dict[int, float] = {
    0: 443, 1: 490, 2: 560, 3: 665, 4: 705, 5: 740,
    6: 783, 7: 842, 8: 865, 9: 940, 10: 1375, 11: 1610, 12: 2190,
}
S2_ALL_WAVELENGTHS = [S2_WAVELENGTHS[i] for i in range(13)]

# Common wavelength presets
WAVELENGTH_PRESETS: dict[str, list[float]] = {
    "rgb": [665.0, 560.0, 490.0],                                    # B4, B3, B2
    "rgbn": [665.0, 560.0, 490.0, 842.0],                           # + B8
    "ms6": [665.0, 560.0, 490.0, 842.0, 1610.0, 2190.0],           # + SWIR
    "s2_all": [float(S2_WAVELENGTHS[i]) for i in range(13)],        # All 13
    "aerialwaste_rgb": [665.0, 560.0, 490.0],                       # AerialWaste R,G,B
    "wv3_vnir": [427.0, 478.0, 546.0, 608.0, 659.0, 724.0, 833.0, 949.0],  # WV-3 8 VNIR
}


class DOFAClassifier(nn.Module):
    """DOFA ViT-Base/16 classifier with wavelength-conditioned input.

    Unlike SSL4EOClassifier which slices pretrained weights, DOFA's
    hypernetwork dynamically generates patch embedding weights based on
    input wavelengths. The same model handles any band configuration.

    Args:
        n_classes: Number of output classes (1 for binary with BCE, >1 for CE).
        wavelengths: List of center wavelengths (nm) for input bands.
            Determines the number of input channels at forward time.
        freeze_backbone: If True, freeze the entire backbone.
        drop_head: Dropout rate before classification head.
        pretrained: Load DOFA MAE pretrained weights.
    """

    def __init__(
        self,
        n_classes: int = 2,
        wavelengths: list[float] | None = None,
        freeze_backbone: bool = True,
        drop_head: float = 0.1,
        pretrained: bool = True,
    ) -> None:
        super().__init__()

        self.wavelengths = wavelengths or S2_ALL_WAVELENGTHS
        self.n_bands = len(self.wavelengths)

        # Load DOFA backbone from TorchGeo
        weights = DOFABase16_Weights.DOFA_MAE if pretrained else None
        self.backbone = dofa_base_patch16_224(
            weights=weights, num_classes=0, global_pool=True,
        )
        self.embed_dim = self.backbone.embed_dim  # 768

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
            "DOFAClassifier: %d bands (%.0f-%.0fnm), embed_dim=%d, "
            "params=%.1fM (trainable=%.1fM)",
            self.n_bands,
            min(self.wavelengths), max(self.wavelengths),
            self.embed_dim, n_params / 1e6, n_trainable / 1e6,
        )

    def freeze_backbone(self) -> None:
        """Freeze all backbone parameters."""
        for param in self.backbone.parameters():
            param.requires_grad = False
        logger.info("DOFA backbone frozen — only head is trainable")

    def phase1(self) -> None:
        """Phase 1: freeze backbone, train head only."""
        self.freeze_backbone()

    def phase2(self, n_blocks: int = 4) -> None:
        """Phase 2: unfreeze last n transformer blocks for fine-tuning."""
        total_blocks = len(self.backbone.blocks)
        start = max(0, total_blocks - n_blocks)
        for i in range(start, total_blocks):
            for param in self.backbone.blocks[i].parameters():
                param.requires_grad = True
        if hasattr(self.backbone, "norm"):
            for param in self.backbone.norm.parameters():
                param.requires_grad = True

        n_trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        logger.info(
            "DOFA Phase 2: unfrozen blocks[%d:%d] + norm — trainable=%.1fM",
            start, total_blocks, n_trainable / 1e6,
        )

    def forward(
        self,
        x: torch.Tensor,
        wavelengths: list[float] | None = None,
    ) -> torch.Tensor:
        """Forward pass.

        Args:
            x: Input tensor [B, n_bands, 224, 224].
            wavelengths: Override wavelengths for this forward call.
                If None, uses self.wavelengths set at init.

        Returns:
            Logits [B, n_classes].
        """
        wl = wavelengths or self.wavelengths
        features = self.backbone(x, wl)  # [B, embed_dim]
        return self.head(features)       # [B, n_classes]

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
