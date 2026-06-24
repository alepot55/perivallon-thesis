# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**PERIVALLON** — Multispectral waste detection from remote sensing imagery.
Master's Thesis (Politecnico di Milano), part of PERIVALLON Horizon Europe (Grant 101073952).
Advisor: Thomas Martinoli.

Three parallel workstreams, organized as top-level pillars:

| Pillar | Purpose | Main artifact |
|---|---|---|
| `waste/` | Main baseline — illegal waste classification on AerialWaste v3 | Swin-T + RSP, 95.2% F1 (best ckpt) |
| `asbestos/` | Pilot Fase 1 — asbestos roof detection on Lombardia (SuperDove + SAM) | WFS ground truth + Planet PSScene |
| `spectral/` | Reference spectral signatures from USGS splib07a | 9 plots + PDF + CSVs |

Plus `papers/` (reference bibliography) and the LaTeX thesis (kept on Overleaf, not in this repo).

## Layout

```
Tesi/
├── README.md          ← top-level index
├── CLAUDE.md          ← this file
├── waste/             ← FILONE 1: deep-learning baseline (was perivallon-waste/)
├── asbestos/          ← FILONE 2: parallel task amianto Lombardia
├── spectral/          ← FILONE 3: spectral signatures (was firme-spettrali/)
└── papers/            ← reference bibliography (PDFs)
```

Each pillar has its own `README.md`. The `waste/` pillar has its own `CLAUDE.md` with build/run details.

## Quick commands

### waste/ (main baseline)
```bash
cd waste
uv venv --python 3.11 && source .venv/bin/activate && uv pip install -e ".[dev]"
python scripts/download_data.py --download-rsp     # dataset + RSP weights (~18 GB)
python scripts/train.py training.phase=both        # full two-step training
pytest tests/ -v
ruff check src/ scripts/ tests/ && mypy src/
```

### asbestos/ (briefing + analysis)
```bash
cd asbestos/notebooks
jupyter lab 05_amianto_briefing.ipynb              # uses geopandas/rasterio/folium
```
Reuses the `waste/` Python environment (geopandas, rasterio already pulled in).

### spectral/ (regenerate plots)
```bash
cd spectral
python3 scripts/generate.py                        # rebuilds figures/, csv/, PDF
```

## Conventions

- **Two-step training** (Gibellini et al. 2025): Transfer Learning (10 ep, head only, LR 2.236e-3) → Fine-Tuning (20 ep, last Swin stage unfrozen, LR 2.236e-4). LR = paper × √5 to compensate gradient accumulation (eff. batch = 24 × 5 = 120).
- **Models** in `waste/src/waste_detection/models/`: `swin_rsp_baseline.py` (core), `swin_ms_adapter.py` (multispectral via weight_inflation / random_init_extra / late_fusion), `dofa_classifier.py`, `ssl4eo_classifier.py`.
- **Configs** via Hydra YAML in `waste/configs/`. All hyperparams CLI-overridable.
- **Tests** use synthetic fixtures from `waste/tests/conftest.py` — no real data needed.
- **Asbestos paths** in the notebook resolve via `ROOT = '/home/alepot55/Desktop/uni/Tesi'`, then `f'{ROOT}/asbestos/data'`, `f'{ROOT}/spectral'`.

## Checkpoints

- `waste/checkpoints/rsp_swin_t_e300.pth` — RSP pretrained Swin-T backbone (input weights).
- `waste/checkpoints/baseline_swin_rsp_best_f1_0.9519.ckpt` — current best result (val F1 = **0.9519**, epoch 13 of the FT phase).
- Heavy intermediate ckpts (eurosat_ablation, backbone_comparison, all non-best baseline epochs) have been removed — results are preserved in `waste/data/processed/eurosat_ablation_results.json` and in the analysis notebooks.

## Datasets

- **AerialWaste v3** (`waste/data/raw/`): ~11.7k RGB tiles 500×500 px, 3 sources (AGEA 20 cm, WV3 30 cm, Google Earth 50 cm). 80/20 split, 2:1 neg:pos. 22 fine-grained → 5 coarse groups (`waste/configs/data/class_groups.yaml`).
- **EuroSAT MS** (`waste/data/eurosat/`): 13-band Sentinel-2, used for band-ablation experiments.
- **Lombardia WFS** (`asbestos/data/*.gpkg`): `Mappatura_2020` (10,903 roofs) + `Mappature_precedenti` (50,131) + aree + comuni + province, all in EPSG:32632.
- **Planet PSScene** (`asbestos/data/planet/PSScene/`): 7 strip 2026-03-30 (`prima prova`), 4-band SR. Coverage ↔ GT = 0 (out-of-area), kept as pipeline-test data only.

## Disk footprint (current)

| Pillar | Size | Notes |
|---|---|---|
| `waste/` | ~23 GB | Dominated by `data/raw/images/` (17 GB) + `data/eurosat/` (4.8 GB) |
| `asbestos/` | ~1.9 GB | Mostly Planet PSScene tiles |
| `spectral/` | 29 MB | Library + plots + CSVs |
| `papers/` | 43 MB | Reference PDFs |
| **Total** | **~25 GB** | |

The `.venv/` (~8 GB) is **not committed** — regenerate with `cd waste && uv venv --python 3.11 && uv pip install -e ".[dev]"`. AerialWaste imagery zips (~17 GB) are also gone — re-download with `python scripts/download_data.py` if needed (the extracted images in `data/raw/images/` are sufficient for training).
