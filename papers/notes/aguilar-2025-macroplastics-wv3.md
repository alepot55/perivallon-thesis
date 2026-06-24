---
id: "aguilar-2025-macroplastics-wv3"
title: "Mapping terrestrial macroplastics and polymer-coated materials in an urban watershed using WorldView-3 and laboratory reflectance spectroscopy"
authors: ["Aguilar", "Sousa", "Uhrin", "Gudino-Elizondo", "Biggs"]
year: 2025
venue: "Environmental Monitoring and Assessment"
doi: "10.1007/s10661-025-14125-z"
arxiv: null
link: "https://doi.org/10.1007/s10661-025-14125-z"
tags: ["wv-3", "swir", "plastic", "high-resolution", "high-res-survey"]
relevance: "high"
status: "downloaded"
pdf: "library/aguilar-2025-macroplastics-wv3.pdf"
in_slides: ["high-res-survey"]
relates_to: ["ndpi-2020-wv3", "tasseron-2021-plastic-classifier"]
---

## Obiettivo
Mappare aggregazioni di plastica terrestre usando le 8 bande SWIR di WorldView-3.

## Metodo
Spectral analysis su WV3 SWIR (8 bande, 3.7 m). Correlazione firme lab vs satellite. Target: aggregazioni 80-150 m2.

## Risultati
Precision 0.92-0.95. Correlazione lab-to-satellite r = 0.95. Le firme spettrali sono consistenti da laboratorio a 600 km.

## Riassunto
Dimostra che le firme spettrali di laboratorio sono rilevabili da satellite nel SWIR. WV3 è il gold standard per material classification.

## Cosa riutilizzare (tesi)
Validazione dell'approccio spettrale. Se si ottengono dati WV3, le bande SWIR sono le più discriminanti per la plastica.

## Note Claude
**Punti chiave**
- Aguilar, Sousa, Uhrin, Gudino-Elizondo, Biggs (SDSU + NOAA) mappano macroplastiche e materiali polymer-coated in 10.5 km^2 di Los Laureles Canyon (confine USA-Mexico, Tijuana) usando WorldView-3 SWIR (8 bande, ~4 m GSD) + spettroscopia di riflettanza laboratorio. Tre fasi: survey di campo (44 reach con Trash Condition Categories 1-12), 22 oggetti raccolti (17 plastici inclusi nel library: HDPE, LDPE, PET, PS, PVC), e matched filter su WV-3.
- Costruzione di Mean Laboratory Plastic Spectrum (MLPS) su 18 spettri (4 HDPE + 4 LDPE + 7 PET + 2 PS + 1 PVC dall'USGS), convolto alla SRF di WV-3; image endmember derivato da PCA spettrale identifica 4 vertici (Substrate/Vegetation/Dark/Polymer) — separabilita' perfetta (J-M = TD = 2.0 fra tutti gli endmember).
- Validazione: 200 poligoni random sample, certainty level 1-5 visivo su VHR true-color, precision 92.5% complessivo, 95.3% per CL 4-5 (High/Very High).

**Figure/tabelle usabili in slide**
- Fig. 4a-b: spettri lab di PS/PET/HDPE-PVC/LDPE confrontati con vegetazione/substrato/urban materials, e versione convolta a 8 bande WV-3 — slide #9 per spiegare CHE COSA si perde dal lab al sensore (assorbimenti a 1140, 1660, 1908 nm spariscono nelle bande larghe).
- Fig. 5: WV-3 SWIR spectral feature space (PC1-PC2-PC3) con 4 endmember cerchiati (S/V/D/P) e spettri associati — illustra geometricamente la separabilita' che WV-3 raggiunge e S2 NON raggiunge.
- Fig. 7: matched filter map sull'intero bacino con zoom su rooftops bianco/rosso (MF alto, slide #9 caso "polymer-coated infrastructure"), recreational courts, waste patches SE/SW (MF medio) — il "caso piu' forte" per spectral added value urbano.
- Tabella 3-4: correlazioni Pearson e SSV laboratorio vs image endmember vs USGS — MLPS-vs-image-endmember r = 0.95**, SSV < 0.4 (massima similarita').

**Numeri forti**
- 8 bande SWIR WV-3 (1195-2365 nm), GSD 3.7 m. PAN 0.31 m, VNIR 1.24 m. Acquisizioni 2018-01-18, 2019-01-04, 2020-05-03 (off-nadir 27.5deg).
- Precision 92.5% (185/200 TP), 95.3% per CL>=4 (161/169). Aggregazioni waste largest 80-150 m^2 (4-20 pixel WV-3).
- Assorbimenti diagnostici PE/HDPE/LDPE/PVC: 1210, 1400-1430, 1728 nm; PET 1415, 1660, 1908, 2132 nm; PS 1141, 1450, 1678, 2167 nm.

**Limite onesto**
- MF privilegia pixel con grandi instanze omogenee di plastica (rooftops, sintetic turf) e sotto-rileva aggregazioni sparse di waste in stream channels — la classificazione per rischio "discarica informale" risulta meno robusta della classificazione per "tetto coperto in polimero". Inoltre il "polymer-coated" e' non-uniqueness: vernici e coating polimerici producono firme indistinguibili dalla plastica pura. La generalizzazione fuori da contesti aridi e non testata, e il lag temporale 2020-immagine vs 2021-campo ha introdotto omissioni di Tipo II non quantificabili.

**Cross-link**
- `ndpi-2020-wv3` (Guo & Li 2020): NDPI usa le stesse bande SWIR di WV-3 ma con indice scalare; Aguilar 2025 supera NDPI con approccio matched filter spettrale completo.
- `tasseron-2021-plastic-classifier` (citato come reference SWIR FX10): fornisce lo spettro di riferimento dei polimeri usato per categorizzare i 17 sample senza RIC visibile.
- `aguilar-2021-wv3-ablation`: predecessore della stessa autrice, ablazione canonica delle 8 bande WV-3 per greenhouses.
- `kokaly-2017-splib07a`: fornisce lo spettro PVC USGS aggiunto al library del paper (1 di 18 sample).
- `emit-2025-plastic`: stesso framework MF ma a 60 m hyperspectral; Aguilar e' la versione VHR multispettrale dello stesso paradigma.
- `plastics-uv-swir-2020`: caratterizzazione laboratorio delle stesse feature 1210/1660/1728/2300 nm.
