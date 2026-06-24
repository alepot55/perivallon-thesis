#!/usr/bin/env python3
"""Visual verification of the extracted roof signatures.

Fig A  roof_extraction_map.png    where: strips + extracted roofs over Lombardia
Fig B  roof_extraction_chips.png  what: PSScene RGB crops with the roof polygon
                                  overlaid — 8 mineral + 8 vegetated examples

Usage: python3 scripts/verify_roof_extraction.py   (from asbestos/)
"""
from __future__ import annotations

import argparse
import glob
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import from_bounds
from shapely.geometry import box

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIGS = ROOT / "figures"

CHIP_HALF_M = 90  # half-window around the roof centroid (m)

GT_FILES = {"precedenti": "mappature_precedenti.gpkg", "2020": "mappatura_2020.gpkg"}


def load(gt_which: str = "precedenti", planet_dir: str = "data/planet/PSScene",
         tag: str = "") -> tuple[pd.DataFrame, gpd.GeoDataFrame, list[str]]:
    suffix = f"_{tag}" if tag else ""
    sig = pd.read_csv(DATA / "processed" / f"roof_signatures{suffix}.csv")
    if "ndvi" not in sig.columns:
        sig["ndvi"] = (sig["sr_nir"] - sig["sr_red"]) / (sig["sr_nir"] + sig["sr_red"] + 1e-9)
    gt = gpd.read_file(DATA / GT_FILES[gt_which])[["gml_id", "geometry"]]
    df = sig.merge(gt, on="gml_id", how="left")
    tifs = sorted(glob.glob(str(ROOT / planet_dir / "*AnalyticMS_SR*clip.tif")))
    return df, gpd.GeoDataFrame(df, geometry="geometry", crs=gt.crs), tifs


def render_chip(ax, roof, tifs: list[str]) -> bool:
    cx, cy = roof.geometry.centroid.x, roof.geometry.centroid.y
    want = box(cx - CHIP_HALF_M, cy - CHIP_HALF_M, cx + CHIP_HALF_M, cy + CHIP_HALF_M)
    for t in tifs:
        with rasterio.open(t) as src:
            if not box(*src.bounds).contains(want):
                continue
            win = from_bounds(*want.bounds, src.transform)
            rgb_idx = [6, 4, 2] if src.count == 8 else [3, 2, 1]  # R,G,B
            img = src.read(rgb_idx, window=win).astype(float)
            if img.size == 0 or (img <= 0).all():
                continue
            rgb = np.dstack([img[i] for i in range(3)])
            lo, hi = np.nanpercentile(rgb[rgb > 0], [2, 98])
            rgb = np.clip((rgb - lo) / (hi - lo + 1e-9), 0, 1)
            ax.imshow(rgb, extent=(want.bounds[0], want.bounds[2],
                                   want.bounds[1], want.bounds[3]), origin="upper")
            polys = (roof.geometry.geoms if roof.geometry.geom_type == "MultiPolygon"
                     else [roof.geometry])
            for p in polys:
                xs, ys = p.exterior.xy
                ax.plot(xs, ys, color="#FFD400", lw=1.8)
            ax.set_xlim(want.bounds[0], want.bounds[2])
            ax.set_ylim(want.bounds[1], want.bounds[3])
            return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt", choices=["precedenti", "2020"], default="precedenti")
    ap.add_argument("--planet-dir", default="data/planet/PSScene")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    suffix = f"_{args.tag}" if args.tag else ""
    df, gdf, tifs = load(args.gt, args.planet_dir, args.tag)
    print(f"signatures: {len(gdf)}")

    # ── Fig A: context map ──────────────────────────────────────────────────
    # province.gpkg has no geometry (attributes-only WFS table) — use the full
    # GT roof cloud as geographic backdrop instead.
    all_gt = gpd.read_file(DATA / GT_FILES[args.gt])[["geometry"]]
    bg = all_gt.centroid
    pts = gdf.geometry.centroid
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    ax = axes[0]
    ax.scatter(bg.x, bg.y, s=0.4, color="0.82", label="GT Mappature_precedenti (50k roofs)")
    for t in tifs:
        with rasterio.open(t) as src:
            b = gpd.GeoSeries([box(*src.bounds)], crs=src.crs).to_crs(gdf.crs)
            b.boundary.plot(ax=ax, color="#3F7FBF", lw=1.4)
    ax.scatter(pts.x, pts.y, s=5, color="#8F1D44", label=f"extracted roofs ({len(gdf)})")
    ax.legend(fontsize=9, loc="upper right", markerscale=3)
    ax.set_title(f"Coverage — GT {args.gt} (grey), PSScene strips (blue),\nroofs with extracted signature (red)")
    ax.set_aspect("equal")
    ax.set_axis_off()

    ax = axes[1]
    minx, miny, maxx, maxy = gdf.total_bounds
    pad = 2000
    sel = bg[(bg.x > minx - pad) & (bg.x < maxx + pad) & (bg.y > miny - pad) & (bg.y < maxy + pad)]
    ax.scatter(sel.x, sel.y, s=2, color="0.85", label="GT not extractable")
    mineral = gdf[gdf["ndvi"] < 0.2]
    veg = gdf[gdf["ndvi"] >= 0.3]
    mp, vp = mineral.geometry.centroid, veg.geometry.centroid
    ax.scatter(mp.x, mp.y, s=10, color="#8F1D44", alpha=0.7, label=f"mineral n={len(mineral)}")
    ax.scatter(vp.x, vp.y, s=10, color="#3D8B37", alpha=0.7, label=f"vegetated n={len(veg)}")
    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)
    ax.legend(fontsize=9, markerscale=2)
    ax.set_title("Covered area zoom — NDVI split")
    ax.set_aspect("equal")
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(FIGS / f"roof_extraction_map{suffix}.png", dpi=200)

    # ── Fig B: verification chips ───────────────────────────────────────────
    big = gdf[gdf["n_px"] >= 20]
    m_ex = big[big["ndvi"] < 0.1].nlargest(8, "area_m2")
    v_ex = big[big["ndvi"] >= 0.4].nlargest(8, "area_m2")
    fig, axes = plt.subplots(2, 8, figsize=(20, 5.6))
    for ax_row, sel, tag in [(axes[0], m_ex, "MINERAL"), (axes[1], v_ex, "VEGETATED")]:
        for k, ax in enumerate(ax_row):
            if k >= len(sel):
                ax.set_visible(False)
                continue
            roof = sel.iloc[k]
            ok = render_chip(ax, roof, tifs)
            ax.set_xticks([]), ax.set_yticks([])
            if ok:
                ax.set_title(f"{tag}  NDVI={roof['ndvi']:.2f}\n{roof['area_m2']:.0f} m² · {roof['n_px']} px",
                             fontsize=8)
    fig.suptitle("Extraction check — Planet RGB 3 m, GT outline in yellow "
                 "(row 1: 'mineral' roofs · row 2: 'vegetated' = likely remediated)", y=1.0)
    fig.tight_layout()
    fig.savefig(FIGS / f"roof_extraction_chips{suffix}.png", dpi=180, bbox_inches="tight")
    print(f"Figs → {FIGS}")


if __name__ == "__main__":
    main()
