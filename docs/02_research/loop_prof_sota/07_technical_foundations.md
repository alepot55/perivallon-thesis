# Scientific Foundations — Material ↔ Feature ↔ Band, Remote AC Degradation, Generalization, Object-vs-Material

*Autonomous research loop, iteration 4 (2026-06-28). Study-ready deepening of the thesis foundations. Verification corrections folded in: refuted/unverified items dropped or downgraded, confidence HIGH / MEDIUM / UNCERTAIN. This document is the **physics and experimental logic**, not the dataset/direction (covered in 01–06).*

---

## 0. Sensor band reference — what each band physically buys

**WorldView-3 VNIR — 8 bands @ 1.24 m** (~1.5 m²/pixel)

| # | Name | Center µm | Buys you |
|---|---|---|---|
| 1 | Coastal | 0.425 | aerosol/water, weak material info |
| 2 | Blue | 0.480 | colour, iron-oxide shoulder |
| 3 | Green | 0.545 | colour, vegetation peak |
| 4 | Yellow | 0.605 | **unique to WV-3** — discolouration cues |
| 5 | Red | 0.660 | chlorophyll (moss/lichen on AC) |
| 6 | RedEdge | 0.725 | **vegetation/colonization red-edge** — drives AC weathering index |
| 7 | NIR1 | 0.833 | biomass, cellulose, iron-oxide |
| 8 | NIR2 | 0.950 | **unique to WV-3** — iron-oxide/rust, moisture shoulder |

**WorldView-3 SWIR — 8 bands @ 3.7 m native** (~14 m²/pixel)

| # | Center µm | Buys you (diagnostic chemistry) |
|---|---|---|
| S1 | 1.210 | **plastics C-H** overtone (1215 nm) |
| S2 | 1.570 | broadband, carbonate shoulder |
| S3 | 1.660 | clay/OH shoulder |
| S4 | 1.730 | **plastics C-H** combination — strongest usable plastic band |
| S5 | 2.160 | Al-OH (clay), AC-weathering shoulder |
| S6 | 2.200 | Al-OH (clay/C&D fines) |
| S7 | 2.260 | chrysotile/cement contrast shoulder |
| S8 | 2.330 | **chrysotile Mg-OH (~2.30–2.33)** + carbonate (~2.34) + plastics C-H (~2.31) — single most diagnostic band |

**Pléiades Neo VNIR — 6 bands @ 1.2 m, NO SWIR**: DeepBlue 0.425, Blue 0.483, Green 0.562, Red 0.655, RedEdge ~0.725, NIR ~0.84. Pan ~0.30 m (both).
→ PNeo has **no Yellow, no NIR2, no SWIR** → every chemistry-bound class collapses to a shape/colour proxy. `HIGH`

---

## 1. Material ↔ Feature ↔ Band MASTER TABLE (the centerpiece)

Rule (Waste Management 2024 survey + Gibellini 2025): **feasible at broadband VNIR if identity lives in shape/context; weak if it lives in spectral chemistry.** `HIGH`

| # | Class | Identity carrier | Diagnostic feature (µm) | WV-3 band | On PNeo (no SWIR) | Verdict at VHR | Conf |
|---|---|---|---|---|---|---|---|
| 13 | **Asbestos-cement** | shape + **chemistry** | chrysotile Mg-OH 2.30–2.33; OH ~1.39 | **SWIR8 (2.33)** + S7 2.26 | shape + VNIR moss/lichen proxy | corrugated shape at 30–50 cm; **confirm needs SWIR** | HIGH |
| 9 | **Plastics (polymer)** | presence=texture; **type=chemistry** | C-H 1.215 / 1.730 / 2.31 | **S1, S4, S8** | presence only | presence at VHR; **polymer ID needs SWIR** | HIGH |
| 1 | **C&D / inert rubble** | **shape** + chemistry | carbonate 2.34; Al-OH 2.20 | **S8, S6** | heap morphology | strong by shape; composition needs SWIR | HIGH |
| 2 | **Foundry slag** | **chemistry** (data-starved) | Fe-oxide 0.87–0.95; glassy SWIR | NIR1/**NIR2**; SWIR | weak Fe-oxide cue | **GAP** (spectral + ~9 labels) | HIGH |
| 4 | **Scrap metal** | scene=**shape**; type=chemistry | metals ~flat/specular, **no feature** | none | scrapyard scene | scene-detectable; **type=GAP even w/ SWIR** | MEDIUM |
| 12 | **Tyres (rubber)** | shape / **dark target** | carbon-black ⇒ low R; weak C-H | broadband low; S4 weak | dark piles | piles OK; confuses w/ shadow/water/asphalt | MEDIUM |
| 8 | **Wood / organic** | **shape** (stacks) | cellulose-lignin ~2.1/2.3; red-edge | NIR1/SWIR; RedEdge | stacked piles | good by shape | MEDIUM |
| 7 | **Sludge** | **context** + chemistry | water + organic, no sharp feature | broadband + NIR | lagoon context | **GAP** (composition) | MEDIUM |
| 10 | **Big-bags / FIBC** | shape but **small** | woven PP → C-H 1.73 (sub-pixel) | S4 (diluted) | shape, tiny | near-GAP (~3×3 px @30 cm) | MEDIUM |
| 3 | **Vehicles / ELV** | **shape** | — | — | shape | excellent (object) | HIGH |
| 11 | **Tanks / cisterns** | **shape** (circular) | — | — | shape | excellent — *not a gap* | HIGH |
| 6 | **Containers / skips** | **shape** | — | — | shape | strong (object) | MEDIUM |
| 5 | **Bulky items** | **shape** | — | — | shape | good (object) | MEDIUM |

**Synthesis.** 8/13 shape-identifiable at 30–50 cm; **5 chemistry-bound** (asbestos, plastic-type, foundry slag, sludge, scrap composition) — where RGB fails and the MS/risk argument must live. **Asbestos and plastics are ideal test beds**: shape cue + chemistry cue coexist → object findable in RGB, risk-defining identity needs the spectrum. `HIGH`

**⚠ The SWIR-8 bottleneck.** Chrysotile Mg-OH (~2.32), carbonate (~2.34), plastics C-H (~2.31) all crowd into the **same WV-3 SWIR8 (2.33)** ~40 nm band → WV-3 cannot *resolve* them within it, only flag "something absorbs near 2.33". Discrimination leans on **shoulders** (S5 2.16, S6 2.20 clay; S7 2.26; S1/S4 plastic) + VNIR context. A hyperspectral sensor (~6.5 nm) would resolve the triplet; WV-3 won't. `HIGH`

### Verified spectral anchors
- Chrysotile Mg-OH **2.30–2.33 µm** (min ~2.32). `HIGH`
- Plastics C-H **1.215 / 1.730 µm** dominant (2.31 weaker, in a water-vapour region). `HIGH`
- Carbonate/calcite **~2.335–2.34 µm** (distinct from chrysotile 2.32). `HIGH`
- Iron-oxide **0.87–0.95 µm** (WV-3 NIR1/NIR2). `MEDIUM`

---

## 2. Remote estimation of asbestos-cement roof degradation

**Critical framing:** the regulatory **Indice di Degrado (ID)** is a *site-inspection* score, NOT a spectral quantity, and NOT in the public WFS (verified, `05_field_metadata.md`). The thesis can build a *remote proxy* for **part** of it, never the full ID.

### 2.1 Physics of AC weathering
- **VNIR = biological/colour signal:** weathered porous surfaces host **moss/lichen** → chlorophyll ~0.68 µm + red-edge ~0.74 µm + darkening. Cilia's index tracks moss/lichen abundance, not surfacing fibres directly. `HIGH`
- **SWIR = matrix-loss / fibre-exposure:** acid-rain/carbonation erode the cement matrix, exposing chrysotile → deepening Mg-OH ~2.32. `MEDIUM`
- **Double-edged caveat:** lichens both weather AC *and* cover/bind loose fibres → colonization proxies *age/exposure*, not necessarily *fibre-release hazard*. `MEDIUM`

### 2.2 Published indices (Martínez 2024, 149 field roofs, 16% low / 84% high priority)
| Index | Bands (µm) | Targets | Precision | Conf |
|---|---|---|---|---|
| ISDVeg (Cilia-type) | 0.680 / 0.740 | moss/lichen + matrix colour | ~40.7% | HIGH |
| ISD2327 | 2.326–2.331 vs 2.387 | chrysotile vs cement peak | ~40.5% | HIGH |
| ISDCAP | depth @2.327 vs endmembers | fibre exposure | ~70.6% | HIGH |
| R2327 | single band ~2.31 | fibre exposure | ~71.0% | HIGH |

**Key:** SWIR chrysotile indices (ISDCAP, R2327) **outperform** the VNIR vegetation index for *grading* (VNIR confounded by climate-dependent biology); but **VNIR alone is strong for AC *detection*** (~96% OA). `HIGH`
*Cilia 2015's often-quoted "~40% high-priority; 86% UA / 89% PA" figures are `UNCERTAIN` (not re-confirmed) — don't present as load-bearing.*

### 2.3 Band mapping
- **WV-3:** ISDVeg from VNIR (Red/RedEdge/NIR1); coarse R2327/ISDCAP from **SWIR8 + S5/S7**. But WV-3 SWIR is 3.7 m + ~40 nm + atm. H₂O → undersamples the chrysotile feature → expect the SWIR proxy weak, possibly non-significant. `MEDIUM`→`UNCERTAIN`
- **Pléiades Neo:** no SWIR → only the **VNIR/ISDVeg moss-lichen proxy**. `HIGH`

### 2.4 Regulatory ID vs what is observable
`ID = (A+B+C+D+E+F+G+H) × I`; thresholds **≤25 / 26–44 / ≥45** (d.d.g. 13237/2008). `HIGH`

| Factor | Measures | Remotely observable? |
|---|---|---|
| A consistency | binder cohesion | **No** (tactile/acoustic) |
| B cracks/flaking | fracturing | Partial (pan ~0.3 m, large only) |
| C stalactites/deposits | matrix leaching | **No** (sub-pixel/underside) |
| D friability/fibre exposure | fibre release | **Proxy** (SWIR chrysotile) |
| E ventilation | exposure | No (GIS/building model) |
| F visible from interior | exposure | No |
| G distance to windows ≤5 m | exposure | Partial (GIS proximity) |
| H sensitive sites ≤300 m | exposure | **Yes** (pure GIS) |
| I age multiplier (×2/3/4) | age | Proxy (colonization/darkening) or cadastral |

→ Only the **surface block A–D** is imaging-targetable, and only **D (weakly B)** has a spectral handle; **A, C invisible**. The **exposure block E–H + age I are GIS/registry problems**, several directly computable.

### 2.5 Proposed Remote Degradation Proxy (RDP) — honest two-tier
- **Tier 1 (spectral surface class):** WV-3 = ISDVeg + coarse SWIR; PNeo = ISDVeg only → output an **ordinal class (low/med/high weathering)**, NOT a fake continuous ID (matches Cilia 2-class / Martínez HIP-LIP and Thomas's "classify by risk").
- **Tier 2 (GIS overlay, free accuracy):** compute H (≤300 m sensitive sites), G (window proximity), I (age) directly from vectors — 1:1 with regulatory factors, no imagery.
- **Combine** Tier 1 × Tier 2 → **risk-priority ranking** for ARPA, explicitly a *screening pre-filter*, not a substitute for on-site ID.

**Validation GT (best→worst):** (1) filed ID surveys from ATS/ARPA via advisors; (2) small field campaign scoring A–D; (3) photo-interpretation into low/med/high (risks circularity); (4) HIP/LIP binary proxy. WFS gives locations + possibly install-year (factor I) but **no condition field**. `HIGH`

---

## 3. Generalization ("generalizzazione") — the advisor's claim is quantifiable

| Mode | Mechanism | Magnitude | Conf |
|---|---|---|---|
| **Cross-sensor / cross-band** (WV-3↔PNeo) | band centers/widths/SNR/calibration differ | **2–4× drop** (no overlap); **5–25%** (superset) | HIGH |
| **Cross-region** (Lombardia → EU) | covariate shift, soil/building stock | **−5.1% F1** (92.0→86.9; GR 85.4 / SE 83.8 / RO 91.5) | HIGH |
| **Cross-time/season** | phenology, weathering, moisture | task-specific double-digit | MEDIUM |
| **Atmospheric/illumination** | TOA vs surface R, BRDF, shadows | removed by surface-R correction | HIGH |

Sensor/acquisition shift dominates because the signal lives in *narrow* features (asbestos 2.32, plastics 1.215/1.73) — exactly what band-set/atmosphere perturb.

**Evidence:** GeoCrossBench (arXiv 2511.02831) — 2–4× no-overlap, 5–25% superset; best = χViT (channel-sampling); **even general DINOv3 beat DOFA-style wavelength-conditioning** in their protocol (χViT 44.51 > DINOv3 42.88 > … > DOFA 38.21). `HIGH` mechanism / `MEDIUM` single benchmark. · Shepherd 2025 EnMAP asbestos ACE 91.4% lib → 86% field. · Corley CVPR-W 2024 — resize+per-channel normalization recovers much of the "domain gap"; **cheapest highest-ROI fix, do first**. `HIGH`

**Mitigations by leverage:** (1) resize+normalization; (2) surface reflectance (prereq for SAM/ACE transfer + WV-3/PNeo comparability); (3) wavelength-conditioned FM (DOFA — right mechanism, NOT a guaranteed fix); (4) channel/band-sampling SSL + band-dropout; (5) domain adaptation only if 1–4 insufficient.

**Report it credibly:** hold out **entire regions** (never random tiles — spatial autocorrelation leaks); report **ID + OOD + the gap (ID−OOD) as a first-class metric**; match preprocessing across domains and say so; ≥3 seeds, per-region/class; include a normalization-only baseline; for ARPA report **precision@k of high-risk sites** (ranking can survive OOD even when F1 drops).

### 3.1 Publishable question: does multiband NARROW or WIDEN the gap vs RGB?
- **Narrows** within-sensor: material rests on *physical absorptions*, more invariant than RGB colour/texture (Shepherd 91→86%). `MEDIUM`
- **Widens** cross-sensor: extra bands are exactly where mismatch lives; GeoCrossBench penalties are *driven by* non-RGB bands; RGB = lowest common denominator, ports trivially. `HIGH`

**Defensible claim:** *MS narrows the gap for cross-region/cross-time on a fixed sensor, but widens it cross-sensor unless the band mismatch is explicitly handled (reflectance harmonization + wavelength-conditioning/band-sampling). MS-over-RGB value is conditional on closing the radiometric/band gap; reported naïvely, MS can look worse OOD than RGB.* → Clean novel experiment = **2-D table: ablation level (R0→R3) × generalization axis (cross-region / cross-sensor / cross-time), ID−OOD gap per cell.**

---

## 4. Object vs Material, and mixed pixels

**Central caveat:** at VHR, **detection** is largely solved by **shape/context** (Gibellini F1 92.02% / Acc 94.56%; AerialWaste ensemble 92.41%; Disaitek ~95% on objects ≥2 m²). So the MS value proposition is **not** detection — it's **material/risk classification**, which the VHR literature leaves empty. `HIGH`

### 4.1 Mixed pixels set the ceiling (out of scope, but discussable)
Footprints: WV-3 VNIR ~1.5 m² · SuperDove ~9 m² · WV-3 SWIR ~14 m². Waste objects are decimetre-scale → **essentially no pure pixels**; each integrates waste + soil + shadow + vegetation. Linear mixing (segregated) vs nonlinear/intimate mixing (soil-coated plastic, mixed rubble — common on dumps). The cited SOTA target detectors (Aguilar matched-filter, EMIT plastics) are **already sub-pixel** — "we don't do unmixing" is true of our *method*, but unmixing physics governs the *ceiling*. Diagnostic features are diluted by sub-pixel fraction; **GSD, not band count, is often the binding constraint**. `HIGH`

### 4.2 Separating object (texture) from material (chemistry) — the experiment that makes MS defensible
A CNN has a receptive field → MS-CNN > RGB-CNN could be *texture in extra channels*, not chemistry. Four-cell decomposition:

| | RGB bands | MS bands |
|---|---|---|
| **Spatial-context-FREE** (per-pixel/per-object-mean; RF=1 px) | A | B |
| **Full CNN** (spatial RF) | C | D |

- **B − A = pure chemistry/spectral gain** — the number that attributes MS value to material, not texture.
- **D − C = total MS gain in the deployed CNN** (chemistry + MS-texture).
- **B−A ≈ 0 but D−C > 0 ⇒ the gain is texture** — an honest negative result for the material claim.

**Context-free baselines (precedent):** per-pixel/per-object classifier (1×1 conv, MLP, RF, SVM, KNN) — *Saba Fine-KNN on WV-3 VNIR pixel features, Macro-F1 97.6% asbestos* `HIGH`; texture-destruction permutation control; pure-endmember upper bound (splib07a convolved to WV-3/SuperDove). Band ladder sits on the full-CNN row and **must be paired with the per-pixel row**.

**Expected (Aguilar 2021 WV-3 analogy): OA 90.85 (VNIR) → 96.79 (SWIR) → 97.38 (all)** — small VNIR uplift, large SWIR jump. *Caveat: Aguilar = greenhouse **plastic-film** (NDPI), a plastic-class analogy, not generic material; previously-quoted "+14% kappa" is `UNCERTAIN` — dropped.* `HIGH` (OA).

### 4.3 The "VNIR penalty" number — handle with care
"asbestos HS 97.3% vs MS 74.4%" is **`UNCERTAIN`** (paywalled) — don't present as load-bearing. Use **Saba Fine-KNN Macro-F1 97.6% (WV-3 VNIR)** `HIGH` as the verified VNIR-asbestos anchor. Bonifazi WV-3 VNIR+SWIR AC F1 0.87 is `UNCERTAIN` (repo-note only) — confirm before use.

---

## 5. Corrections folded in (audit trail)
- **Dropped:** Aguilar "+14% kappa" (unverified); chrysotile "~5 nm feature width" (overstated — tens of nm).
- **Downgraded UNCERTAIN:** Saba "HS 97.3% vs MS 74.4%"; Bonifazi AC F1 0.87; Cilia "~40%/86%/89%".
- **Reframed:** Aguilar = plastic-film (NDPI) analogy, not generic material.
- **Sharpened:** GeoCrossBench — even general DINOv3 beat DOFA.
- **Confirmed anchors:** chrysotile 2.30–2.33; plastics 1.215/1.730; carbonate 2.34; Gibellini 92.0/86.9/−5.1; GeoCrossBench 2–4× / 5–25%; Shepherd 91.4/86; Martínez suite (40.7/40.5/70.6/71.0, 149 roofs, 16/84); Aguilar OA 90.85/96.79/97.38; Saba 97.6; ID thresholds 25/44/45; pixel footprints.

### Sources
Gibellini/Torres arXiv:2502.06607 · GeoCrossBench arXiv:2511.02831 · Corley CVPR-W 2024 arXiv:2305.13456 · DOFA arXiv:2403.15356 · Shepherd 2025 Nature s41598-025-09738-w · Cilia 2015 IJGI 4(2):928 · Martínez 2024 Heliyon PMC10865312 · Aguilar 2021 Remote Sens. 13(11):2133 · Garaba & Dierssen 2021 PMC7940656 · d.d.g. Lombardia 13237/2008 · USGS splib07a.
