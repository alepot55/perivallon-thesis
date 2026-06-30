---
title: "Datasets we can actually use for this thesis — usability panorama"
subtitle: "Re-centred on the WorldView-3 + Pléiades Neo data reality"
author: "PERIVALLON thesis · Politecnico di Milano"
date: "2026-06-27"
status: "study-ready overview — synthesised from datasets_catalog.md, datasets_study_guide.md, and iteration-1 research"
---

# 0. Read this first — the whole dataset story in 6 lines

- **Our imagery (WV-3 + Pléiades Neo) has NO labels.** We self-pair it with external label sources. So "datasets" = (1) **label sources** to attach to our imagery + (2) **public benchmarks** to develop/pretrain methods + (3) **spectral references** to justify bands + (4) **pretraining weights**.
- **The gap that is the thesis:** *no public dataset combines VHR-satellite imagery + terrestrial waste + material-level labels.* Every resource sits on one side of that hole.
- **The bridge that fills it:** take **geolocated waste/asbestos locations** (AerialWaste, the Lombardy asbestos WFS) → **re-image them with WV-3 / Pléiades Neo** → you have created the missing multiband material dataset.
- **One bridge is open now, one is gated:** the **asbestos WFS is public + geolocated → usable immediately**; **AerialWaste coordinates are withheld (ARPA confidentiality) → need an in-group agreement** (feasible — the thesis is inside the PoliMi/ARPA group, but it is a dependency to resolve).
- **The asbestos pilot is therefore the immediately-feasible dataset.** The broader 13-class waste dataset depends on the AerialWaste coordinate agreement.
- Everything else below is a *supporting* role: method baseline, spectral reference, or pretraining corpus that feeds that one experiment — none does the job for you.

---

# 1. The four roles (the lens for judging any dataset)

1. **Label source** — geolocated truth you attach to *your* WV-3/PNeo imagery (asbestos WFS, AerialWaste).
2. **Public benchmark** — labelled imagery to develop/validate method before the small AOI (EuroSAT, Toulouse, Houston).
3. **Spectral reference** — pure material signatures to justify which band matters and build endmembers (USGS splib07a, WaRM).
4. **Pretraining corpus / FM weights** — large pretraining to initialise the backbone (SSL4EO-S12, DOFA, Prithvi).

A dataset's fit for *us* is decided by three properties: **GSD** (resolves a dump/roof? our point is sub-metre VHR), **SWIR present?** (material chemistry lives at 1–2.5 µm; only WV-3 has it), **label level** (material vs land-use vs binary — the thesis needs *material*).

---

# 2. THE usability matrix — datasets we can actually use

⭐⭐⭐ = core / use directly · ⭐⭐ = important · ⭐ = supporting. "Ready?" = usable with our WV-3/PNeo setup without blockers.

## Role 1 — Label sources (the actual training data)

| Dataset | What it gives | GSD / bands | Ready? | Priority | Note |
|---|---|---|---|---|---|
| **Lombardy asbestos WFS** (`Mappatura_2020` 10,903 + `precedenti` 50,131 roofs) | geolocated asbestos-roof polygons (EPSG:32632) | vector | ✅ **public, in-repo** | ⭐⭐⭐ | the clean, immediate pilot label source — pair with WV-3/PNeo roofs |
| **AerialWaste v3** | 3,478 waste-positive locations in Lombardy + **22 material categories** + 169 seg masks | RGB 20–50 cm (incl. ~250 from WV-3, pansharpened RGB) | ⚠️ **coords withheld** (ARPA agreement needed) | ⭐⭐⭐ (gated) | the location/label bridge for the *waste* dataset; only 11 tiles tagged presumed-asbestos |
| **DroneWaste** (PERIVALLON) | 4,993 UAV images, 17 dumps, **20 material types** | cm, RGB | ✅ in-project (Zenodo) | ⭐⭐ | material taxonomy + UAV-confirmation framing; not satellite |
| **CWLD** (Beijing C&D) | pixel masks, 4 C&D classes, 3,653 samples | GF-2 0.8 m + GE 0.5 m | ✅ public (Zenodo) | ⭐ | transfer/benchmark for C&D segmentation at our GSD |

## Role 2 — Public benchmarks (method development, band ablation, transfer)

| Dataset | What for | GSD / bands | SWIR | Priority |
|---|---|---|---|---|
| **EuroSAT MS** | controlled **band-ablation testbed** (RGB→+NIR→+RedEdge→13) + adapter sanity check | 10 m, 13 S2 bands | ✅(20 m) | ⭐⭐⭐ (have locally) |
| **Toulouse Hyperspectral** (2024) | closest **public material + SWIR** benchmark; 32 urban materials → SWIR band-selection, method dev | 1 m, 310 ch VNIR+SWIR | ✅ | ⭐⭐ |
| **GRSS Houston 2013/2018 · Pavia** | urban-material HSI **method baselines** (3D-CNN reaches OA 96% on Houston) | 1–2.5 m | mixed | ⭐ |
| **SpectralWaste · RECONMATIC · Tecnalia WEEE** | **material-evidence proof** (RGB+HSI lab/conveyor); justify "spectra separate materials" | conveyor/lab | ✅ | ⭐ |
| **MARIDA / MADOS** | material-at-satellite-scale precedent (but **marine**, S2 10 m) | 10 m, S2 | ✅ | ⭐ (context only) |

## Role 3 — Spectral references (justify bands, build endmembers, SAM)

| Library | What for | Coverage | Priority |
|---|---|---|---|
| **USGS splib07a** | the reference; **WV-3 + S2 band convolutions pre-computed** → synthetic WV-3/PNeo endmembers | 350–2500 nm, 1300+ materials | ⭐⭐⭐ (in `spectral/`) |
| **WaRM** (Walloon roof materials) | **corrugated asbestos-cement** spectra — directly the pilot | 350–2500 nm, 7 roof classes | ⭐⭐ |
| **KLUM / LUMA SLUM** | urban materials (concrete, metal, PVC, plastic, tile) | VNIR+SWIR | ⭐ |
| **MADLib / Garaba** | polymer SWIR features (1215/1410/1730 nm) — why VNIR can't do polymer type | 350–2500 nm | ⭐ |
| **EnMAP asbestos field library** | 2,714 weathered/moss/paint AC spectra; chrysotile 2.32 µm Mg-OH | VNIR+SWIR | ⭐ |

## Role 4 — Pretraining corpora / foundation-model weights

| Resource | Why for us | Priority |
|---|---|---|
| **DOFA** | wavelength-conditioned → **ingests WV-3 & PNeo bands natively** (closes the band gap; not the GSD gap) | ⭐⭐⭐ |
| **SSL4EO-S12** | ready S2 pretrained weights (ResNet/ViT) — VNIR transfer baseline | ⭐⭐ |
| **Prithvi-EO-2.0** | native **SWIR1/SWIR2 bands** → matches WV-3 SWIR / asbestos 2.3 µm | ⭐⭐ |
| **SpectralEarth** | EnMAP HSI (full SWIR) pretraining — HSI reference | ⭐ |

---

# 3. The bridge, concretely (how we get a multiband material dataset)

```
ASBESTOS PILOT (open now):
  Mappatura_2020 roof polygons (public)  ──pair──>  WV-3 (VNIR+SWIR) + Pléiades Neo (VNIR) over the AOI
     → per-roof spectra → exploratory clustering / classification → asbestos vs non-asbestos
     → feeds ARPA's Indice di Degrado risk workflow (see risk framing)

WASTE DATASET (gated on agreement):
  AerialWaste positive locations (coords withheld)  ──[ARPA/Torres agreement]──>  re-image with WV-3 + PNeo
     → transfer the 22 material categories → the missing VHR-satellite + waste + material-label dataset
```

**Action implied:** secure the AerialWaste coordinates (or a coordinate-bearing subset) from the PoliMi/ARPA team early — it is the gate on the headline contribution. Until then, the asbestos pilot carries the experimental weight.

---

# 4. If you study only 8 things tomorrow

1. **Lombardy asbestos WFS** — your immediate, public label source (already in `asbestos/data`).
2. **AerialWaste v3 (Torres 2023)** — the waste label/location bridge + its **coordinate-withholding caveat**.
3. **EuroSAT MS** — your band-ablation testbed (already local).
4. **USGS splib07a** — band justification + endmembers (WV-3 convolutions; already in `spectral/`).
5. **Toulouse Hyperspectral** — the closest public material+SWIR benchmark.
6. **DOFA** — the FM that natively eats WV-3/PNeo bands.
7. **Aguilar 2021 (WV-3 VNIR/SWIR ablation)** — your yardstick for "what SWIR buys" (90.85 / 96.79 / 97.38).
8. **WaRM + EnMAP asbestos library** — the asbestos-cement spectral references for the pilot.

---

# 5. Open dataset questions for Thomas (decide the design)

1. **AerialWaste coordinates** — can we get them (or a subset) for re-imaging? This gates the waste dataset.
2. **WV-3 product** — does it include the 8 SWIR bands? (Decides whether the spectral-reference datasets and the `+SWIR` ablation are real.)
3. **AOI extent** — does the WV-3/PNeo coverage overlap AerialWaste positives and the `Mappatura_2020` roofs? (No overlap = no labels.)
4. **Material labels** — any provided, or self-annotation against AerialWaste categories + the asbestos WFS?
5. **SuperDove** — still used (free, near-daily 3 m) as a cheaper/temporal layer, or dropped?

> Full dense reference (DOIs, 42 datasets): `../datasets_catalog.md`. Role-based study guide: `../datasets_study_guide.md`. Per-class data fit: `../sota_vhr_13classes.md`.
