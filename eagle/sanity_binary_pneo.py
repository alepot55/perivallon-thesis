"""Sanity training: binary landfill detection sui tile PNEO (split di Thomas).

Legge gli split in /data/waste/datasets/SatRaw/PNEO/Thomas/<RES>/binary/,
ritaglia ogni tile al volo dai mosaici in
/archive/satellite/processed/PNEO_LOMBARDIA_2023_ALL_30cm_16bit_THOMAS/
(bande RGB dal pansharpened a 0.3m, o dal MS mosaic a 1.2m),
e allena un ResNet-50 ImageNet per un check di fine pipeline.

Uso:
    python sanity_binary_pneo.py --res 0.3m --epochs 5
Output: metriche per epoca su stdout + best F1 su val.
"""

import argparse
import json
import glob
import numpy as np
import rasterio
import rasterio.mask
import torch
import torch.nn as nn
from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform as shp_transform
from torch.utils.data import Dataset, DataLoader
from torchvision.models import resnet50, ResNet50_Weights

SPLIT_DIR = "/data/waste/datasets/SatRaw/PNEO/Thomas/{res}/binary"
MOSAIC_DIR = "/archive/satellite/processed/PNEO_LOMBARDIA_2023_ALL_30cm_16bit_THOMAS"
# PNEO: B G R NIR (+ altre); nel prodotto 6 bande l'ordine tipico e' B,G,R,RE,NIR,DeepBlue.
# Per il sanity uso le prime 3 riportate a RGB; l'ordine esatto si verifica con Enrico.
RGB_BANDS = (3, 2, 1)
TILE_PX = 224


def load_mosaics(res):
    """Footprint e path dei mosaici delle 5 strip. Ritorna [(footprint, path_tif)]."""
    fname = "MS_pansharpened.tif" if res == "0.3m" else "MS_mosaic.tif"
    out = []
    for strip in sorted(glob.glob(f"{MOSAIC_DIR}/*/")):
        with open(strip + "Mosaic_footprint.geojson") as f:
            gj = json.load(f)
        out.append((shape(gj["features"][0]["geometry"]), strip + fname))
    return out


class PneoTiles(Dataset):
    # le geometrie degli split sono in EPSG:4326, i mosaici in EPSG:32632
    _to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True).transform

    def __init__(self, split_json, mosaics, stats=None):
        """stats: None = normalizzazione per-tile max (sanity); oppure (mean, std) per banda."""
        with open(split_json) as f:
            records = json.load(f)["images"]
        self.stats = stats
        self.paths = [p for _, p in mosaics]
        self._open = {}  # cache per-worker: i dataset rasterio non passano il fork
        # assegna il mosaico a ogni record (centroide, fallback intersezione); scarta i non risolvibili
        self.records = []
        dropped = 0
        for rec in records:
            geom = shp_transform(self._to_utm, shape(rec["geometry"]))
            idx = next((k for k, (fp, _) in enumerate(mosaics) if fp.contains(geom.centroid)), None)
            if idx is None:
                idx = next((k for k, (fp, _) in enumerate(mosaics) if fp.intersects(geom)), None)
            if idx is None:
                dropped += 1
                continue
            self.records.append((rec, geom, idx))
        if dropped:
            print(f"attenzione: {dropped}/{len(records)} tile fuori da tutti i mosaici, scartate")

    def __len__(self):
        return len(self.records)

    def _dataset(self, idx):
        if idx not in self._open:
            self._open[idx] = rasterio.open(self.paths[idx])
        return self._open[idx]

    def __getitem__(self, i):
        rec, geom, idx = self.records[i]
        label = 1.0 if rec.get("categories") else 0.0
        img, _ = rasterio.mask.mask(self._dataset(idx), [geom], crop=True, indexes=list(RGB_BANDS))
        img = img.astype(np.float32)
        if self.stats is None:
            img = img / max(img.max(), 1.0)  # uint16 -> [0,1] per-tile (sanity only)
        else:
            mean, std = self.stats
            img = (img - np.array(mean, dtype=np.float32)[:, None, None]) / np.array(std, dtype=np.float32)[:, None, None]
        t = torch.from_numpy(img)
        t = nn.functional.interpolate(t.unsqueeze(0), size=(TILE_PX, TILE_PX), mode="bilinear").squeeze(0)
        return t, torch.tensor(label)


def f1_score(tp, fp, fn):
    p = tp / max(tp + fp, 1)
    r = tp / max(tp + fn, 1)
    return 2 * p * r / max(p + r, 1e-9)


def evaluate(model, loader, device):
    model.eval()
    tp = fp = fn = 0
    with torch.no_grad():
        for x, y in loader:
            pred = (torch.sigmoid(model(x.to(device))).squeeze(1) > 0.5).cpu()
            y = y.bool()
            tp += (pred & y).sum().item()
            fp += (pred & ~y).sum().item()
            fn += (~pred & y).sum().item()
    return f1_score(tp, fp, fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", default="0.3m", choices=["0.3m", "1.2m"])
    ap.add_argument("--epochs", type=int, default=5)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--smoke", action="store_true", help="carica 5 tile e esce")
    args = ap.parse_args()

    mosaics = load_mosaics(args.res)
    print(f"mosaici aperti: {len(mosaics)}")
    d = SPLIT_DIR.format(res=args.res)
    train_ds = PneoTiles(f"{d}/train.json", mosaics)
    val_ds = PneoTiles(f"{d}/val.json", mosaics)
    print(f"train {len(train_ds)}, val {len(val_ds)}")

    if args.smoke:
        for i in range(5):
            x, y = train_ds[i]
            print(f"tile {i}: shape {tuple(x.shape)}, range [{x.min():.3f},{x.max():.3f}], label {int(y)}")
        print("smoke test ok")
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    model.fc = nn.Linear(model.fc.in_features, 1)
    model = model.to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.05)
    lossf = nn.BCEWithLogitsLoss()

    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=args.workers)
    val_dl = DataLoader(val_ds, batch_size=args.batch, num_workers=args.workers)

    best = 0.0
    for ep in range(args.epochs):
        model.train()
        tot = 0.0
        for x, y in train_dl:
            opt.zero_grad()
            loss = lossf(model(x.to(device)).squeeze(1), y.to(device))
            loss.backward()
            opt.step()
            tot += loss.item() * len(y)
        f1 = evaluate(model, val_dl, device)
        best = max(best, f1)
        print(f"epoch {ep + 1}/{args.epochs}  loss {tot / len(train_ds):.4f}  val F1 {f1:.4f}")
    print(f"best val F1 ({args.res}): {best:.4f}")


if __name__ == "__main__":
    main()
