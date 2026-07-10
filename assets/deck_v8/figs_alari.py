"""Per-category results of Alari 2024, Table 4.13 (IDA + ResNet50, ten categories).
Produces figs/alari_f1.png for the deck.
"""
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / "figs"
INK = "#1A1A1A"; MUT = "#666666"; GRID = "#E8E8E8"; BAR = "#B9B9B9"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 11, "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK,
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "savefig.dpi": 300, "savefig.bbox": "tight",
})

# F1 per class, Alari 2024, Table 4.13
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
WEIGHTED = 59.42

labels = [d[0] for d in data][::-1]
values = [d[1] for d in data][::-1]

fig, ax = plt.subplots(figsize=(5.4, 4.1))
ax.barh(labels, values, color=BAR, edgecolor=INK, lw=0.8, height=0.62)
for i, v in enumerate(values):
    ax.text(v + 1.2, i, f"{v:.1f}", va="center", fontsize=9, color=INK)
ax.axvline(WEIGHTED, color=INK, ls="--", lw=1.2)
ax.text(WEIGHTED + 1, 9.55, f"weighted F1 {WEIGHTED:.1f}", fontsize=8.5, color=MUT)
ax.set_xlim(0, 100)
ax.set_xlabel("F1 (%)")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.grid(axis="x", alpha=0.3, color=GRID)
ax.tick_params(axis="y", labelsize=9.5)
fig.savefig(OUT / "alari_f1.png")
print("saved", OUT / "alari_f1.png")
