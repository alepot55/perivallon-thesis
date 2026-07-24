"""Build the 60 cm patch dataset from the 30 cm one.

Each 700x700 tile at 30 cm becomes a 350x350 tile at 60 cm by 2x2 block
averaging (see derive_60cm.py), keeping georeferencing and file names. The
per-band statistics in metadata.json are recomputed on the new tiles, since
averaging reduces the standard deviation.

Usage:
    python make_60cm_dataset.py <src_dir_30cm> <dst_dir_60cm>
"""

import json
import os
import sys

import numpy as np
import rasterio
from rasterio import Affine


def block_mean_2x2(arr):
    b, h, w = arr.shape
    h2, w2 = h // 2, w // 2
    arr = arr[:, : h2 * 2, : w2 * 2]
    return arr.reshape(b, h2, 2, w2, 2).mean(axis=(2, 4))


def convert(src_path, dst_path):
    with rasterio.open(src_path) as src:
        data = src.read()
        t = src.transform
        profile = src.profile.copy()
    out = block_mean_2x2(data.astype(np.float64))
    if np.issubdtype(data.dtype, np.integer):
        out = np.rint(out)
    out = out.astype(data.dtype)
    profile.update(width=out.shape[2], height=out.shape[1],
                   transform=Affine(t.a * 2, t.b, t.c, t.d, t.e * 2, t.f))
    with rasterio.open(dst_path, "w", **profile) as dst:
        dst.write(out)
    return out


def main():
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    meta = json.load(open(os.path.join(src, "metadata.json")))
    scale = float(meta["scale"])
    n_bands = int(meta["num_bands"])

    tifs = sorted(f for f in os.listdir(src) if f.endswith(".tif"))
    # running sums per band, on the 0-1 scaled values used by the training code
    s = np.zeros(n_bands)
    s2 = np.zeros(n_bands)
    count = 0
    for i, name in enumerate(tifs, 1):
        out = convert(os.path.join(src, name), os.path.join(dst, name))
        v = out.reshape(n_bands, -1).astype(np.float64) / scale
        s += v.sum(axis=1)
        s2 += (v ** 2).sum(axis=1)
        count += v.shape[1]
        if i % 200 == 0:
            print(f"{i}/{len(tifs)}", flush=True)

    mean = s / count
    std = np.sqrt(np.maximum(s2 / count - mean ** 2, 0))
    meta["img_folder"] = dst
    meta["num_files"] = len(tifs)
    for i, band in enumerate(meta["band_order"]):
        entry = meta["per_band"].get(band, {})
        entry["mean"] = float(mean[i])
        entry["std"] = float(std[i])
        entry["mean_raw"] = float(mean[i] * scale)
        entry["std_raw"] = float(std[i] * scale)
        meta["per_band"][band] = entry
    json.dump(meta, open(os.path.join(dst, "metadata.json"), "w"), indent=2)

    print(f"done: {len(tifs)} tiles -> {dst}")
    for band in meta["band_order"]:
        b = meta["per_band"][band]
        print(f"  {band}: mean {b['mean']:.4f} std {b['std']:.4f}")


if __name__ == "__main__":
    main()
