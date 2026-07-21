---
id: "gibellini-2025-pipeline"
title: "A deep learning pipeline for solid waste detection in remote sensing images"
authors: ["Gibellini", "Torres", "Fraternali"]
year: 2025
venue: "Waste Management Bulletin"
doi: "10.1016/j.wmb.2025.100246"
arxiv: "2502.06607"
link: "arXiv:2502.06607"
tags: ["waste", "baseline", "swin-t", "rsp", "aerialwaste"]
relevance: "critical"
status: "downloaded"
pdf: "library/gibellini-2025-pipeline.pdf"
in_slides: ["baseline", "approach"]
relates_to: []
---

## Obiettivo
Costruire una pipeline DL end-to-end per la detection binaria (waste/no-waste) da immagini RS ad alta risoluzione.

## Metodo
Swin-T con Remote Sensing Pretraining (RSP). Training two-step: TL (backbone frozen) poi FT (ultimo stage). AerialWaste v3, GSD 20 cm/px.

## Risultati
92.02% F1, 94.56% accuracy. +63% discovery rate, -12% tempo analisi vs ispezione manuale. RSP batte ImageNet di ~2.3pp F1.

## Riassunto
Pipeline baseline RGB-only per waste detection su AerialWaste. Il modello migliore è Swin-T RSP a 20 cm GSD. Dimostra che il RS pretraining è superiore a ImageNet per immagini aeree.

## Cosa riutilizzare (tesi)
Architettura (Swin-T + RSP), strategia two-step training, AerialWaste v3 come dataset. È la baseline da estendere al multispettrale.

## Note Claude
### gibellini-2025-pipeline
**Punti chiave** (3-5 bullet):
- Pipeline end-to-end (tile → binary classifier → Grad-CAM saliency → GIS) co-progettata con ARPA Lombardia per scanning territoriale semi-automatico.
- Esperimento factorial 36-condizioni: 2 architetture (ResNet-50 vs Swin-T) x 3 GSD (20/30/50 cm) x 3 context size (100/150/210 m) x 2 pretraining (ImageNet vs RSP/Million-AID).
- Best model = Swin-T + RSP + GSD 20 cm + context 100 m (F1 92.02%, Acc 94.56%); Swin-T sempre > ResNet-50 a parita di setup.
- Generalizzazione testata su Grecia/Svezia/Romania: F1 medio 86.92% (-5.10pp vs Lombardia) - dimostra trasferibilita cross-country accettabile.
- Utility study con 4 operatori ARPA: AI-supported trova +63.2% siti, riduce area ispezionata -60.2%, tempo per sito -12.2%, tempo complessivo -30% a threshold 0.7.

**Figure/tabelle usabili in slide**:
- Fig. 1: Pipeline overview (tile → classifier → saliency → GIS) - canonica per slide intro
- Fig. 2: TP/TN samples con saliency Grad-CAM overlay - molto efficace visivamente
- Fig. 3: Effect context size (100/150/210 m) e GSD (20/30/50 cm) sulla stessa scena
- Tab. 2: matrice 36 esperimenti con F1/Precision/Recall/Acc per RSP e INP
- Fig. 4: F1 vs GSD/context per pretraining - mostra robustezza Swin-T
- Tab. 3 + Fig. 5/6/7: generalization study (TP/FP/FN/TN per Grecia/Svezia/Romania)
- Tab. 4: utility evaluation con numeri operativi ARPA

**Numeri forti da citare**:
- F1 92.02%, Accuracy 94.56% (Swin-T+RSP, 20 cm, context 100 m)
- Swin-T 27M params vs ResNet-50 23M; batch 120; LR TL=0.001, FT=0.0001
- Generalizzazione: Grecia 85.45% F1, Svezia 83.82%, Romania 91.48%
- Utility: -60.2% area ispezionata, +63.2% siti detected (155 vs 95), -12.2% tempo/sito, -30% tempo complessivo a threshold 0.7
- Inference su 100 km^2 trascurabile su RTX 2080 Ti 12GB

**Limite onesto (gap che lasciano):**
- RGB-only su tile a 20 cm: nessun valore aggiunto spettrale, non distingue materiali. La generalizzazione si limita a contesti visivamente simili (paesaggi agricoli/urbani europei) - rimane aperto se modelli RGB possano "classificare per rischio" senza informazione MS/SWIR.
- RSP da Million-AID porta solo +modesto vs ImageNet perche GSD del pretraining (0.5-153 m) non matcha GSD del task (20-50 cm).

**Cross-link**: cita Torres ([14]=torres-2023-aerialwaste come dataset, [12]=torres-2021), Sun et al. [25] (= global-dumpsites-2023), Kruse et al. [15] (S2 plastic). Da survey fraternali-2024-survey come gap intro. E baseline per qualsiasi estensione MS (DOFA, SSL4EO, SatMAE).
