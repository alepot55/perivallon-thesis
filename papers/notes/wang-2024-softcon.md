---
id: "wang-2024-softcon"
title: "SoftCon: Simulation Opportunity-driven Foundation Training with Contrastive learning for multi-label RS"
authors: ["Wang", "et al."]
year: 2024
venue: "arXiv"
doi: null
arxiv: "2405.20462"
link: "arXiv:2405.20462"
tags: ["foundation-model", "contrastive", "multilabel"]
relevance: "high"
status: "downloaded"
pdf: "library/wang-2024-softcon.pdf"
in_slides: ["foundation-models"]
relates_to: []
---

## Obiettivo
Valutare strategie di adattamento di foundation model (DINOv2) a input multispettrale RS.

## Metodo
Random init dell'input embedding + fine-tuning con DINOv2. Benchmark su 11 task EO.

## Risultati
SOTA su 10/11 task EO. Random init + FT è 'both flexible and impressively effective'. Batte weight inflation.

## Riassunto
Conferma che con backbone ViT potenti (DINOv2), l'inizializzazione random dei canali extra è sufficiente. Non serve weight inflation.

## Cosa riutilizzare (tesi)
Evidenza per eliminare random init extra come strategia inferiore — in contrasto con i risultati EuroSAT. Da interpretare con cautela.

## Note Claude
### wang-2024-softcon

**Punti chiave**
- Soft contrastive learning multi-label: invece di binary positive/negative usa soft similarity da label vector cosine (Dynamic World land-cover come supervisione multi-label).
- Continual pretraining: inizializza da vision FM forte (DINOv2 per ViT, DINO per ResNet) + Siamese masking per memoria.
- Dataset costruito ad hoc: SSL4EO-S12-ML = 780k immagini SSL4EO-S12 matched con Dynamic World multi-label (9 classi land-cover).
- Backbone leggeri (ResNet50 ~25M, ViT-S/B ~22-86M) ma batte SOTA su 10/11 task downstream.
- Bande: tutte e 13 S2 (multispectral) + SAR (S1). Strategia per canali mismatched: random init del primo layer.

**Quale problema chiave risolve per la mia tesi**
SoftCon e principalmente un *metodo di training* riapplicabile. I checkpoint rilasciati sono S2-13band -> stesso vincolo di SSL4EO-S12 per il SuperDove. NON sensor-agnostico: serve mapping di bande. Punto di interesse: il paradigma "random-init first layer + DINOv2 backbone forte" e una baseline empiricamente molto solida per chi non ha tempo di pretrain ad hoc -> direttamente applicabile come strategia per adattare DINOv2 alle 8 bande SuperDove.

**Numeri forti da citare**
- ResNet50 ViT-S (~22M) raggiunge 84.8/85.0 linear probe mAP su BigEarthNet-10%, sopra ViT-L 300M (CROMA/SatMAE).
- ViT-B 86M nuovo SOTA: 86.8 multispectral, 82.5 SAR su BigEarthNet-10%.
- Vince 10/11 downstream task (BigEarthNet, EuroSAT, fMoW-sentinel, DFC2020, OSCD, GEO-Bench multispectral subset).
- Continual pretrain 100 epoche su 4x A100 -> molto efficiente.

**Limite onesto (gap che lasciano):**
Soft labels da Dynamic World sono noisy a pixel-level (auto-generated). Vincolato a S2 13-band: nessuna estensione esplicita a SuperDove/WV-3. La dipendenza da land-cover labels limita il transfer a domini molto diversi (es. material classification fine-grained dove le label LULC sono troppo grossolane).

**Cross-link**
Build on `wang-2023-ssl4eo-s12` (SSL4EO-S12 dataset). Compete con `xiong-2024-dofa` (DOFA flessibilita sensoriale > SoftCon su S2 only) ma SoftCon vince in efficienza param. Complementare con `cong-2022-satmae` (MAE vs contrastive). Citato in survey `fm-rs-survey-2024`.
