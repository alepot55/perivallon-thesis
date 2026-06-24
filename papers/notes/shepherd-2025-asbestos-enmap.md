---
id: "shepherd-2025-asbestos-enmap"
title: "Detection of asbestos-based cement rooftops in conflict-affected settings using EnMAP hyperspectral data"
authors: ["Shepherd", "Sagi", "Zagron", "Aharoni-Mack", "et al."]
year: 2025
venue: "Scientific Reports"
doi: "10.1038/s41598-025-09738-w"
arxiv: null
link: "https://doi.org/10.1038/s41598-025-09738-w"
tags: ["asbestos", "enmap", "hyperspectral", "satellite", "sam", "low-res-survey"]
relevance: "critical"
status: "downloaded"
pdf: "library/shepherd-2025-asbestos-enmap.pdf"
in_slides: ["low-res-survey", "asbestos-anchor"]
relates_to: ["cilia-2015-ac-weathering", "bonifazi-2026-ac-python"]
---

## Obiettivo
Mappare tetti in asbesto-cemento in aree di conflitto (Israele post-2023) usando dati iperspettrali satellitari EnMAP a 30 m, con calibrazione field-spectra.

## Metodo
EnMAP Level 2A (230 bande, 30 m), MNF noise reduction, co-registrazione, cloud mask. Cascade di 8 classificatori supervisionati (LSU, SVM, SAM, ACE, Mahalanobis, ML, SID, MF) con filtering iterativo. Field calibration con ASD FieldSpec 4 High-Res.

## Risultati
86% positive-match rate vs ground truth esaustivo. Dimostra fattibilità di mappatura asbestos orbitale a scala in contesti high-risk.

## Riassunto
Paper Sci Rep (Nature OA) sul rilevamento asbestos da satellite iperspettrale EnMAP. Costruisce libreria spettrale field-collected, applica cascata multi-classificatore, validazione esaustiva on-ground. Il riferimento più diretto per la giustificazione satellite-vs-aereo del pilot Fase 1 amianto.

## Cosa riutilizzare (tesi)
Metodologia di field-spectra calibration; cascade di 8 classificatori come comparator; struttura della validazione 86% match; argomento per VPN/SWIR satellite vs RGB.

## Note Claude

**Punti chiave**
- Pipeline end-to-end EnMAP iperspettrale (230 bande, 30 m) per tetti AC in zona conflitto (Western Negev, post-7 ottobre 2023). Campagna field 4 mesi con ASD FieldSpec 4 + SoilPro® per libreria spettrale disturbance-free di 2714 spettri (1213 in situ + 1501 EnMAP).
- Cascata di 8 classificatori supervisionati (LSU, SVM, SAM, ACE, Mahalanobis, MLC, SID, MF) con consensus rule "6-of-8" + human-in-the-loop verification. ACE singolo arriva a 91.4% accuracy, k=0.87.
- Ground-truth blind in 10 villaggi + 2 città (May–Aug 2024) su 823 detection candidate; rural Kibbutzim >92% match grazie a tetti omogenei, urban dense soffre mixed-pixel da rubble e paint-sealing.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 1: Sentinel-2 + zoom UAV mostra distruzione rocket-fire — anchor visivo conflict setting.
- Fig. 2: GT vs EnMAP overlay su UAV — verde=positive EnMAP, rosso=struttura reale; eccellente per slide low-res asbestos.
- Fig. 3: spettri "confirmed asbestos" vs grey-paint-sealed vs bare soil su EnMAP 500–2500 nm — mostra discriminabilità.
- Fig. 4: heatmap density classified AC roofs su county boundaries Western Negev.
- Tab. 1: accuracy 7 classifiers (OA, Precision, Recall, F1, k).

**Numeri forti** (metriche concrete: OA, F1, # bande, GSD)
- 86% positive match rate vs GT esaustivo. ACE 91.4% OA / k=0.87 / F1=91.2; SID 90.1% / k=0.85; SVM 89.2% / k=0.83; LSU 84.5% (worst, mixed-pixel). 230 bande EnMAP, 30 m GSD, MNF first 15 components >99% varianza, co-registration RMSE<0.3 px. 2714 spettri field, 823 detection finali da 2300 candidati iniziali.

**Limite onesto** (terminologia: "generalizzazione" non "OOD", "classificare per rischio" non "rilevare")
- 30 m GSD impone mixed-pixel errors in urban denso (rubble + paint mimano asbestos). Generalizzazione climatica limitata: pipeline calibrata in semi-arid Negev — climi temperati/umidi richiedono librerie locali per lichen/moss/canopy. Pesante human-in-the-loop curation (spectrum-by-spectrum) — automazione DL indicata come future work. "Classificare per rischio" (intact vs partially destroyed vs burned) supportato dal field log.

**Cross-link**
- `cilia-2015-ac-weathering`: precursore aereo MIVIS per AC italiano; Shepherd alza la sfida a satellite + cascata 8-vs-1 classifier.
- `bonifazi-2026-ac-python`: confronto diretto satellite high-res (WV-3 1.24m, MLC singolo) vs satellite low-res hyperspectral (EnMAP 30m, ensemble 8) — due strategie complementari per stesso target.
- `aguilar-2021-wv3-ablation`: SWIR e SAM/MF condivisi; Shepherd estende a 230 bande iperspettrali con consensus ensemble.
- `kokaly-2017-splib07a`: libreria USGS è il complemento "lab" della libreria field-collected qui costruita.
