"""Deck v6 figures — WorldView-3 + Pléiades Neo direction.

Reuses the rigorous splib07a / verified-number figures already in
spectral/figures/deck, and builds the NEW figures the pivot needs:
spec cards, SWIR-8 bottleneck (real splib07a), 3-axis ablation cube,
generalization 2-D table, risk chain, asbestos pilot, DOFA schematic,
band->material diagnostic map.

Run:  cd Tesi && python3 assets/deck_v6/make_figs.py
All numbers are verified from papers/notes (see footers); the two
forward-looking figures (cube, 2-D table) are labelled EXPECTED.
"""
from __future__ import annotations
import shutil, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

ROOT = Path("/home/alepot55/Desktop/uni/Tesi")
SPECDIR = ROOT / "spectral"
OUT = ROOT / "assets" / "deck_v6" / "figs"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(SPECDIR))

C = {
    "veg": "#3D8B37", "plastic": "#E07A3F", "concrete": "#555555",
    "asbestos": "#9B3D6F", "teal": "#2E8B8B", "teal_dk": "#1F6F6F",
    "teal_lt": "#A6CFCF", "accent": "#E07A3F", "ink": "#222222",
    "vnir": "#D6EAF1", "swir": "#F5E6D3", "grey": "#888888",
    "gold": "#C9A227", "ok": "#3D8B37", "no": "#C0392B",
}
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "axes.titlesize": 14, "axes.titleweight": "bold",
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "savefig.dpi": 300, "savefig.bbox": "tight",
})

# ── helpers ───────────────────────────────────────────────────────────────
def rbox(ax, x, y, w, h, fc, ec, lw=1.4, rad=0.04, alpha=1.0, z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rad}",
                       fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z,
                       mutation_aspect=1)
    ax.add_patch(p); return p

def arrow(ax, x0, y0, x1, y1, color=C["ink"], lw=2.2, z=3, style="-|>", ms=14):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style,
                 mutation_scale=ms, lw=lw, color=color, zorder=z))

def footer(fig, text):
    fig.text(0.995, 0.012, text, ha="right", va="bottom",
             fontsize=8.5, style="italic", color="#8A8A8A")

def noax(ax):
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

# ── 1. SPEC CARDS — WV-3 vs Pléiades Neo ──────────────────────────────────
def fig_spec_cards():
    fig, ax = plt.subplots(figsize=(11, 5.4)); noax(ax)
    ax.text(50, 95, "The chosen data: two very-high-resolution satellites",
            ha="center", fontsize=16, fontweight="bold", color=C["ink"])
    cards = [
        dict(x=5, title="WorldView-3", sub="Maxar · commercial / ESA TPM",
             accent=C["teal"], rows=[
                ("VNIR", "8 bands @ 1.24 m", C["ok"]),
                ("SWIR", "8 bands @ 3.7 m", C["ok"]),
                ("Pan", "~0.31 m", C["ok"]),
                ("Unique", "Yellow · NIR2", C["ink"]),
                ("Role", "full ladder incl. R3 chemistry", C["teal_dk"]),
             ], badge="SWIR ✓  rare civilian SWIR at VHR", bcol=C["ok"]),
        dict(x=52, title="Pléiades Neo", sub="Airbus · commercial / ESA TPM",
             accent=C["accent"], rows=[
                ("VNIR", "6 bands @ 1.2 m", C["ok"]),
                ("SWIR", "none", C["no"]),
                ("Pan", "~0.30 m", C["ok"]),
                ("Unique", "Deep Blue", C["ink"]),
                ("Role", "VNIR-only cross-sensor axis", C["accent"]),
             ], badge="SWIR ✗  tests how far VNIR-only gets", bcol=C["no"]),
    ]
    for c in cards:
        x = c["x"]; w = 43
        rbox(ax, x, 12, w, 74, "#FFFFFF", c["accent"], lw=2.4, rad=0.05)
        rbox(ax, x, 78, w, 8, c["accent"], c["accent"], rad=0.05)
        ax.text(x + w/2, 82, c["title"], ha="center", va="center",
                fontsize=15, fontweight="bold", color="white")
        ax.text(x + w/2, 74.5, c["sub"], ha="center", fontsize=9.5,
                style="italic", color=C["grey"])
        yy = 67
        for k, v, col in c["rows"]:
            ax.text(x + 3, yy, k, ha="left", fontsize=11, fontweight="bold",
                    color=C["ink"])
            ax.text(x + w - 3, yy, v, ha="right", fontsize=11, color=col)
            ax.plot([x+3, x+w-3], [yy-3.2, yy-3.2], color="#EEEEEE", lw=0.8)
            yy -= 10.5
        rbox(ax, x + 2.5, 13.5, w - 5, 7.5, "#F7F7F7", c["bcol"], lw=1.2)
        ax.text(x + w/2, 17.3, c["badge"], ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=c["bcol"])
    ax.annotate("", xy=(52, 50), xytext=(48, 50),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=C["grey"]))
    ax.text(50, 53, "same\nsites", ha="center", fontsize=8.5, color=C["grey"])
    ax.text(50, 7, "Both sub-metre VHR · access feasible for free via ESA Third-Party Missions (~9-week proposal lead + 1-yr quota)",
            ha="center", fontsize=9.5, color=C["ink"])
    footer(fig, "Specs: Maxar WV-3 · Airbus Pléiades Neo · ESA TPM")
    fig.savefig(OUT / "spec_cards.png"); plt.close(fig)

# ── 2. SWIR-8 bottleneck — real splib07a ──────────────────────────────────
def fig_swir_bottleneck():
    from spectral_plots.data import load_spectrum
    from spectral_plots import config
    ZIP = SPECDIR / "data" / "ASCIIdata_splib07a.zip"
    want = [("Chrysotile (asbestos)", C["asbestos"], "Asbestos-cement (chrysotile)"),
            ("Concrete (road)", C["concrete"], "Concrete / C&D"),
            ("HDPE (white opaque)", C["plastic"], "Plastic (HDPE)")]
    fig, ax = plt.subplots(figsize=(11, 5.2))
    for name, col, lab in want:
        try:
            fp, wt, _ = config.SPECTRA[name]
            wl, r = load_spectrum(ZIP, fp, wt)
            wl = wl * 1000.0 if np.nanmax(wl) < 100 else wl
            m = ~np.isnan(r) & (r > -1.0) & (wl >= 2000) & (wl <= 2500)
            ax.plot(wl[m], r[m], color=col, lw=2.2, label=lab)
        except Exception as e:
            print("  swir skip", name, e)
    for b in [2160, 2200, 2260, 2330]:
        ax.axvspan(b-18, b+18, color=C["teal"], alpha=0.10, zorder=0)
        ax.axvline(b, color=C["teal_dk"], lw=0.7, ls=":", zorder=1)
    ax.axvspan(2300, 2350, color=C["asbestos"], alpha=0.12, zorder=0)
    ax.annotate("Mg-OH ~2.30-2.33 um
(asbestos diagnostic)",
                xy=(2330, 0.66), xytext=(2150, 0.50), fontsize=9.5,
                color=C["asbestos"], fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C["asbestos"], lw=1.2))
    ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Reflectance")
    ax.set_xlim(2000, 2500)
    ax.set_title("The SWIR-8 bottleneck: three hazards crowd into one WV-3 band", pad=10)
    ax.legend(loc="lower left", frameon=True, fontsize=9.5)
    ax.text(0.5, -0.20,
            "asbestos 2.32 . concrete 2.34 . plastic 2.31 - all inside WV-3 SWIR-7 (~2.33 um); discrimination leans on shoulders + VNIR shape",
            transform=ax.transAxes, ha="center", fontsize=9, color=C["ink"],
            bbox=dict(boxstyle="round,pad=0.35", fc="#FFF8F0", ec=C["accent"], lw=0.9))
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(alpha=0.22)
    footer(fig, "USGS splib07a (Kokaly et al., 2017) . WV-3 SWIR band centres: Maxar")
    fig.savefig(OUT / "swir8_bottleneck.png"); plt.close(fig)

def fig_band_material():
    mats = ["Asbestos
(Mg-OH)", "Plastics
(C-H)", "Concrete/C&D
(carbonate)",
            "Slag/rust
(Fe-oxide)", "AC weathering
(moss/lichen)"]
    feats = ["RGB", "Red
Edge", "NIR", "SWIR
1.2um", "SWIR
1.73um", "SWIR
2.2um", "SWIR
2.33um"]
    M = np.array([
        [0,0,0,0,0,1,2],
        [0,0,0,2,2,1,1],
        [0,0,0,0,0,2,2],
        [0,1,2,0,0,0,0],
        [0,2,1,0,0,0,0],
    ])
    fig, ax = plt.subplots(figsize=(11, 5.4))
    cmap = {0:"#F2F2F2", 1:C["teal_lt"], 2:C["teal"]}
    nr, nc = len(mats), len(feats)
    for i in range(nr):
        for j in range(nc):
            v = M[i, j]
            ax.add_patch(mpatches.Rectangle((j, nr-1-i), 1, 1, fc=cmap[v], ec="white", lw=2))
            if v == 2: ax.text(j+0.5, nr-1-i+0.5, "*", ha="center", va="center", color="white", fontsize=16, fontweight="bold")
            elif v == 1: ax.text(j+0.5, nr-1-i+0.5, "o", ha="center", va="center", color=C["teal_dk"], fontsize=12, fontweight="bold")
    ax.axvline(3, color=C["accent"], lw=2.4, ls="--")
    ax.text(1.5, nr+0.30, "Pleiades Neo (VNIR-only)", ha="center", color=C["accent"], fontsize=10.5, fontweight="bold")
    ax.text(5, nr+0.30, "WorldView-3 adds SWIR", ha="center", color=C["teal_dk"], fontsize=10.5, fontweight="bold")
    ax.set_xlim(0, nc); ax.set_ylim(0, nr+0.9)
    ax.set_xticks(np.arange(nc)+0.5); ax.set_xticklabels(feats, fontsize=9)
    ax.set_yticks(np.arange(nr)+0.5); ax.set_yticklabels(mats[::-1], fontsize=9.5)
    ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title("Where each hazard becomes separable: diagnostic feature - band", pad=26)
    leg = [mpatches.Patch(fc=C["teal"], label="strong"), mpatches.Patch(fc=C["teal_lt"], label="weak"), mpatches.Patch(fc="#F2F2F2", label="none")]
    ax.legend(handles=leg, loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=False, fontsize=9.5)
    fig.text(0.5, 0.01, "Diagnostic features: USGS splib07a . Aguilar 2021/2025 . Cilia 2015",
             ha="center", fontsize=8.5, style="italic", color="#8A8A8A")
    fig.savefig(OUT / "band_material_map.png", bbox_inches="tight"); plt.close(fig)

def fig_cube():
    fig, ax = plt.subplots(figsize=(11, 5.6)); noax(ax)
    ax.text(50, 95, "The experiment: a 3-axis band ablation", ha="center",
            fontsize=16, fontweight="bold", color=C["ink"])
    # axis A spectral ladder
    rungs = ["R0 RGB", "R1 +RedEdge/NIR", "R2 full VNIR", "R3 +SWIR"]
    cols = ["#CFE8E8", "#9FD3D3", "#5FB5B5", C["teal"]]
    x0 = 8
    for i, (rg, cc) in enumerate(zip(rungs, cols)):
        rbox(ax, x0 + i*20, 58, 18, 12, cc, C["teal_dk"], lw=1.3)
        ax.text(x0 + i*20 + 9, 64, rg, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color=C["ink"])
        if i < 3:
            arrow(ax, x0+i*20+18, 64, x0+(i+1)*20, 64, color=C["teal_dk"], lw=1.8, ms=12)
    ax.text(4, 64, "A", ha="center", va="center", fontsize=14, fontweight="bold",
            color=C["teal_dk"], bbox=dict(boxstyle="circle,pad=0.3", fc="white", ec=C["teal_dk"]))
    ax.text(8, 73, "Axis A — spectral content (R3 = WV-3 only; the headline test)", fontsize=9.5, color=C["grey"])
    # axis B sensor
    rbox(ax, 8, 38, 34, 12, "#EAF6F6", C["teal"], lw=1.3)
    ax.text(25, 44, "WorldView-3  (VNIR + SWIR)", ha="center", va="center", fontsize=10.5, fontweight="bold", color=C["teal_dk"])
    rbox(ax, 50, 38, 34, 12, "#FDEFE6", C["accent"], lw=1.3)
    ax.text(67, 44, "Pléiades Neo  (VNIR-only)", ha="center", va="center", fontsize=10.5, fontweight="bold", color=C["accent"])
    ax.text(4, 44, "B", ha="center", va="center", fontsize=14, fontweight="bold",
            color=C["accent"], bbox=dict(boxstyle="circle,pad=0.3", fc="white", ec=C["accent"]))
    ax.text(8, 52, "Axis B — sensor (same physical sites)", fontsize=9.5, color=C["grey"])
    # axis C resolution
    rbox(ax, 8, 18, 34, 12, "#F2F2F2", C["grey"], lw=1.3)
    ax.text(25, 24, "native bands", ha="center", va="center", fontsize=10.5, fontweight="bold", color=C["ink"])
    rbox(ax, 50, 18, 34, 12, "#F2F2F2", C["grey"], lw=1.3)
    ax.text(67, 24, "pansharpened", ha="center", va="center", fontsize=10.5, fontweight="bold", color=C["ink"])
    ax.text(4, 24, "C", ha="center", va="center", fontsize=14, fontweight="bold",
            color=C["grey"], bbox=dict(boxstyle="circle,pad=0.3", fc="white", ec=C["grey"]))
    ax.text(8, 32, "Axis C — resolution control (\"SWIR helps\" must hold in native, not only after pan)", fontsize=9.5, color=C["grey"])
    ax.text(50, 8, "Same DOFA backbone throughout · Swin-RSP = RGB reference · run per-pixel AND full-CNN  →  B−A = pure chemistry gain, D−C = total MS gain",
            ha="center", fontsize=9.5, color=C["ink"],
            bbox=dict(boxstyle="round,pad=0.4", fc="#F7FBFB", ec=C["teal"], lw=0.9))
    footer(fig, "Design: loop_prof_sota/04_experimental_design.md")
    fig.savefig(OUT / "ablation_cube.png"); plt.close(fig)

# ── 5. GENERALIZATION 2-D table (EXPECTED) ────────────────────────────────
def fig_gen2d():
    fig, ax = plt.subplots(figsize=(10.5, 4.8)); noax(ax)
    ax.text(50, 95, "Generalization as a first-class axis  (expected pattern, to be measured)",
            ha="center", fontsize=14.5, fontweight="bold", color=C["ink"])
    rows = ["R0 RGB", "R2 full VNIR", "R3 +SWIR"]
    cols = ["In-domain", "Cross-region", "Cross-sensor"]
    # illustrative deltas vs RGB ID; arrows show narrowing/widening
    txt = [["baseline", "−5.1% (Gibellini)", "ports trivially"],
           ["+ small", "gap narrows", "needs harmonization"],
           ["+ chemistry", "gap narrows most", "widens unless SBAF"]]
    shade = [["#F2F2F2", "#FBECEC", "#EAF6F6"],
             ["#E7F3F3", "#EAF6F6", "#FBF3E8"],
             ["#D4EBEB", "#D4EBEB", "#FBECEC"]]
    x0, y0, cw, ch = 18, 18, 24, 16
    for j, c in enumerate(cols):
        ax.text(x0 + j*cw + cw/2, y0 + 3*ch + 4, c, ha="center", fontsize=10.5, fontweight="bold", color=C["teal_dk"])
    for i, r in enumerate(rows):
        ax.text(x0 - 2, y0 + (2-i)*ch + ch/2, r, ha="right", va="center", fontsize=10.5, fontweight="bold", color=C["ink"])
        for j in range(3):
            yy = y0 + (2-i)*ch
            rbox(ax, x0 + j*cw, yy, cw-1.5, ch-1.5, shade[i][j], "#FFFFFF", lw=2, rad=0.03)
            ax.text(x0 + j*cw + (cw-1.5)/2, yy + (ch-1.5)/2, txt[i][j], ha="center", va="center", fontsize=9, color=C["ink"])
    ax.text(50, 9, "Whether added bands narrow or widen the generalization gap is publishable either way — report ID−OOD ΔF1 per cell.",
            ha="center", fontsize=9.5, style="italic", color=C["grey"])
    footer(fig, "Cross-region −5.1%: Gibellini 2025 · cross-sensor: GeoCrossBench — cell values EXPECTED")
    fig.savefig(OUT / "generalization_2d.png"); plt.close(fig)

# ── 6. RISK CHAIN ─────────────────────────────────────────────────────────
def fig_risk_chain():
    fig, ax = plt.subplots(figsize=(11, 4.6)); noax(ax)
    ax.text(50, 93, "From pixels to an ARPA intervention priority", ha="center",
            fontsize=15, fontweight="bold", color=C["ink"])
    steps = [("Image", "WV-3 / PNeo
tile", C["teal_lt"]),
             ("Material", "multiband
-> chemistry", C["teal"]),
             ("EWC hazard", "asbestos
17 06 05*", C["asbestos"]),
             ("Risk", "hazard x exposure
x magnitude", C["accent"]),
             ("ARPA priority", "ranked
inspection list", C["gold"])]
    n = len(steps); w = 17.0; gap = (100 - n*w) / (n+1)
    for i, (t, s, cc) in enumerate(steps):
        x = gap + i*(w+gap)
        rbox(ax, x, 42, w, 26, "#FFFFFF", cc, lw=2.4, rad=0.06)
        rbox(ax, x, 60, w, 8, cc, cc, rad=0.06)
        ax.text(x + w/2, 64, t, ha="center", va="center", fontsize=10, fontweight="bold", color="white")
        ax.text(x + w/2, 51, s, ha="center", va="center", fontsize=9, color=C["ink"])
        if i < n-1:
            arrow(ax, x+w+0.5, 55, x+w+gap-0.5, 55, color=C["grey"], lw=2.0, ms=13)
    ax.text(gap + w/2, 36, "RGB detects the site
(shape / context)", ha="center", fontsize=8.3, color=C["grey"])
    ax.text(gap + 2*(w+gap) + w/2, 36, "multiband infers the material
(SWIR chemistry)", ha="center", fontsize=8.3, color=C["grey"])
    ax.text(50, 18, "Indice di Degrado (d.d.g. 13237/2008) is NOT in the public WFS -> estimated remotely (SWIR Mg-OH + VNIR weathering) = a thesis contribution",
            ha="center", fontsize=8.8, style="italic", color=C["grey"])
    footer(fig, "EWC List of Waste 2000/532/EC . Indice di Degrado d.d.g. 13237/2008 . Fazzo et al. 2023")
    fig.savefig(OUT / "risk_chain.png"); plt.close(fig)

def fig_pilot():
    fig, ax = plt.subplots(figsize=(11, 5.2)); noax(ax)
    ax.text(50, 95, "Phase-1 asbestos pilot: the immediately-feasible demonstrator",
            ha="center", fontsize=15, fontweight="bold", color=C["ink"])
    boxes = [
        (6, 70, "WFS Mappatura_2020\n10,903 roofs (EPSG:32632)", C["teal_lt"]),
        (38, 70, "Self-pair on WV-3 + PNeo\n→ surface reflectance", C["teal_lt"]),
        (70, 70, "Per-roof spectral\nsignature", C["teal_lt"]),
        (6, 42, "(A) Unsupervised\nclustering (no labels)", C["teal"]),
        (38, 42, "DECISION GATE\nclusters form only\nwith SWIR?", C["accent"]),
        (70, 42, "(B) Supervised\nRGB / VNIR / VNIR+SWIR", C["teal"]),
        (38, 14, "EWC 17 06 05*  →  risk tier  →  ARPA priority", C["gold"]),
    ]
    W, H = 26, 18
    for x, y, t, cc in boxes:
        if "GATE" in t:
            rbox(ax, x, y, W, H, "#FDEFE6", C["accent"], lw=2.6, rad=0.05)
        elif "EWC" in t:
            rbox(ax, x, y, 50, 12, "#FBF6E6", C["gold"], lw=2.2, rad=0.05)
        else:
            rbox(ax, x, y, W, H, "#FFFFFF", cc, lw=2.0, rad=0.05)
        tw = 50 if "EWC" in t else W
        th = 12 if "EWC" in t else H
        ax.text(x + tw/2, y + th/2, t, ha="center", va="center",
                fontsize=9.3, color=C["ink"], fontweight="bold" if ("GATE" in t or "EWC" in t) else "normal")
    arrow(ax, 32, 79, 38, 79, color=C["grey"]); arrow(ax, 64, 79, 70, 79, color=C["grey"])
    arrow(ax, 19, 70, 19, 60, color=C["grey"]); 
    ax.text(83, 60, "median reflectance/band\n+ Mg-OH depth ~2.33µm\n+ VNIR weathering (Cilia)", fontsize=8, color=C["grey"], va="top")
    arrow(ax, 51, 42, 51, 26, color=C["accent"])
    ax.text(7, 35, "Public, pixel-accurate labels · textbook SWIR diagnostic · de-risks the whole pipeline before AerialWaste coordinates arrive",
            fontsize=8.8, color=C["grey"])
    footer(fig, "GT: Lombardia WFS Mappatura_2020 · physics: chrysotile Mg-OH 2.30–2.33µm (splib07a)")
    fig.savefig(OUT / "pilot_workflow.png"); plt.close(fig)

# ── 8. DOFA schematic ─────────────────────────────────────────────────────
def fig_dofa():
    fig, ax = plt.subplots(figsize=(11, 4.8)); noax(ax)
    ax.text(50, 94, "DOFA: a band-agnostic backbone makes the comparison fair",
            ha="center", fontsize=15, fontweight="bold", color=C["ink"])
    inputs = [("RGB\n3 b", C["grey"]), ("PNeo\n6 b", C["accent"]),
              ("SuperDove\n8 b", C["gold"]), ("WV-3\n16 b", C["teal"]),
              ("EnMAP\n200+ b", C["asbestos"])]
    for i, (t, cc) in enumerate(inputs):
        y = 78 - i*15
        rbox(ax, 4, y, 15, 11, "#FFFFFF", cc, lw=1.8)
        ax.text(11.5, y+5.5, t, ha="center", va="center", fontsize=9.5, fontweight="bold", color=cc)
        arrow(ax, 19, y+5.5, 38, 45, color=cc, lw=1.4, ms=10)
    rbox(ax, 38, 30, 26, 38, "#EAF6F6", C["teal_dk"], lw=2.4, rad=0.05)
    ax.text(51, 60, "wavelength-\nconditioned\nhypernetwork", ha="center", va="center", fontsize=10, fontweight="bold", color=C["teal_dk"])
    ax.text(51, 42, "generates patch-embed\nweights from each band's\ncentral wavelength", ha="center", va="center", fontsize=8.6, color=C["ink"])
    arrow(ax, 64, 49, 80, 49, color=C["ink"])
    rbox(ax, 80, 40, 16, 18, "#FFFFFF", C["ink"], lw=1.8)
    ax.text(88, 49, "one model\nRGB vs VNIR\nvs SWIR\nfairly", ha="center", va="center", fontsize=8.8, fontweight="bold", color=C["ink"])
    ax.text(50, 12, "Apples-to-apples, not apples-to-oranges: the same backbone ingests any band set keyed by wavelength.",
            ha="center", fontsize=9.5, color=C["grey"])
    footer(fig, "Xiong et al. 2024 (DOFA, arXiv:2403.15356) — pretrained on 5 modalities, handles 202 bands")
    fig.savefig(OUT / "dofa_schematic.png"); plt.close(fig)

# ── 9. reuse rigorous existing figures ────────────────────────────────────
def copy_existing():
    src = SPECDIR / "figures" / "deck"
    for f in ["fingerprint_4_materials.png", "rgb_fails_two_panels.png",
              "where_info_lives.png", "bands_plateau.png", "aguilar_bars.png",
              "sensor_radar.png"]:
        if (src / f).exists():
            shutil.copy(src / f, OUT / f)
            print("  reused", f)
        else:
            print("  MISSING", f)
    # spectral signature library plots
    fs = SPECDIR / "figures"
    for f in ["spectral_plot_03_construction.png", "spectral_plot_01_plastics.png"]:
        if (fs / f).exists(): shutil.copy(fs / f, OUT / f)

def main():
    print("building figures ->", OUT)
    copy_existing()
    # NOTE: swir/band/risk/pilot are produced by fix_figs.py (cleaner layout); run it after.
    for fn in [fig_spec_cards, fig_cube, fig_gen2d, fig_dofa]:
        try:
            fn(); print("  ok", fn.__name__)
        except Exception as e:
            import traceback; print("  FAIL", fn.__name__, e); traceback.print_exc()
    print("done:", len(list(OUT.glob('*.png'))), "figures")

if __name__ == "__main__":
    main()
