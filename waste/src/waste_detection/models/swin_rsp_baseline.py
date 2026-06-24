"""Swin-T with RSP pretraining for binary waste classification.

Replicates the best configuration from Gibellini et al. (2025):
  - Architecture: Swin-T (timm) with RSP weights from Million-AID
  - Head: single FC neuron + sigmoid for binary classification
  - Two-step training: Transfer Learning (frozen backbone) → Fine-Tuning (stage 4 unfrozen)

Reference: arXiv:2502.06607
RSP weights: https://github.com/ViTAE-Transformer/RSP
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import timm
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)


class SwinRSPClassifier(nn.Module):
    """Swin-T binary classifier with RSP pretraining support.

    Args:
        pretrained_imagenet: Use ImageNet pretrained weights from timm.
        rsp_checkpoint_path: Path to RSP checkpoint for Million-AID pretrained weights.
            Mutually exclusive with ``pretrained_imagenet``.
        num_classes: Number of output classes (1 for binary with BCE).
        freeze_backbone: If True, freeze the entire backbone (for Transfer Learning phase).
        unfreeze_last_stage: If True, unfreeze only the last Swin stage (for Fine-Tuning phase).
    """

    def __init__(
        self,
        pretrained_imagenet: bool = False,
        rsp_checkpoint_path: str | Path | None = None,
        num_classes: int = 1,
        image_size: int = 224,
        freeze_backbone: bool = False,
        unfreeze_last_stage: bool = False,
        drop_rate: float = 0.1,
    ) -> None:
        super().__init__()

        # Create Swin-T backbone via timm (uses timm default drop_path_rate)
        self.backbone = timm.create_model(
            "swin_tiny_patch4_window7_224",
            pretrained=pretrained_imagenet and rsp_checkpoint_path is None,
            num_classes=0,  # remove classifier head
            img_size=image_size,
        )
        embed_dim = self.backbone.num_features  # 768 for Swin-T

        # Load RSP pretrained weights if provided
        if rsp_checkpoint_path is not None:
            self._load_rsp_weights(Path(rsp_checkpoint_path))

        # Binary classification head with dropout
        self.head = nn.Sequential(
            nn.Dropout(p=drop_rate),
            nn.Linear(embed_dim, num_classes),
        )

        # Freeze control
        if freeze_backbone:
            self.freeze_backbone()
        if unfreeze_last_stage:
            self.unfreeze_last_stage()

    def _load_rsp_weights(self, checkpoint_path: Path) -> None:
        """Load backbone weights from an RSP checkpoint.

        Handles the key naming difference between the original Microsoft Swin
        implementation (used by RSP/ViTAE-Transformer) and timm's Swin:
        - Microsoft: downsample at the END of each stage → layers.{i}.downsample
        - timm: downsample at the START of the next stage → layers.{i+1}.downsample

        Also skips non-parameter buffers (relative_position_index, attn_mask)
        that differ between implementations.
        """
        if not checkpoint_path.exists():
            logger.warning("RSP checkpoint not found at %s, using random init", checkpoint_path)
            return

        ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
        state_dict = ckpt.get("model", ckpt.get("state_dict", ckpt))

        # Keys to skip: head, buffers that differ between implementations
        skip_prefixes = ("head.", "fc.")
        skip_suffixes = ("relative_position_index", "attn_mask")

        backbone_state = {}
        for k, v in state_dict.items():
            k = k.removeprefix("module.")

            if any(k.startswith(p) for p in skip_prefixes):
                continue
            if any(k.endswith(s) for s in skip_suffixes):
                continue

            # Remap downsample keys: RSP layers.{i}.downsample → timm layers.{i+1}.downsample
            if ".downsample." in k:
                parts = k.split(".")
                layer_idx = int(parts[1])
                parts[1] = str(layer_idx + 1)
                k = ".".join(parts)

            backbone_state[k] = v

        missing, unexpected = self.backbone.load_state_dict(backbone_state, strict=False)
        # Filter expected missing keys (buffers)
        missing = [m for m in missing if not any(m.endswith(s) for s in skip_suffixes)]
        if missing:
            logger.info("RSP load — missing keys: %s", missing)
        if unexpected:
            logger.warning("RSP load — unexpected keys: %s", unexpected)
        logger.info("Loaded RSP weights from %s (%d keys)", checkpoint_path, len(backbone_state))

    def freeze_backbone(self) -> None:
        """Freeze all backbone parameters (Transfer Learning phase)."""
        for param in self.backbone.parameters():
            param.requires_grad = False
        logger.info("Backbone frozen — only head is trainable")

    def unfreeze_last_stage(self) -> None:
        """Unfreeze the 4th (last) Swin stage for fine-tuning."""
        # Swin-T has layers: [layers.0, layers.1, layers.2, layers.3]
        # Stage 4 = layers.3
        for name, param in self.backbone.named_parameters():
            if "layers.3" in name or "norm" in name:
                param.requires_grad = True
        logger.info("Last Swin stage (layers.3) + norm unfrozen for fine-tuning")

    def unfreeze_all(self) -> None:
        """Unfreeze everything."""
        for param in self.parameters():
            param.requires_grad = True

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Args:
            x: Input tensor [B, 3, H, W].

        Returns:
            Logits tensor [B, num_classes] (pre-sigmoid).
        """
        features = self.backbone(x)  # [B, embed_dim]
        logits = self.head(features)  # [B, num_classes]
        return logits

    def get_trainable_params(self) -> list[dict[str, Any]]:
        """Return parameter groups for optimizer (useful for differential LR)."""
        head_params = list(self.head.parameters())
        head_ids = {id(p) for p in head_params}
        backbone_params = [p for p in self.backbone.parameters() if p.requires_grad and id(p) not in head_ids]

        groups = []
        if backbone_params:
            groups.append({"params": backbone_params, "name": "backbone"})
        groups.append({"params": head_params, "name": "head"})
        return groups
