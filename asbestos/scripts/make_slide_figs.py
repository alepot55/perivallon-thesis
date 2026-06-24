#!/usr/bin/env python3
"""Slide-ready variants of the asbestos figures: no internal titles,
large fonts, tight margins. Output: asbestos/slides/figs/.

Usage: python3 scripts/make_slide_figs.py   (from asbestos/)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from shapely.geometry import box

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from verify_roof_extraction import load, render_chip  # noqa: E402

OUT = ROOT / "slides" / "figs"
OUT.mkdir(parents=True, exist_ok=True)

MAROON, GREEN, GREY = "#8F1D44", "#4A7A44", "0.45"
plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 14,
    "axes.edgecolor": "0.25", "axes.labelcolor": "0.1",
    "xtick.color": "0.25", "ytick.color": "0.25",
})

ap = argparse.ArgumentParser()
ap.add_argument("--gt", choices=["precedenti", "2020"], default="precedenti")
ap.add_argument("--planet-dir", default="data/planet/PSScene")
ap.add_argument("--tag", default="")
args = ap.parse_args()

df, gdf, tifs = load(args.gt, args.planet_dir, args.tag)
mineral = gdf[gdf["ndvi"] < 0.2]
veg = gdf[gdf["ndvi"] >= 0.3]
# bands inferred from the CSV column order
CENTER = {"coastalblue": 443, "blue": 490, "greeni": 531, "green": 565,
          "yellow": 610, "red": 665, "rededge": 705, "nir": 865}
cols = [c for c in gdf.columns if c.startswith("sr_")]
centers = [CENTER[c[3:]] for c in cols]

# ── 1 · map ──────────────────────────────────────────────────────────────────
from verify_roof_extraction import GT_FILES
all_gt = gpd.read_file(ROOT / "data" / GT_FILES[args.gt])[["geometry"]]
bg, pts = all_gt.centroid, gdf.geometry.centroid
fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.6))
ax = axes[0]
gt_label = {"precedenti": "PRAL ground truth (50k roofs)",
            "2020": "Mappatura_2020 ground truth (10.9k roofs)"}[args.gt]
ax.scatter(bg.x, bg.y, s=0.5, color="0.83", label=gt_label)
for t in tifs:
    with rasterio.open(t) as src:
        b = gpd.GeoSeries([box(*src.bounds)], crs=src.crs).to_crs(gdf.crs)
        b.boundary.plot(ax=ax, color="0.2", lw=1.3)
ax.scatter(pts.x, pts.y, s=6, color=MAROON, label=f"extracted roofs ({len(gdf):,})")
ax.plot([], [], color="0.2", lw=1.3, label="PSScene strips")
ax.legend(fontsize=12, loc="upper right", markerscale=2.5, frameon=False)
ax.set_aspect("equal"); ax.set_axis_off()

ax = axes[1]
minx, miny, maxx, maxy = gdf.total_bounds
pad = 2000
sel = bg[(bg.x > minx - pad) & (bg.x < maxx + pad) & (bg.y > miny - pad) & (bg.y < maxy + pad)]
ax.scatter(sel.x, sel.y, s=2.5, color="0.85", label="GT, not extractable")
mp, vp = mineral.geometry.centroid, veg.geometry.centroid
ax.scatter(mp.x, mp.y, s=12, color=MAROON, alpha=0.75, label=f"mineral  n={len(mineral)}")
ax.scatter(vp.x, vp.y, s=12, color=GREEN, alpha=0.75, label=f"vegetated  n={len(veg)}")
ax.set_xlim(minx - pad, maxx + pad); ax.set_ylim(miny - pad, maxy + pad)
ax.legend(fontsize=12, markerscale=2, frameon=False, loc="lower left")
ax.set_aspect("equal"); ax.set_axis_off()
fig.tight_layout(pad=0.4)
fig.savefig(OUT / "map.png", dpi=200, bbox_inches="tight")

# ── 2 · chips ────────────────────────────────────────────────────────────────
big = gdf[gdf["n_px"] >= 20]
m_ex = big[big["ndvi"] < 0.1].nlargest(7, "area_m2")
v_ex = big[big["ndvi"] >= 0.4].nlargest(7, "area_m2")
fig, axes = plt.subplots(2, 7, figsize=(18, 5.4))
for ax_row, sel_df, tag in [(axes[0], m_ex, "mineral"), (axes[1], v_ex, "vegetated")]:
    for k, ax in enumerate(ax_row):
        ax.set_xticks([]); ax.set_yticks([])
        if k >= len(sel_df):
            ax.set_visible(False); continue
        roof = sel_df.iloc[k]
        if render_chip(ax, roof, tifs):
            ax.set_title(f"NDVI {roof['ndvi']:.2f} · {roof['area_m2']:.0f} m²", fontsize=11)
        for sp in ax.spines.values():
            sp.set_color("0.6")
axes[0][0].set_ylabel("mineral", fontsize=14)
axes[1][0].set_ylabel("vegetated", fontsize=14)
fig.tight_layout(pad=0.5)
fig.savefig(OUT / "chips.png", dpi=200, bbox_inches="tight")

# ── 3 · fan + USGS comparison ───────────────────────────────────────────────
ref_csv = ROOT.parent / "spectral/csv/asbestos/asbestos_resampled_SuperDove.csv"
rdf = pd.read_csv(ref_csv)
ref = np.array([rdf.loc[rdf["center_nm"] == c, "AC roof weathered"].iloc[0] for c in centers])

def sam_deg(a, b):
    a, b = a / a.mean(), b / b.mean()
    return float(np.degrees(np.arccos(np.clip(
        np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)), -1, 1))))

fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.2))
ax = axes[0]
for sub, color, label in [(mineral, MAROON, "mineral"), (veg, GREEN, "vegetated")]:
    arr = sub[cols].to_numpy()
    p25, p50, p75 = np.percentile(arr, [25, 50, 75], axis=0)
    ax.fill_between(centers, p25, p75, color=color, alpha=0.18)
    ax.plot(centers, p50, "o-", color=color, lw=2.4, ms=7,
            label=f"{label}  n={len(sub)}  (median, IQR)")
ax.set_xlabel("band center (nm)"); ax.set_ylabel("surface reflectance")
ax.legend(fontsize=12, frameon=False); ax.grid(alpha=0.2)

ax = axes[1]
m50 = np.percentile(mineral[cols].to_numpy(), 50, axis=0)
v50 = np.percentile(veg[cols].to_numpy(), 50, axis=0)
ax.plot(centers, m50 / m50.mean(), "o-", color=MAROON, lw=2.4, ms=7,
        label=f"mineral — SAM {sam_deg(ref, m50):.1f}°")
ax.plot(centers, v50 / v50.mean(), "o-", color=GREEN, lw=1.8, ms=6, alpha=0.85,
        label=f"vegetated — SAM {sam_deg(ref, v50):.1f}°")
ax.plot(centers, ref / ref.mean(), "s--", color="0.2", lw=2,
        label="USGS asbestos-cement model")
ax.set_xlabel("band center (nm)"); ax.set_ylabel("reflectance (shape-normalized)")
ax.legend(fontsize=12, frameon=False); ax.grid(alpha=0.2)
fig.tight_layout(pad=0.6)
fig.savefig(OUT / "fan.png", dpi=200, bbox_inches="tight")

# ── 4 · Mg-OH band depth ────────────────────────────────────────────────────
bd = pd.read_csv(ROOT.parent / "spectral/csv/asbestos/asbestos_mgoh_band_depth.csv")
names, depths = bd.iloc[:, 0], bd.iloc[:, 1].astype(float)
colors = [MAROON if n.startswith("AC roof") else "0.62" for n in names]
fig, ax = plt.subplots(figsize=(11.5, 5.2))
ax.barh(names, depths, color=colors, height=0.62)
ax.axvline(0, color="0.2", lw=0.9)
ax.set_xlabel("continuum-removed band depth @ 2.31 µm")
ax.invert_yaxis()
ax.grid(alpha=0.2, axis="x")
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)
fig.tight_layout(pad=0.5)
fig.savefig(OUT / "band_depth.png", dpi=200, bbox_inches="tight")

print("slide figs →", OUT)
