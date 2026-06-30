# PERIVALLON Master Cheat-Sheet — One-Page Revision

*Autonomous research loop, iteration 4 (2026-06-28). Detect illegal waste from VHR satellite, then **classify by risk** (material). Core measurement: added value of **multiband over RGB** for material discrimination. Quick-revision companion to the full panorama (see README).*

---

## Sensors at a glance
| Sensor | VNIR | SWIR | Pan | Role |
|---|---|---|---|---|
| **WorldView-3** | 8 bands @ **1.24 m** | **8 bands @ 3.7 m** | ~0.3 m | full ladder incl. R3 chemistry |
| **Pléiades Neo** | 6 bands @ **1.2 m** | **none** | ~0.3 m | cross-sensor axis; VNIR-only |
| SuperDove | 8 bands @ 3 m | none | — | R2 full-VNIR (free, near-daily) |
| Sentinel-2 | 10–20 m | 20 m | — | **too coarse for material** |
| EnMAP/PRISMA | hyperspectral ~6.5 nm | yes | — | resolves 2.3 µm triplet but **30 m** |

**WV-3 VNIR:** Coastal .425 · Blue .48 · Green .545 · **Yellow .605** · Red .66 · **RedEdge .725** · NIR1 .833 · **NIR2 .95** µm (Yellow+NIR2 unique vs PNeo)
**WV-3 SWIR:** 1.21 · 1.57 · 1.66 · **1.73** · 2.16 · 2.20 · 2.26 · **2.33** µm
**PNeo VNIR:** DeepBlue .425 · Blue .483 · Green .562 · Red .655 · RedEdge .725 · NIR .84 (NO SWIR)

---

## The band ladder (ablation)
**R0 RGB → R1 +RedEdge/NIR → R2 full VNIR (8-band) → R3 +SWIR (WV-3).**
R3 = only step adding diagnostic chemistry. Expected: small VNIR uplift, large SWIR jump for chemistry-bound classes (Aguilar plastic-film analogy: OA 90.85→96.79→97.38).
**Run ladder on BOTH rows:** per-pixel (context-free) AND full-CNN. **B−A = pure chemistry gain; D−C = total MS gain.**

---

## Diagnostic features → band (memorize)
| Material | Feature µm | WV-3 band | PNeo? |
|---|---|---|---|
| **Asbestos** (chrysotile Mg-OH) | **2.30–2.33** | SWIR8 (2.33) | ✗ |
| **Plastics** (C-H) | **1.215 / 1.730** / 2.31 | S1, **S4**, S8 | ✗ |
| **Concrete/C&D** (carbonate / clay) | **2.34** / 2.20 | S8 / S6 | ✗ |
| Slag/rust (Fe-oxide) | 0.87–0.95 | NIR1/**NIR2** | weak |
| AC weathering (moss/lichen) | 0.68 + 0.74 | Red+RedEdge | ✓ |

⚠ **SWIR-8 bottleneck:** asbestos 2.32 + concrete 2.34 + plastic 2.31 all crowd into ONE WV-3 band → cannot resolve within it; discrimination uses shoulders (2.16/2.20/2.26, 1.21/1.73) + VNIR shape.

---

## 13 classes: shape vs chemistry
**Shape-identifiable (8, RGB OK):** vehicles, tanks, containers, rubble, bulky, wood, tyres, big-bags.
**Chemistry-bound (5, RGB blind — MS lives here):** **asbestos, plastic-type, foundry slag, sludge, scrap-metal composition.**
Asbestos + plastics = ideal test beds (shape cue AND chemistry cue coexist).

---

## Key numbers
- **Detection solved on RGB:** Gibellini F1 **92.02%** / Acc 94.56%; AerialWaste ensemble F1 92.41%; Disaitek ~95% @ ≥2 m².
- **Cross-region drop:** **−5.1% F1** (92.0→86.9; GR 85.4 / SE 83.8 / RO 91.5).
- **Cross-sensor (band mismatch):** **2–4× drop** (no overlap), **5–25%** (superset) — GeoCrossBench. χViT > DINOv3 > … > DOFA.
- **Asbestos VNIR:** Saba Fine-KNN Macro-F1 **97.6%** (WV-3 VNIR, per-pixel). Shepherd EnMAP ACE 91.4→86% field.
- **AC degradation indices (Martínez, 149 roofs, 16/84):** ISDVeg 40.7 / ISD2327 40.5 / ISDCAP 70.6 / **R2327 71.0%** — SWIR > VNIR for grading.
- **Pixel footprints:** WV-3 VNIR ~1.5 m² · SuperDove ~9 m² · WV-3 SWIR ~14 m². **No pure pixels over a dump.**
- **Indice di Degrado:** ID=(A..H)×I; thresholds **≤25 / 26–44 / ≥45**; NOT in public WFS.
- **Data:** free via ESA TPM (~9 wk proposal + 1-yr quota). Asbestos GT: Mappatura_2020 = 10,903 roofs, EPSG:32632.

---

## The risk chain
RGB detects **site** (shape/context) → multiband infers **material** (chemistry) → material → **EWC hazard code** (asbestos 17 06 05*) → **risk = hazard × exposure × magnitude** → **ranking** for ARPA triage (report precision@k, not just F1). Template: Fazzo 2020.

## Generalization verdict
MS **narrows** gap within-sensor (physics > appearance); **widens** gap cross-sensor unless reflectance harmonized + band-gap handled. RGB = lowest common denominator, ports trivially. → Publishable 2-D table: **ablation × generalization axis, ID−OOD gap per cell.**

## Cheapest wins first
1. resize + per-channel normalization (Corley) 2. surface reflectance (atmospheric correction) 3. DOFA/χViT band-handling 4. band-dropout augmentation 5. domain adaptation.

## Honest caveats to volunteer
- WV-3 SWIR 3.7 m + ~40 nm + atm. H₂O → asbestos feature attenuated, R3 may ≈ R2 (still a valid finding).
- B−A ≈ 0 ⇒ MS gain is texture, not chemistry (negative-result protection).
- Lab numbers = pure-pixel upper bounds; on-satellite = mixed-pixel lower bound.
- Unmixing = out of scope but sets the ceiling.

## ⚠ Don't-quote-as-fact (downgraded)
- Aguilar "+14% kappa" — DROPPED (use OA only); it's plastic-film/NDPI, not generic material.
- Saba "HS 97.3% vs MS 74.4%" — UNVERIFIED (paywalled).
- Bonifazi AC F1 0.87; Cilia "40%/86%/89%" — UNVERIFIED.
- chrysotile "~5 nm width" — WRONG (tens of nm).

---

## Glossary
- **EO** Earth Observation · **MS** multispectral (few broad bands) · **HSI** hyperspectral (100s narrow bands) · **VNIR** visible-near-IR (0.4–1.0 µm) · **SWIR** short-wave IR (1.0–2.5 µm; molecular overtones).
- **GSD** Ground Sample Distance (pixel size on ground; keep untranslated) · **Pan** panchromatic (single broad high-res band).
- **SAM / ACE / SID** spectral matching: Spectral Angle Mapper / Adaptive Coherence Estimator / Spectral Information Divergence.
- **EWC** **European Waste Catalogue / European Waste Codes** (List of Waste, Decision 2000/532/EC; asbestos = 17 06 05*). *(Not to be confused with the ML term "Elastic Weight Consolidation".)*
- **MNF** Minimum Noise Fraction (denoising/dim-reduction) · **NDPI** Normalized Difference Plastic Index · **RSP** Remote Sensing Pretraining.
- **Endmember** pure-material reference spectrum · **Mixed pixel** pixel integrating ≥2 materials · **Unmixing** estimating sub-pixel abundances.
- **ID (Indice di Degrado)** Lombardia AC-roof site-inspection degradation score (d.d.g. 13237/2008).
- **Generalizzazione** = performance on data unlike training (cross-region / cross-sensor / cross-time) · **ID/OOD gap** = in-domain minus out-of-domain score.
- **DOFA** wavelength-conditioned foundation model (variable band sets) · **χViT** channel-sampling ViT (strong cross-band generalizer).
- **C-H / Mg-OH / CO₃ / Al-OH** molecular bonds whose SWIR vibration overtones identify plastics / asbestos / carbonate / clay.
