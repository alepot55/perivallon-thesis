---
id: "zhou-2021-plastic-classifier"
title: "A knowledge-based, validated classifier for the identification of aliphatic and aromatic plastics by WorldView-3 satellite data"
authors: ["Zhou", "Kuester", "Bochow", "Bohn", "Brell", "Kaufmann"]
year: 2021
venue: "Remote Sensing of Environment"
doi: "10.1016/j.rse.2021.112598"
arxiv: null
link: "https://doi.org/10.1016/j.rse.2021.112598"
tags: ["plastic", "hyperspectral", "classifier", "aliphatic-aromatic", "wv-3", "gfz"]
relevance: "high"
status: "downloaded"
pdf: "library/zhou-2021-plastic-classifier.pdf"
in_slides: ["high-res-survey"]
relates_to: []
---

## Obiettivo
Discriminare polimeri alifatici (PE, PP, PVC) da aromatici (PET, PS) usando le 8 bande SWIR di WorldView-3.

## Metodo
Classificatore knowledge-based basato sulle posizioni e profondità delle feature C-H a 1660/1730 nm nelle bande WV-3 SWIR. Validazione su target controllati.

## Risultati
Producer accuracy >80% per discriminazione aromatico vs alifatico. Definisce le frazioni minime rilevabili per ciascuna combinazione plastica-background.

## Riassunto
Paper chiave per il trade-off tra bande SWIR strette (WV-3) e bande larghe (S2 B11/B12). Spiega perché WV-3 risolve PE vs PET e S2 no.

## Cosa riutilizzare (tesi)
Riferimento per la sezione band coverage. Motiva la scelta di usare bande specifiche S2 (B11, B12) pur sapendo che sono meno selettive di WV-3 SWIR.

## Note Claude
**Punti chiave**
- Classificatore decision-tree **knowledge-based** (no training data, no statistical fitting) basato su feature spettrali diagnostiche delle 8 bande SWIR WV-3 (1195/1570/1660/1730/2165/2205/2260/2330 nm).
- Identifica **3 cluster** di plastica: (1) alifatici PE/PVC/EVAC/PP/POM/PMMA/PA, (2) aromatici PET/PS/PC/SAN, (3) aromatici PBAT/ABS/PU. Più cluster non-plastica.
- Validazione multi-layer: libreria JPL-ECOSTRESS + USGS + GFZ in-house → laboratorio → aereo → satellite WV-3 reale su Almeria/Cairo/Accra.
- Confronto con SAM e Maximum Likelihood Estimation (MLE): il knowledge-based vince in robustezza su scenari background variabili.
- Modello in-house **HySimCaR** (ray tracing 3D) simula variazione brightness/transparency/fraction/background per quantificare la robustezza.

**Figure/tabelle usabili in slide**
- Fig. spettri firme: posizioni assolute delle absorption feature C-H per ciascun gruppo polimerico — usabile per giustificare la scelta SWIR vs VNIR.
- Fig. flowchart decision-tree del classifier — utile per slide "approach" se proponessi un workflow ispirato.
- Mappe risultanti su Almeria (serre), Cairo, Accra — esempi visuali di "cosa il WV-3 SWIR cattura in scenario urbano reale".

**Numeri forti**
- 8 bande SWIR WV-3 strette (range ~1100–2400 nm, larghezza ~40–50 nm ciascuna)
- Discriminazione aliphatic vs aromatic con producer accuracy >80% su validation set
- Discriminazione di sub-cluster aromatici (PET vs PS vs ABS) basata su differenze di pochi % di riflettanza nelle bande 2.2–2.3 µm
- HySimCaR determina **frazioni minime di pixel** rilevabili per ogni polimero su ogni background (numeri specifici per slide #10)

**Limite onesto**
- Knowledge-based richiede **calibrazione fine** delle soglie per ogni nuovo sensore — se generalizzo da WV-3 SWIR a SuperDove (no SWIR), il metodo non si trasferisce direttamente.
- Validazione field-truth difficile per plastica reale ("temporal relocation, debris geometrically irregular"): autori ammettono che le confusion matrix sono solide su lab+airborne, ma su WV-3 reale si fidano della "reasonable appearance" delle mappe.
- Solo discriminazione **plastica**: per asbestos servono feature diverse (Mg-OH @2.31 µm) — modello concettualmente trasferibile ma threshold tutti da rifare.

**Cross-link**
- `aguilar-2025-macroplastics-wv3`: stesso sensore WV-3 SWIR, approccio matched-filter vs knowledge-based — Aguilar usa endmember spectra, Zhou usa decision tree su band ratios. Complementari.
- `guo-li-2020-ndpi-wv3`: NDPI è una singola spectral index, Zhou è un albero decisionale completo basato su molteplici feature. Zhou è l'evoluzione metodologica.
- `aguilar-2021-wv3-ablation`: stesso sensore, dimostra che SWIR contiene 96.79% del segnale predittivo (giustifica metodologicamente l'approccio Zhou).
- `kokaly-2017-splib07a`: USGS è una delle 3 librerie convolute al WV-3 spectral response in questo paper.
- `cdw-2025-critical-wavelengths`: tesi simile — pochi λ ben scelti bastano. Conferma Zhou's filosofia di band selection.
