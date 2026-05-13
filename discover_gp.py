"""
discover_gp — Genetic Programming symbolic regression with eml/eml★.

Uses DEAP. Works on complex-valued data.
Supports CSV input, ADF rounds, parsimony, and simplification.

Usage:
    # Demo mode (conj(z) test)
    python3 discover_gp.py

    # CSV mode
    python3 discover_gp.py --csv data.csv --pop 300 --gen 40 --runs 10

    # ADF mode (multiple rounds, increasing depth)
    python3 discover_gp.py --adf data.csv --rounds 3

CSV format: z_real,z_imag,target_real,target_imag
"""

import numpy as np
import warnings
import random
import time
import re
import operator
import sys
import csv
from functools import partial

from deap import base, creator, gp, tools, algorithms

from oxieml_star import eml, eml_star, conj_eml


# ============================================================
# Safe Primitives
# ============================================================

def safe_add(x, y):
    return np.asarray(x, dtype=complex) + np.asarray(y, dtype=complex)

def safe_sub(x, y):
    return np.asarray(x, dtype=complex) - np.asarray(y, dtype=complex)

def safe_mul(x, y):
    return np.asarray(x, dtype=complex) * np.asarray(y, dtype=complex)

def safe_div(x, y):
    x = np.asarray(x, dtype=complex)
    y = np.asarray(y, dtype=complex)
    y_safe = np.where(np.abs(y) < 1e-30, 1e-30 + 0j, y)
    return x / y_safe

def safe_ln(z):
    try:
        z = np.asarray(z, dtype=complex)
        z_safe = np.where(np.abs(z) < 1e-30, 1e-30 + 0j, z)
        return np.log(z_safe)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)

def safe_log10(z):
    try:
        z = np.asarray(z, dtype=complex)
        z_safe = np.where(np.abs(z) < 1e-30, 1e-30 + 0j, z)
        return np.log10(z_safe)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)

def safe_eml(x, y):
    try:
        return eml(x, y)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(x, dtype=complex), np.nan)

def safe_eml_star(x, y):
    try:
        return eml_star(x, y)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(x, dtype=complex), np.nan)

def safe_conj_eml(z):
    try:
        return conj_eml(z)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)


def _rand_const():
    """Ephemeral random constant for GP."""
    return complex(round(random.uniform(-10, 10), 2), 0)


# ============================================================
# GP Setup
# ============================================================

def _setup_pset():
    """Create DEAP primitive set with eml/eml★ operators."""
    pset = gp.PrimitiveSet("MAIN", 1)
    pset.renameArguments(ARG0="z")

    # Binary operators
    pset.addPrimitive(safe_eml, 2, name="eml")
    pset.addPrimitive(safe_eml_star, 2, name="eml_star")
    pset.addPrimitive(safe_add, 2, name="add")
    pset.addPrimitive(safe_sub, 2, name="sub")
    pset.addPrimitive(safe_mul, 2, name="mul")
    pset.addPrimitive(safe_div, 2, name="div")

    # Unary operators
    pset.addPrimitive(safe_conj_eml, 1, name="conj_eml")
    pset.addPrimitive(safe_ln, 1, name="ln")
    pset.addPrimitive(safe_log10, 1, name="log10")

    # Constants
    pset.addTerminal(0.0 + 0j, name="zero")
    pset.addTerminal(1.0 + 0j, name="one")
    pset.addTerminal(0.5 + 0j, name="half")
    pset.addTerminal(5.0 + 0j, name="five")
    pset.addTerminal(25.0 + 0j, name="twentyfive")
    pset.addTerminal(2.302585 + 0j, name="ln10")

    # Ephemeral random constant
    pset.addEphemeralConstant("rc", partial(_rand_const))

    return pset


# ============================================================
# Evaluation
# ============================================================

PARSIMONY_WEIGHT = 0.0002

def _eval_individual(individual, pset, z_data, targets):
    """Evaluate a GP individual. Returns (mse + parsimony,) tuple."""
    try:
        func = gp.compile(expr=individual, pset=pset)
        pred = func(z_data)
        pred = np.asarray(pred, dtype=complex)

        if pred.shape != targets.shape:
            return (float('inf'),)

        err = pred - targets
        mse = float(np.mean(np.abs(err) ** 2))

        if not np.isfinite(mse):
            return (float('inf'),)

        # Parsimony pressure: penalize large trees
        return (mse + PARSIMONY_WEIGHT * len(individual),)
    except (ValueError, FloatingPointError, OverflowError,
            ZeroDivisionError, TypeError, MemoryError):
        return (float('inf'),)


# ============================================================
# Formula Simplifier
# ============================================================

def simplify_formula(formula_str):
    """Remove trivial patterns from GP formula strings."""
    s = formula_str
    for _ in range(10):
        prev = s
        s = re.sub(r'add\(([^,()]+), zero\)', r'\1', s)
        s = re.sub(r'add\(zero, ([^,()]+)\)', r'\1', s)
        s = re.sub(r'mul\(([^,()]+), one\)', r'\1', s)
        s = re.sub(r'mul\(one, ([^,()]+)\)', r'\1', s)
        s = re.sub(r'mul\([^,()]+, zero\)', 'zero', s)
        s = re.sub(r'mul\(zero, [^,()]+\)', 'zero', s)
        s = re.sub(r'sub\(([^,()]+), zero\)', r'\1', s)
        s = re.sub(r'div\(([^,()]+), one\)', r'\1', s)
        if s == prev:
            break
    return s


# ============================================================
# CSV Loader
# ============================================================

def load_csv(path):
    """Load complex data from CSV.

    Expected columns: z_real, z_imag, target_real, target_imag
    Or: z_real, z_imag, target_real (target_imag assumed 0)
    """
    z_list = []
    t_list = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        for row in reader:
            if len(row) >= 4:
                z_list.append(float(row[0]) + 1j * float(row[1]))
                t_list.append(float(row[2]) + 1j * float(row[3]))
            elif len(row) >= 3:
                z_list.append(float(row[0]) + 1j * float(row[1]))
                t_list.append(float(row[2]) + 0j)
    return np.array(z_list), np.array(t_list)


# ============================================================
# Main GP Runner
# ============================================================

def run_gp(z_data, targets, pop=300, gen=40, runs=10,
           max_depth=8, seed=None, verbose=True):
    """Run GP symbolic regression with eml★ primitives.

    Parameters
    ----------
    z_data : array, shape (n,), dtype complex
    targets : array, shape (n,), dtype complex
    pop : int — population size per run
    gen : int — generations per run
    runs : int — independent GP runs
    max_depth : int — maximum tree depth
    seed : int or None
    verbose : bool

    Returns
    -------
    list of dict: formula, mse, size, has_eml_star, run
    """
    z_data = np.asarray(z_data, dtype=complex)
    targets = np.asarray(targets, dtype=complex)
    pset = _setup_pset()

    # DEAP creator (avoid duplicate creation)
    if not hasattr(creator, "FitnessMin_gp"):
        creator.create("FitnessMin_gp", base.Fitness, weights=(-1.0,))
    if not hasattr(creator, "Individual_gp"):
        creator.create("Individual_gp", gp.PrimitiveTree,
                       fitness=creator.FitnessMin_gp)

    all_results = []

    for run_idx in range(runs):
        run_seed = seed + run_idx if seed is not None else None
        if run_seed is not None:
            random.seed(run_seed)
            np.random.seed(run_seed)

        toolbox = base.Toolbox()
        toolbox.register("expr", gp.genHalfAndHalf, pset=pset,
                         min_=1, max_=4)
        toolbox.register("individual", tools.initIterate,
                         creator.Individual_gp, toolbox.expr)
        toolbox.register("population", tools.initRepeat,
                         list, toolbox.individual)
        toolbox.register("compile", gp.compile, pset=pset)
        toolbox.register("evaluate", _eval_individual,
                         pset=pset, z_data=z_data, targets=targets)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("mate", gp.cxOnePoint)
        toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut,
                         pset=pset)

        toolbox.decorate("mate",
                         gp.staticLimit(key=operator.attrgetter("height"),
                                        max_value=max_depth))
        toolbox.decorate("mutate",
                         gp.staticLimit(key=operator.attrgetter("height"),
                                        max_value=max_depth))

        population = toolbox.population(n=pop)
        hof = tools.HallOfFame(5)

        if verbose:
            print(f"Run {run_idx + 1}/{runs}...", end=" ", flush=True)

        start = time.time()
        algorithms.eaSimple(population, toolbox,
                            cxpb=0.7, mutpb=0.2, ngen=gen,
                            halloffame=hof, verbose=False)
        elapsed = time.time() - start

        best = hof[0]
        # Report raw MSE without parsimony penalty
        best_mse = best.fitness.values[0] - PARSIMONY_WEIGHT * len(best)
        if best_mse < 0:
            best_mse = 0.0
        formula_str = simplify_formula(str(best))
        has_star = "eml_star" in formula_str or "conj_eml" in formula_str

        if verbose:
            status = "EXACT" if best_mse < 1e-20 else f"MSE={best_mse:.2e}"
            star_flag = " [eml★]" if has_star else ""
            print(f"{status}{star_flag} ({elapsed:.1f}s)")

        all_results.append({
            'formula': formula_str,
            'mse': best_mse,
            'size': len(best),
            'has_eml_star': has_star,
            'run': run_idx + 1,
        })

    all_results.sort(key=lambda r: r['mse'])

    if verbose:
        print(f"\nBest overall: MSE={all_results[0]['mse']:.2e}")
        print(f"Formula: {all_results[0]['formula']}")
        exact = sum(1 for r in all_results if r['mse'] < 1e-20)
        with_star = sum(1 for r in all_results if r['has_eml_star'])
        print(f"Exact: {exact}/{runs}, with eml★: {with_star}/{runs}")

    return all_results


# ============================================================
# ADF: Automatically Defined Functions
# ============================================================

def find_common_subtrees(results, min_count=2):
    """Find sub-expressions that appear in multiple good formulas."""
    subtrees = {}
    for r in results:
        f = r['formula']
        # Extract function calls with simple (non-nested) arguments
        for match in re.finditer(
            r'(eml|eml_star|conj_eml|add|sub|mul|ln|log10|div)\([^()]*\)', f
        ):
            sub = match.group()
            if len(sub) > 5 and sub != f:
                subtrees[sub] = subtrees.get(sub, 0) + 1

    common = [(expr, count) for expr, count in
              sorted(subtrees.items(), key=lambda x: -x[1])
              if count >= min_count]
    return common[:10]


def run_gp_with_adf(z_data, targets, pop=500, gen=100, runs=5, rounds=3,
                     max_depth=8, seed=42, verbose=True):
    """Run GP with Automatically Defined Functions.

    Round 1: normal GP
    Round 2+: extract common subtrees, report patterns, increase gens
    """
    z_data = np.asarray(z_data, dtype=complex)
    targets = np.asarray(targets, dtype=complex)

    all_results = []

    for round_idx in range(rounds):
        round_gen = gen * (round_idx + 1)  # more gens each round

        if verbose:
            print(f"\n{'='*60}")
            print(f"  Round {round_idx + 1}/{rounds} | pop={pop} gen={round_gen}")
            print(f"{'='*60}")

        results = run_gp(z_data, targets, pop=pop, gen=round_gen, runs=runs,
                        max_depth=max_depth,
                        seed=seed + round_idx * 100 if seed else None,
                        verbose=verbose)
        all_results.extend(results)

        # Find common subtrees from results
        good = [r for r in results if r['mse'] < float('inf')]
        common = find_common_subtrees(good, min_count=2)

        if verbose and common:
            print(f"\nCommon subtrees found:")
            for expr, count in common[:5]:
                print(f"  [{count}x] {expr}")
        elif verbose:
            print("\nNo common subtrees found.")

    # Sort all results
    all_results.sort(key=lambda r: r['mse'])

    if verbose:
        print(f"\n{'='*60}")
        print(f"  FINAL RESULTS ({rounds} rounds, {len(all_results)} total)")
        print(f"{'='*60}")
        print(f"Best MSE: {all_results[0]['mse']:.4e}")
        print(f"Formula: {all_results[0]['formula']}")
        exact = sum(1 for r in all_results if r['mse'] < 1e-20)
        with_star = sum(1 for r in all_results if r['has_eml_star'])
        print(f"Exact: {exact}/{len(all_results)}")
        print(f"With eml★: {with_star}/{len(all_results)}")

    return all_results


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    # Parse mode
    if len(sys.argv) > 1 and sys.argv[1] == "--adf":
        # ADF mode
        if len(sys.argv) < 3:
            print("Usage: python3 discover_gp.py --adf data.csv [--rounds 3]")
            sys.exit(1)

        csv_path = sys.argv[2]
        rounds = 3
        i = 3
        while i < len(sys.argv) - 1:
            if sys.argv[i] == "--rounds":
                rounds = int(sys.argv[i + 1])
            i += 2

        print(f"Loading {csv_path}...")
        z_data, targets = load_csv(csv_path)
        print(f"Loaded {len(z_data)} points")
        print(f"ADF mode: {rounds} rounds\n")

        results = run_gp_with_adf(z_data, targets, pop=1000, gen=100,
                                   runs=5, rounds=rounds, seed=42)

        out_path = csv_path.replace(".csv", "_adf_results.txt")
        with open(out_path, "w") as f:
            for r in results:
                f.write(f"MSE={r['mse']:.4e}  eml_star={r['has_eml_star']}  "
                        f"{r['formula']}\n")
        print(f"\nResults saved to {out_path}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--csv":
        # CSV mode
        if len(sys.argv) < 3:
            print("Usage: python3 discover_gp.py --csv data.csv "
                  "[--pop 300] [--gen 40] [--runs 10]")
            sys.exit(1)

        csv_path = sys.argv[2]
        pop = 300
        gen = 40
        runs = 10

        i = 3
        while i < len(sys.argv) - 1:
            if sys.argv[i] == "--pop":
                pop = int(sys.argv[i + 1])
            elif sys.argv[i] == "--gen":
                gen = int(sys.argv[i + 1])
            elif sys.argv[i] == "--runs":
                runs = int(sys.argv[i + 1])
            i += 2

        print(f"Loading {csv_path}...")
        z_data, targets = load_csv(csv_path)
        print(f"Loaded {len(z_data)} points")
        print(f"Settings: pop={pop}, gen={gen}, runs={runs}\n")

        results = run_gp(z_data, targets, pop=pop, gen=gen, runs=runs)

        out_path = csv_path.replace(".csv", "_results.txt")
        with open(out_path, "w") as f:
            for r in results:
                f.write(f"MSE={r['mse']:.4e}  eml_star={r['has_eml_star']}  "
                        f"{r['formula']}\n")
        print(f"\nResults saved to {out_path}")

    else:
        # Demo mode
        print("=" * 60)
        print("  discover_gp — GP Symbolic Regression with eml★")
        print("=" * 60)

        grid = np.linspace(-2, 2, 15)
        re_g, im_g = np.meshgrid(grid, grid)
        z = (re_g + 1j * im_g).ravel()
        mask = np.abs(z.imag) < np.pi - 0.1
        z = z[mask]
        targets = np.conj(z)

        print(f"\nTarget: conj(z), {len(z)} points")
        print(f"Settings: pop=200, gen=30, runs=3, depth<=6\n")

        results = run_gp(z, targets, pop=200, gen=30, runs=3,
                         max_depth=6, seed=42)
