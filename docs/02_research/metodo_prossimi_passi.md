# Metodo — prossimi passi dopo EXP-008

Data: 2026-07-23. Ricerca web time-boxed (~25 min, 9 ricerche) sui metodi per mappe di
localizzazione ad alta risoluzione da label image-level. Complementare a `wsol_mini_sota.md`.
Ogni claim marcato [fatto] (verificato su fonte) o [inferenza].

## 1. Il requisito (da EXP-008)

Gli oggetti annotati hanno lato mediano 27 px a 0.3 m (~8 m); il 99% sta sotto una cella
della griglia 7×7 [fatto, EXP-008]. L'oracolo mostra che una CAM perfetta a 7×7 dà pointing
game 0.06 (= il nostro reale), a 28×28 dà 0.86 [fatto, EXP-008]. Quindi il collo di bottiglia
è la risoluzione della mappa, non la qualità della CAM. Requisito: mappe di localizzazione
ad almeno 28×28 nello spazio dell'annotazione, meglio pixel-level, ottenute da sole label
image-level. Vincoli: 1020 immagini di training, Swin-T + RSP, 1 GPU (98 GB), 351 bbox di test.

## 2. Tabella opzioni metodo

Ordinata per rapporto valore/costo nel nostro contesto (costi in giorni = [inferenza]).

| # | Opzione | Idea in una frase | Risoluzione mappa | Costo | Rischio | Fonti verificate |
|---|---|---|---|---|---|---|
| 1 | Input ad alta risoluzione + CAM stage-3 | Alzare l'input da 224 a 448/704 px: la griglia Swin cresce in proporzione, gli oggetti tornano sopra la cella | 28×28 (448) fino a 44×44 (704) | 1-2 gg | Basso: solo compute (~10× token a 704) e riadatto del resize | Aritmetica Swin [fatto, sotto]; nessun metodo nuovo |
| 2 | SAM come refiner (picco CAM → prompt → maschera) | I massimi locali della CAM diventano point-prompt per SAM, che restituisce maschere pixel-level senza training | Pixel-level | 2-3 gg | Medio: SAM debole su oggetti piccoli (~12-27 px) e su tessiture omogenee | Chen 2023 (arXiv 2305.05803); Qian 2024 (RS 16:1532); Osco 2023; SOPSeg 2025 |
| 3 | Consistency cross-GSD a stage-3 (EXP-007 riposizionato) | Regolarizzare la coerenza delle mappe 0.3 m vs 1.2 m, ma sulla griglia 14×14+ dove il tetto lo consente | 14×14–44×44 (dipende da #1) | in corso +1-2 gg | Medio: a 7×7 non può alzare i numeri (EXP-008); prior art da citare | SEAM (CVPR 2020); SSENet (arXiv 2019); SAN (RS 2025) |
| 4 | Self-training con decoder leggero | Le pseudo-maschere (da #1/#2) allenano una testa di segmentazione sul backbone: mappa densa a inference | Pixel-level | 3-5 gg | Medio: dipende dalla qualità delle pseudo-maschere a monte | Prassi WSSS multi-stage (pipeline PSA/IRNet) |
| 5 | Affinity propagation (PSA / IRNet) | Una rete impara le affinità tra pixel dalle zone confidenti della CAM e propaga il seed con random walk | Pixel-level | 4-7 gg | Medio-alto: pipeline a 2-3 stadi tarata su PASCAL (~10k img); con 1020 img esito incerto [inferenza] | Ahn 2018 (CVPR); Ahn 2019 (CVPR) |
| 6 | Fusione CAM multi-livello (UM-CAM-style) | Fondere CAM di stage diversi pesate per incertezza | Intermedia (fino a 56×56) | 1-2 gg | Valore basso qui: EXP-006 mostra che LayerCAM/fusioni non aiutano su questo task [fatto] | UM-CAM (Pattern Recognition 2024) |
| 7 | Token contrast (ToCo) | Contrasto tra token di layer intermedi e finali per CAM più complete su ViT | Patch-level (16×16 su ViT) | 5-8 gg | Alto: pensato per ViT plain con class token, non Swin; cambio backbone | Ru 2023 (CVPR) |

Aritmetica Swin [fatto]: stride degli stage = 4/8/16/32. Input 224 → stage-3 14×14, stage-4 7×7.
Input 448 → 28×28 / 14×14. Input 704 (700 nativi + pad) → 44×44 / 22×22. Token a 704 ≈ 9.9×
quelli a 224; con window attention il costo cresce ~linearmente → fattibile su 98 GB con batch
ridotto [inferenza]. Nota: oggi il resize 700→224 riduce l'oggetto mediano da 27 a ~9 px; a
input pieno resta 27 px, cioè ~1.7 celle a stride 16. L'opzione 1 attacca il tetto direttamente.

Su SAM e oggetti piccoli [fatto, da valutazioni pubblicate]: le valutazioni di SAM su remote
sensing riportano degrado marcato su oggetti piccoli o a basso contrasto; a 24 cm GSD auto da
~12×12 px vengono fuse in un'unica maschera. SOPSeg (2025) lo mitiga con ritaglio e ingrandimento
adattivo della regione prima del prompt. Per noi: prompt su crop ingrandito attorno al picco CAM,
non sull'intera tile [inferenza]. Pesi SAM pubblici (repo facebookresearch/segment-anything,
checkpoint ViT-B/L/H scaricabili) [fatto].

Valutazione a livello di sito: nessun protocollo standard trovato per aggregare box vicine in
"siti" ai fini della metrica [inferenza, assenza nei risultati]. Sun 2023 (Nature Comm.) lavora
per dumpsite ma con valutazione qualitativa delle CAM [fatto, da mini-SOTA]. Se serve, va
proposta come scelta di protocollo nostra (union di box dilatate), dichiarata e motivata.

## 3. Tre raccomandazioni operative (7-10 giorni)

1. **Input ad alta risoluzione (opzione 1) — primo esperimento subito.**
   Passo A (mezza giornata): inference-only, checkpoint esistenti, input 448 e 704, CAM da
   stage-3/4, stessa pipeline metrica di EXP-005. Swin accetta input più grandi interpolando
   il relative position bias [fatto, proprietà nota di Swin]. Misura: pointing game e IoU vs
   tetto oracolo 28×28 (0.86 / 0.61). Passo B (1-2 giorni GPU): retrain a 448 (6 bande, 0.3 m,
   seed 42) se il passo A mostra segnale. Dati/pesi: già tutti disponibili.

2. **SAM come refiner delle CAM migliori (opzione 2) — offline, senza training.**
   Scaricare i pesi SAM (ViT-B per iterare, ViT-H per il run finale). Sulle 50 immagini di
   EXP-005: top-k massimi locali di gradcam_s3 6 bande 0.3 m (la migliore, IoU 0.143) → point
   prompt su crop ingrandito → maschere → stessa metrica. Misura: quanto le pseudo-maschere
   superano la CAM sogliata; soglia di decisione per usarle nel self-training (opzione 4).
   Rischio noto: oggetti da 27 px al limite delle capacità di SAM; il crop ingrandito è la
   mitigazione da provare per prima.

3. **Riposizionare EXP-007 sulla griglia giusta e chiudere la lettura.**
   Rileggere i risultati di EXP-007 con il tetto di EXP-008: a 7×7 la consistency non può
   alzare i numeri assoluti [fatto, EXP-008]. Se si ri-lancia, applicare la loss di consistency
   alle mappe stage-3 (o a input 448) e valutare con lo stesso protocollo. Misura: delta di
   pointing game/IoU a 0.3 m e a 1.2 m rispetto al retrain liscio della raccomandazione 1.
   In scrittura, citare SEAM/SSENet/SAN come prior art della consistency e differenziare (sotto).

Sequenza: 1A → (1B e 2 in parallelo) → 3; l'opzione 4 (self-training) parte solo se 1 o 2
producono pseudo-maschere sopra la CAM sogliata.

## 4. Posizionamento di EXP-007 (consistency cross-GSD) vs prior art

Prior art trovato, da citare:
- L'idea "coerenza delle CAM tra versioni ri-scalate della stessa immagine" esiste dal 2019-2020:
  SSENet (equivarianza alla scala) e SEAM (equivarianza ad affini + pixel correlation), entrambe
  come regolarizzazione siamese per WSSS su immagini naturali [fatto].
- In remote sensing, SAN (Remote Sensing 2025) usa una siamese con trasformazioni affini per la
  consistency delle CAM, più SAM per raffinare i seed [fatto]. È il lavoro più vicino al nostro.
- In detection fully-supervised esiste la distillazione cross-risoluzione (teacher ad alta
  risoluzione → student a bassa), es. Multi-Scale Aligned Distillation, 2021 [fatto].
- Scale-MAE (ICCV 2023) rende il GSD un asse esplicito del pretraining (positional encoding
  GSD-aware), ma è self-supervised pretraining, non localizzazione weakly-supervised [fatto].

Verdetto: il claim "consistency per la localizzazione weakly-supervised" da solo NON è nuovo.
La differenza difendibile resta su tre punti [inferenza, su assenze verificate]:
(a) il prior art usa resize sintetici della stessa immagine a GSD fisso (il contenuto informativo
non cambia); noi imponiamo coerenza tra acquisizioni a GSD reale diverso (0.3 vs 1.2 m), dove
il degrado informativo è reale; (b) l'obiettivo del prior art è migliorare la CAM a risoluzione
fissa, il nostro è anche misurare la robustezza della localizzazione lungo l'asse GSD, che
nessun lavoro trovato misura (confermato il verdetto del mini-SOTA: nessun controesempio emerso
in queste 9 ricerche); (c) dominio waste + protocollo quantitativo. In scrittura: presentare
EXP-007 come adattamento della regolarizzazione di equivarianza (SEAM/SSENet) all'asse GSD,
non come invenzione della consistency. Conseguenza pratica da EXP-008: ha senso solo su mappe
a 14×14 o più fini.

## 5. Riferimenti verificati

- Learning Pixel-level Semantic Affinity with Image-level Supervision for WSSS (PSA), 2018, CVPR.
- Weakly Supervised Learning of Instance Segmentation with Inter-pixel Relations (IRNet), 2019, CVPR (oral).
- Self-supervised Scale Equivariant Network for WSSS (SSENet), 2019, arXiv 1909.03714.
- Self-supervised Equivariant Attention Mechanism for WSSS (SEAM), 2020, CVPR (oral).
- Token Contrast for Weakly-Supervised Semantic Segmentation (ToCo), 2023, CVPR.
- Segment Anything Model (SAM) Enhanced Pseudo Labels for WSSS, 2023, arXiv 2305.05803.
- The Segment Anything Model (SAM) for remote sensing applications: from zero to one shot, 2023, Int. J. Appl. Earth Obs. Geoinf. (arXiv 2306.16623).
- Scale-MAE: A Scale-Aware Masked Autoencoder for Multiscale Geospatial Representation Learning, 2023, ICCV.
- SAM-Induced Pseudo Fully Supervised Learning for WSOD in Remote Sensing Images, 2024, Remote Sensing (MDPI) 16(9):1532.
- UM-CAM: Uncertainty-weighted Multi-resolution CAM for weakly-supervised segmentation, 2024, Pattern Recognition.
- Weakly Supervised Semantic Segmentation of Remote Sensing Images Using Siamese Affinity Network (SAN), 2025, Remote Sensing (MDPI) 17(5):808.
- SOPSeg: Prompt-based Small Object Instance Segmentation in Remote Sensing Imagery, 2025, arXiv 2509.03002.
- Multi-Scale Aligned Distillation for Low-Resolution Detection, 2021, arXiv 2109.06875.
- Segment Anything (repo facebookresearch/segment-anything, checkpoint pubblici ViT-B/L/H), 2023.
