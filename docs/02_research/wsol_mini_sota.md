# WSOL mini-SOTA — weakly-supervised waste localization under GSD degradation

Data: 2026-07-21. Time-boxed (~20 min). Fonti: repo locale + Mazzola PDF + web (9 ricerche).
Ogni claim marcato [fatto] (verificato su fonte) o [inferenza].

## 1. Domanda del documento

Il claim di novelty "weakly-supervised waste localization under GSD degradation"
(localizzare discariche da label binarie image-level e misurare quantitativamente
come la localizzazione degrada da 0.3 m a 1.2 m di GSD) regge alla letteratura
2020-2026 e ai lavori interni al gruppo (Mazzola, Gibellini, Sun)?

## 2. WSOL in 10 righe

WSOL (weakly-supervised object localization) = localizzare oggetti usando solo
label image-level, senza box o maschere in training. Il metodo base è la CAM
(class activation map) e le varianti Grad-CAM, Grad-CAM++, LayerCAM: la heatmap
del classifier viene sogliata e convertita in box o maschera. Limite noto: la CAM
copre solo le parti discriminative dell'oggetto, non tutta la sua estensione.
La valutazione standard (Choe et al. 2020, poi TPAMI 2023) usa GT-known metrics:
MaxBoxAcc (IoU box predetta vs GT >= 0.5), MaxBoxAccV2 (media su soglie IoU
0.3/0.5/0.7), pointing game (il massimo della heatmap cade dentro il GT), oppure
PxAP se esistono maschere. In remote sensing il WSOL è attivo (survey del gruppo
Fraternali 2022; benchmark dedicati C45V2 e PN2 dal 2023) ma la valutazione resta
per lo più a GSD fisso; l'asse risoluzione non è un asse di studio. [fatto]

## 3. Lavori chiave (verificati)

| Paper | Anno | Task | Dominio | Metodo | Eval localizzazione |
|---|---|---|---|---|---|
| Choe et al., Evaluating WSOL Methods Right (CVPR; est. TPAMI 2023) | 2020 | WSOL protocol | Natural images | Protocollo + benchmark | MaxBoxAcc, MaxBoxAccV2, PxAP |
| Zhang et al., WSOL and Detection: A Survey (TPAMI) | 2021 | Survey WSOL/WSOD | Natural + RS | Rassegna CAM-based | Top-1 Loc, GT-known, CorLoc |
| Fasana, Pasini, Milani, Fraternali, WSOD for RSI: A Survey (Remote Sensing) | 2022 | Survey WSOD | Remote sensing | Rassegna (survey del gruppo) | mAP, CorLoc |
| Object Localization in Weakly Labeled RSI via Deep Conv Features (Remote Sensing) | 2022 | WSOL a punti | Remote sensing | Feature conv + label image-level | Localizzazione (x,y), point-based |
| Bai, Ren et al., Localizing From Classification: Self-Directed WSOL for RSI (IEEE, Xplore 10242056) | 2023 | WSOL | Remote sensing | Grad-CAM++ guida una self-directed loss | Benchmark nuovi C45V2, PN2 |
| Sun et al., Global dumpsite detection (Nature Communications) | 2023 | Detection siti rifiuti | Satellite globale | Deep detection; CAM mostrate | Qualitativa (CAM illustrative) [fatto, da repo] |
| Torres, Fraternali, AerialWaste (Scientific Data) | 2023 | Dataset discariche | Aereo + satellite | 169 img test con maschere (841 poligoni) per WSL | Nessuna metrica riportata; CAM qualitative |
| Mazzola (tesi PoliMi, corr. Gibellini) | 2024 | Classif. binaria asbestos | WV-3 + Pléiades Neo MS | CNN + Grad-CAM, WSL | IoU box predetta vs GT (quantitativa) |
| SAM-Induced Pseudo Fully Supervised WSOD (Remote Sensing) | 2024 | WSOD | Remote sensing | Pseudo-label da SAM + detector | mAP, CorLoc |
| Gibellini et al., Solid Waste Detection in RSI: A Case Study (arXiv 2502.06607) | 2025 | Classif. binaria rifiuti | Aereo (+ satellite) | Pipeline tile -> classifier -> Grad-CAM -> GIS | Qualitativa; ablation GSD 20/30/50 cm solo su classificazione [fatto, da repo] |

## 4. Mazzola 2024: cosa fa e cosa non fa

Fonte: `asbestos/reference/Mazzola_2024_Thesis.pdf` (PoliMi 2023-2024, adv. Fraternali, corr. Gibellini).

Cosa fa [fatto, dal PDF]:
- Classificazione binaria asbestos su WV-3 + Pléiades Neo pansharpened (0.3 m), CNN ImageNet (EfficientNetB0, ResNet50, InceptionV3), RGB vs MS.
- WSL quantitativa: "to quantitatively evaluate localization performance, we calculated the Intersection over Union (IoU) metric ... between the predicted and ground truth bounding boxes" (Sez. 4.1). IoU compare come colonna nelle tabelle risultati; MS batte RGB di ~4 punti IoU (EfficientNetB0 su Pléiades Neo).
- Confronto risoluzione (Sez. 4.3): MS pansharpened 0.3 m vs MS nativo 1.2 m, con Precision/Recall/IoU migliori a 0.3 m.
- Grad-CAM definita "qualitative study" per interpretabilità e shortcut learning; shift robustness sugli input.

Cosa non fa [fatto, assenza verificata nel PDF]:
- Nessun protocollo WSOL standard: niente MaxBoxAcc, niente pointing game, niente analisi per soglia CAM; il testo non descrive come si estrae la bounding box predetta dalla heatmap.
- Il confronto 0.3 vs 1.2 m è pansharpened-vs-nativo (2 soli punti, con il confound del pansharpening), non una degradazione controllata di GSD sulla stessa immagine; e l'asse risoluzione è letto soprattutto sulle metriche di classificazione.
- Task diverso: tetti in asbestos (oggetto compatto, GT poligonale regionale), non discariche (oggetto diffuso, multi-materiale).
- Nessun metodo oltre vanilla Grad-CAM (nessun refinement, nessuna pseudo-mask, nessuna consistency cross-risoluzione).

## 5. Verdetto

**Novel con condizioni.** To our knowledge, nessuno studio valuta quantitativamente
la localizzazione weakly-supervised sotto degradazione controllata di risoluzione/GSD
in remote sensing: 3 ricerche mirate (CAM + resolution degradation, WSOL + GSD,
WSOL low-resolution) non hanno trovato alcun lavoro del genere, né in RS né in
computer vision generale [fatto, assenza nei risultati; resta inferenza sull'inesistenza].
L'incrocio "WSOL quantitativo x asse GSD x waste" appare libero.

Ma i singoli ingredienti non sono nuovi, quindi il claim regge solo con questi delta espliciti:
1. **Delta vs Mazzola (obbligatorio, competitor interno):** task waste (non asbestos);
   protocollo WSOL standard e riproducibile (MaxBoxAcc/V2, pointing game, curve per
   soglia CAM) al posto di una singola colonna IoU non documentata; degradazione GSD
   controllata multi-punto (stessa immagine ricampionata) al posto del confronto a 2
   punti pansharpened-vs-nativo; metodo oltre vanilla Grad-CAM.
2. **Delta vs Gibellini 2025:** la sua ablation GSD (20/30/50 cm, aereo) misura solo
   la classificazione; qui si misura la localizzazione, su satellite.
3. **Delta vs AerialWaste/Sun:** loro CAM qualitative; qui valutazione quantitativa.
4. **Delta vs WSOL-RS (Bai 2023 ecc.):** loro migliorano la CAM a GSD fisso; qui
   l'asse di studio è la robustezza della localizzazione al GSD.

Condizioni di fattibilità: già soddisfatte in larga parte [fatto, da EDA]: esistono
2827 bounding box object-level su 286 immagini positive del dataset satellite-only
(`aw36_od_bin_sat_only.json`) e split pronti a 0.3 m e 1.2 m. La valutazione
bbox-based (MaxBoxAcc, pointing game, box IoU) è possibile con dati esistenti,
senza campagna di annotazione. La gating question del piano 7 punti è quindi
sostanzialmente chiusa per la via bbox [inferenza: resta da verificare la qualità
delle box e la loro copertura del test set].

Rischio residuo [inferenza]: la commissione può leggere "estensione di Mazzola a
un altro materiale" se i delta 1-4 non sono dichiarati e misurati; il metodo oltre
vanilla CAM (pseudo-mask refinement o consistency cross-GSD) resta necessario
perché il solo asse di valutazione potrebbe non bastare come contributo.

## 6. Riferimenti

- Evaluating Weakly Supervised Object Localization Methods Right, 2020, CVPR (estensione TPAMI 2023).
- Weakly Supervised Object Localization and Detection: A Survey, 2021, IEEE TPAMI.
- Weakly Supervised Object Detection for Remote Sensing Images: A Survey, 2022, Remote Sensing (MDPI).
- Object Localization in Weakly Labeled Remote Sensing Images Based on Deep Convolutional Features, 2022, Remote Sensing (MDPI).
- Localizing From Classification: Self-Directed WSOL for Remote Sensing Images, 2023, IEEE (Xplore 10242056).
- Revealing influencing factors on global waste distribution via deep-learning based dumpsite detection, 2023, Nature Communications.
- AerialWaste dataset for landfill discovery in aerial and satellite images, 2023, Scientific Data.
- Mazzola, Deep Learning approaches for asbestos classification via Multispectral Satellite Images, 2024, tesi PoliMi (politesi 10589/230433).
- SAM-Induced Pseudo Fully Supervised Learning for WSOD in Remote Sensing Images, 2024, Remote Sensing (MDPI).
- Solid Waste Detection in Remote Sensing Images: A Case Study, 2025, arXiv 2502.06607.
- A Realistic Protocol for Evaluation of Weakly Supervised Object Localization, 2024, arXiv 2404.10034.
