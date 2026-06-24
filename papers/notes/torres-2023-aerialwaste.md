---
id: "torres-2023-aerialwaste"
title: "AerialWaste: A dataset for illegal landfill discovery in aerial images"
authors: ["Torres", "Fraternali"]
year: 2023
venue: "Scientific Data"
doi: "10.1038/s41597-023-01976-9"
arxiv: null
link: "https://doi.org/10.1038/s41597-023-01976-9"
tags: ["waste", "dataset", "aerialwaste"]
relevance: "critical"
status: "downloaded"
pdf: "library/torres-2023-aerialwaste.pdf"
in_slides: ["dataset"]
relates_to: []
---

## Obiettivo
Creare un dataset benchmark annotato per la detection di discariche illegali da immagini aeree.

## Metodo
Raccolta da 3 sorgenti (AGEA, WV3, Google Earth). Annotazioni a 3 livelli: binary, 22 classi materiale, segmentation masks (169 imgs).

## Risultati
10.434 immagini (v3: 11.700+), rapporto neg:pos = 2:1. 22 categorie di materiale. Disponibile su Zenodo.

## Riassunto
Dataset di riferimento per waste detection da RS. RGB-only, tre sorgenti a GSD diversi. Le coordinate sono withholded dagli autori.

## Cosa riutilizzare (tesi)
Dataset per baseline e esperimenti. Le 22 classi materiale per la classificazione multi-class. Serve accordo per le coordinate.

## Note Claude
### torres-2023-aerialwaste
**Punti chiave** (3-5 bullet):
- Primo dataset pubblico per illegal landfill discovery in aerial imagery: 10.434 immagini (3.478 pos + 6.956 neg), MS COCO format, su Zenodo via aerialwaste.org.
- 3 sorgenti eterogenee: AGEA ortofoto 20 cm (~1100 pos), WV-3 30 cm (~250 pos, pansharpened RGB), Google Earth 50 cm (~2200 pos). Tutte RGB.
- Tre livelli annotazione: (1) binary scene classification, (2) multi-label su 22 categorie Type of Object (TO) + 7 Storage Mode (SM), (3) 169 immagini test con segmentation masks (841 maschere su 9 classi).
- Costruito con ARPA Lombardia su 487 comuni: 33% siti reali (waste-confirmed), 67% sampling random a 1-5 km dai positivi - rispetta strategia neg:pos = 2:1 per emulare class imbalance reale.
- Metadati ricchi (evidence 0-3, severity 0-3, area type) presenti su ~72% dei positivi ma non usati nel training, disponibili per analisi downstream.

**Figure/tabelle usabili in slide**:
- Fig. 1: workflow creazione dataset (esperti ARPA → location DB → tile da 3 sorgenti → annotazioni ODIN)
- Fig. 3 + Fig. 6: esempi positivi per WV3/AGEA/GE - mostra diversita visiva
- Fig. 4: distribuzione pos/neg per sorgente (Google Earth dominante)
- Tab. 1: 22 TO + 7 SM con conteggi (Rubble 294, Bulky 286, Fire wood 173, Scrap 167, Plastic 126, **Corrugated sheets/presumed asbestos 11**)
- Fig. 5: distribuzione evidence/severity/area type
- Fig. 10: F1 baseline ResNet50+FPN per sorgente (AGEA 0.82, WV3 0.75, GE 0.80)
- Fig. 12: CAM examples per i tre sorgenti

**Numeri forti da citare**:
- 11.700+ tiles totali nella v3 (paper originale: 10.434 v1)
- Baseline ResNet50+FPN: 87.99% AP, 80.70% F1 (precision 81.89%, recall 79.54%) su test set completo; 94.5% AP / 88.2% F1 su solo AGEA (qualita alta omogenea)
- 169 immagini con segmentation masks, 841 maschere totali su 9 classi
- Pilot ARPA: 69 siti scanned, 50% confidence > 0.75, avg 0.66
- Solo 11 immagini con corrugated sheets presumed asbestos (rilevante per pilot Fase 1)

**Limite onesto (gap che lasciano):**
- RGB-only su 3 sorgenti a GSD differenti (20/30/50 cm) = mismatch spettrale - il dataset non puo essere usato per testare il "valore aggiunto MS vs RGB" su cui si fonda la tesi. I planned extensions (sezione Usage Notes) menzionano esplicitamente "Multi-modal imagery: AerialWaste contains only RGB images. Addition of NIR could help via stressed vegetation" = gap dichiarato dagli autori.
- Coordinate withheld per riservatezza ARPA, limitando re-acquisizione MS sugli stessi siti senza accordo.
- Geografia ristretta (Lombardia): selection bias riconosciuto, classificazione per rischio cross-region non valutata.

**Cross-link**: dataset usato da gibellini-2025-pipeline (la sua baseline + ablation). Citato in fraternali-2024-survey come unico dataset italiano e in global-dumpsites-2023 come benchmark di confronto. Riferimento per tisza-2023-waste-change (S2 change detection complementare). Per estensione MS guardare wang-2023-ssl4eo-s12, cong-2022-satmae, xiong-2024-dofa.
