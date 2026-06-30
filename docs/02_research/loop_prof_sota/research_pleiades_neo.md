# Pléiades Neo — Focused Deep Dive for the PERIVALLON Thesis

*Airbus Pléiades Neo constellation (NOT Pléiades-1A/1B "Pléiades HR"). All facts tagged HIGH / MEDIUM / UNCERTAIN; vendor claims flagged as such. Autonomous research loop, iteration 1, 2026-06-27.*

---

## 1. Exact sensor specification

**Confidence: HIGH** — confirmed against eoPortal (which mirrors Airbus/CNES technical sheets) and cross-checked with ESA Earth Online and the Airbus Pléiades Neo User Guide.

| Band | Wavelength range | Notes |
|---|---|---|
| **Deep Blue (coastal/aerosol)** | **400–450 nm** | NEW vs Pléiades-1 |
| Blue | 450–520 nm | |
| Green | 530–590 nm | |
| Red | 620–690 nm | |
| **Red Edge** | **700–750 nm** | NEW vs Pléiades-1 |
| Near-IR | 770–880 nm | |
| Panchromatic | 450–800 nm | |

- **Pan GSD 0.30 m; MS GSD 1.2 m** (native, at nadir). HIGH.
- **Radiometric depth: 12-bit** at acquisition. HIGH.
- **Swath: 14 km** at nadir; geolocation <5 m CE90 (Airbus advertises ~3.5 m). HIGH / MEDIUM.
- **Revisit:** twice-daily anywhere (≤46° off-nadir), once-daily at ≤30°. Constellation of **4 identical satellites at ~620 km**; Neo 3 (Apr 2021) and Neo 4 (Aug 2021) operational, Neo 5 & 6 lost in the Dec 2022 Vega-C launch failure — so the operational constellation is **2 satellites, not 4**. HIGH (important caveat: vendor "twice daily" assumes the full 4-bird constellation that no longer exists).

**What Deep Blue + Red Edge buy for MATERIAL discrimination** (vs plain RGB+NIR like Pléiades-1 or SuperDove minus its extra bands):
- **Deep Blue (400–450 nm)** is primarily an atmospheric/aerosol and water-penetration band. For *material* discrimination its added value is modest: it extends the visible blue shoulder, marginally helping separate dark/shadowed surfaces and some pigments, but it carries little material-diagnostic absorption signal. MEDIUM — its documented utility is atmospheric correction and turbidity, not roofing/waste materials.
- **Red Edge (700–750 nm)** is the high-value addition: it samples the steep vegetation reflectance rise, which sharply separates **vegetal/organic waste and vegetated background from inert man-made materials** (plastics, construction debris, metal, asbestos-cement). This directly supports the thesis's material/risk-classification axis by suppressing vegetation confusion — a known false-positive source in dumpsite detection. MEDIUM-HIGH.
- Critically, **neither band reaches SWIR**, where the diagnostic absorptions for plastics (~1.7/2.3 µm), hydrocarbons, and asbestos-cement carbonate/hydroxyl features live. So Pléiades Neo, like SuperDove, is a **VNIR-only** sensor: its "added MS value" is *texture + vegetation/edge separation*, not true spectral material fingerprinting. HIGH — this is the key honest framing for the thesis.

---

## 2. Studies using Pléiades Neo for material/waste discrimination

**Confidence: MEDIUM-LOW for peer-reviewed; the field is young (sensor live only since mid-2021).** Most evidence is vendor/grey literature; rigorous peer-reviewed material-classification papers on *Neo specifically* are scarce.

- **Disaitek "Illegal Waste Tracker" on Pléiades Neo 30 cm** (operational, Airbus case study + disaitek.ai). Task: illegal dumping detection, localization, and *waste-type qualification* (end-of-life vehicles, construction waste, tyres, vegetal waste). Claimed: detection of waste volumes down to **~2 m²** with reliability "reaching 95%." Bands/method not disclosed (proprietary AI on pansharpened 30 cm). **Public data: NO; metric is a vendor claim, not independently validated.** MEDIUM (existence verified; numbers UNCERTAIN).
- **Pléiades Neo for urban vegetation / land cover** (Airbus–Space Climate Observatory case study, and UP42 Red-Edge NDVI demonstration). Classes: built-up, road, bare soil, water, vegetation. Confirms Neo's 6-band VHR usefulness for urban surface separation, but these are *cover-type*, not *material*, tasks. MEDIUM.
- **Roof-material identification from Pléiades spectral responses** (academia.edu, supervised classification) — this uses **Pléiades-1, not Neo** (no Red Edge/Deep Blue). Relevant as method precedent only. MEDIUM.
- **BIRDIA / Airbus "roof health" monitoring** on Pléiades Neo — roof-facet segmentation, covering/wear characterization via hybrid DL + expert rules. Grey literature; no public benchmark. MEDIUM.
- **Solar/roof segmentation from off-nadir Pléiades Neo 30 cm + photogrammetric DSM** (arXiv 2408.14400). Geometry/segmentation task, not spectral material ID. MEDIUM.
- **USGS "System characterization report on the Pléiades Neo Imager"** (USGS Open-File Report 2021-1030) — independent radiometric/geometric characterization; the authoritative non-vendor reference for sensor quality. HIGH (for sensor characterization, not for a material task).

**Bottom line:** there is **no strong peer-reviewed Pléiades-Neo material-classification benchmark** to anchor against. This is both a gap and an opportunity for the thesis.

---

## 3. Pansharpening to 0.30 m and spectral fidelity

**Confidence: MEDIUM.**

- Products ship in **DIMAP V2**. Airbus offers: Panchromatic (0.3 m), Multispectral (1.2 m), **Bundle** (pan + MS delivered separately, 5- or 7-band), and **Pansharpened** (MS resampled to 0.3 m pan grid). HIGH.
- The honest scientific concern for *material* work: pansharpening is a **resolution-enhancement that injects pan spatial detail into MS bands; it does not create new spectral information.** The MS bands' true spectral sampling remains 1.2 m. Pansharpening can introduce **spectral distortion** (the well-documented spatial-vs-spectral-consistency trade-off across CS/MRA/variational/DL methods). For pixel-level material discrimination the safer practice is to **classify on the native 1.2 m MS (Bundle) and use the 0.3 m pan only for texture/segmentation/edges**, rather than trusting per-band radiometry at 0.3 m. MEDIUM (general pansharpening literature; no Neo-specific spectral-fidelity benchmark found).
- Practical implication: at 0.3 m a small dump/roof is many pixels (texture-rich), but each MS spectrum effectively integrates a ~1.2 m footprint — the "spectral" resolution for materials is 1.2 m, not 0.3 m. HIGH (logical consequence of the optics).

---

## 4. Research access

**Confidence: HIGH.**

- **ESA Third Party Missions (TPM)** — Pléiades Neo full archive + tasking is available to the scientific community **free of charge within an ESA-approved quota**, via an evaluated **project proposal** (typical evaluation 4–6 weeks). This is the same channel PoliMi/ESA-member researchers already use for Pléiades 50 cm. Route: ESA Earth Online → "Pléiades Neo full archive and tasking" → submit proposal. **This is the recommended free route for the thesis.** HIGH.
- **Airbus OneAtlas** — commercial platform (Living Library streaming/download, tasking). Paid; relevant only if TPM quota or tasking windows are insufficient. HIGH.
- **Airbus Pléiades Neo "Applications Campus" / Call for Projects** — periodic Airbus programme granting Neo imagery to selected research/startup projects; a possible no-cost tasking route worth a proposal. MEDIUM.

---

## 5. Pléiades Neo vs WorldView-3 for THIS thesis

**Confidence: HIGH on specs, MEDIUM on "which wins."**

| Axis | Pléiades Neo | WorldView-3 |
|---|---|---|
| Pan GSD | **0.30 m** | 0.31 m |
| MS GSD | 1.2 m, **6 VNIR bands** | 1.24 m, **8 VNIR bands** |
| SWIR | **None** | **8 SWIR bands @ 3.7 m** ← decisive for materials |
| Distinctive bands | Deep Blue, Red Edge | Coastal, Yellow, Red Edge, NIR2 + SWIR |
| Radiometry | 12-bit | 11-bit (VNIR) |
| Revisit | sub-daily (2-sat constellation) | ~1 day |

- **Band overlap:** both have Coastal/Deep-Blue, Blue, Green, Red, Red Edge, NIR. WV-3 adds Yellow + NIR2 in VNIR.
- **Where each is stronger:** **WV-3 is materially superior for the thesis's core question** because its SWIR carries the diagnostic absorptions for plastics, hydrocarbons, and asbestos-cement — the only true "spectral material fingerprint" in the available data. **Pléiades Neo is the geometry/texture champion** (slightly finer native pan, 12-bit, cleaner Red Edge, faster tasking) but is VNIR-only.
- **Combination strategy:** treat **WV-3 SWIR as the spectral-evidence sensor** and **Pléiades Neo as the high-fidelity VNIR/texture sensor**; near-coincident acquisitions over the Lombardia AOI would let you test whether VNIR-only Neo can approach WV-3+SWIR performance — a clean ablation that *is* the MS-vs-RGB question, extended to "VNIR-MS vs full-MS."

---

## What this means for the thesis

- **Pléiades Neo is a VNIR-only VHR sensor.** Its "MS over RGB" gain is essentially **Red Edge (vegetation/organic separation) + 12-bit dynamics + texture from 0.3 m pan** — *not* SWIR-style material fingerprinting. Frame its added value honestly as edge/vegetation discrimination, not material spectroscopy.
- **Deep Blue adds little for materials**; do not over-claim it. Its role is atmospheric/water. Red Edge is the band to highlight.
- **Classify on native 1.2 m Bundle MS, use 0.3 m pan for texture/segmentation.** Avoid trusting pansharpened per-band radiometry for material decisions — pansharpening enhances space, not spectrum.
- **WV-3 vs Pléiades Neo becomes a built-in experiment:** "full VNIR+SWIR (WV-3)" vs "VNIR-only VHR (Neo)" directly quantifies the marginal value of SWIR for waste/asbestos material discrimination — a stronger, more defensible version of the RGB-vs-MS question.
- **Free data via ESA TPM** (proposal + quota) is the realistic acquisition path; budget 4–6 weeks lead time and write the proposal early. Airbus Applications Campus is a secondary free route.
- **Operational precedent exists but is unvalidated:** Disaitek's Neo waste tracker (~2 m² objects, "95%" vendor claim) shows feasibility but offers no public benchmark — your work could be among the first *reproducible* Neo waste/material studies.
- **Caveat the revisit:** with only 2 operational Neo satellites, "twice-daily" vendor figures overstate real tasking cadence — relevant if you need multi-temporal stacks.
- **Cross-sensor co-registration matters:** Neo (0.3 m) and WV-3 SWIR (3.7 m) differ by >10× in MS footprint; design fusion at a common analysis grid and be explicit that material spectra are sampled at the coarser (1.2 m / 3.7 m) scales.

---

**Sources:** [eoPortal – Pléiades Neo](https://www.eoportal.org/satellite-missions/pleiades-neo) · [ESA Earth Online – Pléiades Neo full archive & tasking](https://earth.esa.int/eogateway/catalog/pleiades-neo-full-archive-and-tasking) · [ESA TPM SPOT/Pléiades/Pléiades-Neo terms (PDF)](https://earth.esa.int/eogateway/documents/20142/37627/SPOT-Pleiades-data-terms-of-applicability.pdf) · [Airbus – Pléiades Neo product page](https://space-solutions.airbus.com/imagery/our-optical-and-radar-satellite-imagery/pleiades-neo/) · [Airbus case study – illegal dumping detection](https://space-solutions.airbus.com/resources/case-studies/forestry-environment/illegal-dumping-detection-monitoring/) · [Disaitek – illegal dumping](https://www.disaitek.ai/illegal-dumping) · [Airbus/SCO – urban vegetation mapping](https://space-solutions.airbus.com/resources/case-studies/pleiades-neo/pleiades-neo-space-climate-observatory-project-map-urban-vegetation/) · [UP42 – Red Edge analysis](https://up42.com/blog/pleiades-neo-in-action-analyzing-vegetation-health-using-the-new-red-edge) · [USGS – System characterization report on the Pléiades Neo Imager (OFR 2021-1030)](https://pubs.usgs.gov/publication/ofr20211030P) · [Pléiades Neo User Guide (Apollo Mapping PDF)](https://wp-cdn.apollomapping.com/web_assets/user_uploads/2021/11/08103301/2021.10_PleiadesNeo_UserGuide-EarlyRelease_20211015.pdf) · [ESA Charter Mapper – Pléiades Neo](https://docs.disasterscharter.org/missions/opt/pleiades-neo/) · [Airbus – roof health monitoring](https://space-solutions.airbus.com/resources/case-studies/pleiades-neo/monitoring-roof-health-over-time-with-pleiades-neo/) · [Airbus – research programmes](https://space-solutions.airbus.com/imagery/research-programmes/)
