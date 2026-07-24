# Call 2026-07-24 — Enrico + Thomas: codice, dataset, regole operative

Partecipanti: Ale, Thomas, Enrico. Fonte: trascrizione STT + screenshot (repo VS Code, Excel Drive). Nomi propri STT verificati.

## Fatti — dataset e piano esperimenti (Thomas)

- Piano esperimenti di Thomas in un PDF su Drive: asse risoluzione su tre livelli GSD.
- **120 cm: dataset PRONTO** — si parte da qui. Razionale: IRIDE (~1 m).
- **30 cm: in preparazione** (stanno pansharpenando le immagini), pronto ~settimana prossima; **Thomas avvisa lui** quando c'è.
- **60 cm: lo deriviamo NOI** aggregando i pixel (es. 2×2 → 1; media o massimo — "non inventare la ruota, vedi cosa suggeriscono"). Razionale: ≈ SkySat (50 cm).
- **SSL pretraining in corso nel gruppo** per avere pesi su tutte le bande ("a certe risoluzioni è difficile se non impossibile trovarli") — terzo tipo di pretraining nell'Excel.
- RSP = nomenclatura interna dell'ufficio, deriva da Million-AID.

## Fatti — codice del gruppo (Enrico)

- Repo **GitLab**, Enrico ha creato la **branch "Alessandro Potenza"** dal suo codice di lavoro. Libertà totale sulla branch: modificare, aggiungere, **pushare** (mai su main). Link per il clone: lo manda in giornata e ci aggiunge alla repo.
- Struttura (workspace "landfills", package `network/`):
  - `command_creator_enrico.ipynb` — notebook che genera i comandi di training con tutti i parametri (gli stessi di `config`); ⚠️ i notebook **non girano in tmux**: mettere il parametro apposito a `false`, copiare il comando stampato e incollarlo in un tmux **creato dentro `network/`**.
  - `run.py` — dispatcher: in base ai parametri chiama train o inferenza (in `steps/`).
  - `datasets/awclassificationdataset.py` — classi `AWClassificationDataset(Tiff/TiffNamed)`: leggono tiff con rasterio, **band_order ['DB','B','G','R','RE','NIR']**, `bands_selected` default `['R','G','B']`; la variante Named restituisce anche il nome file (serve per salvare CAM/predizioni per immagine).
  - `nets/` — `resnet.py` (18/50/101/152, pretrain ImageNet; **RSP solo per ResNet50**), `swint.py`, `ViT.py` (sperimentale, mai girato).
  - Inferenza: salva le predizioni come array NumPy; `evaluation_tiff.ipynb` le carica e mostra precision/recall/ROC/PR e curve per threshold + **visualize CAM**.
  - Codice con parti legacy: se un parametro non si capisce, probabilmente non serve — chiedere pure.
- **Enrico ha già esplorato le CAM** ("vedere se i pixel guardati erano quelli dove c'era il waste") — il filone localizzazione è condiviso, non conflittuale: "prova, cambia, implementa; poi ci raccontiamo".

## Fatti — Excel "Binary Experiments Results" (Drive, da tenere aggiornato)

Matrice ufficiale degli esperimenti binari (una riga = una configurazione):
- **Dataset**: PNEO+WV3. **GSD**: 120 / 30 / 60 cm. **Bands**: RGB / VNIR / FS (definizione esatta di VNIR vs FS da chiarire).
- **Image size NATIVA, niente resize**: 120 cm → 176×176 px (211,2 m); 30 cm → 700×700 px (210 m); 60 cm → 350×350 px. (Questo risolve il nostro caveat input-size: il protocollo del gruppo tiene i pixel nativi.)
- **Status dataset**: 120 ready · 30 wip · 60 to do.
- Scelte per riga: **Architecture** (ResNet50 / ViT / SwinT), **Pretraining** (1=ImageNet, 2=RSP, 3=SSL), **Augmentation** = Aug_1 (FlipH, FlipV, Multiples90, Brightness; Resize barrato), Batch, LR, **Seed**.
- Da compilare dopo il run: Accuracy/Precision/Recall/F1 + Thresholds / Best Thresholds (l'evaluation notebook fa le curve per threshold).

## Regole operative (Thomas, vincolanti)

1. **Nomi esperimenti descrittivi**, non "esperimento 1,2,3" — organizzati, tracciati ("dopo tre giorni non ti ricordi cosa hai fatto").
2. **Turni GPU**: chi runna senza essersi segnato rischia il **kill del training**; prenotare solo il necessario e **togliersi appena finito**.
3. **Cambiare una cosa alla volta** tra esperimenti.
4. Guida Docker: rispettare dove salvare dati e codice.

## Decisioni nostre post-call

- Ci allineiamo alla pipeline del gruppo: lavoro sulla **branch Alessandro Potenza**, il nostro codice esplorativo confluisce lì dove migliora il loro (Enrico esplicitamente aperto).
- Migrazione naming esperimenti a schema descrittivo allineato all'Excel (v. EXPERIMENTS_LOG).
- Partenza ufficiale: esperimenti a **120 cm** (dataset pronto — nota: le nostre tile "1.2m" da 176px SONO quel dataset).
- Attese: link GitLab (Enrico, in giornata), dataset 30 cm (Thomas avvisa), definizione VNIR vs FS.
