"""Spectrum loading from USGS splib07a and ECOSTRESS, plus CSV export."""
from __future__ import annotations

import csv, re, zipfile
from pathlib import Path

import numpy as np
import requests

from . import config

_wvl_cache: dict[str, np.ndarray] = {}


def _load_wavelengths(zip_path: Path, wvl_file: str) -> np.ndarray:
    if wvl_file not in _wvl_cache:
        with zipfile.ZipFile(zip_path) as z:
            raw = z.read(wvl_file).decode().strip().split("\n")
        _wvl_cache[wvl_file] = np.array([float(x) for x in raw[1:] if x.strip()]) * 1000.0
    return _wvl_cache[wvl_file]


def load_spectrum(zip_path: Path, filepath: str, wvl_type: str = "ASD",
                  ) -> tuple[np.ndarray, np.ndarray]:
    """Return (wavelengths_nm, reflectance) from USGS splib07a zip."""
    wvl_file = config.WVL_ASD if wvl_type == "ASD" else config.WVL_BECK
    wvl = _load_wavelengths(zip_path, wvl_file)
    with zipfile.ZipFile(zip_path) as z:
        raw = z.read(filepath).decode().strip().split("\n")
    r = np.array([float(x) for x in raw[1:] if x.strip()])
    r[r < -1e30] = np.nan
    n = min(len(wvl), len(r))
    return wvl[:n].copy(), r[:n].copy()


def load_all(zip_path: Path) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Load all spectra defined in config.SPECTRA."""
    data = {}
    for name, (fp, wt, _sid) in config.SPECTRA.items():
        data[name] = load_spectrum(zip_path, fp, wt)
    return data


def download_ecostress_rubber() -> tuple[np.ndarray | None, np.ndarray | None]:
    """Download rubber roofing spectrum from ECOSTRESS/JPL."""
    plotfile = "manmade.roofingmaterial.rubber.solid.all.0795uuurbr.jhu.becknic.spectrum.txt"
    try:
        resp = requests.post(
            "https://speclib.jpl.nasa.gov/ecospeclibinteractive",
            data={"plotfile": plotfile},
            headers={"Content-type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        m = re.search(r'https://speclib\.jpl\.nasa\.gov/graphs/eco_inter_data_[^"]+\.csv', resp.text)
        if m:
            lines = [l.strip() for l in requests.get(m.group(), timeout=30).text.strip().split("\n")[1:] if "," in l]
            d = [ln.split(",") for ln in lines]
            return np.array([float(x[0]) for x in d]) * 1000, np.array([float(x[1]) for x in d]) / 100
    except Exception:
        pass
    return None, None


# ── CSV export ────────────────────────────────────────────────────────────────

def save_individual_csv(out_dir: Path, name: str, wl: np.ndarray,
                        r: np.ndarray, sample_id: str) -> None:
    safe = re.sub(r"[^\w\-]", "_", name).strip("_")
    with open(out_dir / f"{safe}_{sample_id}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wavelength_nm", "reflectance"])
        for wv, rv in zip(wl, r):
            w.writerow([f"{wv:.2f}", "" if np.isnan(rv) else f"{rv:.6f}"])


def save_combined_csv(out_path: Path,
                      spectra: dict[str, tuple[np.ndarray, np.ndarray]]) -> None:
    """Interpolate all spectra onto 350–2500 nm / 1 nm grid and write CSV."""
    grid = np.arange(350, 2501, 1)
    cols: dict[str, np.ndarray] = {}

    for col_name, mat_key in config.CSV_COLUMNS:
        wl, r = spectra[mat_key]
        v = ~np.isnan(r)
        if v.sum() < 10:
            cols[col_name] = np.full_like(grid, np.nan, dtype=float)
            continue
        out = np.interp(grid, wl[v], r[v])
        out[grid < wl[v].min()] = np.nan
        out[grid > wl[v].max()] = np.nan
        cols[col_name] = out

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["wavelength_nm"] + [c for c, _ in config.CSV_COLUMNS])
        for i, wv in enumerate(grid):
            row = [str(int(wv))]
            for col_name, _ in config.CSV_COLUMNS:
                val = cols[col_name][i]
                row.append("" if np.isnan(val) else f"{val:.6f}")
            w.writerow(row)
