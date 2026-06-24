"""Plot rendering engine — all figures use the same pipeline."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec

from . import config

# ─────────────────────────────────────────────────────────────────────────────
# Global matplotlib style
# ─────────────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":        "sans-serif",
    "font.sans-serif":    ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size":          10,
    "axes.labelsize":     11,
    "axes.titlesize":     14,
    "axes.titleweight":   "bold",
    "axes.linewidth":     0.6,
    "axes.grid":          True,
    "grid.color":         "#E0E0E0",
    "grid.linewidth":     0.35,
    "grid.linestyle":     "-",
    "xtick.major.size":   4,
    "xtick.minor.size":   2,
    "xtick.major.width":  0.5,
    "xtick.minor.visible":True,
    "ytick.major.size":   4,
    "ytick.minor.size":   2,
    "ytick.major.width":  0.5,
    "ytick.minor.visible":True,
    "legend.fontsize":    8.5,
    "legend.framealpha":  0.95,
    "legend.edgecolor":   "#CCCCCC",
    "figure.facecolor":   "white",
    "savefig.facecolor":  "white",
    "savefig.dpi":        300,
    "savefig.bbox":       "tight",
})

# ─────────────────────────────────────────────────────────────────────────────
# Band bar renderer (same style for every plot, regardless of x-range)
# ─────────────────────────────────────────────────────────────────────────────
_ROW_Y  = {"S2": 0.78, "SD": 0.46, "WV3": 0.14}
_BAR_H  = 0.24
_VW_SCALE = 0.88  # visual width = fwhm × this


def _draw_band_bar(ax: plt.Axes, x0: float, x1: float,
                   row: str, color: str, label: str,
                   xmin: float, xmax: float) -> None:
    """Draw one sensor band rectangle, clipped to visible range."""
    x0c, x1c = max(x0, xmin), min(x1, xmax)
    if x0c >= x1c:
        return
    yc = _ROW_Y[row]
    ax.add_patch(mpatches.Rectangle(
        (x0c, yc - _BAR_H / 2), x1c - x0c, _BAR_H,
        facecolor=color, edgecolor="white", linewidth=0.8,
        alpha=1.0, zorder=3,
    ))
    # label only if bar wide enough
    if (x1c - x0c) > (xmax - xmin) * 0.012:
        ax.text((x0c + x1c) / 2, yc, label,
                fontsize=6, ha="center", va="center",
                color="white", fontweight="bold", zorder=4)


def draw_sensor_bands(ax: plt.Axes, xmin: float = 350, xmax: float = 2500) -> None:
    """Render the three-row sensor band panel (axis-off)."""
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(bottom=False, labelbottom=False)
    ax.set_facecolor("white")

    # separator lines
    for y in [0.32, 0.63]:
        ax.axhline(y, color="#E0E0E0", linewidth=0.4, zorder=1)

    # row labels
    for key in ("S2", "SD", "WV3"):
        ax.text(-0.005, _ROW_Y[key], config.SENSOR_LABELS[key],
                transform=ax.transAxes, fontsize=8.5, fontweight="semibold",
                color=config.SENSOR_COLORS[key], ha="right", va="center")

    # Sentinel-2
    c_s2 = config.SENSOR_COLORS["S2"]
    for lbl, cen, fw in config.S2_BANDS:
        vw = fw * _VW_SCALE
        _draw_band_bar(ax, cen - vw/2, cen + vw/2, "S2", c_s2, lbl, xmin, xmax)

    # SuperDove
    c_sd = config.SENSOR_COLORS["SD"]
    for lbl, cen, fw in config.SD_BANDS:
        vw = fw * _VW_SCALE
        _draw_band_bar(ax, cen - vw/2, cen + vw/2, "SD", c_sd, lbl, xmin, xmax)

    # SWIR gap
    gx = max(config.SD_SWIR_GAP_NM, xmin)
    if gx < xmax:
        ax.axvspan(gx, xmax,
                   ymin=_ROW_Y["SD"] - _BAR_H/2,
                   ymax=_ROW_Y["SD"] + _BAR_H/2,
                   alpha=0.08, color="#CC0000", zorder=2)
        if (xmax - gx) > (xmax - xmin) * 0.12:
            ax.text((gx + xmax) / 2, _ROW_Y["SD"], "No SWIR coverage",
                    fontsize=6.5, color="#BB3333", alpha=0.7,
                    ha="center", va="center", style="italic")

    # WorldView-3 SWIR
    c_wv = config.SENSOR_COLORS["WV3"]
    for lbl, cen, fw in config.WV3_BANDS:
        vw = fw * _VW_SCALE
        _draw_band_bar(ax, cen - vw/2, cen + vw/2, "WV3", c_wv, lbl, xmin, xmax)


# ─────────────────────────────────────────────────────────────────────────────
# Annotation renderer
# ─────────────────────────────────────────────────────────────────────────────

def draw_annotations(ax: plt.Axes, annotations: list[tuple],
                     xmin: float = 350, xmax: float = 2500) -> None:
    """Draw absorption feature annotations.

    annotations: [(wavelength, label, "top"|"bottom"), ...]
    """
    for wl, label, pos in annotations:
        if not (xmin <= wl <= xmax):
            continue
        ax.axvline(wl, color="#D0D0D0", linewidth=0.5, zorder=1)
        yf = 0.93 if pos == "top" else 0.04
        va = "top" if pos == "top" else "bottom"
        ax.annotate(
            f"{label}  {int(wl)} nm",
            xy=(wl, yf), xycoords=("data", "axes fraction"),
            fontsize=8, color="#333333", ha="center", va=va, zorder=5,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.88),
        )


# ─────────────────────────────────────────────────────────────────────────────
# Figure generation — one function handles every plot spec
# ─────────────────────────────────────────────────────────────────────────────

def generate_plot(
    spec: dict,
    spectra: dict[str, tuple[np.ndarray, np.ndarray]],
    out_dir: Path,
) -> Path:
    """Render a single figure from a plot spec dict. Returns output path."""
    xmin, xmax = spec.get("xrange", (350, 2500))
    figsize = spec.get("figsize", (14, 7.5))
    lw = spec.get("lw", 1.6)

    fig = plt.figure(figsize=figsize, dpi=300)
    gs = GridSpec(2, 1, figure=fig, height_ratios=[1, 4.5], hspace=0.04)
    ax_bands = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1])

    # band panel
    draw_sensor_bands(ax_bands, xmin, xmax)
    ax_bands.set_title(spec["title"], fontsize=14, fontweight="bold", pad=10)

    # main axes setup
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Reflectance")
    ax.set_xlim(xmin, xmax)
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(4))

    # citation
    ax.text(0.995, 0.008, config.CITATION, transform=ax.transAxes,
            ha="right", va="bottom", fontsize=6.5, color="#888888", style="italic")

    # curves
    for mat_key, color_key, label in spec["curves"]:
        wl, r = spectra[mat_key]
        mask = ~np.isnan(r)
        if xmin != 350 or xmax != 2500:
            mask = mask & (wl >= xmin) & (wl <= xmax)
        ax.plot(wl[mask], r[mask], color=config.COLORS[color_key],
                linewidth=lw, label=label, zorder=4)

    # auto y-limit
    lines = ax.get_lines()
    ymax = max((np.nanmax(l.get_ydata()) for l in lines if len(l.get_ydata())), default=1.0)
    ax.set_ylim(0, min(ymax * 1.10, 1.05))

    # optional note
    if "note" in spec:
        ax.text(0.5, 0.97, spec["note"], transform=ax.transAxes,
                ha="center", va="top", fontsize=7.5, color="#555",
                style="italic",
                bbox=dict(fc="#FFFDE7", ec="none", alpha=0.88, pad=3))

    # legend (outside right)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0),
              borderaxespad=0, framealpha=0.95, edgecolor="#CCCCCC")

    # annotations
    if "annotations" in spec:
        draw_annotations(ax, spec["annotations"], xmin, xmax)

    # save
    path = out_dir / spec["filename"]
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def generate_pdf(png_paths: list[Path], pdf_path: Path) -> None:
    """Assemble all PNGs into a single PDF."""
    with PdfPages(pdf_path) as pdf:
        for p in png_paths:
            img = plt.imread(str(p))
            fig, ax = plt.subplots(figsize=(14, 7.5))
            ax.imshow(img)
            ax.axis("off")
            pdf.savefig(fig, bbox_inches="tight", dpi=150, facecolor="white")
            plt.close(fig)
        d = pdf.infodict()
        d["Title"]  = "Spectral Signature Library — PERIVALLON"
        d["Author"] = "USGS splib07a (Kokaly et al., 2017)"
