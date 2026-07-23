"""EXP-009: sfondare il tetto di EXP-008 alzando la risoluzione di input (inference-only).

Idea (da metodo_prossimi_passi.md): con input 448 lo stage-3 di Swin produce mappe 28x28,
con input 672 mappe 42x42 — sopra il tetto geometrico (oracolo 28x28: pointing game 0.86).
Qui si valutano i checkpoint GIA' allenati a 224 sugli input piu' grandi (le finestre Swin
restano 7x7, cambia solo la griglia): niente training, solo inference + Grad-CAM.

Uso: python exp009_highres_input.py
Output: per input size / config: F1 detection test + metriche WSOL (gradcam s3 e s4).
"""

import os
import numpy as np
import timm
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

from exp005_wsol_eval import CKPTS, REF, cam_to_box, iou
from exp006_cam_ladder import cams_all_variants
from sanity_binary_pneo import SPLIT_DIR, PneoTiles, evaluate, load_mosaics
from baseline_swin_rsp_pneo import SwinBinary, RSP_CKPT

SIZES = [224, 448, 672]  # griglie stage3: 14, 28, 42 (tutte divisibili per finestra 7)


def load_at_size(res, bands, size):
    """Ricrea il modello con img_size diverso e ci carica il checkpoint 224 (i buffer
    dipendenti dalla griglia — attn_mask, relative_position_index — vengono scartati)."""
    model = SwinBinary(RSP_CKPT, in_chans=6 if bands == "all6" else 3)
    if size != 224:
        model.backbone = timm.create_model(
            "swin_tiny_patch4_window7_224", pretrained=False, num_classes=0,
            in_chans=6 if bands == "all6" else 3, img_size=size)
    sd = torch.load(os.path.join(os.path.expanduser("~/experiments"), os.path.basename(CKPTS[(res, bands)])),
                    map_location="cpu")
    target = model.state_dict()
    filtered = {k: v for k, v in sd.items() if k in target and target[k].shape == v.shape}
    model.load_state_dict(filtered, strict=False)
    print(f"  caricati {len(filtered)}/{len(sd)} tensori (scartati i buffer legati alla griglia)")
    return model.cuda().eval()


def wsol_metrics(model, ds):
    thresholds = np.arange(0.1, 1.0, 0.1)
    out = {}
    for variant in ["gradcam_s3", "gradcam_s4"]:
        pgs, bests = [], []
        hits = {t: [] for t in thresholds}
        for i in range(len(ds)):
            rec = ds.records[i][0]
            rw, rh, anns = REF[rec["file_name"]]
            if not anns:
                continue
            gts = [a["bbox"] for a in anns]
            x, _ = ds[i]
            cams = cams_all_variants(model, x.unsqueeze(0).cuda())
            cam = F.interpolate(cams[variant][None, None], size=(rh, rw), mode="bilinear")[0, 0].cpu().numpy()
            py, px = np.unravel_index(np.argmax(cam), cam.shape)
            pgs.append(any(gx <= px < gx + gw and gy <= py < gy + gh for gx, gy, gw, gh in gts))
            best = 0.0
            for t in thresholds:
                box = cam_to_box(cam, t)
                if box is None:
                    hits[t].append(False)
                    continue
                m = max(iou(box, g) for g in gts)
                best = max(best, m)
                hits[t].append(m >= 0.5)
            bests.append(best)
        out[variant] = (np.mean(pgs), max(np.mean(hits[t]) for t in thresholds), np.mean(bests))
    return out


def main():
    for res, bands in [("0.3m", "rgb"), ("0.3m", "all6"), ("1.2m", "rgb")]:
        mosaics = load_mosaics(res)
        for size in SIZES:
            ds = PneoTiles(SPLIT_DIR.format(res=res) + "/test.json", mosaics,
                           stats="official", bands=bands, tile_px=size)
            model = load_at_size(res, bands, size)
            f1 = evaluate(model, DataLoader(ds, batch_size=24, num_workers=8), "cuda")
            m = wsol_metrics(model, ds)
            for v, (pg, mba, biou) in m.items():
                print(f"{res} {bands} input{size} {v}: pg {pg:.3f} | MaxBoxAcc@0.5 {mba:.3f} | "
                      f"meanIoU {biou:.3f} | test F1 {f1:.3f}")
            del model
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
