# Gap Analysis: Complementary Literature for a Multispectral Satellite-Based Asbestos & Illegal-Waste Detection Thesis (PERIVALLON / PoliMi)

## TL;DR
- The 12-paper reading list is strong on **asbestos-cement (AC) roof detection with VNIR/CNNs** and on **deep-learning illegal-waste detection from VHR orthophotos**, but is missing four entire research families: (a) self-supervised / foundation-model pretraining for multispectral & hyperspectral EO (SatMAE, Prithvi-EO-2.0, SpectralGPT, SpectralEarth, DOFA, AnySat, HyperSIGMA, SpectralFormer, HyperspectralViTs); (b) physics-based spectral unmixing & matched-filter mineral mapping (Tetracorder, USGS splib07a, EnGeoMAP, MESMA); (c) the marine-plastic / WV-3 SWIR plastic-index literature that directly speaks to the "multispectral vs. RGB" question (Biermann FDI, Guo & Li NDPI, Aguilar/Uhrin 2025, MARIDA, MADOS); and (d) recent hyperspectral spaceborne mission work (PRISMA, EnMAP, EMIT) including a 2025 EnMAP asbestos-cement study that is the closest published analogue to the thesis itself.
- For the user's *core* question ("added value of multispectral over RGB"), the highest-priority external references are **Aguilar et al. 2021 (WV-3, OA = 97.38% with all bands vs. 90.85% with VNIR-only vs. 96.79% with SWIR-only)**, **Aguilar/Uhrin et al. 2025 (WV-3 SWIR terrestrial macroplastics)**, **Kaur et al. 2024 (SuperDove 8-band SVM OA = 0.94 vs. 4-band OA = 0.78–0.83)**, and **Biermann et al. 2020 FDI** — these are the canonical "ablate the bands" studies and are absent from the reading list.
- The single most directly competing paper that is **missing** from the reading list is **Aharoni-Mack et al. 2025 (Scientific Reports, EnMAP hyperspectral detection of asbestos-cement rooftops; ACE OA = 91.4%; SID 90.1%; SVM 89.2%; 86% ground-truth positive-match rate)** — it covers the AC-roof use case with a real spaceborne hyperspectral sensor and **must** be cited and benchmarked.

---

## Key Findings

### What the existing 12-paper list covers well
- Asbestos VNIR mapping with classical ML + CNN (papers 1, 2, 4, 5, 7)
- Hyperspectral airborne AC mapping with weathering (paper 3, Frassy/Bassani 2015)
- Multi-temporal AC change detection (paper 6)
- Illegal-waste / landfill detection with VHR orthophotos and deep CNNs (papers 8, 10, 11, 12)
- Generic landfill satellite-monitoring review (paper 9)

### What the list does NOT cover (gaps to fill)
1. **No foundation-model / SSL pretraining baseline.** None of the 12 cite SatMAE, Prithvi, SpectralGPT, Clay, DOFA, AnySat, SpectralEarth, HyperSIGMA, Presto, or SatMAE++ — yet PERIVALLON-style operational deployment with limited labels is the canonical use case for these models.
2. **No transformer-only spectral architecture.** SpectralFormer (Hong et al. TGRS 2022) and HyperspectralViTs (Růžička & Markham, JSTARS 2025) are missing.
3. **No physics-based unmixing / spectral library reference.** Tetracorder (Clark et al. JGR 2003), USGS splib07a (Kokaly et al. 2017), EnGeoMAP 2.0 (Mielke et al. RS 2016), MESMA (Roberts 1998 / Zhou & Gader 2018) are not cited.
4. **No WV-3 SWIR plastic / hydrocarbon literature.** Aguilar et al. 2021 (NDPI), Guo & Li 2020 (NDPI), Asadzadeh & de Souza Filho 2016 (HC index), Schmidt et al. 2021, and Aguilar/Uhrin 2025 are absent — these directly inform what the SWIR bands buy you over VNIR/RGB.
5. **No marine-plastic spectral-index literature.** Biermann et al. 2020 (FDI), Topouzelis et al., MARIDA (Kikaki 2022), MADOS (Kikaki ISPRS 2024), MADLib reference library.
6. **No spaceborne hyperspectral material mapping.** PRISMA landfill work (Dutta et al. 2022, ESPR), EnMAP mineral exploration (Booysen, Koerting), EMIT + EnMAP + PRISMA landfill methane (Yang et al. ES&T 2025).
7. **No SuperDove-specific 4 vs 8 band ablation.** Kaur et al. 2024 (Sustainable Cities and Society) and Wang/Vanhellemont 2023 are absent.
8. **No vision-language / RemoteCLIP / GeoChat coverage** — relevant for label-efficient deployment.
9. **The most recent direct competitor — Aharoni-Mack et al. 2025 (Scientific Reports, EnMAP asbestos-cement)** is absent.

---

## Details

### A) Methodological gaps

**A.1 — Self-supervised pretraining for multispectral / hyperspectral EO**

| # | Paper | Year | Sensor/Bands | Why complementary |
|---|---|---|---|---|
| A1.1 | **Cong et al., "SatMAE: Pre-training Transformers for Temporal and Multi-Spectral Satellite Imagery"**, NeurIPS 2022, arXiv:2207.08051. Code: github.com/sustainlab-group/SatMAE | 2022 | Sentinel-2, 13 bands | Canonical MAE for MSI; introduces fMoW-Sentinel. None of the 12 papers use SSL pretraining. |
| A1.2 | **Noman, Naseer, Cholakkal, Anwer, Khan, Khan, "SatMAE++: Rethinking Transformers Pre-training for Multi-Spectral Satellite Imagery"**, CVPR 2024, arXiv:2403.05419. Code: github.com/techmn/satmae_pp | 2024 | Sentinel-2 + RGB, multi-scale | Multi-scale MSI MAE, direct upgrade. Useful baseline backbone. |
| A1.3 | **Hong et al., "SpectralGPT: Spectral Remote Sensing Foundation Model"**, IEEE TPAMI 46(8):5227–5244, 2024, DOI 10.1109/TPAMI.2024.3362475, arXiv:2311.07113 | 2024 | Sentinel-2 spectral cube, 3D-MAE | The reference spectral FM; released in Base (~100M), Large (~300M), Huge (~600M) variants pretrained on 1M spectral RS images; tested on segmentation + change detection. |
| A1.4 | **Szwarcman et al., "Prithvi-EO-2.0: A Versatile Multi-Temporal Foundation Model for Earth Observation Applications"**, arXiv:2412.02732, HuggingFace ibm-nasa-geospatial/Prithvi-EO-2.0 | 2024 | HLS (Landsat/S2), 6 bands incl. SWIR1/2 | IBM–NASA–Jülich FM at 300M and 600M params; trained on 4.2M HLS time-series; the 600M model outperforms Prithvi-EO-1.0 by 8% on GEO-Bench. The SWIR1/SWIR2 bands cover the AC absorption near 2.31 µm; Apache 2.0. |
| A1.5 | **Braham, Albrecht, Mairal, Chanussot, Wang, Zhu, "SpectralEarth: Training Hyperspectral Foundation Models at Scale"**, IEEE JSTARS 2025, DOI 10.1109/JSTARS.2025.3581451, arXiv:2408.08447. Code: github.com/AABNassim/spectral_earth | 2025 | EnMAP, 202 bands VNIR+SWIR (420–2450 nm) | The only HSI-FM pretrained on a real spaceborne HSI sensor with full SWIR — directly relevant to asbestos at 2.31 µm; 538,974 patches from 11,636 EnMAP scenes. |
| A1.6 | **Wang et al., "HyperSIGMA: Hyperspectral Intelligence Comprehension Foundation Model"**, IEEE TPAMI 2025, DOI 10.1109/TPAMI.2025.3557581, arXiv:2406.11519. Code: github.com/WHU-Sigma/HyperSIGMA | 2025 | Multi-source HSI, 1B+ params | Largest HSI FM to date; sparse-sampling attention; full HyperGlobal-450K dataset released. |
| A1.7 | **Xiong et al., "DOFA: Neural Plasticity-Inspired Multimodal Foundation Model for Earth Observation"**, arXiv:2403.15356. Code: github.com/zhu-xlab/DOFA | 2024 | S1+S2+Landsat+NAIP+EnMAP | Wavelength-conditioned hypernetwork — handles arbitrary spectral inputs, ideal for cross-sensor S2 → SuperDove transfer. |
| A1.8 | **Astruc et al., "AnySat: One Earth Observation Model for Many Resolutions, Scales, and Modalities"**, CVPR 2025, arXiv:2412.14123. Code: github.com/gastruc/AnySat | 2025 | 11 sensors, 0.2–250 m GSD | Scale-adaptive JEPA; handles SuperDove (3 m) and S2 (10 m) in one model. |
| A1.9 | **Tseng et al., "Presto: Lightweight, Pre-trained Transformers for Remote Sensing Timeseries"**, NeurIPS CCAI 2023, arXiv:2304.14065. Code: github.com/nasaharvest/presto | 2023 | S1+S2+ERA5+SRTM | Lightweight (sub-100k params), good for limited-compute environments. |

**A.2 — Transformer-only spectral / spatial-spectral classifiers**

- **Hong, Han, Yao, Gao, Zhang, Plaza, Chanussot, "SpectralFormer: Rethinking Hyperspectral Image Classification with Transformers", IEEE TGRS 2022, vol. 60, art. 5518615, DOI 10.1109/TGRS.2021.3130716, arXiv:2107.02988. Code: github.com/danfenghong/IEEE_TGRS_SpectralFormer.** The first major pixel-wise transformer for HSI; introduces Group-wise Spectral Embedding (GSE) and Cross-layer Adaptive Fusion (CAF). Foundational citation for the methodology chapter.
- **Růžička & Markham, "HyperspectralViTs: General Hyperspectral Models for On-board Remote Sensing", IEEE JSTARS 2025, DOI 10.1109/JSTARS.2025.3557527, arXiv:2410.17248. Code: github.com/previtus/HyperspectralViTs.** Adapts SegFormer and EfficientViT for HSI without classical product preprocessing; demonstrated on methane and mineral identification — directly relevant if the thesis extends to PRISMA/EnMAP.

**A.3 — Spectral unmixing / Tetracorder / canonical references**

- **Clark, Swayze, Livo, Kokaly, Sutley, Dalton, McDougal, Gent, "Imaging spectroscopy: Earth and planetary remote sensing with the USGS Tetracorder and expert systems", JGR Planets 2003, 108(E12), 5131, DOI 10.1029/2002JE001847.** The canonical Tetracorder reference; this is the standard expert-system mineral identifier used by NASA EMIT and is the proper citation when discussing chrysotile/serpentine spectral identification.
- **Kokaly, Clark, Swayze, Livo, Hoefen, Pearson, Wise, Benzel, Lowers, Driscoll, Klein, "USGS Spectral Library Version 7", USGS Data Series 1035, 2017, DOI 10.3133/ds1035; data DOI 10.5066/F7RR1WDJ.** The reference spectral library (splib07a). Convolved versions for Sentinel-2, Landsat-8, WorldView-3 and ASTER are released — directly usable to build synthetic SuperDove (close to S2) and WV-3 endmembers for asbestos minerals.
- **Swayze, Clark, Goetz, Chrien, Gorelick, "Effects of spectrometer band pass, sampling, and SNR on spectral identification using the Tetracorder algorithm", JGR Planets 2003, DOI 10.1029/2002JE001975.** Quantifies how band-pass and SNR constrain mineral ID — directly relevant to the SuperDove feasibility question.
- **Mielke, Rogass, Boesche, Segl, Altenberger, "EnGeoMAP 2.0 — Automated Hyperspectral Mineral Identification for the German EnMAP Space Mission", Remote Sensing 2016, 8(2), 127, DOI 10.3390/rs8020127.** Open-source EnMAP material mapping tool based on Tetracorder/MICA principles.
- **Roberts, Gardner, Church, Ustin, Scheer, Green, "Mapping chaparral in the Santa Monica Mountains using MESMA", RSE 1998, 65(3), 267–279, DOI 10.1016/S0034-4257(98)00037-6** + **Zhou, Wetherley, Gader, "Unmixing urban hyperspectral imagery with a Gaussian mixture model on endmember variability", arXiv:1801.08513.** Canonical MESMA references; particularly useful given AC-roof endmember variability (weathering, paint sealing).

**A.4 — Few-shot / open-set (out-of-distribution problem in Mazzola thesis)**

- The reading list has no coverage. Frame the asbestos-vs-everything-else problem as a one-class / open-set HSI classification task — see the open-set hyperspectral literature centred on the Indian Pines / Houston-2013 benchmarks (Liu, Yu, Roy, et al., "Reciprocal Points Learning for Open-Set HSI Classification", IEEE TGRS 2024).

**A.5 — Domain adaptation for material classification under distribution shift**

- **Tuia, Persello, Bruzzone, "Domain Adaptation for the Classification of Remote Sensing Data: An Overview of Recent Advances", IEEE GRSM 2016, DOI 10.1109/MGRS.2016.2548504, arXiv:2104.07778.** The standard DA survey for RS. Frames the four-family taxonomy (feature selection, representation matching, classifier adaptation, selective sampling) that the thesis can adopt for its discussion of generalisation outside the training scene.

**A.6 / A.7 — Super-resolution & pansharpening for MSI**

- **Vivone, Dalla Mura, Garzelli, Restaino, Scarpa, Ulfarsson, Alparone, Chanussot, "A New Benchmark Based on Recent Advances in Multispectral Pansharpening", IEEE GRSM 2021, DOI 10.1109/MGRS.2020.3019315.** The canonical pansharpening benchmark.

**A.8 — Spectral indices for man-made materials**

- **Guo & Li, "Normalized Difference Plastic Index (NDPI) for satellite-based plastic detection"**, 2020 / 2021 (cited extensively in WV-3 SWIR literature). Threshold-based plastic detector exploiting WV-3 SWIR bands near 1.6 µm and 2.2 µm.
- **Asadzadeh & de Souza Filho, "Investigating the capability of WorldView-3 superspectral data for direct hydrocarbon detection", RSE 2016, DOI 10.1016/j.rse.2016.07.030.** Hydrocarbon Index (HC) using WV-3 SWIR.
- **Biermann, Clewley, Martinez-Vicente, Topouzelis, "Finding Plastic Patches in Coastal Waters using Optical Satellite Data", Scientific Reports 2020, 10:5364, DOI 10.1038/s41598-020-62298-z.** Floating Debris Index (FDI). Demonstrates that the SWIR-1 / red-edge bands carry the discriminative power — the canonical citation for the thesis' RGB-vs-multispectral argument.
- **Themistocleous et al., "Plastic Index (PI)", 2020** — the simpler Red/NIR-only version, useful as a low-spectral-resolution baseline.

### B) Dataset / sensor gaps

**B.1 — Hyperspectral spaceborne datasets / missions**

- **Loizzo et al., "PRISMA: The Italian Hyperspectral Mission", IGARSS 2018**, and **Dutta et al., "Satellite hyperspectral imaging technology as a potential rapid pollution assessment tool for urban landfill sites: case study of Ghazipur and Okhla landfill sites in Delhi, India", Env. Sci. & Pollution Research 2022, DOI 10.1007/s11356-022-22421-1.** The only published PRISMA landfill spectral-index application.
- **Dutta, Sharma, Datta, "Unfolding the potential of next generation hyperspectral satellites for pollution monitoring at municipal solid waste landfill site", Cleaner Engineering and Technology 2025 (PII S2211464525000880).** PRISMA + EnMAP multi-platform dashboard framework.
- **Yang et al., "Global Identification of Solid Waste Methane Super Emitters Using Hyperspectral Satellites", ES&T 2025, DOI 10.1021/acs.est.4c14196.** EMIT + EnMAP + PRISMA combined for 38 landfills; the authors estimate that these instruments could detect 35–60% of global landfill emissions.
- **Booysen, Lorenz, Thiele, et al., "Leveraging EnMAP hyperspectral data for mineral exploration: Examples from different deposit types", International Journal of Applied Earth Observation and Geoinformation 2025 (PII S016913682500472X).** Best EnMAP mineral-mapping demonstration; informs the "asbestos-as-serpentine-mineral-mapping" framing.
- **Koerting, Rogass, Lorenz, et al., "Assessment of the spaceborne EnMAP hyperspectral data for alteration mineral mapping: A case study of the Reko Diq porphyry CuAu deposit, Pakistan", RSE 2024, DOI 10.1016/j.rse.2024.114254.** EnMAP-quality demonstrated at scene level; canonical 2.2 µm mineral mapping with absorption features for white micas (2195–2210 nm), chlorite, epidote, calcite.
- **Aharoni-Mack et al., "Detection of asbestos-based cement rooftops in conflict-affected settings using EnMAP hyperspectral data", Scientific Reports 2025, DOI 10.1038/s41598-025-09738-w.** ⭐ **THE most directly competing paper not in the reading list** — EnMAP L2A data; eight supervised classifiers; reported accuracies: **ACE 91.4%, Spectral Information Divergence 90.1%, SVM 89.2%**, with rural Kibbutzim and Moshavim achieving >92% match rates and overall ground-truth surveys reaching an 86% positive-match rate. Must be benchmarked.

**B.2 — Public datasets for waste**

- **Kikaki, Kakogeorgiou, Mikeli, Raitsos, Karantzalos, "MARIDA: A benchmark for Marine Debris detection from Sentinel-2", PLOS ONE 2022, DOI 10.1371/journal.pone.0262247.** First S2-based marine-debris benchmark; 1,381 patches (256×256) across 15 classes.
- **Kikaki, Kakogeorgiou, Hoteit, Karantzalos, "MADOS: Detecting Marine Pollutants and Sea Surface Features with Deep Learning in Sentinel-2 Imagery", ISPRS J. P&RS 2024, DOI 10.1016/j.isprsjprs.2024.02.017.** 174 Sentinel-2 scenes across 47 globally distributed tiles (2015–2022), ~1.5M annotated pixels; introduces MariNeXt; the largest available S2 marine-pollution dataset.
- **Garaba, Park, Vermeulen, "MADLib: MArine Debris hyperspectral reference Library", ESSD 2025, 17, 7293.** 24,889 hyperspectral reflectances from 3,032 debris samples.
- **Bashkirova et al., "ZeroWaste Dataset", CVPR 2022, arXiv:2106.02740.** In-the-wild conveyor-belt waste segmentation — useful OOD baseline.
- **Proença & Simões, "TACO: Trash Annotations in Context", arXiv:2003.06975.** 60 classes, hierarchical taxonomy — useful for waste-type ontology design.
- **Casado-García et al., "SpectralWaste Dataset", arXiv:2403.18033, 2024.** Multimodal RGB + hyperspectral conveyor waste-sorting dataset.

**B.3 — Public datasets for asbestos / building roof material**: no large public dataset exists. Spectral libraries below substitute.

**B.4 — Spectral libraries**

- **USGS splib07a (Kokaly et al. 2017, DOI 10.3133/ds1035).** Contains chrysotile, amosite, crocidolite, tremolite spectra **already convolved to WorldView-3 and Sentinel-2 band passes** — directly usable for SuperDove (close to S2 bands).
- **Meerdink, Hook, Roberts, Abbott, "The ECOSTRESS spectral library version 1.0" (renamed ASTER spectral library v2.0), RSE 2019, DOI 10.1016/j.rse.2019.05.015.**
- **Bonifazi, Capobianco, Serranti, "Asbestos containing materials detection and classification by the use of hyperspectral imaging", J. Hazardous Materials 344 (2018), 981–993, DOI 10.1016/j.jhazmat.2017.11.056.** Lab-grade SWIR signatures of chrysotile, amosite, crocidolite in cement matrices with chemometric (PCA + SIMCA) classification. Identifies the hydroxyl combination bands at **Mg-OH (2300 nm) and Fe-OH (2280–2343 nm)** — exactly the absorption features that any SuperDove-based attempt necessarily MISSES because SuperDove ends near 865 nm.

**B.5 — SuperDove-specific applications**

- **Kaur et al., "A comparative analysis of PlanetScope 4-band and 8-band imageries for land use land cover classification", Sustainable Cities and Society 2024 (PII S1195103624000235).** ⭐ **The exact 4-band vs. 8-band ablation the thesis needs.** Reports the highest accuracy with 8-band imagery using SVM (OA = 0.94), while the lowest overall accuracies — 0.78 (Town of Three Rivers), 0.82 (City of Summerside), 0.83 (City of Charlottetown) — occurred with 4-band imagery over PEI, Canada.
- **Wang, McCabe, Aragon, et al., "The radiometric accuracy of the 8-band multi-spectral surface reflectance from the planet SuperDove constellation", International Journal of Applied Earth Observation and Geoinformation 2022 (PII S1569843222002230).** Quantifies SuperDove surface-reflectance uncertainty (VIS-NIR: accuracy 2.1–10.69%, precision 7.2–11.33%, total uncertainty 7.51–15.56%); essential for atmospheric-correction discussion.
- **Loureiro et al., "Accuracy assessment of PlanetScope SuperDove products for aquatic reflectance retrieval", International Journal of Applied Earth Observation and Geoinformation 2025 (PII S092427162500262X).** SuperDove validation over Brazilian inland and coastal waters; PSR vs. ACOLITE atmospheric-correction comparison.
- **Anwar et al., "Feasibility of PlanetScope SuperDove constellation for water quality monitoring of inland and coastal waters", Frontiers in Remote Sensing 2025, DOI 10.3389/frsen.2025.1624783.** Reports SuperDove SNRs across the eight bands (highest 248:1 at 443 nm; lowest 8:1 at 865 nm; other visible bands 26:1–98:1) — critical for understanding which bands carry signal vs. noise.

**B.6 — WorldView-3 SWIR applications**

- **Aguilar, Nemmaoui, Aguilar, Jiménez-Lao, "Evaluation of Object-Based Greenhouse Mapping Using WorldView-3 VNIR and SWIR Data: A Case Study from Almería (Spain)", Remote Sensing 2021, 13(11), 2133, DOI 10.3390/rs13112133.** ⭐ The cleanest **VNIR-only vs. SWIR-only vs. all-bands ablation** in the WV-3 literature: **OA = 90.85% (VNIR), 96.79% (SWIR), 97.38% (All Features)** — the canonical "RGB-vs-multispectral added value" benchmark. NDPI is the single most predictive feature.
- **Aguilar, Sousa, Uhrin, Gudino-Elizondo, Biggs, "Mapping terrestrial macroplastics and polymer-coated materials in an urban watershed using WorldView-3 and laboratory reflectance spectroscopy", Environmental Monitoring and Assessment 2025, 197(7), DOI 10.1007/s10661-025-14125-z.** ⭐ Up-to-date Uhrin/Aguilar paper requested by user; demonstrates urban polymer mapping at WV-3 SWIR with lab spectra. SWIR absorption features near 931, 1130–1192, 1205–1215, 1394–1460, 1660, and 1728–1732 nm are consistent across polymer types.
- **Kühn, Oppermann, Hörig, "Hydrocarbon Index — an algorithm for hyperspectral detection of hydrocarbons", IJRS 2004, DOI 10.1080/01431160310001642287.** Foundational HC index.
- **Schmidt et al., "A knowledge-based, validated classifier for the identification of aliphatic and aromatic plastics by WorldView-3 satellite data", RSE 2021, DOI 10.1016/j.rse.2021.112623.** WV-3 SWIR plastic identification with eight narrow SWIR bands; the authors demonstrate that plastic mapping algorithms based on SWIR reflectance alone can outperform algorithms using the entire spectrum — a strong claim for the thesis' positioning.

### C) Contiguous domains for transfer

**C.1 — Marine plastic litter (informs spectral-signature side)**

- **Biermann et al. 2020 (Sci. Rep.) FDI** — already cited.
- **Topouzelis, Papakonstantinou, Garaba, "Detection of floating plastics from satellite and unmanned aerial systems (Plastic Litter Project 2018)", IJAEOG 2019, 79, 175–183, DOI 10.1016/j.jag.2019.03.011.**
- **Garaba & Dierssen, "An airborne remote sensing case study of synthetic hydrocarbon detection using SWIR imaging spectrometer", RSE 2018, DOI 10.1016/j.rse.2018.04.030.** Foundational SWIR-plastic spectroscopy.

**C.2 — Mineral mapping / Cuprite type sites**

- **Swayze, Clark, et al. (2003)** and **Booysen 2025 (EnMAP)** — already cited above.

**C.3 — Urban material / roof material classification**

- **Heiden, Segl, Roessner, Kaufmann, "Determination of robust spectral features for identification of urban surface materials in hyperspectral remote sensing data", RSE 2007, DOI 10.1016/j.rse.2007.02.030.** The classic HyMap urban-materials reference.

**C.4 — Band-contribution ablation (the thesis' central question)**

- **Aguilar 2021 (Almería) — already cited; the cleanest published ablation.**
- **Kaur 2024 SuperDove 4 vs 8 — already cited.**
- **Schmidt 2021 — already cited.**

**C.5 — Hyperspectral plastic identification (lab + airborne)**

- **Bonifazi/Capobianco/Serranti 2018 (J. Haz. Mat.) — already cited; covers asbestos + plastic in a lab HSI.**
- **Tasseron, van Emmerik, Peller, Schreyers, Biermann, "Advancing floating macroplastic detection from space using experimental hyperspectral imagery", Remote Sensing 2021, 13(12), 2335, DOI 10.3390/rs13122335.**

**C.6 — Foundation models evaluated on material tasks**

- **No FM in A.1 has been benchmarked on AC roofs.** The closest is Prithvi-EO-2.0's burn-scar / flood-mapping benchmarks (HLS bands include SWIR2 ≈ 2.2 µm relevant for AC). Running the first published Prithvi-EO-2.0 or SpectralEarth AC benchmark would be a clear thesis contribution.

### D) Additional themes

**D.1 — Atmospheric correction impact**

- **Wang et al. 2022 (SuperDove radiometric accuracy)** — already cited; quantifies 6SV-based PlanetScope SR uncertainty.
- **Vermote, Justice, Claverie, Franch, "Preliminary analysis of the performance of the Landsat 8/OLI land surface reflectance product", RSE 2016, DOI 10.1016/j.rse.2016.04.008.** Reference 6SV / LaSRC citation.

**D.2 — Cross-sensor transfer**

- **DOFA (Xiong 2024)** and **AnySat (Astruc 2025)** — already cited; explicit cross-sensor models. Worth running a S2-pretrained → SuperDove fine-tune ablation.

**D.3 — Temporal stack approaches**

- **Presto (Tseng 2023) — already cited.** Pixel-time-series transformer.

**D.4 — Weak supervision / pseudo-labelling**

- MARIDA (cited above) is explicitly built for weakly-supervised pixel-level segmentation.
- **Sakti et al., "Identification of illegally dumped plastic waste in a highly polluted river in Indonesia using Sentinel-2 satellite imagery", Scientific Reports 2023, DOI 10.1038/s41598-023-32087-5.** Adjusted Plastic Index + random forest using UAV pseudo-labels for the Citarum river system.

**D.5 — Vision-language models for RS**

- **Liu et al., "RemoteCLIP: A Vision-Language Foundation Model for Remote Sensing", IEEE TGRS 2024, DOI 10.1109/TGRS.2024.3390838, arXiv:2306.11029.**
- **Kuckreja et al., "GeoChat: Grounded Large Vision-Language Model for Remote Sensing", CVPR 2024, arXiv:2311.15826.**
- These are RGB-only, so they highlight, by contrast, why a multispectral approach is needed for material discrimination.

**D.6 — Recent 2024-2026 illegal-dump papers NOT in reading list**

- **Marrocco et al., "Illegal Microdumps Detection in Multi-Mission Satellite Images With Deep Neural Network and Transfer Learning Approach", IEEE Access 12 (2024), DOI 10.1109/ACCESS.2024.3409393.** Pleiades + GeoEye-1 cross-mission transfer in Campania (Italy); RetinaNet + InceptionV3 cascade. Highly relevant — Italian case study, multispectral VHR satellites, explicit cross-sensor TL.
- **Cai et al., "CascadeDumpNet: Enhancing open dumpsite detection through deep learning and AutoML", RSE 2024 (PII S0034425724003754; DOI 10.1016/j.rse.2024.114322 — verify with publisher).** Two-stage detection with Contextual Feature Synthesis module.
- **Fraternali, Morandini, Herrera González, "A Deep Learning Pipeline for Solid Waste Detection in Remote Sensing Images", Waste Management Bulletin 2025, DOI 10.1016/j.wmb.2025.100246, arXiv:2502.06607.** From the PoliMi group itself; uses AerialWaste with WV-3 imagery; systematic GSD/context/pretraining ablation. **This paper is from the user's own department and should be cited as the immediate methodological precursor.**
- **Sharmily et al., "Automated Landfill Detection Using Deep Learning: A Comparative Study of Lightweight and Custom Architectures with the AerialWaste Dataset", arXiv:2508.18315, 2025.** Lightweight-architecture benchmarks on the AerialWaste dataset.

---

## Recommendations

**Stage 1 — citations to add immediately (high priority, < 1 week):**
1. **Aharoni-Mack et al. 2025 (Sci. Rep., EnMAP AC roofs)** — closest direct competitor; benchmark against ACE OA = 91.4%.
2. **Aguilar et al. 2021 (Almería, WV-3, NDPI ablation: 90.85% / 96.79% / 97.38%)** — structurally identical question to the thesis.
3. **Aguilar/Uhrin et al. 2025 (terrestrial macroplastics, WV-3 SWIR)** — most recent terrestrial WV-3 SWIR plastic paper.
4. **Kaur 2024 (SuperDove 4 vs 8 band: 0.94 vs 0.78–0.83)** — the sensor-specific RGB-vs-MS benchmark.
5. **Biermann et al. 2020 (FDI, Sci. Rep.)** — foundational marine-plastic spectral-index citation.
6. **Clark et al. 2003 (Tetracorder) + Kokaly et al. 2017 (splib07a)** — canonical references for the asbestos chapter.
7. **Fraternali et al. 2025 (PoliMi pipeline) + Marrocco et al. 2024 (IEEE Access)** — most recent illegal-dump literature; the former is an in-house precursor.

**Stage 2 — methodology baselines (≈ 2–4 weeks):**
8. **SatMAE++ and Prithvi-EO-2.0** as Sentinel-2 / HLS pretrained backbones for SuperDove transfer.
9. **SpectralFormer** as a transformer-only pixel-spectral baseline.
10. **MESMA + USGS splib07a (WV-3-convolved subset)** for a physics-based unmixing baseline against the DL methods — gives reviewers a "your DL doesn't beat physics" sanity check.

**Stage 3 — stretch goals (≈ 1–3 months):**
11. Run **DOFA or AnySat** in cross-sensor mode (S2 pretrain → SuperDove fine-tune) — there is no published baseline.
12. Build a **WV-3 / EnMAP SWIR ablation** showing exactly which absorption bands (2.31 µm Mg-OH, 2.20 µm Al-OH, 1.6 µm) carry the AC signal that SuperDove will MISS — directly answers "what does multispectral buy you?" by quantifying what SuperDove leaves on the table.

**Decision benchmarks that would change the recommendations:**
- If the user gains access to PRISMA / EnMAP scenes over Lombardy → upgrade B.1 / A.1.5 / A.1.6 papers to "must read", and Aharoni-Mack becomes the head-to-head reference.
- If the user is locked to SuperDove only → Aguilar 2021 + Kaur 2024 + Schmidt 2021 become the single most important triad, because they explicitly quantify the cost of dropping SWIR.
- If the user wants a foundation-model angle → Prithvi-EO-2.0 (because of its SWIR bands) and SpectralEarth (because of EnMAP pretraining) are the two highest-impact backbones.

## Caveats

- **CascadeDumpNet DOI inferred** from ScienceDirect PII; verify against the publisher record before citing.
- **HyperSIGMA pretraining sensor mix** is described as multi-source HSI (Hyperion-class); confirm exact list in §3 of the TPAMI version.
- **Aharoni-Mack et al. 2025** is currently published as Scientific Reports preceded by a Research Square preprint (10.21203/rs.3.rs-6366701/v1); confirm final DOI 10.1038/s41598-025-09738-w against the publisher.
- The user's reading-list paper #1 (J. Haz. Mat. 2026 on WV-3 VNIR AC detection) likely already cites Frassy/Bassani 2015 (paper #3) and the Bonifazi/Capobianco/Serranti 2018 J. Haz. Mat. paper — confirm to avoid redundant introduction.
- Several "2026" entries (the reading list's papers 1–2 and 7, and the Frontiers 2026 MARIDA+MADOS paper) are very recent and may still be in press; track the final DOIs.
- The "Richards M, Jones G, Rowe J. Enhanced detection of asbestos roofing in southwestern UK using Sentinel-2 and spectral unmixing. Environ Monit Assess. 2018; 190(10):581." reference cited inside Aharoni-Mack 2025 could not be cross-verified here; **independently confirm** before adopting in a literature review.
- All accuracy numbers reported in the table are taken from the cited primary sources; the user should re-verify the exact numerical claims (e.g., Aharoni-Mack ACE 91.4% / SID 90.1% / SVM 89.2% / 86% ground-truth positive-match rate; Aguilar 2021 90.85% / 96.79% / 97.38%; Kaur 2024 OA = 0.94 with 8-band SVM vs. 0.78 / 0.82 / 0.83 with 4-band) against the published PDFs before quoting in the thesis.

### Summary table

| # | Paper / resource | Gap | Year | OA | Priority | Reason |
|---|---|---|---|---|---|---|
| 1 | Aharoni-Mack et al. — EnMAP AC roofs (Sci. Rep. 2025) | B.1 | 2025 | Yes | **HIGH** ⭐ | Closest direct competitor; spaceborne HSI for AC; ACE OA 91.4% |
| 2 | Aguilar et al. — Almería WV-3 (RS 2021) | C.4 / B.6 | 2021 | Yes | **HIGH** ⭐ | VNIR 90.85% / SWIR 96.79% / All 97.38% — RGB-vs-MS canonical |
| 3 | Aguilar/Uhrin et al. — terrestrial macroplastics (EMAS 2025) | B.6 | 2025 | Yes | **HIGH** ⭐ | Latest WV-3 SWIR terrestrial work |
| 4 | Kaur 2024 — SuperDove 4 vs 8 band (Sustainable Cities) | B.5 | 2024 | No (sub) | **HIGH** ⭐ | 8-band SVM OA 0.94 vs 4-band 0.78–0.83 |
| 5 | Biermann et al. 2020 — FDI (Sci. Rep.) | A.8 / C.1 | 2020 | Yes | **HIGH** | Canonical spectral-index for material discrimination |
| 6 | Clark et al. 2003 — Tetracorder (JGR Planets) | A.3 | 2003 | Yes | **HIGH** | Canonical material-ID reference; used by NASA EMIT |
| 7 | Kokaly et al. 2017 — USGS splib07a (DS 1035) | B.4 | 2017 | Yes | **HIGH** | Required reference library (with WV-3 + S2 convolutions) |
| 8 | Fraternali et al. 2025 — DL waste pipeline (WMB) | D.6 | 2025 | Yes | **HIGH** | PoliMi-internal precursor on AerialWaste |
| 9 | Marrocco et al. 2024 — Pleiades/GeoEye microdumps (IEEE Access) | D.6 | 2024 | Yes | HIGH | Italian VHR cross-sensor transfer |
| 10 | Schmidt et al. 2021 — WV-3 polymer ID (RSE) | A.8 / B.6 | 2021 | No (sub) | HIGH ⭐ | "SWIR alone outperforms full spectrum" claim |
| 11 | Cong et al. 2022 — SatMAE (NeurIPS) | A.1 | 2022 | Yes | HIGH | Canonical multispectral MAE |
| 12 | Noman et al. 2024 — SatMAE++ (CVPR) | A.1 | 2024 | Yes | HIGH | Multi-scale upgrade |
| 13 | Hong et al. 2024 — SpectralGPT (TPAMI) | A.1 | 2024 | Yes | HIGH | Spectral-only FM; Base/Large/Huge (100/300/600M) |
| 14 | Szwarcman et al. 2024 — Prithvi-EO-2.0 | A.1 | 2024 | Yes | HIGH | HLS SWIR bands → AC absorption; 4.2M HLS training samples |
| 15 | Braham et al. 2025 — SpectralEarth (JSTARS) | A.1 | 2025 | Yes | HIGH | EnMAP HSI FM with full 420–2450 nm SWIR |
| 16 | Wang et al. 2025 — HyperSIGMA (TPAMI) | A.1 | 2025 | Yes | Medium | Large (1B+) but compute-heavy |
| 17 | Xiong et al. 2024 — DOFA | A.1 / D.2 | 2024 | Yes | HIGH | Cross-sensor wavelength conditioning |
| 18 | Astruc et al. 2025 — AnySat (CVPR) | A.1 / D.2 | 2025 | Yes | Medium | Multi-resolution; SuperDove ↔ S2 |
| 19 | Tseng et al. 2023 — Presto (NeurIPS CCAI) | A.1 | 2023 | Yes | Medium | Lightweight pixel-time-series |
| 20 | Hong et al. 2022 — SpectralFormer (TGRS) | A.2 | 2022 | Yes | HIGH | Canonical spectral transformer |
| 21 | Růžička & Markham 2025 — HyperspectralViTs (JSTARS) | A.2 | 2025 | Yes | Medium | HSI ViT; methane + mineral ID |
| 22 | Mielke et al. 2016 — EnGeoMAP 2.0 (RS) | A.3 / B.1 | 2016 | Yes | Medium | Open-source EnMAP mineral mapper |
| 23 | Roberts et al. 1998 — MESMA (RSE) | A.3 | 1998 | No | HIGH | Canonical unmixing reference |
| 24 | Bonifazi/Capobianco/Serranti 2018 — HSI asbestos (J. Haz. Mat.) | A.8 / B.4 | 2018 | No (sub) | HIGH | Lab spectra of chrysotile/amosite/crocidolite with SIMCA; Mg-OH 2300 nm, Fe-OH 2280–2343 nm |
| 25 | Tuia, Persello, Bruzzone 2016 — DA survey (GRSM) | A.5 | 2016 | Yes | Medium | Canonical DA taxonomy |
| 26 | Kikaki et al. 2022 — MARIDA (PLOS ONE) | B.2 | 2022 | Yes | Medium | S2 marine debris benchmark |
| 27 | Kikaki et al. 2024 — MADOS (ISPRS JPRS) | B.2 | 2024 | Yes | Medium | 174 S2 scenes, ~1.5M annotated pixels |
| 28 | Garaba et al. 2025 — MADLib (ESSD) | B.4 | 2025 | Yes | Medium | Plastic spectral reference library |
| 29 | Dutta et al. 2022 — PRISMA Delhi landfills (ESPR) | B.1 | 2022 | No (sub) | Medium | Only PRISMA landfill spectral-index work |
| 30 | Yang et al. 2025 — global landfill methane (ES&T) | B.1 / D.3 | 2025 | Yes | Medium | EMIT+EnMAP+PRISMA landfill survey (38 sites) |
| 31 | Booysen et al. 2025 — EnMAP mineral exp. (JAG) | B.1 / C.2 | 2025 | No (sub) | Medium | Best EnMAP mineral-mapping demo |
| 32 | Asadzadeh & de Souza Filho 2016 — HC index (RSE) | A.8 / B.6 | 2016 | No (sub) | HIGH ⭐ | WV-3 SWIR foundational |
| 33 | Wang et al. 2022 — SuperDove radiometric accuracy (JAG) | B.5 / D.1 | 2022 | No (sub) | HIGH ⭐ | SuperDove uncertainty 7.5–15.6% |
| 34 | Anwar et al. 2025 — SuperDove SNR (Frontiers in RS) | B.5 | 2025 | Yes | HIGH ⭐ | Reports per-band SNR (8:1 at 865 nm to 248:1 at 443 nm) |
| 35 | Sharmily et al. 2025 — AerialWaste lightweight benchmark (arXiv) | D.6 | 2025 | Yes | Low | Confirms baseline AerialWaste numbers |
| 36 | Sakti et al. 2023 — Citarum river plastic (Sci. Rep.) | D.4 | 2023 | Yes | Medium | Pseudo-labelling + API index for S2 |
| 37 | Liu et al. 2024 — RemoteCLIP (TGRS) | D.5 | 2024 | Yes | Low | RGB VLM; useful as contrast |
| 38 | Kuckreja et al. 2024 — GeoChat (CVPR) | D.5 | 2024 | Yes | Low | RGB VLM; useful as contrast |
| 39 | Vivone et al. 2021 — Pansharpening benchmark (GRSM) | A.6 / A.7 | 2021 | No (sub) | Low | Canonical pansharpening reference |
| 40 | Topouzelis et al. 2019 — PLP UAV+S2 (JAG) | C.1 | 2019 | No (sub) | Medium | Plastic Litter Project |

⭐ marks papers using **SuperDove or WV-3 SWIR specifically**, or directly answering the **"RGB vs multispectral added value"** question — these are the user's highest-priority reads.