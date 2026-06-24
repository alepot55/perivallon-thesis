#!/usr/bin/env python3
"""Generate all spectral signature plots, PDF, and CSVs.

Usage:  cd spectral && python3 scripts/generate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spectral_plots import config
from spectral_plots.data import (
    download_ecostress_rubber,
    load_all,
    save_combined_csv,
    save_individual_csv,
)
from spectral_plots.plotting import generate_pdf, generate_plot

ZIP  = ROOT / "data" / "ASCIIdata_splib07a.zip"
FIGS = ROOT / "figures"
CSV  = ROOT / "csv"
CSVP = CSV / "per_material"

FIGS.mkdir(parents=True, exist_ok=True)
CSV.mkdir(parents=True, exist_ok=True)
CSVP.mkdir(parents=True, exist_ok=True)

# ── Load ──────────────────────────────────────────────────────────────────────
print("Loading USGS splib07a …")
spectra = load_all(ZIP)
print(f"  {len(spectra)} spectra")

print("ECOSTRESS …")
rub_wl, rub_r = download_ecostress_rubber()
print(f"  rubber: {'OK' if rub_wl is not None else 'failed (non-critical)'}")

# ── Individual CSVs ───────────────────────────────────────────────────────────
for name, (_fp, _wt, sid) in config.SPECTRA.items():
    wl, r = spectra[name]
    save_individual_csv(CSVP, name, wl, r, sid)
if rub_wl is not None:
    save_individual_csv(CSVP, "Rubber_roofing", rub_wl, rub_r, "0795uuurbr")

# ── Plots ─────────────────────────────────────────────────────────────────────
print(f"\nGenerating {len(config.PLOTS)} plots …")
produced = []
for spec in config.PLOTS:
    path = generate_plot(spec, spectra, FIGS)
    produced.append(path)
    print(f"  ✓ {spec['filename']}")

# ── PDF ───────────────────────────────────────────────────────────────────────
pdf_path = FIGS / "spectral_signature_library.pdf"
generate_pdf(produced, pdf_path)
print(f"  ✓ spectral_signature_library.pdf ({len(produced)} pages)")

# ── Combined CSV ──────────────────────────────────────────────────────────────
csv_path = CSV / "spectral_signatures_all_materials.csv"
save_combined_csv(csv_path, spectra)
print(f"  ✓ spectral_signatures_all_materials.csv ({len(config.CSV_COLUMNS)} × 2151)")

print(f"\nDone → {FIGS}")
