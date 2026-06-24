# PERIVALLON — Multispectral Waste Detection

Multispectral deep learning for illegal waste detection from remote sensing imagery.
Part of the [PERIVALLON Horizon Europe project](https://perivallon-he.eu) (Grant 101073952),
Master's Thesis at Politecnico di Milano.

## Baseline

Replication of [Gibellini et al. (2025)](https://arxiv.org/abs/2502.06607):
**Swin-T + RSP pretraining** on AerialWaste v3, achieving **92% F1 / 94.5% accuracy**
on binary waste scene classification.

## Setup

```bash
# Create environment with uv
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e ".[dev]"

# Download dataset (~18 GB)
python scripts/download_data.py --download-rsp

# Run smoke tests
pytest tests/ -v
```

## Training

Two-step procedure following the paper:

```bash
# Full training (Transfer Learning → Fine-Tuning)
python scripts/train.py training.phase=both

# With wandb logging
python scripts/train.py training.phase=both logging.use_wandb=true

# Adjust batch size for your GPU
python scripts/train.py data.batch_size=64 training.phase=both
```

## Project Structure

```
waste/
├── configs/              # Hydra YAML configs (model/, data/, train.yaml)
├── data/
│   ├── raw/              # AerialWaste v3 imagery + JSON splits
│   ├── eurosat/          # EuroSAT MS dataset (ablation)
│   ├── synthetic_ms/     # Generated MS test data
│   └── processed/        # Computed statistics, plots, ablation JSON
├── src/waste_detection/
│   ├── data/             # Datasets + DataModules (binary, MS, multiclass)
│   ├── models/           # Swin-T+RSP, MS adapter, DOFA, SSL4EO
│   ├── training/         # Lightning modules
│   └── evaluation/       # Metrics
├── checkpoints/
│   ├── rsp_swin_t_e300.pth                       # RSP pretrained backbone
│   └── baseline_swin_rsp_best_f1_0.9519.ckpt     # Our best baseline
├── notebooks/            # 01_eda, 02_eurosat_ablation, 04_backbone_multiclass
├── scripts/              # download_data, train, run_*, compute_stats
├── tests/                # Smoke tests with synthetic data
├── vendor/aerialwaste-model/   # Original ResNet50+FPN (git submodule)
└── pyproject.toml
```

## Dataset

**AerialWaste v3** — ~11,700 tiles from 3 sources:
- AGEA ortophotos (~20 cm/px GSD)
- WorldView-3 (~30 cm/px GSD)
- Google Earth (~50 cm/px GSD)

80/20 train/test split, 2:1 negative:positive ratio.

## References

- Gibellini et al., "A Deep Learning Pipeline for Solid Waste Detection in Remote Sensing Images", *Waste Management Bulletin* 3 (2025). [arXiv:2502.06607](https://arxiv.org/abs/2502.06607)
- Torres & Fraternali, "AerialWaste dataset for landfill discovery in aerial and satellite images", *Scientific Data* 10, 63 (2023). [DOI:10.1038/s41597-023-01976-9](https://doi.org/10.1038/s41597-023-01976-9)
- Wang et al., "An Empirical Study of Remote Sensing Pretraining", *IEEE TGRS* 61 (2023). [GitHub](https://github.com/ViTAE-Transformer/RSP)

## License

Research use only. Dataset under CC-BY-NC-ND 4.0.
