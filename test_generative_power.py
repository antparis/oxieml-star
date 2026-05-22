#!/usr/bin/env python3
"""
test_generative_power.py
HONEST test of generative power: can the reference toolbox
{eml, eml*, my_real, +, -, *, /, const} RECONSTRUCT a candidate
EML-type operator? If yes (MSE ~ machine precision) -> the candidate is
EQUIVALENT to what eml* already gives (redundant). If PySR fails with a
large budget -> the candidate RESISTS reconstruction (a candidate for
genuine novelty -- NOT a proof of impossibility, see note below).

This is the real version of generative_power.py: PySR actually runs and
the MSE is the arbiter, not a hard-coded return.

Operator definitions copied VERBATIM from double_validation_v6.py to stay
consistent with the paper-v8 toolbox. eml* is the canonical A form
exp(x) - log(conj(y)).

Candidates tested (the non-trivial ones; trivial cases like id(z)-id(conj z)
= 2i*Im(z) are obviously reconstructible and skipped):
  1. exp(conj z) - log(z)         (the unnamed "mirror" hybrid)
  2. sin(z)      - cos(conj z)    (sin/cos hybrid: most likely to resist)
  3. sin(conj z) - cos(conj z)    (sin/cos pure anti-holomorphic)
  4. cos(z)      - log(conj z)    (mixed sin-cos / log hybrid)

Target data is generated EXACTLY (numpy), so the only question is whether
PySR can rebuild it from the reference toolbox.

NOTE ON INTERPRETATION (the SPARC/EHT lesson):
  - low MSE  => reconstructible => EQUIVALENT to eml* (solid conclusion)
  - high MSE => PySR could not rebuild it with this budget. This is
    [HEURISTIC] evidence of novelty, NOT proof: PySR failing is not a
    mathematical impossibility. A resistant candidate would then need a
    symbolic proof (paper-style lemma) before any "new operator" claim.

Usage:
    python3 -u test_generative_power.py
Author: Anthony Monnerot, 2026.
"""
import numpy as np
import sympy as sp

try:
    from pysr import PySRRegressor
except ImportError:
    print("ERROR: PySR not installed. pip install pysr")
    exit(1)

# ---- reference toolbox (verbatim from double_validation_v6.py) ----
EML_DEF     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR_DEF = "emlstar(x, y) = exp(x) - log(conj(y) + (1e-30 + 0im))"  # canonical A
MYREAL_DEF  = "my_real(z) = complex(real(z))"

EXTRA_SYMPY_MAPPINGS = {
    "eml": lambda x, y: sp.exp(x) - sp.log(y),
    "emlstar": lambda x, y: sp.exp(x) - sp.log(sp.conjugate(y)),  # canonical A
    "my_real": lambda z: sp.re(z),
}

PYSR_BASE = dict(
    niterations=100,
    population_size=50,
    precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    verbosity=1,
    progress=True,
    deterministic=True,
    parallelism="serial",
    random_state=42,
    maxsize=25,
    maxdepth=10,
)

# ---- candidate operators (as exact numpy functions of z) ----
CANDIDATES = {
    "mirror_exp_conj_minus_log":  lambda z: np.exp(np.conj(z)) - np.log(z),
    "sin_z_minus_cos_conj":       lambda z: np.sin(z) - np.cos(np.conj(z)),
    "sin_conj_minus_cos_conj":    lambda z: np.sin(np.conj(z)) - np.cos(np.conj(z)),
    "cos_z_minus_log_conj":       lambda z: np.cos(z) - np.log(np.conj(z)),
}

def make_data(fn, n=600, seed=42):
    rng = np.random.default_rng(seed)
    # sample inside the safe strip Im in (-pi,pi), avoid 0 for log
    re = rng.uniform(-1.5, 1.5, n)
    im = rng.uniform(-2.5, 2.5, n)
    z = re + 1j*im
    z = z[np.abs(z) > 0.2]            # keep away from log singularity
    y = fn(z)
    good = np.isfinite(y)
    z, y = z[good], y[good]
    X = z.reshape(-1, 1).astype(np.complex128)
    return X, y.astype(np.complex128)

def reconstruct(X, y):
    model = PySRRegressor(
        binary_operators=["+", "-", "*", "/", EML_DEF, EMLSTAR_DEF],
        unary_operators=["exp", "log", "sin", "cos", MYREAL_DEF],
        extra_sympy_mappings=EXTRA_SYMPY_MAPPINGS,
        **PYSR_BASE,
    )
    model.fit(X, y)
    eq  = str(model.get_best()["equation"])
    mse = float(model.get_best()["loss"])
    return eq, mse

def main():
    print("Reference toolbox: {eml, emlstar(A), my_real, +,-,*,/, exp,log,sin,cos}")
    print("Reconstructing each candidate; low MSE => EQUIVALENT, high => RESISTS\n")
    results = {}
    for name, fn in CANDIDATES.items():
        print(f"\n{'='*60}\nCANDIDATE: {name}\n{'='*60}")
        X, y = make_data(fn)
        print(f"  data: {len(y)} complex points")
        eq, mse = reconstruct(X, y)
        verdict = "EQUIVALENT (reconstructed)" if mse < 1e-15 else "RESISTS (candidate novelty)"
        print(f"  best eq : {eq}")
        print(f"  MSE     : {mse:.3e}")
        print(f"  verdict : {verdict}")
        results[name] = dict(mse=mse, eq=eq, verdict=verdict)

    print(f"\n{'='*60}\nSUMMARY\n{'='*60}")
    for name, r in results.items():
        print(f"  {name:34s} MSE={r['mse']:.2e}  {r['verdict']}")
    print("\nReminder: 'RESISTS' is [HEURISTIC] evidence only; PySR failing is")
    print("not a proof of impossibility. Resistant candidates need a symbolic")
    print("proof before any 'new operator' claim.")

if __name__ == "__main__":
    main()
