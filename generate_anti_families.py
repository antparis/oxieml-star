#!/usr/bin/env python3
"""
generate_anti_families.py
Generate clean, natively-complex datasets covering DIFFERENT families of
anti-holomorphic structure (not just the Tricorn motif conj(z)^2+c).
All inputs z are drawn natively in the complex plane (no artificial real->
complex encoding), inside |Im(z)| < pi to respect the log branch condition
used by emlstar. This avoids the SPARC-type encoding artefact.
Families generated:
  conj_linear  : conj(z) + c          (pure anti, degree 1)
  mod_squared  : z * conj(z) = |z|^2  (mixed holo x anti; real-valued output)
  mixed_deg3   : z * conj(z)^2        (mixed, conjugation-dominant)
  holo_control : z^2 + c              (holomorphic control)
Extended families (verdicts certified by the SymPy judge, df/d(zbar)):
  anti_conj_cube : conj(z)^3          (pure anti, degree 3)
  anti_exp_conj  : exp(conj(z))       (anti, TRANSCENDENTAL)
  anti_re_z2     : Re(z^2)            (anti, real-valued output)
  holo_exp       : exp(z)             (holomorphic, transcendental control)
  holo_trap_inv  : conj(1/conj(z))=1/z(holomorphic trap: anti*anti cancels)
Output CSVs use the standard columns z_real,z_imag,target_real,target_imag
so they plug directly into double_validation_v3.py.
Author: Anthony Monnerot, 2026.
"""
import os
import numpy as np
import pandas as pd
OUT_DIR = "data"
N = 200
SEED = 42
C = -0.7 + 0.27015j   # same constant as the fractal datasets
FAMILIES = {
    "anti_conj_linear": lambda z: np.conj(z) + C,
    "anti_mod_squared": lambda z: z * np.conj(z),
    "anti_mixed_deg3":  lambda z: z * np.conj(z) ** 2,
    "holo_control":     lambda z: z ** 2 + C,
    # --- extended families (judge-certified via df/d(zbar)) ---
    "anti_conj_cube":   lambda z: np.conj(z) ** 3,       # anti, degree 3
    "anti_exp_conj":    lambda z: np.exp(np.conj(z)),    # anti, transcendental
    "anti_re_z2":       lambda z: np.real(z ** 2) + 0j,  # anti, real-valued
    "holo_exp":         lambda z: np.exp(z),             # holo, transcendental
    "holo_trap_inv":    lambda z: 1.0 / z,               # holo, 1/z (trap)
}
# Families whose target diverges near the origin; module is clipped to >=0.1
# for these only, leaving the rng state (and the existing CSVs) untouched.
CLIP_ORIGIN = {"holo_trap_inv"}
def main():
    rng = np.random.default_rng(SEED)
    # Native complex sampling inside the strip |Im| < pi (use |Im|<=~0.8 to be safe,
    # matching the scale of the existing fractal datasets in [-1,1]^2).
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fn in FAMILIES.items():
        re = rng.uniform(-1.0, 1.0, N)
        im = rng.uniform(-1.0, 1.0, N)
        z = re + 1j * im
        if name in CLIP_ORIGIN:
            # push points too close to 0 out to radius 0.1, preserving phase
            small = np.abs(z) < 0.1
            if np.any(small):
                z[small] = 0.1 * np.exp(1j * np.angle(z[small]))
        t = fn(z)
        df = pd.DataFrame({
            "z_real": z.real,
            "z_imag": z.imag,
            "target_real": t.real,
            "target_imag": t.imag,
        })
        path = os.path.join(OUT_DIR, f"{name}.csv")
        df.to_csv(path, index=False)
        # quick self-report
        target_is_complex = bool(np.any(np.abs(t.imag) > 1e-9))
        print(f"{name:20s} N={N}  |Im(z)|max={np.abs(z.imag).max():.3f}  "
              f"target_complex={target_is_complex}  -> {path}")
if __name__ == "__main__":
    main()
