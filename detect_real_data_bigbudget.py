#!/usr/bin/env python3
"""
detect_real_data.py
Anti-holomorphic vs holomorphic detector for a single REAL natively-complex
dataset (CSV with columns z_real,z_imag,target_real,target_imag).

Same engine as double_validation_v6.py:
  - operators: eml, emlstar, my_real, my_conj (+ standard holomorphic ops)
  - two independent routes to anti-holomorphy:
      Route A (eml*) : toolbox containing emlstar
      Route B (Re)   : toolbox containing my_real
  - verdict per route: marker present in best equation => anti, else holo
  - verbosity=1 + progress=True (live PySR generations)
  - JSON checkpoint with --resume / --force

This is the EXTERNAL-DATA version: it reads ONE arbitrary CSV instead of the
synthetic battery, and writes a self-contained result JSON. The exact
anti/holo nature must still be certified afterwards by the SymPy judge
(verify_exact.py) on the produced equations -- numbers from PySR are
provisional until the judge speaks.

Usage:
  python3 -u detect_real_data.py data/eht_m87_visibility.csv --niter 60
  python3 -u detect_real_data.py data/eht_m87_visibility.csv --resume

Author: Anthony Monnerot, 2026.
"""
import os
import sys
import json
import argparse
import numpy as np
import pandas as pd
import sympy

# -------------------------------------------------------------------------
# Custom operators — Julia string definitions injected directly into PySR
# (FIX Bug 1: replaced JULIA_OPERATORS dict with explicit string constants)
# -------------------------------------------------------------------------
EML_DEF     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR_DEF = "emlstar(x, y) = exp(x) - log(conj(y) + (1e-30 + 0im))"  # FIX: exp(x) not exp(conj(x))
MYREAL_DEF  = "my_real(z) = complex(real(z))"
MYCONJ_DEF  = "my_conj(z) = conj(z)"

# Toolboxes: each route gets exactly ONE anti-holomorphic gate, plus the
# shared holomorphic operators.
TOOLBOXES = {
    "A_emlstar": {
        "binary_operators": ["+", "-", "*", "/", EML_DEF, EMLSTAR_DEF],
        "unary_operators":  ["exp", "log", "sin", "cos", MYCONJ_DEF],
        "marker": "emlstar",
    },
    "B_re": {
        "binary_operators": ["+", "-", "*", "/", EML_DEF],
        "unary_operators":  ["exp", "log", "sin", "cos", MYREAL_DEF],
        "marker": "my_real",
    },
}

# SymPy mappings for post-hoc symbolic verification
EXTRA_SYMPY_MAPPINGS = {
    "eml":     lambda x, y: sympy.exp(x) - sympy.log(y),
    "emlstar": lambda x, y: sympy.exp(x) - sympy.log(sympy.conjugate(y)),
    "my_real": lambda z: sympy.re(z),
    "my_conj": lambda z: sympy.conjugate(z),
}


def log(msg):
    print(msg, flush=True)


def load_dataset(path):
    df = pd.read_csv(path)
    z = df["z_real"].to_numpy() + 1j * df["z_imag"].to_numpy()
    t = df["target_real"].to_numpy() + 1j * df["target_imag"].to_numpy()
    return z, t


def build_regressor(toolbox, niter):
    from pysr import PySRRegressor
    # Build sympy mappings for operators present in this toolbox
    all_ops = " ".join(toolbox["binary_operators"] + toolbox["unary_operators"])
    mappings = {name: fn for name, fn in EXTRA_SYMPY_MAPPINGS.items()
                if name in all_ops}
    model = PySRRegressor(
        niterations=niter,
        binary_operators=toolbox["binary_operators"],
        unary_operators=toolbox["unary_operators"],
        extra_sympy_mappings=mappings,          # FIX Bug 2: was empty {}
        elementwise_loss="loss(x, y) = abs2(x - y)",
        verbosity=1,
        progress=True,
        deterministic=True,
        parallelism="serial",
        random_state=0,
        population_size=150,
        precision=64,
        maxsize=40,
        maxdepth=8,
    )
    return model


def run_route(z, t, toolbox_name, niter):
    toolbox = TOOLBOXES[toolbox_name]
    log(f"   building regressor for {toolbox_name} ...")
    model = build_regressor(toolbox, niter)
    X = z.reshape(-1, 1).astype(np.complex128)   # FIX Bug 3: was column_stack -> shape (N,)
    model.fit(X, t)
    eq = str(model.get_best()["equation"])
    mse = float(model.get_best()["loss"])
    marker = toolbox["marker"]
    verdict = "anti" if marker in eq else "holo"
    log(f"   eq      = {eq[:90]}")
    log(f"   MSE     = {mse:.3e}   verdict={verdict} "
        f"(marker '{marker}' {'present' if verdict=='anti' else 'absent'})")
    return {"best_equation": eq, "mse": mse, "verdict": verdict,
            "marker": marker}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="dataset CSV (z_real,z_imag,target_real,target_imag)")
    ap.add_argument("--niter", type=int, default=60)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    base = os.path.splitext(os.path.basename(args.csv))[0]
    out_json = f"detect_{base}_result.json"

    # checkpoint
    # JSON layout matches double_validation_v6 so that verify_exact.py reads it:
    #   results["runs"][dataset_name][route]["best_equation"]
    # Here the single dataset is keyed by `base`.
    results = {"dataset": args.csv, "niter": args.niter, "runs": {base: {}}}
    if os.path.exists(out_json) and args.resume and not args.force:
        with open(out_json) as fh:
            results = json.load(fh)
        results.setdefault("runs", {}).setdefault(base, {})
        log(f"[resume] loaded {len(results['runs'][base])} existing route(s)")

    z, t = load_dataset(args.csv)
    log(f"Loaded {len(z)} points from {args.csv}")
    log(f"  |z| max = {np.abs(z).max():.3f}   |t| max = {np.abs(t).max():.3f}")
    log("=" * 72)

    routes = list(TOOLBOXES.keys())
    for i, route in enumerate(routes, 1):
        if route in results["runs"][base] and not args.force:
            log(f"[{i}/{len(routes)}] {route}  (already done, skipped)")
            continue
        log(f"[{i}/{len(routes)}] {route}  (running PySR...)")
        results["runs"][base][route] = run_route(z, t, route, args.niter)
        with open(out_json, "w") as fh:
            json.dump(results, fh, indent=2)
        log(f"   [saved to {out_json}]")

    # summary
    log("=" * 72)
    log("SUMMARY")
    log("=" * 72)
    log(f"{'Route':14s} {'Verdict':10s} {'MSE':12s}")
    for route in routes:
        r = results["runs"][base].get(route, {})
        log(f"{route:14s} {r.get('verdict','?'):10s} {r.get('mse',float('nan')):.3e}")
    agree = len({results['runs'][base][r]['verdict']
                 for r in results['runs'][base]}) == 1
    log(f"Routes agree: {agree}")
    log(f"Results written to {out_json}")
    log("NOTE: PySR verdicts are numerical/provisional. Certify with the SymPy")
    log("judge:  python3 verify_exact.py " + out_json)


if __name__ == "__main__":
    main()
