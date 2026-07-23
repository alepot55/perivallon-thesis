"""EXP-008: perche' la CAM fallisce — dimensioni degli oggetti e tetto teorico della griglia.

Tre analisi, tutte su CPU (nessun training):
  1. Statistiche delle GT bbox (test e intero sat_only): aree in pixel a 0.3m e in metri,
     frazione di box piu' piccole di una cella CAM (stage4 = 100 px, stage3 = 50 px a 0.3m).
  2. Oracolo di griglia: CAM "perfetta" = maschera GT ridotta a 7x7 / 14x14 / 28x28,
     poi stessa pipeline box+IoU di EXP-005 -> upper bound di MaxBoxAcc e IoU.
  3. IoU per sottogruppi (severity, site_type, numero di box) con gradcam_s3 gia' calcolata? No:
     qui solo oracolo e statistiche; il breakdown del modello reale si fa quando la GPU e' libera.

Uso: python exp008_bbox_analysis.py
"""

import json
import numpy as np
from scipy import ndimage

from sanity_binary_pneo import SPLIT_DIR
from exp005_wsol_eval import cam_to_box, iou

CELL = {"stage4": 100.0, "stage3": 50.0, "stage2": 25.0}  # lato cella in px @0.3m (700px/griglia)


def bbox_stats(name, images):
    areas_px, sides_px, n_per_img = [], [], []
    for im in images:
        anns = im.get("annotations") or []
        if anns:
            n_per_img.append(len(anns))
        for a in anns:
            x, y, w, h = a["bbox"]
            areas_px.append(w * h)
            sides_px.append(np.sqrt(w * h))
    sides = np.array(sides_px)
    areas_m2 = np.array(areas_px) * (0.3 * 0.3)
    print(f"--- {name}: {len(sides)} box su {len(n_per_img)} immagini (mediana {np.median(n_per_img):.0f} box/img)")
    print(f"    lato equivalente px @0.3m: mediana {np.median(sides):.0f}, p25 {np.percentile(sides,25):.0f}, p75 {np.percentile(sides,75):.0f}")
    print(f"    area: mediana {np.median(areas_m2):.0f} m2")
    for k, c in CELL.items():
        print(f"    box con lato < 1 cella {k} ({c:.0f}px): {(sides < c).mean()*100:.0f}%")
    return sides


def oracle(images, grid):
    """CAM perfetta alla risoluzione di griglia data: quanto si puo' localizzare al massimo?"""
    pgs, bests = [], []
    for im in images:
        anns = im.get("annotations") or []
        if not anns:
            continue
        rw, rh = im["width"], im["height"]
        gts = [a["bbox"] for a in anns]
        mask = np.zeros((rh, rw), np.float32)
        for x, y, w, h in gts:
            mask[max(0, y):y + h, max(0, x):x + w] = 1.0
        # riduci alla griglia (media per cella = CAM ideale) e riporta su
        cw, chh = rw / grid, rh / grid
        cam_g = np.zeros((grid, grid), np.float32)
        for gy in range(grid):
            for gx in range(grid):
                cam_g[gy, gx] = mask[int(gy*chh):int((gy+1)*chh), int(gx*cw):int((gx+1)*cw)].mean()
        cam = np.kron(cam_g, np.ones((int(np.ceil(chh)), int(np.ceil(cw)))))[:rh, :rw]
        if cam.max() > 0:
            cam = cam / cam.max()
        py, px = np.unravel_index(np.argmax(cam), cam.shape)
        pgs.append(any(gx <= px < gx+gw and gy <= py < gy+gh for gx, gy, gw, gh in gts))
        best = 0.0
        for t in np.arange(0.1, 1.0, 0.1):
            box = cam_to_box(cam, t)
            if box is not None:
                best = max(best, max(iou(box, g) for g in gts))
        bests.append(best)
    return np.mean(pgs), np.mean(bests)


def main():
    test = json.load(open(SPLIT_DIR.format(res="0.3m") + "/test.json"))["images"]
    full = json.load(open("/data/waste/datasets/AerialWaste3.6/prod/gt/aw36_od_bin_sat_only.json"))["images"]

    bbox_stats("test set (351 box)", test)
    bbox_stats("intero satellite-only (2827 box)", full)

    print("--- ORACOLO (CAM perfetta, upper bound su test):")
    for grid, name in [(7, "stage4 7x7"), (14, "stage3 14x14"), (28, "stage2 28x28"), (56, "56x56")]:
        pg, best = oracle(test, grid)
        print(f"    griglia {name}: pointing game {pg:.3f} | mean best IoU {best:.3f}")

    # breakdown del test per metadati (per capire dove sara' piu' facile localizzare)
    from collections import Counter
    ann_imgs = [im for im in test if im.get("annotations")]
    print("--- composizione test annotato:")
    print("    severity:", dict(Counter(str(im.get('severity')) for im in ann_imgs)))
    print("    site_type:", dict(Counter(str(im.get('site_type')) for im in ann_imgs).most_common(5)))


if __name__ == "__main__":
    main()
