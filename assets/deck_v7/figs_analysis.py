"""Deck v7 analysis figures (verified numbers only).
1. alari_perclass.png  - per-class F1, 10-category model (Alari 2024, Table 4.13)
2. bands_evidence.png  - accuracy vs number of bands (Vitek 2025) + where the
                         optimal extra bands fall vs WV-3 / PNeo VNIR bands
"""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figs")
INK = "#1A1A1A"; MUT = "#666666"; GRID = "#E8E8E8"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 11, "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK,
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "savefig.dpi": 300, "savefig.bbox": "tight",
})

# 1 -- Alari 2024 per-class F1, 10 categories (thesis Table 4.13, ResNet-50 + IDA)
data = [
    ("Rubble / excavated earth", 72.49),
    ("Bulky items", 70.69),
    ("Closed containers", 67.75),
    ("Scrap", 61.60),
    ("Vehicles", 50.00),
    ("Plastic", 44.14),
    ("Wood", 37.04),
    ("Big bags", 34.62),
    ("Unknown waste", 34.29),
    ("Tires", 18.57),
]
SPECTRAL = {"Rubble / excavated earth", "Plastic", "Wood", "Tires"}
labels = [d[0] for d in data][::-1]
vals = [d[1] for d in data][::-1]
cols = ["#1A1A1A" if l in SPECTRAL else "#C4C4C4" for l in labels]

fig, ax = plt.subplots(figsize=(6.4, 4.1))
bars = ax.barh(labels, vals, color=cols, edgecolor=INK, lw=0.6, height=0.62)
for b, v in zip(bars, vals):
    ax.text(v + 1.2, b.get_y() + b.get_height() / 2, f"{v:.1f}",
            va="center", fontsize=9, color=INK)
ax.axvline(59.42, color=MUT, lw=1.2, ls="--")
ax.text(59.42, 9.55, "weighted F1 59.4", fontsize=8.5, color=MUT,
        ha="center", va="bottom")
ax.set_xlim(0, 85)
ax.set_xlabel("F1 (%)")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.grid(axis="x", alpha=0.3, color=GRID)
ax.tick_params(axis="y", labelsize=9.5)
leg = [Rectangle((0, 0), 1, 1, fc="#1A1A1A", ec=INK, lw=0.6),
       Rectangle((0, 0), 1, 1, fc="#C4C4C4", ec=INK, lw=0.6)]
ax.legend(leg, ["spectral-analysis target", "other classes"],
          loc="lower right", fontsize=8.5, frameon=False)
fig.savefig(os.path.join(OUT, "alari_perclass.png")); plt.close(fig)

# 2 -- Vitek 2025: few well-chosen bands close most of the RGB gap
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.4),
                             gridspec_kw={"width_ratios": [1, 1.25]})

# left: accuracy vs number of bands (RCR 2025, Fig. 5 values)
x = [3, 5, 12]
y = [0.87, 0.96, 0.97]
a1.plot(x, y, color=INK, lw=1.8, marker="o", ms=6, mfc="white", mec=INK)
a1.annotate("RGB only", xy=(3, 0.87), xytext=(10, -4), textcoords="offset points",
            fontsize=9, color=INK)
a1.annotate("RGB + 2 chosen bands", xy=(5, 0.96), xytext=(10, -14),
            textcoords="offset points", fontsize=9, color=INK)
a1.axhline(0.97, color=MUT, lw=1.0, ls=":")
a1.text(11.8, 0.9745, "12 bands $\\approx$ full spectrum (768)", fontsize=8.5,
        color=MUT, va="bottom", ha="right")
a1.set_xlim(2, 13); a1.set_ylim(0.82, 1.0)
a1.set_xticks([3, 5, 12])
a1.set_xlabel("number of input bands"); a1.set_ylabel("accuracy, 10 C&D materials")
for sp in ("top", "right"): a1.spines[sp].set_visible(False)
a1.grid(alpha=0.3, color=GRID)

# right: where the optimal extra bands sit vs sensor VNIR bands
wv3 = [("Coastal", 400, 450), ("Blue", 450, 510), ("Green", 510, 580),
       ("Yellow", 585, 625), ("Red", 630, 690), ("Red Edge", 705, 745),
       ("NIR1", 770, 895)]
wv3_nir2 = (860, 1040)
pneo = [("Deep Blue", 400, 450), ("Blue", 450, 520), ("Green", 530, 590),
        ("Red", 620, 690), ("Red Edge", 700, 750), ("NIR", 770, 880)]
def overlaps(lo, hi):
    return (lo < 750 and hi > 650) or (lo < 1000 and hi > 850)
for lo, hi in [(650, 750), (850, 1000)]:
    a2.axvspan(lo, hi, color="#EDEDED", zorder=0)
a2.text(700, 2.72, "optimal\n650-750", fontsize=8, ha="center", color=MUT)
a2.text(925, 2.72, "optimal\n850-1000", fontsize=8, ha="center", color=MUT)
for name, lo, hi in wv3:
    dark = name in ("Red Edge", "NIR1")
    a2.add_patch(Rectangle((lo, 1.95), hi - lo, 0.50,
                 fc="#1A1A1A" if dark else "white", ec=INK, lw=0.9))
a2.add_patch(Rectangle((wv3_nir2[0], 1.62), wv3_nir2[1] - wv3_nir2[0], 0.22,
             fc="#1A1A1A", ec=INK, lw=0.9))
a2.text(1048, 1.73, "NIR2", fontsize=7.5, va="center", color=INK)
for name, lo, hi in pneo:
    dark = name in ("Red Edge", "NIR")
    a2.add_patch(Rectangle((lo, 0.70), hi - lo, 0.50,
                 fc="#1A1A1A" if dark else "white", ec=INK, lw=0.9))
a2.text(392, 2.05, "WorldView-3", fontsize=9.5, ha="right", va="center")
a2.text(392, 0.95, "Pléiades Neo", fontsize=9.5, ha="right", va="center")
a2.set_xlim(385, 1105); a2.set_ylim(0.35, 3.25)
a2.set_yticks([])
a2.set_xticks([400, 500, 600, 700, 800, 900, 1000])
a2.set_xlabel("Wavelength (nm)")
for sp in ("top", "right", "left"): a2.spines[sp].set_visible(False)
leg = [Rectangle((0, 0), 1, 1, fc="#1A1A1A", ec=INK, lw=0.9),
       Rectangle((0, 0), 1, 1, fc="white", ec=INK, lw=0.9)]
a2.legend(leg, ["extra band (beyond RGB) overlapping an optimal region", "other VNIR bands"],
          loc="upper left", fontsize=8, frameon=False, ncol=2,
          bbox_to_anchor=(0.02, 1.13), handlelength=1.4)
fig.subplots_adjust(wspace=0.25)
fig.savefig(os.path.join(OUT, "bands_evidence.png")); plt.close(fig)
print("ok")
