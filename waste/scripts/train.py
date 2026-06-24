#!/usr/bin/env python3
"""Training script for waste classification with Hydra config.

Implements the two-step training procedure from Gibellini et al. (2025):
  Step 1 — Transfer Learning: frozen backbone, LR=1e-3
  Step 2 — Fine-Tuning: last stage unfrozen, LR=1e-4

Usage:
    # Full two-step training (default)
    python scripts/train.py

    # Override config
    python scripts/train.py data.batch_size=64 trainer.max_epochs=100

    # Only transfer learning phase
    python scripts/train.py training.phase=tl

    # With wandb logging
    python scripts/train.py logging.use_wandb=true
"""

from __future__ import annotations

import logging
from pathlib import Path

import hydra
import pytorch_lightning as pl
import torch
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint, RichProgressBar
from pytorch_lightning.loggers import CSVLogger, WandbLogger

from waste_detection.data.aerialwaste_dm import AerialWasteDataModule
from waste_detection.training.lightning_module import WasteClassifierModule

logger = logging.getLogger(__name__)


def set_seed(seed: int, deterministic: bool = False) -> None:
    pl.seed_everything(seed, workers=True)
    torch.backends.cudnn.deterministic = deterministic
    torch.backends.cudnn.benchmark = not deterministic  # faster with fixed input sizes
    torch.set_float32_matmul_precision("high")  # use TF32 on Tensor Cores


def build_loggers(cfg: DictConfig) -> list:
    loggers = []
    csv_dir = Path(cfg.logging.csv_dir)
    csv_dir.mkdir(parents=True, exist_ok=True)
    loggers.append(CSVLogger(save_dir=str(csv_dir), name="waste_detection"))

    if cfg.logging.use_wandb:
        loggers.append(
            WandbLogger(
                project=cfg.logging.wandb_project,
                entity=cfg.logging.wandb_entity,
                config=OmegaConf.to_container(cfg, resolve=True),
            )
        )
    return loggers


def build_callbacks(cfg: DictConfig) -> list:
    ckpt_dir = Path(cfg.checkpoint.dirpath)
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    return [
        ModelCheckpoint(
            dirpath=str(ckpt_dir),
            filename=cfg.checkpoint.filename,
            monitor=cfg.checkpoint.monitor,
            mode=cfg.checkpoint.mode,
            save_top_k=cfg.checkpoint.save_top_k,
        ),
        EarlyStopping(
            monitor=cfg.early_stopping.monitor,
            patience=cfg.early_stopping.patience,
            min_delta=cfg.early_stopping.min_delta,
            mode=cfg.early_stopping.mode,
        ),
        RichProgressBar(),
    ]


def build_trainer(cfg: DictConfig, phase: str, max_epochs: int) -> pl.Trainer:
    return pl.Trainer(
        max_epochs=max_epochs,
        accelerator=cfg.trainer.accelerator,
        devices=cfg.trainer.devices,
        precision=cfg.trainer.precision,
        log_every_n_steps=cfg.trainer.log_every_n_steps,
        accumulate_grad_batches=cfg.trainer.get("accumulate_grad_batches", 1),
        deterministic=cfg.trainer.deterministic,
        logger=build_loggers(cfg),
        callbacks=build_callbacks(cfg),
        default_root_dir=f"outputs/{phase}",
    )


@hydra.main(config_path="../configs", config_name="train", version_base="1.3")
def main(cfg: DictConfig) -> None:
    logger.info("Configuration:\n%s", OmegaConf.to_yaml(cfg))
    set_seed(cfg.seed, deterministic=cfg.trainer.deterministic)

    # Data
    dm = AerialWasteDataModule(
        root=cfg.data.root,
        image_size=cfg.data.image_size,
        target_gsd=cfg.data.target_gsd,
        batch_size=cfg.data.batch_size,
        num_workers=cfg.data.num_workers,
        val_fraction=cfg.data.val_fraction,
        mean=tuple(cfg.data.mean),
        std=tuple(cfg.data.std),
        seed=cfg.seed,
    )

    model_cfg = {
        "pretrained_imagenet": cfg.model.pretrained_imagenet,
        "rsp_checkpoint_path": cfg.model.rsp_checkpoint_path,
        "num_classes": cfg.model.num_classes,
        "image_size": cfg.model.image_size,
    }

    # Phase 1: Transfer Learning
    if cfg.training.phase in ("tl", "both"):
        logger.info("=" * 60)
        logger.info("PHASE 1: Transfer Learning (frozen backbone)")
        logger.info("=" * 60)

        module = WasteClassifierModule(
            model_cfg={**model_cfg, "freeze_backbone": True, "unfreeze_last_stage": False},
            lr=cfg.training.lr_tl,
            training_phase="tl",
            threshold=cfg.training.threshold,
            weight_decay=cfg.training.weight_decay,
        )

        trainer = build_trainer(cfg, "tl", cfg.training.tl_epochs)
        trainer.fit(module, dm)

        # Save TL checkpoint path for FT phase
        tl_ckpt = trainer.checkpoint_callback.best_model_path
        logger.info("TL best checkpoint: %s", tl_ckpt)

    # Phase 2: Fine-Tuning
    if cfg.training.phase in ("ft", "both"):
        logger.info("=" * 60)
        logger.info("PHASE 2: Fine-Tuning (last stage unfrozen)")
        logger.info("=" * 60)

        if cfg.training.phase == "both" and tl_ckpt:
            # Load from TL checkpoint and switch to FT
            module = WasteClassifierModule.load_from_checkpoint(tl_ckpt)
            module.switch_to_finetune(lr=cfg.training.lr_ft)
        else:
            module = WasteClassifierModule(
                model_cfg={**model_cfg, "freeze_backbone": True, "unfreeze_last_stage": True},
                lr=cfg.training.lr_ft,
                training_phase="ft",
                threshold=cfg.training.threshold,
                weight_decay=cfg.training.weight_decay,
            )

        trainer = build_trainer(cfg, "ft", cfg.training.ft_epochs)
        trainer.fit(module, dm)

        ft_ckpt = trainer.checkpoint_callback.best_model_path
        logger.info("FT best checkpoint: %s", ft_ckpt)

        # Test
        logger.info("Running test evaluation...")
        trainer.test(module, dm, ckpt_path=ft_ckpt)

    logger.info("Training complete!")


if __name__ == "__main__":
    main()
