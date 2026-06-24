---
id: "global-dumpsites-2023"
title: "Revealing influencing factors on global waste distribution via deep-learning based dumpsite detection from satellite imagery"
authors: ["(unknown)"]
year: 2023
venue: "Nature Comms"
doi: "10.1038/s41467-023-37136-1"
arxiv: null
link: "https://doi.org/10.1038/s41467-023-37136-1"
tags: ["waste", "global", "deep-learning", "dumpsites"]
relevance: "high"
status: "downloaded"
pdf: "library/global-dumpsites-2023.pdf"
in_slides: ["low-res-survey"]
relates_to: []
---

## Obiettivo
Rilevare discariche globali da immagini VHR con DL e analizzare i fattori socioeconomici che ne influenzano la distribuzione.

## Metodo
Deep CNN su immagini VHR RGB in 28 città (Asia, Africa, Europa, Americhe). Correlazione con indicatori socioeconomici (GDP, densità, governance).

## Risultati
~1.000 discariche rilevate in 28 città. Riduzione del tempo di investigazione del 96.8% rispetto a ispezione manuale. Correlazione significativa con governance e gestione urbana.

## Riassunto
Peer di Gibellini su scala globale. Dimostra la scalabilità dell'approccio DL per waste detection e fornisce un riferimento quantitativo per il risparmio di tempo operativo.

## Cosa riutilizzare (tesi)
Argomento a supporto dell'utilità operativa della tesi. Evidenza che il DL su imagery RGB funziona a scala globale, motivando l'estensione MS come passo successivo.

## Note Claude
**Punti chiave**
- Sun et al. (Nature Communications 2023) costruiscono il primo dataset globale fine-grained di discariche su immagini satellitari VHR (0.3-1 m/px), classificate in 4 tipologie: Domestic, Construction, Agricultural, Covered Waste. Circa 4.800 km^2 etichettati a mano su 2.500 discariche in 7 paesi (Cina, India, Bangladesh, Sri Lanka, Congo, Nigeria, Germania).
- Propongono BCA-Net (Blocked Channel Attention Network), modulo attention su Faster R-CNN+FPN+ResNet50 che blocca i feature channel in regioni e impara importanza differenziata per regione — risolve la confusione tra discariche di forma irregolare e sfondi simili (parcheggi, tetti, rocce).
- Analisi spaziale su 28 città mondiali con Global Dumpsite Index (GDI = log2 N): correlazione Spearman con 18 attributi sociali (GNI 0.538**, sanitation 0.487**, urbanizzazione 0.418*, latitudine assoluta -0.424*, paese sviluppato -0.554**).

**Figure/tabelle usabili in slide**
- Fig. 1d: griglia di esempi VHR delle 4 tipologie (Agricultural/Construction/Covered/Domestic) — illustra che la classificazione per rischio richiede risoluzione sub-metrica e non funziona a 10-30 m.
- Fig. 2 a-c: foto reale a terra + CAM dell'attivazione del modello su una discarica domestica a Pechino — slide #7 per spiegare cosa il modello BECCA su VHR.
- Fig. 3 a-b: mappa GDI mondiale con coppie città avanzate/ordinarie e barplot GDI per tipologia — slide #8 per evidenziare il gap di copertura globale.
- Fig. 5: serie temporale 2015-2019 di 4 discariche (demolizione->green belt->ufficio) — mostra il "change detection" che a 10 m non sarebbe visibile.

**Numeri forti**
- Sensitivity media 98.0% (Domestic 0.975, Construction 0.982, Covered 0.991, Agricultural 0.973). Precisione media 70.1% (Covered 0.967, Domestic 0.680).
- 763 vs 755 discariche su 28 città di test (98.6% recall vs ground truth manuale). Investigazione automatica in 6 giorni vs 6 mesi manuali (-96.8% tempo).
- GSD imagery 0.3-1 m/px, tile 1024x1024 ~614x614 m^2. k-fold k=5, batch 8 NVIDIA RTX3090.

**Limite onesto**
- La precisione resta bassa (~70%) perche a 0.3-1 m si vedono macro-caratteristiche ma non la composizione materiale: il modello non distingue plastica da rifiuto edile per firma spettrale, solo per pattern morfologico — quindi non puo classificare per rischio chimico/sanitario. Inoltre il dataset e geograficamente sbilanciato (Cina sovra-rappresentata), riducendo la generalizzazione a contesti europei o americani.

**Cross-link**
- `torres-2023-aerialwaste`: stesso approccio CNN ma su dataset italiano aereo a 20-50 cm; global-dumpsites e la versione globale a basso costo, AerialWaste il riferimento high-quality regionale.
- `gibellini-2025-pipeline`: pipeline Swin-T che porta la baseline di torres su AerialWaste; global-dumpsites mostra il "scale up" globale.
- `marida-2022-marine-debris`: complementare acqua/terra — entrambi RGB/MS ma global-dumpsites a sub-metrica trova oggetti che a 10 m S2 non si vedrebbero.
- `tisza-2023-waste-change`: change detection ma con MS a 10 m, qui invece change detection con VHR temporale.
