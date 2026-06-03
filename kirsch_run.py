#!/usr/bin/env python3
"""
kirsch_run.py -- PySR detector harness for the Kirsch closed-form datasets.

Why a separate harness:
  pysr_stacking.py is a stacking engine with a hard-coded LAYER_DATASETS map
  and is stable since 2026-05-23. Modifying it would risk side effects on
  the existing brick discoveries. This harness keeps pysr_stacking.py untouched
  and just runs the same toolbox (MIXTE) and the same ingestion convention on
  the three Kirsch CSVs.

Ingestion convention (verbatim from pysr_stacking.py lines 200-215):
    z = (df.iloc[:, 0] + 1j * df.iloc[:, 1]).astype(complex128)
    target = (df.iloc[:, 2] + 1j * df.iloc[:, 3]).astype(complex128)
    X = z.reshape(-1, 1)            # ONE complex feature (no SPARC trap)

Toolbox (verbatim, MIXTE):
    binary  : +, -, *, /, eml, emlstar
    unary   : sin, cos, exp, log, my_conj, my_real, my_imag, my_abs2
    emlstar(x,y) = exp(x) - log(conj(y))   (conj on the 2nd arg only)

Per-dataset PySR config is conservative; tweakable via flags.

The verdict is NEVER the marker. The official judge (verify_exact.py) must
certify the best_equation; MSE >= 1e-3 invalidates the claim regardless.
This harness writes one JSON per dataset and prints the judge commands.

Author: Anthony Monnerot, 2026. English only.
"""

import argparse
import json
import os
import time
import numpy as np
import pandas as pd
import sympy as sp

try:
    from pysr import PySRRegressor
except ImportError:
    raise SystemExit("ERROR: PySR not installed. pip install pysr")


# ---------------------------------------------------------------------------
# Toolbox -- MIXTE, copied verbatim from pysr_stacking.py (lines 152-174)
# ---------------------------------------------------------------------------
def build_toolbox():
    binary_operators = [
        "+", "-", "*", "/",
        "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))",
        "emlstar(x, y) = exp(x) - log(conj(y) + (1e-30 + 0im))",
    ]
    unary_operators = [
        "sin", "cos", "exp", "log",
        "my_conj(z) = conj(z)",
        "my_real(z) = complex(real(z))",
        "my_imag(z) = complex(imag(z))",
        "my_abs2(z) = z * conj(z)",
    ]
    extra_sympy_mappings = {
        "eml": lambda x, y: sp.exp(x) - sp.log(y),
        "emlstar": lambda x, y: sp.exp(x) - sp.log(sp.conjugate(y)),  # MIXTE
        "my_conj": lambda z: sp.conjugate(z),
        "my_real": lambda z: sp.re(z),
        "my_imag": lambda z: sp.im(z),
        "my_abs2": lambda z: z * sp.conjugate(z),
    }
    return binary_operators, unary_operators, extra_sympy_mappings


# ---------------------------------------------------------------------------
# One-dataset run
# ---------------------------------------------------------------------------
def run_one(csv_path, label, niter, pop, maxsize, parsimony, out_dir, verbose):
    print()
    print("=" * 74)
    print(f"PYSR -- {label}  (csv={csv_path})")
    print("=" * 74)
    if not os.path.exists(csv_path):
        msg = f"missing CSV: {csv_path}"
        print(f"  ERROR: {msg}")
        return {"label": label, "csv": csv_path, "error": msg}

    df = pd.read_csv(csv_path)
    z = (df.iloc[:, 0].values + 1j * df.iloc[:, 1].values).astype(np.complex128)
    y = (df.iloc[:, 2].values + 1j * df.iloc[:, 3].values).astype(np.complex128)
    X = z.reshape(-1, 1)
    print(f"  rows: {len(z)}   X.shape={X.shape}   complex inputs OK")

    binops, unops, smap = build_toolbox()
    model = PySRRegressor(
        niterations=niter,
        population_size=pop,
        maxsize=maxsize,
        parsimony=parsimony,
        binary_operators=binops,
        unary_operators=unops,
        extra_sympy_mappings=smap,
        precision=64,
        parallelism="multithreading",
        deterministic=False,
        verbosity=1 if verbose else 0,
        progress=False,
        tempdir=os.path.join(out_dir, f"pysr_output_kirsch_{label}"),
    )
    t0 = time.time()
    model.fit(X, y)
    dt = time.time() - t0
    best = model.get_best()
    eq = str(best["equation"])
    mse = float(best["loss"])
    print(f"  done in {dt:.1f}s")
    print(f"  best_mse  = {mse:.3e}")
    print(f"  best_eq   = {eq}")
    return {
        "label": label,
        "csv": csv_path,
        "best_equation": eq,
        "best_mse": mse,
        "mse_below_1e-3": bool(mse < 1e-3),
        "complexity": int(best["complexity"]) if "complexity" in best else None,
        "elapsed_s": dt,
        "toolbox": "MIXTE (verbatim pysr_stacking.py)",
        "pysr_config": dict(niterations=niter, population_size=pop, maxsize=maxsize,
                            parsimony=parsimony, precision=64,
                            parallelism="multithreading", deterministic=False),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--niter", type=int, default=60)
    ap.add_argument("--pop", type=int, default=300)
    ap.add_argument("--maxsize", type=int, default=30)
    ap.add_argument("--parsimony", type=float, default=0.001)
    ap.add_argument("--only", choices=["all", "kirsch", "holo", "shuf"], default="all")
    ap.add_argument("--out_dir", default=".")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    datasets = [
        ("kirsch", "kirsch_closed_form.csv"),
        ("holo",   "kirsch_holo_control.csv"),
        ("shuf",   "kirsch_shuffled.csv"),
    ]
    if args.only != "all":
        datasets = [(lbl, csv) for (lbl, csv) in datasets if lbl == args.only]

    bundle = {"script": "kirsch_run.py", "results": {}}
    for label, csv in datasets:
        r = run_one(csv, label, args.niter, args.pop, args.maxsize, args.parsimony,
                    args.out_dir, verbose=not args.quiet)
        bundle["results"][label] = r
        with open(f"kirsch_{label}_result.json", "w") as fh:
            json.dump(r, fh, indent=2)
        print(f"  [written] kirsch_{label}_result.json")

    with open("kirsch_run_summary.json", "w") as fh:
        json.dump(bundle, fh, indent=2)

    print()
    print("=" * 74)
    print("SUMMARY")
    print("=" * 74)
    for label, _ in datasets:
        r = bundle["results"][label]
        if "error" in r:
            print(f"  {label}: ERROR {r['error']}")
            continue
        flag = "OK" if r["mse_below_1e-3"] else "FAIL (MSE >= 1e-3)"
        print(f"  {label:6s}  MSE={r['best_mse']:.3e}  [{flag}]")
        print(f"          eq = {r['best_equation']}")

    print()
    print("OFFICIAL CERTIFICATION -- paste each (the judge is the only authority):")
    for label, _ in datasets:
        r = bundle["results"][label]
        if "error" in r:
            continue
        eq = r["best_equation"].replace('"', '\\"')
        print(f'    python3 verify_exact.py --formula "{eq}"   # {label}')
    print()
    print("Expected (to verify):")
    print("  kirsch -> judge dw/dzbar != 0  (anti/mixed)  AND  MSE < 1e-3")
    print("  holo   -> judge dw/dzbar == 0  (holomorphic) AND  MSE < 1e-3")
    print("  shuf   -> REJECTED at MSE (>> 1e-3) regardless of marker")
    print()
    print("Honest reading: a clean pass = VALIDATION of a 1933-classical")
    print("Kolosov-Muskhelishvili decomposition recovered blindly by symbolic")
    print("regression from time-free spatial data. NOT a discovery about nature.")


if __name__ == "__main__":
    main()
