#!/usr/bin/env python3
"""
hasegawa_mima_gen.py
Screened Hasegawa-Mima single drift-wave vortex. Projet-A target: anti-holo
FORCED by finite ion-sound Larmor radius rho_s, transcendental (log zbar),
NON-removable. Encadrement proven analytically + SymPy-verified:
  psi = (Gamma/2pi) K0(|z|/rho_s)        (real, screened Poisson)
  w   = -(i Gamma/2pi rho_s) K1(|z|/rho_s) zbar/|z|
  dw/dzbar = (i Gamma/4pi rho_s^2) K0(|z|/rho_s) != 0 at finite rho_s
  w -> -i Gamma/(2pi z), dw/dzbar -> 0  ONLY as rho_s -> oo
Raw complex velocity w fed directly (NO envelope division): anti is forced.

Regime: strong screening rho_s=0.3 on a short domain -> anti is dominant
(residual/total ~ 1.6), not buried under the holomorphic point-vortex term.
Sandbox check: PySR-accessible {1/z, zbar, zbar*log(zz), ...} fits to MSE~2e-7.

Datasets:
  hm_vortex.csv : rho_s=0.3 finite       -> expect ANTI (log zbar)
  hm_holo.csv   : rho_s=1e6 (unscreened)  -> expect HOLO (-iG/2pi z)  [encadrement control]
  hm_shuf.csv   : hm_vortex shuffled      -> negative control
CSV: z_real,z_imag,target_real,target_imag

Author: Anthony Monnerot, 2026.
"""
import numpy as np
import pandas as pd
from scipy.special import kv

GAMMA = 1.0
RHO_S = 0.3
RHO_BIG = 1.0e6
N = 90
HALF = 0.6
RMIN = 0.05
SEED = 0

def grid(half, n):
    xs = np.linspace(-half, half, n); ys = np.linspace(-half, half, n)
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    return (X + 1j * Y).ravel()

def velocity(Z, gamma, rho_s):
    r = np.abs(Z)
    return -(1j * gamma / (2 * np.pi * rho_s)) * kv(1, r / rho_s) * (np.conj(Z) / r)

def mask_core(Z, f, rmin):
    m = np.abs(Z) > rmin
    return Z[m], f[m]

def write_csv(path, Z, f):
    pd.DataFrame({"z_real": Z.real, "z_imag": Z.imag,
                  "target_real": f.real, "target_imag": f.imag}).to_csv(path, index=False)

def main():
    Z = grid(HALF, N)
    Zv, fv = mask_core(Z, velocity(Z, GAMMA, RHO_S), RMIN)
    write_csv("hm_vortex.csv", Zv, fv)
    Zh, fh = mask_core(Z, velocity(Z, GAMMA, RHO_BIG), RMIN)
    write_csv("hm_holo.csv", Zh, fh)
    rng = np.random.default_rng(SEED)
    write_csv("hm_shuf.csv", Zv, fv[rng.permutation(len(fv))])
    print(f"hm_vortex.csv N={len(Zv)} |z|max={np.abs(Zv).max():.3f} rho_s={RHO_S}")
    print(f"hm_holo.csv   N={len(Zh)} rho_s={RHO_BIG:.0e} (unscreened)")
    print(f"hm_shuf.csv   N={len(Zv)} (shuffled)")
    err = np.max(np.abs(fh - (-(1j*GAMMA)/(2*np.pi*Zh))))
    dev = np.max(np.abs(fv - (-(1j*GAMMA)/(2*np.pi*Zv))))
    print(f"\nhm_holo vs -iG/(2pi z): max err = {err:.2e} (should be ~0)")
    print(f"hm_vortex vs -iG/(2pi z): max dev = {dev:.3e} (should be large)")

if __name__ == "__main__":
    main()
