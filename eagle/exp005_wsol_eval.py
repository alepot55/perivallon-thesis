"""EXP-005: prima valutazione quantitativa della localizzazione weakly-supervised.

Per ogni immagine positiva del test con bounding box (50 img, 351 box):
Grad-CAM dal classificatore allenato -> upsample nello spazio delle annotazioni
(coordinate del record 0.3m) -> metriche WSOL standard:
  - pointing game: il massimo della CAM cade dentro una GT box
  - MaxBoxAcc: max su soglie CAM della frazione di immagini con IoU(box CAM, GT) >= 0.5
  - mean best IoU: media del miglior IoU per immagine

Uso: python exp005_wsol_eval.py
Valuta le 4 config (rgb/all6 x 0.3m/1.2m) con i checkpoint seed 42.
"""

import glob
import json
import os
import numpy as np
import torch
import torch.nn.functional as F
from scipy import ndimage

from sanity_binary_pneo import SPLIT_DIR, PneoTiles, load_mosaics
from baseline_swin_rsp_pneo import SwinBinary, RSP_CKPT

CKPTS = {
    ("0.3m", "rgb"): "baseline_swin_rsp_0.3m_valf1_0.7963.pt",
    ("1.2m", "rgb"): "baseline_swin_rsp_1.2m_valf1_0.7290.pt",
    ("0.3m", "all6"): sorted(glob.glob(os.path.expanduser("~/experiments/baseline_swin_rsp_0.3m_all6_seed42_*.pt")))[-1],
    ("1.2m", "all6"): sorted(glob.glob(os.path.expanduser("~/experiments/baseline_swin_rsp_1.2m_all6_seed42_*.pt")))[-1],
}

# spazio di riferimento delle annotazioni = width/height dei record 0.3m
REF = {im["file_name"]: (im["width"], im["height"], im.get("annotations") or [])
       for im in json.load(open(SPLIT_DIR.format(res="0.3m") + "/test.json"))["images"]}


def gradcam(model, x):
    """Grad-CAM sull'ultimo stage dello Swin. x: (1,C,224,224). Ritorna (7,7) in [0,1]."""
    feats = model.backbone.forward_features(x)          # (1, 7, 7, 768)
    logit = model.head(feats.mean(dim=(1, 2)))          # stesso pooling del forward
    grad = torch.autograd.grad(logit.sum(), feats)[0]
    w = grad.mean(dim=(1, 2))                           # (1, 768)
    cam = torch.relu((feats * w[:, None, None, :]).sum(-1))[0]
    cam = cam - cam.min()
    return (cam / cam.max().clamp(min=1e-8)).detach()


def cam_to_box(cam, thr):
    """Bounding box della componente connessa piu' grande della CAM sogliata."""
    mask = (cam >= thr).astype(np.uint8)
    if mask.sum() == 0:
        return None
    lab, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    ys, xs = np.where(lab == (np.argmax(sizes) + 1))
    return xs.min(), ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1


def iou(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix = max(0, min(ax + aw, bx + bw) - max(ax, bx))
    iy = max(0, min(ay + ah, by + bh) - max(ay, by))
    inter = ix * iy
    return inter / (aw * ah + bw * bh - inter + 1e-9)


def evaluate_config(res, bands):
    mosaics = load_mosaics(res)
    ds = PneoTiles(SPLIT_DIR.format(res=res) + "/test.json", mosaics, stats="official", bands=bands)
    model = SwinBinary(RSP_CKPT, in_chans=6 if bands == "all6" else 3)
    model.load_state_dict(torch.load(os.path.join(os.path.expanduser("~/experiments"), os.path.basename(CKPTS[(res, bands)])), map_location="cpu"))
    model = model.cuda().eval()

    thresholds = np.arange(0.1, 1.0, 0.1)
    hits_pg, best_ious = [], []
    box_hits = {t: [] for t in thresholds}
    for i in range(len(ds)):
        rec = ds.records[i][0]
        _, _, anns = REF[rec["file_name"]]
        if not anns:
            continue
        gts = [a["bbox"] for a in anns]
        rw, rh = REF[rec["file_name"]][0], REF[rec["file_name"]][1]
        x, _ = ds[i]
        cam7 = gradcam(model, x.unsqueeze(0).cuda())
        cam = F.interpolate(cam7[None, None], size=(rh, rw), mode="bilinear")[0, 0].cpu().numpy()

        py, px = np.unravel_index(np.argmax(cam), cam.shape)
        hits_pg.append(any(gx <= px < gx + gw and gy <= py < gy + gh for gx, gy, gw, gh in gts))

        best = 0.0
        for t in thresholds:
            box = cam_to_box(cam, t)
            if box is None:
                box_hits[t].append(False)
                continue
            m = max(iou(box, g) for g in gts)
            best = max(best, m)
            box_hits[t].append(m >= 0.5)
        best_ious.append(best)

    n = len(best_ious)
    maxboxacc = max(np.mean(box_hits[t]) for t in thresholds)
    print(f"{res} {bands}: n={n} | pointing game {np.mean(hits_pg):.3f} | "
          f"MaxBoxAcc@0.5 {maxboxacc:.3f} | mean best IoU {np.mean(best_ious):.3f}")


if __name__ == "__main__":
    for res in ["0.3m", "1.2m"]:
        for bands in ["rgb", "all6"]:
            evaluate_config(res, bands)
