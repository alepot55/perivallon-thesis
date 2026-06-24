---
id: "anysat-2024"
title: "AnySat: An Earth Observation Model for Any Resolutions, Scales, and Modalities"
authors: ["Astruc", "et al."]
year: 2025
venue: "arXiv"
doi: null
arxiv: "2412.14123"
link: "arXiv:2412.14123"
tags: ["foundation-model", "any-resolution", "any-modality"]
relevance: "high"
status: "downloaded"
pdf: "library/anysat-2024.pdf"
in_slides: ["foundation-models"]
relates_to: []
---

## Obiettivo
Creare un modello EO che gestisce qualsiasi risoluzione, scala e modalità in un singolo framework.

## Metodo
Architettura multi-risoluzione e multi-modale con joint embedding. Pretrained su dati eterogenei.

## Risultati
Competitive con modelli specializzati su benchmark multipli. Un singolo modello per input eterogenei.

## Riassunto
Architettura alternativa a DOFA per il problema multi-sensore/multi-risoluzione.

## Cosa riutilizzare (tesi)
Da monitorare come alternativa a DOFA se servono input a risoluzioni miste (es. S2 10m + S2 20m nello stesso modello).

## Note Claude
### anysat-2024

**Punti chiave**
- Architettura JEPA (Joint Embedding Predictive) multimodale + scale-adaptive patch encoder che gestisce qualsiasi risoluzione/scala/modalita.
- Patch divisi in sub-patch di dimensione fissa delta_m (in pixel) -> # token varia con risoluzione, ma encoder e fisso.
- Modality-specific MLP di proiezione (phi^proj), shared spatial transformer (phi^trans), modality combiner cross-attention.
- Pretrain SSL su GeoPlex: 5 dataset (TreeSatAI-TS, FLAIR, PLANTED, S2NAIP-URBAN, PASTIS-HD), 11 sensori distinti, risoluzioni 0.2-250m, scale 0.36-164 hectares.
- Sensori inclusi: Aerial RGB+NIR 0.2m, NAIP 1.25m, SPOT6 1.5m, Sentinel-1/2 10m, Landsat 7/8/9 30m, ALOS-2, MODIS 250m.

**Quale problema chiave risolve per la mia tesi**
Concorrente diretto di DOFA con filosofia diversa: invece di hypernetwork wavelength-conditioned (DOFA), AnySat usa modality-specific projection + cross-attention combiner. Crucially per SuperDove: AnySat NON ha visto SuperDove in pretrain ma "impara sensor-specific scalar" durante SSL e puo gestire nuovi sensori in fine-tuning via random-init projection. SuperDove cadrebbe in fine-tune-only (no probing). GSD 3m e dentro pretrain range. Bande SuperDove richiederebbero comunque mapping.

**Numeri forti da citare**
- 5 dataset / 11 sensori distinti / 249k km2 / 171B pixel pretrain.
- SOTA su 9 task downstream (semseg, classif, change det, regression).
- ~75% dei parametri shared cross-modality (efficiency).
- Channel count gestiti: 3-11 bande native (TreeSatAI ha 11 ch S1+S2).

**Limite onesto (gap che lasciano):**
SSL su 5 dataset = scala modesta vs DOFA (8M) o Prithvi (4.2M). Nessun sensore VNIR a 8 bande tipo SuperDove/WV3 in pretrain -> SuperDove resta out-of-distribution. Per probing servirebbe matching geometrico con un sensore visto -> per nuovi sensori "only fine-tune", che limita il caso plug-and-play. Per sensori "too different from training mix" non e probing-ready, esplicitamente.

**Cross-link**
Diretto vs `xiong-2024-dofa` (entrambi any-modality, DOFA via hypernetwork, AnySat via JEPA+combiner). Cita OmniSat come predecessore. Complementare a `cong-2022-satmae` (SatMAE = baseline storico multispectral). Compete con `szwarcman-2024-prithvi-eo2` ma su scala/scope diverso (Prithvi profondo su HLS, AnySat largo su sensori). Citato in `fm-rs-survey-2024` come trend "versatile EO models".
