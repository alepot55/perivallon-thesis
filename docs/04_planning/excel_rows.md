# Righe pronte per l'Excel "Binary Experiments Results"

> Ale: copia questi valori nella riga giusta della matrice su Drive. Una sezione = un run concluso, in ordine cronologico inverso. Le colonne seguono l'ordine dell'Excel; se una colonna non c'è o ha altro nome, adatta a vista. Metriche sul **test** (139 img, comuni mai visti), threshold 0.5 salvo dove indicato.

## EXP-014 — multi-seed SwinT, seed 42 e 43 (2026-07-24)

Config identiche a EXP-012 (RGB) e EXP-013 (VNIR = 6 bande), cambia solo il seed. Una riga Excel per run:

| Run | Bands | Seed | Accuracy | Precision | Recall | F1 | Best th → F1 | AUROC |
|---|---|---|---|---|---|---|---|---|
| b120_rgb_swint_rsp_aug1_s42 | RGB | 42 | 0.698 | 0.573 | 0.927 | 0.708 | 0.52 → 0.723 | 0.826 |
| b120_rgb_swint_rsp_aug1_s43 | RGB | 43 | 0.676 | 0.563 | 0.818 | 0.667 | 0.51 → 0.672 | 0.764 |
| b120_vnir_swint_rsp_aug1_s42 | VNIR (6) | 42 | 0.691 | 0.579 | 0.800 | 0.672 | 0.59 → 0.704 | 0.795 |
| b120_vnir_swint_rsp_aug1_s43 | VNIR (6) | 43 | 0.662 | 0.549 | 0.818 | 0.657 | 0.45 → 0.676 | 0.787 |

Medie a 3 seed (se l'Excel vuole una riga aggregata): RGB **F1 0.694 ± 0.019** · VNIR **F1 0.665 ± 0.006**.

## EXP-013 — b120_vnir_swint_rsp_aug1_s0 (2026-07-24)

| Colonna | Valore |
|---|---|
| Dataset | PNEO |
| GSD | 120 cm |
| Bands | VNIR (tutte e 6: DB,B,G,R,RE,NIR) |
| Image size | 176 (nativa) |
| Architecture | SwinT (v1_t, patch-embed multibanda) |
| Pretraining | 2 (RSP) |
| Augmentation | Aug_1 senza Brightness (fliph .5, flipv .5, rot90) |
| Batch | 50 |
| LR | 1e-3 (TL) → 1e-4 (FT) |
| Seed | 0 |
| Accuracy | 0.719 |
| Precision | 0.629 |
| Recall | 0.709 |
| F1 | 0.667 |
| Best threshold | 0.34 (su test) → F1 0.686 |
| Note | TL 19 ep + FT 16 ep; AUROC 0.782; norm per banda da metadata; run: `/data/waste/multilabel/SatRaw/Mosaico_PNEO_2_3_9/b120_vnir_swint_rsp_aug1_s0` |

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
