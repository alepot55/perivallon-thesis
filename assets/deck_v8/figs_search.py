"""Literature-search flow figure (figs/search_flow.png).
Minimal version: four stations on one line, no boxes.
Counts verified against papers/literature_search and papers/INDEX.md.
"""
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).resolve().parent / "figs"
INK = "#1A1A1A"; MUT = "#666666"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "savefig.dpi": 300, "savefig.bbox": "tight",
})

# main text, size, sub-label
stations = [
    ("699", 26, "unique records\nscripted Scopus queries"),
    ("screening", 15, "task fit, GSD,\nrecency"),
    ("47", 26, "papers selected\nannotated library"),
    ("47", 26, "cited in this deck"),
]

fig, ax = plt.subplots(figsize=(9.6, 1.7))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
xs = [12.5, 37.5, 62.5, 87.5]
for x, (main, sz, sub) in zip(xs, stations):
    ax.text(x, 68, main, ha="center", va="center",
            fontsize=sz, fontweight="bold", color=INK)
    ax.text(x, 26, sub, ha="center", va="center", fontsize=9.5, color=MUT)
for x0, x1 in zip(xs[:-1], xs[1:]):
    ax.add_patch(FancyArrowPatch((x0 + 9, 68), (x1 - 9, 68),
                 arrowstyle="-|>", mutation_scale=12, lw=1.1, color=INK))
fig.savefig(OUT / "search_flow.png"); plt.close(fig)
print("saved", OUT / "search_flow.png")
