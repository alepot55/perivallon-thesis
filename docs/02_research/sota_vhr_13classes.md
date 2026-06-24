# SOTA — detecting Thomas's 13 waste/material classes from 30–50 cm VHR satellite (+ drone)

*Re-scoped research, 2026-06-23. Companion to the literature matrix already drafted. This is the **correct** operating point: input = VHR 30–50 cm SATELLITE imagery (WorldView-2/3, Pléiades / Pléiades Neo, GeoEye-1, SuperView, Gaofen, SkySat); spatial resolution is the priority, spectral/SWIR is secondary. Sentinel-2 (10 m) and EnMAP/PRISMA (30 m) are out of scope and appear only as the SWIR upper bound.*

Built by merging the first literature matrix with a second deep-research pass (5 search angles, 29 sources, adversarial verification — key claims confirmed HIGH confidence; raw verified claims in the run journal). **[NEW]** = surfaced/confirmed in the June-2026 pass, beyond the first matrix.

---

## 1. The one framing that governs everything: object vs material

At 30–50 cm broadband VNIR (no SWIR), a class is feasible if its **identity lives in shape/context**, and weak if its identity lives in **spectral chemistry**.

- **Object/shape classes — detectable at 30–50 cm:** vehicles, tanks/cisterns, containers, rubble/C&D heaps, bulky items, firewood, tires, big bags.
- **Material/spectral classes — weak at broadband VHR, need SWIR or finer GSD:** asbestos-cement, plastic polymer type, foundry slag, sludge composition, scrap-metal composition.

This split is confirmed independently by the *Waste Management* 2024 survey (Solid waste detection in RS: a survey) and by the Gibellini-2025 literature review.

---

## 2. The anchors (verified) — "is anyone doing this with satellite?"

| Work | Platform / GSD | Method | Result | Note |
|---|---|---|---|---|
| **Gibellini et al. 2025** (Waste Management Bulletin; arXiv 2502.06607) | VHR <50 cm (AGEA 20 cm, WV-3 30 cm, GE 50 cm) | **Swin-T + RSP**, binary waste/no-waste scene classifier | **F1 92.02%, Acc 94.56%**; −5.1% F1 cross-region | The thesis baseline. Swin-T > ResNet-50. **[verified from PDF]** |
| **AerialWaste** (Torres & Fraternali 2023) | WV-3 0.3 m + GE 0.5 m + AGEA 0.2 m | ResNet-50+FPN scene class. + object/segmentation labels | binary AP 87.99% (full) / 94.5% (0.2 m) | the dataset; carries the 13-class object labels |
| **[NEW] CascadeDumpNet** (Remote Sensing of Environment 313, 2024) | **Pléiades 0.5 m** | dual-stage CNN object detection + AutoML, Context-Fusion module | **84.6% mAP**, transferable Shenzhen→Shanghai/Guangzhou | newer than Sun-2023; cuts false alarms via context **[verified HIGH]** |
| **Sun et al. 2023** (Nature Communications 14:1444) | Gaofen/SuperView 0.3–1 m | CNN + Blocked Channel Attention | ~1000 dumpsites, 28 cities/15 countries; −96.8% time | global dumpsite scene detection |
| **[NEW] AerialWaste ensemble benchmark** (arXiv 2508.18315, Aug 2025) | AerialWaste VHR | lightweight CNN + transformer ensemble | binary F1 92.41% | confirms field still does binary, not 13-class |
| **[NEW] Disaitek + Airbus Pléiades Neo** (operational, CNES/Airbus agreement 27 May 2024) | **Pléiades / Pléiades Neo 30 cm** | AI semantic segmentation | detects waste ≥**2 m²** at **~95%** reliability; **qualifies type: end-of-life vehicles, construction waste, tires, vegetal waste** | the strongest "someone does this operationally from satellite", covers classes #1/#3/#12. Vendor claim, not peer-reviewed |
| **[NEW] European Space Imaging / SZTAKI** | GeoEye-1, WV-2, WV-3 (30–50 cm) | CNN encoder-decoder semantic segmentation (FCN/U-Net) | ~90% landfill detection | grey-literature; per-material left as future work |

**Common message:** every VHR-satellite waste system today detects **aggregate dumpsites / binary "waste"**, by shape+context — *none* does per-class material classification of the 13 classes. That empty cell is the thesis space.

---

## 3. Per-class verdict (the core table)

S = satellite, D = drone. ✓ served · ◐ partial/morphological-only · ✗ essentially no dedicated literature (gap).

| # | Class | S | D | Best evidence / method / GSD / accuracy | Verdict at 30–50 cm |
|---|---|:--:|:--:|---|---|
| 1 | **Rubble / C&D debris** | ✓ | ✓ | S: **[NEW] CWLD** GF-2 80 cm + GE 50 cm, improved DeepLabV3+ seg, **F1 88.9% / IoU 82%** (Beijing 2024); Yong DeepLabv3+ 1 m, F1 77.4%; Disaitek "construction waste" 30 cm. D: **[NEW]** FCN + SfM drone, **IoU 0.9** concrete + volume | strong — heap morphology |
| 2 | **Foundry waste / slag** | ✗ | ✗ | only AerialWaste annotation (9 labels); composition = close-range hyperspectral (EJRS 2015) | **GAP** (spectral + data-starved) |
| 3 | **Vehicles / ELV** | ✓ | ✓ | S: region-based detector + domain adaptation (RS 12:575, +10%); heavy-duty truck classify (PMC 2025); Disaitek "end-of-life vehicles" 30 cm | excellent — object. *Generic* vehicles mature; ELV-scrapyard-specific is a sub-gap |
| 4 | **Scrap metal** | ◐ | ✗ | scrapyard *scenes* in AerialWaste (167 labels); composition = close-range IR (**[NEW]** Hybrid-YOLOv5 ELV non-ferrous 84.2% mAP, *not* RS) | scene-detectable; **metal type = GAP** |
| 5 | **Bulky items** | ✓ | ◐ | AerialWaste 286 labels (2nd most frequent); **[NEW]** UAV ~450 km² dual-branch seg >94% OA (generic "solid waste pile") | good — object; no per-type split |
| 6 | **Containers / skips** | ✓ | — | CenterNet+Mask R-CNN container detection (PMC); Satellogic ~90% counting @0.7 m; AerialWaste 167 labels | strong — object |
| 7 | **Sludge (fanghi)** | ✗ | ✗ | analogue only: tailings-pond SSD on GF-1, 90.2% acc; AerialWaste 19 labels | **GAP** — lagoons visible by context, composition spectral |
| 8 | **Wood / firewood** | ✓ | ◐ | AerialWaste 173 labels (4th most frequent); woody-debris volume = airborne | good — stacked-pile morphology |
| 9 | **Plastic** | ◐ | ✓ | S VHR: morphological only (WV-3 spectral anomaly; Pléiades+S2 API). Spectral plastic only at S2 10 m (out of scope). D: **[NEW]** UAV-SWIR Attention-U-Net **96.8% acc / 91.1% F1**; **[NEW]** UAV-RGB+IoT **92%** (rivers) | presence by texture at VHR; **polymer type needs SWIR → drone-HSI** |
| 10 | **Big bags / FIBC** | ◐ | ✗ | only AerialWaste 50 labels; ~1 m³ ≈ 3×3 px @30 cm | **near-GAP** — small + data-scarce |
| 11 | **Tanks / cisterns** | ✓ | — | **[NEW]** YOLOv7-OT **90% acc / 95.9% prec** (RS 2024); Ramachandran Nat. Commun. 2024 **P 0.962 / R 0.968** (>169k tanks); Bakırman YOLO SPOT | excellent — circular shape. **NOT a gap** (move out of the data-thin bucket) |
| 12 | **Tires** | ✓ | ◐ | TIRe model QuickBird 0.6 m (piles ≥100–400 tires); Disaitek "tires" 30 cm; AerialWaste 45 labels | good for piles; dark-target confusion w/ shadow/water |
| 13 | **Asbestos-cement roofing** | ✓ | ✓ | S-SWIR: **[NEW] Bonifazi 2026** WV-3 VNIR+**SWIR** MLC building-level (Mantua, open Python); Saba WV-3 8-VNIR **Macro-F1 97.6%**; EnMAP 30 m ACE 91.4% (out of scope = SWIR upper bound). S/aerial broadband (**no SWIR**): **[NEW] Abbasi 2024** Nearmap aerial, DenseNet+LSTM multi-temporal, **OA 95.8–96.0%, AC 94%**. D: **[NEW]** asbestos-slate drone-RGB DL (2023) | corrugated **shape** detectable at 30–50 cm; **material confirmation needs SWIR** (≥1.2 m WV-3) or very fine VHR + temporal |

---

## 4. Methods seen, by family

- **Object detection** (shape classes): YOLOv7-OT/CBAM (tanks), region-based + domain adaptation (vehicles), CenterNet+Mask R-CNN (containers), Yu 2-step YOLOv8+ResNet on Gaofen 1–2 m (84.1% mAP, 5 waste types), Zhou SWDet on WV-2/SPOT 1.8 m (77.58% mAP on SWAD).
- **Semantic segmentation** (heaps / pixel maps): improved DeepLabV3+ (CWLD C&D), DeepLabv3+ (Yong C&D), dual-branch UAV nets, U-Net/FCN encoder-decoders (ESI landfills), FCN+SfM (drone C&D volume).
- **Scene classification** (binary candidate sites): Swin-T+RSP (Gibellini), ResNet-50+FPN (AerialWaste), lightweight CNN+transformer ensembles.
- **Foundation models**: **[NEW]** fine-tuned CLIPSeg ("fCLIPSeg") for post-hurricane debris, aerial RGB, Dice 0.70 — the SAM/CLIP-family route for the data-thin shape classes.
- **Spectral / OBIA** (material classes): MLC on WV-3 VNIR+SWIR (asbestos, Bonifazi), 8-classifier consensus on EnMAP (asbestos, Shepherd), Attention-U-Net on UAV-SWIR (plastic), OBIA+DenseNet+LSTM change detection (asbestos, Abbasi).

---

## 5. The gaps — say these explicitly to Thomas

1. **No dedicated VHR-satellite OR drone detector** for **foundry slag (#2), sludge (#7), big bags (#10), scrap-metal composition (#4)** — only rare AerialWaste annotations or close-range/analogue studies.
2. **Asbestos at true 30–50 cm is not validated** — every strong asbestos result is either WV-3 ≥1.2 m **with SWIR**, EnMAP 30 m hyperspectral, or fine aerial (≤25 cm) — not 30–50 cm broadband satellite.
3. **Plastic polymer type needs SWIR** — at 30–50 cm satellite you get presence/extent only; identity comes from drone-HSI or S2-scale indices.
4. **The whole field is binary/aggregate** — no public per-class (13-material) detector at the VHR satellite operating point. This is the contribution space.
5. **Correction vs the first matrix:** **tanks (#11) are NOT a gap** — there is a mature standalone VHR detector literature (YOLOv7-OT, Ramachandran). Move #11 from "data-thin" to "well-served object".

---

## 6. Sources (29, deduped) — quick index

Peer-reviewed (primary): CascadeDumpNet (RSE 313, 2024); CWLD construction-waste dataset (Scientific Data, 2024); Gibellini 2025 (arXiv 2502.06607 / Waste Management Bulletin); AerialWaste ensemble benchmark (arXiv 2508.18315, 2025); Post-Hurricane debris / fCLIPSeg (arXiv 2504.12542, 2025); C&D drone FCN+SfM (Drones, 2022); large-area UAV solid-waste seg (Applied Sciences 14:2084, 2024); YOLOv7-OT tanks (Remote Sensing 16:4510, 2024); UAV-SWIR plastic Attention-U-Net (Remote Sensing 18:182, 2026); UAV+IoT plastic (J. Haz. Mat. Advances, 2025); EnMAP asbestos (Scientific Reports 15:24166, 2025); Bonifazi asbestos Python (Geomatics 6:41, 2026); Abbasi asbestos change detection (RSASE, 2024); asbestos-slate drone (PMC, 2023); Hybrid-YOLOv5 ELV non-ferrous (Scientific Reports 15:23170, 2025); vehicle detection + DA (Remote Sensing 12:575, 2020); heavy-duty truck satellite (PMC, 2025); Waste Management RS survey (2024); UAV waste systematic review (Drones 9:550, 2025).

Grey / operational: Disaitek Illegal Waste Tracker; Airbus Pléiades Neo case study + Applications Campus (2024/2025); European Space Imaging / SZTAKI landfills; Innoter; Satellogic.

*Verification: adversarial 3-vote pass confirmed the CascadeDumpNet (0.5 m, dual-stage CNN+AutoML), Gibellini (Swin-T, 92.02% F1, from the PDF), and EnMAP-asbestos (ACE 91.4%, 30 m hyperspectral = out of VHR scope) claims at HIGH confidence. The synthesize stage of the workflow was interrupted by session crashes; this document is the hand-synthesis from the verified journal.*
