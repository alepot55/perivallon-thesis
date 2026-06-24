"""Evaluation utilities and metric computation."""

from __future__ import annotations

from typing import Any

import numpy as np
import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def compute_binary_metrics(
    preds: np.ndarray | torch.Tensor,
    labels: np.ndarray | torch.Tensor,
    threshold: float = 0.5,
) -> dict[str, float]:
    """Compute binary classification metrics matching Gibellini et al.

    Args:
        preds: Predicted probabilities (after sigmoid).
        labels: Ground truth binary labels.
        threshold: Classification threshold.

    Returns:
        Dict with f1, precision, recall, accuracy.
    """
    if isinstance(preds, torch.Tensor):
        preds = preds.cpu().numpy()
    if isinstance(labels, torch.Tensor):
        labels = labels.cpu().numpy()

    binary_preds = (preds >= threshold).astype(int)

    return {
        "f1": float(f1_score(labels, binary_preds)),
        "precision": float(precision_score(labels, binary_preds)),
        "recall": float(recall_score(labels, binary_preds)),
        "accuracy": float(accuracy_score(labels, binary_preds)),
    }


def compute_confusion_matrix(
    preds: np.ndarray | torch.Tensor,
    labels: np.ndarray | torch.Tensor,
    threshold: float = 0.5,
) -> np.ndarray:
    """Compute confusion matrix."""
    if isinstance(preds, torch.Tensor):
        preds = preds.cpu().numpy()
    if isinstance(labels, torch.Tensor):
        labels = labels.cpu().numpy()

    binary_preds = (preds >= threshold).astype(int)
    return confusion_matrix(labels, binary_preds)


def format_metrics(metrics: dict[str, float]) -> str:
    """Format metrics dict as a readable string."""
    return " | ".join(f"{k}: {v:.4f}" for k, v in metrics.items())
