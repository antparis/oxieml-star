#!/usr/bin/env python3
"""
optical_vortex_to_csv.py
Adapter: turn the Laguerre-Gauss optical vortex (physics from
optical_vortex_gen.py) into the synthetic-battery CSV format
(z_real,z_imag,target_real,target_imag) consumed by kirsch_stack.run_one,
so the optical vortex goes through the CERTIFIED pipeline
(PySR -> verify_exact judge -> reality_check), exactly like vortex_N1.

Physics (unchanged from optical_vortex_gen.py):
    beam(l) ~ z^l * exp(-|z|^2/w^2)        for l >= 0  (holomorphic phase)
    beam(l) ~ conj(z)^|l| * exp(-|z|^2/w^2) for l < 0   (anti-holomorphic phase)
We send the ENVELOPE-DIVIDED field (explicit analysis choice): anti -> conj(z)^3,
holo -> z^3. Clean ALGEBRAIC monomial the judge can certify.

Targets:
    optical_anti.csv : l=-3 envelope divided -> conj(z)^3  (expect ANTI, complex)
    optical_holo.csv : l=+3 envelope divided -> z^3        (expect HOLO)
    optical_shuf.csv : optical_anti targets shuffled       (negative control)

NOTE: CALIBRATION on a physical (optical) system, ALGEBRAIC anti (monomial),
NOT the transcendental log(zbar) of vortex_N1.

Author: Anthony Monnerot, 2026.
"""
import numpy as np
import pandas as pd

W = 2.0
N = 80
L = 3
SEED = 0

def grid():
    xs = np.linspace(-3, 3, N)
    ys = np.linspace(-3, 3, N)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    return (X + 1j * Y).ravel()

def beam_envdiv(Z, l):
    if l >= 0:
        return Z ** l
    return np.conj(Z) ** abs(l)

def mask_center(Z, f, rmin=0.15):
    m = np.abs(Z) > rmin
    return Z[m], f[m]

def write_csv(path, Z, f):
    df = pd.DataFrame({
        "z_real": Z.real, "z_imag": Z.imag,
        "target_real": f.real, "target_imag": f.imag,
    })
    df.to_csv(path, index=False)
    return df

def main():
    Z = grid()
    Za, fa = mask_center(Z, beam_envdiv(Z, -L))
    write_csv("optical_anti.csv", Za, fa)
    Zh, fh = mask_center(Z, beam_envdiv(Z, +L))
    write_csv("optical_holo.csv", Zh, fh)
    rng = np.random.default_rng(SEED)
    idx = rng.permutation(len(fa))
    write_csv("optical_shuf.csv", Za, fa[idx])
    for name, Zc, fc in [("anti", Za, fa), ("holo", Zh, fh)]:
        cmplx = bool(np.any(np.abs(fc.imag) > 1e-12))
        print(f"optical_{name}.csv  N={len(Zc)}  |Im(z)|max={np.abs(Zc.imag).max():.3f}  target_complex={cmplx}")
    print(f"optical_shuf.csv  N={len(Za)}  (anti targets permuted)")

if __name__ == "__main__":
    main()
