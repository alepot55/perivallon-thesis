# Datasets — an explained guide (PERIVALLON thesis)

A readable, reasoned guide to **every dataset relevant to this thesis**, organised by the *role* each one plays — not just an alphabetical list. For the dense 42-entry reference (with full DOIs and pixel counts) see [`datasets_catalog.md`](datasets_catalog.md); for the latest finds see its **"Addendum — June 2026"**. This guide is the one to *read*; the catalog is the one to *look things up in*.

---

## 0. How to read this guide

A satellite/EO dataset is only useful to us in one of **three roles**. Always ask which role a dataset is for before judging it:

1. **Training / evaluation target** — labelled imagery you can actually train or test a model on (e.g. AerialWaste, MARIDA, EuroSAT).
2. **Spectral reference** — pure material signatures (point spectra, not images) used to *interpret* bands, build endmembers, or justify why a band matters (e.g. USGS splib07a, WaRM).
3. **Pretraining corpus** — large unlabelled or LULC-labelled imagery used to pretrain a backbone before fine-tuning on our small target set (e.g. SSL4EO-S12, SpectralEarth).

And three properties decide fit for *our* problem:

- **Spatial resolution (GSD)** — can it resolve a 50–200 m² dump? (SuperDove 3 m ✓ ; Sentinel-2 10 m ✗ for small sites; hyperspectral 30 m ✗✗.)
- **SWIR present?** — material chemistry (plastic C–H, asbestos Mg-OH, clay Al-OH) lives at 1000–2500 nm. SuperDove (our sensor) is **VNIR-only**, so SWIR datasets are *reference/upper-bound*, not training data.
- **Label level** — *material* (what it's made of) vs *land-use* (what it's for) vs *binary* (waste / no-waste). The thesis's whole gap is **material labels**.

### The one-line gap that frames everything
> **No public dataset combines multispectral-satellite imagery + terrestrial waste + material-level labels.** Confirmed across three deep-research rounds (June 2026), mission by mission. Every existing resource sits on *one side* of this gap — satellite-but-binary, or material-but-lab, or material-but-marine. The thesis lives in the hole.

---

## 1. Core datasets — what the thesis actually uses

These are the few you train/evaluate on or that anchor the pilot. Know these cold.

### AerialWaste v3 — the baseline dataset
- **What:** the PoliMi illegal-waste dataset (Torres & Fraternali, *Nature Scientific Data* 2023). ~11,700 RGB tiles (≈3,478 positive / 6,956 negative in the v-earlier count), three sources at different GSD: **AGEA ortophoto ~20 cm, WorldView-3 ~30 cm, Google Earth ~50 cm**.
- **Labels/task:** binary (waste / no-waste) + **22 fine material categories** (rubble, tires, vehicles, containers, big-bags…) + segmentation masks on 169 images. Task = **scene classification**.
- **SWIR / bands:** **RGB-only** (3 bands). This is the crux: it has material *categories* but no spectral bands to exploit them.
- **Access:** Zenodo (DOI 10.5281/zenodo.12607190); model code `nahitorres/aerialwaste-model`.
- **Role & why it matters:** the **training/eval target** and the Gibellini-2025 baseline (Swin-T + RSP, F1 92%). The thesis extends it from 3 → N bands. Its RGB-only nature *is* the limitation the thesis attacks.
- **Limit:** RGB-only, Lombardy-centric → poor generalisation evidence (−5.1pp cross-country).

### DroneWaste — the PERIVALLON UAV companion
- **What:** newly released PERIVALLON dataset, 4,993 UAV images, 17 dumps, **20 material types**, cm-level GSD, RGB.
- **Role:** material-level ground truth at very fine scale — useful as a *material taxonomy* reference and for UAV-confirmation framing, but RGB-only and not satellite.
- **Access:** Zenodo 10.5281/zenodo.17288038.

### EuroSAT MS — the band-ablation workhorse
- **What:** 27,000 Sentinel-2 patches, **13 bands @10 m**, 10 land-use classes.
- **Role:** *not* a waste dataset — it's our **controlled band-ablation testbed** (RGB vs +NIR vs +RedEdge vs full-13) and a sanity check for the multispectral adapter. Labels are LULC, not material.
- **Access:** open; in TorchGeo. Local copy in `waste/data/eurosat/`.

### Lombardy asbestos WFS — the pilot ground truth
- **What:** the regional asbestos-roof inventory: **`Mappatura_2020` (10,903 roofs) + `Mappature_precedenti` (50,131)**, EPSG:32632, vector polygons.
- **Role:** the **label source for Phase-1 asbestos pilot** (with/without-asbestos roof polygons → SuperDove signatures → exploratory clustering). It is *ground truth*, not imagery.
- **Access:** Lombardy WFS/REST (see `reference_lombardy_asbestos_wfs.md`).

### Planet SuperDove archive — the sensor (not a labelled set)
- **What:** 8 VNIR bands (Coastal Blue, Blue, 2×Green, Yellow, Red, Red Edge, NIR) @ **3 m**, near-daily, free via Planet E&R. **No SWIR.**
- **Role:** the **imagery source** for both Phase 1 (asbestos) and Phase 2 (waste). You self-pair it with the labels above. There is no off-the-shelf labelled SuperDove waste/asbestos dataset — that's the gap.

---

## 2. Waste & debris remote-sensing datasets (the direct comparators)

Closest in *task*, but each fails one criterion (RGB-only, marine, or no material labels).

| Dataset | Year | Sensor / GSD | SWIR | Labels / task | Why it matters / limit |
|---|---|---|---|---|---|
| **MARIDA** | 2022 | S2, 10–60 m | ✅ (11 S2 bands) | pixel **segmentation**, 15 classes (incl. Marine Debris) | closest *public* MS + material-ish benchmark; but **marine**, debris-vs-natural not polymer type |
| **MADOS** | 2024 | S2, 10–60 m | ✅ | segmentation, 15 classes (+oil spill) | larger MARIDA successor; still marine |
| **Global Dumpsite** (Sun 2023) | 2023 | VHR 0.3–1 m | ❌ RGB | **detection**, 4 waste *types* (domestic/construction/agri/covered) | first global classified-dumpsite benchmark; RGB-only, academic-use (scidb.cn) |
| **Tisza river-waste** (Magyar 2023) | 2023 | S2 + **PlanetScope 4-band BGRN @3 m** | ❌ VNIR | pixel-class, dedicated **"waste"** class, ~96% | ⭐ strongest *methodological* transfer to SuperDove (VNIR-only, 4 common bands) |
| **FloatingObjects** | 2021 | S2 | ✅ | binary floating-object detection | global S2 baseline; binary only |
| **Duarte Floating-Marine-Debris** | 2023–24 | S2, 13 band | ✅ | 6 floating *material* classes (plastic/driftwood/…) | material-level at satellite scale — but marine |
| **Plastic Litter Projects (PLP)** | 2019–22 | S2 + UAV HSI | ✅ | known targets (PET/LDPE/wood), subpixel | controlled spectral-unmixing validation |
| **SWAD** | — | ~1–2 m RGB | ❌ | bounding boxes (1 class) | RGB detection only |
| **UAVVaste / TACO / TrashNet** | — | RGB (UAV / close-range) | ❌ | detection / classification | RGB-only, not satellite — context only |

**Takeaway:** the satellite waste world is either **binary** (no material) or **marine** (not terrestrial). Material-at-satellite-scale only exists for floating debris.

---

## 3. Spectral libraries (Role 2 — reference signatures)

Point-spectra collections. You don't train on these; you use them to build endmembers, justify bands, and validate. Most cover full **VNIR+SWIR (350–2500 nm)**.

**General / authoritative**
- **USGS splib07a** — the reference library: 2,151 channels 350–2500 nm, 1,300+ materials, **S2/WV-3 convolutions pre-computed** (use directly). The backbone of all our signature plots. (`reference_usgs_splib07a.md`)
- **ECOSTRESS** — >3,400 spectra, adds thermal-IR emissivity. Complements USGS.

**Urban materials**
- **KLUM** (Karlsruhe) — 181 urban material samples, 12 classes incl. plastic, metal, concrete, with weathering metadata.
- **LUMA SLUM** (London) — 74 samples incl. **PVC and rubber** + emissivity. Directly waste-relevant.
- **WaRM** (Walloon Roof Materials) — 26 roof spectra incl. **corrugated asbestos-cement** ⭐ — directly analogous to the pilot.

**Plastics / polymers (for the waste material argument)**
- **MADLib** (2025) — 24,889 marine-debris spectra, polymer-specific, the definitive plastic reference.
- **Garaba & Dierssen** — 11 virgin polymer types; diagnostic SWIR at 1215/1410/1730 nm.
- **Knaeps** — submerged plastics (shows how water degrades the signal).
- **Olyaei** (2024) — first freshwater plastic HSI database with fractional abundance.
- **Open Specy / FLOPP / FTIR-Plastics / NIST NIR-SORT** — FTIR/NIR polymer & textile libraries (lab spectroscopy, not imaging) — endmember references for polymer/textile types.

**Asbestos-specific (pilot)**
- **EnMAP asbestos-cement field library** (SciReports 2025) — 2,714 spectra incl. **weathered / moss-covered / paint-sealed** AC (the "artificial-cover" failure mode). On request only; Israel campaign.
- Diagnostic asbestos features to remember: **chrysotile 1.385 µm (OH) and 2.323 µm (Mg-OH)** — the 2.32 µm band is the satellite workhorse, and it's **outside SuperDove's VNIR range**.

**Soil**
- **LUCAS Soil** (~45k EU topsoil) and **OSSL** (>100k) — soil composition spectroscopy; context/background-class reference.

---

## 4. Urban / material hyperspectral image benchmarks (Role 2/3 — method references)

Labelled HSI *images* with material classes — decades of validated spectral classification. Mostly **airborne**, 30 cm–20 m, often VNIR+SWIR. Use as **method baselines** ("this is how material classification from spectra is done") and to justify the spectral approach. None is waste.

- **Pavia University / Pavia Centre** — the most-benchmarked: 9 classes, 6 are urban materials (asphalt, bitumen, bricks, tiles…). VNIR only.
- **Toulouse Hyperspectral** (2024) — state of the art: 310 channels **VNIR+SWIR**, 32 material classes incl. multiple paving/roof subtypes, 1 m. Best modern urban-material benchmark.
- **Berlin-Urban-Gradient** — HyMap VNIR+SWIR + simulated EnMAP, with endmember library (unmixing).
- **MUUFL Gulfport / MDAS Augsburg / HYDICE Urban** — airborne HSI (+LiDAR / +S2 fusion) with road/roof/material classes; classic unmixing/fusion benchmarks.
- **IEEE GRSS DFC 2013 / 2018** — Houston urban material+LiDAR contests (road, parking, synthetic surfaces).
- **ISPRS Potsdam** — 4-band (RGB+NIR) aerial seg; "impervious surface" is coarse (asphalt+concrete merged).
- **MCubeS** — close-range RGB+NIR+polarization, 20 material classes — shows NIR+polarisation adds +2.7–8.7% mIoU over RGB (evidence for "beyond RGB helps").
- **Geology:** **Cuprite** (AVIRIS, the gold-standard mineral benchmark), **Indian Pines / Salinas** (AVIRIS crop/material), **WHU-Hi** (UAV HSI, HanChuan scene includes a **plastic** class), **EnGeoMAP** (simulated EnMAP mineral ID). Mineral mapping = the strongest proof that spectra identify materials at molecular level.

---

## 5. Recycling / industrial-waste datasets (Role 2 — material proof, wrong setting)

Conveyor-belt / lab HSI of waste materials. Prove polymer/metal discrimination works, but operate indoors at cm scale — not transferable to satellite, useful as *material evidence*.

- **SpectralWaste** (IROS 2024) — first public HSI+RGB from a real sorting plant; fusion RGB+spectral wins.
- **Tecnalia WEEE** — e-waste metal sorting, 5 metal classes, pixel masks.
- **RECONMATIC** — construction & demolition waste HSI (mortar/concrete/brick/wood/gypsum/plastic).
- **WoodVIT** (2026) — multimodal bulky-waste (VIS+NIR-HSI+thermal+THz), wood vs 16 subclasses.
- **Hyperspectral Scrap Metal** (2025) — contaminant (wood/plastic) detection in metal streams.

---

## 6. Foundation-model pretraining corpora (Role 3)

Large EO datasets used to pretrain backbones. Labels are LULC, not material — they give the backbone "EO eyes," then you fine-tune on AerialWaste/SuperDove.

| Dataset | Bands | Use |
|---|---|---|
| **BigEarthNet v2** | S1+S2 (12) | multi-label LULC pretraining, huge |
| **SSL4EO-S12** | all 13 S2 | **ready-made pretrained weights** (ResNet/ViT) for S2 — practical starting point |
| **SEN12MS / So2Sat LCZ42** | S1+S2 | scene/segmentation, climate zones |
| **SpectralEarth** (2024) | EnMAP HSI 224 (**SWIR**) | largest HSI pretraining set (538k patches); downstream tasks all LULC |
| **HySpecNet-11k** | EnMAP HSI (**SWIR**) | HSI compression/SSL benchmark; **no material labels** |
| **fMoW** | RGB/MS | functional categories; mostly RGB context |

For *our* sensor the relevant FM is **DOFA** (wavelength-conditioned, sensor-agnostic) — it doesn't ship a dataset, it ships a backbone you feed SuperDove's 8 band-wavelengths to.

---

## 7. Roof-material datasets (Role 1/2 — pilot-adjacent)

Surfaced in June 2026. Useful for roof-material taxonomy and the asbestos pilot.

- **RoofNet** (2025) — 51,503 EO tiles, 112 countries, **14 roof-material classes** — but **no asbestos class** (add separately). CC-BY-NC.
- **Nacala-Roof-Material** (2025) — drone RGB, **explicit asbestos class** (566/17,954 buildings) — rare asbestos ground truth, but RGB-only, Mozambique.
- **RoofSense** (2025) — NL aerial+LiDAR, 8 roof materials, no asbestos — segmentation methodology.
- **GlobalBuildingMap** (2024) — 790k **PlanetScope @3 m** building masks (CC-BY-4.0); same platform as the pilot → roof-localisation pre-step. Imagery not redistributable.
- **FloodPlanet** (2023) — cross-sensor PlanetScope+S1/S2/L8 flood segmentation — rare *paired* annotated example (likely Dove-Classic, not 8-band SuperDove).

---

## 8. Spaceborne hyperspectral missions — data status (mostly raw, no labels)

The June 2026 mission-by-mission pass: **none ships a public material-labelled benchmark.** They are imagery archives. The public *labelled* SWIR data is mostly **methane/CO₂ plume masks** (STARCOP, UNEP-IMEO MARS-Hyperspectral, Carbon Mapper) — gas, not solid materials.

| Mission | Bands / GSD | Material-labelled benchmark? | Note |
|---|---|---|---|
| **PRISMA** (ASI) | ~240, 30 m, VNIR+SWIR | ❌ | raw archive only; landfill studies output risk maps |
| **EnMAP** (DLR) | ~224, 30 m, VNIR+SWIR | ❌ | new labelled sets all LULC/crop/biomass; can map minerals (result maps only) |
| **EMIT** (NASA/ISS) | 285, 60 m, VNIR+SWIR | ⭐ no benchmark, but: | **Estrela 2025 (GRL)** detects HDPE/PVC globally via SWIR matched filter — feasibility/validation reference |
| **Tanager-1** (Planet) | ~424, 30 m, VNIR+SWIR | ❌ (labels) | **Tanager Open Data**: ~50+ scenes, CC-BY-4.0, full VSWIR — *unlabelled* → self-annotation candidate |
| **GaoFen-5 / AHSI, ZY1-02D** | VNIR+SWIR | ❓ unresolved | needs Chinese-language search |

---

## 9. Validation track — the WorldView-3 SWIR option (Thomas's interest)

Not a dataset, but the practical route to a SWIR gold standard:
- **ESA eoGateway** — full WV-3 archive incl. **SWIR up to 3.7 m**, **free to ESA-member (Italy/PoliMi) researchers** via project proposal (~9-week eval). Raw imagery, self-annotate.
- **Saba et al. 2026 (J. Hazardous Materials)** — WV-3 **VNIR-only** 8-band asbestos, F1 97.6% / ~99–100% binary → a near-competitor proving 8 VNIR bands suffice for asbestos (supports the SuperDove pilot).
- **Cartagena HySpex** (Heliyon 2024) — airborne VNIR+SWIR asbestos @0.8 m; data on request — the upper-bound reference.

---

## 10. Recommendation — which dataset for which job

| Thesis need | Use |
|---|---|
| Baseline (replicate Gibellini) | **AerialWaste v3** (RGB, Swin-T+RSP) |
| Band ablation (RGB → +NIR → full) | **EuroSAT MS** (controlled) → then SuperDove on AerialWaste AOIs |
| Phase-1 asbestos pilot | **Lombardy WFS** labels × **SuperDove** imagery; signatures vs **USGS splib07a / WaRM** |
| Material evidence (justify spectra) | **USGS splib07a**, **MARIDA**, **Aguilar WV-3** (in library), **MCubeS** |
| Pretraining backbone | **SSL4EO-S12** (S2) or **DOFA** (sensor-agnostic, for SuperDove) |
| SWIR gold-standard / validation | **WV-3 via ESA eoGateway**; reference **Saba 2026**, **EMIT plastic**, **Cartagena** |
| Roof taxonomy / asbestos GT (extra) | **RoofNet**, **Nacala** (asbestos class), **GlobalBuildingMap** (localisation) |

### Bottom line
The thesis's contribution opportunity is exactly the empty cell: **pair SuperDove (3 m, 8 VNIR bands) imagery with material-level labels (asbestos roofs, then waste), and measure how far VNIR-only gets toward the SWIR upper bound.** Every dataset above is either a label source, an imagery source, a spectral reference, or a pretraining corpus that feeds that one experiment — none does it for you.

---

*Sources: this guide synthesises [`datasets_catalog.md`](datasets_catalog.md) (42 entries + June-2026 addendum), [`research_compendium.md`](research_compendium.md), [`technical_foundations.md`](../00_context/technical_foundations.md), and the `papers/` library. Specs are as verified in those files; check the catalog for exact DOIs and counts.*
