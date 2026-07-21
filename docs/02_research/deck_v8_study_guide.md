---
title: "Deck v8 study guide"
subtitle: "Classification of waste materials in very-high-resolution satellite imagery — everything behind the 28 slides"
author: "PERIVALLON thesis · Politecnico di Milano"
date: "2026-07-10"
geometry: margin=2.2cm
fontsize: 10pt
colorlinks: true
toc: true
toc-depth: 2
---

\newpage

# 0. How to use this guide

This document backs `assets/deck_v8/deck_v8.pdf` (28 slides, presented structure of 2026-07-09/10). It has five parts:

1. **The story** — the one-page narrative the deck tells, and the five gaps that generate the proposal.
2. **Slide-by-slide companion** — for each slide: what it claims, where every number comes from, and the questions it invites.
3. **Reference cards** — all cited works, grouped as in the three reference slides. Each card states the *task* (classification / object detection / segmentation / dataset / survey), because "che task è?" is asked for every cited work.
4. **Q&A drill** — the hard questions with defensible answers, aligned to the current scope (VNIR only, no SWIR, no Sentinel-2, no foundation-model backbones).
5. **Cheat sheets** — numbers to memorize, sensor bands, terminology, and known errata/traps.

Delivery reminders (from the 2026-05-27 dry run): present in Italian, keep consolidated English terms in English; linear flow, never jump back to a work already discussed; do not over-explain the physics (NIR/vegetation stays high level); be precise on the SWIR/Sentinel-2 trap — Sentinel-2 already has SWIR, its limit is *resolution* (10–20 m), not the band.

# 1. The story in one page

**Context.** Illegal waste dumping is an environmental crime with public-health consequences. Agencies (ARPA) have limited inspection capacity; priority depends on *what* is dumped — rubble, plastics and asbestos-cement imply very different hazards. Detecting dump *sites* from images is mature; recognising the *material* is not. The group survey (Fraternali et al. 2024: 50 works, 1987–2023, almost all RGB) marks material identification as an open problem.

**Task.** Given a VHR satellite image of a suspected dump site, output the set of waste materials present. Multi-label classification at image level. Input: VHR optical imagery, GSD 0.2–1.3 m. Aerial RGB for the baseline (AerialWaste); satellite VNIR for the multispectral arm, up to 8 bands. SWIR excluded (not in the planned acquisitions; its 3.7 m GSD does not match the task). Sentinel-2 excluded (10–20 m, too coarse). Classification, not detection or segmentation: annotations are image-level, waste piles have no stable shape for boxes, and no segmentation masks exist for these datasets.

**Research question.** *Does VNIR input improve waste-material classification over RGB, and for which materials?*

**Predecessors.** Gibellini 2025 solves site-level binary detection on RGB (Swin-T + RSP, F1 92.02). Alari 2024 is the only direct multi-material predecessor: multi-label classification over 13 categories on AerialWaste-based imagery, weighted F1 69.21 (5 categories) / 59.42 (10 categories), RGB only. The taxonomy and the annotation base come from Alari; the architecture and training recipe come from Gibellini.

**The five gaps (slide 21) and how each maps to the proposal:**

| # | Gap | Proposal element |
|---|---|---|
| 1 | One direct multi-material precedent, ample margin (wF1 59–69) | Continue the group line, same taxonomy (slide 22) |
| 2 | No work measures VNIR added value over RGB for waste materials at VHR | Band ablation, everything else fixed (slide 22) |
| 3 | Results reported as aggregates; per-material behaviour not analysed | Per-material F1 as primary metric (slide 25) |
| 4 | Generalisation across regions rarely evaluated (−5 F1 at site level) | Disjoint geographic train/test areas (slide 25) |
| 5 | Asbestos studied on roofs, in isolation, never inside a waste taxonomy | Asbestos pilot as first step and decision gate (slide 24) |

**Proposal.** Multi-label classification, Swin-T with remote-sensing pretraining (the group baseline), input extended from RGB to VNIR; band ablation RGB → +NIR → full VNIR with same architecture and same splits. Imagery: WorldView-3 (8 VNIR bands, pan 0.31 m) and Pléiades Neo (6 VNIR bands, pan 0.30 m), commercial or free quota via ESA proposal. First step: the asbestos pilot on the Lombardy WFS ground truth (Mappatura 2020, 10,903 roofs) — one material, public pixel-accurate labels, direct regulatory value; the measured VNIR delta on it is the decision gate before the full multi-label extension. A documented negative result ("VNIR does not help material X") retains practical value for sensor choice.

\newpage

# 2. Slide-by-slide companion

## Part I — Problem and task (slides 3–7)

**Slide 1 — Title.** "Classification of waste materials in very-high-resolution satellite imagery. State of the art and thesis proposal."

**Slide 2 — Outline.** Four linear sections: Problem and task (3–7), Literature search (8–10), State of the art (11–21), Proposed work (22–25). Say explicitly that the proposal is derived from the gaps at the end of part 3 — this is the deck's logic and Thomas's requested order.

**Slide 3 — Context.** Claims: detection of dump sites is mature, material recognition is not; the reference survey (Fraternali 2024, 50 works 1987–2023, almost all RGB) marks it open; one group thesis addresses material classification directly (Alari 2024). Images: AerialWaste positives (Torres & Fraternali 2023, CC BY 4.0).
*Likely question:* "mature according to whom?" → Gibellini F1 92.02, AerialWaste ensemble 92.4, Disaitek ~95% operational (vendor), CascadeDumpNet mAP 84.6, Sun 2023 ~2,500 dumpsites — all site-level, all RGB.

**Slide 4 — Task definition.** The most attacked slide; know every sentence.

- Objective: given a VHR satellite image of a suspected site, output the *set* of materials present. Multi-label, image level.
- Input GSD 0.2–1.3 m. Baseline arm: aerial RGB (AerialWaste, 20–50 cm). Multispectral arm: satellite VNIR up to 8 bands (WV-3), 6 bands (Pléiades Neo).
- SWIR excluded for two independent reasons: (a) not in the planned acquisitions; (b) WV-3 SWIR is 3.7 m GSD — incompatible with a sub-metre task. Do not say "SWIR is useless": the spectral evidence for SWIR is strong (plastics C–H at 1215/1732 nm, asbestos Mg–OH at ~2.31 µm), the exclusion is *practical and geometric*.
- Sentinel-2 excluded: 10–20 m. The limit is resolution, not band coverage (it has SWIR).
- Why classification and not object detection / segmentation: annotations are image-level (Alari: 11,477 multi-label); waste piles have no stable shape for boxes; no segmentation masks exist for these datasets (AerialWaste has masks on only 169 test images — evaluation material, not training).
- Research question: does VNIR improve waste-material classification over RGB, and for which materials?

**Slide 5 — Task scheme.** One image in, a set of material labels out; the same scheme runs with RGB or VNIR input; only the first layer of the network changes. Tile from Alari 2024. This is the visual anchor for "everything fixed except the input".

**Slide 6 — The material taxonomy.** Ten-category grouping used by Alari; the full annotation set counts 13 categories (adds foundry waste, sludge, tanks as separate classes). Samples and taxonomy from Alari 2024 (politesi 10589/230633), built on AerialWaste annotations. Know the 13: rubble/excavated earth, foundry waste, vehicles, scrap, bulky items, containers, sludge, wood, plastic, big bags, tanks, tires, asbestos(-cement). The 10-category experimental set: rubble, bulky, wood, scrap, plastic, vehicles, tires, big bags, closed containers, unknown material.

**Slide 7 — Materials: which and why.** The scoping table:

| Material group | Target | Spectral analysis | Reason |
|---|---|---|---|
| Rubble, plastic, wood, tires | yes | yes | frequent and confusable in RGB |
| Asbestos-cement | yes | yes, dedicated pilot | public regional ground truth (WFS) |
| Vehicles, tanks, containers, scrap, bulky, big bags | yes | no | shape-based; RGB sufficient in literature |
| Sludge, foundry waste | yes | no | few labels; visually ambiguous at this GSD |

All 13 remain classification targets (continuity with the group dataset); the RGB-vs-VNIR analysis concentrates where colour is ambiguous *and* labels are sufficient. Decision criteria: visual ambiguity in RGB, label availability, hazard relevance.
*Likely question:* "why keep sludge and foundry waste as targets if you don't analyse them?" → continuity and comparability with Alari; they stay in the head, they are just not the focus of the spectral analysis (few labels: 5 of 13 classes have <400 samples in Alari).

## Part II — Literature search (slides 8–10)

**Slide 8 — How it was run.** Scripted queries on the Scopus API (two topics: waste detection in remote sensing; asbestos roof mapping), deduplication, manual screening with explicit criteria, snowballing from the Fraternali 2024 survey and the Alari 2024 references. Artifacts in `papers/literature_search/`; script `papers/scripts/scopus_search.py`. Full accounting: 47 papers, each with a structured note, in `papers/INDEX.md`.

**Slide 9 — What the search returned.** Per-topic table; the message: site detection is well covered, material-level literature is thin.

| Topic | Works at task scale | Note |
|---|---|---|
| Waste sites, no material distinction | Torres 2023, Gibellini 2025, Sun 2023, CascadeDumpNet 2024, CWLD 2024, Disaitek 2024 | mature; answers *where*, not *what* |
| Multi-material waste classification | Alari 2024 | the only direct precedent |
| Asbestos-cement | Saba 2026, Bonifazi 2026, Abbasi 2024, Cilia 2015 | roofs only, never inside a waste taxonomy |
| Tanks | Ramachandran 2024, YOLOv7-OT 2024 | mature object detection |
| Vehicles, containers | vehicle DA 2020, truck-and-container 2025 | VHR object detection |
| Scrap | ELV Hybrid-YOLOv5 2025 | close-range infrared, not satellite |
| Rubble / inert | CWLD 2024; debris volume UAV 2022 | C&D segmentation; UAV photogrammetry |
| Plastic, wood, tires, bulky, big bags, sludge, foundry | none found in scope | only as classes in AerialWaste / Alari |

**Slide 10 — What was kept, what was excluded.** Five excluded groups; each exclusion has one reason:

| Excluded group | Examples | Reason |
|---|---|---|
| Sentinel-2 and marine debris | MARIDA 2022, Tisza 2023 | 10–20 m: pixels too mixed; different domain |
| Spaceborne hyperspectral | Shepherd 2025 (EnMAP), EMIT 2025 | material evidence, but 30–60 m GSD |
| SWIR-based VHR | Aguilar 2021, Guo & Li 2020, Zhou 2021, Aguilar 2025 | SWIR not in our acquisitions; 3.7 m GSD |
| Laboratory / spectral libraries | Vitek 2025, SpectralWaste 2024, Knaeps 2020 | not Earth observation; kept as band evidence |
| EO foundation models | DOFA, AnySat, Prithvi-EO-2, SpectralGPT, +6 | pretrained at 10–30 m; sub-metre transfer unproven |

Kept: works on terrestrial waste or roof materials at task-compatible GSD, plus the reference spectral library. Excluded papers stay in the annotated library as context. Note the deliberate double role: hyperspectral and lab studies are excluded as *methods* but cited as *evidence* that the spectral signal exists — be ready to state this distinction cleanly.

## Part III — State of the art (slides 11–21)

**Slide 11 — Site-level waste detection (table).** Seven rows; know input, task, method, result for each:

| Work | Input / GSD | Task | Method | Result |
|---|---|---|---|---|
| Gibellini 2025 | aerial RGB, 20 cm | classification | Swin-T, RSP pretraining | F1 92.0; cross-region −5.1 |
| AW ensemble 2025 * | aerial RGB | classification | CNN + transformer ensemble | binary F1 92.4 |
| Disaitek 2024 | Pléiades Neo, 30 cm | detection | operational service | ~95% on sites >2 m² (vendor) |
| CascadeDumpNet 2024 | Pléiades, 50 cm | object detection | two-stage CNN + AutoML | mAP 84.6, cross-city transfer |
| Sun 2023 | VHR RGB, 0.3–1 m | object detection | BCA-Net (Faster R-CNN) | ~2,500 dumpsites, 28 cities |
| CWLD 2024 | GF-2 + GE, 0.5–0.8 m | segmentation | DeepLabV3+ variant | F1 88.9, construction waste |
| AerialWaste, Torres 2023 | aerial RGB, 20–50 cm | dataset + cls. | ResNet-FPN baseline | F1 80.7; 22 material tags |

Takeaway line: all RGB — they answer *where* a site is, not *what* it contains. The asterisk marks a preprint; Disaitek is a vendor figure. Precision on Sun 2023 if probed: ~2,500 dumpsites is the hand-labelled dataset (7 countries, ~4,800 km²); the 28 cities are the automated test deployment (763 found, ~98.6% recall vs manual, but precision ~70%).

**Slide 12 — AerialWaste.** 10,434 locations from ARPA Lombardia records, 487 municipalities; three sources: AGEA orthophotos (20 cm), WorldView-3 (30 cm, pansharpened RGB), Google Earth (50 cm). Binary site labels for detection, plus 22 material tags (type of visible object + storage mode) annotated by experts; tags cover ~72% of positives but are metadata, not a benchmark — the dataset was published for detection. This is the label base both Gibellini 2025 and Alari 2024 build on.
Extra depth if asked: 3,478 positive / 6,956 negative (2:1 by design, to emulate real imbalance); 33% waste-confirmed sites, negatives sampled 1–5 km from positives; 169 test images carry 841 segmentation masks over 9 classes; official baseline ResNet50+FPN F1 80.70 / AP 87.99; coordinates withheld (ARPA confidentiality) — re-acquiring multispectral imagery over the same sites requires an agreement; the authors themselves list "addition of NIR" as a planned extension.

**Slide 13 — Gibellini 2025, the site-level baseline.** Binary waste/no-waste on AerialWaste; Swin-T with remote-sensing pretraining (RSP, Million-AID), two-step fine-tuning (TL head-only, then FT unfreezing the last stage). F1 92.02 in domain, accuracy 94.56 (best of a 36-condition factorial: 2 architectures × 3 GSD × 3 context sizes × 2 pretrainings; best = Swin-T + RSP + 20 cm + 100 m context). Cross-region drop 5.1 F1 points on average.

**Erratum to own before anyone else finds it:** the slide says "Greece 85.4, *Serbia* 83.8, Romania 91.5". The paper's generalization sets (Table 3) are Greece 85.45, **Sweden** 83.82, Romania 91.48 — the Greek tiles from a WV-3 acquisition, the Swedish and Romanian ones from Google Earth. Average across the three: F1 86.92 (−5.10), accuracy 87.73 (−6.83). Fix the slide or correct it verbally.
Extra depth: saliency (Grad-CAM) confirms the model attends to waste heaps; output is presence only. Utility study with ARPA operators at threshold 0.7: +63.2% sites found (155 vs 95), −60.2% area inspected, −12.2% time per site, −30% total time. RSP beats ImageNet by ~2.3 F1. This architecture and recipe (reproduced in `waste/`: val F1 0.9519) is the starting point of the proposal.

**Slide 14 — Objects and close range (table).**

| Work | Input | Task | Result |
|---|---|---|---|
| Ramachandran 2024 | VHR satellite | object detection | tanks, P 0.96 / R 0.97, >169k mapped |
| YOLOv7-OT 2024 * | VHR satellite | object detection | tanks, precision 95.9 |
| Truck-and-container 2025 * | VHR satellite | object detection | container size and status |
| Vehicle DA 2020 * | VHR 30–50 cm | object detection | +10% with domain adaptation |
| ELV Hybrid-YOLOv5 2025 | close-range IR | object detection | scrap metals, mAP 84.2 |
| UAV solid waste 2024 * | UAV RGB | segmentation | OA >94, generic waste piles |
| C&D debris UAV 2022 * | UAV + photogrammetry | segmentation | IoU 0.90 + volume estimation |
| fCLIPSeg 2025 | aerial RGB | segmentation | debris, Dice 0.70, event-agnostic |
| Plastic UAV-SWIR 2026 * | UAV hyperspectral SWIR | segmentation | plastic waste, cross-domain |
| Plastic UAV-IoT 2025 * | UAV RGB | object detection | plastic waste, edge deployment |

Takeaway: shape-defined objects are mature; material composition still needs spectra or close range (UAV line surveyed in Drones 2025). Asterisks = pending full-text verification — say so if pressed on a starred number.

**Slide 15 — The asbestos line, in detail.** Six works, one sentence each:

- **Saba 2026** — WorldView-3, VNIR only, 32 classifiers compared; best Macro-F1 97.6 *per-pixel*; Red Edge and NIR carry the discrimination. (Paywalled: numbers from abstract/secondary reporting; say so if pressed.)
- **Bonifazi 2026** — WorldView-3 multi-temporal workflow (Mantova); building-level decisions from pixel classification; tracks roof removals between acquisitions.
- **Abbasi 2024** — aerial RGB with temporal features, OA ~96: shape and time can substitute spectra at fine GSD. (The counter-evidence to "spectra always needed".)
- **Cilia 2015** — airborne hyperspectral (MIVIS), PA 89 / UA 86, plus a weathering index from red/NIR chlorophyll absorption: the degradation angle.
- **Shepherd 2025** — spaceborne hyperspectral (EnMAP, 30 m), field-calibrated library, 86% match on exhaustive ground truth: the signature survives from orbit; the limit is resolution.
- **Asbestos slate on drone RGB (2023)** — partially recognisable by shape and texture alone.

Why it matters here: public ground truth (Lombardy WFS, 10,903 roofs) + VNIR evidence make asbestos the natural pilot. Image: building-level classification on WV-3, Bonifazi et al. 2026, Geomatics (CC BY 4.0).

**Slide 16 — Material-level classification (table).**

| Work | Input / GSD | Task | Result |
|---|---|---|---|
| Alari 2024 (PoliMi) | satellite RGB | multi-label cls. | wF1 69.2 (5 cat.), 59.4 (10 cat.) |
| Saba 2026 * | WV-3 VNIR, 1.24 m | pixel cls. | asbestos, Macro-F1 97.6 |
| Bonifazi 2026 | WV-3 VNIR+SWIR | pixel cls. | asbestos roofs, removal tracking |
| Abbasi 2024 * | aerial RGB | OBIA cls. | asbestos, OA ~96 (shape + time) |
| Cilia 2015 | airborne HSI, 3 m | pixel cls. | asbestos, PA 89 / UA 86 |

One multi-material predecessor; everything else is a single material (asbestos) on roofs. No work measures RGB vs VNIR on waste materials. `*` = paywalled or preprint, reported as such.

**Slide 17 — Alari 2024: framing.** The anchor reference. Know it cold:

- M.Sc. thesis, PoliMi, advisor Fraternali, co-advisor Gibellini, politesi 10589/230633. The only work framing waste-material recognition as multi-label classification, same group, same imagery base.
- Dataset: 11,477 multi-label annotations over 13 categories; 3,190 positive and 7,190 negative images, built on AerialWaste imagery and ARPA records.
- Models: ResNet-50 and Swin backbones with FPN; three multi-label classification heads compared (IDA, Query2Label, ML-Decoder) plus FPN; weighted binary cross-entropy for label imbalance; different pretraining sources compared.
- Headline: weighted F1 69.21 (five categories), 59.42 (ten). RGB only; the spectral dimension untouched — Chapter 5 explicitly lists multi/hyper-spectral imagery as future work (with dataset extension, synthetic augmentation, multi-class pretraining, object detection).

Detail nuance worth having ready: 69.21 is ResNet152+FPN (ResNet50+FPN gives 68.84); 59.42 is ResNet50+IDA, *chosen over* ResNet152+IDA (60.18 wF1) because the smaller model had better positive-instance Hamming loss (0.3035 vs 0.3227) and co-occurrence distribution closer to ground truth — an example of metrics beyond aggregate F1 driving model choice, which conveniently supports gap #3. Head comparison at 10 categories: ML-Decoder 24.05, FPN 57.60, Query2Label 58.69, IDA 59.42 (wF1).

**Slide 18 — Alari 2024: results by category.** The bar chart is Table 4.13 (IDA + ResNet50, ten categories); memorize the order:

| Class | F1 | Class | F1 |
|---|---|---|---|
| Rubble / excavated earth | 72.49 | Plastic | 44.14 |
| Bulky items | 70.69 | Wood | 37.04 |
| Closed containers | 67.75 | Big bags | 34.62 |
| Scrap | 61.60 | Unknown waste | 34.29 |
| Vehicles | 50.00 | Tires | 18.57 |

Weighted F1 59.42 (dashed line). Claims on the slide: 5→10 categories costs 9.8 weighted-F1 points (69.2 → 59.4); five of ten classes below F1 50; attributed to few annotations (tires: 316 images; big bags: 398), high intra-class variance (wood: pallets, sawdust, logs) and inter-class similarity in RGB. The classes that hold are shape/texture-distinctive; the ones that fail are those where RGB appearance is ambiguous. Per-category behaviour, not the aggregate, is where the margin is — this is the starting point of the proposal.
If asked about precision/recall: failing classes fail on *precision* (tires P 11.5 / R 48.2; plastic P 31.0 / R 76.4; wood P 27.9 / R 55.1) — the model over-predicts them.

**Slide 19 — The in-scope SOTA at a glance.** Ten lines summarising every in-scope line of work; the two summary numbers: material-level evidence = one multi-label predecessor + one material (asbestos) studied in isolation. Fraternali 2024 declares the material gap; AerialWaste has 22 tags as metadata only; Gibellini has none (presence); Alari has 13 categories at wF1 59–69; site detectors have none; CWLD covers one material (C&D); the asbestos quartet covers one material; tanks/vehicles/scrap works capture shape, not composition.

**Slide 20 — Where RGB falls short, and what VNIR adds.** Four evidence bullets — this is the scientific heart, know the sources:

1. Different materials share the same colour at 0.3–1.3 m: plastic sheets, asbestos-cement and concrete all appear grey; separation lies beyond 700 nm (spectral libraries: Kokaly 2017 = USGS splib07a; Knaeps 2020 = plastics library).
2. In the group predecessor, 5→10 categories costs 9.8 F1 points (Alari). Finer material distinctions are the hard part.
3. Red Edge and NIR separate vegetation, bare soil and weathered surfaces; in Saba 2026 they drive asbestos discrimination.
4. On 10 construction-and-demolition materials, RGB gives 0.87 accuracy; RGB plus two bands at 650–750 and 850–1000 nm gives 0.96, matching the full 768-band spectrum (Vitek 2025 — *laboratory study*, caveat stated on the slide).

Closing: whether this transfers to waste materials at task GSD, and for which ones, has not been measured — it is the object of the thesis. Figure: reflectance from splib07a, 400–1050 nm, with WV-3/PNeo band centres (Maxar, Airbus data sheets).

**Slide 21 — What is missing.** The five gaps verbatim (see §1). "Material-level labels still missing" is the fundamental gap and comes first in discussion. Each gap maps to one proposal element.

## Part IV — Proposed work (slides 22–25)

**Slide 22 — Approach.** Multi-label image classification, continuing the group line (Gibellini 2025, Alari 2024). Same taxonomy, input extended RGB → VNIR. Band ablation with everything else fixed: same architecture, same splits, only the input changes. Backbone: Swin-T with RSP (the group baseline); extra bands enter via the input layer (weight inflation / random init of the extra channels — implementation detail, volunteer only if asked).

**Slide 23 — Available imagery.** WorldView-3: 8 VNIR bands, pan 0.31 m. Pléiades Neo: 6 VNIR bands, pan 0.30 m. Access: commercial, or free quota via ESA proposal (Third Party Missions; roughly a 9-week proposal cycle plus a one-year quota). This is the band budget: no SWIR, no Sentinel-2. RGB baseline runs on AerialWaste (20–50 cm). Band ranges from Maxar and Airbus data sheets (see §6).

**Slide 24 — First step: the asbestos pilot.** Asbestos is the entry material (single material, public pixel-accurate labels, direct regulatory value). Four steps:

1. Extract roof polygons from the Lombardy WFS registry (Mappatura 2020: 10,903 mapped asbestos-cement roofs, EPSG:32632) and pair them with the available imagery.
2. Build matched RGB and VNIR inputs for the same roofs; add negative roofs from regional building footprints.
3. Train the same classifier on both inputs; compare F1, precision, recall on held-out areas.
4. Decision point: the measured VNIR delta on a single well-labelled material tells whether the full multi-label extension is worth the acquisition cost.

Background not on the slide: the current data track for the pilot is Planet SuperDove (8-band VNIR, 3 m) — signature extraction from GT polygons, pairwise SAM distances, exploratory clustering; the first PSScene strips (2026-03-30) had zero overlap with the GT and serve as pipeline-test data. If the sensor question comes up: the pilot logic (matched RGB vs VNIR on labelled roofs) is sensor-agnostic; SuperDove gives free near-daily 8-band VNIR at 3 m for the signature work, the VHR acquisitions serve the sub-metre classification task.

**Slide 25 — Evaluation.** Five commitments:

- Per-material F1 alongside weighted and macro averages (aggregates hide the target classes).
- Delta vs the RGB baseline per band configuration, with confidence intervals over repeated runs.
- Generalisation: train/test on disjoint geographic areas, besides the standard split.
- Reference points: wF1 69.2 / 59.4 (Alari); Macro-F1 97.6 (Saba, per-pixel) as an upper reference for the pilot, *not directly comparable* (per-pixel vs image-level, roofs vs dumps).
- A negative result (VNIR does not help material X) is documented and practically valuable for sensor choice.

Footer: per-class F1, macro-F1, weighted F1, confusion matrices; splits frozen before testing.

## Part V — References (slides 26–28)

Three thematic slides: waste detection (26), materials and spectra (27), objects/platforms/excluded backbones (28); 47 works total, foundation-model line reported only as an explicit exclusion. Full cards in §3 of this guide.

\newpage

# 3. Reference cards — every cited work

Format: **task** first (the "che task è?" answer), then input/GSD, method, verified numbers, role in the deck, and the caveat to volunteer. Status flags: (paywalled) = numbers from abstract or secondary sources; (preprint) = not peer-reviewed; (vendor) = commercial claim.

## 3.1 Waste detection (reference slide 26)

### Alari 2024 — the anchor
*Fighting environmental crime with deep learning: classifying waste materials from illegal landfills in satellite imagery.* M.Sc. thesis, PoliMi (advisor Fraternali, co-advisor Gibellini), politesi 10589/230633.

- **Task:** multi-label image classification (13 material categories; experiments on 5- and 10-category formulations).
- **Data:** 11,477 multi-label annotations, 3,190 positive + 7,190 negative images, built on AerialWaste imagery + ARPA records. RGB only. Ten-category split: 8,205 train / 1,927 test annotations. Thin classes: vehicles 208 images, tires 316, big bags 398, wood 716 — 5 of 13 classes under 400 samples.
- **Method:** ResNet-50/152 and Swin backbones; FPN vs three multi-label heads (IDA = Interventional Dual Attention, Query2Label, ML-Decoder); weighted BCE for imbalance; pretraining sources compared; evaluation with weighted/macro metrics, multi-label confusion matrices, co-occurrence analysis, Grad-CAM.
- **Numbers:** wF1 69.21 five categories (ResNet152+FPN; ResNet50+FPN 68.84), 59.42 ten categories (ResNet50+IDA; ResNet152+IDA reaches 60.18 but was discarded on Hamming-positive 0.3227 vs 0.3035 and co-occurrence fidelity). Ten-category heads: ML-Decoder 24.05 / FPN 57.60 / Q2L 58.69 / IDA 59.42. Per-class F1: see slide-18 table. Five-category per-class F1 (R50+FPN report): rubble 72.62, bulky 73.61, scrap 58.20, closed containers 69.80, unknown 68.20.
- **Role:** slides 3, 4, 5, 6, 7, 16, 17, 18, 20, 25 — the direct predecessor and comparison baseline; its Ch. 5 lists multispectral as future work, which is the thesis's entry point.
- **Caveats:** used *as comparison*, not as a margin to beat per se; image-level multi-label wF1 is not comparable with per-pixel asbestos figures.

### Fraternali et al. 2024 — the survey
*Solid waste detection, monitoring and mapping in remote sensing images: a survey.* Waste Management / arXiv:2402.09066 (Fraternali, Castelli, Torres).

- **Task:** systematic survey (PRISMA), 50 works 1987–2023 from 1,235 initial records; 3 objectives (Detection 27, Monitoring 11, Mapping 12), 6 task types; 23 satellites, 4 public datasets; only 11/50 use DL, almost all on RGB/pansharpened imagery.
- **Declared gaps** (memorize — they legitimate the thesis): no standard benchmark; poor geographic generalisation; **waste material identification not addressed** (needs ≤30 cm and multispectral); RS cannot tell legal from illegal (risk assessment missing); RS foundation models unexplored for waste; court-proof evidence collection open.
- **Role:** slides 3, 19, 21 — the source of "detection mature, material open".
- **Note:** the arXiv preprint and the Waste Management journal paper are the same work — the library counts them as two entries; if the 47 count is challenged, this is the honest footnote.

### Torres & Fraternali 2023 — AerialWaste
*AerialWaste: a dataset for illegal landfill discovery in aerial images.* Scientific Data 10:63.

- **Task:** dataset (binary scene classification) + baseline classifier.
- **Data:** 10,434 images (v3 ~11.7k): 3,478 pos / 6,956 neg (2:1), 487 Lombardy municipalities, three sources — AGEA 20 cm (~1,100 pos), WV-3 30 cm pansharpened RGB (~250 pos), Google Earth 50 cm (~2,200 pos). Three annotation levels: binary; 22 Type-of-Object + 7 Storage-Mode multi-label tags (~72% of positives); 841 segmentation masks on 169 test images (9 classes). Only 11 images tagged "corrugated sheets / presumed asbestos".
- **Baseline:** ResNet50+FPN, F1 80.70 / AP 87.99 (per-source F1: AGEA 0.82, WV3 0.75, GE 0.80).
- **Role:** slides 3, 11, 12, 19 — the label base of the whole group line.
- **Caveats:** RGB only (authors list NIR as planned extension); coordinates withheld (re-acquisition of MS imagery over the same sites needs an ARPA agreement); Lombardy-only geography.

### Gibellini et al. 2025 — the baseline
*A deep learning pipeline for solid waste detection in remote sensing images.* Waste Management Bulletin, DOI 10.1016/j.wmb.2025.100246 (arXiv 2502.06607).

- **Task:** binary scene classification (waste / no waste) + operational pipeline (tile → classifier → Grad-CAM saliency → GIS), co-designed with ARPA Lombardia.
- **Method:** 36-condition factorial — ResNet-50 vs Swin-T × GSD 20/30/50 cm × context 100/150/210 m × ImageNet vs RSP (Million-AID). Two-step training (TL then FT). Best: Swin-T + RSP + 20 cm + 100 m.
- **Numbers:** F1 92.02, accuracy 94.56; RSP > ImageNet ~2.3 F1; generalization Greece 85.45 (WV-3 tiles), **Sweden** 83.82, Romania 91.48 (Google Earth tiles) — average F1 86.92 (−5.10), accuracy 87.73 (−6.83). Utility (threshold 0.7): +63.2% sites found (155 vs 95), −60.2% area, −12.2% time per site, −30% total time.
- **Role:** slides 11, 13, 21, 22 — architecture and recipe of the proposal; gap #4 (generalisation) quantified here. Reproduced in the repo at val F1 0.9519.
- **Caveats:** presence only, no material; RGB only, stated by the authors as the open limit. Terminology: frame the utility numbers as "individuare siti e classificarli per rischio", not "+63% scoperta".

### Sharmily et al. 2025 — AerialWaste ensembles (preprint)
arXiv:2508.18315. **Task:** binary classification. Lightweight CNN + transformer ensembles on AerialWaste; binary F1 92.41. Role: slide 11/19 — shows the field still does binary, not the 13-class split. Caveat: preprint.

### Zhang & Ma 2024 — CascadeDumpNet
Remote Sensing of Environment 313. **Task:** object detection. Pléiades 0.5 m; two-stage CNN + AutoML, context-fusion module against false alarms; mAP 84.6; Shenzhen→Shanghai/Guangzhou transfer. Role: slide 11 — VHR-satellite dumpsite branch. Caveat: closed access; claims verified via deep-research run.

### Sun et al. 2023 — global dumpsites
*Revealing influencing factors on global waste distribution...* Nature Communications 14:1444.

- **Task:** object detection (BCA-Net = channel-attention module on Faster R-CNN + FPN + ResNet50).
- **Data/numbers:** VHR RGB 0.3–1 m; ~2,500 hand-labelled dumpsites over ~4,800 km² in 7 countries, 4 types (domestic, construction, agricultural, covered). Deployment on 28 cities: 763 dumpsites vs 755 manual (98.6% recall), −96.8% investigation time (6 days vs 6 months). Sensitivity ~98.0% average, precision ~70.1%.
- **Role:** slide 11 — global scale of RGB site detection. Caveat: low precision because at 0.3–1 m the model sees morphology, not composition; China-heavy geography.

### CWLD 2024
*A construction waste landfill dataset of two districts in Beijing.* Scientific Data. **Task:** semantic segmentation dataset + baseline. GF-2 (~80 cm) + Google Earth (~50 cm), 3,653 samples, improved DeepLabV3+: F1 88.9 / IoU 82. Single material family (C&D). Role: slides 11, 19 — the "one material, segmentation" row.

### Disaitek 2024 (vendor)
Illegal Waste Tracker, Disaitek + Airbus Pléiades Neo, CNES agreement 2024-05-27. **Task:** operational detection service. Pléiades Neo 30 cm; ~95% reliability on sites ≥2 m²; qualifies coarse type (end-of-life vehicles, construction waste, tires, vegetal). Role: slides 11, 19 — operational relevance on the exact PNeo sensor. Caveat: grey literature, not peer-reviewed — always attach "vendor figure".

### Tisza 2023
*Waste detection and change analysis based on multispectral satellite imagery.* arXiv:2303.14521. **Task:** pixel classification + change detection (Random Forest). Sentinel-2 (10–20 m bands) + PlanetScope 4-band 3 m; Plastic Index PI = NIR/(NIR+Red); ~96% cross-validation accuracy on ~200k training pixels; river Tisza waste blockages. Role: slide 10 — excluded (10–20 m, different domain), kept as evidence NIR discriminates. Caveat: works only on large dense accumulations (>100 m²); no material analysis.

### MARIDA 2022
*A benchmark for Marine Debris detection from Sentinel-2.* PLOS ONE (Kikaki et al.). **Task:** pixel-level benchmark dataset (15 classes) + baselines. 63 S2 scenes, 11 countries, 1,381 patches 256×256, 837,357 annotated pixels, 3,339 marine-debris pixels. Baselines: RF mean F1 0.79 vs U-Net 0.69; debris IoU 0.55–0.67 (RF). Role: slide 10 — excluded exemplar (10 m, marine). Caveat: debris is sub-pixel at 10 m; separability rides on NIR-865 and SWIR.

## 3.2 Materials and spectra (reference slide 27)

### Saba et al. 2026 (paywalled)
*Asbestos-cement roof classification from WorldView-3 VNIR.* Journal of Hazardous Materials. **Task:** per-pixel classification. WV-3 8 VNIR bands @1.24 m; 32 classifiers compared; best (Fine-KNN) Macro-F1 97.6; binary AC ~99–100%; Red Edge and NIR drive the discrimination. Role: slides 15, 16, 20, 25 — the strongest "VNIR-only suffices for asbestos at fine GSD" evidence, and the pilot's upper reference. Caveats: paywalled (numbers not verified on full text — say so); per-pixel on roofs ≠ image-level on dumps; the sometimes-quoted "HSI 97.3 vs MS 74.4" comparison is unverified — do not use.

### Bonifazi et al. 2026
*A Python-based workflow for asbestos roof mapping and temporal monitoring using satellite imagery.* Geomatics 6(3):41, MDPI, open access.

- **Task:** per-pixel supervised classification (Maximum Likelihood) + building-level aggregation + multi-temporal change.
- **Data:** WV-3 VNIR 8 bands @1.24 m + SWIR 8 bands @3.7 m (16 bands, resampled 1 m), Mantova, Aug 2023 + Jul 2024; fully open-source stack (Py6S, rasterio, scikit-learn).
- **Numbers:** building-level F1 0.87 at 30% threshold (P 0.81 / R 0.92), 0.86 at 20% (P 0.78 / R 0.97); 25,319 buildings processed, 2,286 AC-positive at 20% / 1,554 at 30%; 2024 pass F1 0.79; removal cross-check vs ATS Valpadana registers: 47/80 removed roofs correctly AC in 2023, 31 of those gone in 2024 (~46.6% of 133 documented removals identified).
- **Role:** slides 15, 16 (image credit on 15) — the Italian, satellite, open-source asbestos reference; methodological template for building-level decisions.
- **Caveats:** screening tool, not legal evidence; thresholds Mantova-calibrated; uses SWIR too (our arm does not — cite it for the workflow and the VNIR share, not as a VNIR-only proof).

### Abbasi et al. 2024 (paywalled)
*Multi-temporal change detection of asbestos roofing.* Remote Sensing Applications: Society and Environment. **Task:** OBIA classification + change detection (DenseNet121 + LSTM/Conv1D). Nearmap aerial VHR, **no SWIR**; OA 95.8–96.0, AC class ~94. Role: slides 15, 16 — the counter-evidence: at fine GSD, shape + time can substitute spectra. Useful in Q&A when someone says "asbestos needs SWIR".

### Cilia et al. 2015
*Mapping of asbestos cement roofs and their weathering status using hyperspectral aerial images.* ISPRS IJGI 4(2) (Milano-Bicocca + CNR-IREA).

- **Task:** per-pixel classification (two-step SAM on MNF components) + weathering index.
- **Data:** airborne MIVIS, 102 bands (VIS→TIR), 3 m GSD, five Brianza municipalities (65 km²).
- **Numbers:** PA 89 / UA 86 after the second SAM pass (PA from 75 to 86–89); 3,170 AC buildings ≈ 8% of roofs; ISD weathering index built on chlorophyll absorption at 0.68 µm (moss/lichen colonisation as degradation proxy); ISD vs field ASD R²=0.62 (n=11); ANOVA year F=6.04 p<0.001, exposure F=33.38 p<0.001.
- **Role:** slide 15 — the Italian canonical precursor and the "degradation angle". Caveats: ISD is a vegetation proxy, not a fibre measure; 3 m GSD misses roofs <36 m²; airborne, not scalable. Historical note: an earlier internal memo attributed this DOI to Frassy/Bassani — it is Cilia et al.

### Shepherd et al. 2025
*Detection of asbestos-based cement rooftops in conflict-affected settings using EnMAP hyperspectral data.* Scientific Reports, DOI 10.1038/s41598-025-09738-w.

- **Task:** per-pixel classification, cascade of 8 supervised classifiers (LSU, SVM, SAM, ACE, Mahalanobis, MLC, SID, MF) with 6-of-8 consensus + human verification.
- **Data:** EnMAP L2A, 230 bands, 30 m; Western Negev post-Oct-2023; 2,714 field/scene spectra (ASD FieldSpec 4).
- **Numbers:** ACE best single classifier OA 91.4 / k 0.87 / F1 91.2; SID 90.1; SVM 89.2; 86% positive-match rate vs exhaustive ground survey (823 final detections from 2,300 candidates); rural villages >92%, dense urban worse (mixed pixels, paint-sealing).
- **Role:** slides 10, 15 — proves the AC signature survives from orbit; the limit is the 30 m resolution. That is exactly the sensor trade-off argument.

### Asbestos slate from drone imagery, 2023
PMC open access. **Task:** training-data construction for DL on drone RGB. At UAV GSD asbestos slate is partially recognisable by shape/texture alone. Role: slide 15, last bullet. Thin note; keep to one sentence.

### Vitek et al. 2025 — critical wavelengths
*Critical wavelengths for construction and demolition waste materials.* Resources, Conservation and Recycling, DOI 10.1016/j.resconrec.2025.108123 (CTU Prague).

- **Task:** laboratory band-selection study (hyperspectral camera SPECIM, 768 bands 400–1000 nm; MLP classifier, 2×20 hidden units) on 10 C&D materials (AAC, EPS, asphalt, brick, concrete, mortar, roof tile, ceramic tiles ×2, wood).
- **Numbers (the slide-20 quote):** RGB only = 0.87 accuracy; RGB + 2 well-chosen bands (one in 650–750 nm, one in 850–1000 nm) = 0.96, matching full spectrum (0.97 with 12 features). Insensitive to filter FWHM 5–50 nm. Whole-spectrum features *degrade* the model.
- **Role:** slide 20 — the cleanest "few extra VNIR bands close most of the gap" evidence; note it is 400–1000 nm only, i.e. entirely within our VNIR budget.
- **Caveats:** laboratory (halogen illumination, clean isolated samples); generalisation to outdoor/satellite mixed pixels not tested; concrete remains the confused class. Always attach "laboratory study" — it is printed on the slide.

### Kokaly et al. 2017 — USGS splib07a
USGS Data Series 1035. **Task:** reference spectral library. 2,151 channels, 350–2,500 nm @ ~1 nm; ~2,400 spectra of ~1,300 materials (minerals incl. chrysotile, polymers, vegetation, construction materials); convolutions released for S2, WV-3, Landsat, ASTER. Role: slide 20 figure (reflectance 400–1050 nm with WV-3/PNeo band centres) and the `spectral/` pillar. Caveat: lab conditions — no atmosphere, no mixed pixels, no weathering; it shows separability *exists*, not that a sensor achieves it.

### Knaeps et al. 2020 — plastics library
*Hyperspectral UV to SWIR characteristics of marine-harvested, washed-ashore and virgin plastics.* ESSD 12:77. **Task:** spectral library (ASD FieldSpec, 350–2,500 nm; 11 virgin polymers + marine-harvested micro/macroplastics; on EcoSIS). Key facts: 8 diagnostic absorptions (931, 1045, 1215, 1417, 1537, 1732, 2046, 2313 nm); only 1215 and 1732 sit in atmospheric windows; wetting attenuates 12–90% (mean ~56%) but preserves shape. Role: slides 10, 20 — evidence that plastic chemistry lives mostly beyond VNIR; honest about it: within VNIR, plastics separate by colour/brightness/NIR shoulder, which is why plastic is a "target with spectral analysis" but the expected VNIR delta is uncertain.

### EMIT 2025
*Global-scale detection of plastic from space with the EMIT imaging spectrometer.* Geophysical Research Letters, DOI 10.1029/2024GL112416 (JPL). **Task:** matched-filter detection. 285 bands, 60 m, ISS; targets HDPE (GDS385) and PVC (GDS338) from splib07a; SWIR features 1200/1710/2300 nm; hotspots Spain, Sicily, Mexico, Taiwan. Role: slide 10 — excluded (60 m) but proves lab signatures transfer to orbit. Caveat: sub-pixel detections; PET/PS/PP under-represented.

### Zhou et al. 2021
*A knowledge-based, validated classifier for aliphatic and aromatic plastics with WorldView-3.* Remote Sensing of Environment. **Task:** knowledge-based decision-tree classification (no training data) on WV-3's 8 SWIR bands; aliphatic vs aromatic producer accuracy >80%; validated lab → airborne → satellite (Almería, Cairo, Accra); HySimCaR simulation for minimum detectable fractions. Role: slides 10, 27 — the polymer-type-needs-SWIR datapoint (supports the honest statement of what VNIR cannot do).

### Guo & Li 2020 (closed access)
*Normalized Difference Plastic Index using WorldView-3.* ISPRS JPRS. **Task:** spectral-index mapping. NDPI on WV-3 SWIR bands (~1.57/1.73 µm C–H absorptions); canonical plastic index, cited by all later WV-3 plastic work. Role: slide 10 (excluded, SWIR-based). Status: PDF not retrieved (VPN needed); details from secondary sources.

### Aguilar et al. 2021 — the ablation blueprint
*Evaluation of object-based greenhouse mapping using WorldView-3 VNIR and SWIR data.* Remote Sensing 13(11):2133 (Almería).

- **Task:** OBIA classification (segmentation + decision tree), plastic-covered greenhouses.
- **Numbers (memorize):** OA 90.85 (VNIR-only, 20 features) / 96.79 (SWIR-only, 19) / 97.38 (all 39 features); NDPI is the top feature; knowledge-based NDPI_B pushes OA to 98.08.
- **Role:** slide 10 (excluded, SWIR) — but methodologically it is the canonical "band-group ablation with everything else fixed" that the proposal replicates within VNIR. Caveats: plastic film, not waste; the "+14% kappa" formulation was dropped as an internal claim — quote OA only.

### Aguilar et al. 2025
*Mapping terrestrial macroplastics and polymer-coated materials in an urban watershed using WorldView-3 and laboratory reflectance spectroscopy.* Environmental Monitoring and Assessment 197(7). **Task:** matched-filter detection on WV-3 SWIR (8 bands, 3.7 m), Tijuana watershed; lab-to-satellite endmember correlation r=0.95; precision 92.5% (95.3% on high-certainty polygons); waste aggregations 80–150 m². Role: slide 10 — lab signatures visible from 600 km; also the source of the "3.7 m SWIR under-detects sparse waste" caveat that supports our SWIR exclusion.

### SpectralWaste 2024
arXiv:2403.18033 (Zaragoza + ATRIA). **Task:** multimodal segmentation dataset (sorting plant conveyor: RGB + Specim FX17 HSI, 224 bands 900–1,700 nm; 6 classes, 852 annotated images). Fusion CMX mIoU 58.2 vs RGB 48.4 vs HSI 54.3; HSI alone wins big on thin shapeless classes (video tape +18.4, filament +36.9 mIoU). Role: slide 10 — industrial, not EO; kept as "spectra help precisely where shape fails" evidence.

### Plastic UAV-SWIR segmentation 2026 (pending)
Remote Sensing 18(1):182. **Task:** semantic segmentation (attention-gated residual U-Net) on UAV hyperspectral SWIR 900–1,700 nm; 96.8 accuracy / 91.1 F1; 1215/1732 nm drive it. Role: slide 14 table. Caveat: starred on the slide (pending full-text verification).

### Plastic UAV-IoT 2025 (pending)
J. Hazardous Materials Advances. **Task:** object detection on UAV RGB with edge deployment; river plastic, 92% accuracy (Bogor, Indonesia). Role: slide 14 table — plastic *presence* by appearance, polymer type not addressed.

## 3.3 Objects, platforms, excluded backbones (reference slide 28)

### Ramachandran et al. 2024
*Deep learning to map well pads and storage tanks.* Nature Communications. **Task:** object detection, VHR satellite; tanks P 0.962 / R 0.968; >169k tanks and >70k well pads mapped across US basins. Role: slide 14 — tanks are solved object detection; that is why the tanks class needs no spectral analysis (slide 7).

### YOLOv7-OT 2024 (pending)
Remote Sensing 16(23):4510. **Task:** object detection (YOLOv7 + CBAM); tanks, precision 95.9, edge re-stitching for large scenes.

### Truck-and-container detection 2025 (preprint/pending)
PMC. **Task:** object detection (CenterNet + Mask R-CNN ensemble); classifies container size and status from satellite.

### Vehicle detection with domain adaptation 2020 (pending)
Remote Sensing 12(3):575 (Koga et al.). **Task:** object detection on ~30–50 cm VHR; CORAL + adversarial domain adaptation, +10% in unlabelled target domain. Also a useful cross-region-generalisation technique reference.

### ELV Hybrid-YOLOv5 2025
Scientific Reports. **Task:** object detection, close-range infrared (not remote sensing); non-ferrous metals in end-of-life vehicles, mAP 84.2. Role: slide 9/14 — documents that scrap *composition* needs close range or spectra; the object-vs-material boundary in one paper.

### UAV solid-waste segmentation 2024 (pending)
Applied Sciences. **Task:** semantic segmentation, dual-branch, ~450 km² UAV imagery; OA >94, recall 88.6; one generic "waste pile" class, no materials.

### C&D debris volume from UAV photogrammetry 2022 (pending)
Drones 6:279. **Task:** segmentation (FCN) + SfM 3D volume estimation; concrete debris IoU 0.90. The volume capability is something 2D satellite lacks.

### AI-powered drones in waste management, 2025
Drones 9:550. **Task:** PRISMA systematic review (~10 UAV+DL studies); YOLO family dominates (YOLOv8 ~97 acc / 94.7 mAP@50 on dumps). Role: slide 14 takeaway footnote ("UAV line surveyed in Drones 2025").

### fCLIPSeg 2025
arXiv:2504.12542. **Task:** semantic segmentation; CLIPSeg fine-tuned for post-hurricane debris on aerial RGB; Dice 0.70, event-agnostic across three hurricanes. A vision-FM adaptation recipe for data-thin shape classes (not an EO foundation model).

### The excluded EO foundation-model line (slide 10, slide 28)
One shared exclusion reason: pretrained at 10–30 m (occasionally 1 m RGB), no evidence of sub-metre transfer for material tasks; adopting one would add an unjustified variable to a controlled RGB-vs-VNIR comparison. Per-model one-liners:

- **DOFA 2024** (Xiong et al., arXiv:2403.15356): wavelength-conditioned hypernetwork generates the patch embedding for any band set; pretrained on 5 modalities (~8M samples, S1/S2/Gaofen/NAIP/EnMAP). The most relevant if a sensor-agnostic backbone were ever needed; still 1–30 m pretraining, sub-metre unproven.
- **AnySat 2025** (arXiv:2412.14123): JEPA, scale-adaptive patch encoder; 11 sensors, 0.2–250 m, GeoPlex pretraining; new sensors = fine-tune only (no probing).
- **Prithvi-EO-2.0 2024** (Szwarcman et al., arXiv:2412.02732): NASA/IBM, ViT 300M/600M, 3D MAE on 4.2M HLS samples, 6 fixed bands @30 m; +8% on GEO-Bench vs v1. Fixed band set, 30 m — weakest fit.
- **SpectralGPT 2024** (TPAMI): 3D spectral masking (90%) on Sentinel-2 12-band, up to 600M params; spectral coupling modelling, but S2-locked.
- **SatMAE 2022** (Cong et al., NeurIPS): band grouping + spectral positional encoding, fMoW-Sentinel; the historical predecessor (EuroSAT 98.98 in 2022); +14% transfer vs ImageNet-RGB init is the classic "MS pretraining helps" number.
- **SSL4EO-S12 2023** (Wang et al.): 3M S1/S2 patches, 251k locations; MoCo/DINO/MAE checkpoints on all 13 S2 bands; ~+10% over ImageNet in linear probing.
- **SoftCon 2024** (Wang et al.): soft contrastive learning with Dynamic World multi-labels on 780k SSL4EO images; ViT-B SOTA on 10/11 EO tasks; also the evidence that "random-init first layer + strong backbone" adapts channels well.
- **Corley et al. 2024**: not a FM — a methodology paper: resize-to-pretraining-size + per-channel normalization moves benchmarks more than the pretraining choice (+11.16 EuroSAT, +32.28 So2Sat MSI); ImageNet stays competitive when preprocessing is fair. Direct implication for our ablation: identical preprocessing across RGB and VNIR arms, stated explicitly.
- **FM-RS survey 2024** (IEEE GRSM 2025): taxonomy of 18+ EO FMs and 11 pretraining corpora (GSD 0.1–153 m); the citation that documents the 10–30 m pretraining regime.
- **DEFLECT 2025** (Thoreau et al., ICCV): <1% extra parameters to adapt a geospatial ViT to new channels (untangled patch embedding + attention). Cited as the parameter-efficient alternative in the excluded line.

If pressed "why not DOFA, it handles any bands?": right mechanism, unproven at our GSD; independent benchmarking (GeoCrossBench) even found simple channel-adapted ViTs beating it cross-sensor; and the thesis question is a controlled sensor comparison, not a backbone contest. The Swin-T+RSP baseline keeps continuity with Gibellini and isolates the input variable.

\newpage

# 4. Q&A drill

Twenty questions, current scope (VNIR only, no SWIR arm, no Sentinel-2, no FM backbones). Answers are written the way they should be *said*: short, factual, no hedging beyond the honest caveat.

**Q1 — What is the task, exactly?**
Multi-label classification at image level: given a VHR satellite image of a suspected dump site, output the set of waste materials present. Not detection (sites are assumed suspected/detected — that problem is mature on RGB, Gibellini F1 92.0), not object detection or segmentation (annotations are image-level; waste piles have no stable shape; no masks exist at training scale). The contribution is measuring the added value of VNIR over RGB for the material labels, per material.

**Q2 — If RGB already detects waste at F1 92, why multispectral?**
Detection ≠ risk. ARPA prioritises by hazard, and hazard depends on the material. RGB wins on morphology and context; several materials share the same colour at 30–130 cm (plastic sheets, asbestos-cement, concrete: all grey) and their separation lies beyond 700 nm. The predecessor's per-class results show exactly this: shape-distinctive classes hold (rubble 72, bulky 71), colour-ambiguous ones fail (plastic 44, wood 37, tires 19).

**Q3 — Why not Sentinel-2? It's free and has SWIR.**
Resolution, not bands. S-2 is 10–20 m; a dump is metres. At that GSD a whole site is a handful of mixed pixels — the marine and river lines (MARIDA, Tisza) work only on large dense accumulations. Be precise: S-2's limit is GSD; the SWIR bands themselves are fine.

**Q4 — Why exclude SWIR if the chemistry lives there?**
Two practical reasons: it is not in the planned acquisitions, and WV-3 SWIR is 3.7 m GSD against a sub-metre task (a SWIR pixel is ~14 m² — no pure pixels over a dump). The chemistry argument is real (plastics C–H 1215/1732 nm, asbestos Mg–OH ~2.31 µm — Knaeps, Zhou, Guo & Li) and is cited as evidence, but as an experimental axis SWIR mixes band effect with a 3× resolution penalty, which would contaminate the ablation. The question the thesis can answer cleanly is RGB → +NIR → full VNIR at constant GSD.

**Q5 — What can VNIR realistically add without SWIR?**
Red Edge and NIR separate vegetation, bare soil and weathered surfaces (Saba 2026: they drive asbestos discrimination at 1.24 m); Vitek 2025 shows on 10 C&D materials that RGB+2 bands within 650–1000 nm goes from 0.87 to 0.96 accuracy, matching the full spectrum — all within a VNIR budget. Whether this transfers from lab/roofs to waste at task GSD is exactly the open question.

**Q6 — Isn't Vitek a lab study?**
Yes, and the slide says so. Controlled illumination, clean samples. It proves the information content is in those wavelengths; it does not prove a satellite recovers it through atmosphere and mixed pixels. That is the gap between evidence and claim, and the thesis measures the difference.

**Q7 — Mixed pixels: at ~1.2 m nothing is pure. Doesn't that kill the material claim?**
It sets the ceiling, not the feasibility. Library numbers are pure-endmember upper bounds; satellite results are mixed-pixel lower bounds. Aguilar 2025 still reaches precision >92% on 80–150 m² plastic aggregations at 3.7 m; Saba works at 1.24 m per-pixel. Our images are 0.3–1.3 m, the most favourable mixing regime in this literature.

**Q8 — How do you prove a VNIR gain is spectral and not just extra channels/texture?**
The ablation keeps everything fixed (architecture, splits, preprocessing, training recipe) and changes only the input bands; deltas come with confidence intervals over repeated runs. Per-material deltas are the primary output: a spectral explanation predicts gains concentrated on colour-ambiguous classes, not uniformly. If needed, a per-pixel (context-free) classifier on the pilot separates spectral from spatial contributions.

**Q9 — What about generalisation?**
Rarely evaluated in this literature; at site level it costs 5.1 F1 (Gibellini: Greece 85.4, Sweden 83.8, Romania 91.5 — note: Sweden, the slide's "Serbia" is a typo). Plan: hold out disjoint geographic areas, report in-domain and out-of-domain side by side. Terminology: "generalizzazione", not "OOD".

**Q10 — Is the contribution novel or a re-run?**
The combination is unmeasured: no published work quantifies RGB-vs-VNIR added value for waste materials at VHR, per material. Individual pieces (multi-label waste classification: Alari; band ablations: Aguilar 2021 on plastic film; VNIR asbestos: Saba) exist; the controlled measurement at this operating point does not — the survey and Alari's own future-work chapter say so.

**Q11 — Why Swin-T + RSP and not a foundation model?**
Continuity and control. The group baseline is validated on this exact imagery (F1 92 site-level; reproduced at 0.95 on v3); FMs are pretrained at 10–30 m with unproven sub-metre transfer, and swapping backbone would confound the input comparison. DOFA's wavelength-conditioned embedding is the right mechanism if a sensor-agnostic backbone becomes necessary — noted as context, not used.

**Q12 — Why is asbestos the pilot and not, say, plastic?**
Only material with public, pixel-accurate, regional ground truth (Mappatura 2020: 10,903 roofs); demonstrated VNIR discriminability at fine GSD (Saba, plus Bonifazi's workflow and Cilia's history); direct regulatory value. Plastic has no comparable GT and its strongest spectral evidence sits in SWIR.

**Q13 — The pilot is on roofs; the thesis is about dumps. Isn't that a domain mismatch?**
Yes, deliberately. The pilot isolates the *sensor* question (does VNIR beat RGB on a well-labelled material?) from the *label* problem (waste GT is weak). Roofs give clean labels; the measured delta is a controlled, per-material data point that gates the acquisition investment. Saba's 97.6 per-pixel is the upper reference, not a comparable target.

**Q14 — What exactly is the decision gate?**
If matched RGB vs VNIR on the same roofs shows a material delta (F1/precision/recall on held-out areas), the multi-label extension justifies the acquisition cost; if the delta is ~0, that is a documented negative result that redirects the thesis (and still informs sensor choice for the consortium).

**Q15 — Where does the imagery come from, and is it feasible?**
WorldView-3 (8 VNIR bands, pan 0.31 m) and Pléiades Neo (6 VNIR, pan 0.30 m), advisor-provided over the Lombardia AOI; access either commercial or via ESA Third Party Missions free quota (proposal cycle ~9 weeks + 1-year quota). The RGB baseline needs nothing new (AerialWaste). Known constraint: AerialWaste coordinates are withheld, so pairing MS imagery with existing labels needs the ARPA/group agreement — the advisor-provided acquisitions are the plan.

**Q16 — Alari got wF1 59 on ten classes. Why do you expect to do better?**
The target is not "beat 59" as such; it is the per-material delta from adding bands. Alari's failure modes (precision collapse on tires/plastic/wood — over-prediction of colour-ambiguous classes) are precisely where spectral input plausibly helps. Any improvement claim will be per-class with the RGB re-baseline run under our identical setup — not against Alari's numbers directly, since data and splits differ.

**Q17 — Whose numbers on your slides are not peer-reviewed?**
Flagged on-slide: Disaitek (~95%, vendor); AW ensemble 92.4 (preprint); the starred rows of the objects table and Saba/Abbasi (paywalled or pending full-text verification). Everything else is from journals or verified full texts.

**Q18 — What are the 13 categories, and which does the spectral analysis target?**
Rubble/excavated earth, foundry waste, vehicles, scrap, bulky items, containers, sludge, wood, plastic, big bags, tanks, tires, asbestos. All remain classification targets (continuity with the group dataset). The spectral analysis concentrates on rubble, plastic, wood, tires (frequent, colour-ambiguous) plus asbestos (pilot). Shape-based classes (vehicles, tanks, containers, scrap, bulky, big bags) have mature RGB object-detection literature; sludge and foundry waste have too few labels.

**Q19 — Strongest single number for "RGB is not enough for material"?**
Two, one per direction: Alari's 5→10 category drop (−9.8 wF1, five classes under F1 50, precision-driven) shows RGB saturating on fine distinctions; Vitek's 0.87→0.96 with two extra VNIR bands (lab) shows where the missing information sits. Saba's 97.6 VNIR-only per-pixel asbestos is the satellite-side confirmation.

**Q20 — Biggest risk of a null result, and what then?**
That at 30–50 cm with pansharpened VNIR the per-material deltas are small or noisy (labels thin for exactly the interesting classes). Mitigations: pilot first on clean GT; confidence intervals over repeated runs; per-material reporting so partial positives survive. A measured "VNIR does not help materials X, Y at this GSD" is publishable and operationally useful — it prices the spectral option for the agencies.

\newpage

# 5. Numbers to memorize

| Fact | Number | Source |
|---|---|---|
| Gibellini in-domain | F1 92.02, Acc 94.56 | WMB 2025 |
| Gibellini generalisation | −5.10 F1 avg; GR 85.45 / **SE** 83.82 / RO 91.48 | Table 3 |
| Gibellini utility (thr 0.7) | +63.2% sites, −60.2% area, −30% time | Table 4 |
| Our reproduction | val F1 0.9519 (epoch 13 FT) | repo ckpt |
| AerialWaste size | 10,434 imgs (3,478 pos), v3 ~11.7k; 22 tags; masks 169 imgs | Sci Data 2023 |
| AerialWaste baseline | F1 80.70 / AP 87.99 | ResNet50+FPN |
| AerialWaste sources | AGEA 20 cm / WV-3 30 cm / GE 50 cm | ibid. |
| Alari dataset | 11,477 annotations, 13 cat., 3,190 pos / 7,190 neg | thesis |
| Alari headline | wF1 69.21 (5 cat, R152+FPN) / 59.42 (10 cat, R50+IDA) | Tab. 4.11–4.13 |
| Alari 5→10 cost | −9.8 wF1; 5 of 10 classes < F1 50 | ibid. |
| Alari best/worst class | rubble 72.49 / tires 18.57 | Tab. 4.13 |
| Survey scope | 50 works 1987–2023; 11/50 DL; almost all RGB | Fraternali 2024 |
| Sun 2023 | ~2,500 dumpsites dataset; 28 cities test; −96.8% time; precision ~70% | Nat Comms |
| CascadeDumpNet | mAP 84.6, Pléiades 0.5 m | RSE 2024 |
| CWLD | F1 88.9 / IoU 82, C&D segmentation | Sci Data 2024 |
| Disaitek | ~95% on ≥2 m² (vendor), PNeo 30 cm | Airbus 2024 |
| AW ensemble | binary F1 92.41 (preprint) | arXiv 2025 |
| Saba 2026 | Macro-F1 97.6 per-pixel, WV-3 VNIR 1.24 m; Red Edge+NIR | JHM (paywalled) |
| Bonifazi 2026 | building-level F1 0.87 @30% thr; 16 bands; Mantova | Geomatics |
| Abbasi 2024 | OA ~96, aerial RGB + temporal, no SWIR | RSASE |
| Cilia 2015 | PA 89 / UA 86; MIVIS 102 bands @3 m; ISD index | ISPRS IJGI |
| Shepherd 2025 | ACE OA 91.4; 86% field match; EnMAP 230 bands @30 m | Sci Rep |
| Vitek 2025 | RGB 0.87 → RGB+2 bands 0.96 (≈ full 768) | RCR (lab) |
| Knaeps plastics | C–H at 1215 / 1732 nm (atmospheric windows) | ESSD 2020 |
| Aguilar 2021 | OA 90.85 VNIR / 96.79 SWIR / 97.38 all | RS 13:2133 |
| Aguilar 2025 | precision 92.5%; lab-satellite r 0.95; 3.7 m SWIR | EMA |
| Zhou 2021 | aliphatic vs aromatic PA >80%, WV-3 SWIR | RSE |
| EMIT 2025 | HDPE/PVC global, 285 bands @60 m | GRL |
| SpectralWaste | fusion mIoU 58.2 vs RGB 48.4 vs HSI 54.3 | arXiv 2024 |
| Ramachandran tanks | P 0.962 / R 0.968; >169k tanks | Nat Comms 2024 |
| ELV scrap | mAP 84.2, close-range IR | Sci Rep 2025 |
| WFS ground truth | Mappatura 2020: 10,903 roofs, EPSG:32632 | Regione Lombardia |
| Library | 47 papers, structured notes, papers/INDEX.md | repo |

# 6. Sensors and bands

| Sensor | VNIR bands | MS GSD | Pan | SWIR | Role |
|---|---|---|---|---|---|
| WorldView-3 | 8 | 1.24 m | 0.31 m | 8 @ 3.7 m (excluded) | main MS arm |
| Pléiades Neo | 6 | 1.2 m | 0.30 m | none | second MS arm / cross-sensor |
| Planet SuperDove | 8 | 3 m | — | none | asbestos signature track |
| Sentinel-2 | 10 (+3 @60 m) | 10–20 m | — | 2 @ 20 m | excluded (GSD) |
| EnMAP / EMIT | hyperspectral | 30 / 60 m | — | yes | excluded (GSD); evidence only |
| AGEA / GE aerial | RGB | 20 / 50 cm | — | none | RGB baseline (AerialWaste) |

Approximate band centres (µm) — from Maxar / Airbus data sheets:

- **WV-3 VNIR (8):** Coastal 0.425 · Blue 0.480 · Green 0.545 · Yellow 0.605 · Red 0.660 · Red Edge 0.725 · NIR1 0.833 · NIR2 0.950. Yellow and NIR2 have no Pléiades Neo counterpart.
- **Pléiades Neo (6):** Deep Blue 0.425 · Blue 0.485 · Green 0.560 · Red 0.655 · Red Edge 0.725 · NIR 0.840.
- **SuperDove (8):** Coastal 0.443 · Blue 0.490 · Green I 0.531 · Green 0.565 · Yellow 0.610 · Red 0.665 · Red Edge 0.705 · NIR 0.865.
- Ablation axis: **RGB → +NIR → full VNIR** (3 → 4 → 6/8 bands), same GSD, same everything else.

Diagnostic wavelengths that fall *outside* the VNIR budget (know them to state honestly what is given up): plastics C–H 1.215/1.732 µm; asbestos chrysotile Mg–OH ~2.31 µm; carbonate ~2.34 µm; clay Al–OH ~2.2 µm. What remains inside VNIR: colour, brightness, Red Edge / NIR shape (vegetation stress, weathering, Fe-oxides ~0.87–0.95 µm), the 650–1000 nm region Vitek found sufficient for C&D materials.

# 7. Terminology and delivery

Thomas's table — apply in slides, text, discussion:

| Don't say | Say |
|---|---|
| "OOD" / "out-of-distribution" | "generalizzazione" / "contesto geografico" |
| "rilevare rifiuti", "+63% scoperta" | "individuare siti e classificarli per rischio" |
| Gibellini as central reference / target | Gibellini as starting point only |
| "SuperDove is the sweet spot" | "balancing access, resolution, spectral coverage" |
| "spectral cube" | "multiband" / "multispectral images" |

Define on first use: EO, MS, MSI, HSI, FM, SAM. GSD needs no definition and stays untranslated. "Material-level labels still missing" is the fundamental gap and comes first when discussing gaps.

Delivery (dry-run 2026-05-27): Italian speech, English technical terms; ~15–20 min, don't drift to 25–30; fluid transitions, no jumping back; physics at high level; for *every* cited work be ready to state its task type (the cards in §3 lead with it); sensor discussion = trade-off spatial resolution / number of bands / revisit, none jointly maximizable.

# 8. Errata and traps

1. **Slide 13 says "Serbia 83.8" — it is Sweden.** Gibellini's generalization sets are Greece / Sweden / Romania (Table 3). Same typo exists in deck_v7. Fix in `build_deck.py` or correct verbally.
2. **Alari's 69.21 is ResNet152+FPN**, not ResNet50 (ResNet50+FPN = 68.84); and 59.42 (ResNet50+IDA) was preferred over 60.18 (ResNet152+IDA) on non-aggregate diagnostics. Useful, not embarrassing — it supports gap #3.
3. **Sun 2023 precision is ~70%** despite ~98% sensitivity; don't present it as a solved problem, present it as "detection mature, qualification weak".
4. **Survey double-entry:** the arXiv and Waste Management versions of the Fraternali survey are the same work; the 47-paper count includes both entries.
5. **Do not quote** (internally downgraded): Aguilar "+14% kappa"; Saba "HSI 97.3 vs MS 74.4" (paywalled, unverified); Bonifazi/Cilia secondary figures beyond those in §3; "chrysotile feature ~5 nm wide" (wrong — tens of nm).
6. **Vendor/preprint flags** must be spoken when quoting Disaitek, AW ensemble, and every starred row of slide 14.
7. **SWIR/S-2 trap:** Sentinel-2 has SWIR; its problem is 10–20 m GSD. WV-3 has SWIR but at 3.7 m. Keep band vs resolution vs both distinct in every answer.
8. **Superseded scope pivots** (S-2→SuperDove 2026-04-24; VHR-13-class 06-23; "SWIR back in" 06-27) may surface in old documents — the 2026-07-03 constraints win: VNIR only, Swin-T+RSP baseline, WV-3 + Pléiades Neo, 13 material classes, asbestos pilot on SuperDove.
