---
id: "guo-li-2020-ndpi-wv3"
title: "Mapping plastic materials in an urban area: Development of the normalized difference plastic index using WorldView-3 superspectral data"
authors: ["Guo", "Li"]
year: 2020
venue: "ISPRS J. Photogr. & Remote Sensing"
doi: "10.1016/j.isprsjprs.2020.09.009"
arxiv: null
link: "https://doi.org/10.1016/j.isprsjprs.2020.09.009"
tags: ["wv-3", "swir", "plastic", "spectral-index", "urban", "ndpi"]
relevance: "high"
status: "vpn-required"
pdf: null
in_slides: ["high-res-survey"]
relates_to: ["aguilar-2025-macroplastics-wv3", "zhou-2021-plastic-classifier"]
---

## Obiettivo
Creare un indice spettrale specifico per quantificare la plastica urbana da satellite.

## Metodo
Indice NDPI basato su rapporto di bande SWIR di WorldView-3. Validazione su aree urbane.

## Risultati
NDPI supera indici esistenti per la quantificazione di plastica urbana. Le bande SWIR sono sufficienti senza iperspettrale.

## Riassunto
Dimostra che indici spettrali semplici basati su SWIR possono quantificare la plastica. Non serve iperspettrale.

## Cosa riutilizzare (tesi)
Concetto di spectral index per plastica. Se si usano bande SWIR, l'NDPI è un feature engineering utile.

## Note Claude

**Status: PDF non disponibile** (Elsevier closed access, da scaricare via VPN PoliMi → https://doi.org/10.1016/j.isprsjprs.2020.09.009).

Da letteratura secondaria (citato in `aguilar-2021-wv3-ablation`, `aguilar-2025-macroplastics-wv3`, `zhou-2021-plastic-classifier`):

**Punti chiave (preliminari, da verificare a lettura)**
- Definisce il **Normalized Difference Plastic Index (NDPI)** come `(B7 - B8) / (B7 + B8)` su bande SWIR strette di WorldView-3 (~1.57 e 1.73 µm — assorbimenti C-H di idrocarburi).
- Applicazione a area urbana per mappare materiali plastici. Caso studio Cina.
- Riferimento canonico per spectral index plastica su WV-3, citato da praticamente tutti i lavori successivi su plastica VHR.

**Cross-link**
- `aguilar-2021-wv3-ablation`: identifica NDPI come la feature singola più predittiva nell'ablation studio (96.79% OA solo SWIR domina grazie a NDPI).
- `aguilar-2025-macroplastics-wv3`: cita Guo & Li come precedente teorico, ne estende l'uso da urbano a riparian-watershed.
- `zhou-2021-plastic-classifier`: NDPI è un'index scalare, Zhou estende a classifier decision-tree su molteplici feature C-H per discriminare polimeri specifici.
- **Da rileggere** appena scaricato il PDF corretto via VPN.
