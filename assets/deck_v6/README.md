# Deck — WorldView-3 + Pléiades Neo (black & white, minimal)

`deck_bw.pptx` (27 slides) + `deck_bw.pdf`. Built by **editing the original
`~/Downloads/ultime_slide.pptx` in place** (`edit_deck.py`): the good initial
slides and their embedded paper images are preserved; only the content needed
for the **WV-3 + Pléiades Neo** pivot is changed, and new slides are added in the
SAME minimal B/W standard style (Calibri 23 bold title / 14 body / 8 grey footer).

## Structure (24 slides) — a rigorous SOTA of the task
Reframed as a dataset-independent **state-of-the-art review** of *material classification of
illegal waste from multispectral satellite imagery* (not an experiment pitch). Paper-dense:
6 survey-table slides (Work | Input/GSD | Method | Key result) covering ~30 papers, grouped:
RGB detection · asbestos · plastics/urban · datasets · foundation models · object-vs-material.
Plus physical basis (spectral fingerprint, RGB-fails, feature→band), the SWIR divide, the
Aguilar ablation, gaps, generalization, and a light dataset-independent direction.
Low-resolution Sentinel slides and the experiment/pipeline slides were removed.

## Regenerate
```bash
cd Tesi && source waste/.venv/bin/activate
python3 assets/deck_v6/figs_bw.py      # 4 B/W figures
python3 assets/deck_v6/edit_deck.py    # edits ~/Downloads/ultime_slide.pptx -> deck_bw.pptx (+ ~/Downloads/ultime_slide_v2.pptx)
libreoffice --headless --convert-to pdf --outdir assets/deck_v6 assets/deck_v6/deck_bw.pptx
```
`edit_deck.py` rebuilds two image slides LibreOffice cannot render (fingerprint, sensor)
so the PDF is complete; the pptx itself opens correctly in Google Slides / PowerPoint.
