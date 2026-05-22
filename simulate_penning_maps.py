#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simulate_penning_maps.py

SANITY CHECK (NOT a discovery) for the eml / eml-star / eml-zero detector.

Goal
----
The transverse motion of a charged particle in a Penning trap is natively
complex: rho = x + i*y (Cohen-Tannoudji, College de France 1984-85, transp.
II-1 / II-4). The radial dynamics splits into circular components of opposite
chirality (the "quanta circulaires droit/gauche" a_d, a_g of the course),
and a squeezing / Bogoliubov transformation mixes the amplitude alpha with its
conjugate alpha* (the S(xi) operation in J. Foo's trapped-ion control scheme).

A time curve rho(t) is parametrised by REAL time t, so feeding it to a
d/dz-bar judge is meaningless (conj(t) = t -> the SPARC artefact). What is
genuinely testable is the set of *maps of the complex plane* z = x+iy -> f(z)
that the trap physics provides. Each map below is natively complex (x and y
sampled independently over a 2D region) and its holomorphic character is
GUARANTEED by exact mathematics. We therefore know the expected verdict in
advance: this validates the detector, it does not discover anything.

Maps generated
--------------
  HOLO    f(z) = e^{i theta} * z                      -> ground truth: holomorphic
  ANTI    f(z) = e^{i theta} * conj(z)                -> ground truth: anti-holomorphic
  HYBRID  f(z) = cosh(r)*z + e^{i phi} sinh(r)*conj(z) -> ground truth: hybrid (squeezing)
  HOLO_SHUFFLED  negative control: imaginary part of the HOLO output is
                 randomly permuted, destroying the holomorphic structure.
                 The detector must NOT classify it as clean holomorphic.

Outputs
-------
  penning_holo.csv
  penning_anti.csv
  penning_hybrid.csv
  penning_holo_shuffled.csv
Columns: z_re, z_im, f_re, f_im  (NATIVELY COMPLEX input AND output)

NOTE ON COLUMN NAMES: these are generic. Adapt them to whatever your
pysr_stacking.py loader expects (the detector pipeline runs on YOUR machine;
this script only manufactures the natively-complex data).

The script also prints an EXACT SymPy certification of d f / d z-bar and
d f / d z for each map (Wirtinger derivatives). That symbolic check is the
authoritative ground truth (what the SymPy judge ought to recover). It is NOT
a claim that PySR works -- the actual detector run (PySR + verify_exact.py)
must be executed on your machine.

Status of what this script establishes:
  [ESTABLISHED] the exact holomorphic class of each map (SymPy, below).
  [PENDING]     whether the detector recovers it (your PySR + judge run).
"""

import numpy as np
import pandas as pd
import sympy as sp


# ----------------------------------------------------------------------
# 1. Physical parameters (illustrative; classification is independent of
#    their exact values as long as theta != 0 and r > 0).
#    Values inspired by Cohen-Tannoudji transp. II-5: B0 = 1.8 T,
#    w_c/2pi ~ 51 GHz. We only need a representative non-trivial angle.
# ----------------------------------------------------------------------
THETA = 1.0          # rotation angle (rad); stands for w'_c * dt, generic non-zero
R_SQUEEZE = 0.6      # squeezing parameter r (>0 -> genuine hybrid)
PHI = 0.7            # squeezing phase phi (rad)

N_POINTS = 4000      # number of natively-complex samples
RADIUS = 2.0         # sampling radius in the complex plane
SEED = 20260522      # reproducibility


def sample_complex_plane(n, radius, seed):
    """Sample z = x + i*y with x and y INDEPENDENT (natively complex)."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(-radius, radius, size=n)
    y = rng.uniform(-radius, radius, size=n)
    return x + 1j * y


def to_frame(z, f):
    return pd.DataFrame(
        {"z_re": z.real, "z_im": z.imag, "f_re": f.real, "f_im": f.imag}
    )


def main():
    z = sample_complex_plane(N_POINTS, RADIUS, SEED)

    # --- the three physical maps -------------------------------------
    c = np.exp(1j * THETA)                       # complex constant e^{i theta}
    f_holo = c * z                               # cyclotron rotation
    f_anti = c * np.conj(z)                       # opposite-chirality / mirror
    f_hybrid = (np.cosh(R_SQUEEZE) * z
                + np.exp(1j * PHI) * np.sinh(R_SQUEEZE) * np.conj(z))  # squeezing

    # --- negative control: destroy holomorphic structure -------------
    rng = np.random.default_rng(SEED + 1)
    f_holo_shuffled = f_holo.copy()
    perm = rng.permutation(len(f_holo_shuffled))
    f_holo_shuffled = f_holo_shuffled.real + 1j * f_holo_shuffled.imag[perm]

    datasets = {
        "penning_holo.csv": to_frame(z, f_holo),
        "penning_anti.csv": to_frame(z, f_anti),
        "penning_hybrid.csv": to_frame(z, f_hybrid),
        "penning_holo_shuffled.csv": to_frame(z, f_holo_shuffled),
    }

    print("=" * 70)
    print("NATIVELY-COMPLEX CHECK (input z and output f both genuinely 2D)")
    print("=" * 70)
    for name, df in datasets.items():
        # correlation between Im(z) and Im(f): if ~0 and structure is real,
        # we would risk a SPARC-type degeneracy. Here we just report ranges.
        df.to_csv(name, index=False)
        print(f"{name:28s}  n={len(df)}  "
              f"z_im in [{df.z_im.min():+.2f},{df.z_im.max():+.2f}]  "
              f"f_im in [{df.f_im.min():+.2f},{df.f_im.max():+.2f}]")

    # ------------------------------------------------------------------
    # 2. EXACT SymPy ground truth (Wirtinger derivatives).
    #    d/dz-bar = 1/2 (d/dx + i d/dy);  d/dz = 1/2 (d/dx - i d/dy).
    #    holomorphic  <=> d f / d z-bar == 0
    #    anti-holo    <=> d f / d z     == 0
    # ------------------------------------------------------------------
    print()
    print("=" * 70)
    print("EXACT GROUND TRUTH  [ESTABLISHED by SymPy]  (authoritative)")
    print("=" * 70)

    x, y = sp.symbols("x y", real=True)
    th = sp.Rational(0)  # symbolic check independent of theta; use general const
    theta = sp.symbols("theta", real=True)
    r = sp.symbols("r", positive=True)
    phi = sp.symbols("phi", real=True)
    I = sp.I
    zc = x + I * y  # complex z built from real x, y

    def wirtinger(fexpr):
        dfdzbar = sp.simplify((sp.diff(fexpr, x) + I * sp.diff(fexpr, y)) / 2)
        dfdz = sp.simplify((sp.diff(fexpr, x) - I * sp.diff(fexpr, y)) / 2)
        return dfdz, dfdzbar

    maps = {
        "HOLO    e^{i th} z":
            sp.exp(I * theta) * zc,
        "ANTI    e^{i th} conj(z)":
            sp.exp(I * theta) * sp.conjugate(zc),
        "HYBRID  cosh(r) z + e^{i ph} sinh(r) conj(z)":
            sp.cosh(r) * zc + sp.exp(I * phi) * sp.sinh(r) * sp.conjugate(zc),
    }

    for label, fexpr in maps.items():
        dfdz, dfdzbar = wirtinger(fexpr)
        is_holo = dfdzbar == 0
        is_anti = dfdz == 0
        if is_holo and not is_anti:
            verdict = "HOLOMORPHIC"
        elif is_anti and not is_holo:
            verdict = "ANTI-HOLOMORPHIC"
        elif is_holo and is_anti:
            verdict = "CONSTANT"
        else:
            verdict = "HYBRID"
        print(f"\n{label}")
        print(f"    d f / d z      = {dfdz}")
        print(f"    d f / d z-bar  = {dfdzbar}")
        print(f"    -> GROUND TRUTH: {verdict}")

    print()
    print("=" * 70)
    print("Expected detector verdicts (what your PySR + verify_exact.py "
          "should recover):")
    print("  penning_holo.csv            -> HOLO")
    print("  penning_anti.csv            -> ANTI")
    print("  penning_hybrid.csv          -> HYBRID")
    print("  penning_holo_shuffled.csv   -> NOT clean HOLO (negative control)")
    print("=" * 70)
    print("\nReminder: no MSE / no PySR verdict is produced here. Those are")
    print("VALID ONLY after execution on your machine + the SymPy judge.")


if __name__ == "__main__":
    main()
