---
id: "spectralwaste-2024-dataset"
title: "SpectralWaste: A Multimodal Spectral Dataset for Waste Sorting"
authors: ["(unknown)"]
year: 2024
venue: "arXiv"
doi: null
arxiv: "2403.18033"
link: "arXiv:2403.18033"
tags: ["waste", "dataset", "hyperspectral", "sorting"]
relevance: "medium"
status: "downloaded"
pdf: "library/spectralwaste-2024-dataset.pdf"
in_slides: []
relates_to: []
---

## Obiettivo
Creare il primo benchmark RGB vs iperspettrale per waste sorting, confrontare fusione modale.

## Metodo
RGB + HSI (224 bande) da nastro trasportatore. PCA a 3 bande. Confronto RGB-only, HSI-only, fusione.

## Risultati
PCA-reduced 3-band HSI = miglior trade-off accuratezza/efficienza. Fusione RGB+spectral batte sempre le singole modalità.

## Riassunto
La fusione di RGB con dati spettrali supera costantemente entrambe le modalità singole. Anche solo 3 bande spettrali via PCA migliorano su RGB.

## Cosa riutilizzare (tesi)
Evidenza che la fusione multimodale è superiore. Supporta l'approccio late fusion nella tesi.

## Note Claude

**Punti chiave**
- Casao, Pena, Sabater et al. (Universidad de Zaragoza + ATRIA Innovation, arXiv 2403.18033, marzo 2024): SpectralWaste e' il primo dataset multimodale RGB + iperspettrale raccolto da un impianto reale di sorting di rifiuti plastici (no setup di laboratorio).
- Acquisizione su nastro trasportatore con due telecamere line-scan sincronizzate: RGB Teledyne DALSA Linea (1200x1184, 8-bit) + HSI Specim FX17 (224 bande 900-1700 nm, 600x640, 16-bit). 6 classi target che causano problemi operativi: film, basket, cardboard, video tape, filament, trash bag.
- Contributo metodologico: label-transfer algorithm basato su SAM (Segment Anything) + COTR feature matching che propaga annotazioni RGB -> HSI senza calibrazione: +23.3% mIoU rispetto a manual alignment. PCA a 3 componenti (HYPER3) preserva 99.7% della varianza.
- Finding: la fusione RGB+HSI con CMX (architettura ibrida basata su SegFormer) batte sia RGB sia HSI puri (mIoU 58.2% vs 48.4% RGB-only, vs 54.3% HSI-only). HSI da sola supera RGB su classi sottili (video tape, filament) dove la firma spettrale del materiale e' piu' discriminante della forma.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 1: prototipo industriale con schema delle due telecamere + esempio RGB vs falso colore HSI - slide-ready per "ecco il setup multimodale".
- Fig. 2: 18 esempi (RGB + maschere ground-truth + HSI annotato via label-transfer) per le 6 classi - perfetta per slide didattica sulle classi target.
- Fig. 6: griglia qualitativa con risultati di 3 architetture x 5 modalita' (RGB, HYPER, HYPER3, RGB-HYPER, RGB-HYPER3) - mostra visivamente dove HSI aiuta.
- Tab. IV: tabella numerica completa con mIoU + FPS + GFLOPs + parametri per ogni combinazione (MiniNet-v2, SegFormer-B0, CMX-B0) - argomento "trade-off accuracy vs costo".

**Numeri forti** (metriche concrete, # bande, GSD)
- 2059 annotated instances su 852 immagini + 6803 immagini unlabeled per SSL/semi-sup. 6 classi: film (339), basket (300), cardboard (68), video tape (287), filament (111), trash bag (954).
- HSI: 224 bande 900-1700 nm SWIR (FX17), spazio nativo 600x640. PCA HYPER3 = 3 canali principali.
- Best mIoU: CMX RGB+HYPER 58.2% (54.7 M parametri, 8.4 GFLOPs); CMX RGB+HYPER3 56.6% (55.1 M, 5.6 GFLOPs).
- HSI da sola su SegFormer: video tape 33.6 mIoU vs solo 15.2 con RGB (+18.4 pt); filament 43.0 vs 6.1 (+36.9 pt).

**Limite onesto** (gap del paper — usa "generalizzazione" non "OOD")
- Setting industriale controllato (LED + halogen lighting, distanza fissa 1.7 m, nastro): la generalizzazione a setting satellitare o aereo con GSD molto piu' grossolane, illuminazione solare variabile, atmosfera e occlusioni non e' studiata. Range SWIR 900-1700 nm e' un sottoinsieme di quello disponibile a satelliti come WV-3, ma non copre 2000-2500 nm dove sono le feature C-H piu' diagnostiche. Solo 6 classi waste + classi imbalanced (cardboard 68 vs trash bag 954). Le due telecamere sono non-calibrate: label-transfer e' un workaround, non una soluzione strutturale.

**Cross-link**
- `cdw-2025-critical-wavelengths`: messaggio complementare - mentre cdw mostra "pochi narrowband bastano", SpectralWaste mostra "fusione RGB+HSI > singole modalita'". Insieme delineano il quando-quanto della spettralita'.
- `marida-2022-marine-debris`: dataset waste-correlato ma satellite (Sentinel-2), utile per il contrasto setting industriale vs setting orbitale.
- `plastics-uv-swir-2020`: spiega fisicamente perche' il SWIR 900-1700 nm discrimina plastiche (assorbimenti C-H a 1215, 1417, 1537, 1732 nm) - fornisce la base di firma per le 6 classi di SpectralWaste.
- `torres-2023-aerialwaste`: dataset di waste detection RGB aereo - confronto naturale "RGB-only ad alta risoluzione" vs "RGB+HSI a media risoluzione" per il framing del valore aggiunto MS.
- `fraternali-2024-survey`: survey waste detection che inquadra il gap tra setting industriale (SpectralWaste) e setting Earth Observation.
- `xiong-2024-dofa` / `anysat-2024`: FM "any-sensor" candidati per gestire la differenza di numero di bande tra RGB-only e RGB+HSI con architettura unica.

