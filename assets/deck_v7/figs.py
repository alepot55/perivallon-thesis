"""Deck v7 figures. Sober, few, verified.
1. vnir_signatures.png  - splib07a curves restricted to 400-1050 nm with WV-3/PNeo band centres
2. search_flow.png      - literature search numbers (Scopus 699 -> library 47)
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path("/home/alepot55/Desktop/uni/Tesi")
sys.path.insert(0, str(ROOT / "spectral"))
from spectral_plots.data import load_spectrum
from spectral_plots import config

ZIP = ROOT / "spectral/data/ASCIIdata_splib07a.zip"
OUT = ROOT / "assets/deck_v7/figs"
INK = "#1A1A1A"; MUT = "#666666"; GRID = "#E8E8E8"
VEG = "#008300"; PLA = "#eb6834"; CON = "#555555"; ASB = "#9B3D6F"
WV3 = "#2a78d6"; PNEO = "#eb6834"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 11, "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK,
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "savefig.dpi": 300, "savefig.bbox": "tight",
})

# 1 -- VNIR signatures (400-1050 nm only; SWIR is out of scope)
series = [("Green vegetation", VEG, "Vegetation"),
          ("HDPE (white opaque)", PLA, "Plastic (HDPE)"),
          ("Concrete (road)", CON, "Concrete"),
          ("Chrysotile (asbestos)", ASB, "Asbestos (chrysotile)")]
fig, ax = plt.subplots(figsize=(9.4, 4.3))
for key, col, lab in series:
    fp, wt, _ = config.SPECTRA[key]
    wl, r = load_spectrum(ZIP, fp, wt)
    wl = wl * 1000.0 if np.nanmax(wl) < 100 else wl
    m = ~np.isnan(r) & (r > -1.0) & (wl >= 400) & (wl <= 1050)
    ax.plot(wl[m], r[m], color=col, lw=2.2)
    ax.annotate(lab, xy=(wl[m][-1], r[m][-1]), xytext=(6, 0),
                textcoords="offset points", fontsize=9.5, color=col,
                fontweight="bold", va="center")
# band centres: WV-3 VNIR (8) above, PNeo (6) below
wv3 = [425, 480, 545, 605, 660, 725, 833, 950]
pneo = [425, 483, 562, 655, 725, 840]
for b in wv3:
    ax.plot([b], [1.05], marker="v", ms=6, color=WV3, ls="none")
for b in pneo:
    ax.plot([b], [1.00], marker="^", ms=6, color=PNEO, ls="none")
ax.text(1035, 1.05, "WorldView-3 (8 bands)", fontsize=8.5, color=WV3, va="center")
ax.text(1035, 1.00, "Pléiades Neo (6 bands)", fontsize=8.5, color=PNEO, va="center")
ax.axvspan(400, 700, color="#F3F3F3", zorder=0)
ax.text(550, 0.90, "RGB", fontsize=10, color=MUT, ha="center")
ax.text(870, 0.90, "Red Edge + NIR", fontsize=10, color=MUT, ha="center")
ax.set_xlim(400, 1250); ax.set_ylim(0, 1.10)
ax.set_xticks([400, 500, 600, 700, 800, 900, 1000])
ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Reflectance")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.grid(alpha=0.3, color=GRID)
fig.savefig(OUT / "vnir_signatures.png"); plt.close(fig)

# 2 -- literature search flow (verified counts from papers/literature_search)
fig, ax = plt.subplots(figsize=(9.6, 2.5))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
steps = [("Scopus queries\n(scripted, 2 query sets)", ""),
         ("699 unique records\n622 waste + 77 asbestos", ""),
         ("Screening\ntask fit, GSD, recency", ""),
         ("47-paper library\nannotated notes", ""),
         ("This deck\n13 works cited", "")]
n = len(steps); w = 17.0; gap = (100 - n * w) / (n + 1)
for i, (t, _) in enumerate(steps):
    x = gap + i * (w + gap)
    ax.add_patch(Rectangle((x, 25), w, 50, fc="white", ec=INK, lw=1.3))
    ax.text(x + w / 2, 50, t, ha="center", va="center", fontsize=9.3, color=INK)
    if i < n - 1:
        ax.add_patch(FancyArrowPatch((x + w + 0.4, 50), (x + w + gap - 0.4, 50),
                     arrowstyle="-|>", mutation_scale=12, lw=1.4, color=INK))
fig.savefig(OUT / "search_flow.png"); plt.close(fig)
print("figs:", sorted(p.name for p in OUT.glob("*.png")))
