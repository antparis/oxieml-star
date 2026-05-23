#!/usr/bin/env python3
"""
pysr_stacking.py
PySR Brick Stacking — Iterative Discovery Engine

Each run discovers a formula. Good formulas become Julia operators
for the next run. Like hydrogen → helium → carbon.

Does NOT modify discover_pysr.py. Uses PySR directly.

Usage:
    python3 pysr_stacking.py                    # start fresh
    python3 pysr_stacking.py --resume           # resume from last save
    python3 pysr_stacking.py --report           # show discoveries
    python3 pysr_stacking.py --rounds 20        # run 20 stacking rounds

Author: Anthony Monnerot, 2026.
"""

import os
import re
import json
import time
import argparse
import numpy as np
import pandas as pd
import sympy
from datetime import datetime

try:
    from pysr import PySRRegressor
except ImportError:
    print("ERROR: PySR not installed. pip install pysr")
    exit(1)


# ============================================================
# CONFIGURATION
# ============================================================

BRICKS_FILE = "pysr_bricks.json"
REPORT_FILE = "pysr_stacking_report.txt"
DATA_DIR = "data"

# Only natively complex datasets — no galaxy artefacts
# Layered datasets: round N uses layer N
# Each layer is harder, but solvable if you found the brick at layer N-1
LAYER_DATASETS = {
    1: [
        "layer_mandelbrot_1.csv",   # z → z²+c
        "layer_tricorn_1.csv",      # z → conj(z)²+c
        "layer_damped_1.csv",       # ψ → ψ×U
    ],
    2: [
        "layer_mandelbrot_2.csv",   # z → (z²+c)²+c = brick(brick(z))
        "layer_tricorn_2.csv",      # z → conj(conj(z)²+c)²+c
        "layer_damped_2.csv",       # ψ → ψ×U²
    ],
    3: [
        "layer_mandelbrot_3.csv",   # z → ((z²+c)²+c)²+c = brick(brick(brick(z)))
        "layer_tricorn_3.csv",      # z → conj(conj(conj(z)²+c)²+c)²+c
        "layer_damped_3.csv",       # ψ → ψ×U⁴
    ],
}

# Fallback: original flat datasets if layers not found
DATASETS = [
    "fractal_mandelbrot.csv",
    "fractal_tricorn.csv",
    "wm_damped.csv",
]

# Fallback names (some scripts use evo_ prefix)
DATASET_ALIASES = {
    "fractal_mandelbrot.csv": "evo_mandelbrot.csv",
    "fractal_tricorn.csv": "evo_tricorn.csv",
    "wm_damped.csv": "evo_damped.csv",
}

# Promotion criteria
MSE_THRESHOLD = 1e-10       # must be below this to promote
IMPROVEMENT_MIN = 0.10      # must improve MSE by >10% vs last brick

# PySR base config (from reference — do not change without reason)
PYSR_BASE = dict(
    niterations=200,
    population_size=500,
    precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    verbosity=0,
    deterministic=False,
    parallelism="multithreading",
    maxsize=30,
    maxdepth=8,
)


# ============================================================
# BRICK MANAGEMENT
# ============================================================

def load_bricks():
    """Load previously discovered bricks."""
    if os.path.exists(BRICKS_FILE):
        with open(BRICKS_FILE, "r") as f:
            return json.load(f)
    return {"bricks": [], "history": []}


def save_bricks(state):
    """Save bricks to disk."""
    state["last_updated"] = datetime.now().isoformat()
    with open(BRICKS_FILE, "w") as f:
        json.dump(state, f, indent=2)


def equation_to_julia(eq_str, brick_name):
    """Convert a PySR equation string to a Julia function definition.

    Careful: must not corrupt identifiers like my_conj.
    Only replace 'j' when it's a complex literal suffix (preceded by digit).
    """
    # Replace x0 with z
    julia_body = eq_str.replace("x0", "z")

    # Replace complex literals: only j preceded by a digit → im
    # This avoids corrupting identifiers like my_conj, conj, etc.

    julia_body = re.sub(r'(\d+\.?\d*(?:[eE][+-]?\d+)?)[jJ]', r'\1im', julia_body)

    # Build Julia function definition
    julia_def = f"{brick_name}(z) = {julia_body}"
    return julia_def


def equation_to_sympy_lambda(eq_str, brick_name):
    """Create a sympy mapping for a discovered brick.
    This is approximate — used for display, not computation."""
    z = sympy.Symbol('z')
    # Return identity as fallback — PySR uses the Julia definition
    return lambda z: z


# ============================================================
# BUILD OPERATOR SET
# ============================================================

def build_operators(bricks):
    """Build the full operator set: base + discovered bricks."""

    # Base binary operators (always present)
    binary_operators = [
        "+", "-", "*", "/",
        "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))",
        "emlstar(x, y) = exp(x) - log(conj(y) + (1e-30 + 0im))",
    ]

    # Base unary operators (always present)
    unary_operators = [
        "cos", "sin", "exp", "log",
        "my_conj(z) = conj(z)",
        "my_real(z) = complex(real(z))",
        "my_imag(z) = complex(imag(z))",
        "my_abs2(z) = z * conj(z)",
    ]

    # Base sympy mappings
    extra_sympy = {
        "eml": lambda x, y: sympy.exp(x) - sympy.log(y),
        "emlstar": lambda x, y: sympy.exp(x) - sympy.log(sympy.conjugate(y)),
        "my_conj": lambda z: sympy.conjugate(z),
        "my_real": lambda z: sympy.re(z),
        "my_imag": lambda z: sympy.im(z),
        "my_abs2": lambda z: z * sympy.conjugate(z),
    }

    # Add discovered bricks as unary operators
    for brick in bricks:
        name = brick["name"]
        julia_def = brick["julia_def"]

        # Extract the function body from "brick_N(z) = ..."
        # and add as unary operator
        unary_operators.append(julia_def)

        # Add sympy mapping (approximate — for display)
        extra_sympy[name] = equation_to_sympy_lambda(
            brick["equation"], name
        )

    return binary_operators, unary_operators, extra_sympy


# ============================================================
# LOAD DATA
# ============================================================

def load_dataset(csv_path):
    """Load a single dataset."""
    df = pd.read_csv(csv_path)
    z = (df.iloc[:, 0].values + 1j * df.iloc[:, 1].values).astype(np.complex128)
    target = (df.iloc[:, 2].values + 1j * df.iloc[:, 3].values).astype(np.complex128)
    return z, target


# ============================================================
# SINGLE STACKING ROUND
# ============================================================

def run_round(dataset_name, z, target, bricks, seed=42):
    """Run one PySR round with current brick set."""

    binary_ops, unary_ops, sympy_maps = build_operators(bricks)

    X = z.reshape(-1, 1)
    y = target

    model = PySRRegressor(
        **PYSR_BASE,
        binary_operators=binary_ops,
        unary_operators=unary_ops,
        extra_sympy_mappings=sympy_maps,
        
    )

    model.fit(X, y)
    y_pred = model.predict(X)
    mse = float(np.mean(np.abs(y - y_pred) ** 2))

    best = model.get_best()
    equation = str(best["equation"])
    complexity = int(best["complexity"])

    # Check for eml★ markers
    markers = ["emlstar", "my_conj", "my_abs2", "my_imag"]
    # Also check for brick names that use eml★
    for brick in bricks:
        if brick.get("uses_emlstar"):
            markers.append(brick["name"])
    uses_star = any(m in equation for m in markers)

    return {
        "dataset": dataset_name,
        "equation": equation,
        "mse": mse,
        "complexity": complexity,
        "uses_emlstar": uses_star,
        "n_bricks": len(bricks),
        "n_operators": len(unary_ops) + len(binary_ops),
    }


# ============================================================
# MAIN STACKING LOOP
# ============================================================

def stack(rounds=10, resume=False):
    print("=" * 60)
    print("  PySR BRICK STACKING ENGINE")
    print("  Discoveries become operators for the next round")
    print("=" * 60)

    # Load state
    state = load_bricks() if resume else {"bricks": [], "history": []}
    bricks = state["bricks"]
    history = state["history"]

    start_round = len(history)
    if resume and bricks:
        print(f"\nResumed: {len(bricks)} bricks, {len(history)} rounds completed")
        for b in bricks:
            print(f"  {b['name']:15s} MSE={b['mse']:.4e}  {b['equation'][:50]}")
    else:
        print("\nStarting fresh — no bricks yet")

    # Load datasets — layer-aware
    print("\nDatasets by layer:")
    all_datasets = {}  # layer_num -> {name: (z, target)}

    # Try layered datasets first
    has_layers = False
    for layer_num, fnames in LAYER_DATASETS.items():
        layer_ds = {}
        for fname in fnames:
            path = os.path.join(DATA_DIR, fname)
            if os.path.exists(path):
                z, target = load_dataset(path)
                name = fname.replace(".csv", "")
                layer_ds[name] = (z, target)
                has_layers = True
        if layer_ds:
            all_datasets[layer_num] = layer_ds
            print(f"  Layer {layer_num}: {list(layer_ds.keys())}")

    # Fallback to flat datasets if no layers found
    if not has_layers:
        print("  No layered datasets found. Using flat datasets.")
        flat_ds = {}
        for fname in DATASETS:
            path = os.path.join(DATA_DIR, fname)
            if not os.path.exists(path) and fname in DATASET_ALIASES:
                path = os.path.join(DATA_DIR, DATASET_ALIASES[fname])
            if os.path.exists(path):
                z, target = load_dataset(path)
                name = fname.replace(".csv", "")
                flat_ds[name] = (z, target)
                print(f"  {fname:35s} ({len(z)} pts)")
        all_datasets[1] = flat_ds

    if not all_datasets:
        print("No datasets. Run generate_layers.py first.")
        return

    max_layer = max(all_datasets.keys())

    print(f"\nRunning {rounds} stacking rounds...")
    print()

    # Track best MSE per dataset for improvement check
    best_mse = {}
    for layer_ds in all_datasets.values():
        for name in layer_ds:
            relevant = [b["mse"] for b in bricks if b.get("source_dataset") == name]
            best_mse[name] = min(relevant) if relevant else float("inf")

    for rnd in range(start_round, start_round + rounds):
        round_start = time.time()

        # Select layer for this round
        layer = min(rnd + 1, max_layer)
        datasets = all_datasets.get(layer, all_datasets[max_layer])

        print(f"--- Round {rnd + 1} | Layer {layer} | {len(bricks)} bricks | "
              f"{len(bricks) + 12} operators ---")

        round_results = []

        for ds_name, (z, target) in datasets.items():
            seed = 42 + rnd * 100 + hash(ds_name) % 100

            result = run_round(ds_name, z, target, bricks, seed=seed)
            round_results.append(result)

            star = "YES" if result["uses_emlstar"] else "no"
            print(f"  {ds_name:30s} MSE={result['mse']:.4e} eml★={star} "
                  f"cx={result['complexity']} | {result['equation'][:45]}")

            # Check promotion criteria
            mse = result["mse"]
            prev_best = best_mse.get(ds_name, float("inf"))
            improvement = (prev_best - mse) / (prev_best + 1e-30) if prev_best < float("inf") else 1.0

            if mse < MSE_THRESHOLD and improvement > IMPROVEMENT_MIN:
                # Promote!
                brick_name = f"brick_{len(bricks) + 1}"
                julia_def = equation_to_julia(result["equation"], brick_name)

                # Guard: verify the Julia definition is safe to inject
                # Check for obvious conversion failures
                julia_ok = True
                warn_msg = ""

                # Check: "j" not inside identifiers (would corrupt them)
                if re.search(r'[a-zA-Z_]j[a-zA-Z_]', julia_def):
                    julia_ok = False
                    warn_msg = "Julia conversion corrupted an identifier"

                # Check: balanced parentheses
                if julia_def.count('(') != julia_def.count(')'):
                    julia_ok = False
                    warn_msg = "Unbalanced parentheses in Julia definition"

                # Check: function body is not empty
                if '=' not in julia_def or julia_def.split('=', 1)[1].strip() == '':
                    julia_ok = False
                    warn_msg = "Empty Julia function body"

                if not julia_ok:
                    print(f"    Promotion SKIPPED: {warn_msg}")
                    print(f"    Raw equation: {result['equation'][:60]}")
                    print(f"    Julia attempt: {julia_def[:60]}")
                    continue

                new_brick = {
                    "name": brick_name,
                    "round": rnd + 1,
                    "source_dataset": ds_name,
                    "equation": result["equation"],
                    "julia_def": julia_def,
                    "mse": mse,
                    "complexity": result["complexity"],
                    "uses_emlstar": result["uses_emlstar"],
                    "improvement": improvement,
                    "timestamp": datetime.now().isoformat(),
                }
                bricks.append(new_brick)
                best_mse[ds_name] = mse

                print(f"    *** PROMOTED as {brick_name} (improvement: {improvement:.1%}) ***")
                print(f"    Julia: {julia_def[:70]}")
                save_bricks({"bricks": bricks, "history": history})
            elif mse < prev_best:
                best_mse[ds_name] = mse

        # Save history
        history.append({
            "round": rnd + 1,
            "n_bricks": len(bricks),
            "results": round_results,
            "elapsed": time.time() - round_start,
            "timestamp": datetime.now().isoformat(),
        })

        # Save state after each round
        state = {"bricks": bricks, "history": history}
        save_bricks(state)

        elapsed = time.time() - round_start
        print(f"  Round time: {elapsed:.0f}s | Total bricks: {len(bricks)}")
        print()

    # Final report
    generate_report(state)


# ============================================================
# REPORT
# ============================================================

def generate_report(state=None):
    if state is None:
        state = load_bricks()

    bricks = state["bricks"]
    history = state["history"]

    lines = []
    lines.append("=" * 70)
    lines.append("  PySR BRICK STACKING REPORT")
    lines.append(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  Rounds: {len(history)} | Bricks: {len(bricks)}")
    lines.append("=" * 70)

    if bricks:
        lines.append("\n  DISCOVERED BRICKS:")
        lines.append(f"  {'Name':>10s} {'Round':>5s} {'Dataset':>25s} {'MSE':>12s} "
                     f"{'eml★':>5s} {'Improv':>8s}")
        lines.append(f"  {'-' * 70}")
        for b in bricks:
            star = "YES" if b["uses_emlstar"] else "no"
            lines.append(f"  {b['name']:>10s} {b['round']:>5d} {b['source_dataset']:>25s} "
                         f"{b['mse']:>12.4e} {star:>5s} {b['improvement']:>7.1%}")
            lines.append(f"    EQ: {b['equation'][:60]}")
            lines.append(f"    JL: {b['julia_def'][:60]}")

    if history:
        lines.append(f"\n  ROUND HISTORY (last 5):")
        for h in history[-5:]:
            lines.append(f"    Round {h['round']:3d}: {h['n_bricks']} bricks, "
                         f"{h['elapsed']:.0f}s")

    # Summary stats
    if bricks:
        star_bricks = [b for b in bricks if b["uses_emlstar"]]
        lines.append(f"\n  SUMMARY:")
        lines.append(f"    Total bricks:     {len(bricks)}")
        lines.append(f"    eml★ bricks:      {len(star_bricks)}")
        lines.append(f"    Best MSE overall: {min(b['mse'] for b in bricks):.4e}")

    lines.append("\n" + "=" * 70)

    report = "\n".join(lines)

    with open(REPORT_FILE, "w") as f:
        f.write(report)

    print(report)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PySR Brick Stacking")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--rounds", type=int, default=10)
    args = parser.parse_args()

    if args.report:
        generate_report()
    else:
        stack(rounds=args.rounds, resume=args.resume)
