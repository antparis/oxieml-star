#!/usr/bin/env python3
"""
kirsch_stack.py -- Harness "B" for Kirsch: PySR with inv(z)=1/z and
inv_bar(z)=1/conj(z) given as PRIMITIVES on top of the standard MIXTE toolbox.

Why this is not cheating
  The real difficulty of the Kirsch displacement is NOT to discover 1/z (banal).
  It is to find the right COMBINATION of z, conj(z), 1/z, 1/conj(z) and the more
  exotic z/conj(z)^3 with the right coefficients. Adding 1/z and 1/conj(z) as
  primitives removes the trivial step and lets PySR concentrate its budget on
  the combinatorial structure -- which is the only thing worth testing here.

Toolbox (extends MIXTE by two unary ops):
  binary  : +, -, *, /, eml, emlstar
  unary   : sin, cos, exp, log, my_conj, my_real, my_imag, my_abs2,
            inv(z) = 1/z, inv_bar(z) = 1/conj(z)
  (emlstar = exp(x) - log(conj(y)) -- MIXTE, conj on 2nd arg only)

Ingestion: identical to pysr_stacking.py (z = col0+i*col1 atomic complex,
X = z.reshape(-1,1), target = col2+i*col3).

Verdict: the judge verify_exact.py is the only authority. MSE >= 1e-3 invalidates
any claim regardless of marker. This harness writes one JSON per dataset and
prints the judge commands; it does NOT certify anything by itself.

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
        # NEW primitives for harness B (Kirsch):
        "inv(z) = 1 / (z + (1e-30 + 0im))",
        "inv_bar(z) = 1 / (conj(z) + (1e-30 + 0im))",
    ]
    extra_sympy_mappings = {
        "eml": lambda x, y: sp.exp(x) - sp.log(y),
        "emlstar": lambda x, y: sp.exp(x) - sp.log(sp.conjugate(y)),
        "my_conj": lambda z: sp.conjugate(z),
        "my_real": lambda z: sp.re(z),
        "my_imag": lambda z: sp.im(z),
        "my_abs2": lambda z: z * sp.conjugate(z),
        "inv": lambda z: 1 / z,
        "inv_bar": lambda z: 1 / sp.conjugate(z),
    }
    return binary_operators, unary_operators, extra_sympy_mappings


def run_one(csv_path, label, niter, pop, maxsize, parsimony, out_dir, verbose):
    print()
    print("=" * 74)
    print(f"PYSR (harness B) -- {label}  (csv={csv_path})")
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
    print(f"  toolbox: MIXTE + inv + inv_bar  (added 1/z and 1/conj(z) as primitives)")

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
        tempdir=os.path.join(out_dir, f"pysr_output_kirsch_stack_{label}"),
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
        "toolbox": "MIXTE + inv + inv_bar",
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

    bundle = {"script": "kirsch_stack.py", "results": {}}
    for label, csv in datasets:
        r = run_one(csv, label, args.niter, args.pop, args.maxsize, args.parsimony,
                    args.out_dir, verbose=not args.quiet)
        bundle["results"][label] = r
        with open(f"kirsch_stack_{label}_result.json", "w") as fh:
            json.dump(r, fh, indent=2)
        print(f"  [written] kirsch_stack_{label}_result.json")

    with open("kirsch_stack_summary.json", "w") as fh:
        json.dump(bundle, fh, indent=2)

    print()
    print("=" * 74)
    print("SUMMARY (harness B)")
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


if __name__ == "__main__":
    main()
