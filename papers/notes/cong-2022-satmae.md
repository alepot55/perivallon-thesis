---
id: "cong-2022-satmae"
title: "SatMAE: Pre-training Transformers for Temporal and Multi-Spectral Satellite Imagery"
authors: ["Cong", "et al."]
year: 2022
venue: "NeurIPS"
doi: null
arxiv: "2207.08051"
link: "arXiv:2207.08051"
tags: ["foundation-model", "multispectral", "pretraining"]
relevance: "high"
status: "downloaded"
pdf: "library/cong-2022-satmae.pdf"
in_slides: ["foundation-models"]
relates_to: []
---

## Obiettivo
Adattare il pretraining MAE a immagini satellitari multispettrali e multi-temporali.

## Metodo
Band grouping per risoluzione (10m, 20m) con patch embedding separati. Spectral positional encoding. MAE pretraining su fMoW-Sentinel.

## Risultati
+7% su benchmark supervisionati, +14% su transfer learning vs RGB-only. Il guadagno nel TL indica rappresentazioni MS generalizzabili.

## Riassunto
Introduce band grouping e spectral positional encoding per Sentinel-2. Dimostra che il pretraining multispettrale migliora significativamente il downstream, specialmente in transfer learning.

## Cosa riutilizzare (tesi)
Architettura di band grouping (idea per gestire bande a risoluzioni diverse). Spectral positional encoding. Evidenza quantitativa del delta RGB-MS.

## Note Claude
### cong-2022-satmae

**Punti chiave**
- MAE adattato a satellite: 2 idee chiave = (a) temporal encoding + masking indipendente per time-series fMoW; (b) band grouping per multispettrale Sentinel-2.
- Band groups Sentinel-2: 3 gruppi per risoluzione/wavelength: RGB+NIR (B2,B3,B4,B8), RedEdge (B5,B6,B7,B8A), SWIR (B11,B12). Drop B1/B9/B10 (60m).
- Spectral positional encoding additivo per identificare il gruppo.
- ViT-Large pretrained su fMoW-Sentinel (~713k immagini, 12 bande S2 = B1-B12 + B8A).
- Risultati: +6.27% su fMoW vs supervised scratch; +14% transfer su EuroSAT vs ImageNet init.

**Quale problema chiave risolve per la mia tesi**
Modello FM "classico" per multispettrale: NON sensor-agnostico ma flessibile via grouping. Per SuperDove dovrei: ridefinire gruppi (Coastal+Blue+Green+Yellow / Red+RedEdge / NIR) e reinizializzare patch embedding. Approccio "intermedio" tra band-stack e DOFA. Storicamente importante: baseline che ogni paper FM successivo (DOFA, SoftCon, SpectralGPT, Prithvi) cita come predecessore.

**Numeri forti da citare**
- ViT-Large, fMoW-Sentinel: 61.48% top-1 acc, +5.4% vs supervised ImageNet init.
- EuroSAT: SatMAE+Group+IM raggiunge 98.98% (SOTA in 2022).
- BigEarthNet mAP 82.13.
- 10 bande utili / 13 Sentinel-2 (drop di B1/B9/B10 60m).

**Limite onesto (gap che lasciano):**
Band grouping rigido va riadattato per ogni nuovo sensore (no auto-discovery). Pretrain solo a 10/20m S2 (no high-res). Architettura datata: superata da DOFA, Prithvi-2, SpectralGPT in pari datasets. Generalizzazione cross-sensor mai testata nel paper. Patch embedding richiede reinit per # bande diverso da 10.

**Cross-link**
Predecessore di tutti i FM multispettrali successivi. Diretto vs `xiong-2024-dofa` (DOFA risolve il problema rigid-grouping con hypernetwork), `spectralgpt-2024` (3D masking invece di grouping piatto), `szwarcman-2024-prithvi-eo2` (Prithvi 3D temporal MAE) e `wang-2024-softcon` (contrastive vs MAE). Citato in `fm-rs-survey-2024` Tab III.
