# Deck v8 — restructure after Thomas's feedback on v7 (2026-07-09)

`deck_v8.pptx` (28 slides) + `deck_v8.pdf`. Content is v7's, reorganised; two new
slides (Outline, Alari results by category) and one new figure (`figs/alari_f1.png`).

Second pass (2026-07-10): citations widened to the full 47-paper library.
Inline additions: Shepherd 2025 (asbestos slide), Vitek 2025 + Kokaly/Knaeps
(RGB-vs-VNIR slide), Guo-Li 2020 / Knaeps 2020 / SpectralGPT etc. (excluded
groups), plastic UAV works (objects table). References split by theme over
three slides (waste detection / materials and spectra / objects, platforms,
excluded backbones), 47 works total. `figs_search.py` regenerates the search
flow with the aligned count (47 cited, was inconsistently 24 vs a 23 footer).

What changed versus v7:

- Four linear sections, marked top-right on each slide: Problem and task (3-7),
  Literature search (8-10), State of the art (11-21), Proposed work (22-25).
  New Outline slide (2) states the structure.
- Literature search told in Thomas's order: how it was run (8) -> what it
  returned (9, per-topic table now including the site-level line) -> what was
  kept and why (10). In v7 the found/kept slides came before the method.
- SOTA analysis is one block that funnels from site level to the direct
  predecessor: site-level table -> AerialWaste -> Gibellini -> objects ->
  asbestos -> material-level table -> Alari (two slides) -> synthesis ->
  RGB limits -> gaps. Nothing SOTA remains after the gaps slide.
- Alari 2024 gets two slides: framing/dataset/models (17) and per-category
  results with a verified bar chart from Table 4.13 (18). Regenerate the chart
  with `python3 figs_alari.py`.
- The asbestos pilot slide keeps only the method steps and the decision point;
  its literature rationale lives in the asbestos analysis (slide 15).
- "Available imagery" moved from mid-SOTA to the proposal section (23).

Figures in `figs/` are copies of deck_v7's (state of 2026-07-08) plus
`alari_f1.png`. Regenerate the deck: `python3 build_deck.py`, then convert with
libreoffice. Paths are relative to this directory, no hardcoded ROOT.
