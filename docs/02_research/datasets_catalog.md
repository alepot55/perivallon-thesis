# Multispectral datasets with material-level annotations: a cross-domain catalog

**Beyond-RGB spectral bands consistently improve material classification by 5–20%**, with the SWIR region (1000–2500 nm) emerging as the single most impactful addition across every domain studied. This catalog identifies **42 publicly available datasets** spanning eight domains—from urban rooftop mapping to polymer sorting—that provide material-level annotations with four or more spectral bands. A critical gap persists: **no dedicated public multispectral dataset exists for illegal waste site detection**, making cross-domain transfer from marine debris, recycling, and urban material datasets the most viable strategy for a thesis on this topic.

---

## A. Remote sensing with material-relevant classes

Most large-scale satellite datasets use land-use labels (e.g., "residential") rather than material labels (e.g., "asphalt"), severely limiting their utility for material classification. Only a handful pass the material-relevance filter.

### 1. IEEE GRSS DFC 2013 — University of Houston

| Attribute | Detail |
|---|---|
| **Year** | 2013 (acquired June 2012) |
| **Domain** | Urban land cover / material classification |
| **Bands** | **144 hyperspectral** (CASI sensor), 380–1050 nm (VNIR), 2.5 m GSD; co-registered LiDAR DSM |
| **Platform** | Airborne |
| **Classes (15)** | Healthy Grass, Stressed Grass, **Synthetic Grass**, Trees, **Soil**, Water, Residential, Commercial, **Road (asphalt)**, **Highway (asphalt)**, **Railway (metal/gravel)**, **Parking Lot 1 (asphalt)**, **Parking Lot 2 (concrete/gravel)**, **Tennis Court (synthetic)**, **Running Track (synthetic)** |
| **Size** | 349 × 1905 pixels; ~15,029 labeled pixels |
| **Annotation** | Pixel-level semantic segmentation |
| **Access** | Free via https://machinelearning.ee.uh.edu/ |
| **Paper** | Debes et al., "Hyperspectral and LiDAR Data Fusion: Outcome of the 2013 GRSS Data Fusion Contest," *IEEE JSTARS*, 2014 |
| **Code** | DeepHyperX and many others on GitHub |
| **Relevance** | One of the most widely benchmarked hyperspectral material classification datasets. Classes like road, highway, parking lots, and synthetic surfaces are genuine material labels. |

### 2. IEEE GRSS DFC 2018 — University of Houston

| Attribute | Detail |
|---|---|
| **Year** | 2018 (acquired Feb 2017) |
| **Domain** | Urban material and vegetation classification |
| **Bands** | **48 hyperspectral** (ITRES CASI-1500, 380–1050 nm, 1 m GSD) + **3-channel multispectral LiDAR** (Optech Titan: 532, 1064, 1550 nm) + VHR RGB (5 cm) |
| **Platform** | Airborne multi-sensor |
| **Classes (20)** | Healthy Grass, Stressed Grass, **Artificial Turf**, Evergreen Trees, Deciduous Trees, **Bare Earth**, Water, Residential Buildings, Non-Residential Buildings, **Roads**, **Sidewalks**, **Crosswalks**, Major Thoroughfares, Highways, Railways, **Paved Parking Lots**, **Unpaved Parking Lots**, Cars, Trains, Stadium Seats |
| **Size** | Large area at 0.5 m GSD ground truth |
| **Annotation** | Pixel-level semantic segmentation |
| **Access** | IEEE DataPort (open access): https://ieee-dataport.org/open-access/2018-ieee-grss-data-fusion-challenge |
| **Paper** | Xu et al., "Advanced Multi-Sensor Optical Remote Sensing for Urban Land Use and Land Cover Classification," *IEEE JSTARS*, 2019 |
| **Relevance** | Explicitly designed for urban material discrimination. The multispectral LiDAR at three wavelengths adds unique material discrimination capability unavailable in any other public dataset. |

### 3. ISPRS Potsdam 2D Semantic Labeling

| Attribute | Detail |
|---|---|
| **Year** | ~2012 |
| **Domain** | Urban aerial semantic segmentation |
| **Bands** | **4 bands**: Blue, Green, Red, NIR at 5 cm GSD; co-registered DSM/nDSM |
| **Platform** | Airborne aerial photography |
| **Classes (6)** | **Impervious Surfaces** (asphalt, concrete, paved), Building, Low Vegetation, Tree, Car, Clutter |
| **Size** | 38 tiles of 6000 × 6000 pixels; 24 with ground truth |
| **Annotation** | Pixel-level semantic segmentation |
| **Access** | https://www.isprs.org/education/benchmarks/UrbanSemLab/ (free registration) |
| **Paper** | Rottensteiner et al., ISPRS 2D Semantic Labeling Contest |
| **Code** | Supported in mmsegmentation, torchgeo |
| **Relevance** | Borderline — "Impervious Surfaces" aggregates asphalt/concrete but does not differentiate between them. Just meets the 4-band threshold. Widely benchmarked. |

**Notable exclusions from this domain:** EuroSAT (13 Sentinel-2 bands but all 10 classes are land-use), BigEarthNet (CORINE land-cover labels), So2Sat LCZ42 (local climate zones, not materials), SEN12MS (IGBP scheme), fMoW (63 functional categories). All have excellent multispectral coverage but fail the material-level annotation filter. RESISC-45, PatternNet, MillionAID, DOTA, iSAID, LoveDA, and OpenEarthMap are all RGB-only.

---

## B. Urban material mapping

This domain contains the richest material-level datasets, driven by decades of airborne hyperspectral research.

### 4. University of Pavia

| Attribute | Detail |
|---|---|
| **Year** | ~2003 (ROSIS campaign) |
| **Domain** | Urban material mapping |
| **Bands** | **103 bands** (ROSIS-03 sensor), 0.43–0.86 µm (VNIR only) |
| **Platform** | Airborne, 1.3 m GSD |
| **Classes (9)** | **Asphalt**, Meadows, **Gravel**, Trees, **Painted Metal Sheets**, **Bare Soil**, **Bitumen**, **Self-Blocking Bricks**, Shadows |
| **Size** | 610 × 610 pixels; 42,776 labeled pixels |
| **Annotation** | Pixel-level classification |
| **Access** | https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes; also Kaggle, HuggingFace |
| **Paper** | Licciardi et al., *IEEE TGRS*, vol. 47(11), 2009 |
| **Code** | DeepHyperX (https://github.com/nshaud/DeepHyperX) and hundreds of implementations |
| **Relevance** | The single most benchmarked hyperspectral material classification dataset. Six of nine classes are construction/urban materials. Gold standard for method comparison. |

### 5. Pavia Centre

| Attribute | Detail |
|---|---|
| **Year** | ~2003 |
| **Bands** | **102 bands** (ROSIS), 0.43–0.86 µm, 1.3 m GSD |
| **Classes (9)** | Water, Trees, **Asphalt**, **Self-Blocking Bricks**, **Bitumen**, **Tiles**, Shadows, Meadows, **Bare Soil** |
| **Size** | 1096 × 1096 pixels |
| **Access** | Same as Pavia University |
| **Relevance** | Companion to Pavia University with additional material class (tiles). |

### 6. Toulouse Hyperspectral Data Set

| Attribute | Detail |
|---|---|
| **Year** | 2024 (acquired June 2021) |
| **Domain** | Large-scale urban material mapping |
| **Bands** | **310 usable channels** (AisaFENIX 1K), 0.4–2.5 µm (**VNIR + SWIR**), spectral resolution 3.6 nm (VNIR) / 7.8 nm (SWIR) |
| **Platform** | Airborne, 1 m GSD, ~90 km² over Toulouse, France |
| **Classes (32)** | **Asphalt, Concrete, Gravel, Red Paving Stone, Brown Paving Stone, Red Porous Concrete**, multiple roof material types, vegetation types, bare soil, water — 16 impermeable + 16 permeable |
| **Size** | >380,000 labeled pixels; multi-tile coverage |
| **Annotation** | Pixel-level semantic segmentation |
| **Access** | Tiles at https://camcatt.sedoo.fr/catalogue/; 1D at https://huggingface.co/datasets/Romain3Ch216/TlseHypDataSet/ |
| **Paper** | Thoreau et al., "Toulouse Hyperspectral Data Set," *ISPRS J. Photogrammetry & Remote Sensing*, vol. 212, pp. 323–337, 2024 |
| **Code** | https://github.com/Romain3Ch216/tlse-experiments |
| **Relevance** | **State-of-the-art for urban material mapping.** Widest spectral range (VNIR + SWIR), finest material-class granularity (32 classes including multiple paving and roof subtypes), and largest spatial coverage of any hyperspectral urban material dataset. |

### 7. Berlin-Urban-Gradient Dataset

| Attribute | Detail |
|---|---|
| **Year** | 2016 (acquired 2009) |
| **Bands** | **~128 bands** (HyMap airborne), 0.4–2.5 µm (VNIR + SWIR), 3.6 m and 9 m GSD; plus simulated EnMAP (244 bands, 30 m) |
| **Platform** | Airborne + simulated satellite |
| **Classes** | Hierarchical urban land cover with spectral endmember library; impervious surfaces, vegetation, soil, water |
| **Access** | GFZ Data Services: https://doi.org/10.5880/enmap.2016.008 (CC-BY-SA 4.0) |
| **Paper** | Okujeni et al., GFZ Data Services, 2016 |
| **Relevance** | Excellent for spectral unmixing of urban materials. Full VNIR–SWIR range with endmember library. |

### 8. MUUFL Gulfport

| Attribute | Detail |
|---|---|
| **Year** | 2013 (acquired Nov 2010) |
| **Bands** | **64 usable bands** (72 acquired), 375–1050 nm (VNIR); co-registered LiDAR |
| **Platform** | Airborne, 1 m GSD; 325 × 220 pixels |
| **Classes (11)** | Trees, Grass, Mixed Ground, **Dirt and Sand**, **Road**, Water, Building Shadow, **Buildings**, **Sidewalk**, Yellow Curb, Cloth Panels |
| **Access** | https://github.com/GatorSense/MUUFLGulfport |
| **Paper** | Gader et al., Univ. of Florida Tech. Rep., 2013 |
| **Relevance** | Includes road, sidewalk, building, and dirt/sand material classes with co-registered LiDAR. |

### 9. MDAS Augsburg

| Attribute | Detail |
|---|---|
| **Year** | 2023 (acquired May 2018) |
| **Bands** | **~180 bands** (HySpex airborne, VNIR + SWIR) + Sentinel-2 (12 bands) + Sentinel-1 SAR + DSM + GIS |
| **Platform** | Airborne (~3 m) + satellite (10 m) |
| **Access** | https://doi.org/10.14459/2022mp1657312 |
| **Paper** | Hu et al., "MDAS: A new multimodal benchmark dataset for remote sensing," *Earth System Science Data*, vol. 15, pp. 113–131, 2023 |
| **Code** | https://github.com/zhu-xlab/augsburg_Multimodal_Data_Set_MDaS |
| **Relevance** | Unique multimodal fusion of airborne hyperspectral with satellite and GIS data over a full city. |

### 10. HYDICE Urban

| Attribute | Detail |
|---|---|
| **Bands** | **162 usable bands** (210 acquired), 400–2500 nm (VNIR + SWIR), 2 m GSD |
| **Endmembers (4–6)** | **Asphalt, Grass, Tree, Roof** (+Dirt, +Metal in 5/6-endmember versions) |
| **Size** | 307 × 307 pixels |
| **Access** | https://lesun.weebly.com/hyperspectral-data-set.html |
| **Relevance** | Classic spectral unmixing benchmark with direct urban material endmembers. |

### 11. MCubeS — Multimodal Material Segmentation

| Attribute | Detail |
|---|---|
| **Year** | 2022 |
| **Domain** | Outdoor road-scene material segmentation |
| **Bands** | **4 modalities**: RGB + NIR (~700–1000 nm) + AoLP (angle of linear polarization) + DoLP (degree of linear polarization) |
| **Platform** | Close-range (vehicle-mounted cameras) |
| **Classes (20)** | **Asphalt, Concrete, Metal, Fabric, Glass, Plaster, Rubber, Leather, Wood, Paper/Cardboard**, Plastic, Ceramic, Stone, Brick, Water, Vegetation, Skin, Food, Sky, Other |
| **Size** | 500 image sets, 42 outdoor road scenes, 1920 × 1080 resolution |
| **Annotation** | Pixel-level semantic segmentation |
| **Paper** | Liang et al., "Multimodal Material Segmentation," *CVPR*, pp. 19800–19808, 2022 |
| **Code** | GitHub (MCubeSNet, MMSFormer, CMNeXt benchmarks) |
| **Relevance** | **Premier close-range material segmentation benchmark.** Demonstrates that adding NIR and polarization to RGB yields +2.7% to +8.7% mIoU improvement. Twenty material-level classes — the most fine-grained material annotation of any multimodal dataset. |

---

## Urban spectral libraries

These lab/field measurement collections provide the highest spectral resolution for material reference spectra.

### 12. KLUM — Karlsruhe Library of Urban Materials

| Attribute | Detail |
|---|---|
| **Year** | 2019 (acquired summer 2018) |
| **Bands** | **2,151 channels**, 350–2500 nm (VNIR + SWIR), 3 nm (VNIR) / 8 nm (SWIR) spectral resolution |
| **Platform** | Field spectroradiometer (Spectral Evolution RS-3500) |
| **Classes (12, 33 subclasses)** | **Asphalt**, **Brick** (red/yellow/white), **Concrete** (grey/dark/light), **Gravel**, **Metal** (copper/zinc/iron), **Natural Stone** (sandstone/granite/marble), **Plaster**, **Roof Tile** (red/brown), **Tar/Bitumen**, **Wood**, **Glass**, **Plastic** |
| **Size** | 181 material samples (97 façade, 46 ground, 38 roof) |
| **Access** | https://github.com/rebeccailehag/KLUM_library |
| **Paper** | Ilehag et al., "KLUM: An Urban VNIR and SWIR Spectral Library," *Remote Sensing*, 11(18), 2149, 2019 |
| **Relevance** | Purpose-built for urban material classification research. Includes metadata on weathering state, surface structure, and solar angle. |

### 13. LUMA SLUM — London Urban Micromet Spectral Library

| Attribute | Detail |
|---|---|
| **Year** | 2014 (samples from 2012) |
| **Bands** | Continuous VIS-SWIR (350–2500 nm) + LWIR emissivity (8–14 µm) |
| **Platform** | Field spectroradiometer + FTIR |
| **Classes (10)** | **Asphalt/Tarmac, Concrete, Stone/Rock, Brick, Roofing (slate, tile), Metal (aluminium, zinc, iron), Glass, Rubber, PVC, Composite** |
| **Size** | 74 material samples |
| **Access** | https://doi.org/10.5281/zenodo.4263842 |
| **Paper** | Kotthaus et al., "Derivation of an urban materials spectral library," *ISPRS JPRS*, vol. 94, pp. 194–212, 2014 |
| **Relevance** | Unique dual-range (reflectance + emissivity) coverage. Directly relevant to the thesis as it includes PVC and rubber alongside construction materials. |

### 14. WaRM — Walloon Roof Material Spectral Library

| Attribute | Detail |
|---|---|
| **Year** | 2023 |
| **Bands** | **2,151 bands**, 350–2500 nm (ASD FieldSpec3) |
| **Classes (7)** | **Metals, Tiles, Slates, Membranes, PVC, Solar Panels, Corrugated asbestos-cement sheets** |
| **Size** | 26 roof material spectra |
| **Access** | https://doi.org/10.5281/zenodo.7414740 (CC-BY-ND-SA) |
| **Paper** | Hallot, "WaRM: A Roof Material Spectral Library for Wallonia, Belgium," *Data*, 8(3), 59, 2023 |
| **Relevance** | Specifically targets hazardous material detection (asbestos-cement) — directly analogous to illegal waste material identification. |

---

## C. Mineral and geology mapping

Geological hyperspectral datasets represent the longest-established application of spectral material classification, with mineral identification predating all other domains.

### 15. Cuprite, Nevada (AVIRIS)

| Attribute | Detail |
|---|---|
| **Year** | Multiple acquisitions 1990–2008; standard scene from 1997 |
| **Bands** | **224 bands** (188 usable), 370–2480 nm (VNIR + SWIR), ~10 nm spectral resolution |
| **Platform** | Airborne (AVIRIS/NASA-JPL), 20 m GSD |
| **Classes (12–14)** | **Alunite, Andradite, Buddingtonite, Dumortierite, Kaolinite (2 variants), Muscovite, Montmorillonite, Nontronite, Pyrope, Sphene, Chalcedony** |
| **Size** | ROI of 250 × 190 pixels; full flight line ~604 MB |
| **Annotation** | Abundance maps (fractional endmember abundances per pixel) validated against USGS ground-truth mineral maps |
| **Access** | https://aviris.jpl.nasa.gov/data/free_data.html; processed .mat files at http://www.escience.cn/people/feiyunZHU/Dataset_GT.html |
| **Paper** | Swayze et al., "Mapping Advanced Argillic Alteration at Cuprite," *Economic Geology*, 109, 1179–1221, 2014 |
| **Relevance** | The gold-standard geological benchmark. Directly demonstrates that spectral data can identify minerals at the molecular level — the strongest evidence for spectral material classification. |

### 16. USGS Spectral Library Version 7

| Attribute | Detail |
|---|---|
| **Year** | 2017 |
| **Bands** | Continuous UV to far-infrared (0.2–200 µm); thousands of wavelength points per spectrum |
| **Type** | Reference spectral library (not imaging) |
| **Materials** | **1,300+ spectra**: minerals (clays, carbonates, sulfates, oxides, silicates), soils, rocks, coatings, man-made materials, vegetation, organics |
| **Access** | https://doi.org/10.5066/F7RR1WDJ (free) |
| **Paper** | Kokaly et al., "USGS Spectral Library Version 7," USGS Data Series 1035, 2017 |
| **Relevance** | The fundamental reference for all spectral material classification. Every mineral/material mapping algorithm ultimately traces back to this or the ECOSTRESS library for validation. |

### 17. ECOSTRESS Spectral Library

| Attribute | Detail |
|---|---|
| **Year** | 2018 (builds on ASTER Spectral Library 2.0, 2009) |
| **Bands** | Visible to thermal infrared (0.4–15.4 µm) |
| **Materials** | **>3,400 spectra**: minerals, rocks, soils, vegetation, man-made materials |
| **Access** | https://speclib.jpl.nasa.gov/ |
| **Paper** | Meerdink et al., "The ECOSTRESS spectral library version 1.0," *Remote Sensing of Environment*, 230, 111196, 2019 |
| **Relevance** | Complements USGS library with thermal-infrared emissivity spectra critical for silicate mineral discrimination. |

### 18. NASA EMIT — Earth Surface Mineral Dust Source Investigation

| Attribute | Detail |
|---|---|
| **Year** | 2022 (launched July 2022, extended through 2026+) |
| **Bands** | **285 bands**, 381–2493 nm (VSWIR), ~7.4 nm spectral resolution |
| **Platform** | Spaceborne (ISS), **60 m** spatial resolution, 72 km swath |
| **Classes (10 mineral groups)** | **Hematite, Goethite, Illite, Vermiculite, Montmorillonite, Kaolinite, Chlorite, Calcite, Dolomite, Gypsum** |
| **Size** | Global coverage 52°N–52°S; thousands of granules |
| **Annotation** | Per-pixel mineral identification maps + fractional mineralogy + uncertainty |
| **Access** | https://search.earthdata.nasa.gov/ (free) |
| **Paper** | Green et al., "EMIT Earth Surface Mineral Dust Source Investigation," 2022/2023 |
| **Code** | https://github.com/nasa/EMIT-Data-Resources |
| **Relevance** | First global-scale mineral classification from space. Pre-classified products available. Demonstrates industrial-scale material classification from spectral data. |

### 19. EnGeoMAP Test Data (Simulated EnMAP)

| Attribute | Detail |
|---|---|
| **Year** | 2016 |
| **Bands** | **242 bands** (simulated EnMAP), 420–2450 nm, 30 m |
| **Sites** | Mountain Pass, CA (REE deposit, from AVIRIS-NG) and Rodalquilar, Spain (gold-alunite deposit, from HyMap) |
| **Minerals** | Calcite, bastnaesite (REE), alunite, kaolinite, montmorillonite, chlorite, silica |
| **Access** | https://doi.org/10.5880/enmap.2016.001 |
| **Paper** | Mielke et al., "EnGeoMAP 2.0 — Automated Hyperspectral Mineral Identification," *Remote Sensing*, 8, 127, 2016 |
| **Relevance** | Designed specifically for benchmarking mineral identification algorithms, including rare earth element detection. |

---

## D. Marine and floating debris detection

This domain has seen rapid dataset growth since 2021, driven by ESA and EU funding. **Sentinel-2's 11–13 bands provide SWIR coverage essential for discriminating plastics from natural floating materials.**

### 20. MARIDA — Marine Debris Archive

| Attribute | Detail |
|---|---|
| **Year** | 2022 |
| **Bands** | **11 Sentinel-2 bands** (B1–B8A, B11, B12), 443–2190 nm, atmospherically corrected via ACOLITE |
| **Platform** | Satellite (Sentinel-2 MSI), 10/20/60 m |
| **Classes (15)** | **Marine Debris**, Dense Sargassum, Sparse Sargassum, Natural Organic Material, Ship, Clouds, Marine Water, Sediment-Laden Water, Foam, Turbid Water, Shallow Water, Waves, Cloud Shadows, Wakes, Mixed Water |
| **Size** | 1,381 patches (256 × 256 px); ~837,357 annotated pixels; 63 dates, 2015–2021 |
| **Annotation** | Pixel-level semantic segmentation with 3-level confidence |
| **Access** | https://doi.org/10.5281/zenodo.5151941 (Zenodo) |
| **Paper** | Kikaki et al., "MARIDA: A benchmark for Marine Debris detection from Sentinel-2 remote sensing data," *PLoS ONE*, 17(1), e0262247, 2022 |
| **Code** | https://github.com/marine-debris/marine-debris.github.io |
| **Relevance** | Premier satellite-scale marine debris benchmark. Does not distinguish polymer types but separates anthropogenic debris from natural floating materials — essential baseline for waterway waste monitoring. |

### 21. MADOS — Marine Debris and Oil Spill

| Attribute | Detail |
|---|---|
| **Year** | 2024 |
| **Bands** | **13 Sentinel-2 bands** (native multi-resolution preserved) |
| **Classes (15)** | **Marine Debris, Oil Spill**, Dense Sargassum, Sparse Floating Algae, Ships, Oil Platforms, Jellyfish, Sea Snot, + water/atmospheric classes |
| **Size** | 174 scenes (47 tiles), 2,803 image crops, ~1.5M annotated pixels, 22+ countries |
| **Annotation** | Pixel-level sparse semantic segmentation with confidence levels |
| **Access** | https://doi.org/10.5281/zenodo.10664073 |
| **Paper** | Kikaki et al., "Detecting Marine Pollutants and Sea Surface Features," *ISPRS JPRS*, 210, 39–54, 2024 |
| **Code** | https://github.com/gkakogeorgiou/mados (MariNeXt framework) |
| **Relevance** | Extends MARIDA with oil spills and broader pollution types. Larger and more diverse. |

### 22. FloatingObjects (ESA Φ-Lab)

| Attribute | Detail |
|---|---|
| **Year** | 2021 |
| **Bands** | **12–13 Sentinel-2 bands** (L1C/L2A) |
| **Classes** | Binary: floating objects vs. water |
| **Size** | 26 globally distributed scenes; 3,297 annotated objects |
| **Access** | https://github.com/ESA-PhiLab/floatingobjects |
| **Paper** | Mifdal et al., "Towards Detecting Floating Objects on a Global Scale," *ISPRS Annals* V-3-2021, 285–293, 2021 |
| **Relevance** | Binary detection only but provides global-scale coverage using full Sentinel-2 band stack. |

### 23. Floating-Marine-Debris-Data (Duarte et al.)

| Attribute | Detail |
|---|---|
| **Year** | 2023–2024 |
| **Bands** | **13 Sentinel-2 bands** |
| **Classes (6 floating material types)** | **Plastic, Driftwood, Seaweed (Sargassum), Pumice, Sea Snot, Sea Foam** + Water |
| **Size** | Largest freely available pixel-level floating debris dataset; includes 50K synthetic pixels per class (WGAN-augmented) |
| **Access** | https://github.com/miguelmendesduarte/Floating-Marine-Debris-Data |
| **Relevance** | **Critically important**: six material-level floating debris classes from Sentinel-2, distinguishing plastic from natural materials. Directly supports material-level classification at satellite scale. |

### 24. Plastic Litter Projects (PLP 2018/2019/2021)

| Attribute | Detail |
|---|---|
| **Year** | 2019–2022 (three campaigns) |
| **Bands** | **13 Sentinel-2 bands** + UAV hyperspectral (PLP 2021) |
| **Classes** | Known artificial targets: **PET bottles, LDPE bags, wooden planks**; subpixel abundance fractions |
| **Size** | PLP 2019: 5 dates, 12 × 12 px subsets; PLP 2021: 22 S2 images + UAV |
| **Access** | https://doi.org/10.5281/zenodo.3752719 (PLP 2019); https://doi.org/10.5281/zenodo.7085112 (PLP 2021) |
| **Paper** | Topouzelis et al., "Detection of floating plastics from satellite and UAV," *Int. J. Appl. Earth Obs. Geoinf.*, 79, 175–183, 2019 |
| **Relevance** | Controlled experiments with known polymer targets. Critical for spectral unmixing validation and subpixel detection. |

### 25. MADLib — Marine Debris Hyperspectral Reference Library

| Attribute | Detail |
|---|---|
| **Year** | 2025 |
| **Bands** | Hyperspectral UV–SWIR (350–2500 nm), compiled from multiple spectroradiometer datasets |
| **Classes** | Multiple polymer types (**PE, PP, PET, PS, HDPE, LDPE, nylon**), various colors, sizes, weathering states, dry/wet/submerged conditions; also natural debris (algae, wood, shells) |
| **Size** | **24,889 reflectance spectra** from 3,032 samples |
| **Access** | https://doi.org/10.4121/059551d3-2383-4e20-af2d-011c9a59d3ac (4TU.ResearchData) |
| **Paper** | Ohall et al., "The MArine Debris hyperspectral reference Library collection (MADLib)," *Earth Syst. Sci. Data*, 17, 7293–7311, 2025 |
| **Relevance** | **Definitive comprehensive spectral reference for marine debris.** Harmonized, FAIR-compliant. Includes polymer-specific spectra across the full UV–SWIR range. Essential for developing material-specific detection algorithms. |

### 26. Garaba & Dierssen Marine Plastic Spectral Libraries

| Attribute | Detail |
|---|---|
| **Year** | 2017–2020 |
| **Bands** | Hyperspectral UV–SWIR (350–2500 nm), ASD FieldSpec 4 |
| **Classes** | 11 virgin plastic pellet types (**PE, PP, PET, PS, PVC, HDPE, LDPE, nylon**), marine-harvested macro/microplastics |
| **Access** | EcoSIS: https://doi.org/10.21232/C27H34 (virgin pellets); https://doi.org/10.21232/ex5j-0z25 (macroplastics); https://doi.org/10.21232/r7gg-yv83 (microplastics) |
| **Paper** | Garaba & Dierssen, *ESSD*, 12, 77–86, 2020 |
| **Relevance** | Foundational polymer-specific spectral reference. SWIR absorption features at **1215, 1410, 1730 nm** are diagnostic for polymer discrimination. |

### 27. Knaeps et al. — Submerged Marine Litter Spectra

| Attribute | Detail |
|---|---|
| **Year** | 2021 |
| **Bands** | Hyperspectral 350–2500 nm (ASD + Spectral Evolution instruments) |
| **Classes** | 47 plastic specimens (virgin + real samples from Port of Antwerp), measured dry/wet/submerged at varying turbidity |
| **Access** | https://doi.org/10.4121/12896312.v2 (4TU.ResearchData) |
| **Paper** | Knaeps et al., *ESSD*, 13, 713–730, 2021 |
| **Relevance** | Unique dataset showing how water column degrades plastic spectral signatures — critical for riverine and coastal waste monitoring. |

### 28. Olyaei et al. — River Plastic Hyperspectral Database

| Attribute | Detail |
|---|---|
| **Year** | 2024 |
| **Bands** | Hyperspectral 350–2500 nm |
| **Classes** | **PET, HDPE, LDPE, PP, PS, EPS** — virgin and weathered, in clear/turbid/foamy water |
| **Size** | NetCDF files with reflectance spectra + RGB images + pixel-level segmentation masks with fractional abundance |
| **Access** | https://doi.org/10.5281/zenodo.13377060 |
| **Paper** | Olyaei et al., "A Hyperspectral Reflectance Database of Plastic Debris with Different Fractional Abundance in River Systems," *Scientific Data*, 11, 1253, 2024 |
| **Relevance** | **First freshwater plastic hyperspectral database** with polymer-level classes and fractional abundance. Directly relevant to river-based illegal dumping monitoring. |

---

## E. Agricultural material classification

Agricultural hyperspectral datasets treat crops, soils, and residues as distinct material classes, providing strong evidence that spectral data resolves materials that appear identical in RGB.

### 29. Indian Pines (AVIRIS)

| Attribute | Detail |
|---|---|
| **Year** | 1992 (data); benchmark since ~2000 |
| **Bands** | **200 bands** (224 acquired, 24 removed), 400–2500 nm (VNIR + SWIR), 20 m |
| **Platform** | Airborne (AVIRIS) |
| **Classes (16)** | Alfalfa, Corn-notill, Corn-mintill, Corn, Grass-pasture, Grass-trees, Grass-pasture-mowed, Hay-windrowed, Oats, Soybean-notill, Soybean-mintill, Soybean-clean, Wheat, Woods, Buildings-Grass-Trees-Drives, **Stone-Steel-Towers** |
| **Size** | 145 × 145 px; ~10,249 labeled pixels |
| **Access** | http://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes |
| **Paper** | Baumgardner et al., 2015; Purdue DOI: 10.4231/R7RX991C |
| **Relevance** | Crop types and soil tillage practices as material classes. Widely benchmarked for band selection studies. |

### 30. Salinas (AVIRIS)

| Attribute | Detail |
|---|---|
| **Year** | ~1998 |
| **Bands** | **204 bands**, 400–2500 nm, 3.7 m |
| **Platform** | Airborne (AVIRIS) |
| **Classes (16)** | Broccoli (2 variants), Fallow, Fallow-rough-plow, Fallow-smooth, Stubble, Celery, Grapes, **Soil-vinyard-develop**, Corn, Lettuce (4 growth stages), Vinyard (2 variants) |
| **Size** | 512 × 217 px; ~54,129 labeled pixels |
| **Access** | Same EHU site |
| **Relevance** | Fine-grained crop material classification including lettuce at multiple growth stages and different soil/fallow types. |

### 31. WHU-Hi Datasets (three scenes)

| Attribute | Detail |
|---|---|
| **Year** | 2020 (published) |
| **Bands** | **270–274 bands**, 400–1000 nm (VNIR), Headwall Nano-Hyperspec |
| **Platform** | UAV (DJI M600 Pro), 0.04–0.46 m GSD |
| **Scenes** | **LongKou** (9 classes, 550 × 400 px): corn, cotton, sesame, soybean (broad/narrow leaf), rice, water, roads, weed. **HanChuan** (16 classes): includes **plastic**, bare soil, roof types. **HongHu** (22 classes): 15 vegetable cultivar types + **red roof, road, bare soil** |
| **Size** | >204K labeled pixels (LongKou alone) |
| **Access** | http://rsidea.whu.edu.cn/; Kaggle; HuggingFace |
| **Paper** | Zhong et al., *Remote Sensing of Environment*, 250, 112012, 2020 |
| **Relevance** | Highest-resolution agricultural hyperspectral benchmark. HanChuan scene includes **plastic** as a class — directly relevant to agricultural plastic waste detection. |

### 32. LUCAS Soil Spectral Library

| Attribute | Detail |
|---|---|
| **Year** | 2009–2018 (three campaigns) |
| **Bands** | ~**1,050 bands** at 2 nm resolution, 400–2500 nm (VNIR + SWIR) |
| **Type** | Lab spectra (FOSS XDS Rapid Content Analyzer) |
| **Properties** | pH, organic carbon, N, P, K, CEC, CaCO₃, texture (clay/silt/sand), electrical conductivity |
| **Size** | **~45,000 European topsoil samples** across three campaigns |
| **Access** | https://esdac.jrc.ec.europa.eu/content/lucas-2009-topsoil-data (free registration); also via OSSL: https://soilspectroscopy.org |
| **Paper** | Tóth et al., 2013; Orgiazzi et al., *European Journal of Soil Science*, 69, 140–153, 2018 |
| **Relevance** | Largest harmonized European soil spectral library. Demonstrates spectral prediction of material composition (mineral/organic fractions). |

### 33. Open Soil Spectral Library (OSSL)

| Attribute | Detail |
|---|---|
| **Year** | 2022–present |
| **Bands** | VisNIR (350–2500 nm) + MIR (600–4000 cm⁻¹) + NIR-Neospectra (1350–2550 nm) |
| **Size** | **>100,000 spectra** aggregating KSSL (USDA), ICRAF-ISRIC, LUCAS, AfSIS |
| **Access** | https://soilspectroscopy.org (API + bulk download) |
| **Paper** | Safanelli et al., *PLoS ONE*, 2025 |
| **Code** | https://github.com/soilspectroscopy |
| **Relevance** | Unified global platform for soil material spectroscopy. |

---

## F. Waste and recycling

This domain is most directly relevant to the thesis. Datasets are emerging rapidly but remain sparse compared to other domains.

### 34. SpectralWaste

| Attribute | Detail |
|---|---|
| **Year** | 2024 |
| **Domain** | Industrial plastic waste sorting (real facility, conveyor belt) |
| **Bands** | Hyperspectral line-scan camera (co-registered with RGB); PCA-reduced 3-band versions also provided |
| **Classes (6)** | **Film, Basket, Video Tape, Filament, Trash Bag, Cardboard** |
| **Size** | ~1,200 labeled multimodal images + 6,803 unlabeled; 23 GB preprocessed |
| **Annotation** | Pixel-level semantic segmentation |
| **Access** | Zenodo (23 GB preprocessed); https://sites.google.com/unizar.es/spectralwaste |
| **Paper** | Casao et al., "SpectralWaste Dataset: Multimodal Data for Waste Sorting Automation," *IEEE/RSJ IROS*, pp. 5852–5858, 2024 |
| **Code** | https://github.com/ferpb/spectralwaste-segmentation |
| **Relevance** | **First public multimodal (HSI + RGB) dataset from an operational waste sorting plant.** Operationally focused classes. |

### 35. Tecnalia WEEE Hyperspectral Dataset

| Attribute | Detail |
|---|---|
| **Year** | 2024 (cleaned release; original data from 2010) |
| **Domain** | E-waste / WEEE metal sorting |
| **Bands** | **76 bands**, 415–1008 nm (VNIR), Specim PHF Fast10 |
| **Platform** | Conveyor belt imaging (1024 × 1024 sensor) |
| **Classes (5)** | **Copper, Brass, Aluminum, Stainless Steel, White Copper** (+ background) |
| **Size** | 13 hyperspectral scenes with ground-truth masks |
| **Annotation** | Pixel-level classification masks |
| **Access** | https://zenodo.org/records/12565131 |
| **Paper** | Picon et al., "On the analysis of adapting deep learning methods to hyperspectral imaging," *Spectrochimica Acta Part A*, 330, 125665, 2024 |
| **Code** | https://github.com/samtzai/tecnalia_weee_hyperspectral_dataset |
| **Relevance** | Only public hyperspectral dataset for E-waste metal sorting. Material-level (metal type) classification with pixel-level masks. |

### 36. RECONMATIC — CDW Hyperspectral Dataset

| Attribute | Detail |
|---|---|
| **Year** | 2024 |
| **Domain** | Construction & demolition waste (lab) |
| **Bands** | Hyperspectral cubes with calibrated wavelength information |
| **Classes** | **Mortar, Concrete, Brick, Wood, Gypsum, Foam, Plastic** and other CDW materials |
| **Access** | https://doi.org/10.5281/zenodo.14294262 |
| **Paper** | Part of EU Horizon project RECONMATIC (grant 101058580) |
| **Code** | Included (feature extraction, MLP training scripts) |
| **Relevance** | Directly relevant to construction waste classification — a common type of illegal dumping. |

### 37. WoodVIT — Multimodal Bulky Waste Dataset

| Attribute | Detail |
|---|---|
| **Year** | 2026 |
| **Domain** | Bulky waste sorting (C&D waste) |
| **Bands** | 4 modalities: VIS/RGB + **NIR hyperspectral** + temporal IR thermography + THz imaging |
| **Classes** | Wood vs. Non-Wood + **16 subclasses** (plastic, foam, textile, metal, cardboard, etc.) |
| **Size** | 56 multi-sensor scenes; 22,659 annotated patches |
| **Annotation** | Pixel-level masks + patch-wise labels |
| **Paper** | "Multimodal and Hyperspectral Dataset for Segmentation of Bulky Waste," *Scientific Data*, Nature, 2026 |
| **Relevance** | Novel multi-sensor dataset demonstrating that NIR HSI alone struggles with black/painted objects but adds significant value for material separation. |

### 38. Hyperspectral Scrap Metal Dataset

| Attribute | Detail |
|---|---|
| **Year** | 2025 |
| **Domain** | Metal scrap sorting for steel recycling |
| **Bands** | Hyperspectral imaging |
| **Classes** | Unsorted industrial metal scrap + contaminant materials (**wood, plastic** in metal streams) |
| **Access** | https://zenodo.org/records/17076239 |
| **Relevance** | Includes contaminant detection in recycling streams — directly relevant to waste quality control. |

**Key exclusion from this domain:** AerialWaste (Torres & Fraternali, 2023) is **RGB-only** and does not meet the ≥4 spectral bands filter. TrashNet, WasteNet, and TACO are also RGB-only.

---

## G. Construction and infrastructure

Most construction material datasets are captured under urban material mapping (Section B). The Toulouse dataset (#6), KLUM (#12), LUMA SLUM (#13), WaRM (#14), and RECONMATIC (#36) are the most relevant. No dedicated standalone multispectral road pavement classification benchmark exists as a downloadable dataset — researchers typically use custom HyMap/CASI acquisitions or field spectroradiometry.

---

## H. Textile and polymer sorting

Industrial sorting datasets are rapidly emerging, driven by EU circular economy mandates.

### 39. NIST NIR-SORT

| Attribute | Detail |
|---|---|
| **Year** | v1.0: January 2025; v2.0: March 2026 |
| **Domain** | Textile fiber identification for recycling |
| **Bands** | NIR spectroscopy, ~800–2500 nm; multiple instruments for cross-validation |
| **Classes** | **64+ fabric types**: cotton, polyester, nylon, wool, silk, spandex blends, real-world thrift store fabrics |
| **Size** | 64 fabric types (v1.0); expanded in v2.0 with dyed fabrics and additional instruments |
| **Access** | https://data.nist.gov/pdr/lps/ark:/88434/mds2-3325 |
| **Paper** | NIST Technical publications (in development) |
| **Relevance** | Gold-standard textile sorting reference from NIST. Multiple NIR instruments for cross-validation make it the most authoritative textile spectral dataset. |

### 40. Open Specy Community Library

| Attribute | Detail |
|---|---|
| **Year** | 2021 (initial); v1.0 2025 with 40,000+ spectra |
| **Domain** | Microplastic and polymer identification |
| **Bands** | Combined FTIR (400–4000 cm⁻¹) and Raman spectra |
| **Classes** | **600+ reference materials** including all major plastic types, organic matter, minerals |
| **Size** | **40,000+ spectra** (community-contributed, continuously growing) |
| **Access** | https://www.openanalysis.org/openspecy/; R package on CRAN; https://github.com/wincowgerDEV/OpenSpecy |
| **Paper** | Cowger et al., *Analytical Chemistry*, 93(21), 7543–7548, 2021; updated 2025 |
| **Relevance** | Largest open-access polymer spectral library with built-in ML classifiers. Community-maintained, FAIR-compliant. |

### 41. FLOPP / FLOPP-e (FTIR Polymer Libraries)

| Attribute | Detail |
|---|---|
| **Year** | 2021 |
| **Bands** | ATR-FTIR, 400–4000 cm⁻¹ |
| **Classes** | FLOPP: **14 polymer types** (PE, PP, PS, PET, PVC, PA, PC, PMMA, ABS, PUR, PTFE, silicone, cellulose acetate, rubber); FLOPP-e: 15 weathered variants |
| **Size** | 381 spectra total |
| **Access** | https://acs.figshare.com/articles/dataset/17070065 |
| **Paper** | De Frond et al., *Analytical Chemistry*, 93(48), 15878–15885, 2021 |
| **Relevance** | Open-access FTIR reference library including both pristine and environmentally weathered polymer spectra. |

### 42. FTIR-Plastics (C4/C8)

| Attribute | Detail |
|---|---|
| **Year** | 2024 |
| **Bands** | FTIR, 4000–400 cm⁻¹; 3,751 features (C4) / 1,884 features (C8) |
| **Classes (6)** | **PET, HDPE, PVC, LDPE, PP, PS** |
| **Size** | 6,000 spectra (500 per polymer × 6 × 2 configurations) |
| **Access** | https://zenodo.org/records/10736650 |
| **Paper** | Villegas-Camacho et al., *Data in Brief*, 2024 |
| **Relevance** | Standardized, large-scale benchmark for the six most prevalent industrial polymers. Designed for ML/DL classification. |

---

## Quantitative evidence that spectral bands beyond RGB improve material classification

The evidence across domains is unambiguous. The table below summarizes the most rigorous quantitative comparisons from 2022–2026 literature.

| Study | Domain | RGB / Baseline | With extra bands | Gain | Key bands |
|---|---|---|---|---|---|
| MMSFormer (2024) | Road materials, 20 classes | 50.4% mIoU | 53.1% mIoU (RGB+NIR+pol.) | **+2.7%** | NIR, polarization |
| CMNeXt (CVPR 2023) | Road materials, 20 classes | 42.9% mIoU | 51.5% mIoU (4 modalities) | **+8.7%** | NIR, polarization |
| Façade classification (2022) | Building materials, 5 classes | 80% (5-band MS) | 99% (240-band SWIR) | **+19%** | SWIR 1000–2500 nm |
| Sentinel-2 meta-analysis (2025) | Urban mapping | RGB baseline | Full 13-band | **+15–20%** | SWIR (B11, B12) |
| WV-3 urban (2016) | Urban materials | VNIR only | VNIR + SWIR | **+20%** | SWIR 1184–2373 nm |
| Le Bris et al. (2016) | Urban materials | κ = 0.78 (VNIR 4-band) | κ = 0.82 (VNIR+SWIR 4-band) | **+0.04 κ** | Blue, Green, NIR, SWIR |
| Tumor grading (2024) | Tissue materials | 80% (RGB) | 86% (16-band MS) | **+6%** | Optimal 10 of 16 bands |

Three cross-cutting findings emerge from the band importance literature. First, **SWIR (1000–2500 nm) is the single most critical spectral region for material discrimination**, consistently providing the largest accuracy gains (15–20% for urban materials, essential for polymer identification). Nearly **48% of the most important bands for roof material classification** fall in the SWIR region, despite it representing only half the total spectral range. Second, **NIR (700–1000 nm) provides moderate but consistent gains** of 2–6%, particularly for detecting water, wet surfaces, and vegetation/non-vegetation boundaries. Third, **optimal band subsets of 4–10 wavelengths can match or exceed full-spectrum performance** — Kumar et al. (2024) achieved 99.9% OA on Indian Pines with selected bands, and deep band selection methods (Martinez et al., 2026) outperformed full-spectrum baselines by ~1%.

For plastic and polymer classification specifically, the evidence is absolute: **visible-only imagery cannot discriminate between polymer types** that appear identical in RGB. The diagnostic polymer absorption features at **1215, 1410, and 1730 nm** (all in the SWIR) are the basis for all industrial NIR sorting systems. Every benchmark study on plastic waste sorting confirms that NIR/SWIR channels are not merely helpful but strictly necessary for polymer-level material identification.

---

## The gap that defines the thesis opportunity

This catalog reveals a structural gap at the intersection of waste detection and remote sensing. Satellite-scale datasets (MARIDA, MADOS) detect marine debris but do not classify polymer types. Lab spectral libraries (MADLib, Garaba, FLOPP) identify polymers precisely but exist as point measurements without spatial context. Industrial sorting datasets (SpectralWaste, Tecnalia WEEE) operate on conveyor belts, not in open environments. **No public multispectral dataset addresses illegal terrestrial waste dumping** — the precise scenario of greatest regulatory interest.

The most promising path for a thesis on illegal waste detection is to bridge these domains: use satellite multispectral imagery (Sentinel-2's SWIR bands B11 and B12 at 1610 and 2190 nm) for site-level anomaly detection, combined with UAV-mounted hyperspectral sensors for material-level confirmation. The cross-domain evidence cataloged here — from mineral mapping's decades of validated spectral classification to marine debris detection's polymer discrimination — provides strong justification that multispectral bands beyond RGB are not optional but essential for this task.

---

# Addendum — June 2026 (deep-research rounds, adversarially verified)

Three fan-out deep-research passes (June 2026) were run to surface datasets **overlooked** by the catalog above, then verified claim-by-claim (3-vote adversarial). Net result: the **core gap holds** — still no public *multispectral-satellite + terrestrial-waste + material-label* dataset. A handful of genuinely new resources emerged, almost all in the asbestos / roof-material track. SWIR presence is flagged explicitly since SuperDove (the thesis sensor) is VNIR-only.

## A. Genuinely new dataset finds

| Resource | Year | Platform / sensor | GSD | Bands (SWIR?) | Labels / task | Access | Role for thesis |
|---|---|---|---|---|---|---|---|
| **Cartagena de Indias asbestos-cement** (Heliyon 2024) | 2024 | **Airborne** HySpex Mjolnir VS-620 | 0.4 m (→0.8 m) | 490 (200 VNIR + **290 SWIR**, 400–2500 nm) ✅ | AC roof detection/classification | **On request only** (not public) | Gold-standard upper bound for asbestos with SWIR; only a literature/on-request reference |
| **SpectralEarth** (TUM/DLR 2024) | 2024 | EnMAP HSI (spaceborne) | 30 m | 224 (**SWIR**, 420–2450 nm) ✅ | self-supervised pretraining (538,974 patches) | public | FM pretraining reference (HSI), not a material-label set |
| **RoofNet** | 2025 | global EO tiles | — | RGB/MS | **14 roof-material classes** (NO asbestos), classification (51,503 tiles, 112 countries) | CC-BY-NC 4.0, [GitHub](https://github.com/noellelaw/roofnet) | roof-material taxonomy; asbestos must be added separately |
| **RoofSense** | 2025 | aerial + LiDAR (NL) | 8 cm | RGB+LiDAR (no SWIR) | 8 roof materials (NO asbestos), segmentation (300 masks) | MIT / HuggingFace | roof-segmentation methodology reference |
| **Nacala-Roof-Material** | 2025 | DJI Phantom 4 Pro drone (RGB) | 4.4 cm | RGB (no SWIR) | **explicit asbestos class** (566 of 17,954 buildings), det/class/seg | public, [arXiv](https://arxiv.org/abs/2406.04949) | rare public asbestos-roof ground truth; RGB-only, ~100× finer than SuperDove |
| **GlobalBuildingMap (GBM)** | 2024 | **PlanetScope** (3 m) | 3 m | VNIR (no SWIR) | binary building masks (~790k images) | CC-BY-4.0 masks ([GitHub](https://github.com/zhu-xlab/GlobalBuildingMap)); imagery NOT redistributable | building/roof-localization pre-step on the same 3 m Planet platform |
| **FloodPlanet** | 2023 | PlanetScope + S1/S2/L8 (cross-sensor) | 3 m | VNIR (no SWIR) | flood semantic segmentation (366 chips, co-registered) | public ([paper](https://spj.science.org/doi/10.34133/remotesensing.0575)) | rare *cross-sensor paired* annotated example (likely Dove-Classic, NOT 8-band SuperDove) |

## B. VNIR-only asbestos baselines (not SWIR, but directly relevant)

These two were chased specifically. **Both are VNIR-only** — and that is exactly why they matter: they show 8 VNIR bands can classify asbestos-cement at high accuracy, *supporting* the SuperDove pilot framing.

| Paper | Sensor | SWIR? | Task / result | Note |
|---|---|---|---|---|
| **Hikuwai et al. 2023** (Sustainability, doi:10.3390/su15054276) | WV-3 **VNIR** (ceiling ~920 nm) | ❌ | Mask R-CNN instance seg; aerial 94% vs satellite ~63% precision; W. Sydney | data not public |
| **Saba et al. 2026** (J. Hazardous Materials, S0304389426008423) | WV-3 **VNIR 8-band** @1.24 m (by design) | ❌ | 32 classifiers; Fine-KNN **F1 97.6%** multiclass, ~99–100% binary AC; signal in red-edge+NIR | ⭐ near-competitor / strong precedent for the VNIR-only asbestos thesis; paywalled |

## C. Access routes & spectral references (not labeled datasets)

- **WV-3 SWIR imagery via ESA eoGateway** — full WV-3 archive incl. SWIR up to **3.7 m**, **free to ESA-member (Italy/PoliMi) researchers** after project proposal (~9-week eval). Raw imagery only, **no labels** (self-annotate). → makes the WV-3 SWIR *validation track* feasible. [link](https://earth.esa.int/eogateway/catalog/worldview-3-full-archive-and-tasking)
- **USGS WV-3 SWIR mosaic** (Maryland, DOI 10.5066/F7FF3R8Z, ~581 MB GeoTIFF) — WV-3 SWIR surface-reflectance imagery, no thematic labels → pipeline-test data.
- **Asbestos spectral physics** — chrysotile diagnostic SWIR features at **1.385 µm (OH)** and **2.323 µm (Mg-OH)**; the 2.32 µm Mg-OH band is the satellite workhorse → explains *why* SWIR is the upper bound and what SuperDove (VNIR) loses.
- **EnMAP asbestos-cement field library** (SciReports 2025, doi:10.1038/s41598-025-09738-w) — 2,714 spectra incl. weathered / moss-covered / paint-sealed AC; on request, Israel campaign.

## D. Negative results (worth citing — they reinforce the gap)

- **Terrestrial waste/plastic + SWIR:** no *new* dataset. Every SWIR-plastic hit was already ours (Aguilar WV-3, Zhou WV-3, Olyaei river-plastic).
- **Recent spaceborne material-level benchmarks + SWIR:** see the mission-by-mission breakdown in section F — net result **negative** across PRISMA / EnMAP / EMIT / Tanager-1.

## F. Mission-by-mission spaceborne SWIR HSI (June 2026 targeted pass)

**Headline: no public material-level-labeled benchmark exists for any current SWIR-carrying spaceborne imaging spectrometer.** The labeled SWIR data that *is* public is overwhelmingly **trace-gas plume masks** (methane/CO₂), not surface materials — STARCOP (AVIRIS-NG), UNEP-IMEO MARS-Hyperspectral (PRISMA/EnMAP/EMIT), Carbon Mapper/Tanager-1. This is itself a citable finding: it confirms SWIR is the operative absorption-feature region, while the *solid-material* benchmark gap is industry-wide.

| Mission | Bands / SWIR | Verdict | Detail |
|---|---|---|---|
| **PRISMA** | ~240, 400–2500 nm ✅ | ❌ negative | only methane-plume labels (MARS-Hyperspectral); landfill studies output risk-score maps, no benchmark |
| **EnMAP** | ~224, 420–2450 nm ✅ | ❌ negative | new labeled sets (H2Crop, HyBiomass, SpectralEarth's 9 downstream) all LULC/crop/biomass/soil — none material. Can map minerals (REE/Nd @ Mountain Pass) but result maps only |
| **EMIT** | 285, 380–2500 nm ✅ | ⭐ positive (no benchmark) | **Estrela et al. 2025 (GRL)** detect **HDPE & PVC globally** via SWIR matched filter vs USGS GDS338/GDS385 (absorption centers ~1215/1417/1537/1732/2046/2313 nm), 60 m GSD. Feasibility demo + validation reference; no released dataset |
| **Tanager-1** (Planet) | ~424, 380–2500 nm ✅ | ❌ negative (labels) | **Planet Tanager Open Data** ~50+ scenes, **CC-BY-4.0, full VSWIR @30 m, radiance+SR HDF5** = *unlabeled* raw imagery → candidate self-annotation source. Carbon Mapper portal = gas-plume catalog |
| **GaoFen-5 / AHSI, ZY1-02D** | VNIR-SWIR ✅ | ❓ unresolved | no confirmed claim either way — open item, needs Chinese-language search (AI Studio / CSDN) |
| **HSI foundation models** (SpecBPP, HyperKD, SpectralEarth) | EnMAP-based | ❌ negative | downstream tasks all LULC / crop / soil-organic-carbon regression — none material-level |

**Other reference (weak positive):** **GENLIB / GUSL** (Degerickx et al. 2025) — ~9,000 urban-material spectra, 10 cities, via SPECCHIO. A spectral *library*, not an image benchmark; its strict material-level labeling was **refuted** (distills to LULC-overlapping classes) and SWIR coverage unconfirmed → candidate signature reference with caveats.

**Open items from this pass:** (1) GaoFen-5/AHSI/ZY1-02D unresolved; (2) can Tanager Open Data cover Lombardy waste/asbestos AOIs for self-annotation?; (3) is the EMIT HDPE/PVC matched-filter (6 SWIR centers) transferable as a cross-check for the SuperDove classifier despite 60 m GSD?

## E. De-dup / correction notes

- "Geomatics 2026 Mantua WV-3 VNIR+SWIR" workflow = the **same** `bonifazi-2026-ac-python` already in the library — **not** a new find.
- **Refuted / do not cite:** Cartagena per-classifier accuracy figures (unverified); the claim that WV-2/3/4 lack SWIR (WV-3 carries 8 SWIR bands); the "Nearmap-Australia = WorldView-3" framing (it is RGB aerial).