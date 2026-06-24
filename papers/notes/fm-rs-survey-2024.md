---
id: "fm-rs-survey-2024"
title: "Foundation Models for Remote Sensing and Earth Observation: A Survey"
authors: ["(unknown)"]
year: 2024
venue: "arXiv"
doi: null
arxiv: "2410.16602"
link: "arXiv:2410.16602"
tags: ["foundation-model", "survey", "earth-observation"]
relevance: "high"
status: "downloaded"
pdf: "library/fm-rs-survey-2024.pdf"
in_slides: ["foundation-models"]
relates_to: []
---

## Obiettivo
Panoramica completa dei foundation model per RS/EO, tassonomia e confronto.

## Metodo
Literature review. Tassonomia per architettura (ViT, Swin, CNN), pretraining (MAE, contrastive, generative), e dominio.

## Risultati
Mappa 30+ foundation model RS. Identifica trend: scaling, multi-modal, multi-temporal. Gap: evaluation inconsistente.

## Riassunto
Survey completa dei FM per EO. Utile per posizionare la scelta di backbone (SSL4EO, DOFA, Prithvi) nel contesto del campo.

## Cosa riutilizzare (tesi)
Background per la sezione related work della tesi. Tassonomia per giustificare le scelte architetturali.

## Note Claude
### fm-rs-survey-2024

**Punti chiave**
- Survey IEEE GRSM 2025 (Xiao, Xuan, Wang, Huang, Tao, Lu, Yokoya - RIKEN+Tokyo+NTU).
- Tassonomia 3 famiglie: VFMs (visual), VLMs (vision-language), LLMs/altri (generative, weather FMs).
- Pretrain datasets tabulati (Tab II): FMoW-RGB 363k, BigEarthNet 1.2M, SeCo 1M, fMoW-Sentinel 882k, MillionAID 1M, GeoPile 600k, SSL4EO-S12 3M, SatlasPretrain 856k, MMEarth 1.2M, HyperGlobal-450K, Hyper-Seg 41.9k.
- Tab III lista 18+ VFMs con tag SSL-M/SSL-C/Sup/SSL-C&M.
- Discute PEFT (LoRA-like) come essenziale in RS per limiti GPU.

**Quale problema chiave risolve per la mia tesi**
Reference review per la sezione Related Work della tesi sui FM. Permette di posizionare DOFA/AnySat come ultime evoluzioni (any-modality), citare survey-of-surveys per coverage, e mostrare il trend storico SatMAE -> SpectralGPT -> DOFA -> AnySat. Utile anche per identificare 2 dataset HSI pretrain (HyperGlobal-450K, Hyper-Seg) se in futuro lo studio si estende a HSI EnMAP/PRISMA.

**Numeri forti da citare**
- 1200+ paper "FM + RS" su Google Scholar al 2024 (crescita esponenziale, Fig 1).
- 11 dataset pretrain principali tabulati con GSD da 0.1m a 153m.
- 18+ VFMs RS tabulati con architettura/pretrain strategy.
- Pubblicato IEEE GRSM 2025 (high-impact venue settore).

**Limite onesto (gap che lasciano):**
Survey di taxonomy, poco quantitativo (no benchmark unico). Coverage temporale ferma al Q3 2024 (manca AnySat dicembre, Prithvi-EO-2.0 dicembre, alcuni DEFLECT-like). Non analizza problema specifico SuperDove / 8-band sensors. Generico, non orienta tra DOFA vs AnySat per un task material classification.

**Cross-link**
Cita praticamente tutti gli altri della Cluster E. Contesto unificante per `xiong-2024-dofa`, `szwarcman-2024-prithvi-eo2`, `wang-2023-ssl4eo-s12`, `wang-2024-softcon`, `cong-2022-satmae`, `spectralgpt-2024`, `anysat-2024`. Complementare a `fraternali-2024-survey` (survey waste-specific) e `corley-2024-resizing` (paper metodologico su benchmark FM).
