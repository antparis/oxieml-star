#!/usr/bin/env python3
"""
test_gamma_full.py
Give PySR EVERYTHING and let it try to reconstruct the Gamma function.

This is an OPEN test: maximal toolbox, large budget, no built-in assumption
about the outcome. We simply measure how close PySR can get to Gamma and
contrast it with a known-elementary control (sin(z)*exp(z)) on the SAME
budget, so the comparison is fair.

Toolbox (maximal):
  binary: +, -, *, /, eml, eml*, eml0
  unary : exp, log, sin, cos, my_real, my_conj
Budget: large (niterations=200, population 60, maxsize 35) -- much bigger
than the elementary runs, to give Gamma every chance.

Targets:
  gamma_z   : the true Gamma(z)  (data from scipy)         -> open question
  control   : sin(z)*exp(z)      (known elementary)        -> sanity baseline

Interpretation:
  - control should reach ~1e-30 (PySR + budget can do elementary).
  - if gamma_z ALSO reaches ~1e-30 -> surprising, would need scrutiny.
  - if gamma_z plateaus far above (e.g. 1e-2..1e-6) while control nails it
    -> numerical evidence of the hypertranscendence wall (Hoelder).
  The MSE is the arbiter; nothing is hard-coded.

Usage:
    python3 -u test_gamma_full.py 2>&1 | tee gamma_full.log
Author: Anthony Monnerot, 2026.
"""
import numpy as np, sympy as sp
try:
    from scipy.special import gamma as scipy_gamma
except ImportError:
    print("ERROR: scipy needed (pip install scipy)"); exit(1)
try:
    from pysr import PySRRegressor
except ImportError:
    print("ERROR: PySR not installed"); exit(1)

EML_DEF     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR_DEF = "emlstar(x, y) = exp(x) - log(conj(y) + (1e-30 + 0im))"
EML0_DEF    = "eml0(x, y) = exp(x) - im*angle(y)"
MYREAL_DEF  = "my_real(z) = complex(real(z))"
MYCONJ_DEF  = "my_conj(z) = conj(z)"

EXTRA = {
    "eml":     lambda x, y: sp.exp(x) - sp.log(y),
    "emlstar": lambda x, y: sp.exp(x) - sp.log(sp.conjugate(y)),
    "eml0":    lambda x, y: sp.exp(x) - sp.I*sp.arg(y),
    "my_real": lambda z: sp.re(z),
    "my_conj": lambda z: sp.conjugate(z),
}

PYSR_BIG = dict(
    niterations=200, population_size=60, precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    verbosity=1, progress=True, deterministic=False, parallelism="multithreading",
    maxsize=35, maxdepth=12,
)

def make_data(fn, n=800, seed=42):
    rng = np.random.default_rng(seed)
    # Gamma blows up near non-positive integers; sample where it's well-behaved
    re = rng.uniform(0.3, 4.0, n)         # Re in (0,4]: Gamma smooth & finite
    im = rng.uniform(-1.5, 1.5, n)
    z = re + 1j*im
    y = fn(z); good = np.isfinite(y) & (np.abs(y) < 1e6)
    z, y = z[good], y[good]
    return z.reshape(-1,1).astype(np.complex128), y.astype(np.complex128)

def run(X, y, label):
    print(f"\n{'='*60}\n{label}: PySR with FULL toolbox\n{'='*60}")
    m = PySRRegressor(
        binary_operators=["+","-","*","/",EML_DEF,EMLSTAR_DEF,EML0_DEF],
        unary_operators=["exp","log","sin","cos",MYREAL_DEF,MYCONJ_DEF],
        extra_sympy_mappings=EXTRA, **PYSR_BIG)
    m.fit(X, y)
    eq  = str(m.get_best()["equation"]); mse = float(m.get_best()["loss"])
    print(f"  best eq : {eq}\n  MSE     : {mse:.3e}")
    return eq, mse

def main():
    res = {}
    # control: known elementary, same big budget
    Xc, yc = make_data(lambda z: np.sin(z)*np.exp(z))
    res["control_sin*exp"] = run(Xc, yc, "CONTROL sin(z)*exp(z)")[1]
    # the real test: Gamma
    Xg, yg = make_data(lambda z: scipy_gamma(z))
    res["gamma_z"] = run(Xg, yg, "GAMMA(z)")[1]

    print(f"\n{'='*60}\nSUMMARY\n{'='*60}")
    print(f"  control sin*exp (elementary) MSE = {res['control_sin*exp']:.2e}")
    print(f"  Gamma(z)                     MSE = {res['gamma_z']:.2e}")
    ratio = res["gamma_z"]/max(res["control_sin*exp"],1e-300)
    print(f"  Gamma is {ratio:.1e}x worse than the elementary control.")
    print("\nIf control nails ~1e-30 but Gamma plateaus far above, that is the")
    print("numerical signature of the hypertranscendence wall. The MSE decides.")

if __name__ == "__main__":
    main()
