"""EXP-006: scala delle varianti CAM sui checkpoint esistenti.

Confronta, sulle 50 immagini positive di test con bbox:
  - gradcam_s4: Grad-CAM ultimo stage (7x7) — il riferimento di EXP-005
  - gradcam_s3: Grad-CAM stage 3 (14x14)
  - layercam_s3: LayerCAM stage 3 (pesi elemento per elemento, relu(grad)*feat)
  - layercam_s2: LayerCAM stage 2 (28x28)

Stesse metriche di EXP-005 (pointing game, MaxBoxAcc@0.5, mean best IoU).
Uso: python exp006_cam_ladder.py
"""

import json
import os
import numpy as np
import torch
import torch.nn.functional as F

from exp005_wsol_eval import CKPTS, REF, cam_to_box, iou
from sanity_binary_pneo import SPLIT_DIR, PneoTiles, load_mosaics
from baseline_swin_rsp_pneo import SwinBinary, RSP_CKPT


def cams_all_variants(model, x):
    """Un forward con hook sugli stage 2/3/4; ritorna dict nome -> cam 2D in [0,1]."""
    feats = {}
    handles = [
        model.backbone.layers[1].register_forward_hook(lambda m, i, o: feats.__setitem__("s2", o)),
        model.backbone.layers[2].register_forward_hook(lambda m, i, o: feats.__setitem__("s3", o)),
    ]
    f4 = model.backbone.forward_features(x)  # (1, 7, 7, C)
    for h in handles:
        h.remove()
    feats["s4"] = f4
    logit = model.head(f4.mean(dim=(1, 2)))
    grads = torch.autograd.grad(logit.sum(), [feats["s2"], feats["s3"], feats["s4"]])
    out = {}
    for name, f, g in [("s2", feats["s2"], grads[0]), ("s3", feats["s3"], grads[1]), ("s4", feats["s4"], grads[2])]:
        gradcam = torch.relu((f * g.mean(dim=(1, 2), keepdim=True)).sum(-1))[0]
        layercam = (torch.relu(g) * f).sum(-1)[0]
        for label, cam in [(f"gradcam_{name}", gradcam), (f"layercam_{name}", layercam)]:
            cam = cam - cam.min()
            out[label] = (cam / cam.max().clamp(min=1e-8)).detach()
    return out


VARIANTS = ["gradcam_s4", "gradcam_s3", "layercam_s3", "layercam_s2"]


def evaluate_config(res, bands):
    ds = PneoTiles(SPLIT_DIR.format(res=res) + "/test.json", load_mosaics(res), stats="official", bands=bands)
    model = SwinBinary(RSP_CKPT, in_chans=6 if bands == "all6" else 3)
    model.load_state_dict(torch.load(
        os.path.join(os.path.expanduser("~/experiments"), os.path.basename(CKPTS[(res, bands)])), map_location="cpu"))
    model = model.cuda().eval()

    thresholds = np.arange(0.1, 1.0, 0.1)
    agg = {v: {"pg": [], "best": [], "hits": {t: [] for t in thresholds}} for v in VARIANTS}
    for i in range(len(ds)):
        rec = ds.records[i][0]
        rw, rh, anns = REF[rec["file_name"]]
        if not anns:
            continue
        gts = [a["bbox"] for a in anns]
        x, _ = ds[i]
        cams = cams_all_variants(model, x.unsqueeze(0).cuda())
        for v in VARIANTS:
            cam = F.interpolate(cams[v][None, None], size=(rh, rw), mode="bilinear")[0, 0].cpu().numpy()
            py, px = np.unravel_index(np.argmax(cam), cam.shape)
            agg[v]["pg"].append(any(gx <= px < gx + gw and gy <= py < gy + gh for gx, gy, gw, gh in gts))
            best = 0.0
            for t in thresholds:
                box = cam_to_box(cam, t)
                if box is None:
                    agg[v]["hits"][t].append(False)
                    continue
                m = max(iou(box, g) for g in gts)
                best = max(best, m)
                agg[v]["hits"][t].append(m >= 0.5)
            agg[v]["best"].append(best)

    for v in VARIANTS:
        a = agg[v]
        mba = max(np.mean(a["hits"][t]) for t in thresholds)
        print(f"{res} {bands} {v}: pg {np.mean(a['pg']):.3f} | MaxBoxAcc@0.5 {mba:.3f} | mean best IoU {np.mean(a['best']):.3f}")


if __name__ == "__main__":
    for res in ["0.3m", "1.2m"]:
        for bands in ["rgb", "all6"]:
            evaluate_config(res, bands)
