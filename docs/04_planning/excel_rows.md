# Righe pronte per l'Excel "Binary Experiments Results"

> Ale: copia questi valori nella riga giusta della matrice su Drive. Una sezione = un run concluso, in ordine cronologico inverso. Le colonne seguono l'ordine dell'Excel; se una colonna non c'è o ha altro nome, adatta a vista. Metriche sul **test** (139 img, comuni mai visti), threshold 0.5 salvo dove indicato.

## EXP-012 — b120_rgb_swint_rsp_aug1_s0 (2026-07-24)

| Colonna | Valore |
|---|---|
| Dataset | PNEO |
| GSD | 120 cm |
| Bands | RGB |
| Image size | 176 (nativa) |
| Architecture | SwinT (v1_t) |
| Pretraining | 2 (RSP) |
| Augmentation | Aug_1 senza Brightness (fliph .5, flipv .5, rot90) |
| Batch | 50 |
| LR | 1e-3 (TL) → 1e-4 (FT) |
| Seed | 0 |
| Accuracy | 0.712 |
| Precision | 0.593 |
| Recall | 0.873 |
| F1 | 0.706 |
| Best threshold | 0.34 (su test) → F1 0.707 |
| Note | TL 19 ep + FT 17 ep (early stop); AUROC 0.809; run: `/data/waste/multilabel/SatRaw/Mosaico_PNEO_2_3_9/b120_rgb_swint_rsp_aug1_s0` |

## EXP-011 — b120_rgb_resnet50_rsp_aug1_s0 (2026-07-24)

| Colonna | Valore |
|---|---|
| Dataset | PNEO |
| GSD | 120 cm |
| Bands | RGB |
| Image size | 176 (nativa) |
| Architecture | ResNet50 |
| Pretraining | 2 (RSP) |
| Augmentation | Aug_1 senza Brightness (fliph .5, flipv .5, rot90) |
| Batch | 50 |
| LR | 1e-3 (TL) → 1e-4 (FT) |
| Seed | 0 |
| Accuracy | 0.669 |
| Precision | 0.563 |
| Recall | 0.727 |
| F1 | 0.635 |
| Best threshold | 0.26 (su test) → F1 0.645 |
| Note | TL 26 ep + FT 17 ep (early stop); AUROC 0.770; run: `/data/waste/multilabel/SatRaw/Mosaico_PNEO_2_3_9/b120_rgb_resnet50_rsp_aug1_s0` |
