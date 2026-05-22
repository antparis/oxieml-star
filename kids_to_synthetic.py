#!/usr/bin/env python3
"""
kids_to_synthetic.py
Convert the real KiDS PSF field into the synthetic-battery CSV format used by
double_validation_v6.py / verify_exact.py, so the eml* detector can be run on
real complex data WITHOUT modifying the existing pipeline.

Mapping (test A, the PSF field):
    input   z = RA + i*Dec            (sky position, complex)
    target  f = PSF_e1 + i*PSF_e2     (PSF anisotropy, complex, raw)

Why a SQUARE PATCH (critical, methodology)
------------------------------------------
The contiguous subsample covers RA ~109 deg x Dec ~6 deg: a ratio ~18:1 strip.
Under the mandatory ISOTROPIC rescaling (anisotropic scaling would destroy the
conformal structure and hence the holo/anti-holo distinction), such a strip
makes z almost purely real (z_imag ~ z_real / 18). On the real line conj(z)=z,
so eml* collapses onto eml and the test becomes DEGENERATE -- this is exactly
the SPARC "conj(x)=x on R" trap, in geometric form.
Fix: cut a near-square patch (full Dec height, equal RA width) so z is a
genuine 2D field. The PSF varies on ~degree scales, so 5000 points over a
~6x6 deg patch over-determine a smooth field by a wide margin.

Isotropic rescaling
-------------------
    z = (RA - mean_RA)/s + i*(Dec - mean_Dec)/s
    s = sqrt(var(dRA) + var(dDec))     # single isotropic scale (RMS radius)
The SAME s on both axes preserves angles (conformality). f is left RAW
(PSF ~1e-3, already small; rescaling f would not change holo/anti structure).

Negative control (the real arbiter on noisy real data)
------------------------------------------------------
On a noisy real fit the exact judge's "df/d(zbar)==0" test is too strict: a
tiny parasitic term always makes it say "anti". So the control is decisive:
we write a SHUFFLED dataset where the (z) positions are permuted independently
of f, breaking the position<->PSF link while keeping both marginals intact.
  - if real AND shuffled both look "anti"  -> the "anti" is an artifact (SPARC)
  - if real looks "anti" but shuffled does not (or MSE far worse) -> candidate

Outputs:
    data/kids_psf.csv           z_real,z_imag,target_real,target_imag
    data/kids_psf_shuffled.csv  same columns, positions shuffled vs f

Usage:
    python3 kids_to_synthetic.py --in data/kids_real.csv --n 5000 --seed 42
Author: Anthony Monnerot, 2026.
"""
import argparse
import os
import numpy as np
import pandas as pd


def square_patch(df):
    """Cut a near-square sky patch: full Dec height, equal RA width, centred
    on the densest RA band. Returns the sub-DataFrame and patch bounds."""
    ra = df["RA"].values
    dec = df["Dec"].values
    dec_span = dec.max() - dec.min()           # target width in RA too
    nbins = max(1, int(np.ceil((ra.max() - ra.min()) / dec_span)))
    counts, edges = np.histogram(ra, bins=nbins)
    k = int(np.argmax(counts))
    ra_lo = edges[k]
    ra_hi = ra_lo + dec_span
    mask = (ra >= ra_lo) & (ra < ra_hi)
    return df[mask].copy(), (ra_lo, ra_hi, dec.min(), dec.max())


def to_complex_frame(sub, seed, n):
    """Isotropic-rescale z, keep f raw, subsample to n. Returns a DataFrame
    with z_real,z_imag,target_real,target_imag and a scale-info dict."""
    ra = sub["RA"].values.astype(np.float64)
    dec = sub["Dec"].values.astype(np.float64)
    f1 = sub["PSF_e1"].values.astype(np.float64)
    f2 = sub["PSF_e2"].values.astype(np.float64)

    mean_ra, mean_dec = ra.mean(), dec.mean()
    d_ra = ra - mean_ra
    d_dec = dec - mean_dec
    s = np.sqrt(d_ra.var() + d_dec.var())      # isotropic scale (RMS radius)
    z_real = d_ra / s
    z_imag = d_dec / s

    rng = np.random.default_rng(seed)
    m = len(ra)
    if n < m:
        idx = rng.choice(m, size=n, replace=False)
    else:
        idx = np.arange(m)

    out = pd.DataFrame({
        "z_real": z_real[idx],
        "z_imag": z_imag[idx],
        "target_real": f1[idx],
        "target_imag": f2[idx],
    })
    info = dict(mean_ra=mean_ra, mean_dec=mean_dec, scale=s,
                n_patch=m, n_out=len(out),
                z_real_std=float(z_real[idx].std()),
                z_imag_std=float(z_imag[idx].std()))
    return out, info


def make_shuffled(df_real, seed):
    """Permute (z_real,z_imag) jointly, independently of the target. Breaks
    the position<->PSF link; keeps both marginal distributions intact."""
    rng = np.random.default_rng(seed + 1)
    perm = rng.permutation(len(df_real))
    shuf = df_real.copy()
    shuf["z_real"] = df_real["z_real"].values[perm]
    shuf["z_imag"] = df_real["z_imag"].values[perm]
    return shuf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", default="data/kids_real.csv")
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out_real", default="data/kids_psf.csv")
    ap.add_argument("--out_shuffled", default="data/kids_psf_shuffled.csv")
    args = ap.parse_args()

    df = pd.read_csv(args.infile)
    print(f"loaded {len(df)} galaxies from {args.infile}", flush=True)
    print(f"  full coverage: RA [{df['RA'].min():.2f}, {df['RA'].max():.2f}], "
          f"Dec [{df['Dec'].min():.2f}, {df['Dec'].max():.2f}]", flush=True)

    sub, (ra_lo, ra_hi, dec_lo, dec_hi) = square_patch(df)
    print(f"square patch: RA [{ra_lo:.2f}, {ra_hi:.2f}] "
          f"Dec [{dec_lo:.2f}, {dec_hi:.2f}] -> {len(sub)} galaxies", flush=True)
    if len(sub) < args.n:
        print(f"  WARNING: patch has only {len(sub)} galaxies (< n={args.n}); "
              f"using all of them.", flush=True)

    df_real, info = to_complex_frame(sub, args.seed, args.n)
    print(f"isotropic scale s = {info['scale']:.4f} deg", flush=True)
    ratio = info['z_real_std'] / max(info['z_imag_std'], 1e-12)
    print(f"  z_real std = {info['z_real_std']:.3f}, "
          f"z_imag std = {info['z_imag_std']:.3f}  (ratio {ratio:.2f}:1)",
          flush=True)
    print(f"  -> {info['n_out']} points", flush=True)

    os.makedirs(os.path.dirname(args.out_real) or ".", exist_ok=True)
    df_real.to_csv(args.out_real, index=False)
    print(f"wrote {args.out_real}", flush=True)

    df_shuf = make_shuffled(df_real, args.seed)
    df_shuf.to_csv(args.out_shuffled, index=False)
    print(f"wrote {args.out_shuffled}  (positions shuffled vs PSF)", flush=True)


if __name__ == "__main__":
    main()
