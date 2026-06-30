---
title: "PERIVALLON — Master Study Guide"
subtitle: "Multispectral VHR satellite detection and risk-classification of illegal waste"
author: "Politecnico di Milano · PERIVALLON thesis · Alessandro Potenza"
date: "2026-06-28"
---

# 0. How to use this guide

This is the single document to study. It has two parts:

- **Part I — Concepts** (this part): the argument, the sensors, the science, the experiment, the numbers, and a professor-defence Q&A. Study this to *understand and be able to explain* the thesis.
- **Part II — Papers**: a study card per paper (47), grouped by theme, with the one number and the one limitation to remember each. Study this to *cite the literature efficiently*.

**Suggested study order (≈3 h):** §1–§2 (big picture, 20 min) → §3–§4 (sensors + the material↔band table, 35 min) → §5 (datasets, 25 min) → §6 (the science, 35 min) → §7–§8 (experiment + risk chain, 30 min) → §9–§10 (numbers + Q&A, 25 min) → Part II papers (browse cards by tier, 30 min+).

**Terminology discipline (advisor's preference):** say *generalizzazione* (not "OOD"); *classificare per rischio* (not just *rilevare*); *multiband* (not "spectral cube"); never translate **GSD**. Define EO / MS / HSI / VNIR / SWIR on first use.

**The thesis in one sentence.** *Detection of illegal-waste sites from very-high-resolution satellite imagery is already solved on RGB; the open, operationally useful problem is to classify those sites by risk — which requires identifying the material — and the thesis measures, honestly and with controlled ablation, how much multiband (VNIR, and where available SWIR) imagery adds over RGB for that material discrimination at VHR.*

---

# 1. The research question and why it matters

**Central research question.** *What is the added value of multiband over RGB for discriminating the materials that determine the hazard of an illegal-waste site, at VHR — and where does it stop helping?*

Three things make this the right question:

1. **Detection is solved, characterisation is not.** RGB models localise dumpsites from shape and context at ~92% F1 (Gibellini 2025). They cannot tell hazardous from inert material. The operational bottleneck for ARPA is not finding sites but *ranking* them.
2. **Risk is defined by material.** Following the environmental-epidemiology formulation, `risk = hazard × exposure × magnitude` (Fazzo et al. 2020). The *hazard* term is the material (asbestos vs inert rubble), legally codified by the European Waste Catalogue (asbestos = code 17 06 05*). Two of the three risk factors are material-dependent — exactly what RGB cannot see.
3. **The value is real but bounded.** Material identity lives in spectral absorptions outside the visible (NIR/SWIR). But at VHR the spectrum is coarsely sampled and pixels are mixed, so the gain must be *measured*, not assumed — and it differs by material.

**Operational context.** The thesis sits in PERIVALLON (Horizon Europe, Grant 101073952), with ARPA Lombardia as the end user. The deliverable that matters is a *ranked intervention list*, i.e. decision support, not a detector.

---

# 2. The problem framed as risk classification

`risk = hazard(material) × exposure(receptors) × magnitude(area)`

- **Hazard** — the material. Legally codified (European List of Waste / EWC; asterisk = hazardous; asbestos 17 06 05*). This is the term MS imagery can supply and RGB cannot.
- **Exposure** — proximity to people, water, agriculture. Computable from GIS layers (out of the imagery, but cheap to add).
- **Magnitude** — site area / quantity. Computable from the detected footprint.

**Italian operational anchor.** ARPA does not act on detection alone: the *Piano Regionale Amianto* (PRAL) and the *Indice di Degrado* (d.d.g. 13237/2008, thresholds 25 / 44 / 45) already turn material condition into intervention priority. The thesis's risk-tiering therefore mirrors how the agency actually works — a strong "operational relevance" argument. **Fazzo et al. 2020** (the Campania "Land of Fires" GIS risk index) is the citable methodological template.

**The contribution junction.** Prior art either *detects* sites (RGB, material-blind) or *ranks known sites* by GIS exposure with the hazard supplied from ground records. No published pipeline derives the hazard term *from multispectral imagery* and feeds it to a risk tier. That junction is the novelty.

---

# 3. Sensors and the band ladder

The whole thesis turns on which diagnostic absorption falls into which band.

| Sensor | VNIR | SWIR | Pan | Role |
|---|---|---|---|---|
| **WorldView-3** | 8 bands @ 1.24 m | **8 bands @ 3.7 m** | 0.31 m | full ladder incl. R3 chemistry |
| **Pléiades Neo** | 6 bands @ 1.2 m | none | 0.30 m | cross-sensor axis; VNIR-only |
| SuperDove | 8 bands @ 3 m | none | — | free, near-daily; R2 full-VNIR |
| Sentinel-2 | 10–20 m | 20 m | — | too coarse for material |
| EnMAP / PRISMA | hyperspectral ~6.5 nm | yes | — | resolves the 2.3 µm triplet but at 30 m |

**WV-3 VNIR centres (µm):** Coastal 0.425 · Blue 0.48 · Green 0.545 · *Yellow 0.605* · Red 0.66 · *RedEdge 0.725* · NIR1 0.833 · *NIR2 0.95* (Yellow + NIR2 unique vs Pléiades Neo).
**WV-3 SWIR centres (µm):** 1.21 · 1.57 · 1.66 · **1.73** · 2.16 · 2.20 · 2.26 · **2.33**.
**Pléiades Neo VNIR (µm):** DeepBlue 0.425 · Blue 0.483 · Green 0.562 · Red 0.655 · RedEdge 0.725 · NIR 0.84 (no SWIR).

**The band ladder (the independent variable of the experiment):**

> **R0 RGB → R1 +RedEdge/NIR → R2 full VNIR (8-band) → R3 +SWIR (WV-3 only).**

R3 is the only rung that adds diagnostic chemistry. The Pléiades-Neo asymmetry (it stops at R2) is itself a finding, not a defect.

**Data access (no Thomas needed to know this).** Both WV-3 and Pléiades Neo are free to a PoliMi/ESA researcher via **ESA Third Party Missions** (project proposal, ~9-week evaluation, 1-year quota). The real risk is **WV-3 SWIR archive availability** over the chosen AOI (SWIR is tasked separately and may be sparse) — not resolution: the old 7.5 m export cap was relaxed, native SWIR is 3.7 m.

---

# 4. Material → feature → band (the centerpiece table)

**The governing rule:** a class is feasible at broadband VNIR if its identity lives in **shape/context**; it is weak if its identity lives in **spectral chemistry**.

| Class | Identity carrier | Diagnostic feature (µm) | WV-3 band | On Pléiades Neo | Verdict at VHR |
|---|---|---|---|---|---|
| **Asbestos-cement** | shape + chemistry | chrysotile Mg-OH 2.30–2.33 | SWIR8 (2.33) | shape + VNIR weathering proxy | corrugated shape detectable; material confirm needs SWIR |
| **Plastics (polymer)** | presence=texture; type=chemistry | C-H 1.215 / 1.730 | S1, S4, S8 | presence only | presence at VHR; polymer ID needs SWIR |
| **C&D / inert rubble** | shape + chemistry | carbonate 2.34; clay 2.20 | S8, S6 | heap morphology | strong by shape; composition needs SWIR |
| **Foundry slag** | chemistry (data-thin) | Fe-oxide 0.87–0.95 | NIR1/NIR2; SWIR | weak Fe cue | GAP |
| **Scrap metal** | scene=shape; type=chemistry | flat/specular (no feature) | none | scrapyard scene | scene-detectable; type = GAP even with SWIR |
| **Tyres (rubber)** | shape / dark target | carbon-black, low R | broadband low | dark piles | piles OK; confuses with shadow/water |
| **Wood / organic** | shape (stacks) | cellulose ~2.1/2.3 | NIR1/SWIR | stacked piles | good by shape |
| **Sludge** | context (lagoon) | water+organic (no sharp feature) | broadband+NIR | lagoon context | GAP (composition) |
| **Big-bags / FIBC** | shape but small | woven PP C-H 1.73 (sub-pixel) | S4 (diluted) | shape, tiny | near-GAP |
| **Vehicles / ELV** | shape | — | — | shape | excellent (object) |
| **Tanks / cisterns** | shape (circular) | — | — | shape | excellent — not a gap |
| **Containers / skips** | shape | — | — | shape | strong (object) |
| **Bulky items** | shape | — | — | shape | good (object) |

**Read this in one breath:** 8/13 classes are shape-identifiable at 30–50 cm; **5 are chemistry-bound** (asbestos, plastic-type, foundry slag, sludge, scrap composition) — exactly where RGB fails and the MS/risk argument must live. **Asbestos and plastics are the ideal test beds** because a shape cue and a chemistry cue coexist.

**The SWIR-8 bottleneck (say this before the prof does).** Chrysotile (~2.32), carbonate (~2.34) and plastics C-H (~2.31) all crowd into the *single* WV-3 SWIR8 (~2.33 µm, ~40 nm wide) band. WV-3 cannot *resolve* the triplet within it — it can only flag "something absorbs near 2.33". Discrimination then leans on the shoulders (2.16/2.20/2.26; 1.21/1.73) plus VNIR shape. A hyperspectral sensor (~6.5 nm) would resolve it; WV-3 won't, and that limit must be stated.

---

# 5. Datasets you can actually use

**The structural gap (the thesis opportunity):** *no public dataset combines VHR satellite imagery + terrestrial waste + material-level labels.* Every resource sits on one side of the hole.

**The bridge:** take geolocated waste/asbestos locations and re-image them with WV-3 / Pléiades Neo — this creates the missing multiband material dataset.

Datasets by **role**:

- **Label sources (the actual training data).**
  - *Lombardy asbestos WFS* (`Mappatura_2020`, 10,903 roofs; `Mappature_precedenti`, 50,131; EPSG:32632) — **public + geolocated → immediately usable** for the asbestos pilot.
  - *AerialWaste v3* (3,478 waste positives in Lombardy, 22 material categories) — **coordinates withheld (ARPA)** → re-imaging needs an in-group agreement.
  - *DroneWaste* (PERIVALLON UAV, 20 material types, RGB) — material taxonomy; not satellite.
  - *CWLD* (Beijing C&D, GF-2/GE pixel masks) — transfer for the rubble class.
- **Public benchmarks (method dev / band ablation).** EuroSAT MS (the controlled band-ablation testbed, already local); Toulouse Hyperspectral (32 urban materials, VNIR+SWIR, public); GRSS Houston / Pavia (urban-material HSI); SpectralWaste / RECONMATIC / Tecnalia (material-evidence proof); MARIDA/MADOS (material-at-satellite, but marine).
- **Spectral references (justify bands, build endmembers).** USGS splib07a (WV-3 convolutions, in `spectral/`); WaRM (corrugated asbestos-cement); KLUM; MADLib; EnMAP asbestos field library.
- **Pretraining / FM weights.** DOFA (ingests WV-3/PNeo bands natively); SSL4EO-S12 (S2 weights); Prithvi-EO-2.0 (has SWIR); SpectralEarth.

**Verified Lombardy auxiliary layers** (all EPSG:32632, ArcGIS REST, CC-BY 4.0 — co-registerable with the imagery, no reprojection): asbestos WFS (hard positives; **layer 1** = Mappatura 2020, **layer 4** = temporal status codes 1/2/3/4); DUSAF 7.0 land-use (classes 131 Cave / 132 Discariche / 133 Cantieri / 134 Aree degradate — filter on the `DESCR` string, the numeric code is not queryable); PSC-AGISCO contaminated-site points (status + activity type incl. "abbandono rifiuti", "discariche abusive"). **The Indice di Degrado is NOT in the WFS** — it must be estimated remotely (see §6).

---

# 6. The science you must be able to defend

## 6.1 Object vs material (the honest caveat)
At VHR, **detection** is largely solved by shape/context (Gibellini F1 92.02%; AerialWaste ensemble 92.41%; Disaitek ~95% on objects ≥2 m²). So the MS value proposition is **not** detection — it is **material/risk classification**, which the VHR literature leaves empty.

## 6.2 Mixed pixels set the ceiling
Pixel footprints: WV-3 VNIR ≈ 1.5 m², SuperDove ≈ 9 m², WV-3 SWIR ≈ 14 m². Waste objects are decimetre-scale, so **essentially no pixel is pure** — each integrates waste + soil + shadow + vegetation. Lab/library numbers are *upper bounds*; on-satellite numbers are a realistic *mixed-pixel lower bound*. Unmixing is out of experimental scope but governs the ceiling, and the cited target detectors (Aguilar matched-filter, EMIT) are *already* sub-pixel.

## 6.3 Chemistry vs texture — the experiment that makes MS defensible
A CNN has a receptive field, so "MS-CNN beats RGB-CNN" could be *texture in extra channels*, not chemistry. Use a four-cell design:

| | RGB bands | MS bands |
|---|---|---|
| **Spatial-context-free** (per-pixel / per-object mean) | A | B |
| **Full CNN** (spatial receptive field) | C | D |

- **B − A = pure chemistry/spectral gain** (no spatial info to either) — the number that attributes MS value to *material*.
- **D − C = total MS gain in the deployed CNN** (chemistry + MS-texture).
- **B − A ≈ 0 but D − C > 0 ⇒ the gain is texture** — an honest negative result for the material claim.

Precedent that the context-free baseline works: Saba 2026 Fine-KNN on WV-3 VNIR pixel features reaches Macro-F1 97.6% for asbestos with no spatial kernel.

## 6.4 Generalization ("generalizzazione") — the advisor's central claim, quantified
| Mode | Magnitude |
|---|---|
| Cross-region (same sensor) | −5.1% F1 (Gibellini 92.0→86.9; GR 85.4 / SE 83.8 / RO 91.5) |
| Cross-sensor (band mismatch) | 2–4× error increase (no overlap); 5–25% drop (superset) — GeoCrossBench |
| Cross-time/season | task-specific double-digit |
| Atmospheric/illumination | removed by surface-reflectance correction |

**Does multiband narrow or widen the gap?** Genuinely mixed — which is why it is publishable. It **narrows** the gap for cross-region/cross-time on a *fixed* sensor (physical absorptions are more invariant than colour/texture) but **widens** it cross-sensor (the extra bands are exactly where band-centre/width/SNR/calibration mismatch lives; RGB is the lowest common denominator and ports trivially). *Defensible claim:* MS value is conditional on closing the radiometric/band gap; reported naïvely, MS can look worse OOD than RGB. The clean novel experiment is a **2-D table: ablation level (R0→R3) × generalization axis**, reporting the ID−OOD gap per cell. Cheapest highest-ROI fix first: **resize + per-channel normalization** (Corley 2024), then surface reflectance, then wavelength-conditioning (DOFA).

## 6.5 Remote estimation of asbestos degradation (fills the ID gap)
The Indice di Degrado `ID = (A+...+H) × I` is a site-inspection score and is **not** in the WFS. Of its factors, only **D (fibre exposure)** has a spectral handle (SWIR chrysotile, weak at WV-3), **B (large cracks)** is partly visible at pan 0.3 m, **A and C are invisible**; exposure factors E–H and age I are GIS/registry (H = ≤300 m to sensitive sites is pure GIS). VNIR carries the *biological* weathering signal (moss/lichen: chlorophyll 0.68 + red-edge 0.74); SWIR carries the *matrix-loss/fibre-exposure* signal. Published indices (Valdelamar Martínez 2024, 149 roofs): SWIR chrysotile indices (ISDCAP ~70.6%, R2327 ~71.0%) beat the VNIR vegetation index (~40%) for *grading*, while VNIR alone is strong for *detection* (~96% OA). **Proposal:** a two-tier Remote Degradation Proxy — an ordinal spectral surface class (low/med/high) × a GIS exposure overlay — presented as a *screening pre-filter*, not a substitute for on-site ID. The remote estimator is itself a contribution.

---

# 7. Experimental design (condensed)

**Three-axis ablation.** (A) spectral content R0→R3; (B) sensor: WV-3 (with SWIR) vs Pléiades Neo (VNIR-only) on the same sites; (C) native MS vs pansharpened — classify on **native** MS, use the 0.3 m pan for texture only (pansharpening injects space, not spectrum; use MRA/MTF methods, never GS/IHS; report SAM/ERGAS/Q2n). Run the ladder on **both** the per-pixel row and the full-CNN row (§6.3).

**Tasks.** T1 binary detection (floor); T2 material multi-class → coarse risk groups; T2-risk risk tier; **T3 asbestos pilot — run first and in full** (the only sub-problem with public geolocated labels coincident with the imagery and a textbook SWIR diagnostic; de-risks the whole pipeline before AerialWaste coordinates are ever needed).

**Backbones (run all so the conclusion isn't backbone-specific).** Swin-T + RSP extended (weight-inflation / late-fusion / random-init); DOFA (wavelength-conditioned = the structurally-fair spine); CNN-from-scratch (unbiased info-content control); SpectralFormer (spectra-only); per-pixel RF/SVM (the mandatory context-free baseline); Prithvi at R3 only (SWIR specialist). Tooling: TorchGeo, TerraTorch, rasterio, geopandas.

**Metrics.** macro-F1 **and per-class F1** (MS value concentrates in 1–2 hard materials, washed out by OA); for risk tiers add quadratic-weighted κ and ordinal MAE; headline = **ΔF1 vs R0** with bootstrap 95% CI + paired significance (McNemar).

**Splits — make generalization a reported axis.** Spatially-blocked ID split (never random tiles); cross-region (hold out provinces); cross-time; cross-sensor (WV-3↔PNeo). Report the ID−OOD gap per band cell.

---

# 8. The risk chain (end to end)

`RGB detects site (shape/context)` → `multiband infers material (chemistry)` → `material → EWC hazard code (asbestos 17 06 05*)` → `risk = hazard × exposure × magnitude` → `ranked intervention list for ARPA` (report precision@k of high-risk sites, not only global F1). Template: Fazzo 2020; condition term via the remote degradation proxy aligned to the Indice di Degrado thresholds (25/44/45).

---

# 9. Key numbers to memorize

- Detection on RGB: Gibellini **F1 92.02% / Acc 94.56%**; AerialWaste ensemble 92.41%; Disaitek ~95% (≥2 m², vendor).
- Cross-region drop: **−5.1% F1** (92.0→86.9).
- Cross-sensor: **2–4×** error (no band overlap), **5–25%** (superset) — GeoCrossBench.
- Asbestos, VNIR-only: **Saba Macro-F1 97.6%** (WV-3 VNIR, per-pixel). EnMAP ACE 91.4% / 86% field match (Shepherd; 30 m, out of VHR scope).
- WV-3 ablation (plastic-film analogy): OA **90.85 (VNIR) → 96.79 (SWIR) → 97.38 (all)** (Aguilar 2021).
- "Few bands suffice": **RGB + 2 NIR bands ≈ full 768-band HSI** (Vitek/CDW 2025).
- AC-degradation indices (Valdelamar Martínez 2024, 149 roofs): SWIR R2327 ~71% > VNIR ISDVeg ~41% for grading.
- Pixel footprints: WV-3 VNIR ~1.5 m² · SuperDove ~9 m² · WV-3 SWIR ~14 m².
- Indice di Degrado thresholds: **≤25 / 26–44 / ≥45**; asbestos WFS = 10,903 roofs (layer 1).
- Diagnostic features: chrysotile **2.30–2.33 µm**; plastics C-H **1.215 / 1.730 µm**; carbonate **2.34 µm**.

**Do NOT quote as fact (unverified / corrected):** Aguilar "+14% kappa" (use OA only; plastic-film/NDPI, not generic material); Saba "HS 97.3% vs MS 74.4%" (paywalled); Bonifazi AC F1 0.87 (screening-tool figure); Cilia "86/89%" precise figures. CascadeDumpNet = **Zhang & Ma 2024** (not Marrocco). Shepherd 2nd author = **Sagi**.

---

# 10. Professor Q&A (study for the defence)

**Q. What is the task, exactly?** Two sub-problems: detection (solved on RGB, F1 92%) and *classification by risk* of detected sites via the material. The contribution is the second, measured by a band ablation.

**Q. If RGB detects at 92%, why multiband?** Detection ≠ risk. RGB wins on morphology, not chemistry; ARPA must prioritise by hazard = material; ~5 of 13 classes are chemistry-bound where RGB is blind.

**Q. Why not Sentinel-2 (free, has SWIR)?** GSD. S-2 is 10–20 m; a dump is 1–4 mixed pixels there. Every VNIR material success is at 0.25–2.5 m, none ≥3 m.

**Q. What does SWIR buy, and what does Pléiades Neo lose?** SWIR holds the molecular overtones (asbestos 2.32, plastics 1.215/1.73, carbonate 2.34). Pléiades Neo (no SWIR) loses direct material confirmation → asbestos/plastics collapse to shape + VNIR proxy.

**Q. Is WV-3 SWIR useful or too coarse?** Honestly partial, possibly weak: 3.7 m + ~40 nm bands + atmospheric water attenuate the narrow Mg-OH feature. Measuring this (R3 vs R2) *is* the contribution. A null (R3 ≈ R2) is still publishable.

**Q. Mixed pixels — doesn't that kill the material claim?** It sets the ceiling, not zero. Lab numbers are upper bounds; on-satellite are mixed-pixel lower bounds; the cited detectors are already sub-pixel.

**Q. How do you prove the MS gain is chemistry, not texture?** The four-cell design: B−A (per-pixel MS−RGB) isolates pure spectral gain; B−A≈0 with D−C>0 means the gain was texture (honest negative).

**Q. Does multiband help or hurt generalization?** Narrows within-sensor (physics > appearance), widens cross-sensor (band mismatch) unless reflectance is harmonised — a publishable 2-D table.

**Q. Can you predict the Indice di Degrado remotely?** Not fully — only surface factors A–D, and only D weakly via SWIR; exposure E–H and age I are GIS. Output an ordinal screening class, not a fake continuous ID.

**Q. Is the contribution novel?** The 2-D ablation×generalization table at the empty VHR material operating point, the chemistry-vs-texture decomposition, the material→EWC→risk chain, and the asbestos pilot demonstrator — the combination, hedged.

**Q. Is the data feasible?** Free via ESA TPM (~9 wk); asbestos pilot has public WFS labels now; the real risk is WV-3 SWIR archive over the AOI and SWIR co-registration at 3.7 m.

**Q. Why not hyperspectral (EnMAP/PRISMA)?** They resolve the 2.3 µm triplet but at 30 m — useless over decimetre waste. No sensor today has both hyperspectral resolution and sub-metre GSD over wide areas; the thesis works in that realistic gap.

**Q. Biggest risk of a null result?** That WV-3 SWIR at 3.7 m is too diluted to beat VNIR for asbestos (R3 ≈ R2). Still a valid, publishable finding; the four-cell design guards against the opposite error.

---

# 11. Glossary

- **EO** Earth Observation. **MS** multispectral (few broad bands). **HSI** hyperspectral (100s of narrow bands). **VNIR** visible–near-infrared (0.4–1.0 µm). **SWIR** short-wave infrared (1.0–2.5 µm; molecular overtones).
- **GSD** Ground Sampling Distance (pixel size on the ground; keep untranslated). **Pan** panchromatic (one broad high-resolution band).
- **SAM / ACE / SID** spectral matching: Spectral Angle Mapper / Adaptive Cosine (Coherence) Estimator / Spectral Information Divergence. **ERGAS / Q2n** pansharpening quality metrics.
- **EWC** **European Waste Catalogue / European Waste Codes** (List of Waste, Decision 2000/532/EC; asbestos 17 06 05*). *(Not the ML term "Elastic Weight Consolidation".)*
- **Endmember** pure-material reference spectrum. **Mixed pixel** a pixel integrating several materials. **Unmixing** estimating sub-pixel abundances. **NDPI** Normalized Difference Plastic Index. **RSP** Remote Sensing Pretraining.
- **Indice di Degrado** Lombardy AC-roof site-inspection degradation score (d.d.g. 13237/2008). **Generalizzazione** performance on data unlike training (cross-region / cross-sensor / cross-time); **ID−OOD gap** in-domain minus out-of-domain score.
- **DOFA** wavelength-conditioned foundation model (variable band sets). **C-H / Mg-OH / CO₃** molecular bonds whose SWIR absorptions identify plastics / asbestos / carbonate.

---

# PART II — Papers to study

*(Study cards for all 47 papers follow, grouped by theme, each with the one number and the one limitation to remember. Citations reconciled against the verified bibliography.)*
