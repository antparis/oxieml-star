#!/usr/bin/env python3
"""
kids_pipeline.py
Cleaning + pixel-averaging pipeline for a KiDS-like shear catalogue, turning a
raw galaxy catalogue into a clean pixel-averaged complex shear map for the
anti-holomorphic detector, with known additive systematics removed.

Steps (the "SPARC lesson" guardrail), in order:
  1. quality cuts: MASK==0, fitclass==0, weight>0
  2. c-term subtraction using the KNOWN/published per-tile value (columns
     c_e1,c_e2). NEVER re-estimate the c-term from the data: re-estimation
     subtracts the cosmological signal along with the systematic (validated:
     re-estimation drove recovered E/B from 0.085/0.020 down to 0.001/0.001).
  3. PSF-leakage regression: weighted complex alpha from eps ~ alpha*eps_PSF,
     subtract alpha*eps_PSF. Stable only when the PSF amplitude is large
     enough to dominate noise; for real KiDS prefer the published alpha.
  4. pixel-averaging: weighted-mean residual per grid cell (noise ~1/sqrt(N)).

Output: data/<base>_map.csv  (z_real,z_imag,target_real,target_imag).

Usage:
  python3 kids_pipeline.py data/kids_like_mock.csv --grid 6
  python3 kids_pipeline.py <cat.csv> --grid 6 --no-psf   # skip PSF step
  Options: --cterm-cols c_e1 c_e2   (known c-term columns; default these)

Author: Anthony Monnerot, 2026.
"""
import os
import argparse
import numpy as np
import pandas as pd


def log(m):
    print(m, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--grid", type=int, default=6, help="NxN pixel grid")
    ap.add_argument("--min-per-pixel", type=int, default=20)
    ap.add_argument("--no-psf", action="store_true",
                    help="skip PSF-leakage subtraction")
    ap.add_argument("--alpha", nargs=2, type=float, default=[0.0, 0.0],
                    metavar=("RE", "IM"),
                    help="PUBLISHED complex PSF-leakage alpha (re im); "
                         "never regressed on the data")
    ap.add_argument("--cterm-cols", nargs=2, default=["c_e1", "c_e2"],
                    help="known c-term column names (real, imag)")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    log(f"Loaded {len(df)} galaxies from {args.csv}")

    # 1. quality cuts
    m = (df["MASK"] == 0) & (df["fitclass"] == 0) & (df["weight"] > 0)
    df = df[m].copy()
    log(f"  after quality cuts: {len(df)}")

    ra = df["RA"].to_numpy(); dec = df["Dec"].to_numpy()
    e = df["e1"].to_numpy() + 1j * df["e2"].to_numpy()
    w = df["weight"].to_numpy()
    psf = df["PSF_e1"].to_numpy() + 1j * df["PSF_e2"].to_numpy()

    # 2. c-term subtraction using KNOWN columns (never re-estimate)
    cc1, cc2 = args.cterm_cols
    if cc1 in df.columns and cc2 in df.columns:
        cterm = df[cc1].to_numpy() + 1j * df[cc2].to_numpy()
        e = e - cterm
        log(f"  c-term subtracted from known columns ({cc1},{cc2}) "
            f"-- NOT re-estimated")
    else:
        log(f"  WARNING: c-term columns ({cc1},{cc2}) absent; SKIPPING c-term "
            f"(do NOT re-estimate from data)")

    # 3. PSF-leakage subtraction using a PUBLISHED alpha (NEVER regressed on
    #    the data). Regressing alpha on the science data is degenerate: the PSF
    #    field can be partly collinear with the lensing signal, so the fit
    #    aspirates the E-mode and biases everything (validated by failure).
    #    KiDS measures alpha independently on star fields (Giblin 2021); pass it
    #    via --alpha re im. Default 0 0 = skip (equivalent to --no-psf).
    if not args.no_psf:
        ar, ai = args.alpha
        alpha = ar + 1j * ai
        if alpha == 0:
            log("  PSF step: alpha=0 given, nothing subtracted "
                "(use --alpha re im with the PUBLISHED value)")
        else:
            e = e - alpha * psf
            log(f"  PSF leakage subtracted with PUBLISHED alpha = {alpha:.4f} "
                f"(NOT regressed on data)")
    else:
        log("  PSF step skipped (--no-psf)")

    # 4. pixel-averaging
    G = args.grid
    ra0, ra1 = ra.min(), ra.max()
    dec0, dec1 = dec.min(), dec.max()
    ix = np.clip(((ra - ra0) / (ra1 - ra0) * G).astype(int), 0, G - 1)
    iy = np.clip(((dec - dec0) / (dec1 - dec0) * G).astype(int), 0, G - 1)
    cell = iy * G + ix

    # normalized complex coordinate for pixel centers
    zc_all = ((ra - (ra0 + ra1) / 2) + 1j * (dec - (dec0 + dec1) / 2)) \
        / ((ra1 - ra0) / 2)

    rows, ngals = [], []
    for c in np.unique(cell):
        sel = cell == c
        ngal = int(sel.sum())
        if ngal < args.min_per_pixel:
            continue
        wsel = w[sel]
        gbar = np.sum(wsel * e[sel]) / np.sum(wsel)
        zbar = np.sum(wsel * zc_all[sel]) / np.sum(wsel)   # weighted center
        rows.append((zbar.real, zbar.imag, gbar.real, gbar.imag))
        ngals.append(ngal)

    out = os.path.splitext(args.csv)[0] + "_map.csv"
    np.savetxt(out, np.array(rows), delimiter=",",
               header="z_real,z_imag,target_real,target_imag", comments="")
    med = int(np.median(ngals))
    log(f"  pixel grid {G}x{G}: {len(rows)} pixels (>= {args.min_per_pixel} gal); "
        f"median {med} gal/pixel; noise/pixel ~ {0.27/np.sqrt(med):.4f}")
    log(f"  -> {out}")


if __name__ == "__main__":
    main()
