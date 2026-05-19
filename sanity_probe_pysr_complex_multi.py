#!/usr/bin/env python3
"""
sanity_probe_pysr_complex_multi.py

Verify that PySRRegressor accepts X.shape=(N, 2) with dtype=np.complex128
on this machine before launching the full Run A v2.
"""

import json
import os
import random
import sys
from datetime import datetime, timezone

import numpy as np

N_SAMPLES = 200
DOMAIN_HALF_WIDTH = np.pi - 0.05
NUMPY_SEED = 42
PYTHON_RANDOM_SEED = 42
PYSR_RANDOM_STATE = 42

PYSR_NITERATIONS = 10
PYSR_POPULATION_SIZE = 100
PYSR_MAXSIZE = 15

LOSS_THRESHOLD = 1e-20

JSON_OUT = "sanity_probe_result.json"
OUTPUT_DIR = "pysr_output_sanity_probe"


def sample_complex(rng, n):
    re = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=n)
    im = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=n)
    if not (np.all(np.abs(re) <= DOMAIN_HALF_WIDTH)
            and np.all(np.abs(im) <= DOMAIN_HALF_WIDTH)):
        raise RuntimeError("Domain guard violated during sampling")
    return (re + 1j * im).astype(np.complex128)


def main():
    random.seed(PYTHON_RANDOM_SEED)
    np.random.seed(NUMPY_SEED)
    rng = np.random.default_rng(NUMPY_SEED)

    z = sample_complex(rng, N_SAMPLES)
    w = sample_complex(rng, N_SAMPLES)

    X = np.column_stack([z, w]).astype(np.complex128)
    y = (z * w).astype(np.complex128)

    assert X.shape == (N_SAMPLES, 2), f"unexpected X.shape={X.shape}"
    assert X.dtype == np.complex128, f"unexpected X.dtype={X.dtype}"
    assert y.shape == (N_SAMPLES,), f"unexpected y.shape={y.shape}"
    assert y.dtype == np.complex128, f"unexpected y.dtype={y.dtype}"

    print(f"[probe] X.shape={X.shape} X.dtype={X.dtype}", flush=True)
    print(f"[probe] y.shape={y.shape} y.dtype={y.dtype}", flush=True)
    print(f"[probe] seeds: numpy={NUMPY_SEED} "
          f"python_random={PYTHON_RANDOM_SEED} "
          f"pysr_random_state={PYSR_RANDOM_STATE}", flush=True)

    import pysr
    from pysr import PySRRegressor

    pysr_version = str(getattr(pysr, "__version__", "unknown"))
    print(f"[probe] pysr_version={pysr_version}", flush=True)

    model = PySRRegressor(
        niterations=PYSR_NITERATIONS,
        population_size=PYSR_POPULATION_SIZE,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sin", "cos", "exp", "log"],
        maxsize=PYSR_MAXSIZE,
        multithreading=True,
        deterministic=False,
        random_state=PYSR_RANDOM_STATE,
        precision=64,
        output_directory=OUTPUT_DIR,
        progress=True,
        verbosity=1,
    )

    model.fit(X, y)

    eqs = model.equations_
    if eqs is None or len(eqs) == 0:
        raise RuntimeError("PySR returned no equations")

    loss_col = "loss" if "loss" in eqs.columns else "Loss"
    eq_col = "equation" if "equation" in eqs.columns else "Equation"
    cx_col = "complexity" if "complexity" in eqs.columns else "Complexity"

    print("[probe] top 3 rows of model.equations_:", flush=True)
    for i, (_, row) in enumerate(eqs.head(3).iterrows()):
        print(f"  [{i}] complexity={int(row[cx_col])} "
              f"loss={float(row[loss_col]):.6e} "
              f"equation={str(row[eq_col])}", flush=True)

    best_row = eqs.loc[eqs[loss_col].idxmin()]
    best_equation = str(best_row[eq_col])
    best_loss = float(best_row[loss_col])
    best_complexity = int(best_row[cx_col])

    uses_x0 = "x0" in best_equation
    uses_x1 = "x1" in best_equation
    loss_ok = best_loss < LOSS_THRESHOLD

    status = "OK" if (uses_x0 and uses_x1 and loss_ok) else "FAIL"

    print(f"[probe] best_equation: {best_equation}", flush=True)
    print(f"[probe] best_complexity: {best_complexity}", flush=True)
    print(f"[probe] best_loss: {best_loss:.6e}", flush=True)
    print(f"[probe] uses_x0={uses_x0} uses_x1={uses_x1} loss_ok={loss_ok}",
          flush=True)
    print(f"PROBE_STATUS: {status}", flush=True)

    result = {
        "status": status,
        "best_equation": best_equation,
        "best_loss": best_loss,
        "best_complexity": best_complexity,
        "uses_x0": bool(uses_x0),
        "uses_x1": bool(uses_x1),
        "loss_threshold": float(LOSS_THRESHOLD),
        "n_samples": int(N_SAMPLES),
        "dtype": str(X.dtype),
        "shape": list(X.shape),
        "pysr_version": pysr_version,
        "seeds_used": {
            "numpy": int(NUMPY_SEED),
            "python_random": int(PYTHON_RANDOM_SEED),
            "pysr_random_state": int(PYSR_RANDOM_STATE),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "top3_pareto": [
            {
                "complexity": int(row[cx_col]),
                "loss": float(row[loss_col]),
                "equation": str(row[eq_col]),
            }
            for _, row in eqs.head(3).iterrows()
        ],
        "notes": "deterministic=False + multithreading=True; seeds logged for traceability only.",
    }

    tmp_path = JSON_OUT + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(result, f, indent=2)
    os.replace(tmp_path, JSON_OUT)
    print(f"[probe] wrote {JSON_OUT}", flush=True)

    sys.exit(0 if status == "OK" else 1)


if __name__ == "__main__":
    main()
