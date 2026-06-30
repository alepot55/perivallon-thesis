# Deck — WorldView-3 + Pléiades Neo (black & white, minimal)

`deck_bw.pptx` (27 slides) + `deck_bw.pdf`. Built by **editing the original
`~/Downloads/ultime_slide.pptx` in place** (`edit_deck.py`): the good initial
slides and their embedded paper images are preserved; only the content needed
for the **WV-3 + Pléiades Neo** pivot is changed, and new slides are added in the
SAME minimal B/W standard style (Calibri 23 bold title / 14 body / 8 grey footer).

## What changed vs the original 19-slide deck
- New: risk = hazard×exposure×magnitude · asbestos precedents · band→material map ·
  3-axis ablation · generalization table · material→risk tier · asbestos pilot · novelty+checklist.
- Edited: pixel-as-spectrum, sensor trade-off, chosen-data table (WV-3 vs Pléiades Neo),
  Aguilar, more-bands, DOFA, gaps, proposed direction. SuperDove slide → honest-caveat (texture vs chemistry).
- Figures: 4 clean **black & white** figures (`figs_bw/`) from `figs_bw.py`
  (SWIR-8 bottleneck from real splib07a, 3-axis cube, band→material grid, pilot workflow).
  Numbers verified from `papers/notes/`.

## Regenerate
```bash
cd Tesi && source waste/.venv/bin/activate
python3 assets/deck_v6/figs_bw.py      # 4 B/W figures
python3 assets/deck_v6/edit_deck.py    # edits ~/Downloads/ultime_slide.pptx -> deck_bw.pptx (+ ~/Downloads/ultime_slide_v2.pptx)
libreoffice --headless --convert-to pdf --outdir assets/deck_v6 assets/deck_v6/deck_bw.pptx
```
`edit_deck.py` rebuilds two image slides LibreOffice cannot render (fingerprint, sensor)
so the PDF is complete; the pptx itself opens correctly in Google Slides / PowerPoint.
