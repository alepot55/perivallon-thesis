"""EXP-007: training con consistency cross-risoluzione della localizzazione.

Idea: le stesse tile esistono a 0.3 m e 1.2 m. Si allena UN solo classificatore
che vede entrambe le versioni e, sulle positive, si penalizza la differenza tra
le due mappe CAM (la CAM lineare feats @ w_head, differenziabile). Ipotesi: la
localizzazione diventa piu' robusta al degradare della risoluzione.

Controllo: --lam 0 = stesso training dual-resolution senza vincolo (isola l'effetto).

Uso: python exp007_consistency.py --lam 1.0 --seed 42
Output: F1 detection a 0.3m e 1.2m + checkpoint; la valutazione WSOL si fa a parte.
"""

import argparse
import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

from sanity_binary_pneo import SPLIT_DIR, PneoTiles, evaluate, load_mosaics
from baseline_swin_rsp_pneo import SwinBinary, RSP_CKPT


class PairedTiles(Dataset):
    """Stessa tile a due risoluzioni. Riusa due PneoTiles allineati sui record comuni."""

    def __init__(self, split, bands="rgb"):
        self.a = PneoTiles(SPLIT_DIR.format(res="0.3m") + f"/{split}.json", load_mosaics("0.3m"),
                           stats="official", bands=bands)
        self.b = PneoTiles(SPLIT_DIR.format(res="1.2m") + f"/{split}.json", load_mosaics("1.2m"),
                           stats="official", bands=bands)
        names_b = {r[0]["file_name"]: j for j, r in enumerate(self.b.records)}
        self.pairs = [(i, names_b[r[0]["file_name"]]) for i, r in enumerate(self.a.records)
                      if r[0]["file_name"] in names_b]

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, k):
        i, j = self.pairs[k]
        xa, y = self.a[i]
        xb, _ = self.b[j]
        return xa, xb, y


def cam_linear(model, feats):
    """CAM lineare differenziabile: feats (B,7,7,C) @ pesi della head -> (B,49) softmax."""
    w = model.head[1].weight.squeeze(0)          # (C,)
    cam = (feats * w).sum(-1)                    # (B,7,7)
    return F.softmax(cam.flatten(1), dim=1)


def train_phase(model, dl, val03, val12, lam, epochs, lr, cosine, tag, device):
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.05)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs) if cosine else None
    bce = nn.BCEWithLogitsLoss()
    best, best_state = 0.0, None
    for ep in range(epochs):
        model.train()
        tot = cons_tot = 0.0
        for xa, xb, y in dl:
            xa, xb, y = xa.to(device), xb.to(device), y.to(device)
            opt.zero_grad()
            fa = model.backbone.forward_features(xa)
            fb = model.backbone.forward_features(xb)
            la = model.head(fa.mean(dim=(1, 2))).squeeze(1)
            lb = model.head(fb.mean(dim=(1, 2))).squeeze(1)
            loss = 0.5 * (bce(la, y) + bce(lb, y))
            pos = y > 0.5
            cons = torch.tensor(0.0, device=device)
            if lam > 0 and pos.any():
                cons = ((cam_linear(model, fa[pos]) - cam_linear(model, fb[pos])) ** 2).sum(1).mean()
                loss = loss + lam * cons
            loss.backward()
            opt.step()
            tot += loss.item() * len(y)
            cons_tot += float(cons) * len(y)
        if sched:
            sched.step()
        f03 = evaluate(model, val03, device)
        f12 = evaluate(model, val12, device)
        score = 0.5 * (f03 + f12)
        if score > best:
            best = score
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        print(f"[{tag}] ep {ep + 1}/{epochs} loss {tot / len(dl.dataset):.4f} cons {cons_tot / len(dl.dataset):.4f} "
              f"| val F1 0.3m {f03:.4f} 1.2m {f12:.4f}")
    return best, best_state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lam", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--batch", type=int, default=60)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = "cuda"

    train = PairedTiles("train")
    print(f"coppie train: {len(train)}")
    dl = DataLoader(train, batch_size=args.batch, shuffle=True, num_workers=args.workers)
    mk = lambda res, split: DataLoader(
        PneoTiles(SPLIT_DIR.format(res=res) + f"/{split}.json", load_mosaics(res), stats="official"),
        batch_size=120, num_workers=8)
    val03, val12 = mk("0.3m", "val"), mk("1.2m", "val")
    test03, test12 = mk("0.3m", "test"), mk("1.2m", "test")

    model = SwinBinary(RSP_CKPT, in_chans=3).to(device)
    for p in model.backbone.parameters():
        p.requires_grad = False
    _, tl_state = train_phase(model, dl, val03, val12, args.lam, 10, 1e-3, False, "TL", device)
    if tl_state:
        model.load_state_dict(tl_state)
    for name, p in model.backbone.named_parameters():
        if "layers.3" in name or "norm" in name:
            p.requires_grad = True
    ft_best, ft_state = train_phase(model, dl, val03, val12, args.lam, 20, 1e-4, True, "FT", device)
    if ft_state:
        model.load_state_dict(ft_state)

    t03, t12 = evaluate(model, test03, device), evaluate(model, test12, device)
    out = os.path.expanduser(f"~/experiments/consistency_lam{args.lam}_seed{args.seed}.pt")
    torch.save(model.state_dict(), out)
    print(f"RISULTATO lam {args.lam} seed {args.seed}: best val medio {ft_best:.4f} | test F1 0.3m {t03:.4f} | test F1 1.2m {t12:.4f}")
    print(f"checkpoint: {out}")


if __name__ == "__main__":
    main()
