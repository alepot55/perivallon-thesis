# waste/ — CLAUDE.md

Local guidance for the main baseline pillar.

## Commands

All commands run from `waste/` (this directory).

```bash
# Setup
uv venv --python 3.11 && source .venv/bin/activate && uv pip install -e ".[dev]"
python scripts/download_data.py --download-rsp   # dataset + RSP weights (~18 GB)

# Training (Hydra — all params overridable via CLI)
python scripts/train.py training.phase=both                    # full two-step (TL → FT)
python scripts/train.py training.phase=tl                      # transfer learning only
python scripts/train.py training.phase=ft                      # fine-tuning only
python scripts/train.py data.batch_size=64 training.phase=both # override batch size

# Tests
pytest tests/ -v
pytest tests/test_model.py -v
pytest tests/test_ms_adapter.py -k "test_weight_inflation" -v

# Lint & type check
ruff check src/ scripts/ tests/
ruff format --check src/ scripts/ tests/
mypy src/

# Experiments
python scripts/run_eurosat_ablation.py           # band ablation (10 configs)
python scripts/run_backbone_comparison.py        # Swin-T vs SSL4EO vs DOFA
python scripts/run_multiclass_experiment.py      # multi-class (5 coarse groups)
python scripts/run_smoke_tests.py                # lightweight validation
```

## Architecture

**Stack:** PyTorch + Lightning + Hydra + timm + torchgeo. Python 3.11.

**Two-step training** (Gibellini et al. 2025):
1. **Transfer Learning** — 10 ep, backbone frozen, head only, LR 2.236e-3
2. **Fine-Tuning** — 20 ep, last Swin stage unfrozen, LR 2.236e-4, cosine schedule

LR = paper × √5 to compensate gradient accumulation (eff. batch = 24 × 5 = 120).

**Package layout** (`src/waste_detection/`):
- `models/` — Backbone wrappers. `swin_rsp_baseline.py` is the core model with freeze/unfreeze logic. `swin_ms_adapter.py` adds MS input via 3 strategies (`weight_inflation`, `random_init_extra`, `late_fusion`). `dofa_classifier.py`, `ssl4eo_classifier.py` wrap alternative backbones.
- `training/` — Lightning modules: `lightning_module.py` (binary), `ms_module.py` (multispectral), `multiclass_module.py` (multi-class). Differential LR for backbone vs head param groups.
- `data/` — DataModules: `aerialwaste_dm.py` (RGB baseline), `aerialwaste_ms_dm.py` (MS), `eurosat_ms_dm.py` (EuroSAT ablation), `synthetic_ms_dm.py` (test data gen).
- `evaluation/metrics.py` — F1, precision, recall.

**Configs** in `configs/`. `train.yaml` is the root; composes `model/` + `data/` groups. All hyperparams CLI-overridable.

## Conventions

- Models use `timm.create_model` for Swin-T instantiation.
- RSP weights loaded from `checkpoints/rsp_swin_t_e300.pth`.
- Best baseline ckpt: `checkpoints/baseline_swin_rsp_best_f1_0.9519.ckpt`.
- Dataset stats (mean/std) precomputed in `data/processed/dataset_stats.json`.
- Tests use synthetic fixtures from `tests/conftest.py` — no real data needed.
- `vendor/aerialwaste-model/` is a git submodule (original ResNet50+FPN baseline).

## Dataset

**AerialWaste v3** — ~11,700 RGB tiles (500×500 px), 3 sources:
- AGEA orthophotos (20 cm/px GSD)
- WorldView-3 (30 cm/px GSD)
- Google Earth (50 cm/px GSD)

80/20 split, 2:1 negative:positive ratio. 22 fine-grained categories → 5 coarse groups (see `configs/data/class_groups.yaml`).

## Build

Uses `hatchling` build backend. Package installs as `waste_detection`. Ruff: line-length 100, rules E/F/I/UP/B/SIM.

## See also

- Asbestos pilot: `../asbestos/`
- Reference spectral signatures: `../spectral/`
- Reference papers: `../papers/`
