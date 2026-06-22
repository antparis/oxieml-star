#!/usr/bin/env python3
"""
pysr_vortex_calib.py -- SHORT calibration run: can PySR (the translator/discoverer)
recover the composite-vortex anti structure from numerical data?

DATA (validated 3 ways before any PySR: judge=anti, num |d/dzbar|=0.55>>0):
  f(z) = (z/|z|)^n1 * exp(-c1|z|^2) + (z/|z|)^n2 * exp(-c2|z|^2),  n1!=n2.
This is anti-irreducible by construction (FINDINGS_20260621e).

PURPOSE: CALIBRATION, not discovery. We posed the form; PySR recovering it = the
translator is CAPABLE on this structure (capability, not revelation). If PySR plateaus,
distinguish budget limit (raise & retry) from STRUCTURAL ceiling (the (z/|z|)^n =
z^n*(z*zbar)^{-n/2} half-integer-exponent limit already hit in Aharonov-Bohm 2026-06-04).

SHORT run: niterations=40, populations=15, ~15 min target. GC guards for Julia.
Reads the FULL Hall of Fame (not just best) to see if PySR APPROACHES the structure.

Run detached:
  JULIA_NUM_GC_THREADS=1 setsid nohup python3 -u pysr_vortex_calib.py > pysr_vortex_calib.log 2>&1 &
"""
import numpy as np
import json

# ---- 1. Generate validated data (same as the 3-way-validated generator) ----
rng = np.random.default_rng(42)
N = 2000
r = rng.uniform(0.3, 2.0, N)
theta = rng.uniform(-np.pi, np.pi, N)
z = r * np.exp(1j*theta)
mod = np.abs(z)
n1, c1, n2, c2 = 1, 1.0, 2, 1.0
f = (z/mod)**n1 * np.exp(-c1*mod**2) + (z/mod)**n2 * np.exp(-c2*mod**2)

# Features: real coordinates. PySR works on real I/O.
x = z.real
y = z.imag
# Target: real part of f (one run). Imag part is a separate run if needed.
target = f.real

X = np.column_stack([x, y])           # features x, y
print(f"[data] N={N}, X shape={X.shape}, target=Re(f), range [{target.min():.3f},{target.max():.3f}]")

# ---- 2. PySR short calibration run ----
from pysr import PySRRegressor

model = PySRRegressor(
    niterations=40,
    populations=15,
    population_size=33,
    maxsize=30,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["exp", "square", "sqrt_abs(x) = sqrt(abs(x))"],
    extra_sympy_mappings={"sqrt_abs": lambda x: __import__("sympy").sqrt(__import__("sympy").Abs(x))},
    elementwise_loss="loss(prediction, target) = (prediction - target)^2",
    deterministic=False,
    parallelism="multithreading",
    random_state=0,
    verbosity=1,
)

print("[pysr] starting SHORT calibration fit (~15 min target)...")
model.fit(X, target)

# ---- 3. Read FULL Hall of Fame, not just best ----
print("\n" + "="*70)
print("HALL OF FAME (full -- to see if PySR APPROACHES the structure)")
print("="*70)
try:
    eqs = model.equations_
    for i, row in eqs.iterrows():
        print(f"  complexity={row['complexity']:>3}  loss={row['loss']:.3e}  {row['equation']}")
    best = eqs.loc[eqs['loss'].idxmin()]
    print("\n[best] loss=%.3e  eq=%s" % (best['loss'], best['equation']))
    print("[verdict] MSE < 1e-3 ? %s" % (best['loss'] < 1e-3))
    out = {"best_loss": float(best['loss']), "best_eq": str(best['equation']),
           "mse_below_1e-3": bool(best['loss'] < 1e-3),
           "note": "CALIBRATION: posed form. Recovering it = capability not discovery."}
    json.dump(out, open("pysr_vortex_calib_result.json","w"), indent=2)
    print("[saved] pysr_vortex_calib_result.json")
except Exception as e:
    print(f"[error reading HoF] {e}")

print("\n>>> Then: run the SymPy judge on the best formula. Marker is NOT the verdict.")
print(">>> If plateau: budget limit (raise niter/pop) vs structural ceiling (half-int exp)?")
