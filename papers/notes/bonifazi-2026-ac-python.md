---
id: "bonifazi-2026-ac-python"
title: "A Python-Based Workflow for Asbestos Roof Mapping and Temporal Monitoring Using Satellite Imagery"
authors: ["Bonifazi", "Aurigemma", "Salas-Cáceres", "Lorenzo-Navarro", "Serranti", "Paglietti", "Bellagamba", "Malinconico"]
year: 2026
venue: "Geomatics"
doi: "10.3390/geomatics6030041"
arxiv: null
link: "https://doi.org/10.3390/geomatics6030041"
tags: ["asbestos", "wv-3", "vnir", "swir", "python", "open-source", "multi-temporal", "italian"]
relevance: "critical"
status: "downloaded"
pdf: "library/bonifazi-2026-ac-python.pdf"
in_slides: ["asbestos-anchor", "high-res-survey"]
relates_to: ["cilia-2015-ac-weathering", "aguilar-2021-wv3-ablation"]
---

## Obiettivo
Sviluppare un workflow Python end-to-end completamente open-source per detection e monitoring temporale di tetti asbesto-cemento da WV-3 multispettrale.

## Metodo
WorldView-3 VNIR (8 bande) + SWIR (8 bande), acquisizioni 2023+2024 su Mantova. Pipeline: atmospheric correction (Py6S), supervised pixel classification (Maximum Likelihood Classifier su classi roof empiriche), post-processing, building-level aggregation con adaptive thresholding. Confronto multi-temporale per detection di rimozioni.

## Risultati
Classificazione affidabile a livello edificio; comparazione multi-temporale identifica rimozioni. Precision/recall/F1 dipendenti dal threshold di aggregazione building-level.

## Riassunto
Bonifazi et al. 2026 (CNR-ISP + ENEA + Sapienza). Geomatics 6(3):41 MDPI OA. Workflow Python totalmente aperto e replicabile su WV-3 multispettrale per asbestos. Caso d'uso Mantova (Italia). Riferimento recentissimo + open-source = direttamente confrontabile con tuo lavoro.

## Cosa riutilizzare (tesi)
Stack tecnico Python (Py6S, MLC, rasterio); idea di multi-temporal monitoring; building-level aggregation con threshold; come strutturare repository reproducibile.

## Note Claude

**Punti chiave**
- Workflow Python end-to-end completamente open-source per AC roof mapping + multi-temporal monitoring da WV-3 (VNIR 8 bande @1.24 m + SWIR 8 bande @3.70 m → resampled @1 m, totale 16 bande). Stack: Py6S, rasterio 1.4.3, NumPy 2.2.6, GeoPandas 1.1.0, SciPy 1.15.3, scikit-learn 1.6.1, scikit-image 0.25.2. Test su Mantova (Italia), 2 acquisizioni (Agosto 2023, Luglio 2024).
- Classificazione pixel-based con Maximum Likelihood Classifier (MLC) su 9 classi empiriche (water, asbestos-cement, industrial, beige, white, brown1, brown2, dark, water), train 15 AC + 35 non-AC, validation 66+66. Aggregazione building-level via adaptive threshold (testati 0–50%) — sweet-spot a 20–30%.
- Multi-temporal: stesso training riapplicato a 2024 per detection di rimozioni. Cross-check con registri ufficiali ATS Valpadana — 47 di 80 rimossi correttamente identificati come AC nel 2023 e 31 di questi non più nel 2024.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 2: workflow scheme 5 stage (data acquisition → preprocessing → supervised classification → post → accuracy) — diagramma riusabile per slide pipeline tesi.
- Fig. 3: confusion matrix a 20% vs 30% threshold (recall 0.97 vs 0.92, precision 0.78 vs 0.81) — illustra trade-off.
- Fig. 4: classificazione 2023 su zona industriale Mantova (poligoni blu) — esempio operativo.
- Fig. 5: temporal consistency — stessa zona 2023 vs 2024, tetti rimossi (magenta border) correttamente "scomparsi" nel post-rimedio.
- Tab. 1: 16 central wavelengths WV-3 + Esun — utile per qualsiasi pipeline WV-3.
- Tab. 3: precision/recall/F1 vs threshold 0%–50%.

**Numeri forti** (metriche concrete: OA, F1, # bande, GSD)
- F1=0.87 a threshold 30% (precision 0.81, recall 0.92), F1=0.86 a 20% (precision 0.78, recall 0.97). 16 bande WV-3 VNIR+SWIR, GSD 1.24 m VNIR / 3.70 m SWIR. 25319 edifici processati, 2286 AC-positive a 20%, 1554 a 30%. 7.08 s su 4.7 M pixel (~1.5 μs/pixel, ~1.4 ms/tetto). Temporal: 2023 F1=0.87 (1554 edifici AC) → 2024 F1=0.79 (966 AC), -37% buildings, 46.6% delle 133 rimozioni ATS correttamente identificate.

**Limite onesto** (terminologia: "generalizzazione" non "OOD", "classificare per rischio" non "rilevare")
- Workflow di **screening**, non evidence: presenza di FP+FN — gli autori esplicitamente affermano che output deve essere gestito da autorità competenti e verificato sul campo (no enforcement legale diretto). Generalizzazione: Mantova-specific — threshold 20–30% va ricalibrato su altri contesti urbani. Training fisso 2023 riapplicato a 2024 introduce mismatch (alcuni AC training erano già stati rimossi). Building polygon geometry può aggregare tetti adiacenti diluendo classificazione. "Classificare per rischio" coerente con framing della tesi.

**Cross-link**
- `aguilar-2021-wv3-ablation`: stesso sensore WV-3 + stessa rilevanza SWIR (NDPI/PMLI indices per plastica) — Aguilar è il canon di "spectral added value" che Bonifazi sfrutta implicitamente.
- `cilia-2015-ac-weathering`: predecessore aereo MIVIS, stesso problema italiano asbestos; Bonifazi è la "moderna risposta satellite open-source".
- `shepherd-2025-asbestos-enmap`: complementare low-res hyperspectral (EnMAP 30 m + 8 classifier ensemble) vs high-res multispectral open-source (WV-3 1 m + MLC singolo).
- `guo-li-2020-ndpi-wv3`: NDPI originale è la blueprint del feature engineering su SWIR WV-3 che Bonifazi adatta.
