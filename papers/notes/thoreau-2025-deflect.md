---
id: "thoreau-2025-deflect"
title: "DEFLECT: Parameter-Efficient Adaptation of Geospatial Foundation Models through Embedding Deflection"
authors: ["Thoreau", "Marsocci", "Derksen"]
year: 2025
venue: "ICCV 2025"
doi: null
arxiv: "2503.09493"
link: "arXiv:2503.09493"
tags: ["vit", "parameter-efficient", "multispectral-adapter", "geospatial-fm", "peft"]
relevance: "medium"
status: "downloaded"
pdf: "library/thoreau-2025-deflect.pdf"
in_slides: []
relates_to: ["xiong-2024-dofa", "szwarcman-2024-prithvi-eo2"]
---

## Obiettivo
Estendere il patch embedding di ViT a nuovi canali con meno dell'1% di parametri aggiuntivi.

## Metodo
Low-rank adapters sul patch embedding. Freeze del backbone, addestra solo gli adapter.

## Risultati
Performance comparabile al full fine-tuning con <1% parametri extra.

## Riassunto
PEFT applicato al problema dell'adattamento canali. Utile se le GPU sono limitate.

## Cosa riutilizzare (tesi)
Alternativa a weight inflation/random init se serve efficienza parametrica. Da considerare se i costi computazionali diventano un problema.

## Note Claude
### thoreau-2025-deflect

**Punti chiave**
- PEFT (parameter-efficient fine-tuning) per adattare GFM pretrained su RGB a immagini multispettrali con <1% parametri extra.
- 3 elementi: (a) UPE = Untangled Patch Embedding (decompone embedding in x_P RGB-geom + x_A spettrale-radiometrico, x_A via pixel-set encoding NDVI/NDTI-like + statistics); (b) uAtt = Untangled Attention (sub-attention blocks rebrandised per gestire spectral); (c) Embedding Deflection (vincola norma del displacement per preservare struttura latente).
- Testato su 3 GFM (Scale-MAE, DINO-MC, Cross-Scale MAE) e 5 dataset (So2Sat 10 bande, Brick Kiln 13, ForestNet 12, BurnScars 6, MADOS 13).
- Compete con LoRA, BitFit, SLR, NormTuning con 5-10x meno parametri.

**Quale problema chiave risolve per la mia tesi**
Modulo "ortogonale" che si applica SOPRA qualsiasi GFM ViT-based (DOFA, Prithvi, Scale-MAE) per adattarlo a nuovi canali con basso costo. NON e un FM standalone: e un adapter. Se DOFA risolvesse mediocremente su SuperDove ma volessi probing+lightweight fine-tune, DEFLECT e la strategia. Vantaggio: <1% params, addestramento veloce. Plug-and-play sopra qualsiasi ViT pretrained.

**Numeri forti da citare**
- Performance on-par o superiore vs full fine-tune (oracle) con 5-10x meno parametri.
- Testato su 3 GFM x 5 dataset = 15 combinazioni.
- ICCV 2025.
- Su MADOS (marine pollution) DEFLECT batte gli altri PEFT in modo significativo.

**Limite onesto (gap che lasciano):**
Dipende dalla qualita del GFM RGB di partenza: se DOFA ViT-L gia copre multispectral nativamente, DEFLECT aggiunge poco. Pixel-set encoding richiede definizione esplicita di indici spettrali (NDVI, NDTI) -> per bande SuperDove servirebbero indici task-specific. Non testato su SuperDove o sensori a 8 bande VNIR. Vincoli di norma sul deflection sono ad hoc (hard constraint).

**Cross-link**
Complementare a tutti i GFM `xiong-2024-dofa`, `szwarcman-2024-prithvi-eo2`, `cong-2022-satmae` (puo essere applicato sopra). Compete con LoRA-like in `wang-2024-softcon` (random-init first layer). Diversa filosofia da `anysat-2024` (AnySat = pretrain multimodale; DEFLECT = adapter post-hoc su backbone RGB). Citato non in INDEX ma cluster `parameter-efficient/adapter`.
