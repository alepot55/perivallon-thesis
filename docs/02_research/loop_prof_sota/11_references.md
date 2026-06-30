# Annotated Bibliography — verified anchors for the thesis `.bib`

*Autonomous research loop, iteration 6 (2026-06-28). DOIs/citations web-verified. Tags: VERIFIED / PARTIAL / NOT-FOUND. Ready-to-paste BibTeX in `references.bib` (same folder). **Corrections worth noting** are flagged inline — propagate them into the other docs and the thesis.*

> ⚠ **Key corrections from this pass:**
> - **CascadeDumpNet = Zhang & Ma 2024** (RSE 313:114349), **two authors** — NOT Marrocco, NOT "et al.". Marrocco et al. 2024 (IEEE Access) is a *separate* microdump paper.
> - **Torres & Fraternali 2023** real title: *"AerialWaste dataset for landfill discovery in aerial and satellite images"* (Sci. Data 10:63).
> - **Shepherd et al. 2025** second author = **Elad Sagi** (the "Aharoni-Mack" attribution seen elsewhere is wrong).
> - **Gibellini 2025** full author list incl. Boracchi, Morandini, **Martinoli**, Diecidue, Malegori; DOI 10.1016/j.wmb.2025.100246.
> - **"Garaba & Dierssen 2021, Sci. Rep."** does not exist — it conflated two real works (see [15]); pick the right one per intent.

---

## Group 1 — Waste detection (baseline & related)

**[1] Gibellini et al. 2025 — VERIFIED** · Gibellini, F., Fraternali, P., Boracchi, G., Morandini, L., Martinoli, T., Diecidue, A., & Malegori, S. *A Deep Learning Pipeline for Solid Waste Detection in Remote Sensing Images.* Waste Management Bulletin. DOI 10.1016/j.wmb.2025.100246 (arXiv 2502.06607). — The Swin-T+RSP baseline (F1 92.02%) this thesis extends.

**[2] Torres & Fraternali 2023 — VERIFIED (title corrected)** · *AerialWaste dataset for landfill discovery in aerial and satellite images.* Scientific Data 10:63. DOI 10.1038/s41597-023-01976-9. — The main training dataset (RGB, 22 material categories, coords withheld).

**[3] Fraternali et al. 2024 — VERIFIED** · Fraternali, P., Morandini, L., Herrera González, S. L. *Solid waste detection, monitoring and mapping in remote sensing images: A survey.* Waste Management 189:88–102. DOI 10.1016/j.wasman.2024.08.003 (arXiv 2402.09066). — Field survey; RGB-only as a structural limitation.

**[4] Zhang & Ma 2024 (CascadeDumpNet) — VERIFIED (authorship corrected)** · Zhang, S., & Ma, J. *CascadeDumpNet: …dual-stage approach using high-resolution satellite imagery.* Remote Sensing of Environment 313:114349. DOI 10.1016/j.rse.2024.114349. — Pléiades 0.5 m comparator, 84.6% mAP.

**[5] Sun et al. 2023 — VERIFIED** · *Revealing influencing factors on global waste distribution via deep-learning based dumpsite detection…* Nature Communications 14:1444. DOI 10.1038/s41467-023-37136-1. — Global dumpsite detection.

**[6] Sharmily et al. 2025 — PARTIAL (arXiv-only)** · *Automated Landfill Detection Using Deep Learning… with the AerialWaste Dataset.* arXiv 2508.18315. — Lightweight/ensemble benchmark (F1 92.41% binary).

**[7] Marrocco et al. 2024 — VERIFIED** · *Illegal Microdumps Detection in Multi-Mission Satellite Images…* IEEE Access 12:79585–79601. DOI 10.1109/ACCESS.2024.3409393. — Pléiades + GeoEye-1 microdump detection (Campania).

## Group 2 — Asbestos & material spectroscopy

**[8] Saba et al. 2026 — VERIFIED** · *Satellite-based detection of asbestos-cement roofs using WorldView-3 VNIR data…* Journal of Hazardous Materials 508:141864. DOI 10.1016/j.jhazmat.2026.141864. — Closest satellite analogue for the asbestos pilot.

**[9] Bonifazi et al. 2026 — VERIFIED** · *A Python-Based Workflow for Asbestos Roof Mapping and Temporal Monitoring Using Satellite Imagery.* Geomatics 6(3):41. DOI 10.3390/geomatics6030041. — Reproducible WV-3 VNIR + Py6S workflow (primarily VNIR; "VNIR+SWIR" framing not central — note vs earlier docs).

**[10] Shepherd et al. 2025 — VERIFIED (author corrected)** · Shepherd, J. E., Sagi, E., Zagron, G., Ben-Dor, E. *Detection of asbestos-based cement rooftops… using EnMAP hyperspectral data.* Scientific Reports 15:24166. DOI 10.1038/s41598-025-09738-w. — Spaceborne HSI asbestos (30 m = out of VHR scope; upper bound).

**[11] Cilia et al. 2015 — VERIFIED** · *Mapping of Asbestos Cement Roofs and Their Weathering Status Using Hyperspectral Aerial Images.* ISPRS Int. J. Geo-Information 4(2):928–941. DOI 10.3390/ijgi4020928. — Foundational airborne (MIVIS) asbestos + weathering, Italy.

**[12] Valdelamar Martínez et al. 2024 — VERIFIED (descriptor corrected)** · *Assessment of asbestos-cement roof distribution and prioritized intervention approaches through hyperspectral imaging.* Heliyon 10(3):e25612. DOI 10.1016/j.heliyon.2024.e25612. — Degradation indices + prioritization. (HySpex = lab/field spectroscopy, not airborne.)

**[13] Aguilar et al. 2021 — VERIFIED** · *Evaluation of Object-Based Greenhouse Mapping Using WorldView-3 VNIR and SWIR Data…* Remote Sensing 13(11):2133. DOI 10.3390/rs13112133. — WV-3 VNIR/SWIR band-ablation precedent (plastic-film/NDPI).

**[14] Kokaly et al. 2017 — VERIFIED (USGS report)** · *USGS Spectral Library Version 7.* USGS Data Series 1035. Report DOI 10.3133/ds1035; data DOI 10.5066/F7RR1WDJ. — splib07a reference signatures (in `spectral/`).

**[15] Plastic SWIR signatures — PARTIAL (conflation corrected)** · The supplied "Garaba & Dierssen 2021, Sci. Rep." does not exist. Use either:
- (a) **Moshtaghi et al. 2021** *Spectral reflectance of marine macroplastics in the VNIR and SWIR…* Sci. Reports 11:5436. DOI 10.1038/s41598-021-84867-6 — controlled VNIR/SWIR reflectance DB (Dierssen NOT an author);
- (b) **Garaba & Dierssen 2018** *An airborne remote sensing case study of synthetic hydrocarbon detection… SWIR absorption features…* RSE 205:224–235. DOI 10.1016/j.rse.2017.11.023 — the C-H/SWIR diagnostic-feature source.

## Group 3 — Foundation models, benchmarks & health/policy

**[16] Xiong et al. 2024 (DOFA) — VERIFIED** · *Neural Plasticity-Inspired Multimodal Foundation Model for Earth Observation.* arXiv 2403.15356. — Wavelength-conditioned FM (Dynamic-One-For-All).

**[17] Corley et al. 2024 — VERIFIED** · *Revisiting Pre-trained Remote Sensing Model Benchmarks: Resizing and Normalization Matters.* CVPR 2024 Workshops (PBVS). arXiv 2305.13456. — Preprocessing caution.

**[18] GeoCrossBench 2025 — PARTIAL (authors not surfaced)** · *GeoCrossBench: Cross-Band Generalization for Remote Sensing.* arXiv 2511.02831. — Cross-band generalization benchmark (fetch author list before final cite).

**[19] Astruc et al. 2025 (AnySat) — VERIFIED** · *AnySat: One Earth Observation Model for Many Resolutions, Scales, and Modalities.* arXiv 2412.14123; CVPR 2025.

**[20] Szwarcman et al. 2024 (Prithvi-EO-2.0) — VERIFIED** · *Prithvi-EO-2.0: A Versatile Multi-Temporal Foundation Model for Earth Observation Applications.* arXiv 2412.02732.

**[21] Hong et al. 2024 (SpectralGPT) — VERIFIED** · *SpectralGPT: Spectral Remote Sensing Foundation Model.* IEEE TPAMI 46(8):5227–5244. DOI 10.1109/TPAMI.2024.3362475.

**[22] Fazzo et al. 2020 — VERIFIED (full authors TBC)** · *A GIS-Based Indicator of Waste Risk to Investigate the Health Impact of Landfills and Uncontrolled Dumping Sites.* IJERPH 17(16):5789. DOI 10.3390/ijerph17165789. — The risk-model template (hazard × exposure × magnitude).

**[23] Fazzo et al. 2023 — VERIFIED (first author TBC)** · *The health impact of hazardous waste landfills and illegal dumps contaminated sites… Italian Region.* Frontiers in Public Health 11:996960. DOI 10.3389/fpubh.2023.996960.

**[24] Estrela et al. 2025 — VERIFIED (full authors TBC)** · *Global-Scale Detection of Plastic From Space With the EMIT Imaging Spectrometer.* Geophysical Research Letters 52:e2024GL112416. DOI 10.1029/2024GL112416.

---

*Open TODOs before the thesis `.bib` is final: full author lists for GeoCrossBench, Fazzo 2020/2023, Estrela 2025, Prithvi-EO-2.0; confirm Sharmily venue; choose [15](a) vs (b).*
