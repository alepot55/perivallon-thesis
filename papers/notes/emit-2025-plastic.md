---
id: "emit-2025-plastic"
title: "Global-Scale Detection of Plastic From Space With the EMIT Imaging Spectrometer"
authors: ["(unknown)"]
year: 2025
venue: "Geophys. Res. Lett."
doi: "10.1029/2024GL112416"
arxiv: null
link: "https://doi.org/10.1029/2024GL112416"
tags: ["plastic", "hyperspectral", "emit", "global-scale"]
relevance: "high"
status: "downloaded"
pdf: "library/emit-2025-plastic.pdf"
in_slides: ["high-res-survey"]
relates_to: []
---

## Obiettivo
Dimostrare la detection di plastiche specifiche (HDPE, PVC) da orbita su scala globale.

## Metodo
EMIT hyperspectral (285 bande, 60 m GSD, 381-2493 nm). Matched filtering alle bande diagnostiche (1200, 1710, 2300 nm). Validazione su siti agricoli, impianti di riciclaggio, hotspot industriali.

## Risultati
Prima detection globale di HDPE/PVC da satellite. Hotspot identificati in Spagna, Italia, Messico, Taiwan. Le firme di laboratorio trasferiscono a orbita.

## Riassunto
Paper landmark del 2025 per orbital plastic detection. Pubblicato su Geophysical Research Letters. Dimostra che le firme spettrali delle plastiche sono rilevabili da satellite quando il SWIR è disponibile.

## Cosa riutilizzare (tesi)
Riferimento per la sezione firme spettrali e missioni iperspettrali. Conferma empirica della rilevabilità orbitale di HDPE/PVC.

## Note Claude
**Punti chiave**
- Estrela et al. (JPL Caltech, NASA EMIT team) eseguono la prima mappatura continentale di HDPE e PVC da spettrometro imager orbitale (EMIT su ISS, latitudini +/-52deg). Coverage giugno-ottobre 2023 su aree aride (USA Ovest, Sudamerica SW, Nord/Ovest Africa, Medio Oriente, Asia centrale ed est).
- Metodo: matched filter column-wise sulle riflettanze EMIT calibrate (380-2500 nm, 60 m GSD), con spettri target dalla USGS Spectral Library v7 (HDPE = GDS385, PVC = GDS338). Range MF limitato a SWIR 1100-2500 nm, escluse bande di assorbimento del vapore (1300-1560, 1770-2000 nm).
- Detection threshold: MF >0.02 per PVC, >0.03 per HDPE, con doppia validazione su feature 1700+2300 nm e rigetto automatico spettri con assorbimento a 2200 nm (per filtrare falsi positivi da gypsum nel Sahara).

**Figure/tabelle usabili in slide**
- Fig. 1: spettri EMIT su area Aguilas (Spagna, 22/6/2023) con assorbimenti a 1200/1710/2300 nm sovrapposti su RGB image — esempio diretto di MS-vs-hyperspectral signal richness.
- Fig. 2: mappa mondiale dei detection con istogrammi lat/lon e copertura cloud-free; HDPE blu, PVC rosso, cluster forte in Europa per PVC, distribuzione larga per HDPE in Europa+USA+Asia.
- Fig. 3a: tre pannelli Aguilas/Sicily/Hidalgo con foto Google Street View di greenhouses + spettri lab vs EMIT + MF scores (HDPE 0.030-0.032, PVC 0.023-0.028) — caso d'uso "added value spettrale" per slide #9-#10.
- Fig. 4b: detection in aquavoltaic Taiwan con MF HDPE = 0.062 (il piu' forte del paper) — esempio di plastica industriale rilevata anche su sfondo acqueo.

**Numeri forti**
- Coverage 4 mesi, 285 bande EMIT, 60 m GSD. Threshold MF 0.02-0.03. Centri di assorbimento usati: 1215, 1417, 1537, 1732, 2046, 2313 nm.
- Hotspot detection: Spagna (Almeria, Aguilas, Murcia), Italia (Sicilia), Messico (Hidalgo), Taiwan, Corea del Sud, Giappone, Filippine. Plastica agricola FAO 2019 = 12.5 Mt globali, proiezione 9.5 Mt 2030 solo greenhouse/mulching/silage.
- Korea: 50.000 ton/anno di film LDPE da greenhouse 2017-2020.

**Limite onesto**
- A 60 m GSD molte detection sono sub-pixel (l'MF score 0.03 non significa "3% di copertura" ma proiezione spettrale normalizzata); polimeri senza feature SWIR distintive (PET, PS, PP a basso contrasto) sono sotto-rappresentati. La classificazione per rischio resta limitata: landfill coperti o plastica interrata non vengono rilevati, e copertura non globale (Cina esclusa, no monitoraggio temporale denso). La generalizzazione richiedera' missioni SBG e CHIME con coverage polare.

**Cross-link**
- `kokaly-2017-splib07a`: la libreria USGS che fornisce i target HDPE/PVC del matched filter — collegamento diretto laboratorio->orbita.
- `aguilar-2025-macroplastics-wv3`: stesso framework metodologico (matched filter SWIR) ma a 3.7 m con WV-3 invece di 60 m hyperspectral; complementarita' GSD vs ricchezza spettrale.
- `plastics-uv-swir-2020`: caratterizzazione laboratorio delle stesse feature SWIR; EMIT le valida da orbita.
- `shepherd-2025-asbestos-enmap`: parallelo con EnMAP per amianto — entrambe hyperspectral orbitali, EMIT su plastica, EnMAP su asbestos.
- `cdw-2025-critical-wavelengths`: identifica le wavelength chiave per CDW, EMIT le usa per plastica.
