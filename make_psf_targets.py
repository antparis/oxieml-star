#!/usr/bin/env python3
"""
make_psf_targets.py
Two mocks WITH a known PSF leakage, to test that the published-alpha PSF
subtraction is SURGICAL: it removes the anti-holomorphic PSF artefact WITHOUT
destroying a genuine B-mode.

Both: holomorphic E-mode A_E*z + known per-tile c-term + PSF leakage
ALPHA_PSF*psf (psf instrumental, partly collinear with the signal) + noise.
They differ only by the B-mode:
  - psf_noB : B-mode 0     -> after subtracting ALPHA_PSF*psf, must be HOLO
  - psf_B   : B-mode 0.02  -> after subtracting ALPHA_PSF*psf, must be ANTI

The PSF columns PSF_e1,PSF_e2 are written so the pipeline can subtract
alpha*psf with the PUBLISHED alpha (here ALPHA_PSF, the value we injected,
playing the role of the externally-measured KiDS alpha).

Author: Anthony Monnerot, 2026.
"""
import os
import numpy as np

OUT_DIR = "data"
NGAL = 200000
SEED = 11
SIGMA_EPS = 0.27
A_E = 0.08 + 0.03j
ALPHA_PSF = 0.05          # injected leakage = the "published" alpha to subtract
PATCH_DEG = 2.0
TILEG = 8


def build(name, bmode_amp):
    rng = np.random.default_rng(SEED)
    ra = rng.uniform(0.0, PATCH_DEG, NGAL)
    dec = rng.uniform(0.0, PATCH_DEG, NGAL)
    z = ((ra - PATCH_DEG / 2) + 1j * (dec - PATCH_DEG / 2)) / (PATCH_DEG / 2)

    tix = np.minimum((ra / PATCH_DEG * TILEG).astype(int), TILEG - 1)
    tiy = np.minimum((dec / PATCH_DEG * TILEG).astype(int), TILEG - 1)
    tile = tiy * TILEG + tix

    rng_c = np.random.default_rng(99)
    cmap = {t: (rng_c.uniform(-0.01, 0.01) + 1j * rng_c.uniform(-0.01, 0.01))
            for t in np.unique(tile)}
    cvec = np.array([cmap[t] for t in tile])

    pu = (ra - PATCH_DEG / 2) / (PATCH_DEG / 2)
    pv = (dec - PATCH_DEG / 2) / (PATCH_DEG / 2)
    psf_e1 = 0.30 * np.cos(1.7 * pu + 0.5) + 0.20 * pv
    psf_e2 = 0.30 * np.sin(1.3 * pv - 0.4) - 0.20 * pu
    psf = psf_e1 + 1j * psf_e2

    gE = A_E * z
    gB = bmode_amp * np.conj(z)
    leak = ALPHA_PSF * psf
    noise = SIGMA_EPS * (rng.standard_normal(NGAL)
                         + 1j * rng.standard_normal(NGAL))
    eps = gE + gB + leak + cvec + noise

    weight = rng.uniform(0.7, 1.0, NGAL)
    mask = np.zeros(NGAL, dtype=int); fitclass = np.zeros(NGAL, dtype=int)

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{name}.csv")
    arr = np.column_stack([ra, dec, eps.real, eps.imag, weight,
                           psf_e1, psf_e2, mask, fitclass, tile,
                           cvec.real, cvec.imag])
    header = ("RA,Dec,e1,e2,weight,PSF_e1,PSF_e2,MASK,fitclass,"
              "THELI_INT,c_e1,c_e2")
    np.savetxt(path, arr, delimiter=",", header=header, comments="",
               fmt=["%.6f", "%.6f", "%.6f", "%.6f", "%.4f", "%.6f", "%.6f",
                    "%d", "%d", "%d", "%.6f", "%.6f"])
    exp = "HOLO" if bmode_amp == 0 else "ANTI"
    print(f"{name:10s}: B={bmode_amp}  PSF leakage alpha={ALPHA_PSF}  "
          f"-> data/{name}.csv  (after PSF subtraction expect {exp})")


def main():
    build("psf_noB", 0.0)
    build("psf_B", 0.02)
    print()
    print(f"Published alpha to pass to the pipeline: --alpha {ALPHA_PSF} 0")


if __name__ == "__main__":
    main()
