"""
discover_gp — Genetic Programming symbolic regression with eml/eml★.

Uses DEAP. Works on complex-valued data.
This is the real discovery engine, not the brute-force enumerator.

Usage:
    from discover_gp import run_gp

    import numpy as np
    z = np.linspace(-2+0.1j, 2+0.1j, 200)
    targets = np.conj(z)
    results = run_gp(z, targets, pop=300, gen=40, runs=5)
"""

import numpy as np
import warnings
from deap import base, creator, gp, tools, algorithms
import operator
import random
import time

from oxieml_star import eml, eml_star, conj_eml


# ============================================================
# Safe primitives (no crash on bad inputs)
# ============================================================

def safe_add(x, y):
    return np.asarray(x, dtype=complex) + np.asarray(y, dtype=complex)

def safe_mul(x, y):
    return np.asarray(x, dtype=complex) * np.asarray(y, dtype=complex)

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


# ============================================================
# GP Setup
# ============================================================

def _setup_pset():
    """Create DEAP primitive set with eml/eml★ operators."""
    pset = gp.PrimitiveSet("MAIN", 1)
    pset.renameArguments(ARG0="z")

    pset.addPrimitive(safe_eml, 2, name="eml")
    pset.addPrimitive(safe_eml_star, 2, name="eml_star")
    pset.addPrimitive(safe_conj_eml, 1, name="conj_eml")
    pset.addPrimitive(safe_add, 2, name="add")
    pset.addPrimitive(safe_mul, 2, name="mul")

    pset.addTerminal(1.0 + 0j, name="one")
    pset.addTerminal(0.0 + 0j, name="zero")

    return pset


def _eval_individual(individual, pset, z_data, targets):
    """Evaluate a GP individual. Returns (mse,) tuple for DEAP."""
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

        return (mse,)
    except (ValueError, FloatingPointError, OverflowError,
            ZeroDivisionError, TypeError, MemoryError):
        return (float('inf'),)


# ============================================================
# Main GP Runner
# ============================================================

def run_gp(z_data, targets, pop=300, gen=40, runs=10,
           max_depth=8, seed=None, verbose=True):
    """Run GP symbolic regression with eml★ primitives.

    Parameters
    ----------
    z_data : array, shape (n,), dtype complex
        Input complex data.
    targets : array, shape (n,), dtype complex
        Target values to discover formula for.
    pop : int
        Population size per run.
    gen : int
        Number of generations per run.
    runs : int
        Number of independent GP runs.
    max_depth : int
        Maximum tree depth.
    seed : int or None
        Random seed (None = random).
    verbose : bool
        Print progress.

    Returns
    -------
    list of dict with keys: formula, mse, size, has_eml_star, run
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
        best_mse = best.fitness.values[0]
        formula_str = str(best)
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
# Quick Test
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  discover_gp — GP Symbolic Regression with eml★")
    print("=" * 60)

    # Test: discover conj(z)
    grid = np.linspace(-2, 2, 15)
    re, im = np.meshgrid(grid, grid)
    z = (re + 1j * im).ravel()
    mask = np.abs(z.imag) < np.pi - 0.1
    z = z[mask]
    targets = np.conj(z)

    print(f"\nTarget: conj(z), {len(z)} points")
    print(f"Settings: pop=200, gen=30, runs=3, depth<=6\n")

    results = run_gp(z, targets, pop=200, gen=30, runs=3,
                     max_depth=6, seed=42)
