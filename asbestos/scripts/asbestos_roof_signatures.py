#!/usr/bin/env python3
"""Extract spectral signatures of asbestos-cement roofs from Planet SuperDove imagery.

Ground truth is the Lombardy 2020 asbestos mapping (polygons of roofs flagged as
asbestos-cement). For every mapped roof we read the surface-reflectance pixels that
fall inside the polygon, keep only the cloud-free ones, and take the per-band median.
The output is one row per roof (8 SuperDove bands + NDVI) and a summary figure.

Inputs
  - a folder of Planet PSScene clips (one *_AnalyticMS_SR_8b_clip.tif per scene,
    with the matching *_udm2_clip.tif quality mask alongside it)
  - the ground-truth polygons (GeoPackage), e.g. mappatura_2020.gpkg

Output
  - <out>/roof_signatures.csv
  - <out>/roof_signatures.png

Example
  python asbestos_roof_signatures.py \
      --scenes data/planet/AOI1_brescia/PSScene \
      --roofs  data/mappatura_2020.gpkg \
      --out    data/processed
"""
from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask as rio_mask

# SuperDove 8-band order and nominal band centres (nm).
BANDS = [
    ("coastalblue", 443), ("blue", 490), ("greeni", 531), ("green", 565),
    ("yellow", 610), ("red", 665), ("rededge", 705), ("nir", 865),
]
BAND_NAMES = [name for name, _ in BANDS]
BAND_CENTERS = [nm for _, nm in BANDS]

SR_SCALE = 1e-4          # Planet SR is stored as reflectance x 10000
MIN_ROOF_AREA_M2 = 150   # skip roofs too small to hold a few clean 3 m pixels
EDGE_EROSION_M = 3.0     # shrink polygons to drop mixed border pixels
MIN_CLEAR_PIXELS = 5     # need at least this many cloud-free pixels to trust a roof


def load_roofs(gpkg_path: Path) -> gpd.GeoDataFrame:
    """Read the ground-truth roofs, drop tiny ones and erode the edges."""
    roofs = gpd.read_file(gpkg_path)
    roofs = roofs[roofs.geometry.area >= MIN_ROOF_AREA_M2].copy()
    roofs["geometry"] = roofs.geometry.buffer(-EDGE_EROSION_M)
    roofs = roofs[~roofs.geometry.is_empty & roofs.geometry.is_valid]
    return roofs


def find_scenes(scenes_dir: Path) -> list[tuple[Path, Path]]:
    """Pair each surface-reflectance raster with its udm2 quality mask."""
    pairs = []
    for sr_path in sorted(scenes_dir.glob("*AnalyticMS_SR*clip.tif")):
        scene_id = sr_path.name.split("_3B_")[0]
        udm = list(scenes_dir.glob(f"{scene_id}_3B_udm2*clip.tif"))
        if udm:
            pairs.append((sr_path, udm[0]))
    return pairs


def roof_median(sr_src, udm_src, geometry) -> tuple[np.ndarray, int] | None:
    """Median surface reflectance over the cloud-free pixels of one roof."""
    try:
        sr, _ = rio_mask(sr_src, [geometry.__geo_interface__], crop=True)
        clear, _ = rio_mask(udm_src, [geometry.__geo_interface__], crop=True, indexes=[1])
    except ValueError:
        return None  # roof falls outside this scene
    # udm2 band 1 == 1 marks usable pixels; also drop fill (all-zero) pixels.
    usable = (clear[0] == 1) & (sr.sum(axis=0) > 0)
    if usable.sum() < MIN_CLEAR_PIXELS:
        return None
    median = np.array([np.median(sr[b][usable]) for b in range(sr.shape[0])])
    return median * SR_SCALE, int(usable.sum())


def extract(roofs: gpd.GeoDataFrame, scenes: list[tuple[Path, Path]]) -> pd.DataFrame:
    """One signature per roof; if a roof appears in several scenes keep the clearest."""
    best: dict[str, dict] = {}
    for sr_path, udm_path in scenes:
        with rasterio.open(sr_path) as sr_src, rasterio.open(udm_path) as udm_src:
            here = roofs.to_crs(sr_src.crs)
            for roof_id, roof in zip(roofs["gml_id"], here.geometry):
                result = roof_median(sr_src, udm_src, roof)
                if result is None:
                    continue
                median, n_px = result
                if roof_id in best and best[roof_id]["n_px"] >= n_px:
                    continue
                best[roof_id] = {"gml_id": roof_id, "n_px": n_px,
                                 **dict(zip(BAND_NAMES, median))}
        print(f"  {sr_path.name[:24]}  roofs so far: {len(best)}")

    df = pd.DataFrame(best.values())
    df["ndvi"] = (df["nir"] - df["red"]) / (df["nir"] + df["red"] + 1e-9)
    return df


def plot_summary(df: pd.DataFrame, out_png: Path, reference_csv: Path | None) -> None:
    """Median signature with the 25-75 percentile band, optional USGS comparison."""
    sig = df[BAND_NAMES].to_numpy()
    p25, p50, p75 = np.percentile(sig, [25, 50, 75], axis=0)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(BAND_CENTERS, p25, p75, color="#8F1D44", alpha=0.2,
                    label="25-75 percentile")
    ax.plot(BAND_CENTERS, p50, "o-", color="#8F1D44", lw=2, label=f"median (n={len(df)})")

    if reference_csv and reference_csv.exists():
        ref = pd.read_csv(reference_csv).set_index("center_nm")["AC roof weathered"]
        ref = ref.reindex(BAND_CENTERS).to_numpy()
        # scale the reference to the roofs' brightness so the shapes are comparable
        ref = ref * (p50.mean() / np.nanmean(ref))
        ax.plot(BAND_CENTERS, ref, "s--", color="0.4", lw=1.6,
                label="USGS asbestos-cement (weathered)")

    ax.set_xlabel("Band centre (nm)")
    ax.set_ylabel("Surface reflectance")
    ax.set_title("Asbestos-roof spectral signatures — Planet SuperDove")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=200)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenes", type=Path, required=True,
                        help="folder with Planet PSScene SR + udm2 clips")
    parser.add_argument("--roofs", type=Path, required=True,
                        help="ground-truth roof polygons (GeoPackage)")
    parser.add_argument("--out", type=Path, default=Path("."),
                        help="output folder for the CSV and figure")
    parser.add_argument("--reference", type=Path,
                        default=Path("../spectral/csv/asbestos/asbestos_resampled_SuperDove.csv"),
                        help="optional USGS reference spectrum for the comparison plot")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    roofs = load_roofs(args.roofs)
    print(f"Ground-truth roofs (area >= {MIN_ROOF_AREA_M2} m2): {len(roofs)}")

    scenes = find_scenes(args.scenes)
    if not scenes:
        raise SystemExit(f"No SR/udm2 scene pairs found in {args.scenes}")
    print(f"Scenes: {len(scenes)}")

    df = extract(roofs, scenes)
    if df.empty:
        raise SystemExit("No roof signatures extracted — check that scenes overlap the roofs.")
    print(f"Roofs with a usable signature: {len(df)}")

    csv_path = args.out / "roof_signatures.csv"
    png_path = args.out / "roof_signatures.png"
    df.to_csv(csv_path, index=False)
    plot_summary(df, png_path, args.reference)

    print(f"\nWrote {csv_path}")
    print(f"Wrote {png_path}")
    median = df[BAND_NAMES].median()
    print("\nMedian signature (surface reflectance):")
    print(median.round(4).to_string())


if __name__ == "__main__":
    main()
