---
id: "wang-2023-ssl4eo-s12"
title: "SSL4EO-S12: Self-Supervised Learning for Earth Observation - Sentinel-1/2"
authors: ["Wang", "et al."]
year: 2023
venue: "arXiv"
doi: null
arxiv: "2211.07044"
link: "arXiv:2211.07044"
tags: ["foundation-model", "ssl", "sentinel-1-2"]
relevance: "high"
status: "downloaded"
pdf: "library/wang-2023-ssl4eo-s12.pdf"
in_slides: ["foundation-models"]
relates_to: []
---

## Obiettivo
Fornire pesi pretrained self-supervised per tutte le 13 bande Sentinel-2 su architetture standard.

## Metodo
MoCo-v2 (ResNet-50), DINO (ViT-S), MAE (ViT-B/L). 251K locations globali x 4 stagioni.

## Risultati
Pesi pronti per 13 bande S2 su architetture standard. Performance competitive con supervised pretraining.

## Riassunto
Il punto di partenza più pratico per Sentinel-2: pesi pretrained su tutte 13 bande, architetture note (ResNet, ViT), licenza Apache 2.0.

## Cosa riutilizzare (tesi)
Drop-in replacement per il backbone quando si usa Sentinel-2. Pesi ViT-S (DINO) come candidato per confronto con Swin-T RSP.

## Note Claude
### wang-2023-ssl4eo-s12

**Punti chiave**
- Dataset (non modello) di 3M patch 264x264 a 10m, 251k locations globali, 4 stagioni, triplet S1-GRD + S2-L1C + S2-L2A.
- Bench: 4 metodi SSL (MoCo-v2/v3, DINO, MAE, data2vec) addestrati su ResNet50 e ViT-S/16.
- Tutte e 13 bande S2 disponibili (B1-B12 + B8A). Multimodale (radar + ottico) e multi-temporale (4 timestamp).
- Cura: top-10k citta + Gaussian sampling, overlap-filtering, cloud-cover <10%, ~3.7TB raw.
- Risultati: SSL su SSL4EO-S12 batte ImageNet di ~10%, SeCo di ~6% in linear probing su EuroSAT/BigEarthNet.

**Quale problema chiave risolve per la mia tesi**
Fornisce backbone ResNet50 / ViT-S pretrained su tutte e 13 bande S2 a 10m. NON SuperDove-ready: bande S2 differiscono per centro wavelength e bandwidth. Servirebbe band-mapping (Blue/Green/Red/NIR ovvi; Coastal SuperDove vs S2-B1 simili; RedEdge SuperDove ~705nm ~ S2-B5; Yellow 612nm non ha analogo S2 -> deve essere droppato o reinizializzato). E principalmente dataset+benchmark, non un FM unico distribuito.

**Numeri forti da citare**
- 3M patch, 251k locations, 4 stagioni, 13 bande S2 + 2 SAR.
- MoCo+DINO ResNet50 raggiunge 99.1% EuroSAT fine-tune, 86.2% BigEarthNet-10% mAP.
- Multimodale (S1+S2) batte single-modality di 1-4% su BigEarthNet-1%.
- Tempo pretrain 100 epoche: 18-25h su 4x A100.

**Limite onesto (gap che lasciano):**
Non e un FM unico ma una collezione di checkpoint SSL su S2 10m -> rigid sui sensori. ResNet50/ViT-S sono backbone leggeri, non scalano come ViT-L. Bias geografico (top citta + cloud filtering = poche regioni polari/tropicali umide). Per material classification SuperDove serve sub-banda Yellow 612nm e GSD 3m, entrambi assenti in pretrain.

**Cross-link**
Dataset usato da `wang-2024-softcon` (SoftCon ne distilla labels), `xiong-2024-dofa` (DOFA usa Sentinel-2 da fonti simili), `szwarcman-2024-prithvi-eo2` (Prithvi usa HLS, alternativa). E il "baseline dataset" per la generazione SSL pre-DOFA. Citato come precursore in `fm-rs-survey-2024`.
