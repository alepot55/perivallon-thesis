# Deck v7 — full rewrite after Thomas's 2026-07-03 review

`deck_v7.pptx` (28 slides) + `deck_v7.pdf` + `discorso_v7.pdf`. Copy in `~/Downloads/slide_v7.pptx`.

Addresses every review point: explicit task slide + visual task scheme (technique =
multi-label image classification, justified); material taxonomy with real Alari tiles,
all 13 materials with in/out decision and criterion, plus a per-material literature
coverage table; literature-search methodology with real numbers (Scopus scripted
queries → 699 unique records → 47-paper library → 24 cited) and a kept-vs-excluded
table; Sentinel-2 and SWIR only as explicit exclusions; sensors summarized in one
slide next to the RGB-limits slide; no foundation models; work proposal derived from
the gaps (approach + asbestos pilot + evaluation); plain non-AI prose.
Anchor reference: Alari 2024 (group thesis, politesi 10589/230633).

Structure: context → task (definition, scheme) → materials (taxonomy, in/out,
coverage) → search (method, kept/excluded) → site-level (table + AerialWaste /
Gibellini / Alari deep-dives) → material-level (Alari per-class chart, table,
asbestos deep-dive, Cilia weathering, Alari open conclusions) → RGB limits → band-count evidence (Vitek) →
available imagery → SOTA at a glance → gaps → proposal (approach, pilot,
evaluation) → references (24 works). Objects/close-range works appear only in the
coverage table: their task is not ours.

Figures: paper crops in `figs/` (Torres CC BY, Bonifazi CC BY, Gibellini, Alari,
Cilia CC BY) + generated plots (`figs.py`: VNIR signatures; `figs_diagrams.py`:
plain B/W block diagrams; `figs_analysis.py`: Alari per-class F1 from thesis Table
4.13, Vitek band-count evidence vs WV-3/PNeo bands).

Regenerate: `python3 figs.py && python3 figs_diagrams.py && python3 figs_analysis.py && python3 build_deck.py`,
convert with libreoffice. Discorso: `python3 make_discorso.py` (wkhtmltopdf).

QA: iterative build → PDF → thumbnail inspection loop, plus an independent
adversarial number-check (10 findings, all resolved; CascadeDumpNet authorship
re-verified at the source: Zhang & Ma 2024).
