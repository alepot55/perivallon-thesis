# Dataset & Acquisition Verification Report — WV-3 + Pléiades Neo over Lombardia

*Autonomous research loop, iteration 2 (2026-06-27). Scope: what is genuinely USABLE for the MS-vs-RGB-at-VHR waste/risk thesis. Verification corrections are already folded in — refuted claims dropped, uncertain ones downgraded. Confidence tags: **[HIGH]** primary-source-verified · **[MEDIUM]** reasonable/vendor · **[UNCERTAIN]** must confirm before relying on it.*

---

## 0. Two hard corrections from this round (read first)

1. **WV-3 SWIR is NOT export-capped at 7.5 m.** The old NOAA/NGA 7.5 m cap was relaxed (~Feb 2018). The ESA catalog now lists WV-3 SWIR "at 3.7 m or 7.5 m (depending on collection date)", and archived WV-3 SWIR is deliverable at **native 3.7 m**. Any earlier "≤7.5 m hard ceiling" framing is **dropped**. The SWIR risk is *availability over the specific AOI*, not resolution. **[HIGH]**
   Sources: [ESA WV-3 catalog](https://earth.esa.int/eogateway/catalog/worldview-3-full-archive-and-tasking), [Apollo SWIR 3.7 m update](https://apollomapping.com/blog/worldview-3-swir-update-3-7-meter-resolution-updated-pricing).
2. **Microsoft GlobalMLBuildingFootprints is ODbL, not CDLA-Permissive.** The repo LICENSE is Open Data Commons ODbL — *share-alike*, the same constraint as OSM. The argument "use Microsoft footprints to avoid OSM's share-alike" is **void**: both are share-alike. For clean licensing use the **regional DBT `edificato`** layer (CC-BY) as the authoritative footprints. **[HIGH]**
   Source: [GitHub LICENSE](https://github.com/microsoft/GlobalMLBuildingFootprints/blob/main/LICENSE).

---

## 1. Imagery acquisition — the recommended path

**Go ESA Third Party Missions (TPM), archive-first.** Both sensors are free to an Italy/PoliMi researcher for non-commercial civil EO research, via a **Project Proposal (Restrained)**. This is the correct channel for a master's thesis. **[HIGH]**

| | WorldView-3 (Maxar/Vantor) | Pléiades Neo (Airbus) |
|---|---|---|
| ESA TPM access | Project Proposal (Restrained) | Project Proposal (Restrained) |
| Products | Pan 0.31 m, MS 8-band 1.24 m, **SWIR 3.7 m** | Pan 0.30 m, MS 6-band 1.2 m (Deep Blue, Red Edge) |
| Eligibility | ESA Member/Cooperating/Associate states + Canada | same |
| Evaluation | **normally within 9 weeks** (use 9 wk, not "4–6") | within 9 weeks |
| Quota | km²-based, archive vs new-tasking split, consume **within 1 year** | same |

- Access mechanism, eligibility, 9-week evaluation, quota structure = **[HIGH]** (both catalog pages verified).
- **Exact km² ceiling = [UNCERTAIN].** ESA publishes no fixed number; it is negotiated per-proposal ("limited number of products within quota limits"). Do **not** quote the "230–1,161 km²" figure that circulates online — that is OneAtlas *commercial* Living Library, not the TPM quota. Write the requested volume into the proposal and confirm with ESA.
- **Pre-screen before proposing:** draw the AOI in Maxar/Vantor catalog (WV-3) and Airbus OneAtlas/GeoStore (PNeo), confirm scenes exist, then name scene IDs in the proposal. ESA draws from these same archives. **[HIGH]**
- **Timeline imperative:** submit ASAP given Oct/Dec-2026 targets — 9 wk evaluation + 1-yr consumption window.

Sources: [WV-3 catalog](https://earth.esa.int/eogateway/catalog/worldview-3-full-archive-and-tasking) · [PNeo catalog](https://earth.esa.int/eogateway/catalog/pleiades-neo-full-archive-and-tasking) · [TPM data access guide](https://earth.esa.int/eogateway/documents/20142/37627/Third-Party-Mission-Data-Access-Guide.pdf).

### 1.1 The SWIR availability risk (the key feasibility flag)
WV-3 SWIR is a **separately-tasked product**, collected selectively, so its archive is far sparser than VNIR and **over a small Lombardy AOI may be thin or absent**. **[HIGH that it's tasked separately; MEDIUM that AOI archive is thin].** Action:
- Verify SWIR archive scene-by-scene in the Maxar catalog before committing experiments.
- If absent, request **new SWIR tasking** inside the proposal's "new acquisition" quota slice (weeks–months lead, weather-dependent, burns quota faster).
- **Contingency to raise with Thomas early:** if SWIR over the AOI is unavailable, the SWIR-value claim falls back to VNIR-only WV-3 (8-band) + PNeo (6-band), with SWIR argued via literature (Aguilar-2021). Note SWIR resolution is *not* the constraint anymore — only availability.

### 1.2 Commercial pricing (sanity check only — all [UNCERTAIN], vendor list figures)
Pléiades VHR archive ~€18/km², 25 km² min order; WV-3 25 km² min, per-km² by quote; new tasking materially pricier than archive. Treat as order-of-magnitude; ESA TPM should make this moot. Sources: [Apollo price list](https://apollomapping.com/image_downloads/Apollo_Mapping_Imagery_Price_List.pdf), [LAND INFO](https://landinfo.com/satellite-imagery-pricing/).

---

## 2. Lombardy label & auxiliary layers (self-annotation backbone)

All Regione Lombardia layers are on one ArcGIS infra (`cartografia.servizirl.it`), **EPSG:32632** (same CRS as your `.gpkg` and the imagery AOI) → co-registerable with WV-3/PNeo tiles with **no reprojection**. One bbox `query?...&f=geojson` helper retrieves any layer per tile, then rasterize to masks/aux-channels.

### 2.1 Asbestos-cement roof layer — your single most valuable label source **[HIGH]**
- Polygon footprints of AC roofs across Lombardy (Phase 1 from 2007–2018 aerial; Phase 2 = 2020, ~1,300 km²; last revision 2021-12-31). This is the polygon backing of your `Mappatura_2020` (10,903) + `Mappature_precedenti` (50,131).
- **Endpoints verified live:** WFS `…/expo/services/gpt/coperture_amianto/MapServer/WFSServer?`; ArcGIS REST `…/expo/rest/services/gpt/coperture_amianto/MapServer` → `/0/query?where=1=1&geometry=<bbox>&inSR=32632&outFields=*&f=geojson`. Service resolves; layers "Coperture rilevate nel 2020" + "Coperture già esistenti 2007-2012-2015-2018"; SR 32632. CC-BY 4.0.
- **Risk-relevant status code (1=present, 2=removed, 3=removed+PV, 4=demolished): [UNCERTAIN].** Endpoint confirmed but the exact attribute-code → meaning mapping was **not verified** — confirm against the layer field metadata before using it for the RISK head or change-detection.

### 2.2 DUSAF 7.0 land-use/land-cover — context + weak labels + negatives **[HIGH layer; MEDIUM details]**
- Region-wide LULC, CORINE-derived. **Class 13** "Aree estrattive, discariche…" splits into **131 Cave, 132 Discariche, 133 Cantieri, 134 Aree degradate non utilizzate** — near-1:1 with illegal-waste contexts.
- REST: `…/arcgis1/rest/services/territorio/dusaf7/MapServer` (JSON/geoJSON, EPSG:32632); bulk shapefile via Geoportale "Download dati".
- License **CC-BY 4.0 = [MEDIUM]** (Regione IIT default; per-layer tag not pulled). MMU ~1,600 m² and the 131–134 subdivision = **[MEDIUM]**, confirm in DUSAF struttura PDF.
- Use: (a) context channel/prior; (b) confirmed agricultural/forest = clean negatives; (c) 132/134 = weak/candidate positives.

### 2.3 Contaminated/remediated sites (AGISCO / ARPA) **[HIGH]**
- Official ARPA regional register (d.lgs 152/2006). REST `…/expo/rest/services/gpt/siti_bonificati_contaminati/MapServer`; WMS available. EPSG:32632, CC-BY 4.0.
- **Geometry is POINT, not footprint** — use as site-centroid risk prior, not a pixel mask. "Activity type" attribute is directly risk-relevant.

### 2.4 Building footprints — use regional DBT, not the global sets **[HIGH]**
- **DBGT/DBTR `edificato`**: aerophotogrammetric footprints at 1:2,000 urban / 1:5,000 extra-urban — sub-metre-class accuracy, matched to PNeo/WV-3 pan, **CC-BY 4.0**. No roof-material field (rely on §2.1 + spectral classification). Download by municipality via Geoportale.
- **Fallbacks both carry share-alike: Microsoft GlobalMLBuildingFootprints = ODbL (corrected), OSM = ODbL.** VIDA combined (source.coop) is convenient but inherits ODbL. **Google Open Buildings does NOT cover Italy** — exclude. **[HIGH]**
- **Recommendation:** DBT `edificato` is the authoritative, cleanly-licensed footprint layer; reserve MS/OSM only for gap-cross-check, and note their ODbL share-alike if you publish derived data.

### 2.5 National ISPRA layers (coarse context) **[MEDIUM]**
- *Consumo di suolo* (10 m grid, WMS/WFS from 2025) — change/recently-sealed-ground signal near candidate sites.
- *SIN perimeters* via ReNDiS-web (shapefile + WFS/WMS) — few in Lombardy (Brescia-Caffaro, Sesto S.G., Pioltello-Rodano, Broni) — high-risk priors.

### 2.6 Label hierarchy for self-annotation
Hard positives = asbestos polygons (§2.1). Weak/candidate positives = DUSAF 132/134 + AGISCO points. Clean negatives = DUSAF agricultural/forest. Building-vs-ground constraint = DBT `edificato`. Ready-made RISK attributes = asbestos status code (pending §2.1 verification) + AGISCO activity type; all else feeds detection/context, with material/risk discrimination carried by the MS spectral signal.

---

## 3. Recovering the multiband WV-3 behind AerialWaste

AerialWaste's WV-3 tiles (Torres & Fraternali 2023, verified): **pansharpened RGB, no NIR**, ~30 cm GSD, ~700×700 px, **2021 campaign**, **not geo-referenced (coordinates sensitive)**, built with **ARPA Lombardia**. No WV-3 count, scene IDs, or dates published (~250 positives is an estimate). **[HIGH]** → the source scenes are **not identifiable from the published artifacts alone**; recovery is blocked without ARPA geolocation.

Recovery routes (all conditional — treat as "ask ARPA", not facts):
- **Route A (best, fastest) [MEDIUM]:** Ask ARPA/Regione for the **original WV-3 deliverables** (≥8-band VNIR ±SWIR) from the 2021 campaign. The RGB tiles are a derivative (pansharpen→crop→drop NIR); ARPA likely still hold the source MS. Only route guaranteeing co-location with the exact labeled tiles.
- **Route B (fallback) [MEDIUM, conditional]:** Re-pull 8-band VNIR (1.24 m) from the Maxar archive via ESA TPM — **requires ARPA coordinates + dates** (so it depends on Route A info anyway). Recovers native 8-band MS (coarser GSD than the 30 cm chip, but better for material discrimination).
- **SWIR for those tiles [UNCERTAIN]:** unknown whether SWIR was collected on those 2021 strips; do not build the MS-value argument on AerialWaste-SWIR. Your **advisor-provided WV-3 (8 VNIR + 8 SWIR @3.7 m)** is the primary SWIR vehicle. (Note: 3.7 m IS available — the old 7.5 m pessimism is dropped.)

**Action — ask Thomas/ARPA two questions:** (1) Do they retain the original WV-3 MS deliverables from the 2021 campaign? (2) If not, can they release coordinates + dates for the ~250 WV-3 positives so PoliMi can pull native 8-band VNIR free via ESA TPM?

**Marrocco et al. 2024** (IEEE Access, gold-OA, paper readable) — Pléiades→GeoEye microdumps, Campania; **dataset not public** (commercial imagery, no Zenodo/GitHub). Ital-IA 2025 follow-up worth checking for a release. No other new *public* Italian VHR waste dataset; AerialWaste remains the only openly redistributed one.

---

## 4. Genuinely new datasets (2025–2026 sweep)

Only **two** new datasets surfaced — both roof-material, both **optical-only, no SWIR, no asbestos class** — so neither displaces the WV-3 SWIR angle.

- **RoofNet (2025) [MEDIUM]:** 51,503 tiles, 14 roof-material classes, 184 sites/112 countries, RemoteCLIP ViT-L/14 fine-tune. **No asbestos class.** "RGB-only" = **[UNCERTAIN]** (abstract says "multimodal EO+text"; imagery band count not stated). **License correction: CC BY-NC 4.0 with derived geodata under OSM ODbL.** Value: a "RGB-only ceiling" baseline that *reinforces* the MS-contribution argument. Not a Lombardy label source. [arXiv 2505.19358](https://arxiv.org/abs/2505.19358), Kaggle `noellelaw/roofnet`.
- **RoofSense (2025, ISPRS Annals) [UNCERTAIN — not independently re-verified]:** 8 cm aerial + LiDAR, 8 roof-material classes, NL; "multimodal" = optical+geometric, **no NIR/SWIR**, likely no asbestos. Methodological reference for material segmentation + class-imbalance weighting; marginal as data. [ISPRS Annals X-4-W6-2025](https://isprs-annals.copernicus.org/articles/X-4-W6-2025/153/2025/), GitHub `DimitrisMantas/RoofSense`.

**Verified negatives (valuable closures) [MEDIUM — clean negatives are inherently uncertain]:**
- No new public VHR sub-metre waste/dumpsite dataset with material labels beyond AerialWaste v3 + CWLD-Beijing (2024). arXiv 2508.18315 and 2502.06607 are **methods reusing AerialWaste**, not new datasets.
- No new public asbestos/roof-material VHR-MS *dataset* in 2025–26. The 2026 asbestos papers (WV-3 VNIR-only ACR detection; LMIC risk mapping; the MDPI Geomatics 6(3):41 Lombardy ACR Python workflow = your already-cataloged bonifazi-2026) are **methods/code, not labeled datasets**.
- No new Chinese GF/ZY waste or roof-material dataset beyond CWLD-Beijing.
- No new Italian/EU MS waste-material RS dataset (consistent with the coordinates-withheld situation).

Out-of-scope (flagged, skip): Mivia-IWDD (surveillance video), C&D-waste seg (ground-level), Electrolyzers-HSI (lab), FLAIR-HUB (land-cover, no roof-material/SWIR-at-VHR).

---

## 5. Foundation-model & baseline fit (band-ablation backbones)

Decisive question per model: **can it ingest arbitrary band sets by wavelength** (serves every ablation rung with one trunk) or is it **fixed to a band template**?

| Model | Band handling | Role | Conf. |
|---|---|---|---|
| **DOFA** | Wavelength-conditioned hypernetwork on band centers → any channel count from any sensor; pretrained S1/S2/Gaofen-2/NAIP/**EnMAP** (genuine SWIR exposure) | **Primary FM** — structural fairness: only the `wavelengths` arg + channel count change across rungs and across WV-3/PNeo | **[HIGH]** |
| **Swin-T + RSP** (your baseline, 95.2% F1 RGB) | Stem extended via `swin_ms_adapter`: `weight_inflation` (headline R0–R2), `late_fusion` (R3, handles VNIR 1.24 m + SWIR 3.7 m as branches), `random_init_extra` (robustness) | **Headline supervised** | **[HIGH]** |
| **CNN from scratch** (ResNet-50 / lean Swin, no pretrain) | Re-instantiate stem per rung | **Bias-free info-content control** (RGB & MS start equal) | **[HIGH]** |
| **SpectralFormer** (Hong 2022) | Band-Embedding mode (not group/CAF — only 6–16 bands) | **Spectra-only argument** (is the signal in spectra or texture?) | **[MEDIUM]** |
| **Prithvi-EO-2.0** | **Fixed 6-band: Blue,Green,Red,NarrowNIR,SWIR1,SWIR2**, HLS 30 m, not wavelength-conditioned → poor pure-ablation, valid R3 point | **SWIR-specialist comparison at R3 (WV-3 only)** | **[HIGH]** |
| **AnySat** | 3–12 ch, **0.2–500 m** (VHR in range); modality-based, 12-ch cap → R3 (16 band) needs VNIR/SWIR split | Optional multi-sensor | **[MEDIUM]** |
| **SpectralGPT** | Fixed S2 12-band, 3D-ViT, no wavelength conditioning | Optional 3rd FM point | **[MEDIUM]** |

**Net:** DOFA = FM spine (carries the whole ablation cleanly); Swin-T+RSP weight_inflation = supervised headline; CNN-from-scratch = unbiased control; Prithvi = R3 SWIR specialist. Drive through **TorchGeo** (DOFA wrappers, band-subset selection = the natural place to implement rungs) + **TerraTorch** (Prithvi), with **rasterio** (windowed reads, SWIR resampling) and **geopandas** (load EPSG:32632 vectors, spatial-join self-pairing, spatially-blocked splits).

**Two GSD gaps to state explicitly [HIGH]:** (1) pretrain↔target (FMs trained at 10–30 m vs your 0.3–1.24 m → fine-tune, don't linear-probe; AnySat alone natively spans 0.2 m); (2) within-WV-3 VNIR 1.24 m vs SWIR 3.7 m → upsample SWIR to VNIR grid (recommended default) or late-fusion two-branch; never downsample VNIR. Hold the chosen handling identical across R3 variants so the SWIR delta is spectra, not resampling.

Sources: [DOFA arXiv 2403.15356](https://arxiv.org/abs/2403.15356) · [Prithvi-EO-2.0 HF](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-300M-TL) · [AnySat arXiv 2412.14123](https://arxiv.org/abs/2412.14123) · [Maxar WV-3 radiometric note](https://dg-cms-uploads-production.s3.amazonaws.com/uploads/document/file/207/Radiometric_Use_of_WorldView-3_v2.pdf) · [Pléiades Neo eoPortal](https://www.eoportal.org/satellite-missions/pleiades-neo).

---

## 6. Bottom line

1. **ESA TPM, archive-first, submit ASAP** — free for PoliMi, both sensors incl. native-3.7 m SWIR; budget 9 wk eval + 1-yr window. **[HIGH]**
2. **SWIR availability over the AOI is the real risk** (not resolution) — verify per-AOI before designing; tasking as fallback. **[HIGH]**
3. **Asbestos WFS is the cleanest label anchor**; pair imagery↔labels directly in EPSG:32632. Verify the status-code semantics before using them for risk/change. **[HIGH layer; UNCERTAIN codes]**
4. **AerialWaste MS recovery is conditional on ARPA** — ask the two questions; do not assume. **[UNCERTAIN]**
5. **No new dataset displaces the thesis angle**; RoofNet usefully anchors the RGB ceiling. **[MEDIUM]**
6. **DOFA + Swin-RSP + CNN-scratch** is the honest three-axis backbone set; Prithvi at R3 only. **[HIGH]**
