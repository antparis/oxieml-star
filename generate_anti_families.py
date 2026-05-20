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
}


def main():
    rng = np.random.default_rng(SEED)
    # Native complex sampling inside the strip |Im| < pi (use |Im|<=~0.8 to be safe,
    # matching the scale of the existing fractal datasets in [-1,1]^2).
    os.makedirs(OUT_DIR, exist_ok=True)

    for name, fn in FAMILIES.items():
        re = rng.uniform(-1.0, 1.0, N)
        im = rng.uniform(-1.0, 1.0, N)
        z = re + 1j * im
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
