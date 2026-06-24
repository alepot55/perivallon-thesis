---
id: "cilia-2015-ac-weathering"
title: "Mapping of Asbestos Cement Roofs and Their Weathering Status Using Hyperspectral Aerial Images"
authors: ["Cilia", "Panigada", "Rossini", "Candiani", "Pepe", "Colombo"]
year: 2015
venue: "ISPRS Int. J. Geo-Information"
doi: "10.3390/ijgi4020928"
arxiv: null
link: "https://doi.org/10.3390/ijgi4020928"
tags: ["asbestos", "hyperspectral", "mivis", "sam", "weathering", "italian"]
relevance: "high"
status: "downloaded"
pdf: "library/cilia-2015-ac-weathering.pdf"
in_slides: ["asbestos-anchor"]
relates_to: ["shepherd-2025-asbestos-enmap", "bonifazi-2026-ac-python"]
---

## Obiettivo
Mappare tetti in asbesto-cemento in area urbana e sviluppare un indice spettrale per stimare il loro stato di deterioramento (utile per priorità di rimozione).

## Metodo
Sensore aereo MIVIS (102 bande, visibile→termico). Classificazione supervisionata SAM (Spectral Angle Mapper) addestrato su classe cemento. Nuovo Indice di Deterioramento Superficiale (ISD) basato su bande VIS-NIR per quantificare colonizzazione di muschi/licheni su tetti weathered.

## Risultati
User accuracy 86%, producer accuracy 89% per identificazione AC. ISD discrimina due classi di weathering (alta vs bassa). Mappa AC associata a catasto per supporto decisionale ai comuni.

## Riassunto
Cilia, Panigada, Rossini, Candiani, Pepe, Colombo (Università Milano-Bicocca + CNR-IREA). ISPRS Int. J. Geo-Inf. 4(2):928-941. Riferimento canonico italiano per asbestos-cemento via SAM iperspettrale aereo MIVIS. Memoria della tesi attribuiva il DOI a Frassy/Bassani — è in realtà Cilia 2015.

## Cosa riutilizzare (tesi)
Workflow SAM + endmembers; idea dell'Indice di Deterioramento (ISD) per priorità rimozione; integrazione con catasto = utilità ARPA; baseline metodologico storico.

## Note Claude

**Punti chiave**
- Riferimento canonico italiano per mappatura asbestos-cemento via SAM iperspettrale aereo MIVIS (102 bande VIS–TIR, 3 m GSD, 5 strisciate sorvolo 5/7/2013) su 5 municipalità Brianza (Monza, Muggiò, Lissone, Seregno, Biassono, 65 km², 248 mila abitanti).
- Workflow 2-step: (1) SAM su MNF components con endmember-set di 5 materiali (AC, concrete, tiles, alluminio, PVC); (2) seconda SAM ristretta a pixel AC con solo 2 endmember (AC+concrete) per ripulire commissione.
- Introduce un Indice di Deterioramento Superficiale (ISD) basato non sulle fibre ma sull'assorbimento clorofilla a 0.68 μm (muschi/licheni colonizzano AC weathered) — soluzione operativa quando SNR a 2.32 μm (banda diagnostica asbesto) non è raggiungibile.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 2: spettri AC field vs MIVIS per 5 età/esposizione di tetto, mostra effetto matrix-color e vegetation absorption — perfetto per slide "spectral signatures of AC weathering".
- Fig. 5: classification map SAM su Seregno (red=AC, cyan=concrete, peach=tiles) — visualizzazione classica per slide.
- Fig. 6: ISD vs year (1960–1989) e ISD vs exposure (Nord vs altro) — supporto statistico priorità rimozione.
- Fig. 8: ISD map a livello edificio con codifica priorità (rosso >4 alta, verde ≤4 bassa) — esempio operativo per ARPA/Comuni.
- Tab. 1–2: accuracy per RUN — utilissima per quantificare 86% PA / 89% UA.

**Numeri forti** (metriche concrete: OA, F1, # bande, GSD)
- Producer accuracy 89%, User accuracy 86% per AC dopo 2-step (PA passa da 75% media a 86%). MIVIS 102 bande (92 VIS-SWIR 0.43–2.50 μm + 10 TIR 8.20–12.70 μm), 3 m GSD. 3170 edifici AC mappati = 8% dei tetti totali area. 40% ISD>4 (alta priorità), 60% ISD≤4. ISD MIVIS ↔ ISD ASD ground: R²=0.62, p=0.004 (n=11). ANOVA: year F=6.04 p<0.001; exposure F=33.38 p<0.001.

**Limite onesto** (terminologia: "generalizzazione" non "OOD", "classificare per rischio" non "rilevare")
- ISD = proxy della colonizzazione vegetale, non delle fibre rilasciate — assume che tetti vecchi siano sia più colonizzati sia più friabili, ma muschi possono trattenere fibre (riportato da letteratura). 3 m GSD esclude tetti <36 m² (garage, sheds) — generalizzazione a tetti piccoli limitata. Aereo MIVIS = non scalabile su grande scala; necessario sensor satellite (apre la strada a Shepherd 2025 e Bonifazi 2026). Non rileva, ma "classifica per rischio di rimozione".

**Cross-link**
- `shepherd-2025-asbestos-enmap`: parente diretto al satellite — anche Shepherd usa SAM nell'ensemble e MNF. ISD pattern di Cilia potrebbe arricchire la libreria EnMAP.
- `bonifazi-2026-ac-python`: passaggio MIVIS aereo → WV-3 satellite open-source — Bonifazi cita Cilia (PRAL Lombardia + 2-step MLC).
- `aguilar-2021-wv3-ablation`: SAM + MNF + endmember-based su materiale plastica anziché asbestos; metodologicamente parallelo.
- `kokaly-2017-splib07a`: libreria USGS contiene chrysotile/serpentine — fonte di endmember alternativa.
