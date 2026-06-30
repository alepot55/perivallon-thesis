## How to study these papers

Read for the **thesis argument**, not for completeness. The spine is one question: *what is the added value of multispectral (MS) over RGB for classifying illegal waste by material/risk at VHR?* Every paper is either evidence for, evidence against, a method, or context for that question.

- **Tiers.** Spend most time on **critical** papers (the baseline you extend, the datasets you use, the asbestos anchors, the spectral library, DOFA). **High** papers are supporting evidence you must cite by number. **Medium** papers are breadth — know the one-line role and move on.
- **For each paper extract four things:** (1) the *one headline number* (F1/OA/mAP + GSD + #bands); (2) the *method in a sentence*; (3) the *honest limit* (where exam questions live); (4) *where it sits* in the MS-vs-RGB argument.
- **Recurring through-line:** few well-chosen bands beat both RGB and full hyperspectral (cdw-2025, spectralwaste-2024, aguilar-2021); SWIR carries the C-H polymer / Mg-OH asbestos diagnostics (zhou-2021, plastics-uv-swir, emit-2025); but a no-SWIR VHR sensor reframes the work as a generalization / VNIR-sufficiency problem (saba-2026, abbasi-2024).

---

## (a) Baseline & waste detection

### Deep-learning pipeline for solid waste detection (Gibellini 2025)
- **Cite:** Gibellini, Fraternali, Boracchi, Morandini, Martinoli, Diecidue & Malegori 2025, *Waste Management Bulletin*. DOI 10.1016/j.wmb.2025.100246 · arXiv 2502.06607
- **Relevance:** critical · **Tags:** baseline, swin-t, rsp, aerialwaste
- **What it is:** End-to-end RGB pipeline (tile → Swin-T classifier → Grad-CAM → GIS) co-designed with ARPA Lombardia.
- **Why it matters:** This *is* the baseline the thesis extends to multiband.
- **Key things to remember:**
  - Best model = Swin-T + RSP + 20 cm GSD + 100 m context: **F1 92.02%, Acc 94.56%**; Swin-T > ResNet-50 everywhere.
  - 36-condition factorial: 2 archs × 3 GSD × 3 context × 2 pretrains.
  - Cross-country (Greece/Sweden/Romania) mean F1 86.92% (−5.10 pp).
  - Utility: +63.2% sites found, −60.2% area inspected at threshold 0.7.
- **Honest limit:** RGB-only — no spectral value, cannot distinguish materials; RSP gives only modest gain because its pretraining GSD mismatches the 20 cm task.

### AerialWaste dataset (Torres & Fraternali 2023)
- **Cite:** Torres & Fraternali 2023, *Scientific Data* 10:63. DOI 10.1038/s41597-023-01976-9 — real title *"AerialWaste dataset for landfill discovery in aerial and satellite images"* (corrected)
- **Relevance:** critical · **Tags:** dataset, aerialwaste, rgb
- **What it is:** First public dataset for illegal-landfill discovery; 10,434 images (v3 ~11.7k), 3 sources (AGEA 20 cm, WV-3 30 cm, Google Earth 50 cm).
- **Why it matters:** The main training dataset; defines the 22 material categories and class imbalance.
- **Key things to remember:**
  - Three annotation levels: binary scene, 22 Type-of-Object + 7 Storage-Mode labels, 169 images with 841 masks.
  - Baseline ResNet50+FPN: 87.99% AP, 80.70% F1 (94.5% AP on AGEA-only).
  - neg:pos = 2:1; built with ARPA over 487 comuni; **only 11 tiles tagged "corrugated sheets / presumed asbestos."**
- **Honest limit:** RGB-only across 3 mismatched GSDs — cannot itself test MS-vs-RGB; coordinates withheld; authors list "add NIR" as future work.

### Global dumpsite detection (Sun et al. 2023)
- **Cite:** Sun et al. 2023, *Nature Communications* 14:1444. DOI 10.1038/s41467-023-37136-1
- **Relevance:** high · **Tags:** waste, global, dumpsites
- **What it is:** First global fine-grained dumpsite dataset (~2,500 sites, 7 countries, 0.3–1 m) + BCA-Net.
- **Why it matters:** Shows DL scales globally; quantifies operational savings — motivates MS as the next step.
- **Key things to remember:** 4 dumpsite types; mean sensitivity 98.0%, precision ~70.1%; 6 days vs 6 months (−96.8% time); Global Dumpsite Index correlates with GNI.
- **Honest limit:** ~70% precision because morphology, not material, is seen; China over-represented.

### CascadeDumpNet (Zhang & Ma 2024)
- **Cite:** Zhang & Ma 2024, *Remote Sensing of Environment* 313:114349. DOI 10.1016/j.rse.2024.114349 — **two authors, NOT Marrocco/"et al."** (corrected)
- **Relevance:** high · **Tags:** dumpsite, pléiades, object-detection, automl
- **What it is:** Dual-stage CNN detection + AutoML on Pléiades 0.5 m with a Context-Fusion module.
- **Why it matters:** Newest VHR-satellite dumpsite comparator; false-alarm-suppression idea is transferable.
- **Key things to remember:** **84.6% mAP**; transfers Shenzhen → Shanghai/Guangzhou.
- **Honest limit:** Pléiades commercial VHR; object-level, no spectroscopy.

### CWLD construction-waste landfill dataset (Wang et al. 2024)
- **Cite:** Wang et al. 2024, *Scientific Data* 11. DOI 10.1038/s41597-024-03240-0
- **Relevance:** high · **Tags:** construction, dataset, gaofen, segmentation
- **What it is:** Pixel-level C&D-landfill segmentation dataset (3,653 samples) from GF-2 ~80 cm + Google Earth ~50 cm.
- **Why it matters:** Provides the per-pixel masks AerialWaste lacks for the rubble/C&D class.
- **Key things to remember:** Improved DeepLabV3+: **F1 88.9% / IoU 82%**; two Beijing districts.
- **Honest limit:** Single-region; C&D only; RGB.

### C&D debris volume from drones (2022)
- **Cite:** *Drones* 6(10):279, 2022. DOI 10.3390/drones6100279
- **Relevance:** high · **Tags:** debris, drone, fcn, volume
- **What it is:** Drone + SfM 3D reconstruction + FCN segmentation of C&D debris with volume estimation.
- **Why it matters:** Drone route for rubble with 3D volume — a capability 2D satellite detectors lack.
- **Key things to remember:** IoU 0.9 for concrete debris; adds volume, not just footprint.
- **Honest limit:** UAV close-range; RGB.

### Disaitek + Airbus Pléiades Neo tracker (2024)
- **Cite:** Disaitek / Airbus / CNES 2024 — vendor case study (grey literature)
- **Relevance:** high · **Tags:** operational, pléiades-neo, commercial
- **What it is:** Operational service on Pléiades / Pléiades Neo 30 cm detecting waste ≥2 m².
- **Why it matters:** Strongest "someone does this operationally from satellite"; market relevance.
- **Key things to remember:** ~95% reliability claim; qualifies type (ELV, construction, tyres, vegetal); CNES/Airbus agreement 27 May 2024.
- **Honest limit:** Vendor claim, no peer review or published method.

### AerialWaste lightweight/ensemble benchmark (Sharmily et al. 2025)
- **Cite:** Sharmily et al. 2025, arXiv 2508.18315 (PARTIAL — arXiv-only)
- **Relevance:** medium · **Tags:** aerialwaste, ensemble, benchmark
- **What it is:** Lightweight CNN + transformer ensembles on AerialWaste.
- **Why it matters:** Shows the field still does binary scene classification.
- **Key things to remember:** **Binary F1 92.41%**; no public move yet to per-material classification.
- **Honest limit:** Binary only; preprint.

### fCLIPSeg post-hurricane debris (2025)
- **Cite:** 2025, arXiv 2504.12542
- **Relevance:** medium · **Tags:** debris, foundation-model, clipseg
- **What it is:** Fine-tuned CLIPSeg for debris segmentation on aerial RGB.
- **Why it matters:** SAM/CLIP-family adaptation recipe for data-thin shape classes.
- **Key things to remember:** Dice 0.70; event-agnostic across three hurricanes.
- **Honest limit:** Aerial RGB, disaster debris (not illegal waste); modest Dice.

### Large-area UAV solid-waste monitoring (Liu et al. 2024)
- **Cite:** Liu et al. 2024, *Applied Sciences* 14(5):2084. DOI 10.3390/app14052084
- **Relevance:** medium · **Tags:** drone, segmentation, dual-branch
- **What it is:** Dual-branch semantic segmentation of solid-waste piles over ~450 km² UAV imagery.
- **Why it matters:** Evidence drone work treats waste as one generic "heap" class — the material gap.
- **Key things to remember:** OA >94%, recall 88.6%; no per-material breakdown.
- **Honest limit:** Single generic pile class; UAV.

### Tisza waste detection & change (Magyar et al. 2023)
- **Cite:** Magyar, Cserep, Vincellér & Molnár 2023, arXiv 2303.14521
- **Relevance:** medium · **Tags:** change-detection, sentinel-2, planetscope
- **What it is:** RF on Sentinel-2 (13 b) + PlanetScope (4 b, 3 m) for dump hotspots & floating-waste barriers on the Tisza.
- **Why it matters:** Classic ML on MS reaches high accuracy; NIR is the key band — but only for large accumulations.
- **Key things to remember:** ~96% CV accuracy; Plastic Index PI = NIR/(NIR+Red) cardinal; detection floor ~30 m².
- **Honest limit:** At 10–30 m, works only on dense accumulations >100 m²; no spectroscopy.

### Heavy-duty truck detection from satellite (2025)
- **Cite:** 2025, PMC12302943 (open access)
- **Relevance:** medium · **Tags:** vehicles, containers, object-detection
- **What it is:** CenterNet + Mask R-CNN ensemble classifying container size/status and trucks.
- **Why it matters:** Per-class anchor (containers/trucks by shape); flags the absent ELV detector.
- **Honest limit:** Objects, not material; no ELV class.

### Well pads & storage tanks (Ramachandran et al. 2024)
- **Cite:** Ramachandran, Irvin, Omara, Ng & Jackson 2024, *Nature Communications* 15. DOI 10.1038/s41467-024-50334-9
- **Relevance:** high · **Tags:** tanks, object-detection, large-scale
- **What it is:** DL mapping of >169k storage tanks and >70k well pads across US basins.
- **Why it matters:** SOTA tank detection at sub-metre VHR — comparator for the cistern class.
- **Key things to remember:** Tanks **P 0.962 / R 0.968**; continental scale.
- **Honest limit:** Shape-based; no material discrimination.

### YOLOv7-OT storage tanks (2024)
- **Cite:** 2024, *Remote Sensing* 16(23):4510. DOI 10.3390/rs16234510
- **Relevance:** high · **Tags:** tanks, yolo, object-detection
- **What it is:** YOLOv7 + CBAM tank detector with edge re-stitching.
- **Why it matters:** Confirms tanks are a well-served object class, not a gap.
- **Key things to remember:** 90% accuracy / 95.9% precision.
- **Honest limit:** Shape-based; not material/risk.

### Hybrid-YOLOv5 non-ferrous metals in ELVs (2025)
- **Cite:** 2025, *Scientific Reports* 15. DOI 10.1038/s41598-025-02683-8
- **Relevance:** medium · **Tags:** scrap, metal, elv, close-range
- **What it is:** Close-range IR detection of copper/aluminium/steel in end-of-life vehicles.
- **Why it matters:** Documents the scrap-composition gap and the object-vs-material boundary.
- **Key things to remember:** 84.2% mAP; **NOT remote sensing** — needs spectrum / close range.
- **Honest limit:** Close-range IR, not VHR satellite.

## (b) Asbestos & roof material

### Asbestos rooftops from EnMAP (Shepherd et al. 2025)
- **Cite:** Shepherd, **Sagi**, Zagron & Ben-Dor 2025, *Scientific Reports* 15:24166. DOI 10.1038/s41598-025-09738-w (2nd author corrected to Sagi)
- **Relevance:** critical · **Tags:** enmap, hyperspectral, sam, satellite
- **What it is:** Spaceborne HSI AC-roof mapping (EnMAP 230 bands, 30 m) with field-spectra calibration + 8-classifier cascade.
- **Why it matters:** The most direct satellite justification for the asbestos pilot; the HSI upper bound.
- **Key things to remember:** **86% positive-match** vs GT; best single classifier ACE 91.4% OA, κ=0.87; 2,714 field spectra; "6-of-8" consensus.
- **Honest limit:** 30 m → mixed-pixel errors (rubble/paint mimic asbestos); calibrated to semi-arid Negev; heavy manual curation; **30 m is out of VHR scope.**

### Python AC-roof mapping workflow (Bonifazi et al. 2026)
- **Cite:** Bonifazi, Aurigemma, Salas-Cáceres, Lorenzo-Navarro, Serranti, Paglietti, Bellagamba & Malinconico 2026, *Geomatics* 6(3):41. DOI 10.3390/geomatics6030041
- **Relevance:** critical · **Tags:** wv-3, vnir, python, open-source, multi-temporal
- **What it is:** Open-source Python workflow (Py6S → MLC → building aggregation) for AC detection + temporal monitoring on WV-3 over Mantova.
- **Why it matters:** Most recent, reproducible, directly comparable; the technical stack to reuse.
- **Key things to remember:** 16 WV-3 bands (VNIR 1.24 m + SWIR 3.7 m → resampled 1 m); **F1 0.87 at 30% threshold**; multi-temporal caught 46.6% of 133 registered removals.
- **Honest limit:** A *screening* tool (needs field verification); thresholds Mantova-specific.

### AC roofs + weathering from MIVIS (Cilia et al. 2015)
- **Cite:** Cilia, Panigada, Rossini, Candiani, Pepe & Colombo 2015, *ISPRS Int. J. Geo-Information* 4(2):928–941. DOI 10.3390/ijgi4020928
- **Relevance:** high · **Tags:** hyperspectral, mivis, sam, weathering, italian
- **What it is:** Airborne MIVIS (102 bands, 3 m) SAM classification of AC roofs in Brianza + a deterioration index (ISD).
- **Why it matters:** Foundational Italian AC reference; SAM + endmember + deterioration-index workflow + cadastre integration.
- **Key things to remember:** 2-step SAM PA 89% / UA 86%; 3,170 AC roofs; ISD built on chlorophyll (moss/lichen), not fibre release.
- **Honest limit:** ISD is a vegetal-colonisation proxy, not fibre hazard; 3 m excludes roofs <36 m²; airborne not scalable.

### Asbestos from WV-3 VNIR, 8 bands (Saba et al. 2026)
- **Cite:** Saba et al. 2026, *Journal of Hazardous Materials* 508:141864. DOI 10.1016/j.jhazmat.2026.141864
- **Relevance:** high · **Tags:** wv-3, vnir, classification
- **What it is:** 32 classifiers on WV-3's 8 VNIR bands for AC-roof classification.
- **Why it matters:** Strongest evidence that **VNIR-only suffices** for asbestos at fine VHR — central to the no-SWIR framing.
- **Key things to remember:** Fine-KNN Macro-F1 97.6%; binary AC ~99–100%; red-edge & NIR drive it; GSD 1.24 m.
- **Honest limit:** WV-3 VNIR at 1.24 m (not SuperDove 3 m); classifier zoo, single region.

### Multi-temporal asbestos change detection (Abbasi et al. 2024)
- **Cite:** Abbasi et al. 2024, *Remote Sensing Applications: Society and Environment*. DOI 10.1016/j.rsase.2024.101167
- **Relevance:** high · **Tags:** aerial, obia, deep-learning, no-swir
- **What it is:** Nearmap aerial VHR (no SWIR) + DenseNet121 + LSTM/Conv1D multi-temporal AC detection.
- **Why it matters:** Counter-evidence that asbestos is detectable at fine VHR by shape + temporal cues *without SWIR*.
- **Key things to remember:** OA 95.8–96.0%, AC 94%; temporal stacking compensates for missing bands.
- **Honest limit:** Needs multi-temporal aerial; RGB-only; no spectral proof.

### Asbestos slate drone training-data model (2023)
- **Cite:** 2023, PMC10575463 (open access)
- **Relevance:** medium · **Tags:** drone, rgb, training-data
- **What it is:** A DL training-data model from drone RGB of asbestos slate roofs.
- **Why it matters:** Drone-RGB asbestos route; documents the annotation bottleneck.
- **Honest limit:** UAV RGB, no spectral confirmation; annotation-heavy.

## (c) Plastics & spectral signatures

### USGS Spectral Library v7 / splib07a (Kokaly et al. 2017)
- **Cite:** Kokaly et al. 2017, *USGS Data Series 1035*. Report DOI 10.3133/ds1035 · data DOI 10.5066/F7RR1WDJ
- **Relevance:** critical · **Tags:** signature-library, usgs
- **What it is:** The world reference spectral library: ~2,400 signatures, 350–2500 nm, 2,151 channels, with sensor-convolved subsets (S2, WV-3).
- **Why it matters:** Source for the spectral-signature figures and endmembers; the lab-to-sensor bridge.
- **Key things to remember:** Covers polymers, AC/chrysotile, construction materials; local copy in `spectral/`; no-data sentinel **−1.23e+34**; convolved S2 (13 b) & WV-3 (16 b) subsets.
- **Honest limit:** Ideal lab conditions — real scenes need atmospheric correction, BRDF, continuum removal, mixed-pixel handling.

### Knowledge-based aliphatic/aromatic plastic classifier (Zhou et al. 2021)
- **Cite:** Zhou, Kuester, Bochow, Bohn, Brell & Kaufmann 2021, *Remote Sensing of Environment*. DOI 10.1016/j.rse.2021.112598
- **Relevance:** high · **Tags:** wv-3, swir, aliphatic-aromatic, classifier
- **What it is:** Training-free decision-tree classifier using C-H features in WV-3's 8 narrow SWIR bands.
- **Why it matters:** Explains *why narrow SWIR (WV-3) resolves PE vs PET and broad S2 B11/B12 does not* — the band-width argument.
- **Key things to remember:** 3 polymer clusters; producer accuracy >80% aliphatic-vs-aromatic; validated lab → airborne → WV-3.
- **Honest limit:** Thresholds need per-sensor re-calibration; does not transfer to no-SWIR sensors; weak field truth.

### Macroplastics mapping with WV-3 SWIR (Aguilar et al. 2025)
- **Cite:** Aguilar, Sousa, Uhrin, Gudino-Elizondo & Biggs 2025, *Environmental Monitoring and Assessment*. DOI 10.1007/s10661-025-14125-z
- **Relevance:** high · **Tags:** wv-3, swir, plastic, high-resolution
- **What it is:** Matched-filter mapping of terrestrial macroplastics with WV-3 SWIR (8 b, 3.7 m) + lab reflectance.
- **Why it matters:** Lab signatures transfer to satellite in the SWIR; WV-3 as the material gold standard at VHR.
- **Key things to remember:** Precision 92.5% (95.3% high-confidence); lab-to-image r=0.95; smallest detected 80–150 m².
- **Honest limit:** Matched filter favours large homogeneous instances; "polymer-coated" paints indistinguishable from plastic; arid-context only.

### Normalized Difference Plastic Index / NDPI (Guo & Li 2020)
- **Cite:** Guo & Li 2020, *ISPRS J. Photogrammetry & Remote Sensing*. DOI 10.1016/j.isprsjprs.2020.09.009
- **Relevance:** high · **Tags:** wv-3, swir, spectral-index, ndpi
- **What it is:** Defines NDPI, a SWIR band-ratio index on WV-3 for urban plastic quantification.
- **Why it matters:** Origin of the single most predictive feature in WV-3 plastic ablations.
- **Key things to remember:** NDPI uses C-H absorptions (~1.57/1.73 µm); top single feature (drives the 96.79% SWIR-only OA in Aguilar 2021).
- **Honest limit:** Closed-access (details *unverified*); SWIR-dependent, no transfer to SuperDove.

### Global plastic detection with EMIT (Estrela et al. 2025)
- **Cite:** Estrela et al. 2025, *Geophysical Research Letters* 52:e2024GL112416. DOI 10.1029/2024GL112416
- **Relevance:** high · **Tags:** plastic, hyperspectral, emit, global-scale
- **What it is:** First continental-scale HDPE/PVC detection from orbit (EMIT, 285 b, 60 m) via SWIR matched filtering.
- **Why it matters:** Confirms polymer signatures are orbit-detectable *when SWIR is available*.
- **Key things to remember:** Absorption centres 1215/1417/1732/2313 nm; gypsum FP-rejection at 2200 nm; hotspots Spain/Sicily/Mexico/Taiwan.
- **Honest limit:** 60 m → mostly sub-pixel; low-contrast polymers under-represented; buried landfills missed.

### UV–SWIR plastic spectral library (Knaeps et al. 2020)
- **Cite:** Knaeps et al. 2020, *Earth System Science Data* 12:77. DOI 10.5194/essd-12-77-2020
- **Relevance:** high · **Tags:** plastic, hyperspectral, uv-swir, signature-library
- **What it is:** Open ASD FieldSpec library of virgin/marine/washed-ashore plastics, 350–2500 nm.
- **Why it matters:** Physical basis for plastic-detection figures; endmembers for matching/mixing.
- **Key things to remember:** 8 diagnostic absorptions; **1215 and 1732 nm** most robust; wetting attenuates SWIR up to 90% but preserves shape.
- **Honest limit:** Lab-equivalent, white-plastic bias; submerged plastic collapses NIR/SWIR.

### MARIDA marine-debris benchmark (Kikaki et al. 2022)
- **Cite:** Kikaki et al. 2022, *PLOS ONE* 17(1):e0262247. DOI 10.1371/journal.pone.0262247
- **Relevance:** high · **Tags:** marine-debris, sentinel-2, benchmark
- **What it is:** First public pixel-level S2 marine-debris benchmark (1,381 patches, 15 classes).
- **Why it matters:** Most-cited MS waste benchmark; shows SWIR value and the 10 m resolution ceiling.
- **Key things to remember:** RF F1 ~0.79; separability rides on 865 nm + SWIR B11/B12; removing SWIR degrades it.
- **Honest limit:** At 10 m, debris is sub-pixel and confuses with vegetation/foam; learns regional distributions.

### Cross-domain UAV-SWIR plastic segmentation (2026)
- **Cite:** 2026, *Remote Sensing* 18(1):182. DOI 10.3390/rs18010182
- **Relevance:** high · **Tags:** drone, swir, hyperspectral, u-net, generalization
- **What it is:** Attention-gated residual U-Net on UAV hyperspectral SWIR (900–1700 nm).
- **Why it matters:** Polymer-type ID needs SWIR; also an OOD/generalization datapoint.
- **Key things to remember:** 96.8% acc / 91.1% F1; driven by 1215 & 1732 nm.
- **Honest limit:** UAV HSI, not satellite; cross-domain still data-bound.

### UAV + IoT river-plastic detection (2025)
- **Cite:** 2025, *Journal of Hazardous Materials Advances*. DOI 10.1016/j.hazadv.2025.100348
- **Relevance:** medium · **Tags:** plastic, drone, iot, edge
- **What it is:** On-board edge UAV detector for river plastic (Bogor, Indonesia).
- **Why it matters:** Drone-RGB plastic-presence route.
- **Key things to remember:** 92% accuracy; plastic by appearance, not polymer spectrum.
- **Honest limit:** RGB presence only; UAV.

## (d) Sensors, datasets & ablation

### WV-3 VNIR vs SWIR greenhouse ablation (Aguilar et al. 2021)
- **Cite:** Aguilar, Jiménez-Lao & Aguilar 2021, *Remote Sensing* 13(11):2133. DOI 10.3390/rs13112133
- **Relevance:** critical · **Tags:** wv-3, vnir, swir, ablation, methodology-canonical
- **What it is:** Three-way OBIA ablation (VNIR / SWIR / All) for plastic-covered greenhouse mapping in Almería.
- **Why it matters:** The canonical "spectral added value" template — the exact framing the thesis adopts.
- **Key things to remember:** **OA 90.85 (VNIR) / 96.79 (SWIR) / 97.38 (All)**; NDPI top SWIR feature; 16 WV-3 bands.
- **Honest limit:** Material is *plastic*, not asbestos — transferable methodology, not an AC substitute; whitewash masks the SWIR signature.

### Critical wavelengths for C&D waste (Vitek et al. 2025)
- **Cite:** Vitek, Zbiral & Nezerka 2025, *Resources, Conservation & Recycling*. DOI 10.1016/j.resconrec.2025.108123 · arXiv 2501.02239
- **Relevance:** medium · **Tags:** construction-demolition, wavelengths, band-selection
- **What it is:** HSI (768 bands, 400–1000 nm) band-selection over 10 C&D materials.
- **Why it matters:** The "few bands suffice" argument — motivation for MS over both RGB and full HSI.
- **Key things to remember:** **RGB + 2 NIR bands ≈ full 768-band HSI** (0.96 vs 0.87 RGB-only); optimal extra bands ~650–750 + ~850–1000 nm; whole-spectrum features *degrade* the model.
- **Honest limit:** Controlled lab, clean samples — needs re-calibration for outdoor/satellite; concrete stays hardest.

### SpectralWaste dataset (Casao et al. 2024)
- **Cite:** Casao, Peña, Sabater et al. 2024, arXiv 2403.18033
- **Relevance:** medium · **Tags:** dataset, hyperspectral, sorting, multimodal
- **What it is:** First RGB + HSI (224 bands, 900–1700 nm) dataset from a real sorting plant, with SAM label transfer.
- **Why it matters:** RGB+spectral fusion beats either modality — supports late fusion.
- **Key things to remember:** CMX RGB+HSI mIoU 58.2% vs 48.4% RGB vs 54.3% HSI; HSI wins big on thin classes.
- **Honest limit:** Controlled conveyor; SWIR stops at 1700 nm; 6 imbalanced classes.

## (e) Foundation models & methods

### DOFA — wavelength-conditioned foundation model (Xiong et al. 2024)
- **Cite:** Xiong et al. 2024, *DOFA: Neural Plasticity-Inspired Multimodal Foundation Model for EO*, arXiv 2403.15356
- **Relevance:** critical · **Tags:** dofa, cross-modal, any-bands
- **What it is:** A dynamic hypernetwork conditioned on each band's centre wavelength that generates patch-embedding weights — sensor-agnostic.
- **Why it matters:** **SuperDove/WV-3/PNeo-ready** (feed centre wavelengths, no retraining) — the structurally-fair ablation spine.
- **Key things to remember:** Pretrained MIM on 5 modalities (S1/S2/Gaofen/NAIP/EnMAP); Base 86M / Large 300M; in TorchGeo.
- **Honest limit:** High-res pretraining thin (NAIP 1 m RGB only); SuperDove's Coastal/Yellow/RedEdge may be under-represented; not a guaranteed cross-sensor fix.

### SatMAE (Cong et al. 2022)
- **Cite:** Cong et al. 2022, NeurIPS, arXiv 2207.08051
- **Relevance:** high · **Tags:** multispectral, pretraining, mae
- **What it is:** MAE adapted to satellite via band grouping + spectral positional encoding.
- **Why it matters:** Historical baseline; quantifies RGB→MS transfer gain.
- **Key things to remember:** +14% transfer on EuroSAT vs ImageNet; EuroSAT 98.98%.
- **Honest limit:** Rigid grouping needs per-sensor re-adapting; 10/20 m only.

### SpectralGPT (Hong et al. 2024)
- **Cite:** Hong et al. 2024, IEEE TPAMI 46(8):5227–5244. DOI 10.1109/TPAMI.2024.3362475 · arXiv 2311.07113
- **Relevance:** high · **Tags:** spectral, 3d-transformer, foundation-model
- **What it is:** Spectral FM with 3D spectral masking, up to 600M params.
- **Why it matters:** Opposite philosophy to DOFA — deep 3D modelling vs sensor flexibility.
- **Honest limit:** Locked to S2 12-band; 8-band SuperDove needs redesign + re-pretrain; tested only on land-cover.

### Prithvi-EO-2.0 (Szwarcman et al. 2024)
- **Cite:** Szwarcman et al. 2024, arXiv 2412.02732
- **Relevance:** high · **Tags:** nasa-ibm, multi-temporal, mae
- **What it is:** 3D MAE on 4.2M HLS samples at 30 m, 6 fixed bands incl. SWIR1/SWIR2; ViT-L/H.
- **Why it matters:** Backbone with *native SWIR* and multi-temporal support.
- **Key things to remember:** 75.6% mean on GEO-Bench (+8 pp vs Prithvi-1.0).
- **Honest limit:** 6 fixed bands; 30 m → 10× GSD gap to SuperDove; weak candidate here.

### SSL4EO-S12 (Wang et al. 2023)
- **Cite:** Wang et al. 2023, arXiv 2211.07044
- **Relevance:** high · **Tags:** ssl, sentinel-1-2, dataset
- **What it is:** 3M-patch S1/S2 SSL dataset + benchmark across all 13 S2 bands.
- **Why it matters:** Most practical S2 starting point — ready 13-band weights.
- **Key things to remember:** SSL beats ImageNet ~10% in linear probe.
- **Honest limit:** Checkpoint collection, rigid sensors; SuperDove's Yellow 612 nm has no S2 analogue; 3 m unseen.

### SoftCon (Wang et al. 2024)
- **Cite:** Wang et al. 2024, arXiv 2405.20462
- **Relevance:** high · **Tags:** contrastive, multilabel, continual-pretrain
- **What it is:** Soft multi-label contrastive continual-pretraining from DINOv2, random-init first layer for mismatched bands.
- **Why it matters:** Proof that "random-init first layer + strong backbone" is a cheap, solid adaptation for 8 bands.
- **Key things to remember:** ViT-B SOTA (86.8 on BigEarthNet-10%); wins 10/11 downstream.
- **Honest limit:** Soft labels noisy; locked to S2 13-band; LULC labels too coarse for material.

### AnySat (Astruc et al. 2025)
- **Cite:** Astruc et al. 2025, CVPR 2025, arXiv 2412.14123
- **Relevance:** high · **Tags:** any-resolution, any-modality, jepa
- **What it is:** JEPA multimodal model + scale-adaptive patch encoder for any resolution/scale/modality.
- **Why it matters:** Direct DOFA alternative; SuperDove's 3 m is inside its pretrain range.
- **Honest limit:** Modest pretrain scale; no 8-band VNIR sensor seen → SuperDove stays OOD (fine-tune only).

### Resizing & normalization matters (Corley et al. 2024)
- **Cite:** Corley, Robinson, Dodhia, Lavista-Ferres & Najafirad 2024, CVPR-W (PBVS), arXiv 2305.13456
- **Relevance:** high · **Tags:** benchmark, normalization, preprocessing
- **What it is:** Shows preprocessing (resize to 224, channel-wise normalization) often dominates the choice of pretraining.
- **Why it matters:** Mandatory fairness guardrail for the MS-vs-RGB comparison.
- **Key things to remember:** Resize to 224 → +11.16% EuroSAT, +32.28% So2Sat; ImageNet (preprocessed correctly) rivals RS-SSL.
- **Honest limit:** Benchmarks pad extra channels rather than testing real band-config shift; no GSD-shift study.

### DEFLECT — PEFT for new channels (Thoreau et al. 2025)
- **Cite:** Thoreau, Marsocci & Derksen 2025, ICCV 2025, arXiv 2503.09493
- **Relevance:** medium · **Tags:** parameter-efficient, multispectral-adapter, peft
- **What it is:** Adapter extending a ViT to new channels with <1% extra params.
- **Why it matters:** Efficient alternative to weight-inflation/random-init if GPU-bound; plugs on DOFA/Prithvi.
- **Key things to remember:** On par with full fine-tune at 5–10× fewer params.
- **Honest limit:** Value depends on the base GFM; needs explicit band indices; not tested on 8-band sensors.

## (f) Generalization, surveys & context

### PoliMi waste-detection survey (Fraternali et al. 2024)
- **Cite:** Fraternali, Morandini & Herrera González 2024, *Waste Management* 189:88–102. DOI 10.1016/j.wasman.2024.08.003 · arXiv 2402.09066
- **Relevance:** critical · **Tags:** survey, gap-analysis
- **What it is:** Systematic PRISMA survey of 50 RS waste-detection works (1987–2023).
- **Why it matters:** The thesis rationale — names the RGB limitation and material-classification gap.
- **Key things to remember:** 1,235→50 papers; only 11/50 use DL, nearly all RGB; declared gaps: no benchmark, weak generalization, **material identification unaddressed (needs ≤30 cm + MS)**, FMs unexplored.
- **Honest limit:** A taxonomy survey, not quantitative.

### FM for Remote Sensing survey (2024)
- **Cite:** Xiao et al. 2024/2025, IEEE GRSM, arXiv 2410.16602
- **Relevance:** high · **Tags:** foundation-model, survey
- **What it is:** Taxonomy of 30+ RS foundation models with pretrain-dataset tables.
- **Why it matters:** Related-work scaffold to position DOFA/AnySat (SatMAE→SpectralGPT→DOFA→AnySat).
- **Honest limit:** Coverage stops ~Q3 2024; no unified benchmark; doesn't address 8-band sensors.

### Waste RS survey — object-vs-material framing (2024)
- **Cite:** Fraternali, Morandini & Herrera González 2024, *Waste Management* 189:88–102 (published version; object-vs-material angle)
- **Relevance:** high · **Tags:** survey, gap-analysis, object-vs-material
- **What it is:** Catalogues what RS detects vs what is absent.
- **Why it matters:** Independent verification of the per-class gaps and the object-vs-material distinction.
- **Key things to remember:** **No detectors for foundry slag, sludge, big bags, scrap composition.**
- **Honest limit:** Same paper as the survey above (kept separate for the 13-class cross-check).

### AI-drone waste-management review (2025)
- **Cite:** 2025, *Drones* 9(8):550. DOI 10.3390/drones9080550
- **Relevance:** medium · **Tags:** drone, survey, yolo
- **What it is:** PRISMA review of ~10 UAV+DL waste studies.
- **Why it matters:** Cross-check the drone side of the per-class table.
- **Key things to remember:** YOLO dominant (YOLOv8 ~97% acc for dumps); thin per class.
- **Honest limit:** Small corpus; UAV-only; RGB.

### Vehicle detection with domain adaptation (Koga et al. 2020)
- **Cite:** Koga, Miyazaki & Shibasaki 2020, *Remote Sensing* 12(3):575. DOI 10.3390/rs12030575
- **Relevance:** medium · **Tags:** vehicles, object-detection, domain-adaptation
- **What it is:** Region-based vehicle detector on 30–50 cm VHR with CORAL + adversarial unsupervised domain adaptation.
- **Why it matters:** Object anchor for vehicles **and** a label-free cross-region generalization technique.
- **Key things to remember:** Domain adaptation gives +10% in the target domain without labels.
- **Honest limit:** RGB shape-based; vehicles, not waste material.

---

## Master table — all 47 papers

| Citekey | Year | Relevance | One-line role |
|---|---|---|---|
| gibellini-2025-pipeline | 2025 | critical | Swin-T+RSP RGB baseline (F1 92.02%) the thesis extends |
| torres-2023-aerialwaste | 2023 | critical | AerialWaste — the main RGB training dataset (22 classes) |
| global-dumpsites-2023 | 2023 | high | Global VHR dumpsite detection + socioeconomic factors |
| cascadedumpnet-2024 | 2024 | high | Pléiades 0.5 m dual-stage dumpsite detector (84.6% mAP) |
| cwld-2024 | 2024 | high | Beijing C&D-landfill pixel-level VHR dataset (F1 88.9%) |
| cd-debris-drone-2022 | 2022 | high | Drone+SfM 3D C&D debris segmentation & volume |
| disaitek-airbus-pleiades-neo-2024 | 2024 | high | Operational Pléiades Neo waste service (vendor, ~95%) |
| ramachandran-2024-tanks-wellpads | 2024 | high | SOTA VHR storage-tank/well-pad detection (P 0.962) |
| yolov7ot-tanks-2024 | 2024 | high | YOLOv7-OT tank detector (95.9% precision) |
| aerialwaste-ensemble-2025 | 2025 | medium | Lightweight/ensemble benchmark on AerialWaste (F1 92.41%) |
| fclipseg-debris-2025 | 2025 | medium | Fine-tuned CLIPSeg for debris (Dice 0.70) |
| uav-solidwaste-2024 | 2024 | medium | Dual-branch UAV waste-pile segmentation (OA >94%) |
| tisza-2023-waste-change | 2023 | medium | RF on S2/PlanetScope river-waste change detection (~96%) |
| heavyduty-truck-satellite-2025 | 2025 | medium | Satellite truck/container detection; flags ELV gap |
| hybrid-yolov5-elv-2025 | 2025 | medium | Close-range IR scrap-metal in ELVs; material-gap evidence |
| shepherd-2025-asbestos-enmap | 2025 | critical | EnMAP 30 m hyperspectral asbestos (86% match) — HSI upper bound |
| bonifazi-2026-ac-python | 2026 | critical | Open-source WV-3 AC mapping workflow (F1 0.87) |
| cilia-2015-ac-weathering | 2015 | high | MIVIS airborne AC + deterioration index (PA 89%) |
| saba-2026-asbestos-wv3-vnir | 2026 | high | WV-3 VNIR-only asbestos (Macro-F1 97.6%) — no-SWIR evidence |
| abbasi-2024-asbestos-changedetection | 2024 | high | Aerial VHR + temporal asbestos without SWIR (OA ~96%) |
| asbestos-slate-drone-2023 | 2023 | medium | Drone-RGB asbestos slate training-data model |
| kokaly-2017-splib07a | 2017 | critical | USGS reference spectral library (350–2500 nm) |
| zhou-2021-plastic-classifier | 2021 | high | WV-3 SWIR knowledge-based aliphatic/aromatic plastic classifier |
| aguilar-2025-macroplastics-wv3 | 2025 | high | WV-3 SWIR matched-filter macroplastics (P 92.5%) |
| guo-li-2020-ndpi-wv3 | 2020 | high | NDPI spectral index for WV-3 plastic (closed-access) |
| emit-2025-plastic | 2025 | high | EMIT 60 m global HDPE/PVC detection from orbit |
| plastics-uv-swir-2020 | 2020 | high | UV–SWIR plastic spectral library (diagnostic bands) |
| marida-2022-marine-debris | 2022 | high | S2 pixel-level marine-debris benchmark (RF F1 ~0.79) |
| plastic-uav-swir-2026 | 2026 | high | UAV-SWIR plastic segmentation (F1 91.1%) + OOD datapoint |
| plastic-uav-iot-2025 | 2025 | medium | Edge UAV river-plastic presence detection (92%) |
| aguilar-2021-wv3-ablation | 2021 | critical | Canonical VNIR/SWIR/All ablation (OA 90.85/96.79/97.38) |
| cdw-2025-critical-wavelengths | 2025 | medium | "RGB+2 NIR bands ≈ full HSI" band-selection for C&D |
| spectralwaste-2024-dataset | 2024 | medium | RGB+HSI sorting dataset; fusion > single modality |
| xiong-2024-dofa | 2024 | critical | Wavelength-conditioned FM — SuperDove/WV-3/PNeo-ready |
| cong-2022-satmae | 2022 | high | MAE + band grouping; historical MS-FM baseline |
| spectralgpt-2024 | 2024 | high | 3D spectral FM (S2-locked, 600M) |
| szwarcman-2024-prithvi-eo2 | 2024 | high | NASA/IBM 30 m multi-temporal FM with native SWIR |
| wang-2023-ssl4eo-s12 | 2023 | high | S1/S2 SSL dataset + 13-band pretrained weights |
| wang-2024-softcon | 2024 | high | Soft-contrastive continual pretrain; random-init first layer |
| anysat-2024 | 2025 | high | JEPA any-resolution/modality FM (DOFA alternative) |
| corley-2024-resizing | 2024 | high | Preprocessing dominates RS benchmarks — fairness guardrail |
| thoreau-2025-deflect | 2025 | medium | PEFT adapter for new channels (<1% params) |
| fraternali-2024-survey | 2024 | critical | PoliMi waste survey — names the RGB/material gap |
| fm-rs-survey-2024 | 2024 | high | Taxonomy of 30+ RS foundation models |
| waste-rs-survey-2024 | 2024 | high | Published waste survey — object-vs-material gap catalogue |
| uav-waste-review-2025 | 2025 | medium | PRISMA review of UAV+DL waste studies (YOLO-dominant) |
| vehicle-detection-da-2020 | 2020 | medium | VHR vehicle detector + unsupervised domain adaptation (+10%) |
