#!/usr/bin/env python3
"""
fetch_kids_subsample.py
Download a contiguous subsample of the real KiDS-1000 SOM-gold WL catalogue
WITHOUT fetching the full 16.5 GB file, using an HTTP Range request.

The catalogue is a single FITS binary table:
  - 193 columns, 21,262,011 rows, 833 bytes/row
  - data start at byte offset 169920 (after primary + table headers)
The server supports 'accept-ranges: bytes', so we grab only the header plus
the first N rows (~833*N bytes), patch NAXIS2 to N so astropy can parse it,
apply the KiDS quality cuts, and write a CSV in the detector/pipeline format:
  RA,Dec,e1,e2,weight,PSF_e1,PSF_e2,MASK,fitclass,THELI_INT

NOTE: this is a CONTIGUOUS subsample (the first N catalogue rows), which is a
specific sky region, not a random draw. Fine for a methodology test; for a
science result one would stream the whole catalogue or several regions.

Usage:
  python3 fetch_kids_subsample.py --n 250000 --out data/kids_real.csv

Author: Anthony Monnerot, 2026.
"""
import argparse
import io
import re
import urllib.request
import numpy as np
from astropy.io import fits

URL = ("https://kids.strw.leidenuniv.nl/DR4/data_files/"
       "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
DATA_OFF = 169920     # byte offset where the binary data begin
ROW = 833             # bytes per row
NTOTAL = 21262011     # total rows in the catalogue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=250000,
                    help="number of catalogue rows to fetch (before cuts)")
    ap.add_argument("--out", default="data/kids_real.csv")
    args = ap.parse_args()

    n = min(args.n, NTOTAL)
    end = DATA_OFF + ROW * n
    print(f"Fetching header + first {n} rows "
          f"(~{ROW * n / 1e6:.1f} MB) via HTTP Range ...", flush=True)
    req = urllib.request.Request(URL, headers={"Range": f"bytes=0-{end-1}"})
    raw = urllib.request.urlopen(req, timeout=300).read()
    print(f"  got {len(raw)} bytes", flush=True)

    # patch NAXIS2 to n so astropy parses only what we downloaded
    hdr = raw[:DATA_OFF].decode("latin-1")
    hdr = re.sub(r"NAXIS2  =\s*\d+", f"NAXIS2  = {n:>20}", hdr, count=1)
    body = raw[DATA_OFF:]
    pad = (-len(body)) % 2880
    buf = hdr.encode("latin-1") + body + b"\0" * pad

    hdul = fits.open(io.BytesIO(buf))
    t = hdul[1].data
    print(f"  parsed {len(t)} rows", flush=True)

    # quality cuts
    good = (t["MASK"] == 0) & (t["fitclass"] == 0) & (t["weight"] > 0)
    t = t[good]
    print(f"  after cuts (MASK==0, fitclass==0, weight>0): {len(t)}", flush=True)

    out_arr = np.column_stack([
        np.asarray(t["RAJ2000"], float),
        np.asarray(t["DECJ2000"], float),
        np.asarray(t["e1"], float),
        np.asarray(t["e2"], float),
        np.asarray(t["weight"], float),
        np.asarray(t["PSF_e1"], float),
        np.asarray(t["PSF_e2"], float),
        np.asarray(t["MASK"], float),
        np.asarray(t["fitclass"], float),
        np.asarray(t["THELI_INT"], float),
    ])
    header = "RA,Dec,e1,e2,weight,PSF_e1,PSF_e2,MASK,fitclass,THELI_INT"
    np.savetxt(args.out, out_arr, delimiter=",", header=header, comments="",
               fmt=["%.6f", "%.6f", "%.6f", "%.6f", "%.4f", "%.6f", "%.6f",
                    "%d", "%d", "%d"])
    print(f"  -> {args.out}  ({len(t)} galaxies)", flush=True)
    print()
    ra = np.asarray(t["RAJ2000"], float); dec = np.asarray(t["DECJ2000"], float)
    print(f"  sky coverage: RA [{ra.min():.2f}, {ra.max():.2f}], "
          f"Dec [{dec.min():.2f}, {dec.max():.2f}] deg")


if __name__ == "__main__":
    main()
