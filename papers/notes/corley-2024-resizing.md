---
id: "corley-2024-resizing"
title: "Revisiting pre-trained remote sensing model benchmarks: resizing and normalization matters"
authors: ["Corley", "et al."]
year: 2024
venue: "arXiv"
doi: null
arxiv: "2305.13456"
link: "arXiv:2305.13456"
tags: ["foundation-model", "benchmark", "normalization"]
relevance: "high"
status: "downloaded"
pdf: "library/corley-2024-resizing.pdf"
in_slides: []
relates_to: []
---

## Obiettivo
Verificare se i vantaggi riportati del RS pretraining sono reali o artefatti di preprocessing inconsistente.

## Metodo
Benchmark sistematico con preprocessing standardizzato (resize 224x224, normalizzazione dataset-specific). ViT + DINOv2 con random init dell'embedding.

## Risultati
ImageNet pretraining resta competitivo se il preprocessing è corretto. Random init dei canali extra su ViT converge bene. Resize a 224 migliora il transfer.

## Riassunto
Smonta alcune claim sul RS pretraining mostrando che il preprocessing conta più dell'origine dei pesi. Random init extra channels funziona sorprendentemente bene con backbone ViT.

## Cosa riutilizzare (tesi)
Procedura di preprocessing (resize, normalizzazione per-banda). Evidenza che random init extra channels è viable con ViT. Best practice per confronti equi.

## Note Claude

**Punti chiave**
- Corley, Robinson, Dodhia, Lavista-Ferres, Najafirad (UTSA + Microsoft AI for Good, arXiv 2305.13456, maggio 2023): mostrano che il preprocessing (resize + normalizzazione) ha effetti enormi sui benchmark di pretrained models in remote sensing, spesso piu' grandi della scelta del pretraining stesso.
- Setup sistematico: 7 dataset RS (EuroSAT, SAT-6, So2Sat, BigEarthNet, TreeSatAI, UC Merced, RESISC45) x 6 metodi di feature extraction (ResNet-50 con pesi ImageNet/MoCo/SeCo/Random + RCF + Image Statistics) valutati con KNN su embeddings.
- Risultato chiave: resize delle immagini RS alla dimensione di pretraining (224x224, contro nativi 32x32 o 64x64) + normalizzazione channel-wise consistente con il pretraining = +11.16% accuracy su EuroSAT, +32.28% su So2Sat MSI. ImageNet rimane competitivo, batte spesso SSL specifici per RS se misurato correttamente.
- Best practice raccomandate: (1) usa baseline semplici (ImageNet, RCF, image statistics); (2) resize+normalize coerenti con il pretraining; (3) preferisci KNN o linear probe a fine-tuning per misurare quality dei feature; (4) MOSAIKS/RCF e' una baseline sorprendentemente forte per multispettrale.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 1: bar chart con delta di accuracy/mAP solo per il resize a 224 - 18 barre tutte positive, da +1.65% a +32.28%. Visual perfetto per "preprocessing matters".
- Fig. 2: curva accuracy vs image size (32->256) per 7 varianti di ResNet-50 su EuroSAT. Mostra saturazione intorno a 224x224.
- Fig. 3: t-SNE EuroSAT embeddings con e senza normalizzazione: clusters di classi emergono solo con resize+normalizzazione corretti.
- Tab. 1, 3, 6: confronti finali per EuroSAT, So2Sat, RESISC45 contro Scale-MAE, SatMAE, ConvMAE - dove ImageNet correttamente preprocessato ottiene 90.7% OA su RESISC45 vs 85.0% di Scale-MAE.

**Numeri forti** (metriche concrete, # bande, GSD)
- Boost da resize 64->224: ImageNet RGB EuroSAT 82.09 -> 91.17 (+9.08); MoCo SSL4EO MSI So2Sat 49.36 -> 53.54.
- ImageNet ResNet-50 RGB su SAT-6 a 224: 99.89 OA, dimostra che il dataset e' saturo.
- ImageNet su EuroSAT a 224 con linear probe: 93.13% vs SeCo SSL 96.30% - margine molto piu' piccolo di quanto i paper SSL claim.
- RCF/MOSAIKS: top-2 in 4 su 5 dataset multispettrali, batte spesso SSL pretrained.

**Limite onesto** (gap del paper — usa "generalizzazione" non "OOD")
- Tutti i benchmark sono RGB o "MSI all bands" con padding/zero-pad per i canali extra: non testano realmente la generalizzazione a sensori con configurazioni di bande diverse dal pretraining (es. PlanetScope 8-band vs Sentinel-2 13-band). Linear probing puo' sovrastimare la rappresentazione e fine-tuning tende a sottostimare la trasferibilita' su task out-of-distribution. KNN valutato a k=5 fisso. Non considerano effetti di GSD-shift (cambiare GSD durante test e' tema in altri paper come Scale-MAE).

**Cross-link**
- `aguilar-2021-wv3-ablation`: nella nostra pipeline waste, evidenza che la scelta del preprocessing (resize, normalization per-banda) deve essere coerente quando si confrontano backbone con e senza SWIR.
- `wang-2023-ssl4eo-s12` e `wang-2024-softcon`: questo paper smonta parzialmente le claim di SSL4EO/SoftCon mostrando che ImageNet ben preprocessato e' molto vicino.
- `xiong-2024-dofa` e `anysat-2024`: i FM "any-sensor" devono essere valutati con questo stesso rigore - se non lo sono, l'apparente vantaggio puo' sparire.
- `szwarcman-2024-prithvi-eo2` e `spectralgpt-2024`: stesso caveat - vanno benchmarkati con linear probe + resize+normalize controllati.
- `cong-2022-satmae`: SatMAE risulta superato da semplice ImageNet+resize in piu' setup, motivazione forte per non assumere a priori che FM RS = migliore.

