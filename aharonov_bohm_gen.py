#!/usr/bin/env python3
"""
aharonov_bohm_gen.py -- generator for the Aharonov-Bohm-in-magnetic-field
lowest-Landau-level wavefunction, the first POSITIVE chiral transcendental
anti-holomorphic candidate.

    psi(z, zbar) = z^(m + alpha/2) * zbar^(-alpha/2) * exp(-|z|^2 / (4 lB^2))

alpha = magnetic flux / flux quantum (gauge-invariant). The irrational power
zbar^(-alpha/2) is the transcendental, gauge-non-reducible anti-holomorphic
content, forced by the flux. Multivalued: branch fixed via polar form with
theta in (-pi, pi]; origin and the negative-real-axis branch cut are masked.

Outputs 4 CSV datasets (pipeline format z_real,z_imag,target_real,target_imag):
  ab_candidate.csv : alpha = sqrt(2)  -> transcendental chiral anti (1/zbar coeff = -alpha/2)
  ab_alpha0.csv    : alpha = 0        -> NO transcendental term (only the mirror Gaussian)
  ab_integer.csv   : alpha = 2        -> term present but integer => gauge-removable
  ab_shuffled.csv  : candidate with shuffled targets -> negative control (must be rejected)

NOTE on the discriminant: |d/dzbar|/|d/dz| (|mu|) is NONZERO for ALL alpha because
the real Gaussian exp(-|z|^2/4) contributes anti content. The TRUE discriminant is
the presence of the transcendental 1/zbar^(alpha/2) term, i.e. the coefficient of
1/zbar in (d psi/d zbar)/psi equals -alpha/2. alpha=0 has coeff 0 (no transcendental
anti); alpha=sqrt2 has coeff -0.7071 (transcendental); alpha=2 has coeff -1 but is
gauge-removable (single-valued (z/zbar)^1). The SymPy judge sees this exactly.

Author: Anthony Monnerot, 2026.
"""
import numpy as np
import csv, math

LB2 = 1.0   # 1/(4 lB^2) scale; exp(-|z|^2/4)

def psi_AB(z, alpha, m, lB2=LB2):
    r  = np.abs(z)
    th = np.angle(z)                 # principal branch (-pi, pi]
    p_z, p_zb = m + alpha/2, -alpha/2
    amp   = r**(p_z) * r**(p_zb) * np.exp(-r**2/(4*lB2))
    phase = np.exp(1j*th*p_z) * np.exp(-1j*th*p_zb)
    return amp*phase

def make_grid(N=70, L=2.5, rmin=0.15, cut_band=0.08):
    xs = np.linspace(-L, L, N)
    X, Y = np.meshgrid(xs, xs)
    z = (X + 1j*Y).ravel()
    z = z[np.abs(z) > rmin]                          # mask origin
    th = np.angle(z)
    z = z[np.abs(np.abs(th) - np.pi) > cut_band]     # mask branch cut (negative real axis)
    return z

def write_csv(path, z, V):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["z_real", "z_imag", "target_real", "target_imag"])
        for zi, Vi in zip(z, V):
            w.writerow([f"{zi.real:.18e}", f"{zi.imag:.18e}",
                        f"{Vi.real:.18e}", f"{Vi.imag:.18e}"])

def main():
    rng = np.random.default_rng(42)
    z = make_grid()
    m = 1
    print(f"grid: {len(z)} points (origin + branch cut masked)")

    # candidate: alpha = sqrt(2)
    Vc = psi_AB(z, math.sqrt(2), m)
    write_csv("ab_candidate.csv", z, Vc)
    # control alpha=0: no transcendental anti (only mirror Gaussian)
    V0 = psi_AB(z, 0.0, m)
    write_csv("ab_alpha0.csv", z, V0)
    # control alpha=2 integer: gauge-removable
    Vi = psi_AB(z, 2.0, m)
    write_csv("ab_integer.csv", z, Vi)
    # negative control: shuffled targets of the candidate
    idx = rng.permutation(len(Vc))
    write_csv("ab_shuffled.csv", z, Vc[idx])

    print("wrote ab_candidate.csv, ab_alpha0.csv, ab_integer.csv, ab_shuffled.csv")

if __name__ == "__main__":
    main()
