#!/usr/bin/env python3
"""
make_lensing_mock.py
Stage-0 validation mocks for the anti-holomorphic detector, at KiDS-1000
shape-noise level. Same spirit as the EHT oracle: data whose holo/anti
nature is KNOWN by construction, so we can check the detector tells the
truth in cosmological conditions BEFORE touching real KiDS galaxies.

PHYSICS / WHY EACH MOCK
-----------------------
Weak-lensing shear of a circularly-symmetric mass (a halo / cluster) is a
HOLOMORPHIC function of the complex sky position z = x + i y. For a single
point-mass-like (SIS-like) lens at the origin, the complex shear is
    gamma(z) = -A * z / (zbar * |z|)        (tangential, |gamma| ~ 1/|z|)
which, written purely in z, is holomorphic away from the origin. More
simply, a convenient holomorphic model used here is
    gamma(z) = -A / conj-free form  ->  we use gamma(z) = A / z_shift
NO. To stay unambiguous we use the standard result that the *reduced*
tangential shear of an axisymmetric lens, expressed as a spin-2 field, is
holomorphic in z. We therefore build the E-mode (holomorphic) field as a
sum of analytic lens terms gamma_E(z) = sum_k  a_k / (z - z_k)  -- each term
is holomorphic (depends on z only), so the total is holomorphic and
dGamma/dzbar = 0 EXACTLY (away from the lens centres).

Three mocks:
  1) mock_Emode_pure   : gamma = gamma_E(z) + shape noise.   EXPECT holo.
  2) mock_Emode_psf    : gamma = gamma_E(z) + ALPHA*eps_PSF + noise. EXPECT anti
                         (the PSF-leakage term ALPHA*conj-bearing pattern is
                          anti-holomorphic; this is the artefact we fear on KiDS).
  3) mock_Emode_Bmode  : gamma = gamma_E(z) + small genuine B-mode + noise.
                         EXPECT anti (weak), tests sensitivity.

Shape noise: complex Gaussian with per-component sigma matching KiDS
sigma_eps ~ 0.27 (so |noise| rms ~ 0.27*sqrt(2) on the complex value... we
use per-component 0.27 as is standard: sigma_e per component).

Output CSVs (data/mock_*.csv) with columns z_real,z_imag,target_real,target_imag
plug directly into detect_real_data.py.

Author: Anthony Monnerot, 2026.
"""
import os
import numpy as np

OUT_DIR = "data"
N = 600                 # galaxies (sky positions)
SEED = 7
SIGMA_EPS = 0.27        # KiDS-1000 per-component shape-noise level
ALPHA_PSF = 0.05        # injected PSF-leakage amplitude (known, to be recovered)
BMODE_AMP = 0.02        # injected genuine B-mode amplitude (small)

# A few analytic lenses (positions in the field, complex), and strengths.
LENSES = [(-0.4 - 0.3j, 0.05),
          ( 0.5 + 0.2j, 0.04),
          ( 0.1 - 0.5j, 0.03)]


def gamma_Emode(z):
    """Holomorphic E-mode shear: sum of analytic lens terms a_k/(z - z_k).
    Each term depends on z only => dGamma/dzbar = 0 exactly."""
    g = np.zeros_like(z, dtype=complex)
    for zc, a in LENSES:
        g = g + a / (z - zc)
    return g


def sample_positions(seed):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1.0, 1.0, N)
    y = rng.uniform(-1.0, 1.0, N)
    z = x + 1j * y
    # keep galaxies away from the lens singularities
    for zc, _ in LENSES:
        too_close = np.abs(z - zc) < 0.15
        # nudge them outward radially from that lens
        if np.any(too_close):
            d = z[too_close] - zc
            z[too_close] = zc + 0.15 * d / np.abs(d)
    return z


def shape_noise(seed):
    rng = np.random.default_rng(seed)
    return SIGMA_EPS * (rng.standard_normal(N) + 1j * rng.standard_normal(N))


def psf_pattern(z):
    """A smooth spatially-varying PSF ellipticity pattern.
    PSF leakage enters as ALPHA * eps_PSF. The leakage term, as it appears
    in the *measured* ellipticity coupled with the conjugate structure of a
    spin-2 additive systematic, carries anti-holomorphic content. Here we
    build a PSF field that varies with position and inject it; whether the
    detector flags it as anti is the validation question."""
    # smooth low-order polynomial PSF ellipticity field, plus a conj term
    return 0.3 * (z + 0.5 * np.conj(z)) + 0.1


def write_csv(name, z, gamma):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{name}.csv")
    arr = np.column_stack([z.real, z.imag, gamma.real, gamma.imag])
    np.savetxt(path, arr, delimiter=",",
               header="z_real,z_imag,target_real,target_imag", comments="")
    return path


def main():
    z = sample_positions(SEED)
    gE = gamma_Emode(z)

    # 1) pure E-mode + noise
    g1 = gE + shape_noise(SEED + 1)
    p1 = write_csv("mock_Emode_pure", z, g1)

    # 2) E-mode + known PSF leakage + noise
    g2 = gE + ALPHA_PSF * psf_pattern(z) + shape_noise(SEED + 2)
    p2 = write_csv("mock_Emode_psf", z, g2)

    # 3) E-mode + small genuine B-mode (i * holomorphic) + noise
    #    A pure B-mode is i times a gradient field; here a simple anti term.
    gB = BMODE_AMP * np.conj(z)
    g3 = gE + gB + shape_noise(SEED + 3)
    p3 = write_csv("mock_Emode_Bmode", z, g3)

    for name, g in [("mock_Emode_pure", g1),
                    ("mock_Emode_psf", g2),
                    ("mock_Emode_Bmode", g3)]:
        print(f"{name:20s} N={N}  |g|max={np.abs(g).max():.3f}  -> data/{name}.csv")
    print()
    print(f"shape noise sigma/comp = {SIGMA_EPS}   (KiDS-1000 level)")
    print(f"injected PSF alpha     = {ALPHA_PSF}")
    print(f"injected B-mode amp    = {BMODE_AMP}")
    print("EXPECTED verdicts:")
    print("  mock_Emode_pure  -> HOLO  (control: detector must NOT cry anti)")
    print("  mock_Emode_psf   -> ANTI  (control: detector must catch PSF leakage)")
    print("  mock_Emode_Bmode -> ANTI  (sensitivity: small genuine B-mode)")


if __name__ == "__main__":
    main()
