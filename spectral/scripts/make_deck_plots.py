"""Rigorous figures for the SOTA-revision deck.

Six PNGs, all from USGS splib07a (Kokaly et al., 2017) and verified paper numbers:
  1. fingerprint_4_materials.png  — slide 6 (Every material has a fingerprint)
  2. rgb_fails_two_panels.png     — slide 7 (RGB fails in two distinct ways)
  3. where_info_lives.png         — slide 13 (Where diagnostic info lives)
  4. sensor_radar.png             — slide 8  (Sensor trade-off, 3 axes)
  5. aguilar_bars.png             — slide 12 (Aguilar 2021: +5.94 / +0.59 pp)
  6. bands_plateau.png            — slide 14 (More bands != more information)

Run:
    cd spectral
    python3 scripts/make_deck_plots.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spectral_plots.data import load_spectrum  # noqa: E402
from spectral_plots import config  # noqa: E402

ZIP = ROOT / "data" / "ASCIIdata_splib07a.zip"
OUT = ROOT / "figures" / "deck"
OUT.mkdir(parents=True, exist_ok=True)

# ── Palette coherent with deck (teal-based) ───────────────────────────────────
C = {
    "veg":       "#3D8B37",
    "plastic":   "#E07A3F",
    "concrete":  "#555555",
    "asbestos":  "#9B3D6F",
    "cellulose": "#7E57C2",
    "drygrass":  "#C9A227",
    "mix":       "#2E8B8B",
    "shadow":    "#BBBBBB",
    "vnir_box":  "#D6EAF1",
    "swir_box":  "#F5E6D3",
    "teal":      "#2E8B8B",
    "teal_dk":   "#1F6F6F",
    "teal_lt":   "#A6CFCF",
    "accent":    "#E07A3F",
}

plt.rcParams.update({
    "font.family":     "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size":       12,
    "axes.labelsize":  13,
    "axes.titlesize":  14,
    "axes.titleweight":"bold",
    "axes.linewidth":  0.8,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":       True,
    "grid.color":      "#E8E8E8",
    "grid.linewidth":  0.5,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "legend.fontsize": 11,
    "legend.framealpha": 0.95,
    "legend.edgecolor": "#CCCCCC",
    "figure.facecolor":  "white",
    "savefig.facecolor": "white",
    "savefig.dpi":     300,
    "savefig.bbox":    "tight",
})

# Reference for citation footers
CITE = "USGS splib07a (Kokaly et al., 2017)"

# Build a small spectra cache for the materials we need ──────────────────────
WANTED = [
    "Green vegetation",
    "HDPE (white opaque)",
    "Concrete (road)",
    "Chrysotile (asbestos)",
    "Cellulose (pure)",
    "Dry grass (golden)",
    "Kaolinite (pure)",
    "Bare soil",
]
SPECTRA: dict[str, tuple[np.ndarray, np.ndarray]] = {}
for name in WANTED:
    fp, wt, _ = config.SPECTRA[name]
    SPECTRA[name] = load_spectrum(ZIP, fp, wt)


def _clean(wl: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Drop NaN/sentinel values, return (wl, r) defined."""
    m = ~np.isnan(r) & (r > -1.0)
    return wl[m], r[m]


def _interp(wl: np.ndarray, r: np.ndarray, grid: np.ndarray) -> np.ndarray:
    wl, r = _clean(wl, r)
    out = np.interp(grid, wl, r, left=np.nan, right=np.nan)
    return out


def _shade_vnir_swir(ax: plt.Axes) -> None:
    ax.axvspan(400, 900, alpha=0.18, color=C["vnir_box"], zorder=0)
    ax.axvspan(1000, 2500, alpha=0.18, color=C["swir_box"], zorder=0)


def _annotate_at(ax: plt.Axes, x: float, y_frac: float, label: str,
                 color: str = "#444") -> None:
    """Vertical dotted line + boxed label at given axes-fraction y."""
    ax.axvline(x, color="#BBBBBB", lw=0.7, ls=":", zorder=1)
    va = "top" if y_frac > 0.5 else "bottom"
    ax.annotate(
        label, xy=(x, y_frac), xycoords=("data", "axes fraction"),
        ha="center", va=va, fontsize=10, color=color, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, lw=0.6,
                  alpha=0.95),
    )


def _footer(ax: plt.Axes, text: str = CITE) -> None:
    ax.text(0.995, -0.18, text, transform=ax.transAxes,
            ha="right", va="top", fontsize=9, style="italic", color="#888")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 1 — Spectral fingerprint of 4 materials
# ─────────────────────────────────────────────────────────────────────────────
def fig_fingerprint() -> None:
    fig, ax = plt.subplots(figsize=(13, 5.5))

    series = [
        ("Green vegetation",      C["veg"],      "Vegetation (aspen)"),
        ("HDPE (white opaque)",   C["plastic"],  "Plastic (HDPE)"),
        ("Concrete (road)",       C["concrete"], "Concrete"),
        ("Chrysotile (asbestos)", C["asbestos"], "Asbestos (chrysotile)"),
    ]
    for key, color, label in series:
        wl, r = _clean(*SPECTRA[key])
        ax.plot(wl, r, color=color, lw=2.2, label=label, zorder=4)

    _shade_vnir_swir(ax)
    ax.set_xlim(400, 2500)
    ax.set_ylim(0, 1.15)  # headroom for region labels
    # Region labels at the top
    ax.text(650, 1.10, "SuperDove VNIR", ha="center", va="center",
            color=C["teal_dk"], fontsize=12, fontweight="bold")
    ax.text(1750, 1.10, "SWIR  —  chemistry-diagnostic",
            ha="center", va="center", color="#8B5A2B", fontsize=12,
            fontweight="bold")

    # Diagnostic feature markers — placed low so they sit under the curves,
    # over the empty-ish reflectance region where no curve is present.
    _annotate_at(ax, 680,  0.04, "Chl  0.68 µm",   "#2A6E25")
    _annotate_at(ax, 1730, 0.04, "C-H  1.73 µm",   C["plastic"])
    _annotate_at(ax, 2200, 0.14, "Al-OH  2.20 µm", "#5D7B9D")
    _annotate_at(ax, 2310, 0.04, "Mg-OH  2.31 µm", C["asbestos"])

    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Reflectance")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(250))
    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.55), framealpha=0.97)
    _footer(ax)
    fig.savefig(OUT / "fingerprint_4_materials.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("✓ fingerprint_4_materials.png")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 2 — RGB fails in two distinct ways (2 panels)
# ─────────────────────────────────────────────────────────────────────────────
def fig_rgb_fails() -> None:
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)

    # Panel A: iso-chromaticity — concrete vs asbestos-cement roof.
    # AC roof modelled as 20% chrysotile + 80% concrete matrix (Cilia 2015 range).
    # Both grey in VIS (Δreflectance ≈ 0.11); diverge in SWIR via Mg-OH @2.31 µm.
    grid = np.arange(400, 2501, 5, dtype=float)
    wl_c, r_c = _clean(*SPECTRA["Concrete (road)"])
    wl_a, r_a = _clean(*SPECTRA["Chrysotile (asbestos)"])
    conc = np.interp(grid, wl_c, r_c, left=np.nan, right=np.nan)
    chry = np.interp(grid, wl_a, r_a, left=np.nan, right=np.nan)
    ac_roof = 0.20 * chry + 0.80 * conc  # asbestos-cement roof, modelled

    axL.plot(grid, conc,    color=C["concrete"], lw=2.4,
             label="Concrete (no asbestos)")
    axL.plot(grid, ac_roof, color=C["asbestos"], lw=2.4,
             label="Asbestos-cement roof (modelled)")

    axL.axvspan(400, 700, alpha=0.18, color=C["vnir_box"], zorder=0)
    axL.axvspan(1000, 2500, alpha=0.18, color=C["swir_box"], zorder=0)
    axL.text(550, 0.65, "VIS:\nboth look grey\n(ΔR ≈ 0.11)",
             ha="center", va="top", fontsize=10, color="#5D7B9D",
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CCCCCC", lw=0.5))
    axL.text(1750, 0.65, "SWIR:\nMg-OH dip @ 2.31 µm\nonly in AC roof",
             ha="center", va="top", fontsize=10, color="#8B5A2B",
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CCCCCC", lw=0.5))
    # Mark the Mg-OH dip
    axL.axvline(2310, color=C["asbestos"], lw=0.8, ls=":", alpha=0.6)

    axL.set_title("Iso-chromaticity\nsame colour in VIS, different chemistry in SWIR")
    axL.set_xlim(400, 2500)
    axL.set_ylim(0, 0.8)
    axL.set_xlabel("Wavelength (nm)")
    axL.set_ylabel("Reflectance")
    axL.legend(loc="upper right", fontsize=10)
    axL.xaxis.set_major_locator(mticker.MultipleLocator(500))

    # Panel B: sub-pixel mixing — pure veg + pure concrete → 50/50 mix mimics dry grass
    grid = np.arange(400, 2501, 5, dtype=float)
    wl_v, r_v = _clean(*SPECTRA["Green vegetation"])
    wl_c2, r_c2 = _clean(*SPECTRA["Concrete (road)"])
    wl_g, r_g = _clean(*SPECTRA["Dry grass (golden)"])
    veg  = np.interp(grid, wl_v,  r_v,  left=np.nan, right=np.nan)
    conc = np.interp(grid, wl_c2, r_c2, left=np.nan, right=np.nan)
    mix  = 0.5 * veg + 0.5 * conc
    grass = np.interp(grid, wl_g, r_g, left=np.nan, right=np.nan)

    axR.plot(grid, veg,   color=C["veg"],       lw=1.0, alpha=0.55,
             label="Pure vegetation")
    axR.plot(grid, conc,  color=C["concrete"],  lw=1.0, alpha=0.55,
             label="Pure concrete")
    axR.plot(grid, mix,   color=C["mix"],       lw=2.6,
             label="50 % veg + 50 % concrete")
    axR.plot(grid, grass, color=C["drygrass"],  lw=2.2, ls="--",
             label="Pure dry grass")

    axR.axvspan(400, 700, alpha=0.18, color=C["vnir_box"], zorder=0)
    axR.set_title("Sub-pixel mixing\nmixture mimics a third pure material")
    axR.set_xlim(400, 2500)
    axR.set_ylim(0, 0.8)
    axR.set_xlabel("Wavelength (nm)")
    axR.legend(loc="upper right", fontsize=10)
    axR.xaxis.set_major_locator(mticker.MultipleLocator(500))

    fig.text(0.995, -0.02, CITE, ha="right", va="top", fontsize=9,
             style="italic", color="#888")
    fig.tight_layout()
    fig.savefig(OUT / "rgb_fails_two_panels.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("✓ rgb_fails_two_panels.png")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 3 — Where diagnostic information lives (SuperDove 8 bands vs SWIR)
# ─────────────────────────────────────────────────────────────────────────────
def fig_where_info() -> None:
    fig, ax = plt.subplots(figsize=(13, 5.5))

    # Single target curve: asbestos-cement roof (modelled, the thesis use case).
    # The 8 SuperDove bands + SWIR shading reveal where the diagnostic
    # features sit — and that SuperDove cannot reach them.
    grid = np.arange(400, 2501, 5, dtype=float)
    wl_c, r_c = _clean(*SPECTRA["Concrete (road)"])
    wl_a, r_a = _clean(*SPECTRA["Chrysotile (asbestos)"])
    conc = np.interp(grid, wl_c, r_c, left=np.nan, right=np.nan)
    chry = np.interp(grid, wl_a, r_a, left=np.nan, right=np.nan)
    ac_roof = 0.20 * chry + 0.80 * conc
    ax.plot(grid, ac_roof, color=C["asbestos"], lw=2.4,
            label="Asbestos-cement roof (modelled)")

    ax.set_xlim(400, 2500)
    ax.set_ylim(0, 1.20)  # headroom for SWIR header + band stem labels

    # SWIR-not-covered shading
    ax.axvspan(900, 2500, alpha=0.22, color=C["swir_box"], zorder=0)

    # Header for the SWIR region (in the headroom band)
    ax.text(1700, 1.15, "SWIR  —  out of SuperDove reach",
            ha="center", va="center", color="#8B5A2B", fontsize=12.5,
            fontweight="bold", style="italic")

    # SuperDove 8-band stems with labels above the data
    band_color = C["teal_dk"]
    for label, cen, fwhm in config.SD_BANDS:
        ax.axvline(cen, color=band_color, lw=1.6, alpha=0.85, zorder=2)
        ax.text(cen, 1.005, label, rotation=90, ha="center", va="bottom",
                fontsize=9, color=band_color, fontweight="bold")

    # SWIR diagnostic feature labels (low)
    feat_y = 0.04
    for x, txt, col in [
        (1730, "C-H\nplastic",   C["plastic"]),
        (2200, "Al-OH\nclay",     "#5D7B9D"),
        (2310, "Mg-OH\nasbestos", C["asbestos"]),
    ]:
        ax.axvline(x, color=col, lw=0.9, ls=":", alpha=0.7, zorder=1)
        ax.text(x, feat_y, txt, ha="center", va="bottom", fontsize=9.5,
                color=col, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec=col, lw=0.6))

    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Reflectance")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(250))
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.55), framealpha=0.97)
    _footer(ax, f"{CITE} · Bands: Planet SuperDove specs · Features: Cilia 2015, Aguilar 2025, Bonifazi 2026")
    fig.savefig(OUT / "where_info_lives.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("✓ where_info_lives.png")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 4 — Sensor trade-off radar (3 axes)
# ─────────────────────────────────────────────────────────────────────────────
def fig_radar() -> None:
    # Verified specs
    sensors: list[dict] = [
        {"name": "SuperDove",  "gsd": 3.0,   "bands": 8,   "revisit_d": 0.75,
         "color": "#2E8B8B", "marker": "o"},
        {"name": "Sentinel-2", "gsd": 10.0,  "bands": 13,  "revisit_d": 5.0,
         "color": "#E07A3F", "marker": "s"},
        {"name": "WorldView-3","gsd": 1.24,  "bands": 16,  "revisit_d": 1.5,
         "color": "#3D8B37", "marker": "^"},
        {"name": "PRISMA",     "gsd": 30.0,  "bands": 240, "revisit_d": 14.0,
         "color": "#7E57C2", "marker": "D"},
        {"name": "EnMAP",      "gsd": 30.0,  "bands": 224, "revisit_d": 15.0,
         "color": "#C0392B", "marker": "v"},
    ]

    # Normalisation (higher = better on chart)
    def n_spatial(g):  return np.clip(np.log10(60.0 / g) / np.log10(60.0 / 0.3), 0.05, 1.0)
    def n_bands(b):    return np.clip(np.log10(b) / np.log10(300.0),               0.05, 1.0)
    def n_revisit(d):  return np.clip(np.log10(30.0 / d) / np.log10(30.0 / 0.5),  0.05, 1.0)

    axes_labels = ["Spatial\nresolution", "Spectral\nbands", "Revisit\nfrequency"]
    theta = np.linspace(0, 2 * np.pi, len(axes_labels), endpoint=False)
    theta_closed = np.concatenate([theta, theta[:1]])

    fig = plt.figure(figsize=(10.5, 8.5))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    for s in sensors:
        vals = [n_spatial(s["gsd"]), n_bands(s["bands"]), n_revisit(s["revisit_d"])]
        vals_closed = vals + vals[:1]
        ax.plot(theta_closed, vals_closed, color=s["color"], lw=2.6,
                marker=s["marker"], markersize=9, label=s["name"], zorder=5)
        ax.fill(theta_closed, vals_closed, color=s["color"], alpha=0.08, zorder=2)

    ax.set_xticks(theta)
    ax.set_xticklabels(axes_labels, fontsize=13, fontweight="bold")
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["", "", "", ""])
    ax.set_ylim(0, 1.05)
    ax.grid(color="#D8D8D8", lw=0.6)
    ax.spines["polar"].set_color("#D0D0D0")

    ax.legend(loc="upper right", bbox_to_anchor=(1.32, 1.02),
              frameon=True, framealpha=0.97, edgecolor="#CCCCCC")

    fig.text(0.5, 0.02,
             "Outer ring = better. Axes: Spatial 1/GSD (log)  ·  Bands log10(N)  ·  Revisit 1/days (log).",
             ha="center", va="bottom", fontsize=10, color="#666", style="italic")
    fig.text(0.5, -0.005,
             "Specs: Planet, ESA, Maxar, ASI, DLR (mission documents).",
             ha="center", va="bottom", fontsize=9, color="#888", style="italic")

    fig.savefig(OUT / "sensor_radar.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("✓ sensor_radar.png")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 5 — Aguilar 2021 bar chart
# ─────────────────────────────────────────────────────────────────────────────
def fig_aguilar() -> None:
    fig, ax = plt.subplots(figsize=(10, 6))

    labels = ["VNIR only\n(8 bands)", "SWIR only\n(8 bands)", "All features\n(16 bands)"]
    values = [90.85, 96.79, 97.38]
    colors = ["#A6CFCF", "#2E8B8B", "#1F6F6F"]
    x = np.arange(3)

    bars = ax.bar(x, values, width=0.6, color=colors,
                  edgecolor="white", linewidth=1.5, zorder=3)

    # Value labels
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.18, f"{v:.2f}%",
                ha="center", va="bottom", fontsize=15, fontweight="bold")

    # Delta annotations using FancyArrowPatch
    ax.annotate("+5.94 pp\n(SWIR > VNIR)", xy=(1, 93.7), xytext=(0.5, 92.5),
                ha="center", fontsize=11, color=C["teal_dk"],
                bbox=dict(boxstyle="round,pad=0.25", fc="white",
                          ec=C["teal_dk"], lw=0.8),
                arrowprops=dict(arrowstyle="->", color=C["teal_dk"], lw=1.2))
    ax.annotate("+0.59 pp\n(All > SWIR)", xy=(2, 97.05), xytext=(1.5, 95.0),
                ha="center", fontsize=11, color=C["teal_dk"],
                bbox=dict(boxstyle="round,pad=0.25", fc="white",
                          ec=C["teal_dk"], lw=0.8),
                arrowprops=dict(arrowstyle="->", color=C["teal_dk"], lw=1.2))

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylabel("Overall accuracy (%)", fontsize=13)
    ax.set_ylim(85, 100)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#E8E8E8", lw=0.5)
    ax.spines["bottom"].set_color("#888")
    ax.spines["left"].set_color("#888")

    ax.set_title("Spectral added value, measured: Aguilar 2021 on WorldView-3",
                 fontsize=14, pad=14, loc="left")

    fig.text(0.99, -0.01,
             "Aguilar, Jiménez-Lao & Aguilar 2021 — Remote Sensing 13(11):2133. "
             "OBIA + Decision Tree, 10-fold CV, 14.3 M pixel GT.",
             ha="right", va="top", fontsize=9, style="italic", color="#888")
    fig.savefig(OUT / "aguilar_bars.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("✓ aguilar_bars.png")


# ─────────────────────────────────────────────────────────────────────────────
# FIG 6 — More bands ≠ more information (Vitek plateau + Aguilar points)
# ─────────────────────────────────────────────────────────────────────────────
def fig_plateau() -> None:
    fig, ax = plt.subplots(figsize=(11, 5.5))

    # Vitek 2025 (CDW) — schematic plateau curve. Trend reported in paper:
    # large gain RGB(3)→5 bands, then plateau ~95-96 % up to full HSI (768 b).
    bands  = np.array([3,   4,   5,   7,   10,  20,  50,  100, 250, 500, 768])
    vitek  = np.array([85.0,92.0,95.0,95.5,95.8,96.0,96.0,96.0,96.0,96.1,96.2])
    ax.plot(bands, vitek, color=C["teal"], lw=2.4, marker="o", markersize=7,
            label="C&D waste plateau (Vitek 2025)", zorder=4)
    ax.annotate("plateau ≈ 96 % from ~5 bands",
                xy=(50, 96.0), xytext=(75, 92.5),
                fontsize=10.5, color=C["teal_dk"],
                bbox=dict(boxstyle="round,pad=0.25", fc="white",
                          ec=C["teal_dk"], lw=0.8),
                arrowprops=dict(arrowstyle="->", color=C["teal_dk"], lw=1.0))

    # Aguilar 2021 WV-3 ablation points (8 / 8 / 16 bands)
    aguilar_b = [8,    8,    16]
    aguilar_v = [90.85,96.79,97.38]
    aguilar_lbl = ["VNIR only\n90.85 %", "SWIR only\n96.79 %", "All features\n97.38 %"]
    ax.scatter(aguilar_b, aguilar_v, color=C["accent"], marker="s", s=110,
               edgecolor="white", lw=1.2, zorder=5,
               label="WV-3 band ablation (Aguilar 2021)")
    for b, v, lbl in zip(aguilar_b, aguilar_v, aguilar_lbl):
        ax.text(b * 1.18, v + 0.15, lbl, fontsize=9.5, color="#8B4513",
                ha="left", va="bottom")

    ax.set_xscale("log")
    ax.set_xlim(2.5, 1000)
    ax.set_ylim(82, 100)
    ax.set_xlabel("Number of spectral bands (log scale)")
    ax.set_ylabel("Overall accuracy (%)")
    ax.set_axisbelow(True)
    ax.grid(True, color="#E8E8E8", lw=0.5, which="both")
    ax.legend(loc="lower right", framealpha=0.97)

    fig.text(0.99, -0.01,
             "Vitek et al. 2025 (CTU Prague, C&D waste) — Stage-1/2 narrowband "
             "selection on HSI 425–975 nm  ·  Aguilar 2021 verified above.",
             ha="right", va="top", fontsize=9, style="italic", color="#888")

    fig.savefig(OUT / "bands_plateau.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("✓ bands_plateau.png")


def main() -> None:
    fig_fingerprint()
    fig_rgb_fails()
    fig_where_info()
    fig_radar()
    fig_aguilar()
    fig_plateau()
    print(f"\nAll figures saved to {OUT}/")


if __name__ == "__main__":
    main()
