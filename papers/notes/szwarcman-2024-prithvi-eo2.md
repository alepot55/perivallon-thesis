---
id: "szwarcman-2024-prithvi-eo2"
title: "Prithvi-EO-2.0: A Versatile Multi-Temporal Foundation Model for Earth Observation"
authors: ["Szwarcman", "et al."]
year: 2024
venue: "arXiv"
doi: null
arxiv: "2412.02732"
link: "arXiv:2412.02732"
tags: ["foundation-model", "nasa-ibm", "multi-temporal"]
relevance: "high"
status: "downloaded"
pdf: "library/szwarcman-2024-prithvi-eo2.pdf"
in_slides: ["foundation-models"]
relates_to: []
---

## Obiettivo
Creare un foundation model scalabile per EO con supporto nativo multi-temporale e multi-spettrale.

## Metodo
ViT 600M parametri, 3D patch embeddings (spazio+tempo). MAE pretraining su 4.2M campioni HLS (6 bande: Blue, Green, Red, Narrow NIR, SWIR1, SWIR2).

## Risultati
75.6% media su GEO-Bench, +8pp vs 6 altri foundation models. Supporta change detection via input multi-temporale.

## Riassunto
Foundation model NASA/IBM con supporto nativo SWIR. Le 6 bande HLS includono le bande critiche per material discrimination. Fine-tuning via TerraTorch.

## Cosa riutilizzare (tesi)
Backbone alternativo con SWIR nativo. Se i dati sono Sentinel-2 ritagliati alle 6 bande HLS, è drop-in. Pesi su HuggingFace.

## Note Claude
### szwarcman-2024-prithvi-eo2

**Punti chiave**
- MAE 3D (T x H x W) su 4.2M campioni HLS (Harmonized Landsat-Sentinel-2) a 30 m, 2014-2023, sequenze temporali di 4 timestamp.
- 6 bande fisse: Blue/Green/Red/NIR/SWIR1/SWIR2 (le comuni S2 + Landsat). Encoding metadata location (lat/lon) + time (year, day-of-year).
- ViT-L 300M e ViT-H 600M parametri; conv3D patch embedding 1x16x16; varianti TL (con time/location) e plain.
- Pretrain: 80 GPU A100 (21k GPU-h) per 300M, 240 GPU (58k GPU-h) per 600M.
- Distribuito via HuggingFace IBM-NASA-geospatial + TerraTorch (PyTorch Lightning + TorchGeo).

**Quale problema chiave risolve per la mia tesi**
NON SuperDove-ready in modo nativo: pretrain fissato a 6 bande HLS specifiche a 30m. Per usarlo con SuperDove servirebbe (a) selezionare le 4 bande SuperDove sovrapposte (Blue/Green/Red/NIR) scartando Coastal/Yellow/RedEdge, (b) accettare un domain gap GSD enorme (30m -> 3m, fattore 10x). Multi-temporale utile solo se hai stack temporali SuperDove. Verdict: candidato debole per la tesi SuperDove.

**Numeri forti da citare**
- 600M parametri, +8% vs Prithvi-EO-1.0 medio su GEO-Bench.
- Batte 6 GFM concorrenti (Scale-MAE, SatMAE, DOFA, Satlas, Prithvi-1.0, MOCO) su task GEO-Bench.
- 4.2M sample pretrain, scala maggiore di tutti i concorrenti tabulati nel paper.
- Test su risoluzioni 0.1-15m (downscaling) -> generalizza ma con perdita.

**Limite onesto (gap che lasciano):**
Vincolato a 6 bande HLS specifiche. Nessun supporto wavelength-agnostic. Pensato per task land-cover/disaster a media risoluzione (30 m), non per material classification a 3m. Nessun benchmark su sensori 3m-5m nel paper (test su Sen1Floods11 S2 10m). Per SuperDove servirebbe continual pretraining ad hoc.

**Cross-link**
Compete con `xiong-2024-dofa` (DOFA molto piu flessibile sui sensori), `wang-2023-ssl4eo-s12` (SSL S1+S2 invece di HLS), `cong-2022-satmae` (MAE+grouping anziche 3D MAE). Survey `fm-rs-survey-2024` lo cataloga come "video-style temporal MAE". DEFLECT (`thoreau-2025-deflect`) testato anche su Prithvi.
