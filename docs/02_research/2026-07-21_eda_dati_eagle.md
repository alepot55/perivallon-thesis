# Cosa c'è sul server eagle — ricognizione dati (2026-07-21)

Prima esplorazione di `/data` e `/archive` sul container `multispectralwaste`, fatta in sola lettura la sera del 21/7.
Serve per arrivare preparati alla call con Enrico. Tutto verificato aprendo i file; le voci [inferenza] vanno confermate in call.

## La scoperta principale

Il dataset per la tesi esiste già, ed è già impostato per l'asse risoluzione:

```
/data/waste/datasets/SatRaw/PNEO/Thomas/
├── 0.3m/binary/   train.json (1020 img) + val.json (135) + test.json (139) + splits.geojson
└── 1.2m/binary/   stessi identici split, stesse immagini, risoluzione degradata
```

- 1.294 immagini PNEO totali, ~50% positive nel train (508/1020).
- Ogni record ha: `file_name` (es. `Agrate-Brianza_7875_0.tif`), `categories`, `annotations`, `severity` (1-3), `site_type`, `evidence`, `geometry` (footprint georeferenziato del tile).
- [inferenza] "Thomas" nel path = preparato da Thomas; è il punto di partenza naturale per la replica baseline e la griglia di risoluzione. La risoluzione ~0.7 m intermedia non c'è ancora.

## La risposta (parziale) alla domanda gating sui poligoni

In `/data/waste/datasets/AerialWaste3.6/prod/gt/`:

| File | Contenuto |
|---|---|
| `aw36_od_bin_sat_only.json/.geojson` | 1.775 immagini satellite-only (1.294 PNEO + 481 WV3), footprint georeferenziati |
| di cui positive | **286 immagini con 2.827 bounding box a livello di oggetto, 15 categorie di materiale** |
| `aw36_od_bin.json` | inventario completo: 12.997 immagini con gli stessi metadati |

Le annotazioni sono bbox COCO-style (`bbox: [x, y, w, h]`), niente maschere di segmentazione (conferma del "no segmentation masks exist" del deck v7). Ma per la valutazione WSOL le bbox bastano: le metriche standard (MaxBoxAcc, box IoU, pointing game) usano proprio le bbox. Quindi il test-set di localizzazione in gran parte c'è già; resta da capire con Enrico se le 2.827 bbox sono complete e affidabili.

Le 15 categorie: Rubble, Scrap, Sludge-Zootechnical-Manure, Foundry waste-Asphalt milling, Fire wood, Other wood, Bulky items, Tanks, Big bags, Plastic, Vehicles, Tires, Containers, Asbestos, Unknown material. I mapping in `AerialWaste3.6/mappings/` (m1..m6) le raggruppano a vari livelli, fino al codice EWC (European Waste Catalogue).

## Le immagini

- Tile PNEO multispettrali: **6 bande, uint16, EPSG:32632** (esempio: 176x176 px a 1.2 m). Quindi il VNIR completo di Pléiades Neo c'è, non solo RGB.
- `SatRaw/ssl/tiles/`: 1.948 tile MS con relativo `tiles_all_MS.geojson` — [inferenza] il materiale usato per il pretraining SSL del gruppo.
- `/archive/satellite/raw` e `processed`: decine di strip Lombardia (e Grecia/Spagna), naming `SENSORE_AREA_DATA_BANDE_GSD_bit_FONTE`, es. `WV3_ENDINE_20250619_VNIR_30cm_16bit_MAXAR`, `PNEO_LOMBARDIA_2023_ALL_30cm_16bit_THOMAS`, più SkySat 50 cm. Le fonti per estendere il dataset (le ~800 WorldView attese) stanno qui.
- `AerialWaste3.6/images` è un symlink ad AerialWaste3.5 (14.388 png): la 3.6 riorganizza annotazioni e split senza duplicare le immagini. Split geografici per comune (`splits/training_munics.json` / `testing_munics.json`).

## I pesi SSL in-house

`/data/waste/multilabel/SSL_pretrained_models/exported_last_{100,500}_ep.pt`: **ResNet-50, input a 3 canali RGB** (conv1 64x3x7x7), 320 tensori, formato torchvision. Due export a 100 e 500 epoche.

- Nota per la tesi: sono RGB, non multispettrali; e sono ResNet-50, non Swin-T. [inferenza] Il "FM in-house in preparazione" di cui parlava la call potrebbe essere altro; questi sembrano un SSL pretraining già concluso. Da chiarire con Enrico.

## Contorno utile

- `/data/waste/risk/`: layer GIS per il risk assessment ARPA — DUSAF (land use), aree protette, fiumi, strade, Istat, e `siti_critici/` con i punti ARPA 2021-2023 (es. 2023: 501 punti, con provincia, comune, analista, stato attività). Punti, non poligoni: utili come controllo esterno o per pointing-game, non come maschere.
- `/data/waste/` ha anche: `satellite-pipeline/` (GIS, inference, poc — [inferenza] la pipeline di produzione), `change_detection/`, `multimodal/`, `object_detection/`, `volume-estimation/`, `synthetic/`.
- `/data/waste/multilabel/`: il lavoro material classification — `alari/` (code + data), `fede_faspas_replic/`, esperimenti 100/210.

## Domande per Enrico, aggiornate dopo l'EDA

1. Le 2.827 bbox sulle 286 positive satellite-only: chi le ha fatte, sono complete, si può usarle come test-set di localizzazione?
2. `Thomas/0.3m` e `1.2m`: è la configurazione ufficiale degli esperimenti? Esiste già una run baseline con numeri su questi split?
3. Il livello ~0.7 m manca: lo generiamo noi col degrado da 0.3 m? Con che metodo (resampling scelto)?
4. I due export SSL ResNet-50 RGB: che training è (metodo, dati), e che rapporto ha col "FM in-house" annunciato?
5. Le 6 bande PNEO: gli esperimenti finora usano RGB o tutte le bande? Il pansharpening a 0.3 m com'è fatto?
6. Le ~800 WorldView in arrivo: sono le 481 già in `sat_only` più altre, o nuove?
7. Negative sampling: come sono state scelte le 512 negative del train?

## Cheat sheet path

| Cosa | Path |
|---|---|
| Dataset tesi (split per risoluzione) | `/data/waste/datasets/SatRaw/PNEO/Thomas/{0.3m,1.2m}/binary/` |
| GT satellite-only con bbox | `/data/waste/datasets/AerialWaste3.6/prod/gt/aw36_od_bin_sat_only.json` |
| Tile MS per SSL | `/data/waste/datasets/SatRaw/ssl/tiles/` |
| Pesi SSL in-house | `/data/waste/multilabel/SSL_pretrained_models/` |
| Strip satellitari sorgente | `/archive/satellite/{raw,processed}/` |
| Layer risk ARPA | `/data/waste/risk/` |
