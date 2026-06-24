---
id: "xiong-2024-dofa"
title: "Neural Plasticity-Inspired Foundation Model for Observing the Earth Crossing Modalities (DOFA)"
authors: ["Xiong", "et al."]
year: 2024
venue: "arXiv"
doi: null
arxiv: "2403.15356"
link: "arXiv:2403.15356"
tags: ["foundation-model", "dofa", "cross-modal", "any-bands"]
relevance: "critical"
status: "downloaded"
pdf: "library/xiong-2024-dofa.pdf"
in_slides: ["foundation-models", "approach"]
relates_to: []
---

## Obiettivo
Creare un foundation model sensor-agnostico che accetta qualsiasi numero di bande da qualsiasi sensore.

## Metodo
Dynamic hypernetwork condizionato sulle lunghezze d'onda centrali dei canali. Genera i pesi del patch embedding al volo. Pretrained su 5 modalità EO.

## Risultati
Competitive con modelli sensor-specific. Un singolo modello per tutti i sensori. Integrato in TorchGeo.

## Riassunto
Approccio elegante al problema multi-sensore: invece di adattare i pesi, li genera dinamicamente in funzione delle wavelength. Massima flessibilità.

## Cosa riutilizzare (tesi)
Backbone per esperimenti multi-sensore (train su S2, test su SuperDove). Integrazione TorchGeo semplifica l'uso.

## Note Claude
### xiong-2024-dofa

**Punti chiave**
- Hypernetwork dinamica condizionata sulle wavelength centrali di ogni banda: genera i pesi del patch embedding al volo, indipendente dal numero di canali.
- Pretrain MIM (masked image modeling) su 5 modalita EO: Sentinel-1 (2 SAR), Sentinel-2 (9 MS), Gaofen (4 MS), NAIP (3 RGB), EnMAP (202 HSI), ~8M campioni.
- ViT-Base e ViT-Large (~300M). DOFA+ aggiunge distillation da DINOv2 + pretrain compatto su ~410k tile.
- Richiede solo metadata wavelength (nm) come input ausiliario; nessuna fine-tuning del patch embedding.
- Integrato in TorchGeo; checkpoint pubblici.

**Quale problema chiave risolve per la mia tesi**
SuperDove-ready out-of-the-box: passi le 8 wavelength centrali (443/490/531/565/610/665/705/865 nm) e funziona senza retraining. Risolve esattamente il sensor-mismatch S2-to-SuperDove che e il discriminante della tesi. Plug-and-play per linear probing; fine-tune leggero possibile.

**Numeri forti da citare**
- Pretrain su 5 modalita, fino a 202 bande (EnMAP) gestite simultaneamente.
- DOFA-Base 86M / DOFA-Large 300M params; DOFA+ batte SOTA su GEO-Bench m-eurosat / m-bigearthnet / m-so2sat con 50 epoche, cost-compact.
- Valutato su 22+ task downstream (classification, segmentation, detection, change detection).
- Strong performance su m-forestnet (Landsat-8) mai visto in pretrain -> evidenza generalizzazione cross-sensor.

**Limite onesto (gap che lasciano):**
GSD range pretrain 1-30 m: SuperDove a 3 m e dentro range, ma il modello ha visto pochi dati ad alta risoluzione (NAIP 1m e 3-band RGB only). Nessun pretrain a 50 cm (gap rispetto AerialWaste AGEA/WV3). Hypernetwork qualita dipende da quanto le wavelength SuperDove "interpolano" rispetto a quelle viste -> bande Coastal/Yellow/RedEdge SuperDove sono novel e potenzialmente sotto-rappresentate.

**Cross-link**
Compete direttamente con `anysat-2024` (any-modality via JEPA invece di hypernetwork), `spectralgpt-2024` (3D masking specifico spettrale, S2-only), `szwarcman-2024-prithvi-eo2` (HLS-only, 6 bande fisse). DEFLECT (`thoreau-2025-deflect`) e complementare: DOFA come base + DEFLECT come adapter PEFT. SatMAE (`cong-2022-satmae`) e generazione precedente, S2-only con grouping fisso.
