#!/usr/bin/env python3
"""Multicore segfault smoke test for B2. Not a scientific run."""
import os
os.environ.setdefault("JULIA_NUM_GC_THREADS", "1")
import sys
import numpy as np
import pandas as pd

CSV = "data/b2_shear.csv"
N_PROCS = 4

def main():
    if not os.path.exists(CSV):
        print(f"ERROR: {CSV} not found. Run: python3 b2_shear_run.py --gen")
        sys.exit(1)
    from pysr_stacking import build_operators
    from verify_exact import certify
    from pysr import PySRRegressor

    df = pd.read_csv(CSV)
    z = (df.iloc[:, 0].values + 1j * df.iloc[:, 1].values).astype(np.complex128)
    y = (df.iloc[:, 2].values + 1j * df.iloc[:, 3].values).astype(np.complex128)
    if len(z) > 200:
        rng = np.random.default_rng(0)
        idx = rng.choice(len(z), 200, replace=False)
        z, y = z[idx], y[idx]

    binary_ops, unary_ops, sympy_maps = build_operators([])
    print(f"[test] backend  : multithreading, procs={N_PROCS}, "
          f"JULIA_NUM_GC_THREADS={os.environ['JULIA_NUM_GC_THREADS']}")
    print(f"[test] config   : maxsize=12, niterations=40, points={len(z)}")
    print(f"[test] starting PySR ... (Julia compiles first; be patient)")

    model = PySRRegressor(
        niterations=40,
        population_size=50,
        precision=64,
        elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
        maxsize=12,
        maxdepth=8,
        verbosity=1,
        deterministic=False,
        parallelism="multithreading",
        procs=N_PROCS,
        binary_operators=binary_ops,
        unary_operators=unary_ops,
        extra_sympy_mappings=sympy_maps,
    )
    model.fit(z.reshape(-1, 1), y)
    y_pred = model.predict(z.reshape(-1, 1))
    mse = float(np.mean(np.abs(y - y_pred) ** 2))
    best_eq = str(model.get_best()["equation"])

    print("\n" + "=" * 56)
    print("SEGFAULT TEST RESULT")
    print("=" * 56)
    print(f"  finished without crash : YES")
    print(f"  best_equation          : {best_eq}")
    print(f"  MSE                    : {mse:.3e}")
    try:
        verdict, expr, dfdzbar = certify(best_eq)
        print(f"  judge verdict          : {verdict}  (sanity only)")
    except Exception as e:
        print(f"  judge parse note       : {e}")
    print("-" * 56)
    print("  -> multithreading is SAFE on this machine.")
    print("=" * 56)

if __name__ == "__main__":
    main()
