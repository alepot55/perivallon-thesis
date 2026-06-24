"""Pluggable classification heads for binary and multi-class waste tasks.

Supports linear probe, MLP (1 hidden layer), and attention pooling heads.
Includes class-weighted CrossEntropyLoss and focal loss for the severely
imbalanced 22-class AerialWaste taxonomy.

Reference:
    - AerialWaste v3: 22 categories, Glass=6 to Heaps not delimited=355
    - Focal Loss: Lin et al. (2017), https://arxiv.org/abs/1708.02002
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
import torch.nn.functional as F

logger = logging.getLogger(__name__)

# Coarse 5-class grouping for rare-class aggregation
COARSE_GROUPS: dict[str, list[str]] = {
    "organic": ["Fire Wood", "Sludge-Zootechnical waste-Manure"],
    "construction": [
        "Rubble/excavated earth and rocks",
        "Corrugated sheets (presumed asbestos-cement)",
        "Stone/marble processing waste",
        "Asphalt milling",
        "Foundry waste",
    ],
    "metal_plastic": [
        "Scrap",
        "Big bags",
        "Cisterns",
        "Drums bins",
        "Tires",
        "Plastic",
    ],
    "bulky": [
        "Bulky items",
        "Vehicles",
        "Domestic appliances",
        "Paper",
        "Glass",
        "Full pallets",
        "Furniture",
    ],
    "storage": [
        "Heaps not delimited",
        "Full container",
        "Delimited heaps (by barriers/walls/etc)",
    ],
}


class FocalLoss(nn.Module):
    """Focal loss for multi-class classification (Lin et al., 2017).

    Args:
        weight: Per-class weights tensor [n_classes].
        gamma: Focusing parameter (higher = more focus on hard examples).
        reduction: 'mean' or 'sum'.
    """

    def __init__(
        self,
        weight: torch.Tensor | None = None,
        gamma: float = 2.0,
        reduction: str = "mean",
    ) -> None:
        super().__init__()
        self.gamma = gamma
        self.reduction = reduction
        self.register_buffer("weight", weight)

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        ce_loss = F.cross_entropy(logits, targets, weight=self.weight, reduction="none")
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss

        if self.reduction == "mean":
            return focal_loss.mean()
        elif self.reduction == "sum":
            return focal_loss.sum()
        return focal_loss


class WasteCategoryHead(nn.Module):
    """Pluggable classification head for binary and 22-class waste tasks.

    Args:
        in_features: Dimension of input features from backbone.
        n_classes: Number of output classes (2 for binary, 22 for full taxonomy).
        head_type: ``"linear"``, ``"mlp"`` (1 hidden layer), or ``"attention"``.
        dropout: Dropout probability.
    """

    def __init__(
        self,
        in_features: int,
        n_classes: int = 2,
        head_type: str = "mlp",
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        self.in_features = in_features
        self.n_classes = n_classes
        self.head_type = head_type

        if head_type == "linear":
            self.head = nn.Sequential(
                nn.Dropout(p=dropout),
                nn.Linear(in_features, n_classes),
            )
        elif head_type == "mlp":
            hidden = in_features // 2
            self.head = nn.Sequential(
                nn.Linear(in_features, hidden),
                nn.GELU(),
                nn.Dropout(p=dropout),
                nn.Linear(hidden, n_classes),
            )
        elif head_type == "attention":
            self.query = nn.Linear(in_features, in_features)
            self.head = nn.Sequential(
                nn.Dropout(p=dropout),
                nn.Linear(in_features, n_classes),
            )
        else:
            raise ValueError(f"Unknown head_type '{head_type}'. Use 'linear', 'mlp', or 'attention'.")

        logger.info(
            "WasteCategoryHead: %s, in=%d, out=%d, dropout=%.2f",
            head_type, in_features, n_classes, dropout,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Args:
            x: Feature tensor [B, in_features].

        Returns:
            Logits [B, n_classes].
        """
        if self.head_type == "attention":
            # Self-attention pooling: query-based reweighting
            attn_weights = torch.softmax(self.query(x), dim=-1)
            x = x * attn_weights
            return self.head(x)
        return self.head(x)


def compute_class_weights(
    annotation_path: str | Path,
    n_classes: int = 22,
) -> torch.Tensor:
    """Compute inverse-frequency class weights from AerialWaste annotations.

    Uses the formula: weight_c = N_total / (n_classes * N_c)
    where N_c is the count of images containing category c.

    Args:
        annotation_path: Path to training.json.
        n_classes: Number of classes (22).

    Returns:
        Tensor of shape [n_classes] with class weights.
    """
    with open(annotation_path) as f:
        data = json.load(f)

    counts = torch.zeros(n_classes)
    for img in data["images"]:
        for cat_id in img["categories"]:
            if 1 <= cat_id <= n_classes:
                counts[cat_id - 1] += 1  # categories are 1-indexed

    # Avoid division by zero for classes with 0 samples
    counts = counts.clamp(min=1)
    total = counts.sum()
    weights = total / (n_classes * counts)

    return weights


def build_loss(
    loss_type: str = "ce",
    class_weights: torch.Tensor | None = None,
    focal_gamma: float = 2.0,
) -> nn.Module:
    """Build a classification loss function.

    Args:
        loss_type: ``"ce"`` for CrossEntropyLoss, ``"focal"`` for FocalLoss.
        class_weights: Per-class weight tensor.
        focal_gamma: Gamma for focal loss.

    Returns:
        Loss module.
    """
    if loss_type == "ce":
        return nn.CrossEntropyLoss(weight=class_weights)
    elif loss_type == "focal":
        return FocalLoss(weight=class_weights, gamma=focal_gamma)
    else:
        raise ValueError(f"Unknown loss_type '{loss_type}'. Use 'ce' or 'focal'.")
