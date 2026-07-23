"""EXP-007b: la consistency migliora la LOCALIZZAZIONE (non solo la detection)?

Per ognuno dei 6 checkpoint di exp007 (lam 0/1 x seed 42/43/44) misura le metriche
WSOL (gradcam_s3) sul test a 0.3m e a 1.2m. La domanda: con lam=1 il calo di
localizzazione passando da 0.3m a 1.2m si riduce?

Uso: python exp007_eval_wsol.py
"""

import glob
import os
import numpy as np
import torch
import torch.nn.functional as F

from exp005_wsol_eval import REF, cam_to_box, iou
from exp006_cam_ladder import cams_all_variants
from sanity_binary_pneo import SPLIT_DIR, PneoTiles, load_mosaics
from baseline_swin_rsp_pneo import SwinBinary, RSP_CKPT


def wsol_s3(model, ds):
    thresholds = np.arange(0.1, 1.0, 0.1)
    pgs, bests = [], []
    hits = {t: [] for t in thresholds}
    for i in range(len(ds)):
        rec = ds.records[i][0]
        rw, rh, anns = REF[rec["file_name"]]
        if not anns:
            continue
        gts = [a["bbox"] for a in anns]
        x, _ = ds[i]
        cam = cams_all_variants(model, x.unsqueeze(0).cuda())["gradcam_s3"]
        cam = F.interpolate(cam[None, None], size=(rh, rw), mode="bilinear")[0, 0].cpu().numpy()
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
    return np.mean(pgs), np.mean(bests)


def main():
    ds03 = PneoTiles(SPLIT_DIR.format(res="0.3m") + "/test.json", load_mosaics("0.3m"), stats="official")
    ds12 = PneoTiles(SPLIT_DIR.format(res="1.2m") + "/test.json", load_mosaics("1.2m"), stats="official")
    for ck in sorted(glob.glob(os.path.expanduser("~/experiments/consistency_lam*.pt"))):
        model = SwinBinary(RSP_CKPT, in_chans=3)
        model.load_state_dict(torch.load(ck, map_location="cpu"))
        model = model.cuda().eval()
        pg03, iou03 = wsol_s3(model, ds03)
        pg12, iou12 = wsol_s3(model, ds12)
        name = os.path.basename(ck).replace(".pt", "")
        print(f"{name}: 0.3m pg {pg03:.3f} iou {iou03:.3f} | 1.2m pg {pg12:.3f} iou {iou12:.3f} | drop iou {iou03 - iou12:+.3f}")
        del model
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
