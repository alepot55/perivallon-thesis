# Multispectral deep learning for illegal waste detection: a thesis research compendium

**Adding near-infrared and shortwave infrared bands to standard RGB satellite imagery dramatically improves waste material classification — by up to 14% in transfer learning tasks — yet almost no public dataset combines multispectral satellite data with terrestrial waste material labels.** This gap positions a PoliMi thesis squarely at the frontier of environmental remote sensing. The PERIVALLON Horizon Europe project (€5.4M, 24 partners) provides the institutional context, while the AerialWaste dataset and Gibellini et al. (2025) pipeline establish the RGB-only baseline that multispectral approaches can extend. Foundation models like Prithvi-EO-2.0, DOFA, and SSL4EO-S12 now support multispectral input natively, making 2025–2026 the optimal window for this research.

This compendium synthesizes the most relevant literature (2023–2026), satellite platform specifications, deep learning architectures, tools, and datasets across all seven research areas required for the thesis.

---

## 1. Why multispectral bands transform waste detection

The case for moving beyond RGB rests on well-documented spectral signatures. **Plastics exhibit diagnostic absorption features at ~1215 nm, ~1730 nm, and ~2312 nm** (C–H stretch bonds), detectable by SWIR sensors. Krauz et al. (2025) demonstrated that adding just **λ = 800 nm (NIR) to RGB improved construction and demolition waste classification accuracy** comparably to using all 768 hyperspectral bands — a pivotal result for multispectral approaches. Uhrin et al. (2025) achieved **precision scores of 0.92–0.95** mapping waste plastic aggregations (80–150 m²) using WorldView-3's 8 SWIR bands alone, with laboratory-to-satellite spectral correlations of r = 0.95.

The SpectralWaste benchmark (IROS 2024) provided the first rigorous RGB-vs-hyperspectral comparison on waste sorting: PCA-reduced 3-band HSI offered the best accuracy–efficiency trade-off, and **fusion of RGB with spectral data consistently outperformed either modality alone**. FusionSort (2025) confirmed this across both hyperspectral (224-band) and multispectral (9-band) waste datasets. The implication is clear: even a modest increase from 3 to 6–8 bands yields substantial material discrimination gains without hyperspectral overhead.

Material-specific spectral behavior varies significantly. **Metals present flat, featureless reflectance** across VNIR-SWIR, making them distinguishable primarily by brightness and texture. Textiles separate in SWIR: polyester drops at ~1650 nm while natural fibers drop at 1400–1600 nm. Rubber shares hydrocarbon absorption features with plastics but has distinct spectral shapes; black rubber and black plastic remain challenging in NIR due to carbon black absorption. Wood shows cellulose features around 1730 nm and 2100 nm. The USGS Spectral Library and the urban materials spectral library of Kotthaus et al. (2014, ISPRS) provide reference signatures for many of these materials.

Key quantitative comparisons from the literature:

- **Magyar et al. (2023)**: Sentinel-2 multispectral + Random Forest achieved ~96% accuracy detecting illegal waste dumps along the Tisza River; NIR was most effective for plastic debris detection
- **Marrocco et al. (2024)**: Pansharpened Pléiades multispectral + dual-network DL (RetinaNet + InceptionV3) achieved ~90% detection rate for illegal microdumps in Campania, Italy, with cross-mission transferability
- **Guo & Li (2020)**: Normalized Difference Plastic Index using WorldView-3 SWIR substantially outperformed existing indices for urban plastic quantification — demonstrating that **well-chosen SWIR bands suffice without full hyperspectral capability**

---

## 2. The hyperspectral–multispectral resolution dilemma

The trade-off between spectral and spatial resolution is central to sensor selection. Hyperspectral satellites (PRISMA: 239 bands, EnMAP: 230+ bands, EMIT: 285 bands) offer exquisite material discrimination but at **30–60 m spatial resolution** — meaning a typical illegal dump of 50–200 m² occupies just 1–6 pixels. Multispectral commercial satellites achieve 1–4 m resolution with 8–16 bands, making individual waste piles spatially resolvable.

Zhang et al. (2025, Environmental Science & Technology) demonstrated hyperspectral satellites' unique capability for detecting landfill methane emissions from 38 global facilities. Dutta et al. (2025) showed PRISMA and EnMAP capture pollution risk information unavailable from Sentinel-2 alone. Yet for the detection and classification of small-to-medium illegal dump sites, **spatial resolution matters more than spectral resolution**: WorldView-3 at 1.24 m VNIR / 3.7 m SWIR occupies a practical sweet spot.

The literature converges on a **multi-scale "tip and cue" strategy**: Sentinel-2 (free, 5-day revisit, 13 bands at 10–60 m) for large-area screening; VHR commercial satellites for detailed inspection; and optionally drone-based hyperspectral for material composition analysis. This aligns with the progressive monitoring framework described in the Italian studies and with PERIVALLON's operational concept.

---

## 3. Satellite platforms: specifications and research access

### Planet SuperDove (PlanetScope PSB.SD)

The SuperDove constellation provides **8 spectral bands at 3 m resolution with near-daily global coverage** from 130+ satellites. Bands span Coastal Blue (431–452 nm) through NIR (845–885 nm), including Red Edge (697–713 nm) — designed for interoperability with Sentinel-2. Data products include orthorectified GeoTIFF with atmospheric correction (6SV-based surface reflectance). The **Planet Education & Research Program** provides free access to up to 3,000 km²/month of PlanetScope imagery for academic use. ESA's EarthNet Programme offers additional access for EU researchers. API access is available through Planet's RESTful Data API and Python SDK.

### Pléiades Neo (Airbus)

Two operational satellites deliver **6 multispectral bands (Deep Blue 400–450 nm, Blue 450–520 nm, Green 530–590 nm, Red 620–690 nm, Red Edge 700–750 nm, NIR 770–880 nm) at 1.2 m, plus 30 cm panchromatic**. The Red Edge band is particularly valuable for vegetation stress detection near waste sites. Products come as JPEG 2000, GeoTIFF, or NITF in DIMAP V2 format, with pansharpened options merging all spectral information at 30 cm. Research access is available through ESA Third Party Missions proposals. The constellation transmits up to 40 TB/day via laser relay, enabling rapid tasking.

### WorldView-3 (Maxar)

The **only commercial satellite offering SWIR bands at high resolution**: 8 VNIR bands at 1.24 m, **8 SWIR bands at 3.7 m** (commercially resampled to 7.5 m), 31 cm panchromatic, plus 12 CAVIS atmospheric bands. SWIR bands span 1184–2373 nm, covering all critical material absorption features. This sensor provides **165 unique SWIR band combinations** for material signature identification — detecting plastics, metals, paints, asphalt, and chemical substances. Access via ESA Third Party Missions or European Space Imaging (EUSI). Launched in 2014, it remains operational as of 2026.

### Sentinel-2 (Copernicus)

Thirteen bands at 10–60 m resolution with **free and open access**, 5-day revisit, and 290 km swath. The four 10 m bands (B2–B4, B8) provide baseline RGB+NIR; three 20 m Red Edge bands (B5–B7) and two 20 m SWIR bands (B11 at 1610 nm, B12 at 2190 nm) offer material-discriminating capability at coarser resolution. Sentinel-2C replaced 2A in January 2025; 2D is planned. Data is available through the Copernicus Data Space Ecosystem and Google Earth Engine. Level-2A products provide atmospherically corrected surface reflectance.

### Platform comparison

| Platform | Spatial resolution | Bands | SWIR | Revisit | Access |
|---|---|---|---|---|---|
| SuperDove | 3 m | 8 (VNIR) | No | Daily | Free E&R program |
| Pléiades Neo | 30 cm pan / 1.2 m MS | 6 + PAN | No | ~Daily | ESA proposals |
| WorldView-3 | 31 cm pan / 1.24 m MS / 3.7 m SWIR | 8 VNIR + 8 SWIR | **Yes** | <1 day | ESA proposals / commercial |
| Sentinel-2 | 10–60 m | 13 | 2 bands (20 m) | 5 days | **Free & open** |

### Data fusion approaches

Cross-sensor fusion combines VHR spatial detail with multispectral richness. **Pansharpening** (within-sensor PAN+MS fusion) has evolved from classical methods (IHS, Gram-Schmidt, wavelet) to deep learning approaches: PanNet, LambdaPNN, and Spatial-Spectral Fusion Transformers consistently outperform traditional methods. For cross-sensor fusion, Area-To-Point Regression Kriging (ATPRK) preserves both spectral and spatial features across sensors. SuperDove's bands were explicitly designed for Sentinel-2 interoperability, enabling seamless multi-resolution workflows. Deep learning-based fusion using Transformer architectures has achieved 10–30× resolution enhancement in recent work.

---

## 4. Adapting deep learning architectures to multispectral input

Standard pretrained models (ResNet, Swin Transformer, ConvNeXt) accept 3 RGB channels. Four strategies exist for extending them to 6+ spectral channels, each with distinct trade-offs.

**Weight replication (early fusion)** is the most common approach: the first convolutional layer's weights (shape [64, 3, 7, 7] for ResNet) are copied and averaged across N input channels. Corley et al. (CVPR Workshop 2024) showed that with proper resizing (to 224×224) and normalization, **EuroSAT accuracy jumps from 0.66 to 0.91** — demonstrating that preprocessing matters as much as architecture. For Vision Transformers, the SoftCon paper (2024) found that simply **randomly initializing the input embedding layer** while loading DINOv2 backbone weights is "both flexible and impressively effective," achieving state-of-the-art on 10 of 11 downstream EO tasks.

**Band grouping with spectral positional encoding** (late fusion) was pioneered by SatMAE (NeurIPS 2022). Sentinel-2 bands are grouped by ground sample distance — Group 1: B2, B3, B4, B8 (10 m); Group 2: B5, B6, B7, B8A (20 m Red Edge/NIR); Group 3: B11, B12 (20 m SWIR) — with separate patch embedding layers per group. This achieved **+7% improvement on supervised benchmarks and +14% on transfer learning**. SatMAE++ (CVPR 2024) extended this with multi-scale pretraining.

**Wavelength-conditioned dynamic networks** represent the frontier. **DOFA** (Xiong et al., 2024) uses a hypernetwork that generates patch embedding weights dynamically based on input band central wavelengths, allowing a single model to process any sensor modality. DOFA+ achieves state-of-the-art on the PANGEA benchmark. **AnySat** (CVPR 2025) uses Joint Embedding Predictive Architecture with resolution-adaptive spatial encoders, handling datasets with 3–11 channels from 11 sensors simultaneously.

For fine-tuning strategy, the literature strongly favors **full fine-tuning over frozen backbones** — a pansharpening pretraining study (2024) confirmed that "full-tuning consistently outperforms freeze-tuning." However, parameter-efficient methods are maturing: **DEFLECT** (2025) extends patch embeddings with <1% additional parameters, matching full fine-tuning performance. The Gibellini et al. (2025) two-step approach — frozen backbone head training followed by partial unfreezing of the final stage — represents a practical middle ground.

On the question of ImageNet vs. remote sensing pretraining: **ImageNet remains surprisingly competitive** when preprocessing is done correctly (Wang et al., 2025), but RS-specific pretraining provides clear gains for multispectral and SAR modalities where ImageNet features are less transferable.

---

## 5. Foundation models ranked by multispectral waste detection relevance

The remote sensing foundation model landscape has exploded since 2023. The following models are most relevant for multispectral waste detection, ranked by practical applicability.

**Prithvi-EO-2.0** (NASA/IBM, December 2024) accepts **6 HLS bands natively (Blue, Green, Red, Narrow NIR, SWIR1, SWIR2)** — including the SWIR bands critical for material identification. The 600M-parameter ViT model with 3D patch embeddings was trained on 4.2 million global HLS samples and achieves 75.6% average on GEO-Bench, outperforming 6 other foundation models by 8%. Multi-temporal capability enables change detection for waste accumulation monitoring. Fine-tuning is supported through IBM's TerraTorch toolkit. Code: github.com/NASA-IMPACT/Prithvi-EO-2.0; weights: huggingface.co/ibm-nasa-geospatial.

**SSL4EO-S12** (TU Munich/DLR, 2023) provides pretrained weights for **all 13 Sentinel-2 bands** across multiple architectures: MoCo-v2 (ResNet-50), DINO (ViT-S), MAE (ViT-B/ViT-L). Trained on 251,079 globally distributed locations with 4 seasonal timestamps. This is arguably the most practical starting point for Sentinel-2-based waste detection — providing ready-made initialized weights for the full spectral range. Code and weights: github.com/zhu-xlab/SSL4EO-S12, Apache-2.0 license.

**DOFA** (TU Munich, 2024) features a **wavelength-conditioned dynamic hypernetwork** that accepts any number of input channels from any sensor. Pre-trained on 5 EO modalities including multispectral and hyperspectral. Integrated into TorchGeo for easy deployment. Most flexible for multi-sensor fusion scenarios. Code: github.com/zhu-xlab/DOFA.

**Clay Foundation Model** v1.5 (Clay nonprofit, 2024) accepts **any number of bands from any sensor** via wavelength-parameterized embeddings, trained on ~70 million chips (33.8 TB) from Sentinel-2, Landsat, Sentinel-1, NAIP, and MODIS. Open-source (Apache-2.0): github.com/Clay-foundation/model.

**SpectralGPT** (Hong et al., IEEE TPAMI 2024) is purpose-built for spectral data with a **3D generative pretrained transformer** architecture (600M+ parameters) that explicitly captures spatial-spectral coupling. Trained on Sentinel-2 data with multi-target spectral reconstruction. Code: github.com/danfenghong/IEEE_TPAMI_SpectralGPT.

**SatMAE** (Stanford, NeurIPS 2022) introduced spectral band grouping with positional encoding — foundational work that influenced most subsequent models. Code: github.com/sustainlab-group/SatMAE.

Other notable models include **SkySense** (SenseTime, CVPR 2024; 2.06B parameters, multi-modal), **SatMAE++** (CVPR 2024, multi-scale extension), **CROMA** (2024, SAR-MSI cross-modal fusion), and **HyperSigma** (2024, hyperspectral foundation model). Scale-MAE and GFM are RGB-only and would require adaptation.

---

## 6. The PoliMi baseline pipeline and PERIVALLON context

### Gibellini et al. (2025): the current pipeline

The paper "A deep learning pipeline for solid waste detection in remote sensing images" (Waste Management Bulletin, DOI: 10.1016/j.wmb.2025.100246; arXiv: 2502.06607) establishes the baseline. The system performs **binary scene classification** (waste present vs. absent), not object detection or segmentation. **Swin-T with Remote Sensing Pretraining (RSP)** at 20 cm/px GSD achieved the best results: **92.02% F1-score and 94.56% accuracy** on AerialWaste v3. The two-step training strategy — transfer learning with frozen backbone, then fine-tuning of the final stage — proved effective. The pipeline boosts landfill detection by 63% and cuts analysis time by ~12% compared to manual inspection. Code: github.com/nahitorres/aerialwaste-model.

### Fraternali & Morandini (2024): the survey

The companion survey "Solid waste detection, monitoring and mapping in remote sensing images" (Waste Management, Vol. 189, pp. 88–102) explicitly identifies **RGB-only data as a key limitation**, noting that "restricting the dataset to just three bands significantly reduces the available feature information, particularly in the near-infrared band." The survey calls for multi-modal detectors exploiting NIR bands to identify stressed vegetation as a clue for buried waste. It confirms the field **lacks a standardized benchmark** for comparing approaches — most work remains case-study-specific.

### AerialWaste dataset

Created by Torres & Fraternali (Nature Scientific Data, 2023), AerialWaste contains **10,434 images** (3,478 positive, 6,956 negative) from three sources: AGEA Ortophotos (~20 cm), WorldView-3 (~30 cm), and Google Earth (~50 cm). It provides three annotation levels: binary labels, multi-class labels across **22 waste categories** (rubble, tires, vehicles, containers, big bags, etc.), and segmentation masks for a 169-image subset. Version 3 (11,700+ images) is available at Zenodo (DOI: 10.5281/zenodo.12607190). **Critically, AerialWaste is RGB-only** — extending it with multispectral bands is a natural thesis contribution. Website: aerialwaste.org.

### PERIVALLON Horizon Europe project

"Protecting the EuRopean terrItory from organised enVironmentAl crime through inteLLigent threat detectiON tools" (Grant 101073952) runs December 2022 – November 2025 with **€5.4M budget and 24 partners** from 12 countries, including PoliMi, ARPA Lombardia, the EU Satellite Centre, and Italian Carabinieri. The project addresses four environmental crime types; **PUC1 (illegal waste disposal)** is the lead use case. It employs a two-level geospatial intelligence strategy: large-scale satellite mapping for territory scanning, then UAV missions for 3D mapping, material classification using European Waste Codes, and volume quantification. Six pilot iterations have been completed across Italy, Greece, Sweden, and Romania. A newly released **DroneWaste dataset** (4,993 images, 17 dumps, 20 material types) extends the data ecosystem (Zenodo: DOI: 10.5281/zenodo.17288038). Website: perivallon-he.eu; CORDIS: cordis.europa.eu/project/id/101073952.

---

## 7. Material classification at satellite resolution

Waste material classification from satellite imagery operates across three paradigms. **Scene-level classification** (the AerialWaste approach) labels entire tiles as waste/non-waste — practical but coarse. **Pixel-level semantic segmentation** assigns material labels per pixel, ideal with sufficient spectral information but challenged by mixed pixels at 1–5 m resolution. **Object-level analysis** (OBIA) groups pixels into meaningful segments before classification, reducing noise and preserving boundaries.

At satellite resolution, a single pixel often contains multiple materials. **Spectral unmixing** addresses this by decomposing pixel reflectance into endmember spectra weighted by fractional abundances. Traditional Linear Spectral Unmixing (LSU) assumes additive mixing with non-negative, sum-to-one constraints. Deep learning approaches are advancing rapidly: autoencoder-based blind unmixing (DNMF), CNN-based architectures like SCNL that combine spectral libraries with learned features, and dual-branch networks (SISLU-Net) that integrate spatial and spectral information. **Incorporating spectral unmixing into semantic segmentation has been shown to enhance land-cover classification** — a directly transferable approach for waste material estimation.

The TSNET paper (2025) created the first RGB-NIR 4-band solid waste dataset covering 5 waste types (industrial, tailings, household, construction, mixed) from Chinese satellites, but it is not publicly available. **MARIDA** (2022) is the closest public precedent — combining 12 Sentinel-2 bands with pixel-level annotations for 15 classes including marine debris, though focused on ocean rather than land. This absence of a public multispectral terrestrial waste material dataset represents the thesis's primary contribution opportunity.

---

## 8. Benchmark datasets for waste detection and multispectral classification

### Waste-specific remote sensing datasets

| Dataset | Images | Resolution | Bands | Annotations | Download |
|---|---|---|---|---|---|
| **AerialWaste v3** | 11,700+ | 20–50 cm | RGB | Binary + 22 classes + masks | zenodo.org/records/7034382 |
| **DroneWaste** | 4,993 | cm-level (UAV) | RGB | 20 material types, 17 dumps | zenodo.org/records/17288038 |
| **SWAD** | 1,996 | ~1–2 m | RGB | Bounding boxes (1 class) | kaggle.com/datasets/shenhaibb/swad-dataset |
| **UAVVaste** | 772 | cm-level | RGB | COCO detection (1 class) | github.com/PUTvision/UAVVaste |
| **MARIDA** | 1,381 patches | 10 m (S2) | **12 S2 bands** | Pixel-level, 15 classes | zenodo.org/records/5151941 |
| **SpectralWaste** | Operational facility | Conveyor | RGB + 224-band HSI | Segmentation masks | Casao et al. IROS 2024 |

### Multispectral classification datasets

| Dataset | Samples | Resolution | Bands | Task |
|---|---|---|---|---|
| **EuroSAT** | 27,000 | 10 m | 13 (S2) | Scene classification, 10 LULC classes |
| **BigEarthNet v2.0** | 549,488 | 10 m | S1 (2) + S2 (12) | Multi-label, 19 CLC classes |
| **SEN12MS** | 541,986 | 10 m | S1 + S2 (13) + MODIS LC | Scene/segmentation |
| **So2Sat LCZ42** | ~400,000+ | 10 m | S1 (8) + S2 (10) | 17 Local Climate Zones |
| **SSL4EO-S12** | 250,000+ | 10 m | S1 + S2 (all) | Self-supervised pretraining |

**The critical gap**: no existing public dataset combines multispectral satellite bands (especially NIR/SWIR) with terrestrial waste material annotations. Creating such a dataset — even by augmenting AerialWaste locations with Sentinel-2 or Planet multispectral data — would be a significant contribution.

---

## 9. The recommended software stack

**TorchGeo** (Microsoft, v0.8.1) is the primary recommended framework. It provides **110+ pretrained models for multispectral imagery** — a first among ML libraries — with automatic CRS reprojection, geospatial samplers, and loaders for 120+ benchmark datasets including EuroSAT, BigEarthNet, and SEN12MS. DOFA is integrated directly. Built on PyTorch Lightning with CLI training support. Documentation: torchgeo.readthedocs.io; GitHub: github.com/torchgeo/torchgeo.

**Rasterio** (v1.4.4/1.5.0) provides the Pythonic interface to GDAL for all raster I/O — reading multispectral GeoTIFFs, windowed reading of large scenes, CRS handling, and NumPy array integration. **GeoPandas** (v1.0.x) manages vector data: annotation polygons, spatial joins, and vector-raster overlay for extracting multispectral features within labeled waste zones. Both are foundational dependencies.

**eo-learn** (Sentinel Hub, v1.5.7) excels at building end-to-end EO processing pipelines with its EOPatch/EOTask architecture — from Sentinel-2 data download through preprocessing to ML classification, with direct Sentinel Hub API integration. **QGIS** (v3.40+) with the Semi-Automatic Classification Plugin (SCP) and EnMAP-Box 3 provides spectral signature visualization, supervised classification experiments, and the QLSU plugin for spectral unmixing directly in the GUI.

For fine-tuning foundation models, IBM's **TerraTorch** (github.com/IBM/terratorch) supports Prithvi-EO-2.0 with UPerNet and FCN decoder heads. **rioxarray** extends xarray for multidimensional/multitemporal satellite data handling.

---

## Conclusion: where this thesis can push boundaries

The literature reveals a field at an inflection point. RGB-based waste detection is maturing (92% F1 on AerialWaste), but **material classification requires spectral information that RGB cannot provide**. The technology stack is ready: foundation models natively handle 6–13 spectral bands, WorldView-3 SWIR enables material-level discrimination at 3.7 m, and Planet SuperDove provides free 8-band daily coverage for research.

Three concrete thesis contributions emerge from the gaps identified. First, **creating a multispectral waste material dataset** by co-registering AerialWaste locations with Sentinel-2 or Planet imagery would fill the most critical data gap in the field. Second, **systematic ablation studies** comparing RGB vs. RGB+RedEdge+NIR vs. full multispectral performance on waste classification — using Swin-T, ConvNeXt, or DOFA as backbones — would provide the quantitative evidence the community needs. Third, **fine-tuning Prithvi-EO-2.0 or SSL4EO-S12 pretrained weights** for waste material classification, leveraging their native SWIR support, could establish a new state of the art that directly serves PERIVALLON's operational goals.

The key architectural recommendation: start with SSL4EO-S12 pretrained weights (all 13 Sentinel-2 bands, ResNet-50 or ViT) for maximum spectral coverage, or DOFA for sensor-agnostic flexibility. Apply the Gibellini et al. two-step fine-tuning strategy. Validate on both AerialWaste (for detection) and custom multispectral annotations (for material classification). This approach builds naturally on PoliMi's existing pipeline while advancing the field's most pressing limitation — the inability to identify *what kind* of waste is present from orbit.