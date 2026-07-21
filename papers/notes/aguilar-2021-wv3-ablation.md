---
id: "aguilar-2021-wv3-ablation"
title: "Evaluation of Object-Based Greenhouse Mapping Using WorldView-3 VNIR and SWIR Data"
authors: ["Aguilar", "Jiménez-Lao", "Aguilar"]
year: 2021
venue: "Remote Sensing"
doi: "10.3390/rs13112133"
arxiv: null
link: "https://doi.org/10.3390/rs13112133"
tags: ["wv-3", "vnir", "swir", "ablation", "obia", "ndpi", "methodology-canonical"]
relevance: "critical"
status: "downloaded"
pdf: "library/aguilar-2021-wv3-ablation.pdf"
in_slides: ["approach", "high-res-survey"]
relates_to: ["ndpi-2020-wv3", "aguilar-2025-macroplastics-wv3"]
---

## Obiettivo
Investigare il potere predittivo separato di bande WV-3 VNIR vs SWIR vs combinate (All Features) per la mappatura di serre coperte di plastica con approccio OBIA.

## Metodo
WV-3 bundle (PAN+VNIR+SWIR), object-based image analysis (OBIA). 3 strategie: (i) feature solo da bande VNIR, (ii) solo da SWIR, (iii) tutte. Studio caso Almería (Spagna), serre PCG.

## Risultati
OA = 90.85% (VNIR only) / 96.79% (SWIR only) / 97.38% (All Features). SWIR domina, in particolare NDPI (Normalized Difference Plastic Index). Misclassification principale = whitewash stagionale che maschera spettro plastica.

## Riassunto
Aguilar, Jiménez-Lao, Aguilar (Univ. Almería). Remote Sensing 13(11):2133 MDPI OA. Materia=plastica (serre) NON asbestos, ma metodologia di ablation VNIR vs SWIR vs All è il riferimento canonico per 'valore aggiunto MS vs RGB'. Direttamente trasferibile al framing della tesi.

## Cosa riutilizzare (tesi)
Schema ablation 3-via VNIR/SWIR/All come benchmark metodologico; numeri concreti 90.85/96.79/97.38 da citare nelle slide come 'spectral added value'; argomento OBIA vs pixel-based.

## Note Claude
**Punti chiave**
- Riferimento canonico per ablation VNIR vs SWIR vs All-Features su WV-3 (PAN 0.31 m + 8 VNIR 1.24 m + 8 SWIR 3.70 m). Studio caso Almería (Spagna), serre plastic-covered (PCG) su area 20.65 km² con >70% PCG coverage. Approccio OBIA + Decision Tree con segmentazione MRS (eCognition) + AssesSeg ED2=0.313 sui 3188 segmenti.
- 3 strategie testate con 1175 GH + 1175 Non-GH balanced sample, 10-fold CV: (i) solo VNIR (20 features), (ii) solo SWIR (19 features), (iii) All Features (39 features). Pixel-based accuracy su 14.3 M pixel di GT.
- SWIR domina largamente — NDPI (Normalized Difference Plastic Index) ((SWIR10−SWIR12)+(SWIR13−SWIR16))/(SWIR10+SWIR12+SWIR13+SWIR16) e PMLI sono i top feature in entrambe SWIR e All-Features. Whitewash stagionale maschera firma plastica → introdotto indice NDPI_B = NDPI + Brightness/30000 che spinge OA a 98.08%.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 2: flowchart OBIA in 4 step (preprocessing → segmentation → DT classification → full classification) — riusabile.
- Fig. 4: Decision Tree con NDPI come primo split (-0.025), poi PMLI/PGI/SD-SWIR16/NDPI — visualizza explainability.
- Fig. 5: NDPI image + Google Earth foto degli oggetti high-NDPI non-greenhouse (recycling plant, solar panels, abandoned GH) — utile per spiegare confusioni.
- Fig. 7: spettri SWIR 1200–2400 nm per 4 colori plastica (black, grey, green, whitewashed) — mostra effetto masking del whitewash.
- Tab. 4: top-10 feature importance per ciascuna delle 3 strategie — citabile direttamente.
- Tab. 5: pixel-based confusion matrices con OA + UA + PA.

**Numeri forti** (metriche concrete: OA, F1, # bande, GSD)
- **OA = 90.85% (VNIR only) / 96.79% (SWIR only) / 97.38% (All Features)**. Kappa = 0.812 / 0.932 / 0.944. GH PA = 86.87% / 96.14% / 96.90%. NDPI_B knowledge-based: OA=98.08%, k=0.959, GH PA=99.28% (record). Salto VNIR→All-Features = +6.7% OA, +14% kappa (cifra-chiave per "spectral added value"). 16 bande WV-3 (8 VNIR @1.24 m + 8 SWIR @3.70 m → reset @1.2 m).

**Limite onesto** (terminologia: "generalizzazione" non "OOD", "classificare per rischio" non "rilevare")
- Material = plastica (PCG), NON asbestos: trasferibile metodologicamente al framing della tesi, ma non sostituisce un'ablation specifica per AC. Whitewashing introduce false negatives (effetto masking SWIR) — analogo al paint-sealing dei tetti AC. WV-3 commercial VHR = barriera economica per applicazioni large-scale; gli autori stessi raccomandano di esplorare Sentinel-2/Landsat-8/PRISMA per scaling. OBIA segmentation goodness influisce sul risultato finale (ED2=0.313 = "ragionevole" ma non ottimale).

**Cross-link**
- `bonifazi-2026-ac-python`: usa stesso sensore WV-3 16-band per asbestos — Aguilar è la "prova canonica" che SWIR vale la pena.
- `guo-li-2020-ndpi-wv3`: paper origine del NDPI index, citato come fonte primaria.
- `aguilar-2025-macroplastics-wv3`: extension stessa gruppo a macroplastiche marine — continuità linea ricerca.
- `cdw-2025-critical-wavelengths`: complementare per identificazione wavelength SWIR critical su construction waste.
- `plastics-uv-swir-2020`: spettrali lab plastica VNIR–SWIR — fondazione fisica del NDPI.
