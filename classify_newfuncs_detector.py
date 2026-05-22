#!/usr/bin/env python3
"""
classify_newfuncs_detector.py
Run the FULL detector (PySR dual-route A_emlstar / B_re + SymPy judge) on the
phase-2 new base functions and their conjugates, to classify each as
holomorphic / anti-holomorphic, certified by the exact Wirtinger judge.

Pipeline identical to double_validation_v6.py: same operator defs, same
toolboxes, same PYSR config, same JSON format -> the result file can be fed
straight to verify_exact.py for certification.

Targets (each as a function of one complex input x0 = z):
  holomorphic candidates (functions of z only):
    sqrt(z), z**(3/2), z**(1/3), 1/z, arctan(z), arcsin(z), tan(z), sinh(z)
  anti-holomorphic candidates (same, of conj(z)):
    sqrt(conj z), arctan(conj z), 1/conj z, sinh(conj z)

Expected: holo targets -> 'holo' (no marker), anti targets -> 'anti'
(marker present). The judge (verify_exact.py) is the authority.

Usage:
    python3 -u classify_newfuncs_detector.py
    python3 verify_exact.py newfuncs_detector_result.json
Author: Anthony Monnerot, 2026.
"""
import json, numpy as np, sympy as sp
from datetime import datetime

try:
    from pysr import PySRRegressor
except ImportError:
    print("ERROR: PySR not installed."); exit(1)

EML_DEF     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR_DEF = "emlstar(x, y) = exp(x) - log(conj(y) + (1e-30 + 0im))"  # canonical A
MYREAL_DEF  = "my_real(z) = complex(real(z))"

EXTRA_SYMPY_MAPPINGS = {
    "eml": lambda x, y: sp.exp(x) - sp.log(y),
    "emlstar": lambda x, y: sp.exp(x) - sp.log(sp.conjugate(y)),
    "my_real": lambda z: sp.re(z),
}
TOOLBOXES = {
    "A_emlstar": dict(binary_operators=["+","-","*","/",EML_DEF,EMLSTAR_DEF],
                      unary_operators=["cos","sin","exp","log"], marker="emlstar"),
    "B_re": dict(binary_operators=["+","-","*","/",EML_DEF],
                 unary_operators=["cos","sin","exp","log",MYREAL_DEF], marker="my_real"),
}
PYSR_BASE = dict(niterations=100, population_size=50, precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    verbosity=1, progress=True, deterministic=True, parallelism="serial",
    random_state=42, maxsize=25, maxdepth=10)

TARGETS = {
    # holomorphic (function of z)
    "sqrt_z":       (lambda z: np.sqrt(z),                 "holo"),
    "z_pow_1p5":    (lambda z: z**1.5,                     "holo"),
    "z_pow_1o3":    (lambda z: z**(1/3),                   "holo"),
    "inv_z":        (lambda z: 1/z,                        "holo"),
    "arctan_z":     (lambda z: np.arctan(z),               "holo"),
    "sinh_z":       (lambda z: np.sinh(z),                 "holo"),
    # anti-holomorphic (function of conj z)
    "sqrt_conjz":   (lambda z: np.sqrt(np.conj(z)),        "anti"),
    "arctan_conjz": (lambda z: np.arctan(np.conj(z)),      "anti"),
    "inv_conjz":    (lambda z: 1/np.conj(z),               "anti"),
    "sinh_conjz":   (lambda z: np.sinh(np.conj(z)),        "anti"),
}

def make_data(fn, n=600, seed=42):
    rng = np.random.default_rng(seed)
    z = rng.uniform(-1.5,1.5,n) + 1j*rng.uniform(-2.5,2.5,n)
    z = z[np.abs(z) > 0.2]
    y = fn(z); good = np.isfinite(y)
    z, y = z[good], y[good]
    return z.reshape(-1,1).astype(np.complex128), y.astype(np.complex128)

def run_pysr(X, y, tb):
    allops = " ".join(tb["binary_operators"]+tb["unary_operators"])
    maps = {k:v for k,v in EXTRA_SYMPY_MAPPINGS.items() if k in allops}
    m = PySRRegressor(binary_operators=tb["binary_operators"],
                      unary_operators=tb["unary_operators"],
                      extra_sympy_mappings=maps, **PYSR_BASE)
    m.fit(X, y)
    return str(m.get_best()["equation"]), float(m.get_best()["loss"])

def main():
    results = {"timestamp": datetime.now().isoformat()+"+00:00", "runs": {}}
    n = len(TARGETS)*len(TOOLBOXES); done = 0
    for tname,(fn,expected) in TARGETS.items():
        print(f"\n{'='*60}\nTARGET: {tname}  (expected {expected})\n{'='*60}")
        X,y = make_data(fn)
        results["runs"].setdefault(tname, {})
        for tbn,tb in TOOLBOXES.items():
            done += 1
            print(f"[{done}/{n}] {tname} - {tbn} ...")
            eq,mse = run_pysr(X,y,tb)
            anti = tb["marker"] in eq
            print(f"  eq: {eq}\n  MSE: {mse:.2e}  marker {'found' if anti else 'absent'}")
            results["runs"][tname][tbn] = dict(best_equation=eq, best_mse=mse,
                anti_holomorphic=bool(anti), marker=tb["marker"])
        json.dump(results, open("newfuncs_detector_result.json","w"), indent=2)
    print("\nSaved newfuncs_detector_result.json")
    print("Now certify with: python3 verify_exact.py newfuncs_detector_result.json")

if __name__ == "__main__":
    main()
