#!/usr/bin/env python3
"""
make_map_targets.py
Generate two targeted KiDS-like mocks to test, AT THE MAP LEVEL, whether
pixel-averaging unlocks the detector's sensitivity to a weak B-mode that was
invisible per-galaxy (Stage-0 showed the per-galaxy floor is ~0.02 at
sigma_eps=0.27).

Both mocks: holomorphic E-mode A_E*z + per-tile c-term (known cols) + shape
noise. NO PSF leakage (isolated test). They differ only by the B-mode:
  - map_Epure : B-mode amplitude 0       -> averaged map must be HOLO
  - map_EB    : B-mode amplitude 0.02    -> averaged map must be ANTI

After kids_pipeline.py --no-psf (c-term from known columns + averaging), the
detector should say holo on the first and anti on the second. That is the
proof that averaging beats the per-galaxy noise floor.

Author: Anthony Monnerot, 2026.
"""
import os
import numpy as np

OUT_DIR = "data"
NGAL = 200000   # large mock: realistic KiDS density, allows fine grid AND
                # many galaxies/pixel (per-pixel noise << B-mode signal)
SEED = 11
SIGMA_EPS = 0.27
A_E = 0.08 + 0.03j
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

    gE = A_E * z
    gB = bmode_amp * np.conj(z)
    noise = SIGMA_EPS * (rng.standard_normal(NGAL)
                         + 1j * rng.standard_normal(NGAL))
    eps = gE + gB + cvec + noise

    # no PSF leakage in these isolated tests; PSF columns set to zero
    psf_e1 = np.zeros(NGAL); psf_e2 = np.zeros(NGAL)
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
    print(f"{name:12s}: B-mode amp={bmode_amp}  -> data/{name}.csv  "
          f"(expect {'HOLO' if bmode_amp == 0 else 'ANTI'})")


def main():
    build("map_Epure", 0.0)
    build("map_EB", 0.02)


if __name__ == "__main__":
    main()
