---
id: "kokaly-2017-splib07a"
title: "USGS Spectral Library Version 7 (splib07a)"
authors: ["Kokaly", "et al."]
year: 2017
venue: "USGS Data Series"
doi: "10.3133/ds1035"
arxiv: null
link: "https://doi.org/10.3133/ds1035"
tags: ["signature-library", "usgs", "splib07a"]
relevance: "critical"
status: "downloaded"
pdf: "library/kokaly-2017-splib07a.pdf"
in_slides: ["spectral-signatures"]
relates_to: []
---

## Obiettivo
Fornire una libreria spettrale curata di materiali di riferimento (minerali, plastiche, vegetazione, costruzione) per calibrazione e validazione.

## Metodo
Misure con spettrometri da laboratorio e campo. 2151 canali, 350-2500 nm, risoluzione 1 nm. Copre minerali, polimeri (PE, PP, PET, ABS, polistirene), cellulosa, cotone, nylon, poliestere, calcestruzzo, mattoni, asfalto.

## Risultati
Libreria di riferimento più usata al mondo per spectral matching e validazione. Disponibile in ASCII e SPECPR. Copertura VNIR+SWIR completa per materiali di interesse waste.

## Riassunto
Libreria spettrale di riferimento. Già scaricata e verificata (21 MB). Usata nelle slide per i grafici di firme spettrali di plastiche, costruzione, vegetazione, tessili.

## Cosa riutilizzare (tesi)
Fonte primaria per i plot delle firme spettrali nel capitolo teoria. Endmember per analisi di confusion pair.

## Note Claude
**Punti chiave**
- USGS splib07a e' la libreria spettrale di riferimento mondiale: misure di laboratorio, da campo e convolute alla risposta di sensori reali (AVIRIS, ASTER, Landsat, Sentinel-2, WorldView-3) per uso operativo.
- Range 350-2500 nm campionato a ~1 nm (2151 canali) con spettro-radiometri ASD FieldSpec. Copre minerali, polimeri (PE, PP, PET, PVC, ABS, PS, nylon), vegetazione, materiali costruttivi (calcestruzzo, mattoni, asfalto), suoli, neve, materiali artificiali.
- Distribuita in formato ASCII e SPECPR, gia' scaricata localmente in `spectral/USGSSpeclib/usgs_splib07/` (~21 MB). Sentinel value `-1.23e+34` per canali mancanti.
- Anchor di riferimento per le firme spettrali di asbestos cement, plastiche e materiali waste-correlati nelle slide della tesi.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 1: schema di acquisizione spettrale + flusso da misura grezza a libreria convoluta per sensori multispettrali.
- Tab. 1-2: inventario materiali con conteggi per categoria (minerali, vegetazione, polimeri, costruzione).
- Convoluzioni S2/WV-3 disponibili come subset s06av95a_envi, s07av95a_envi: utili per simulare la risposta del nostro sensore SuperDove a partire dalle firme di laboratorio.

**Numeri forti** (metriche concrete, # bande, GSD)
- 2151 canali, 350-2500 nm, risoluzione spettrale ~1 nm.
- ~2400 firme spettrali totali distribuite in ~1300 materiali distinti.
- Subset convoluti per Sentinel-2 (13 bande), WorldView-3 (16 bande VNIR+SWIR), Landsat 7/8, ASTER, MODIS, AVIRIS.
- No-data sentinel: `-1.23e+34` da filtrare in pre-processing.

**Limite onesto** (gap del paper — usa "generalizzazione" non "OOD")
- Misure di laboratorio in condizioni ideali (Lambertiano, illuminazione controllata): la generalizzazione a scene reali satellitari (atmosfera, BRDF, mixed pixels, weathering, geometria di acquisizione) richiede continuum removal, atmospheric correction e attenta gestione delle scale spaziali. Non sostituisce ground truth in-scene.

**Cross-link**
- `plastics-uv-swir-2020`: complementare per plastiche weathered marine vs vergini, stesso range UV-SWIR.
- `cilia-2015-ac-weathering`: firme di asbestos cement weathered da ARPA Lombardia, da confrontare con i pochi spettri AC presenti in splib07a.
- `shepherd-2025-asbestos-enmap`: usa convoluzione di firme di libreria a bande EnMAP per detection AC, esattamente il workflow che possiamo replicare con splib07a per SuperDove.
- `aguilar-2025-macroplastics-wv3` e `guo-li-2020-ndpi-wv3`: assumono firme tipo splib07a come riferimento per definire indici spettrali su WV-3.
