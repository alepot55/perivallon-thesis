# Thesis index v0 — article format (~30 pp + executive summary ~6 pp)

Draft 2026-07-21, post-EDA. Narrative: angle C (weakly-supervised localization under GSD degradation) with base-only fallback built in. Format needs the advisor's written consent (article format rule). Chapter titles in English; the thesis is written in English.

Working title: *Binary illegal-landfill detection in very-high-resolution satellite imagery under resolution degradation, with weakly-supervised localization*

| # | Chapter | Pages | Content (and where it comes from) |
|---|---|---|---|
| 1 | Introduction | 3 | Illegal waste problem, ARPA workflow, PERIVALLON context; why satellite-only and why resolution matters (IRIDE ~1 m, cost); research questions RQ1 (detection vs GSD) and RQ2 (localization from image-level labels vs GSD); contributions list |
| 2 | Related work | 5 | (a) waste detection from remote sensing: Torres 2023 AerialWaste, Gibellini 2025 pipeline (frozen numbers), Sun 2023 dumpsites, Alari 2024 materials; (b) WSOL/CAM methods and their evaluation; (c) resolution/GSD studies. Sources: `baseline_gibellini_frozen.md`, `wsol_mini_sota.md`, loop_prof_sota bibliography |
| 3 | Data | 4 | Satellite-only dataset (1775 tiles: 1294 PNEO + 481 WV3), 6-band VNIR, annotations (binary tile-level; 2827 object bboxes on 286 positives), municipality-based splits at 0.3 m and 1.2 m; the generated ~0.7 m level; strip sources and preprocessing (pansharpening) |
| 4 | Method | 5 | Baseline classifier (Swin-T + RSP, two-step training per Gibellini); resolution degradation protocol; localization: CAM family baseline plus refinement method (defined after mini-SOTA verdict); quantitative localization protocol on the bbox subset (MaxBoxAcc / pointing game / box IoU) |
| 5 | Experiments and results | 8 | E1 baseline across GSD (0.3 / ~0.7 / 1.2 m) — detection F1; E2 localization quality across GSD — the core novelty claim; E3 ablations (CAM variants, spectral bands if time allows, pretraining); comparison against Gibellini aerial numbers as context, not as target |
| 6 | Discussion | 3 | What degrades first (detection vs localization), operational reading for ARPA-style screening at IRIDE-class resolution; limits (dataset size, bbox subset size, no segmentation masks) |
| 7 | Conclusion and future work | 2 | Answers to RQ1/RQ2; future: full VNIR exploitation, in-house FM weights, annotation campaign |
| — | References | — | From `papers/` verified bibliography |

Executive summary (~6 pp): problem, data, method sketch, the two headline results (detection-vs-GSD curve; localization-vs-GSD curve), operational implications.

## Fallback (if the +2 innovation track does not mature by mid-September)

Chapter 5 keeps E1 + a *qualitative* CAM section plus the quantitative evaluation of vanilla Grad-CAM only (still a first for the group's satellite data); chapter 4 drops the refinement method. The rest of the structure is unchanged — this is the ~5-point base thesis, packaged.

## Writing plan hooks

- Every closed experiment feeds its chapter immediately (rule from the 7-point plan); claims tracked in `CLAIMS.md`.
- Chapter 2 draft can start now (sources already frozen); chapter 3 after Enrico confirms dataset details on Thursday; chapter 4 method section after the mini-SOTA verdict.
- Templates: Overleaf IngIndInf Article Format + Executive Summary (links in STATO.md TODO); advisor's written consent required for the article format.
