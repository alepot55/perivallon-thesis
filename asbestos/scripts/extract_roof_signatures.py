#!/usr/bin/env python3
"""Extract real asbestos-roof spectral signatures from Planet PSScene (SuperDove).

GT: Mappature_precedenti (PRAL + ATS) filtered to F2018 == 1 (asbestos still
present at the 2018 flight) — 6.7k of those roofs fall inside the 2026-03-30
PSScene strips. Per roof: erode 3 m (edge/mixed pixels), keep udm2-clear pixels,
take the per-band median of surface reflectance (SR scale 1e-4).

Outputs (asbestos/figures/ + asbestos/data/processed/):
  roof_signatures.csv          per-roof 4-band median SR + metadata
  roof_signatures_fan.png      per-band percentile fan vs USGS AC-roof model
  roof_signatures_overview.png coverage counts + brightness distribution

Usage (from asbestos/):
  python3 scripts/extract_roof_signatures.py                       # legacy 4-band run
  python3 scripts/extract_roof_signatures.py --gt 2020 \
      --planet-dir data/planet/AOI1_brescia --tag aoi1             # new 8-band orders
Band count (4 vs 8) is auto-detected from the rasters.
"""
from __future__ import annotations

import argparse
import csv
import glob
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.mask import mask as rio_mask

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIGS = ROOT / "figures"
PROC = DATA / "processed"

SR_SCALE = 1e-4
MIN_AREA_M2 = 150
EDGE_BUFFER_M = -3.0
MIN_CLEAR_PX = 5

# SuperDove PSScene band orders (name, center nm)
BANDS_4 = [("Blue", 490), ("Green", 565), ("Red", 665), ("NIR", 865)]
BANDS_8 = [("CoastalBlue", 443), ("Blue", 490), ("GreenI", 531), ("Green", 565),
           ("Yellow", 610), ("Red", 665), ("RedEdge", 705), ("NIR", 865)]
BANDS = BANDS_4  # set in main() after raster inspection


def load_gt(which: str) -> gpd.GeoDataFrame:
    if which == "2020":
        gt = gpd.read_file(DATA / "mappatura_2020.gpkg")
        gt["FONTE"] = "Mappatura_2020"
        gt = gt[gt.geometry.area >= MIN_AREA_M2].copy()
    else:
        gt = gpd.read_file(DATA / "mappature_precedenti.gpkg")
        gt = gt[(gt["F2018"] == 1) & (gt.geometry.area >= MIN_AREA_M2)].copy()
    gt["geometry"] = gt.geometry.buffer(EDGE_BUFFER_M)
    gt = gt[~gt.geometry.is_empty & gt.geometry.is_valid]
    return gt


def extract_strip(sr_path: str, gt: gpd.GeoDataFrame) -> list[dict]:
    # udm2 file shares the scene-id prefix (everything up to '_3B_')
    stem = Path(sr_path).name.split("_3B_")[0]
    udm_matches = glob.glob(str(Path(sr_path).parent / f"{stem}_3B_udm2*.tif"))
    if not udm_matches:
        print(f"  ! no udm2 for {Path(sr_path).name} — skipped")
        return []
    udm_path = udm_matches[0]
    rows = []
    with rasterio.open(sr_path) as src, rasterio.open(udm_path) as udm:
        from shapely.geometry import box
        bb = gpd.GeoSeries([box(*src.bounds)], crs=src.crs).to_crs(gt.crs).iloc[0]
        hits = gt[gt.within(bb)]
        for idx, roof in hits.iterrows():
            geom = [roof.geometry.__geo_interface__]
            try:
                img, _ = rio_mask(src, geom, crop=True, all_touched=False)
                clr, _ = rio_mask(udm, geom, crop=True, all_touched=False, indexes=[1])
            except ValueError:
                continue
            clear = (clr[0] == 1) & (img.sum(axis=0) > 0)
            if clear.sum() < MIN_CLEAR_PX:
                continue
            med = [float(np.median(img[b][clear]) * SR_SCALE) for b in range(img.shape[0])]
            rows.append({
                "gml_id": roof["gml_id"], "fonte": roof["FONTE"],
                "comune_istat": roof["Codice_Istat"],
                "area_m2": round(roof.geometry.area, 1),
                "n_px": int(clear.sum()), "strip": Path(sr_path).name[:26],
                **{f"sr_{b.lower()}": m for (b, _), m in zip(BANDS, med)},
            })
    return rows


def usgs_ac_model() -> np.ndarray | None:
    """USGS AC-roof (weathered) resampled to the current PSScene band centers."""
    csv_path = ROOT.parent / "spectral" / "csv" / "asbestos" / "asbestos_resampled_SuperDove.csv"
    if not csv_path.exists():
        return None
    import pandas as pd
    df = pd.read_csv(csv_path)
    sd8 = {row["center_nm"]: row["AC roof weathered"] for _, row in df.iterrows()}
    return np.array([sd8[c] for _, c in BANDS])


def main() -> None:
    global BANDS
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt", choices=["precedenti", "2020"], default="precedenti")
    ap.add_argument("--planet-dir", default="data/planet/PSScene")
    ap.add_argument("--tag", default="", help="suffix for output files, e.g. aoi1")
    args = ap.parse_args()
    suffix = f"_{args.tag}" if args.tag else ""

    FIGS.mkdir(exist_ok=True)
    PROC.mkdir(exist_ok=True)

    tifs = sorted(glob.glob(str(ROOT / args.planet_dir / "*AnalyticMS_SR*clip.tif")))
    if not tifs:
        sys.exit(f"No SR rasters in {args.planet_dir}")
    with rasterio.open(tifs[0]) as src:
        BANDS = BANDS_8 if src.count == 8 else BANDS_4
    print(f"{len(tifs)} strips, {len(BANDS)} bands ({args.planet_dir})")

    gt = load_gt(args.gt)
    print(f"GT {args.gt} (area>={MIN_AREA_M2} m2, eroded): {len(gt)} roofs")

    rows: list[dict] = []
    for sr in tifs:
        new = extract_strip(sr, gt)
        rows.extend(new)
        print(f"  {Path(sr).name[:30]:32s} extracted: {len(new)}")
    # Dedup roofs seen in overlapping strips: keep the obs with most clear px
    best: dict[str, dict] = {}
    for r in rows:
        k = r["gml_id"]
        if k not in best or r["n_px"] > best[k]["n_px"]:
            best[k] = r
    rows = list(best.values())
    print(f"TOTAL unique roofs with signature: {len(rows)}")
    if not rows:
        sys.exit("No signatures extracted — check data paths.")

    sig = np.array([[r[f"sr_{b.lower()}"] for b, _ in BANDS] for r in rows])
    centers = [c for _, c in BANDS]

    # NDVI split: GT is from the 2018 flight, image is 2026 — vegetated roofs
    # are likely remediated / overgrown since. Mineral subset = still-bare roof.
    i_red = [b for b, _ in BANDS].index("Red")
    i_nir = [b for b, _ in BANDS].index("NIR")
    ndvi = (sig[:, i_nir] - sig[:, i_red]) / (sig[:, i_nir] + sig[:, i_red] + 1e-9)
    for r, v in zip(rows, ndvi):
        r["ndvi"] = round(float(v), 4)

    with open(PROC / f"roof_signatures{suffix}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    mineral, vegetated = sig[ndvi < 0.2], sig[ndvi >= 0.3]

    def sam_vs(ref: np.ndarray, v: np.ndarray) -> float:
        a, b = v / v.mean(), ref / ref.mean()
        return float(np.degrees(np.arccos(np.clip(
            np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)), -1, 1))))

    # ── Fig: percentile fan (NDVI split) + USGS model comparison ────────────
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5))
    ax = axes[0]
    for sub, color, label in [(mineral, "#8F1D44", "mineral (NDVI<0.2)"),
                              (vegetated, "#3D8B37", "vegetated (NDVI≥0.3)")]:
        if len(sub) < 10:
            continue
        p10, p25, p50, p75, p90 = np.percentile(sub, [10, 25, 50, 75, 90], axis=0)
        ax.fill_between(centers, p25, p75, color=color, alpha=0.25)
        ax.plot(centers, p50, "o-", color=color, lw=2.2, label=f"{label}, n={len(sub)}")
    ax.set(xlabel="Band center (nm)", ylabel="Surface reflectance",
           title=f"Asbestos-roof signatures — GT {args.gt}\n"
                 f"NDVI split: bare vs vegetated (remediation/overgrowth since mapping)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)

    ax = axes[1]
    ref = usgs_ac_model()
    m50 = np.percentile(mineral, 50, axis=0)
    v50 = np.percentile(vegetated, 50, axis=0) if len(vegetated) >= 10 else None
    ax.plot(centers, m50 / m50.mean(), "o-", color="#8F1D44", lw=2.2, label="mineral subset (shape-norm)")
    if v50 is not None:
        ax.plot(centers, v50 / v50.mean(), "o-", color="#3D8B37", lw=1.6, alpha=0.8, label="vegetated subset")
    if ref is not None:
        ax.plot(centers, ref / ref.mean(), "s--", color="0.35", lw=1.8, label="USGS AC-roof model")
        ax.set_title(f"Shape vs USGS model — SAM: mineral {sam_vs(ref, m50):.1f}°"
                     + (f", vegetated {sam_vs(ref, v50):.1f}°" if v50 is not None else ""))
    ax.set(xlabel="Band center (nm)", ylabel="Reflectance (mean-normalized)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / f"roof_signatures_fan{suffix}.png", dpi=200)
    print(f"NDVI split: mineral {len(mineral)}, intermediate "
          f"{len(sig) - len(mineral) - len(vegetated)}, vegetated {len(vegetated)}")

    # ── Fig: overview ───────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))
    fontes = sorted({r["fonte"] for r in rows})
    counts = [sum(r["fonte"] == f for r in rows) for f in fontes]
    axes[0].bar(fontes, counts, color="0.5")
    axes[0].set_title("Extracted roofs by GT source")
    bright = sig.mean(axis=1)
    axes[1].hist(bright, bins=50, color="#8F1D44", alpha=0.8)
    axes[1].set(xlabel="Mean SR (4 bands)", title="Roof brightness distribution\n(bimodality → weathering / paint states)")
    fig.tight_layout()
    fig.savefig(FIGS / f"roof_signatures_overview{suffix}.png", dpi=200)

    print(f"\nCSV  → {PROC / f'roof_signatures{suffix}.csv'}")
    print(f"Figs → {FIGS}")
    print("\nMedian signature, mineral subset (SR):",
          {b: round(float(v), 4) for (b, _), v in zip(BANDS, m50)})


if __name__ == "__main__":
    main()
