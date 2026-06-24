---
id: "spectralgpt-2024"
title: "SpectralGPT: Spectral Remote Sensing Foundation Model"
authors: ["Hong", "et al."]
year: 2024
venue: "TPAMI"
doi: null
arxiv: "2311.07113"
link: "arXiv:2311.07113"
tags: ["foundation-model", "spectral", "transformer"]
relevance: "high"
status: "downloaded"
pdf: "library/spectralgpt-2024.pdf"
in_slides: ["foundation-models"]
relates_to: []
---

## Obiettivo
Creare un foundation model specifico per dati spettrali con architettura 3D transformer.

## Metodo
3D Generative Pre-trained Transformer (600M+ parametri). Multi-target spectral reconstruction su Sentinel-2.

## Risultati
Cattura esplicitamente il coupling spaziale-spettrale. Performance competitive su task spettrali.

## Riassunto
Foundation model purpose-built per dati spettrali. Il 3D transformer cattura relazioni spaziali-spettrali che ViT 2D perde.

## Cosa riutilizzare (tesi)
Alternativa avanzata se il focus diventa l'analisi spettrale fine. Più complesso di SSL4EO/DOFA.

## Note Claude
### spectralgpt-2024

**Punti chiave**
- Foundation model "purpose-built per dati spettrali" (TPAMI 2024). 3 size: Base 100M, Large 300M, Huge 600M.
- Innovazione chiave: 3D masking spettrale (cubi 8x8x3 spazio-spettro), masking ratio 90%, multi-target reconstruction (token-to-token + spectral-to-spectral).
- ViT-Base backbone con conv3D patch embedding. Spatial + spectral positional encodings appresi.
- Pretrain progressive: fMoW-Sentinel-2 (712k img, 12 bande S2 droppando B10) -> BigEarthNet-S2 (354k, 12 bande). Totale 1.07M.
- SpectralGPT+ = continual pretrain BigEarthNet sopra SpectralGPT base.

**Quale problema chiave risolve per la mia tesi**
NON SuperDove-ready nativamente: vincolato a 12 bande Sentinel-2 specifiche. Filosofia opposta a DOFA: invece di flessibilita sensoriale punta su modeling 3D spazio-spettrale ricco. Per SuperDove servirebbe ridefinire patch 3D (8x8x8 invece di 8x8x3 per le 8 bande) e re-pretrain. Vantaggio teorico: se il modello cattura davvero spectral coupling, transfer su materiali e potenzialmente forte. Pero non c'e evidenza di material classification nel paper.

**Numeri forti da citare**
- 600M parametri (variante Huge).
- 1.47M sample pretrain (fMoW+BigEarthNet) - meno di DOFA (8M) ma molto spettrale-mirato.
- Masking ratio 90% (estremo, vs MAE classico 75%).
- 12 bande S2 (drop B10 cirrus).

**Limite onesto (gap che lasciano):**
Vincolo S2 12-band: per altro sensore serve re-pretrain. 3D masking specifico per cubi spettrali coerenti (problemi su sensori con # bande non multipli di 3 -> SuperDove 8 bande richiede ridisegno). Nessun test su HSI EnMAP/PRISMA nel paper (limite per generalizzazione spettrale). Test downstream solo land-cover (no material classification).

**Cross-link**
Diretto vs `cong-2022-satmae` (SatMAE = 2D grouping, SpectralGPT = 3D cube). Compete su Sentinel-2 con `szwarcman-2024-prithvi-eo2` e `wang-2023-ssl4eo-s12`. Diversa filosofia da `xiong-2024-dofa` (DOFA flessibile sensori, SpectralGPT deep su spettro S2). Citato in `fm-rs-survey-2024` Tab III come SSL-M generative.
