#!/usr/bin/env python3
"""
Master asset generator for Deck v5 (Thomas-style B/N minimal).

Output: PNG files in assets/slide_v5/, ready to embed in pptx.

Style: black/white/grays only, sans-serif, clean. No emoji, no color fill,
minimal grid. Aim for "publication-grade B&W figure".
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D
import rasterio

ROOT = Path("/home/alepot55/Desktop/uni/Tesi")
OUT = ROOT / "assets" / "slide_v5"
OUT.mkdir(parents=True, exist_ok=True)

# Style baseline
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": "#000000",
    "axes.labelcolor": "#000000",
    "xtick.color": "#000000",
    "ytick.color": "#000000",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})


# ============================================================
# Asset 1 — Radar chart sensors (slide 7)
# ============================================================
def asset_radar_sensors():
    """3-axis radar: spatial GSD (inverted log), spectral bands (log),
    revisit time (inverted log). 5 sensors plotted."""
    sensors = {
        "SuperDove": {"gsd_m": 3.0, "bands": 8, "revisit_d": 1.0, "swir": False, "free": True},
        "Sentinel-2": {"gsd_m": 10.0, "bands": 13, "revisit_d": 5.0, "swir": True, "free": True},
        "WorldView-3": {"gsd_m": 1.2, "bands": 16, "revisit_d": 1.0, "swir": True, "free": False},  # tasked
        "PRISMA": {"gsd_m": 30.0, "bands": 240, "revisit_d": 7.0, "swir": True, "free": True},
        "EnMAP": {"gsd_m": 30.0, "bands": 230, "revisit_d": 4.0, "swir": True, "free": True},
    }

    # Normalize axes: 0=worst, 1=best
    # Spatial: smaller = better. Use 1/log(gsd) scaled
    # Bands: more = better. Use log(bands) scaled
    # Revisit: faster (smaller days) = better. Use 1/log(days)
    def norm_spatial(gsd):
        # range: WV-3 1.2m (best) to PRISMA 30m (worst)
        return 1 - (np.log10(gsd) - np.log10(1.2)) / (np.log10(30) - np.log10(1.2))

    def norm_bands(b):
        # range: 8 (worst) to 240 (best)
        return (np.log10(b) - np.log10(8)) / (np.log10(240) - np.log10(8))

    def norm_revisit(d):
        # 1 day best, 7 days worst
        return 1 - (np.log10(d) - np.log10(1)) / (np.log10(7) - np.log10(1))

    labels = ["Spatial\nresolution", "Spectral\nbands", "Revisit\nfrequency"]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    linestyles = ["-", "--", "-.", ":", (0, (1, 1))]
    for i, (name, sp) in enumerate(sensors.items()):
        vals = [norm_spatial(sp["gsd_m"]), norm_bands(sp["bands"]), norm_revisit(sp["revisit_d"])]
        vals += vals[:1]
        lw = 2.5 if name == "SuperDove" else 1.5
        ax.plot(angles, vals, linestyle=linestyles[i % len(linestyles)],
                color="black", linewidth=lw, label=name)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_yticklabels([])
    ax.set_ylim(0, 1)
    ax.grid(color="#cccccc", linewidth=0.6, linestyle="-")
    ax.spines["polar"].set_color("#aaaaaa")

    ax.legend(loc="upper right", bbox_to_anchor=(1.32, 1.10), fontsize=10,
              frameon=False, labelspacing=0.8)

    # title removed - slide has its own
    plt.savefig(OUT / "07_radar_sensors.png", dpi=220, bbox_inches="tight")
    plt.close()
    print("✓ 07_radar_sensors.png")


# ============================================================
# Asset 2 — Spectral signatures of 4 materials (slide 5)
# ============================================================
def asset_spectral_signatures():
    """4 materials from USGS splib07a, B/N, with SuperDove + SWIR regions shaded."""
    csv_path = ROOT / "spectral" / "csv" / "spectral_signatures_all_materials.csv"
    df = pd.read_csv(csv_path)
    df = df[df["wavelength_nm"] >= 400]
    df = df[df["wavelength_nm"] <= 2500]
    wl = df["wavelength_nm"].values / 1000.0  # to µm

    materials = {
        "Vegetation (aspen leaf)": ("GreenVeg_aspen", "-", 2.0),
        "Bare soil (playa)": ("BareSoil_playa", "--", 1.5),
        "Concrete (grey)": ("Concrete_grey_GDS375", "-.", 1.5),
        "PE plastic (HDPE white)": ("HDPE_white_GDS384", ":", 2.0),
    }

    fig, ax = plt.subplots(figsize=(10, 5.5))

    # SuperDove VNIR band (0.43 - 0.86 µm)
    ax.axvspan(0.43, 0.86, color="#eaeaea", alpha=1.0, zorder=0)
    ax.text(0.645, 0.97, "SuperDove VNIR\n(8 bands)", ha="center", va="top",
            fontsize=9, transform=ax.get_xaxis_transform(), color="#444")

    # SWIR region (1.0 - 2.5 µm)
    ax.axvspan(1.0, 2.5, color="#f5f5f5", alpha=1.0, zorder=0)
    ax.text(1.75, 0.97, "SWIR (chemistry-diagnostic)", ha="center", va="top",
            fontsize=9, transform=ax.get_xaxis_transform(), color="#444")

    for label, (col, style, lw) in materials.items():
        if col not in df.columns:
            continue
        ax.plot(wl, df[col].values, color="black", linestyle=style,
                linewidth=lw, label=label)

    # Annotated diagnostic features
    annotations = [
        (2.31, 0.5, "Mg-OH @ 2.31 µm\n(asbestos cement)", "#666"),
        (1.73, 0.4, "C-H @ 1.73 µm\n(plastic)", "#666"),
        (0.68, 0.6, "Chlorophyll @ 0.68 µm", "#666"),
    ]
    for x, y, txt, c in annotations:
        ax.annotate(txt, xy=(x, y * 0.05 + 0.05), xytext=(x, y),
                    fontsize=8, ha="center", color=c,
                    arrowprops=dict(arrowstyle="->", color=c, lw=0.7))

    ax.set_xlabel("Wavelength (µm)", fontsize=11)
    ax.set_ylabel("Reflectance", fontsize=11)
    ax.set_xlim(0.4, 2.5)
    ax.set_ylim(0, 0.8)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(color="#dddddd", linewidth=0.5, axis="y")

    # title removed - slide has its own
    plt.savefig(OUT / "05_spectral_signatures.png")
    plt.close()
    print("✓ 05_spectral_signatures.png")


# ============================================================
# Asset 3 — SuperDove bands on EM spectrum (slide 12 / 14)
# ============================================================
def asset_superdove_bands():
    """8 SuperDove bands shown on EM spectrum, with asbestos chrysotile spectrum
    sketched and SWIR gap highlighted."""
    csv_path = ROOT / "spectral" / "csv" / "spectral_signatures_all_materials.csv"
    df = pd.read_csv(csv_path)
    df = df[(df["wavelength_nm"] >= 400) & (df["wavelength_nm"] <= 2500)]
    wl_um = df["wavelength_nm"].values / 1000.0

    # SuperDove band centers (nm)
    sd_bands = {
        "Coastal Blue": 443,
        "Blue": 490,
        "Green I": 531,
        "Green II": 565,
        "Yellow": 610,
        "Red": 665,
        "Red Edge": 705,
        "NIR": 865,
    }

    fig, ax = plt.subplots(figsize=(11, 4.5))

    # Concrete spectrum (proxy for asbestos cement)
    concrete = df["Concrete_grey_GDS375"].values
    ax.plot(wl_um, concrete, color="#555555", linewidth=1.5,
            label="Concrete (asbestos cement proxy)")

    # SuperDove bands as vertical bars
    for name, c in sd_bands.items():
        ax.axvline(c / 1000, ymin=0, ymax=0.9, color="black", linewidth=1.5, alpha=0.85)
        ax.text(c / 1000, 0.95, name, rotation=90, va="bottom", ha="center",
                fontsize=7.5, transform=ax.get_xaxis_transform())

    # Shade SWIR-missing region
    ax.axvspan(0.86, 2.5, color="#ececec", alpha=0.8, zorder=0)
    ax.text(1.68, 0.5, "SWIR — not covered by SuperDove\n(where Mg-OH, C-H features live)",
            ha="center", va="center", fontsize=10, color="#222",
            transform=ax.get_xaxis_transform())

    # Mark diagnostic SWIR features that SuperDove misses
    for wl, label in [(2.31, "Mg-OH"), (1.73, "C-H"), (2.20, "Al-OH")]:
        ax.axvline(wl, color="#888", linestyle=":", linewidth=1)
        ax.text(wl, 0.05, label, ha="center", va="bottom", fontsize=8,
                color="#444", transform=ax.get_xaxis_transform())

    ax.set_xlabel("Wavelength (µm)", fontsize=11)
    ax.set_ylabel("Reflectance", fontsize=11)
    ax.set_xlim(0.4, 2.5)
    ax.set_ylim(0, 0.6)
    # subtitle removed
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(color="#dddddd", linewidth=0.5, axis="y")

    plt.savefig(OUT / "14_superdove_bands.png")
    plt.close()
    print("✓ 14_superdove_bands.png")


# ============================================================
# Asset 4 — Bands vs accuracy plateau (slide 13)
# ============================================================
def asset_bands_vs_oa():
    """Two datasets: Aguilar 2021 (WV-3 ablation) and cdw-2025 plateau."""
    fig, ax = plt.subplots(figsize=(8, 5))

    # Aguilar 2021 — WV-3 bands vs OA (VNIR=8, SWIR=8, All=16, with VNIR-only=8 → OA 90.85)
    # Actually the original ablation: VNIR (8 bands) 90.85, SWIR (8 bands) 96.79, All (16) 97.38
    # To show as a function of # bands, plot 3 distinct strategies
    bands_aguilar = [8, 8, 16]
    oa_aguilar = [90.85, 96.79, 97.38]
    labels_aguilar = ["VNIR only\n(8 b)", "SWIR only\n(8 b)", "All\n(16 b)"]

    # cdw-2025 — # bands vs OA on C&D waste
    bands_cdw = [3, 4, 5, 10, 50, 200, 768]
    oa_cdw = [85, 92, 95, 95.8, 96, 96.1, 96.2]  # approximate plateau pattern

    ax.plot(bands_cdw, oa_cdw, marker="o", color="black", linewidth=1.5,
            markersize=6, label="C&D waste (Vitek 2025)")

    # Annotate plateau
    ax.annotate("plateau ~96% with ≥5 bands",
                xy=(50, 96), xytext=(150, 90),
                fontsize=9, ha="center",
                arrowprops=dict(arrowstyle="->", color="black", lw=0.6))

    # Aguilar reference points as different markers
    for b, oa, lbl in zip(bands_aguilar, oa_aguilar, labels_aguilar):
        ax.scatter([b], [oa], marker="s", color="white", edgecolor="black",
                   s=80, zorder=5)
        ax.annotate(f"{oa}%\n{lbl}", xy=(b, oa), xytext=(b + 5, oa - 4),
                    fontsize=8, ha="left")

    ax.set_xscale("log")
    ax.set_xlabel("Number of spectral bands (log scale)", fontsize=11)
    ax.set_ylabel("Overall accuracy (%)", fontsize=11)
    ax.set_ylim(80, 100)
    ax.set_xlim(2, 1000)
    # subtitle removed
    ax.grid(color="#dddddd", linewidth=0.5)
    ax.legend(loc="lower right", frameon=False, fontsize=9)

    # Custom legend entry for Aguilar
    handles = [Line2D([], [], marker="s", color="white", markeredgecolor="black",
                      markersize=8, linestyle="None", label="WV-3 ablation (Aguilar 2021)")]
    ax.legend(handles=ax.get_legend().legend_handles + handles,
              loc="lower right", frameon=False, fontsize=9)

    plt.savefig(OUT / "13_bands_vs_oa.png")
    plt.close()
    print("✓ 13_bands_vs_oa.png")


# ============================================================
# Asset 5 — Aguilar ablation bar chart (for slide 10, anchor numbers)
# ============================================================
def asset_aguilar_ablation():
    """Big-number bar chart: VNIR=90.85, SWIR=96.79, All=97.38."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    categories = ["VNIR only\n(8 bands)", "SWIR only\n(8 bands)", "All Features\n(16 bands)"]
    values = [90.85, 96.79, 97.38]
    bars = ax.bar(categories, values, color="white", edgecolor="black",
                  linewidth=1.5, width=0.6, hatch=["", "////", "xx"])

    # Annotate values on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.3,
                f"{val:.2f}%", ha="center", va="bottom",
                fontsize=14, fontweight="bold")

    # Delta annotation
    ax.annotate("", xy=(1, 96.79), xytext=(0, 90.85),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#333"))
    ax.text(0.5, 93.5, "+5.94 pp\n(SWIR>VNIR)", ha="center", va="center",
            fontsize=9, color="#333",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#aaa"))

    ax.annotate("", xy=(2, 97.38), xytext=(1, 96.79),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#333"))
    ax.text(1.5, 97.0, "+0.59 pp\n(All>SWIR)", ha="center", va="center",
            fontsize=9, color="#333",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#aaa"))

    ax.set_ylabel("Overall Accuracy (%)", fontsize=11)
    ax.set_ylim(85, 100)
    # subtitle removed
    ax.grid(color="#dddddd", linewidth=0.5, axis="y")
    ax.set_axisbelow(True)

    plt.savefig(OUT / "10_aguilar_ablation.png")
    plt.close()
    print("✓ 10_aguilar_ablation.png")


# ============================================================
# Asset 6 — Diagnostic regions (slide 12)
# ============================================================
def asset_diagnostic_regions():
    """Bigger view of EM spectrum with SuperDove window vs SWIR diagnostic
    features, asbestos chrysotile sketch."""
    csv_path = ROOT / "spectral" / "csv" / "spectral_signatures_all_materials.csv"
    df = pd.read_csv(csv_path)
    df = df[(df["wavelength_nm"] >= 400) & (df["wavelength_nm"] <= 2500)]
    wl_um = df["wavelength_nm"].values / 1000.0

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True,
                                    gridspec_kw={"height_ratios": [3, 1]})

    # Top: spectra
    for col, label, ls in [
        ("Concrete_grey_GDS375", "Concrete (cement proxy)", "-"),
        ("HDPE_white_GDS384", "PE plastic", "--"),
        ("GreenVeg_aspen", "Vegetation", "-."),
    ]:
        if col in df.columns:
            ax1.plot(wl_um, df[col].values, color="black", linestyle=ls,
                     linewidth=1.5, label=label)

    # SuperDove VNIR window
    ax1.axvspan(0.43, 0.86, color="#dddddd", alpha=0.7, zorder=0)
    ax1.text(0.645, 0.78, "SuperDove\nVNIR",
             ha="center", va="bottom", fontsize=9, fontweight="bold")

    # Annotate diagnostic SWIR
    for wl, label in [(2.31, "Mg-OH\n(asbestos)"), (1.73, "C-H\n(plastic)"), (2.20, "Al-OH\n(clay)")]:
        ax1.axvline(wl, color="#666666", linestyle=":", linewidth=1)
        ax1.text(wl, 0.65, label, ha="center", va="center", fontsize=8.5,
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                           edgecolor="#aaa", linewidth=0.7))

    ax1.set_ylabel("Reflectance", fontsize=11)
    ax1.set_ylim(0, 0.85)
    ax1.legend(loc="upper right", frameon=False, fontsize=9)
    # subtitle removed
    ax1.grid(color="#dddddd", linewidth=0.5, axis="y")

    # Bottom: spectral regions as horizontal bar
    regions = [("VIS", 0.4, 0.7, "#fafafa"),
               ("VNIR (NIR)", 0.7, 1.0, "#f0f0f0"),
               ("SWIR", 1.0, 2.5, "#e0e0e0")]
    for name, x0, x1, c in regions:
        ax2.axvspan(x0, x1, color=c, edgecolor="black", linewidth=0.8)
        ax2.text((x0 + x1) / 2, 0.5, name, ha="center", va="center",
                 fontsize=10, fontweight="bold")

    # Mark SuperDove coverage
    ax2.add_patch(Rectangle((0.43, 0.05), 0.43, 0.20, facecolor="black",
                            edgecolor="none"))
    ax2.text(0.645, 0.05 + 0.10, "SuperDove 8 b", ha="center", va="center",
             color="white", fontsize=8, fontweight="bold")

    # Mark WV-3 SWIR coverage
    ax2.add_patch(Rectangle((1.20, 0.05), 1.20, 0.20, facecolor="black",
                            edgecolor="none"))
    ax2.text(1.80, 0.05 + 0.10, "WV-3 SWIR 8 b", ha="center", va="center",
             color="white", fontsize=8, fontweight="bold")

    ax2.set_xlim(0.4, 2.5)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel("Wavelength (µm)", fontsize=11)
    ax2.set_yticks([])
    ax2.spines["left"].set_visible(False)
    ax2.spines["bottom"].set_visible(True)

    plt.tight_layout()
    plt.savefig(OUT / "12_diagnostic_regions.png")
    plt.close()
    print("✓ 12_diagnostic_regions.png")


# ============================================================
# Asset 7 — Two-step training schematic (slide 3, today's paradigm)
# ============================================================
def asset_two_step_training():
    """Clean B/N schematic: VHR tile → CNN/Transformer → pretraining → 2-step fine-tune → output."""
    fig, ax = plt.subplots(figsize=(11, 3.5))
    ax.axis("off")

    boxes = [
        (0.05, 0.30, 0.14, "VHR aerial /\nsatellite tile\n(RGB)"),
        (0.25, 0.30, 0.14, "CNN /\nTransformer\nbackbone"),
        (0.45, 0.30, 0.14, "Pretraining\n(ImageNet, RSP,\nEO SSL)"),
        (0.65, 0.30, 0.14, "Two-step\nfine-tune\non labels"),
        (0.85, 0.30, 0.14, "Binary\nwaste / no-waste"),
    ]
    for x, y, w, txt in boxes:
        rect = Rectangle((x, y), w, 0.40, facecolor="white", edgecolor="black", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + 0.20, txt, ha="center", va="center", fontsize=10)

    # Arrows
    for x_from, x_to in [(0.19, 0.25), (0.39, 0.45), (0.59, 0.65), (0.79, 0.85)]:
        ax.annotate("", xy=(x_to, 0.50), xytext=(x_from, 0.50),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color="black"))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.savefig(OUT / "03_today_paradigm.png", dpi=220, bbox_inches="tight")
    plt.close()
    print("✓ 03_today_paradigm.png")


# ============================================================
# Asset 8 — Phase 1 workflow (slide 20)
# ============================================================
def asset_phase1_workflow():
    """Asbestos pilot workflow diagram."""
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.axis("off")

    # 6 boxes: SuperDove tiles | Roof polygons | Signature extract | SAM matrix | Clustering | Decision gate
    boxes = [
        (0.02, 0.40, 0.13, "SuperDove\n8-band SR\n(Lombardy)"),
        (0.18, 0.40, 0.13, "Roof polygons\n(WFS Mappatura\n2020 + control)"),
        (0.34, 0.40, 0.13, "Per-polygon\nspectral\nsignature"),
        (0.50, 0.40, 0.13, "SAM pairwise\nsimilarity\nmatrix"),
        (0.66, 0.40, 0.13, "Exploratory\nclustering\n(no labels)"),
        (0.82, 0.40, 0.16, "Decision gate:\nclusters form?\n→ go DL / change"),
    ]
    for x, y, w, txt in boxes:
        rect = Rectangle((x, y), w, 0.40, facecolor="white", edgecolor="black", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + 0.20, txt, ha="center", va="center", fontsize=9)

    for x_from, x_to in [(0.15, 0.18), (0.31, 0.34), (0.47, 0.50), (0.63, 0.66), (0.79, 0.82)]:
        ax.annotate("", xy=(x_to, 0.60), xytext=(x_from, 0.60),
                    arrowprops=dict(arrowstyle="->", lw=1.4, color="black"))

    # Caption
    ax.text(0.5, 0.10, "A terra-terra test before any deep model: get the signatures out, see if they cluster.",
            ha="center", va="center", fontsize=10, style="italic", color="#333")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.savefig(OUT / "20_phase1_workflow.png", dpi=220, bbox_inches="tight")
    plt.close()
    print("✓ 20_phase1_workflow.png")


# ============================================================
# Asset 9 — Roadmap 2 phases (slide 19)
# ============================================================
def asset_roadmap_2phases():
    """Proposed direction: Phase 1 (asbestos pilot) → Phase 2 (MS waste benchmark)."""
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.axis("off")

    # Phase 1 box (left)
    rect1 = Rectangle((0.05, 0.20), 0.40, 0.65, facecolor="white",
                      edgecolor="black", linewidth=2)
    ax.add_patch(rect1)
    ax.text(0.25, 0.78, "Phase 1 — Spectral pilot", ha="center", va="center",
            fontsize=12, fontweight="bold")
    p1_lines = [
        "• Asbestos-cement roofs",
        "• Lombardy WFS ground truth (Mappatura 2020)",
        "• SuperDove 8-band + SAM clustering",
        "• Goal: does VNIR signal exist?",
        "",
        "Decision gate before DL.",
    ]
    for i, line in enumerate(p1_lines):
        ax.text(0.07, 0.65 - i * 0.075, line, ha="left", va="center", fontsize=9.5)

    # Phase 2 box (right)
    rect2 = Rectangle((0.55, 0.20), 0.40, 0.65, facecolor="white",
                      edgecolor="black", linewidth=2)
    ax.add_patch(rect2)
    ax.text(0.75, 0.78, "Phase 2 — MS waste benchmark", ha="center", va="center",
            fontsize=12, fontweight="bold")
    p2_lines = [
        "• Co-register AerialWaste polygons",
        "  with SuperDove archive",
        "• Material-level labels (where available)",
        "• Cross-region train / test split",
        "• DOFA backbone, RGB/+NIR/+RedEdge/8 b",
        "  ablation",
    ]
    for i, line in enumerate(p2_lines):
        ax.text(0.57, 0.65 - i * 0.075, line, ha="left", va="center", fontsize=9.5)

    # Arrow between
    ax.annotate("", xy=(0.55, 0.52), xytext=(0.45, 0.52),
                arrowprops=dict(arrowstyle="->", lw=2, color="black"))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    plt.savefig(OUT / "19_roadmap.png", dpi=220, bbox_inches="tight")
    plt.close()
    print("✓ 19_roadmap.png")


# ============================================================
# Asset 10 — RGB / False-color IR / NDVI three views (slide 4.1)
# ============================================================
def asset_three_views():
    """3 viste della stessa scena PSScene Planet: RGB, false-color IR, NDVI."""
    psscene_path = ROOT / "asbestos/data/planet/PSScene/20260330_105822_49_2514_3B_AnalyticMS_SR_clip.tif"

    with rasterio.open(psscene_path) as src:
        # Pick a window with variety (try a few)
        h, w = src.shape
        # Center-ish, decent size
        win_h, win_w = 600, 800
        row_off = h // 3
        col_off = w // 3
        data = src.read(window=((row_off, row_off + win_h), (col_off, col_off + win_w)))
        # data shape: (4, win_h, win_w) — B, G, R, NIR

    blue, green, red, nir = data[0], data[1], data[2], data[3]

    def stretch(a, pmin=2, pmax=98):
        vmin, vmax = np.percentile(a[a > 0], [pmin, pmax])
        return np.clip((a - vmin) / (vmax - vmin), 0, 1)

    rgb = np.dstack([stretch(red), stretch(green), stretch(blue)])
    nir_fc = np.dstack([stretch(nir), stretch(red), stretch(green)])  # NIR-Red-Green
    ndvi = (nir.astype(float) - red.astype(float)) / (nir.astype(float) + red.astype(float) + 1e-6)
    ndvi = np.clip(ndvi, -1, 1)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(rgb)
    axes[0].set_title("RGB — what we see", fontsize=12, pad=8)
    axes[0].axis("off")

    axes[1].imshow(nir_fc)
    axes[1].set_title("False-color IR — vegetation in red", fontsize=12, pad=8)
    axes[1].axis("off")

    im2 = axes[2].imshow(ndvi, cmap="gray", vmin=-0.2, vmax=0.8)
    axes[2].set_title("NDVI — vegetation index", fontsize=12, pad=8)
    axes[2].axis("off")
    cbar = fig.colorbar(im2, ax=axes[2], fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=8)

    # suptitle removed
    plt.tight_layout()
    plt.savefig(OUT / "04.1_three_views.png", dpi=180, bbox_inches="tight")
    plt.close()
    print("✓ 04.1_three_views.png")


# ============================================================
# Asset 11 — RGB fails: same color different materials (slide 6)
# ============================================================
def asset_rgb_fails():
    """Two pairs side by side: in VIS look identical, in SWIR different."""
    csv_path = ROOT / "spectral" / "csv" / "spectral_signatures_all_materials.csv"
    df = pd.read_csv(csv_path)
    df = df[(df["wavelength_nm"] >= 400) & (df["wavelength_nm"] <= 2500)]
    wl_um = df["wavelength_nm"].values / 1000.0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))

    # Iso-chromaticity: concrete (~grey) vs cellulose (~grey-white) — different SWIR
    pairs = [
        ("Concrete_grey_GDS375", "Concrete", "-"),
        ("Cellulose_SAC6288", "Cellulose (paper)", "--"),
    ]
    for col, lbl, ls in pairs:
        if col in df.columns:
            ax1.plot(wl_um, df[col].values, color="black", linestyle=ls,
                     linewidth=1.6, label=lbl)
    ax1.axvspan(0.43, 0.7, color="#ececec", alpha=0.8, zorder=0)
    ax1.text(0.57, 0.95, "RGB region\n(look similar)", ha="center", va="top",
             fontsize=9, transform=ax1.get_xaxis_transform(), color="#444")
    ax1.axvspan(1.0, 2.5, color="#f5f5f5", alpha=0.8, zorder=0)
    ax1.text(1.75, 0.95, "SWIR\n(diverge)", ha="center", va="top",
             fontsize=9, transform=ax1.get_xaxis_transform(), color="#444")
    ax1.set_xlim(0.4, 2.5)
    ax1.set_ylim(0, 1.0)
    ax1.set_xlabel("Wavelength (µm)")
    ax1.set_ylabel("Reflectance")
    # subtitle removed
    ax1.legend(loc="upper right", frameon=False, fontsize=9)
    ax1.grid(color="#dddddd", linewidth=0.4, axis="y")

    # Sub-pixel mixing: vegetation + concrete → similar to dry grass
    veg = df.get("GreenVeg_aspen")
    conc = df.get("Concrete_grey_GDS375")
    dry = df.get("DryGrass_golden_GDS480")
    if veg is not None and conc is not None and dry is not None:
        mix = 0.5 * veg.values + 0.5 * conc.values
        ax2.plot(wl_um, veg.values, color="black", linestyle="-", linewidth=1.2,
                 alpha=0.5, label="Pure vegetation")
        ax2.plot(wl_um, conc.values, color="black", linestyle="--", linewidth=1.2,
                 alpha=0.5, label="Pure concrete")
        ax2.plot(wl_um, mix, color="black", linestyle="-", linewidth=2.2,
                 label="50% veg + 50% concrete")
        ax2.plot(wl_um, dry.values, color="black", linestyle=":", linewidth=1.8,
                 label="Pure dry grass")
    ax2.axvspan(0.43, 0.7, color="#ececec", alpha=0.8, zorder=0)
    ax2.set_xlim(0.4, 2.5)
    ax2.set_ylim(0, 0.7)
    ax2.set_xlabel("Wavelength (µm)")
    ax2.set_ylabel("Reflectance")
    # subtitle removed
    ax2.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax2.grid(color="#dddddd", linewidth=0.4, axis="y")

    # suptitle removed
    plt.tight_layout()
    plt.savefig(OUT / "06_rgb_fails.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("✓ 06_rgb_fails.png")


if __name__ == "__main__":
    print("Generating Deck v5 assets in", OUT)
    asset_radar_sensors()
    asset_spectral_signatures()
    asset_superdove_bands()
    asset_bands_vs_oa()
    asset_aguilar_ablation()
    asset_diagnostic_regions()
    asset_two_step_training()
    asset_phase1_workflow()
    asset_roadmap_2phases()
    asset_three_views()
    asset_rgb_fails()
    print(f"\nAll assets saved to {OUT}")
