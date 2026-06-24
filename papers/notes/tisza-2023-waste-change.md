---
id: "tisza-2023-waste-change"
title: "Waste detection and change analysis based on multispectral satellite imagery"
authors: ["(Hungarian Tisza team)"]
year: 2023
venue: "arXiv"
doi: null
arxiv: "2303.14521"
link: "arXiv:2303.14521"
tags: ["waste", "change-detection", "multispectral", "sentinel-2", "planetscope"]
relevance: "medium"
status: "downloaded"
pdf: "library/tisza-2023-waste-change.pdf"
in_slides: []
relates_to: []
---

## Obiettivo
Rilevare discariche illegali e analizzare cambiamenti temporali con dati Sentinel-2 multispettrali.

## Metodo
Sentinel-2 (13 bande) + Random Forest. Analisi temporale lungo il fiume Tisza.

## Risultati
~96% accuracy nella detection. NIR risultata la banda più discriminante per debris plastico.

## Riassunto
Conferma che Sentinel-2 multispettrale + ML classico raggiunge alta accuracy per waste detection. Il NIR è la banda chiave.

## Cosa riutilizzare (tesi)
Baseline ML tradizionale (Random Forest) su S2 per confronto. Conferma del ruolo del NIR.

## Note Claude
**Punti chiave**
- Magyar, Cserep, Vincellér, Molnár (ELTE Budapest + Tisza Plastic Cup Initiative) propongono pipeline operativa Random Forest su Sentinel-2 (13 bande, 10-60 m) e PlanetScope (4 bande, 3 m) per due task complementari: identificazione hot-spot di discariche illegali e identificazione di sbarramenti di rifiuti a galla in corrispondenza di dighe idroelettriche sul fiume Tisza (Ucraina/Romania/Ungheria).
- L'indice cardine e' il Plastic Index (PI = NIR/(NIR+Red)) di Themistocleous et al. 2020, accompagnato da NDWI, NDVI, RNDVI, SR; addestramento su due aree note (discarica di Pusztazamor e idroelettrico di Kiskore) con 5 classi (waste, water, forest/meadow, buildings, bare ground).
- Workflow operativo: classificazione RF -> binarizzazione waste+water -> apertura morfologica + dilatazione (kernel 5x5) per eliminare falsi positivi e isolare l'isola di rifiuti; web app con alert email per monitoraggio temporale change-detection.

**Figure/tabelle usabili in slide**
- Fig. 3 (Themistocleous reprise): mosaico 9 indici (NDWI/WRI/NDVI/AWEI/MNDWI/NDMI/SR/PI/RNDVI) sul target plastico — slide #7 per mostrare CHE COSA gli indici a 10 m catturano e cosa no (PI 0.39-0.42 sul target reale).
- Fig. 6 (Deponia Waste Centre, 27/06/2019): before/after/heatmap a tre confidence (red 90-100%, yellow 80-90%, green 70-80%) — caso d'uso "becca la discarica ma con confidence rumorosa".
- Fig. 7 (Lake Calinesti, Romania): isola di plastica galleggiante chiaramente rilevata lungo la riva — esempio positivo a 10 m, da mettere in slide #8.
- Fig. 8-9 (Kiskore hydropower plant): change detection 2019 vs 2020 dello sbarramento — mostra la dinamica temporale che a 10 m e' osservabile solo su accumuli grandi (>100 m^2).

**Numeri forti**
- Cross-validation accuracy ~96% su ~200.000 pixel training. Execution time: hot-spots 26 min per immagine 6.614x5.981 px (S2), water-blockage 29 min.
- Bande S2 usate: tutte 10-20 m (B2-B8a, B11-B12), esclusi B1/B9/B10 a 60 m. PlanetScope: 4 bande 3 m (Blue 455-517, Green 500-590, Red 590-682, NIR 780-888).
- Target di test (Themistocleous): bottiglie 3x10 m = 30 m^2 = ~3 pixel S2 a 10 m — confine inferiore di rilevabilita'.

**Limite onesto**
- A 10-30 m la classificazione per rischio funziona solo su accumuli grandi e densi (idroelettrici, discariche estese >100 m^2); confondibilita' con bare ground/buildings e' alta e richiede post-processing morfologico aggressivo che cancella i piccoli hot-spot. La generalizzazione fuori dal bacino Tisza non e' validata, e l'autunno/inverno produce risultati non utilizzabili per copertura nuvolosa. Niente analisi spettrale del materiale: non distingue plastica vs schiuma vs detriti vegetali.

**Cross-link**
- `marida-2022-marine-debris`: stessa filosofia S2 + ML classico ma in mare, qui in fiume; entrambi mostrano il limite 10 m.
- `global-dumpsites-2023`: complementare — global-dumpsites usa VHR per discariche puntuali, tisza usa MS 10 m per copertura temporale frequente.
- `emit-2025-plastic`: dimostra il salto qualitativo dal "vedere accumuli" al "identificare polimeri" con hyperspectral.
- `aguilar-2025-macroplastics-wv3`: contrasto risoluzione (3.7 m WV-3 con SWIR vs 10 m S2 senza polymer ID).
