# Deck v7 — full rewrite after Thomas's 2026-07-03 review

`deck_v7.pptx` (13 slides) + `deck_v7.pdf` + `discorso_v7.pdf`. Copy in `~/Downloads/slide_v7.pptx`.

Addresses every review point: explicit task slide (technique = multi-label image
classification, justified); all 13 materials with in/out decision and criterion;
literature-search methodology with real numbers (Scopus scripted queries → 699 unique
records → 47-paper library → 13 cited); Sentinel-2 and SWIR only as explicit
exclusions; sensors summarized in one slide next to the RGB-limits slide; no
foundation models; work proposal derived from the gaps; plain non-AI prose.
Anchor reference: Alari 2024 (group thesis, politesi 10589/230633).

Regenerate: `python3 assets/deck_v7/figs.py && python3 assets/deck_v7/build_deck.py`
then convert with libreoffice. Discorso: `python3 assets/deck_v7/make_discorso.py`.

QA: 3 iterations, including an independent adversarial review (10 findings, all
resolved; CascadeDumpNet authorship re-verified at the source: Zhang & Ma 2024).
