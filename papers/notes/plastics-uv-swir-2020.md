---
id: "plastics-uv-swir-2020"
title: "Hyperspectral UV to SWIR characteristics of marine-harvested, washed-ashore and virgin plastics (spectral library)"
authors: ["Knaeps", "et al."]
year: 2020
venue: "ESSD"
doi: "10.5194/essd-12-77-2020"
arxiv: null
link: "https://doi.org/10.5194/essd-12-77-2020"
tags: ["plastic", "hyperspectral", "uv-swir", "signature-library"]
relevance: "high"
status: "downloaded"
pdf: "library/plastics-uv-swir-2020.pdf"
in_slides: ["spectral-signatures"]
relates_to: []
---

## Obiettivo
Creare una libreria spettrale di riferimento per plastiche (virgin, marine-harvested, washed-ashore) in UV-VNIR-SWIR.

## Metodo
ASD FieldSpec 4 su 11 tipi di pellet vergini (PE, PP, PET, PS, PVC, HDPE, LDPE, nylon) e macro/microplastiche raccolte. 350-2500 nm.

## Risultati
Libreria spettrale pubblica (EcoSIS). Feature diagnostiche SWIR confermate: 1215, 1410, 1730 nm per C-H overtones. PET separabile via feature aromatica a 1660 nm.

## Riassunto
Riferimento fondamentale per firme spettrali di plastiche. Utilizzato per calibrare algoritmi di detection orbitale (inclusi Estrela 2025 e Uhrin 2025).

## Cosa riutilizzare (tesi)
Firme spettrali per sezione background/teoria della tesi. Endmember per eventuali esperimenti di spectral matching o simulazione di mixing.

## Note Claude
**Punti chiave**
- Libreria iperspettrale Lambertian-equivalent di plastiche misurate outdoor con ASD FieldSpec 4 in range 350-2500 nm (UV-VIS-NIR-SWIR), pubblicata open-access su EcoSIS.
- Tre famiglie campionate: macroplastiche washed-ashore (USA coast), microplastiche marine-harvested (Atlantico e Pacifico, Neuston net 335 um) sia secche sia bagnate, e 11 polimeri vergini (PVC, PA6, PA6.6, LDPE, PET, PP, PS, FEP, ABS, Merlon, PMMA).
- 8 feature di assorbimento diagnostiche identificate: ~931, 1045, 1215, 1417, 1537, 1732, 2046, 2313 nm. Di queste, 1215 e 1732 nm sono le piu' robuste per detection orbitale (fuori dalle finestre di assorbimento atmosferico H2O).
- Bagnatura attenua il segnale del 12% (UV) fino al 90% (SWIR) ma preserva la forma spettrale: spectral matching basato su shape (continuum removal, derivative, spectral angle) e' la strategia robusta.

**Figure/tabelle usabili in slide** (numero fig + cosa mostra)
- Fig. 3: firme di macroplastiche washed-ashore (8 colori, 8 grafici), con bande diagnostiche evidenziate da barre verticali grigie. Slide-ready per "ecco cosa cerchiamo nello spettro plastica".
- Fig. 4: endmember medio + std delle microplastiche dry marine-harvested. Forma rappresentativa per simulazioni di radiative transfer.
- Fig. 5a: confronto dry vs wet con assorbimento dell'acqua pura sovrapposto: spiega perche' SWIR > 1800 nm diventa quasi inutilizzabile su plastica bagnata.
- Fig. 6: firme dei pellet vergini per polimero (PA6, PA6.6, PET, ABS, PMMA, PVC, LDPE, Merlon, PS, FEP, PP): catalogo polimero-per-polimero.

**Numeri forti** (metriche concrete, # bande, GSD)
- 2151 canali a ~1 nm, 350-2500 nm. 11 polimeri vergini, ~47 particelle di microplastica caratterizzate morfometricamente (Tab. 1).
- Bande diagnostiche post-continuum-removal: 931, 1045, 1215, 1417, 1537, 1732, 2046, 2313 nm. Solo 1215 e 1732 nm in atmospheric window (~931 e ~1417 contaminate da H2O atmosferico).
- Spectral contrast angle (Theta) come metrica di similarita': very strong se Theta <= 5 deg, very weak se > 20 deg.
- Decremento di riflettanza dry->wet: ~56 +/- 23% medio.

**Limite onesto** (gap del paper — usa "generalizzazione" non "OOD")
- Misurazioni Lambertian-equivalent a 0 deg di nadir su sfondo neoprene: la generalizzazione alla scena oceanica reale richiede modelli BRDF, gestione di sub-pixel mixing con acqua, e non copre il caso di plastica sommersa (gia' a pochi cm sotto l'acqua le feature NIR/SWIR collassano). Solo macroplastica bianca dominante nei washed-ashore: bias di colore non quantificato.

**Cross-link**
- `kokaly-2017-splib07a`: stesso strumento (ASD FieldSpec) e stesso range, complementare per i polimeri non coperti da splib07a (marine-weathered).
- `emit-2025-plastic`: usa firme di questo tipo per detection floating plastic da EMIT (SWIR iperspettrale orbitale).
- `aguilar-2025-macroplastics-wv3`: traduce feature 1200/1700 nm in indici WV-3 (band 7/8 SWIR), il bridge naturale dalla libreria al sensore.
- `marida-2022-marine-debris`: dataset Sentinel-2 di marine debris dove queste firme spiegano la separabilita' (o la mancanza, per via della GSD a 10-20 m).
- `zhou-2021-plastic-classifier`: classifier su firme di plastica simili, complementare per la parte ML.
