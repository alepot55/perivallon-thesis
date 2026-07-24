"""Derive 60 cm imagery from 30 cm imagery by 2x2 block averaging.

Each output pixel is the per-band mean of a 2x2 block of input pixels, so a
700x700 tile at 30 cm becomes a 350x350 tile at 60 cm. Georeferencing is kept
(pixel size doubled); odd trailing rows/cols are cropped. Integer inputs are
rounded back to the input dtype.

Usage:
    python derive_60cm.py input.tif output.tif
    python derive_60cm.py input_dir/ output_dir/    # converts every .tif inside

Note: block mean = boxcar downsampling. If the group prefers an MTF-matched
Gaussian filter before decimation (Wald protocol), only convert() changes.
"""

import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio import Affine


def block_mean_2x2(arr):
    """(bands, H, W) float array -> (bands, H//2, W//2) block means."""
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
    profile.update(
        width=out.shape[2],
        height=out.shape[1],
        transform=Affine(t.a * 2, t.b, t.c, t.d, t.e * 2, t.f),
    )
    with rasterio.open(dst_path, "w", **profile) as dst:
        dst.write(out)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        tifs = sorted(src.glob("*.tif"))
        for i, p in enumerate(tifs, 1):
            convert(p, dst / p.name)
            if i % 100 == 0:
                print(f"{i}/{len(tifs)}")
        print(f"done: {len(tifs)} files -> {dst}")
    else:
        convert(src, dst)
        print(f"done: {dst}")


if __name__ == "__main__":
    main()
