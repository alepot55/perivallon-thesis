# Deck v6 — WorldView-3 + Pléiades Neo direction

Expanded SOTA + thesis-direction deck (41 slides, 16:9, didactic colour register).
Pivots off the SuperDove-era deck onto the confirmed experimental data
**WorldView-3 (8 VNIR @1.24 m + 8 SWIR @3.7 m) + Pléiades Neo (6 VNIR @1.2 m)**:
SWIR back in scope, cross-sensor axis, material→EWC→ARPA risk framing.

## Outputs
- `deck_v6.pptx` — the deck (self-contained, figures embedded). Import to Google Slides to refine.
- `deck_v6.pdf` — rendered preview.
- `figs/` — all figures (300 DPI). Data figures from USGS splib07a; numbers verified from `papers/notes/`.

## Regenerate
```bash
cd Tesi && source waste/.venv/bin/activate
python3 assets/deck_v6/make_figs.py     # spec cards, cube, gen-2d, dofa + reuse rigorous figs
python3 assets/deck_v6/fix_figs.py      # swir bottleneck, band→material, risk chain, pilot
python3 assets/deck_v6/fix_figs2.py     # where-info-lives + sensor radar (WV-3 + PNeo)
python3 assets/deck_v6/build_deck.py    # -> deck_v6.pptx
libreoffice --headless --convert-to pdf --outdir assets/deck_v6 assets/deck_v6/deck_v6.pptx
```

## Provenance
- Content: `docs/01_calls/2026-06-30_deck_revision.md` (slide-by-slide plan).
- Research base: `docs/02_research/loop_prof_sota/` (cheatsheet, references, experimental design).
- Forward-looking figures (3-axis cube, generalization 2-D) are labelled EXPECTED — not yet measured.
