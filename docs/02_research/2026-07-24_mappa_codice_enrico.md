# Mappa del codice di Enrico (repo `wds-co/multispectralpotenza`)

Esplorazione del 24/7 sera, subito dopo lo sblocco dell'accesso (ruolo Developer). Clone canonico: eagle `/home/dev/multispectralpotenza`. Copia di lettura locale: `~/Desktop/uni/multispectralpotenza` (fuori dalla repo tesi). Ultimo commit: 24/7 17:03 "Add inference and training scripts for TIFF images".

## 1. Il quadro in una frase

È il codice AerialWaste di Enrico esteso ai TIFF multispettrali: stessi step (tl → ft → infer → cam), stessa struttura dataset (json stile AerialWaste), con in più la selezione bande per nome e la normalizzazione per banda da `metadata.json`. Un progetto GitLab dedicato a noi (non una branch): possiamo pushare liberamente, main compreso — ma teniamo main = snapshot di Enrico e lavoriamo su una nostra branch.

## 2. Struttura (cartella `network/`)

| File | Ruolo |
|---|---|
| `command_creator_enrico.ipynb` | Compone il comando di training/inferenza (parametri → stringa `python run.py ...`). Non gira in tmux: si copia il comando stampato. |
| `run.py` | Dispatcher: seed, cartelle output, poi `train_tiff`/`infer_tiff` se il path immagini contiene "MultiSpectral"... in realtà la selezione è `"MultiSpectral" in args.train_image_folder` — coi path attuali (`/scratch/...patches_MS_8bit...`) NON matcha: si usa comunque train_tiff finché il nome cartella contiene la stringa giusta. Da verificare col primo run [UNCERTAIN]. |
| `misc/config.py` | Tutti gli argomenti CLI (dataset, rete, loss, augmentation, early stopping, CAM). |
| `datasets/awclassificationdataset.py` | `AWClassificationDatasetTiff(Named)`: legge i tif con rasterio, seleziona le bande **per nome** (`bands_selected` vs `band_order` dal metadata). Versione Named restituisce anche il filename (serve a salvare CAM/predizioni per immagine). |
| `steps/train_tiff.py` | Loop di training: augmentation, normalizzazione, val per epoca, best checkpoint, early stopping, TensorBoard. |
| `steps/infer_tiff.py` | Inferenza: predizioni (numpy) e CAM. |
| `misc/cam_visualizer_tiff.py` | Visualizzazione CAM. |
| `nets/resnet.py`, `nets/swint.py` | Architetture (dettagli sotto). |
| `misc/losses/` | bce, double_loss, focal tversky, asymmetric, contrastive (SupCon), zlpr — per il binario si usa `bce`. |
| `evaluation_tiff.ipynb` | Carica le predizioni numpy: metriche, curve per threshold, visualizza CAM. |

## 3. Dataset (verificato sul server, 24/7)

- **Tile pre-tagliate** (non ritaglio al volo come i nostri script):
  - `/scratch/satellite/PNEO_LOMBARDIA_2023_thomas/Mosaico_PNEO_2_3_9/patches_MS_8bit_30cm` — 1294 tif, 700×700 px (+ `metadata.json`)
  - `/scratch/satellite/PNEO_LOMBARDIA_2023_thomas/Mosaico_PNEO_2_3_9/patches_MS_8bit_120cm` — 1294 tif, 176×176 px (+ `metadata.json`)
  - Nomi file: `Comune_offsetX_offsetY.tif` — verificato: **tutti i 1294 file_name degli split matchano 1:1** le tile.
- **1294 tile = esattamente i nostri split Thomas** (1020 train + 135 val + 139 test): stesse geometrie, già materializzate.
- **`metadata.json`** nella cartella tile: `dtype uint8, scale 255`, `band_order [DB,B,G,R,RE,NIR]`, mean/std per banda (normalizzati e raw).
- **Split json** (path REALE sul server): `/data/waste/datasets/SatRaw/PNEO/Thomas/{0.3m,1.2m}/binary/{train,val,test}.json` — il notebook di Enrico punta a `PNEO/{GSD}/binary` senza `Thomas/`, che sul server non esiste: corretto nel nostro runner. Stile AerialWaste: `images[].file_name` + `categories` (una sola categoria: `waste`).
- ⚠️ Il check `"MultiSpectral" in path` di `run.py` coi path /scratch non matcha: risolto con symlink `/home/dev/MultiSpectral_links/patches_MS_8bit_{30,120}cm` → cartelle patch (senza toccare storage condiviso né codice).
- ⚠️ **8 bit, non 16**: le tile sono uint8 (scala 255), mentre i mosaici sorgente sono uint16 riflettanza. Perdita di profondità radiometrica — perché? (domanda per Enrico; per il MS potrebbe contare).

## 4. Protocollo di training (dal command creator)

- **Due fasi**: `tl` (solo testa: `first_trainable [5,0]`, lr 1e-3) → `ft` (tutta la rete: `[0,0]`, lr 1e-4, carica il checkpoint tl). Stesso schema Gibellini.
- Adam, batch 50, max 100 epoche con **early stopping** su val loss (patience 15, min_delta 0.001), scheduler ReduceLROnPlateau (factor 0.1, patience 5).
- **Augmentation reale nel notebook**: FlipH .5, FlipV .5, Rotate90s. `brightness = None` con commento "Inefficient" → l'Aug_1 dell'Excel dichiara anche Brightness ma il default di Enrico la spegne. Da chiarire prima di compilare la colonna Augmentation.
- `train_resize = [native, native]` (176 o 700) → di fatto **nessun resize**, conferma il protocollo tile native.
- **Normalizzazione**: RGB → statistiche ImageNet; qualsiasi altro set di bande → mean/std per banda dal `metadata.json`. (Diverso dal nostro clip p1-p99 + standardize sul 16 bit.)
- Seed: il notebook usa `experiment_seed 0`; `cudnn.deterministic = True`.
- Output: `/data/waste/multilabel/SatRaw/Mosaico_PNEO_2_3_9/<esperimento>/{checkpoints,cams,predictions,tb_logs}` + `train.log`/`infer.log`.

## 5. Architetture

- **ResNet** (`resnet.py`): 18/50/101/152 torchvision; pretraining ImageNet / RSP (solo r50, `nets/weights/rsp-resnet-50-ckpt.pth`) / **SSL** (`nets/weights/SSL_pretrained_models/ssl-resnet-500.pt` — già previsto nel codice!). Multibanda: `build_first_layer()` rifà conv1 mappando i kernel RGB **per nome banda** (R→R, G→G, B→B) e inizializzando le bande extra con la media dei kernel — stessa idea della nostra inflation (senza il rescale ×3/6). In più: `--reduce_first_layer_lr` per addestrare conv1 con lr ridotto.
- **SwinT** (`swint.py`): torchvision (non timm), v1_t/v2_t; RSP caricato con rimappatura posizionale delle chiavi. **Solo 3 canali**: nessun supporto multibanda, e nessun parametro img_size (447/448 non previsti). → qui entrano i nostri contributi.
- ⚠️ `nets/weights/` **non è nella repo** (checkpoint pesanti): i file rsp/ssl vanno procurati o linkati a parte.

## 6. CAM e localizzazione

- `cam_method`: `gradcam, gradcam_tta, gradcam++, eigen_cam, highres_cam, layer_cam, multicam, multicam_tta` (default del notebook: `multicam_tta`).
- Parametri di grid inference (`meter_size`, `grid_number`) per valutazione a griglia.
- Enrico ha già guardato "se i pixel guardati sono quelli col waste" → il filone localizzazione è condiviso. Quello che manca a loro e abbiamo noi: la **valutazione WSOL quantitativa** (pointing game, MaxBoxAcc@0.5, protocollo Choe) contro le bbox GT.

## 7. Differenze pipeline loro vs nostri script

| Aspetto | Loro | Nostri script (`~/experiments`) |
|---|---|---|
| Tile | pre-tagliate 8-bit su /scratch | ritaglio al volo dai mosaici 16-bit |
| Normalizzazione | ImageNet (RGB) / mean-std per banda (MS) | clip p1-p99 + standardize (config Thomas) |
| SwinT | torchvision, RGB only, input nativo | timm + RSP remap, 6 bande inflate, img_size 448/672 |
| Training | tl→ft, Adam, early stop su val loss | tl→ft (Gibellini), AdamW+cosine, epoche fisse |
| Localizzazione | generazione CAM (tante varianti) + visualizer | valutazione WSOL quantitativa vs bbox |
| Tracking | log + TensorBoard (+ Excel di gruppo) | log + EXPERIMENTS_LOG/CLAIMS |

## 8. Cosa portiamo noi dentro la loro pipeline (in ordine)

1. **Riproduzione baseline loro** a 120 cm (resnet50, RSP, RGB, seed 0) — valida la pipeline e riempie la prima riga Excel.
2. **SwinT multibanda**: portare la nostra inflation per nome banda dentro `swint.py` (pattern già presente in `resnet.py`, quindi coerente col loro stile).
3. **Input 448 al 30 cm**: parametro img_size nella SwinT (la nostra scoperta chiave: localizzazione ×7 con detection intatta).
4. **Valutazione WSOL** sulle loro CAM (pointing game + MaxBoxAcc vs `aw36_od_bin_sat_only.json`), riusando i loro output `cams/`.
5. **Consistency loss** come step successivo (metodo, dopo che le baseline girano).
6. **60 cm**: `derive_60cm.py` sulle tile 30 cm → cartella `patches_MS_8bit_60cm` + metadata ricalcolato (350 px).

## 9. Primo run nella loro pipeline (24/7 sera)

`b120_rgb_resnet50_rsp_aug1_s0` — riproduzione esatta dei default del command creator a 120 cm (resnet50+RSP, RGB, fliph/flipv/rot90, seed 0), TL→FT→inferenza test. Runner: `network/commands/b120_rgb_resnet50_rsp_aug1_s0.sh` (branch `ale`). Fix minimi necessari per farla partire (committati sulla branch, da raccontare a Enrico):
- `misc/datasets/nets/__init__.py`: import di moduli assenti dallo snapshot (cam_visualizers, fpn, mobile, dataset Contrastive/Grid) → ridotti a ciò che esiste.
- venv `base`: aggiunti `torcheval torchmetrics tensorboard ipywidgets grad-cam`.
- Pesi RSP: symlink da `/data/waste/synthetic/lain/code/new_network/nets/weights/` (stessi filename attesi dal codice).
- Output: `/data/waste/multilabel/SatRaw/Mosaico_PNEO_2_3_9/b120_rgb_resnet50_rsp_aug1_s0/{tl,ft}`.

## 10. Domande aperte per Enrico/Thomas

1. **VNIR vs FS** nell'Excel: quali bande esattamente?
2. **8 bit**: perché le patch MS sono uint8 e non 16 bit? (per il MS la profondità radiometrica può contare)
3. **Brightness** nell'Aug_1: il notebook la spegne ("Inefficient") — cosa scrivo nell'Excel?
4. Seed: quanti per riga (notebook usa 0; noi proporremmo 3 seed)?
5. Split json: il notebook punta a `PNEO/{GSD}/binary` ma sul server stanno in `PNEO/Thomas/{GSD}/binary` — li spostate voi o adeguiamo il notebook?
6. RSP/SSL checkpoint (`nets/weights/`): confermate quelli in `/data/waste/synthetic/lain/...`? (usati via symlink)
