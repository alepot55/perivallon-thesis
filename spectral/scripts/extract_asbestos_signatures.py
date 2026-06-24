#!/usr/bin/env python3
"""Extract asbestos (cemento-amianto) reference signatures from USGS splib07a.

Produces, in figures/asbestos/ and csv/asbestos/:
  1. Pure asbestos-mineral signatures (chrysotile x3, tremolite, actinolite,
     antigorite) with diagnostic absorption annotations.
  2. Modelled asbestos-cement (AC) roof at 3 weathering levels vs roof confusers.
  3. Sensor view: the same signatures resampled to SuperDove / Sentinel-2 /
     WV-3 SWIR bands (Gaussian SRF from band center + FWHM).
  4. SAM separability matrix: spectral angle between the weathered AC roof and
     each confuser, per band set — quantifies what each sensor can separate.

AC roof model: linear mix chrysotile + concrete. Weathering exposes fibers
(Cilia et al. 2015), so the chrysotile fraction rises with aging:
new 10% / moderate 25% / weathered 40%. Honest label: "modelled".

Usage:  cd spectral && python3 scripts/extract_asbestos_signatures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spectral_plots import config
from spectral_plots.data import load_spectrum

ZIP = ROOT / "data" / "ASCIIdata_splib07a.zip"
FIGS = ROOT / "figures" / "asbestos"
CSV = ROOT / "csv" / "asbestos"

_CM = "ASCIIdata_splib07a/ChapterM_Minerals"
_CA = "ASCIIdata_splib07a/ChapterA_ArtificialMaterials"

# name → (zip path, group)
SOURCES = {
    "Chrysotile HS323.1B":        (f"{_CM}/splib07a_Chrysotile_HS323.1B_ASDNGa_AREF.txt", "asbestos"),
    "Chrysotile coarse fib":      (f"{_CM}/splib07a_Chrysotile_ML99-12A_Coar_Fib_ASDFRb_AREF.txt", "asbestos"),
    "Chrysotile fine fib":        (f"{_CM}/splib07a_Chrysotile_ML99-12C_Fine_Fib_ASDFRb_AREF.txt", "asbestos"),
    "Tremolite":                  (f"{_CM}/splib07a_Tremolite_HS18.3B_ASDFRc_AREF.txt", "asbestos"),
    "Actinolite":                 (f"{_CM}/splib07a_Actinolite_HS116.3B_ASDFRb_AREF.txt", "asbestos"),
    "Antigorite":                 (f"{_CM}/splib07a_Antigorite_NMNH96917.a_gt250_ASDNGb_AREF.txt", "asbestos"),
    "Concrete (road)":            (f"{_CA}/splib07a_Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.txt", "confuser"),
    "Brick red (terracotta)":     (f"{_CA}/splib07a_Brick_GDS349_Paving_Red_ASDFRa_AREF.txt", "confuser"),
    "Asphalt tar roof":           (f"{_CA}/splib07a_Asphalt_Tar_GDS346_Blck_Roof_ASDFRa_AREF.txt", "confuser"),
    "Asphalt shingle grey":       (f"{_CA}/splib07a_Asphalt_Shingle_GDS367_DkGry_ASDFRa_AREF.txt", "confuser"),
    "Fiberglass roofing white":   (f"{_CA}/splib07a_Fiberglass_GDS335_Wh_Roofing_ASDFRa_AREF.txt", "confuser"),
    "Galvanized metal roof":      (f"{_CA}/splib07a_GalvanizedSheetMetal_GDS334_ASDFRa_AREF.txt", "confuser"),
}

# (label, chrysotile fraction) — Cilia 2015: weathering exposes fibers
AC_LEVELS = [("AC roof new", 0.10), ("AC roof moderate", 0.25), ("AC roof weathered", 0.40)]

BAND_SETS = {
    "SuperDove (8b VNIR)": config.SD_BANDS,
    "Sentinel-2 (11b)": config.S2_BANDS,
    "WV-3 SWIR (8b)": config.WV3_BANDS,
}

DIAGNOSTICS = [  # (nm, label)
    (1385, "OH 1.38–1.40 µm"),
    (2320, "Mg-OH 2.31–2.33 µm"),
]


def resample(wl: np.ndarray, r: np.ndarray, bands: list[tuple]) -> np.ndarray:
    """Convolve a spectrum with Gaussian SRFs (center, fwhm) → band values."""
    out = []
    for _label, center, fwhm in bands:
        sigma = fwhm / 2.355
        w = np.exp(-0.5 * ((wl - center) / sigma) ** 2)
        mask = np.isfinite(r) & (w > 1e-3)
        out.append(np.sum(r[mask] * w[mask]) / np.sum(w[mask]) if mask.any() else np.nan)
    return np.array(out)


def sam_deg(a: np.ndarray, b: np.ndarray) -> float:
    """Spectral Angle Mapper between two vectors, in degrees (nan-aware)."""
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 2:
        return np.nan
    a, b = a[m], b[m]
    cos = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))))


def main() -> None:
    FIGS.mkdir(parents=True, exist_ok=True)
    CSV.mkdir(parents=True, exist_ok=True)

    spectra = {name: load_spectrum(ZIP, fp) for name, (fp, _g) in SOURCES.items()}
    wl = spectra["Chrysotile HS323.1B"][0]  # common ASD grid (2151 ch)

    # AC roof models on the common grid
    chry = spectra["Chrysotile HS323.1B"][1]
    conc = spectra["Concrete (road)"][1]
    ac = {label: f * chry + (1 - f) * conc for label, f in AC_LEVELS}

    # ── CSV: full-resolution signatures ─────────────────────────────────────
    import csv as _csv
    all_curves = {**{k: v[1] for k, v in spectra.items()}, **ac}
    with open(CSV / "asbestos_signatures_full.csv", "w", newline="") as f:
        w = _csv.writer(f)
        w.writerow(["wavelength_nm"] + list(all_curves))
        for i in range(len(wl)):
            w.writerow([f"{wl[i]:.1f}"] + [f"{c[i]:.5f}" if np.isfinite(c[i]) else "" for c in all_curves.values()])

    # ── CSV + data: per-sensor resampled values ─────────────────────────────
    resampled: dict[str, dict[str, np.ndarray]] = {}
    for sensor, bands in BAND_SETS.items():
        resampled[sensor] = {n: resample(wl, c, bands) for n, c in all_curves.items()}
        with open(CSV / f"asbestos_resampled_{sensor.split(' ')[0].replace('-', '')}.csv", "w", newline="") as f:
            w = _csv.writer(f)
            w.writerow(["band", "center_nm"] + list(all_curves))
            for bi, (blabel, center, _fw) in enumerate(bands):
                w.writerow([blabel, center] + [f"{resampled[sensor][n][bi]:.5f}" for n in all_curves])

    # ── Fig 1: pure asbestos minerals ───────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 6))
    for name, (fp, g) in SOURCES.items():
        if g != "asbestos":
            continue
        ax.plot(*_clean(spectra[name]), lw=1.6, label=name)
    for nm, label in DIAGNOSTICS:
        ax.axvline(nm, color="0.4", lw=0.8, ls=":")
        ax.text(nm, ax.get_ylim()[1] * 0.97, label, rotation=90, va="top", ha="right", fontsize=8, color="0.3")
    ax.axvspan(885, 2500, color="0.93", zorder=0)
    ax.text(1650, 0.02, "not seen by SuperDove (no SWIR)", fontsize=8, color="0.45", ha="center")
    ax.set(xlabel="Wavelength (nm)", ylabel="Reflectance", xlim=(350, 2500),
           title="Pure asbestos minerals — USGS splib07a (ASD, 2151 ch)")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGS / "asbestos_01_pure_minerals.png", dpi=200)

    # ── Fig 2: AC roof vs confusers ─────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 6))
    for (label, _f), color in zip(AC_LEVELS, ["#D8A0BC", "#B8627F", "#8F1D44"]):
        ax.plot(wl, ac[label], lw=2.0, color=color, label=f"{label} (modelled)")
    for name in ["Concrete (road)", "Brick red (terracotta)", "Asphalt tar roof",
                 "Asphalt shingle grey", "Fiberglass roofing white", "Galvanized metal roof"]:
        ax.plot(*_clean(spectra[name]), lw=1.1, alpha=0.75, label=name)
    for nm, label in DIAGNOSTICS:
        ax.axvline(nm, color="0.4", lw=0.8, ls=":")
    ax.axvspan(885, 2500, color="0.92", zorder=0)
    ax.text(1650, 0.02, "not seen by SuperDove (no SWIR)", fontsize=8, color="0.45", ha="center")
    ax.set(xlabel="Wavelength (nm)", ylabel="Reflectance", xlim=(350, 2500),
           title="Asbestos-cement roof (modelled, Cilia 2015 mixing) vs roof confusers")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGS / "asbestos_02_ac_roof_vs_confusers.png", dpi=200)

    # ── Fig 3: sensor view (resampled) ──────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
    show = ["AC roof weathered", "Concrete (road)", "Brick red (terracotta)", "Asphalt tar roof"]
    colors = {"AC roof weathered": "#8F1D44", "Concrete (road)": "0.35",
              "Brick red (terracotta)": "#C4622D", "Asphalt tar roof": "0.6"}
    for ax_s, (sensor, bands) in zip(axes, BAND_SETS.items()):
        centers = [b[1] for b in bands]
        for name in show:
            ax_s.plot(centers, resampled[sensor][name], "o-", ms=5, lw=1.4,
                      color=colors[name], label=name)
        ax_s.set(title=sensor, xlabel="Band center (nm)")
        ax_s.grid(alpha=0.25)
    axes[0].set_ylabel("Reflectance")
    axes[0].legend(fontsize=7)
    fig.suptitle("What each sensor sees — signatures resampled with Gaussian SRF", y=1.02)
    fig.tight_layout()
    fig.savefig(FIGS / "asbestos_03_sensor_view.png", dpi=200, bbox_inches="tight")

    # ── Fig 4 + CSV: SAM separability ───────────────────────────────────────
    target = "AC roof weathered"
    confusers = [n for n, (_fp, g) in SOURCES.items() if g == "confuser"]
    sets = {"Full ASD (2151 ch)": None, **BAND_SETS}
    matrix = np.zeros((len(confusers), len(sets)))
    for j, (sensor, bands) in enumerate(sets.items()):
        for i, name in enumerate(confusers):
            if bands is None:
                matrix[i, j] = sam_deg(ac[target], spectra[name][1])
            else:
                matrix[i, j] = sam_deg(resampled[sensor][target], resampled[sensor][name])

    with open(CSV / "asbestos_sam_separability.csv", "w", newline="") as f:
        w = _csv.writer(f)
        w.writerow([f"SAM degrees vs '{target}'"] + list(sets))
        for i, name in enumerate(confusers):
            w.writerow([name] + [f"{matrix[i, j]:.2f}" for j in range(len(sets))])

    fig, ax = plt.subplots(figsize=(9, 4.8))
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(range(len(sets)), list(sets), fontsize=8)
    ax.set_yticks(range(len(confusers)), confusers, fontsize=8)
    for i in range(len(confusers)):
        for j in range(len(sets)):
            ax.text(j, i, f"{matrix[i, j]:.1f}°", ha="center", va="center", fontsize=8)
    ax.set_title(f"SAM separability: '{target}' vs confusers (higher = more separable)")
    fig.colorbar(im, label="SAM angle (deg)")
    fig.tight_layout()
    fig.savefig(FIGS / "asbestos_04_sam_separability.png", dpi=200)

    # ── Fig 5 + CSV: Mg-OH 2.31 µm band depth (continuum-removed) ──────────
    # depth = 1 − R(2320)/Rcont, continuum = linear between 2210 and 2400 nm.
    # WV-3 S8 (2330/70) resolves it; S2 B12 (2190/175) washes it out; SuperDove blind.
    def band_depth(curve: np.ndarray) -> float:
        def at(nm: float) -> float:
            i = np.nanargmin(np.abs(wl - nm))
            seg = curve[max(0, i - 3):i + 4]
            return float(np.nanmean(seg))
        l, c, r = at(2210), at(2320), at(2400)
        cont = l + (r - l) * (2320 - 2210) / (2400 - 2210)
        return 1.0 - c / cont

    depth_rows = [(n, band_depth(c)) for n, c in all_curves.items()
                  if n.startswith("AC roof") or SOURCES.get(n, ("", ""))[1] == "confuser"]
    with open(CSV / "asbestos_mgoh_band_depth.csv", "w", newline="") as f:
        w = _csv.writer(f)
        w.writerow(["material", "band_depth_2310nm"])
        w.writerows([(n, f"{d:.4f}") for n, d in depth_rows])

    fig, ax = plt.subplots(figsize=(9, 4.8))
    names = [n for n, _ in depth_rows]
    depths = [d for _, d in depth_rows]
    bar_colors = ["#8F1D44" if n.startswith("AC roof") else "0.6" for n in names]
    ax.barh(names, depths, color=bar_colors)
    ax.axvline(0, color="0.2", lw=0.8)
    ax.set_xlabel("Continuum-removed band depth @ 2.31 µm")
    ax.set_title("Mg-OH 2.31 µm feature — only asbestos-cement shows real depth\n"
                 "(seen by WV-3 SWIR S8; washed out by S2 B12, FWHM 175 nm; invisible to SuperDove)",
                 fontsize=10)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(FIGS / "asbestos_05_mgoh_band_depth.png", dpi=200)

    print("Band depth @2.31 µm:")
    for n, d in depth_rows:
        print(f"  {n:28s} {d:+.4f}")

    print(f"Figures → {FIGS}")
    print(f"CSVs    → {CSV}")
    print("\nSAM matrix (degrees, target = AC roof weathered):")
    print(f"{'confuser':28s}" + "".join(f"{s:>22s}" for s in sets))
    for i, name in enumerate(confusers):
        print(f"{name:28s}" + "".join(f"{matrix[i, j]:>21.1f}°" for j in range(len(sets))))


def _clean(spec: tuple[np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    wl, r = spec
    return wl, np.where(np.isfinite(r), r, np.nan)


if __name__ == "__main__":
    main()
