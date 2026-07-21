---
id: "cdw-2025-critical-wavelengths"
title: "Critical wavelengths for construction and demolition waste materials"
authors: ["(unknown)"]
year: 2025
venue: "arXiv"
doi: null
arxiv: "2501.02239"
link: "arXiv:2501.02239"
tags: ["construction-demolition", "wavelengths", "materials"]
relevance: "medium"
status: "downloaded"
pdf: "library/cdw-2025-critical-wavelengths.pdf"
in_slides: []
relates_to: []
---

## Obiettivo
Identificare le lunghezze d'onda più discriminanti per la classificazione di rifiuti C&D.

## Metodo
Analisi spettrale iperspettrale (768 bande) di materiali C&D. Test con subset progressivi di bande.

## Risultati
Aggiungere la sola banda a 800 nm (NIR) all'RGB dà accuratezze comparabili a tutte le 768 bande. Poche bande ben scelte bastano.

## Riassunto
Risultato chiave: il NIR da solo cattura quasi tutta l'informazione discriminante per materiali C&D. Il SWIR aggiunge margine per plastica e gomma.

## Cosa riutilizzare (tesi)
Motivazione forte per l'approccio multispettrale (poche bande > RGB). Guida nella selezione delle bande prioritarie.

## Note Claude
**Punti chiave**
- Vitek, Zbiral, Nezerka (CTU Praga, Resources Conservation & Recycling 2025, DOI 10.1016/j.resconrec.2025.108123): identificano via iperspettrale (SPECIM PFD4K-65-V10E, 768 bande 400-1000 nm) le lunghezze d'onda critiche per classificare 10 materiali C&D (AAC, EPS, asfalto, mattone, calcestruzzo, malta, tegola, piastrelle top/bottom, legno).
- Pipeline a due stadi: Stage 1 seleziona quante e quali lunghezze d'onda aggiungere a RGB; Stage 2 ottimizza filtri narrowband (lambda centrale 425-975 nm a step 25 nm; FWHM 5/20/35/50 nm). MLP a 2 hidden layers da 20 neuroni come classificatore.
- Finding-bombshell: bastano DUE lunghezze d'onda extra oltre a RGB per arrivare alle stesse prestazioni dell'iperspettrale full-spectrum (768 bande). Optimum: una lambda1 in 650-750 nm + una lambda2 in 850-1000 nm.
- Aggiungere whole-spectrum features (F_peak, F_area) DEGRADA il modello: poche bande mirate > tutto lo spettro. Insensitivita' alla FWHM (5-50 nm): filtri commerciali standard sono ok.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 5: accuracy vs # features (3=RGB only, 4=RGB+1, 5=RGB+2, ...). Plateau a 5 features con accuracy ~0.96; con solo RGB scende a 0.87. Slide-ready per "few bands suffice".
- Fig. 6: heatmap 2D di accuracy in funzione di (lambda1, lambda2) per FWHM=5/20/35/50 nm. Hotspot rosso evidente nella zona NIR. Mostra che la scelta delle bande conta molto piu' della larghezza di banda.
- Fig. C.9: 11 sub-plot delle firme spettrali per materiale - utile per slide "ecco perche' NIR discrimina".
- Fig. A.7: galleria fotografica dei 10 campioni C&D - bel visual per slide didattica.

**Numeri forti** (metriche concrete, # bande, GSD)
- 768 bande iperspettrali tra 400-1000 nm (sampling ~0.78 nm, risoluzione effettiva ~3 nm). RMS spot size <9 um.
- Accuracy: 3 features (RGB) = 0.87; 5 features (RGB + 2 NIR) = 0.96; 12 features = 0.97. Picco F-weighted = 0.9068 con FWHM=35 nm.
- Bande extra ottimali: ~500 nm + ~800 nm (Stage 1) oppure 650-750 nm + 850-1000 nm (Stage 2 con filtri narrowband).
- 10 classi materiali, ~167-314 sample per classe, 80/20 train/test + 25% validation, StandardScaler.

**Limite onesto** (gap del paper — usa "generalizzazione" non "OOD")
- Studio in laboratorio con illuminazione alogena controllata su campioni puliti e isolati: la generalizzazione a sorting lines reali (polvere, occlusioni, illuminazione variabile, mix di materiali in pixel) e a setting outdoor/satellitare richiede ri-calibrazione. Non testato su materiali fuori-set; gli autori avvertono che cambio di composizione richiede di rifare la selezione delle bande. Concrete resta confuso (87% errori): la classe piu' problematica anche col setup ottimo.

**Cross-link**
- `aguilar-2021-wv3-ablation`: analogo concettuale satellitare - poche bande ben scelte di WV-3 bastano per la maggior parte delle classi. Argomento gemello "few bands suffice".
- `spectralwaste-2024-dataset`: stesso messaggio (PCA-3 ~ full HSI) ma su scena di sorting industriale con HSI 224 bande - converge sullo stesso paradigma.
- `plastics-uv-swir-2020` e `kokaly-2017-splib07a`: spiegano fisicamente perche' NIR ~800 nm discrimina (transizioni elettroniche + C-H overtones).
- `bonifazi-2026-ac-python`: stessa logica per asbestos cement nella nostra pipeline Lombardia - selezionare pochi indici spettrali invece che usare tutto lo spettro.
- `corley-2024-resizing`: complementare sul lato preprocessing - quando confronti "pochi canali ben fatti vs molti", il preprocessing deve essere coerente per non inquinare il confronto.
