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
from shapely.geometry import box as shp_box
from shapely.geometry import shape
from shapely.ops import transform as shp_transform
from torch.utils.data import Dataset, DataLoader
from torchvision.models import resnet50, ResNet50_Weights

SPLIT_DIR = "/data/waste/datasets/SatRaw/PNEO/Thomas/{res}/binary"
# due sorgenti di mosaici: archive (processed) + scratch (strip aggiuntive, README Thomas 07/07/26)
MOSAIC_DIRS = [
    "/archive/satellite/processed/PNEO_LOMBARDIA_2023_ALL_30cm_16bit_THOMAS",
    "/scratch/satellite/PNEO_LOMBARDIA_2023_thomas",
]
# ordine bande ufficiale (README + normalization_config.yaml): DB, B, G, R, RE, NIR
# normalizzazione ufficiale del gruppo (valori globali, reflectance x10000): clip p1-p99 poi standardize
_P1_6 = [315.97, 219.90, 233.52, 164.01, 423.21, 496.79]
_P99_6 = [2868.52, 3240.39, 3585.73, 3848.00, 4338.81, 5786.78]
_MEAN_6 = [783.25, 758.37, 933.61, 947.73, 1990.59, 2874.95]
_STD_6 = [424.09, 505.40, 554.01, 708.98, 702.79, 1203.64]

BAND_SETS = {
    # nome: (indici rasterio 1-based, posizioni 0-based nel config per la normalizzazione)
    "rgb": ((4, 3, 2), [3, 2, 1]),   # R, G, B
    "all6": ((1, 2, 3, 4, 5, 6), [0, 1, 2, 3, 4, 5]),  # DB, B, G, R, RE, NIR
}


def norm_arrays(bands):
    _, pos = BAND_SETS[bands]
    pick = lambda vals: np.array([vals[p] for p in pos], dtype=np.float32)[:, None, None]
    return pick(_P1_6), pick(_P99_6), pick(_MEAN_6), pick(_STD_6)


TILE_PX = 224


def load_mosaics(res):
    """Footprint (dai bounds del raster) e path dei mosaici disponibili. Ritorna [(footprint, path_tif)]."""
    fname = "MS_pansharpened.tif" if res == "0.3m" else "MS_mosaic.tif"
    out = []
    for root in MOSAIC_DIRS:
        for tif in sorted(glob.glob(f"{root}/*/{fname}")):
            with rasterio.open(tif) as ds:
                out.append((shp_box(*ds.bounds), tif))
    return out


class PneoTiles(Dataset):
    # le geometrie degli split sono in EPSG:4326, i mosaici in EPSG:32632
    _to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True).transform

    def __init__(self, split_json, mosaics, stats=None, bands="rgb", tile_px=None):
        """stats: None = per-tile max (sanity); "official" = pipeline del gruppo; (mean,std) = custom.
        bands: "rgb" o "all6" (v. BAND_SETS)."""
        with open(split_json) as f:
            records = json.load(f)["images"]
        self.stats = stats
        self.band_indexes = BAND_SETS[bands][0]
        self.tile_px = tile_px or TILE_PX
        self.norm = norm_arrays(bands)
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
        img, _ = rasterio.mask.mask(self._dataset(idx), [geom], crop=True, indexes=list(self.band_indexes))
        img = img.astype(np.float32)
        if self.stats == "official":
            # pipeline del gruppo: clip_p1_p99 poi standardize (normalization_config.yaml)
            p1, p99, mean, std = self.norm
            img = np.clip(img, p1, p99)
            img = (img - mean) / std
        elif self.stats is None:
            img = img / max(img.max(), 1.0)  # uint16 -> [0,1] per-tile (sanity only)
        else:
            mean, std = self.stats
            img = (img - np.array(mean, dtype=np.float32)[:, None, None]) / np.array(std, dtype=np.float32)[:, None, None]
        t = torch.from_numpy(img)
        t = nn.functional.interpolate(t.unsqueeze(0), size=(self.tile_px, self.tile_px), mode="bilinear").squeeze(0)
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
