---
title: "Datasets for waste & material detection from remote sensing"
subtitle: "A study guide for the PERIVALLON thesis — read this instead of the papers"
author: "PERIVALLON thesis · Politecnico di Milano"
date: "2026-06-24"
---

# 0. How to use this guide

This is the one document to *study*. It explains every dataset relevant to the thesis, organised by the **role** each one plays — not alphabetically. For each, ask three questions before judging it.

**The three roles a dataset can play:**

1. **Training / evaluation target** — labelled imagery you can actually train or test a model on (AerialWaste, CWLD, MARIDA, EuroSAT).
2. **Spectral reference** — pure material signatures (point spectra, not images) used to interpret bands and justify why a band matters (USGS splib07a, WaRM).
3. **Pretraining corpus** — large unlabelled or land-cover-labelled imagery to pretrain a backbone before fine-tuning on our small target set (SSL4EO-S12, SpectralEarth).

**The three properties that decide fit for *our* problem:**

- **Spatial resolution (GSD).** Can it resolve a 50–200 m² dump or a single roof? Our operating point is **30–50 cm VHR satellite**; SuperDove (3 m) is the asbestos-pilot sensor. Sentinel-2 (10 m) and hyperspectral missions (30 m) are *out of scope* for detection.
- **SWIR present?** Material chemistry (plastic C–H, asbestos Mg-OH, clay Al-OH) lives at 1000–2500 nm. Our broadband VHR sensors are **VNIR-only**, so SWIR datasets are *reference / upper-bound*, not training data.
- **Label level.** *Material* (what it is made of) vs *land-use* (what it is for) vs *binary* (waste / no-waste). The thesis gap is **material-level labels**.

**The one-line gap that frames everything**

> No public dataset combines **VHR satellite imagery + terrestrial waste + material-level labels**. Every existing resource sits on one side of this gap: satellite-but-binary, or material-but-lab, or material-but-marine. The thesis lives in that hole.

**The rule that governs feasibility (object vs material).** At 30–50 cm broadband VNIR, a class is feasible if its identity is in **shape/context** (vehicles, tanks, containers, rubble heaps, bulky items, firewood, tires, big bags) and weak if its identity is in **spectral chemistry** (asbestos, plastic polymer type, foundry slag, sludge, scrap composition).

\newpage

# 1. Core datasets — what the thesis actually uses

Know these cold.

## AerialWaste v3 — the baseline dataset

- **What:** the PoliMi illegal-waste dataset (Torres & Fraternali, *Scientific Data* 2023). ~10,434 images (v3 ≈ 11,700), three sources at different GSD: **AGEA orthophoto ~20 cm, WorldView-3 ~30 cm, Google Earth ~50 cm**. 3,478 positive / 6,956 negative (≈2:1 neg:pos).
- **Labels / task:** binary (waste / no-waste) + **22 fine material categories** (rubble, tires, vehicles, containers, big bags…) + segmentation masks on 169 images. Task = scene classification.
- **Bands:** **RGB only** (3 bands). This is the crux — it has material *categories* but no spectral bands to exploit them.
- **Access:** Zenodo (DOI 10.5281/zenodo, via aerialwaste.org); model code `nahitorres/aerialwaste-model`.
- **Role & why it matters:** the **training/eval target** and the Gibellini-2025 baseline (Swin-T + RSP, F1 92.0%). The thesis extends it from 3 → N bands. Its RGB-only nature *is* the limitation the thesis attacks.
- **Object-label counts (useful for the 13 classes):** Rubble 294 · Bulky items 286 · Firewood 173 · Scrap 167 · Plastic 126 · Vehicles 53 · Tires 45 · Foundry waste 9. Storage mode: heaps-not-delimited 448 · Containers 167 · Delimited heaps 69 · Big bags 50 · Pallets 50 · Cisterns 35 · Drums/bins 18.

## CWLD — construction-waste landfill dataset (Beijing) **[new]**

- **What:** a 2024 VHR dataset (*Scientific Data*) for construction & demolition (C&D) landfills in two Beijing districts. **GF-2 ~80 cm** (Changping) + **Google Earth ~50 cm** (Daxing); 3,653 samples with pixel-level masks.
- **Labels / task:** semantic segmentation, 4 classes (background, vacant landfillable, buildings/facilities, waste-dumping area). Improved DeepLabV3+ reaches **F1 88.9% / IoU 82%**.
- **Role:** the rare **pixel-level C&D-debris** benchmark from satellite — what AerialWaste lacks. Squarely in our 30–50 cm operating point. Open on Zenodo.

## SWAD — solid-waste aerial dataset

- **What:** public solid-waste detection dataset (WorldView-2 / SPOT class, ~1–2 m); used by SWDet (modified YOLO, 77.58% mAP).
- **Role:** comparator for object-detection of waste piles; coarser than our target GSD but a named public benchmark.

## DroneWaste — the PERIVALLON UAV companion

- **What:** PERIVALLON dataset, 4,993 UAV images, 17 dumps, **20 material types**, cm-level GSD, RGB.
- **Role:** material-level ground truth at very fine scale — a *material taxonomy* reference and UAV-confirmation framing. RGB-only, not satellite.

## EuroSAT MS — the band-ablation workhorse

- **What:** 27,000 Sentinel-2 patches, **13 bands @10 m**, 10 land-use classes.
- **Role:** *not* a waste dataset — our **controlled band-ablation testbed** (RGB vs +NIR vs +RedEdge vs full-13) and a sanity check for the multispectral adapter. Labels are land-use, not material. Local copy in `waste/data/eurosat/`.

## Lombardy asbestos WFS — the pilot ground truth

- **What:** the regional asbestos-roof inventory: **`Mappatura_2020` (10,903 roofs)** + `Mappature_precedenti` (50,131), EPSG:32632, vector polygons.
- **Role:** the **label source for the Phase-1 asbestos pilot** (roof polygons → SuperDove signatures → exploratory clustering). Ground truth, not imagery.

## Planet SuperDove — the asbestos-pilot sensor (not a labelled set)

- **What:** 8 VNIR bands (Coastal Blue, Blue, 2×Green, Yellow, Red, Red Edge, NIR) @ **3 m**, near-daily, free via Planet E&R. **No SWIR.**
- **Role:** the imagery source for the asbestos pilot. You self-pair it with the WFS labels — there is no off-the-shelf labelled SuperDove waste/asbestos dataset (that is the gap). Note: the main waste task uses **30–50 cm VHR satellite**, not SuperDove.

\newpage

# 2. The 13 target classes — which dataset serves which

Thomas's 13 classes, and what data exists at the **30–50 cm satellite (+ drone)** operating point. S = satellite, D = drone. ✓ served · ◐ partial / morphology-only · ✗ gap.

| # | Class | S | D | Dataset / source you would use |
|---|-------|:--:|:--:|--------------------------------|
| 1 | Rubble / C&D | ✓ | ✓ | CWLD (GF-2/GE seg), AerialWaste (294), drone FCN+SfM |
| 2 | Foundry slag | ✗ | ✗ | only AerialWaste (9); else lab hyperspectral — **gap** |
| 3 | Vehicles / ELV | ✓ | ✓ | xView / Pléiades vehicle sets, AerialWaste (53), Disaitek |
| 4 | Scrap metal | ◐ | ✗ | AerialWaste scenes (167); composition lab-IR — **gap** |
| 5 | Bulky items | ✓ | ◐ | AerialWaste (286), UAV solid-waste seg |
| 6 | Containers | ✓ | — | container-detection sets, AerialWaste (167) |
| 7 | Sludge | ✗ | ✗ | tailings-pond analogues only; AerialWaste (19) — **gap** |
| 8 | Wood / firewood | ✓ | ◐ | AerialWaste (173) |
| 9 | Plastic | ◐ | ✓ | VHR morphological only; UAV-SWIR / S-2 indices for type |
| 10 | Big bags (FIBC) | ◐ | ✗ | only AerialWaste (50) — **near-gap** |
| 11 | Tanks / cisterns | ✓ | — | oil-tank detection sets (large, mature), AerialWaste (35) |
| 12 | Tires | ✓ | ◐ | TIRe (QuickBird), AerialWaste (45), Disaitek |
| 13 | Asbestos roofing | ✓ | ✓ | Lombardy WFS + WV-3 (SWIR) / SuperDove; RoofNet/Nacala |

**What to remember:** the *data-thin* classes are **foundry slag, sludge, big bags, scrap-composition** — no dedicated VHR or drone dataset exists. **Tanks are well-served** (mature oil-tank detection literature). Everything else rides on **AerialWaste** plus a few newer per-class sets.

\newpage

# 3. Waste & debris remote-sensing datasets (the direct comparators)

Closest in *task*, but each fails one criterion (RGB-only, marine, or no material labels).

| Dataset | Year | Sensor / GSD | SWIR | Labels / task | Why it matters / limit |
|---------|------|--------------|:----:|---------------|------------------------|
| **AerialWaste** | 2023 | AGEA/WV-3/GE 0.2–0.5 m | ✗ | binary + 22 material cats | the anchor; RGB-only |
| **CWLD** | 2024 | GF-2/GE 0.5–0.8 m | ✗ | C&D segmentation | pixel-level C&D from satellite |
| **SWAD** | — | WV-2/SPOT ~1–2 m | ✗ | waste detection (1 class) | public detection benchmark |
| **Global Dumpsite** (Sun 2023) | 2023 | VHR 0.3–1 m | ✗ | 4 waste *types* | first global classified-dumpsite set |
| **MARIDA** | 2022 | S-2 10–60 m | ✓ | 15-class segmentation | closest MS + material-ish, but **marine** |
| **MADOS** | 2024 | S-2 10–60 m | ✓ | 15-class segmentation | larger MARIDA successor; marine |
| **Tisza river-waste** | 2023 | S-2 + PlanetScope 3 m | ✗ | dedicated waste class | VNIR transfer to SuperDove |
| **FloatingObjects / Duarte / PLP** | 2021–24 | S-2 | ✓ | floating debris / material | material-at-scale, but marine |
| **UAVVaste / TACO / TrashNet** | — | RGB UAV / close-range | ✗ | detection / classification | RGB-only context |

**Takeaway:** the satellite waste world is either **binary** (no material) or **marine** (not terrestrial). Material-at-satellite-scale only exists for floating debris.

\newpage

# 4. Spectral libraries (role 2 — reference signatures)

Point-spectra collections. You don't train on these; you use them to build endmembers, justify bands, and validate. Most cover full **VNIR+SWIR (350–2500 nm)**.

- **USGS splib07a** — the reference library: 2,151 channels 350–2500 nm, 1,300+ materials, **S-2/WV-3 convolutions pre-computed**. Backbone of all our signature plots. Used in `spectral/`.
- **ECOSTRESS** — >3,400 spectra, adds thermal-IR emissivity.
- **Urban:** **KLUM** (181 urban samples, incl. plastic/metal/concrete) · **LUMA SLUM** (PVC, rubber) · **WaRM** (corrugated asbestos-cement ⭐ — directly analogous to the pilot).
- **Plastics:** **MADLib** (24,889 marine-debris spectra) · **Garaba & Dierssen** (11 polymers; SWIR at 1215/1410/1730 nm) · **Open Specy / FTIR libraries** (lab polymer references).
- **Asbestos:** **EnMAP asbestos-cement field library** (2,714 spectra incl. weathered/moss/paint AC). Diagnostic features: **chrysotile 1.385 µm (OH) and 2.323 µm (Mg-OH)** — the 2.32 µm band is the satellite workhorse and is **outside SuperDove's VNIR range**.
- **Soil:** **LUCAS Soil** (~45k EU topsoil) · **OSSL** (>100k) — background-class reference.

\newpage

# 5. Material HSI image benchmarks (role 2/3 — method references)

Labelled hyperspectral *images* with material classes — decades of validated spectral classification, mostly airborne, VNIR+SWIR. Use as **method baselines** ("this is how material classification from spectra is done"). None is waste.

- **Pavia University / Centre** — most-benchmarked urban-material scenes (asphalt, bitumen, bricks, tiles). VNIR only.
- **Toulouse Hyperspectral** (2024) — state of the art: 310 channels **VNIR+SWIR**, 32 material classes, 1 m. Best modern urban-material benchmark; **public**.
- **Berlin-Urban-Gradient / MUUFL / MDAS / HYDICE Urban** — airborne HSI (+LiDAR/+S2) with road/roof/material classes; classic unmixing/fusion benchmarks.
- **GRSS DFC 2013/2018 (Houston)** — urban material + LiDAR contests; **public** (Ma-2023 reaches OA 96% on it with a VNIR 3D-CNN).
- **Geology:** **Cuprite** (AVIRIS mineral gold-standard) · **Indian Pines / Salinas** · **WHU-Hi** (UAV HSI, includes a **plastic** class). Mineral mapping = the strongest proof that spectra identify materials at molecular level.

\newpage

# 6. Recycling / industrial-waste datasets (role 2 — material proof, wrong setting)

Conveyor-belt / lab HSI of waste materials. Prove polymer/metal discrimination works, but operate indoors at cm scale — *material evidence*, not transferable to satellite.

- **SpectralWaste** (2024) — first public HSI+RGB from a real sorting plant; fusion RGB+spectral wins.
- **Tecnalia WEEE** — e-waste metal sorting, 5 metal classes.
- **RECONMATIC** — construction & demolition HSI (mortar/concrete/brick/wood/gypsum/plastic).
- **WoodVIT** (2026) — multimodal bulky-waste (VIS+NIR-HSI+thermal+THz).

\newpage

# 7. Foundation-model pretraining corpora (role 3)

Large EO datasets used to pretrain backbones. Labels are land-use, not material — they give the backbone "EO eyes", then you fine-tune on AerialWaste / SuperDove.

| Dataset | Bands | Use |
|---------|-------|-----|
| **BigEarthNet v2** | S1+S2 (12) | multi-label land-cover pretraining, huge |
| **SSL4EO-S12** | all 13 S2 | **ready-made pretrained weights** (ResNet/ViT) for S2 |
| **SpectralEarth** (2024) | EnMAP HSI 224 (**SWIR**) | largest HSI pretraining set (538k patches) |
| **fMoW** | RGB/MS | functional categories; mostly RGB context |

For *our* sensor the relevant FM is **DOFA** (wavelength-conditioned, sensor-agnostic) — it ships a backbone you feed the band-wavelengths to, not a dataset. It closes the *band* gap, not the *resolution* gap.

\newpage

# 8. Roof-material datasets (role 1/2 — asbestos-pilot-adjacent)

- **RoofNet** (2025) — 51,503 EO tiles, 112 countries, **14 roof-material classes** — but **no asbestos class** (add separately). CC-BY-NC.
- **Nacala-Roof-Material** (2025) — drone RGB, **explicit asbestos class** (566/17,954 buildings) — rare asbestos ground truth, RGB-only, Mozambique.
- **RoofSense** (2025) — NL aerial+LiDAR, 8 roof materials, no asbestos — segmentation methodology.
- **GlobalBuildingMap** (2024) — 790k **PlanetScope @3 m** building masks (CC-BY-4.0) → roof-localisation pre-step.

\newpage

# 9. Recommendation — which dataset for which job

| Thesis need | Use |
|-------------|-----|
| Baseline (replicate Gibellini) | **AerialWaste** (RGB, Swin-T+RSP) |
| Per-class C&D from satellite | **CWLD** (GF-2/GE pixel masks) |
| Band ablation (RGB → +NIR → full) | **EuroSAT MS** (controlled) → then VHR on AerialWaste AOIs |
| Phase-1 asbestos pilot | **Lombardy WFS** labels × **SuperDove**; signatures vs **USGS splib07a / WaRM** |
| Material evidence (justify spectra) | **USGS splib07a**, **MARIDA**, **Toulouse**, **SpectralWaste** |
| Pretraining backbone | **SSL4EO-S12** (S2) or **DOFA** (sensor-agnostic) |
| SWIR gold-standard / validation | **WV-3 via ESA eoGateway**; references Saba 2025, EnMAP asbestos |
| Roof taxonomy / asbestos GT (extra) | **RoofNet**, **Nacala** (asbestos class), **GlobalBuildingMap** |

## Bottom line

The contribution opportunity is the empty cell: **pair VHR satellite (30–50 cm) imagery with material-level labels (asbestos roofs, then the broader waste classes), and measure how far broadband VNIR gets toward the SWIR upper bound.** Every dataset above is either a label source, an imagery source, a spectral reference, or a pretraining corpus that feeds that one experiment — none does it for you.

---

*Companion documents (in `docs/02_research/`): `sota_vhr_13classes.md` (per-class SOTA at 30–50 cm), `datasets_catalog.md` (dense 42-entry reference with DOIs), `sota_highres_material.md` (the 3 m SuperDove spectral framing, asbestos-pilot only).*
