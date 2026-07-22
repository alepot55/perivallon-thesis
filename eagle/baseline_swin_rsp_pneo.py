"""Baseline Swin-T + RSP sul dataset binario PNEO (split di Thomas), protocollo Gibellini 2025.

Two-step training come nel paper (arXiv:2502.06607):
  1. Transfer Learning: 10 epoche, backbone congelato, solo head, LR 1e-3
  2. Fine-Tuning: 20 epoche, ultimo stage Swin sbloccato, LR 1e-4, cosine
Batch 120 (come il paper, senza gradient accumulation). Normalizzazione per banda
con statistiche calcolate sul train (salvate in stats_<res>.json al primo uso).

Uso:
    python baseline_swin_rsp_pneo.py --res 0.3m
Output: metriche per epoca, best F1 su val, F1 finale su test, checkpoint best.
"""

import argparse
import json
import os
import numpy as np
import timm
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from sanity_binary_pneo import SPLIT_DIR, PneoTiles, evaluate, load_mosaics

RSP_CKPT = os.path.expanduser("~/experiments/weights/rsp_swin_t_e300.pth")
SEED = 42


class SwinBinary(nn.Module):
    """Swin-T timm senza head + pesi RSP + head binaria (come la replica in waste/)."""

    def __init__(self, rsp_ckpt):
        super().__init__()
        self.backbone = timm.create_model("swin_tiny_patch4_window7_224", pretrained=False, num_classes=0)
        ckpt = torch.load(rsp_ckpt, map_location="cpu", weights_only=False)
        state = ckpt.get("model", ckpt.get("state_dict", ckpt))
        remapped = {}
        for k, v in state.items():
            k = k.removeprefix("module.")
            if k.startswith(("head.", "fc.")) or k.endswith(("relative_position_index", "attn_mask")):
                continue
            if ".downsample." in k:  # RSP: downsample a fine stage; timm: a inizio stage successivo
                parts = k.split(".")
                parts[1] = str(int(parts[1]) + 1)
                k = ".".join(parts)
            remapped[k] = v
        missing, unexpected = self.backbone.load_state_dict(remapped, strict=False)
        print(f"pesi RSP caricati: {len(remapped)} tensori (missing {len(missing)}, unexpected {len(unexpected)})")
        self.head = nn.Sequential(nn.Dropout(0.1), nn.Linear(self.backbone.num_features, 1))

    def forward(self, x):
        return self.head(self.backbone(x))


def compute_stats(ds, path):
    """Media e std per banda sui pixel raw del train, calcolate una volta e salvate su json."""
    if os.path.exists(path):
        with open(path) as f:
            s = json.load(f)
        return s["mean"], s["std"]
    print("calcolo statistiche per banda sul train...")
    import rasterio.mask
    tot = np.zeros(3)
    totsq = np.zeros(3)
    n = 0
    for rec, geom, idx in ds.records:
        img, _m = rasterio.mask.mask(ds._dataset(idx), [geom], crop=True, indexes=[3, 2, 1])
        img = img.astype(np.float64).reshape(3, -1)
        tot += img.sum(axis=1)
        totsq += (img ** 2).sum(axis=1)
        n += img.shape[1]
    mean = tot / n
    std = np.sqrt(totsq / n - mean ** 2)
    with open(path, "w") as f:
        json.dump({"mean": mean.tolist(), "std": std.tolist()}, f)
    return mean.tolist(), std.tolist()


def train_phase(model, train_dl, val_dl, device, epochs, lr, cosine, tag):
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.05)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs) if cosine else None
    lossf = nn.BCEWithLogitsLoss()
    best, best_state = 0.0, None
    for ep in range(epochs):
        model.train()
        tot = 0.0
        for x, y in train_dl:
            opt.zero_grad()
            loss = lossf(model(x.to(device)).squeeze(1), y.to(device))
            loss.backward()
            opt.step()
            tot += loss.item() * len(y)
        if sched:
            sched.step()
        f1 = evaluate(model, val_dl, device)
        if f1 > best:
            best = f1
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        print(f"[{tag}] epoch {ep + 1}/{epochs}  loss {tot / len(train_dl.dataset):.4f}  val F1 {f1:.4f}")
    return best, best_state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", default="0.3m", choices=["0.3m", "1.2m"])
    ap.add_argument("--batch", type=int, default=120)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    d = SPLIT_DIR.format(res=args.res)
    mosaics = load_mosaics(args.res)
    print(f"mosaici disponibili a {args.res}: {len(mosaics)}")
    # normalizzazione ufficiale del gruppo (clip p1-p99 + standardize, config in /scratch)
    train_ds = PneoTiles(f"{d}/train.json", mosaics, stats="official")
    val_ds = PneoTiles(f"{d}/val.json", mosaics, stats="official")
    test_ds = PneoTiles(f"{d}/test.json", mosaics, stats="official")
    print(f"train {len(train_ds)}, val {len(val_ds)}, test {len(test_ds)}")

    device = "cuda"
    model = SwinBinary(RSP_CKPT).to(device)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=args.workers)
    val_dl = DataLoader(val_ds, batch_size=args.batch, num_workers=args.workers)
    test_dl = DataLoader(test_ds, batch_size=args.batch, num_workers=args.workers)

    # fase 1: transfer learning (backbone congelato)
    for p in model.backbone.parameters():
        p.requires_grad = False
    tl_best, tl_state = train_phase(model, train_dl, val_dl, device, 10, 1e-3, False, "TL")

    # fase 2: fine-tuning (ultimo stage + norm sbloccati), riparte dal best TL
    if tl_state:
        model.load_state_dict(tl_state)
    for name, p in model.backbone.named_parameters():
        if "layers.3" in name or "norm" in name:
            p.requires_grad = True
    ft_best, ft_state = train_phase(model, train_dl, val_dl, device, 20, 1e-4, True, "FT")

    if ft_state:
        model.load_state_dict(ft_state)
    test_f1 = evaluate(model, test_dl, device)
    out = os.path.expanduser(f"~/experiments/baseline_swin_rsp_{args.res}_seed{args.seed}_valf1_{ft_best:.4f}.pt")
    torch.save(model.state_dict(), out)
    print(f"RISULTATO {args.res} seed {args.seed}: best val F1 TL {tl_best:.4f} | best val F1 FT {ft_best:.4f} | test F1 {test_f1:.4f}")
    print(f"checkpoint: {out}")


if __name__ == "__main__":
    main()
