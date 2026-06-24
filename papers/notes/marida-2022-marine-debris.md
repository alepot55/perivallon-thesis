---
id: "marida-2022-marine-debris"
title: "MARIDA: A benchmark for Marine Debris detection from Sentinel-2 remote sensing data"
authors: ["Kikaki", "et al."]
year: 2022
venue: "PLOS ONE"
doi: "10.1371/journal.pone.0262247"
arxiv: null
link: "https://doi.org/10.1371/journal.pone.0262247"
tags: ["marine-debris", "sentinel-2", "benchmark", "low-res-survey"]
relevance: "high"
status: "downloaded"
pdf: "library/marida-2022-marine-debris.pdf"
in_slides: ["low-res-survey"]
relates_to: []
---

## Obiettivo
Creare un benchmark pixel-level multispettrale per la detection di marine debris da Sentinel-2.

## Metodo
1.381 patches Sentinel-2 con annotazioni pixel-level su 15 classi (plastica, schiuma, onde, nubi, ecc.). Tutte 12 bande S2 incluse. Baseline con U-Net, Random Forest, XGBoost.

## Risultati
Primo benchmark MS pubblico con annotazioni material-level per debris. Miglior baseline: U-Net su tutte 12 bande. La rimozione delle bande SWIR degrada significativamente la performance.

## Riassunto
Benchmark più citato per MS waste detection (anche se su acqua, non terra). Dimostra operativamente il valore delle bande SWIR per discriminare plastica da altri materiali galleggianti.

## Cosa riutilizzare (tesi)
Dataset di riferimento per validare la pipeline MS prima di applicarla ad AerialWaste. Struttura delle annotazioni pixel-level come modello. Bande S2 e split train/val/test.

## Note Claude
**Punti chiave**
- Primo benchmark open-access pixel-level su Sentinel-2 dedicato a marine debris, costruito su 63 scene S2 in 11 paesi (2015-2021) con 1.381 patch 256x256 e 837.357 pixel annotati su 15 classi tematiche (Marine Debris, Sargassum dense/sparse, Natural Organic Material, Ship, Foam, Clouds, Marine Water, Turbid/Sediment-Laden/Shallow Water, Waves, Wakes, Mixed Water).
- Annotazione ground-truth multi-fonte (citizen science, 4ocean, social media, letteratura), tre annotatori indipendenti con confidence level (alto/medio/basso) e protocollo inter-annotatore per gestire l'ambiguità spettrale fra MD e NatM.
- Baseline weakly-supervised: Random Forest in tre varianti (solo bande, +indici spettrali NDVI/NDWI/FAI/FDI/NDMI/BSI/NRD, +features GLCM tessiturali) e U-Net, oltre a ResNet per multi-label classification a livello patch.

**Figure/tabelle usabili in slide**
- Fig. 2: mappa mondiale dei 11 siti con punti rossi — ottima per slide #7 a illustrare la sparsità globale a 10 m.
- Fig. 3: firme spettrali medie (440-2200 nm) di Marine Debris vs Natural Organic Material — mostra che a 10/20 m la separabilità si gioca su 865 nm e SWIR (B11/B12), confondendo le due classi nel visibile.
- Fig. 4: t-SNE con SAM metric — visualizza cluster ben distinti per MD e cluster sovrapposti con Ship/Sargassum, segnala cosa il sensore MANCA.
- Tabella 4: IoU/PA/F1 per classe — Marine Debris IoU 0.55-0.67 (RF), U-Net solo 0.33; NatM IoU 0.17-0.31 (gap che peggiora a bassa risoluzione).

**Numeri forti**
- 1.381 patch, 837.357 pixel, 63 scene S2 L1C, 11 bande Rayleigh-corrected a 10 m (esclusi B9 vapore, B10 cirrus).
- 3.339 pixel MD annotati (1.625 high-confidence). Split 50/25/25 = 694/328/359 patch.
- F1 RF migliore = 0.79 medio, U-Net 0.69 medio; SLWater perfetto F1=1.0, SWater peggiore F1=0.16-0.62.

**Limite onesto**
- A 10 m GSD i pixel MD sono quasi sempre sub-pixel e si confondono spettralmente con vegetazione galleggiante (NatM) e schiuma; la generalizzazione fra siti è debole — il modello impara distribuzioni regionali (Honduras Gulf domina i pixel) anziché firme materiali. La classificazione per rischio di contaminazione marina rimane vincolata da risoluzione spaziale e variabilita di stato del mare.

**Cross-link**
- `tisza-2023-waste-change`: stessa filosofia S2 + Random Forest ma su acque interne (Tisza); MARIDA è il riferimento marino, Tisza quello fluviale.
- `global-dumpsites-2023`: complementare — MARIDA copre l'acqua, global-dumpsites la terra a VHR.
- `emit-2025-plastic`: dimostra cosa si guadagna passando da 10 m MS a 60 m hyperspectral (rilevazione di tipi polimerici specifici, non solo classe debris).
- `tasseron-2021-plastic-classifier`: contrasto banda larga S2 vs banda stretta WV-3, motiva i limiti di MARIDA sul SWIR.
