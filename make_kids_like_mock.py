#!/usr/bin/env python3
"""
make_kids_like_mock.py
Dense KiDS-like mock to VALIDATE the pixel-averaging pipeline before touching
the real 16 GB KiDS file. Oracle spirit: holo/anti nature and all injected
systematics are KNOWN by construction.

Columns mimic the real KiDS-1000 SOM-gold WL catalogue we will use:
  RA, Dec, e1, e2, weight, PSF_e1, PSF_e2, MASK, fitclass, THELI_INT, c_e1, c_e2

KNOWN injected structure:
  - E-mode (holomorphic) shear:  A_E * z          (smooth linear, dGamma/dzbar=0)
  - genuine B-mode (anti):       BMODE_AMP * conj(z)
  - per-tile c-term:             constant complex offset per THELI_INT
                                 ALSO written out as columns c_e1,c_e2 so the
                                 pipeline can subtract the KNOWN value rather
                                 than re-estimating it from the data (re-
                                 estimation aspirates the cosmological signal).
  - PSF leakage:                 ALPHA_PSF * (PSF instrumental, independent of z)
  - shape noise:                 sigma_eps = 0.27 per component

Two lessons baked in (validated separately):
  1. The c-term must be subtracted using its KNOWN/published value, never
     re-estimated per tile on the data (that destroys the E- and B-mode).
  2. The PSF field is INSTRUMENTAL, independent of the lensing signal.

Author: Anthony Monnerot, 2026.
"""
import os
import numpy as np

OUT_DIR = "data"
OUT = os.path.join(OUT_DIR, "kids_like_mock.csv")

NGAL = 12000
SEED = 11
SIGMA_EPS = 0.27
A_E = 0.08 + 0.03j        # E-mode (holomorphic) amplitude
BMODE_AMP = 0.02          # genuine B-mode (anti) to recover after averaging
ALPHA_PSF = 0.05          # PSF leakage amplitude
PATCH_DEG = 2.0
TILEG = 8                 # 8x8 = 64 small tiles (E-mode ~ const within a tile)


def main():
    rng = np.random.default_rng(SEED)
    ra = rng.uniform(0.0, PATCH_DEG, NGAL)
    dec = rng.uniform(0.0, PATCH_DEG, NGAL)
    z = ((ra - PATCH_DEG / 2) + 1j * (dec - PATCH_DEG / 2)) / (PATCH_DEG / 2)

    # small-tile id
    tix = np.minimum((ra / PATCH_DEG * TILEG).astype(int), TILEG - 1)
    tiy = np.minimum((dec / PATCH_DEG * TILEG).astype(int), TILEG - 1)
    tile = tiy * TILEG + tix

    # per-tile c-term (known), drawn once per tile
    rng_c = np.random.default_rng(99)
    cmap = {t: (rng_c.uniform(-0.01, 0.01) + 1j * rng_c.uniform(-0.01, 0.01))
            for t in np.unique(tile)}
    cvec = np.array([cmap[t] for t in tile])

    # instrumental PSF field, independent of the lensing signal
    pu = (ra - PATCH_DEG / 2) / (PATCH_DEG / 2)
    pv = (dec - PATCH_DEG / 2) / (PATCH_DEG / 2)
    psf_e1 = 0.30 * np.cos(1.7 * pu + 0.5) + 0.20 * pv
    psf_e2 = 0.30 * np.sin(1.3 * pv - 0.4) - 0.20 * pu
    psf = psf_e1 + 1j * psf_e2

    # measured ellipticity
    gE = A_E * z
    gB = BMODE_AMP * np.conj(z)
    leak = ALPHA_PSF * psf
    noise = SIGMA_EPS * (rng.standard_normal(NGAL)
                         + 1j * rng.standard_normal(NGAL))
    eps = gE + gB + leak + cvec + noise
    e1, e2 = eps.real, eps.imag

    weight = rng.uniform(0.7, 1.0, NGAL)
    mask = np.zeros(NGAL, dtype=int)
    fitclass = np.zeros(NGAL, dtype=int)

    os.makedirs(OUT_DIR, exist_ok=True)
    arr = np.column_stack([ra, dec, e1, e2, weight, psf_e1, psf_e2,
                           mask, fitclass, tile, cvec.real, cvec.imag])
    header = ("RA,Dec,e1,e2,weight,PSF_e1,PSF_e2,MASK,fitclass,"
              "THELI_INT,c_e1,c_e2")
    np.savetxt(OUT, arr, delimiter=",", header=header, comments="",
               fmt=["%.6f", "%.6f", "%.6f", "%.6f", "%.4f", "%.6f", "%.6f",
                    "%d", "%d", "%d", "%.6f", "%.6f"])

    print(f"KiDS-like mock: {NGAL} galaxies, {TILEG}x{TILEG}={TILEG*TILEG} tiles, "
          f"{PATCH_DEG}x{PATCH_DEG} deg")
    print(f"  injected (KNOWN): E-mode A_E={A_E} (holo), B-mode={BMODE_AMP} (anti),")
    print(f"                    PSF leakage alpha={ALPHA_PSF} (instrumental),")
    print(f"                    per-tile c-term (columns c_e1,c_e2),")
    print(f"                    shape noise sigma/comp={SIGMA_EPS}")
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
