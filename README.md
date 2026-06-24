# Tesi — PERIVALLON

Master's Thesis at Politecnico di Milano, part of PERIVALLON Horizon Europe (Grant 101073952).
Multispectral waste detection from remote sensing imagery, with an asbestos-roof pilot on Lombardia.

**Author:** Alessandro Potenza · **Advisor:** Thomas Martinoli

## Workstreams

```
Tesi/
├── waste/         Main baseline — Swin-T + RSP on AerialWaste v3 (95.2% F1)
├── asbestos/      Pilot Fase 1 — asbestos roof detection on Lombardia
├── spectral/      USGS splib07a reference spectral signatures
└── papers/        Reference bibliography
```

The LaTeX thesis is on Overleaf and is not tracked here.

## Quick start

```bash
# Main baseline
cd waste/
uv venv --python 3.11 && source .venv/bin/activate && uv pip install -e ".[dev]"
python scripts/download_data.py --download-rsp        # ~18 GB
python scripts/train.py training.phase=both           # full two-step training

# Asbestos pilot briefing
cd ../asbestos/notebooks
jupyter lab 05_amianto_briefing.ipynb

# Spectral signatures
cd ../../spectral
python3 scripts/generate.py
```

See `CLAUDE.md` for full conventions and each pillar's `README.md` for details.

## Status

- [x] Baseline Swin-T + RSP on AerialWaste v3 — best F1 = **0.9519** (`waste/checkpoints/baseline_swin_rsp_best_f1_0.9519.ckpt`)
- [x] EuroSAT band ablation (10 configs, results in `waste/data/processed/eurosat_ablation_results.json`)
- [x] Backbone comparison (Swin-T vs SSL4EO vs DOFA)
- [x] Multi-class extension (5 coarse groups)
- [x] Asbestos pilot — data inventory, AOI ↔ GT coverage analysis
- [x] USGS splib07a spectral library — 9 reference plots
- [ ] Asbestos — SAM-based spectral matching on PNEO_LOMBARDIA2/3
- [ ] Asbestos — re-acquisition of PSScene over actual GT area

## References

Bibliography in `papers/`. Key entries:

- Gibellini et al. (2025) — *Waste Management Bulletin* 3. Baseline pipeline replicated.
- Torres & Fraternali (2023) — *Scientific Data* 10:63. AerialWaste v3 dataset.
- Mazzola (2024) — *Thesis*. Reference work on asbestos detection (`asbestos/reference/`).
