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
from scipy.optimize import minimize as scipy_minimize


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

def safe_sin(z):
    try:
        z = np.asarray(z, dtype=complex)
        z_clamped = np.clip(z.real, -50, 50) + 1j * np.clip(z.imag, -50, 50)
        result = np.sin(z_clamped)
        return np.where(np.isfinite(result), result, np.nan + 0j)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)

def safe_cos(z):
    try:
        z = np.asarray(z, dtype=complex)
        z_clamped = np.clip(z.real, -50, 50) + 1j * np.clip(z.imag, -50, 50)
        result = np.cos(z_clamped)
        return np.where(np.isfinite(result), result, np.nan + 0j)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)

def safe_exp(z):
    try:
        z = np.asarray(z, dtype=complex)
        z_clamped = np.clip(z.real, -709, 709) + 1j * z.imag
        result = np.exp(z_clamped)
        return np.where(np.isfinite(result), result, np.nan + 0j)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)

def safe_pow(x, y):
    try:
        x = np.asarray(x, dtype=complex)
        y = np.asarray(y, dtype=complex)
        x_safe = np.where(np.abs(x) < 1e-30, 1e-30 + 0j, x)
        result = x_safe ** y
        return np.where(np.isfinite(result), result, np.nan + 0j)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(x, dtype=complex), np.nan)

def safe_arcsin(z):
    try:
        z = np.asarray(z, dtype=complex)
        result = np.arcsin(z)
        return np.where(np.isfinite(result), result, np.nan + 0j)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)

def safe_arccos(z):
    try:
        z = np.asarray(z, dtype=complex)
        result = np.arccos(z)
        return np.where(np.isfinite(result), result, np.nan + 0j)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)

def safe_arctan(z):
    try:
        z = np.asarray(z, dtype=complex)
        result = np.arctan(z)
        return np.where(np.isfinite(result), result, np.nan + 0j)
    except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
        return np.full_like(np.asarray(z, dtype=complex), np.nan)


def _rand_const():
    """Ephemeral random constant for GP."""
    return complex(round(random.uniform(-10, 10), 2), 0)


# ============================================================
# GP Setup
# ============================================================

def _setup_pset(num_vars=1):
    """Create DEAP primitive set with eml/eml★ operators."""
    pset = gp.PrimitiveSet("MAIN", num_vars)
    if num_vars == 1:
        pset.renameArguments(ARG0="z")
    elif num_vars == 2:
        pset.renameArguments(ARG0="z0", ARG1="z1")
    elif num_vars == 3:
        pset.renameArguments(ARG0="z0", ARG1="z1", ARG2="z2")

    # Binary operators
    pset.addPrimitive(safe_eml, 2, name="eml")
    pset.addPrimitive(safe_eml_star, 2, name="eml_star")
    pset.addPrimitive(safe_add, 2, name="add")
    pset.addPrimitive(safe_sub, 2, name="sub")
    pset.addPrimitive(safe_mul, 2, name="mul")
    pset.addPrimitive(safe_div, 2, name="div")
    pset.addPrimitive(safe_pow, 2, name="pow")

    # Unary operators
    pset.addPrimitive(safe_conj_eml, 1, name="conj_eml")
    pset.addPrimitive(safe_ln, 1, name="ln")
    pset.addPrimitive(safe_log10, 1, name="log10")
    pset.addPrimitive(safe_sin, 1, name="sin")
    pset.addPrimitive(safe_cos, 1, name="cos")
    pset.addPrimitive(safe_exp, 1, name="exp")
    pset.addPrimitive(safe_arcsin, 1, name="arcsin")
    pset.addPrimitive(safe_arccos, 1, name="arccos")
    pset.addPrimitive(safe_arctan, 1, name="arctan")

    # Constants
    pset.addTerminal(0.0 + 0j, name="zero")
    pset.addTerminal(1.0 + 0j, name="one")
    pset.addTerminal(0.0 + 1.0j, name="imag_i")
    pset.addTerminal(0.5 + 0j, name="half")
    pset.addTerminal(2.0 + 0j, name="two")
    pset.addTerminal(5.0 + 0j, name="five")
    pset.addTerminal(25.0 + 0j, name="twentyfive")
    pset.addTerminal(2.302585 + 0j, name="ln10")
    pset.addTerminal(3.141593 + 0j, name="pi")

    # Ephemeral random constant
    pset.addEphemeralConstant("rc", partial(_rand_const))

    return pset


# ============================================================
# Evaluation
# ============================================================

PARSIMONY_WEIGHT = 0.0002

def _eval_individual(individual, pset, var_data, targets):
    """Evaluate a GP individual. Returns (mse + parsimony,) tuple.
    
    var_data: list of arrays, one per variable. e.g. [z] or [z0, z1]
    """
    try:
        func = gp.compile(expr=individual, pset=pset)
        pred = func(*var_data)
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
    """Remove trivial patterns and fold constants in GP formula strings."""
    s = formula_str
    for _ in range(20):
        prev = s
        # Identity elimination
        s = re.sub(r'add\(([^,()]+), zero\)', r'\1', s)
        s = re.sub(r'add\(zero, ([^,()]+)\)', r'\1', s)
        s = re.sub(r'mul\(([^,()]+), one\)', r'\1', s)
        s = re.sub(r'mul\(one, ([^,()]+)\)', r'\1', s)
        s = re.sub(r'mul\([^,()]+, zero\)', 'zero', s)
        s = re.sub(r'mul\(zero, [^,()]+\)', 'zero', s)
        s = re.sub(r'sub\(([^,()]+), zero\)', r'\1', s)
        s = re.sub(r'div\(([^,()]+), one\)', r'\1', s)
        s = re.sub(r'pow\(([^,()]+), one\)', r'\1', s)
        s = re.sub(r'pow\(([^,()]+), zero\)', 'one', s)
        s = re.sub(r'exp\(zero\)', 'one', s)
        s = re.sub(r'ln\(one\)', 'zero', s)
        s = re.sub(r'sin\(zero\)', 'zero', s)
        s = re.sub(r'cos\(zero\)', 'one', s)
        s = re.sub(r'add\(([^,()]+), \\1\)', r'mul(two, \1)', s)
        s = re.sub(r'sub\(([^,()]+), \\1\)', 'zero', s)
        s = re.sub(r'div\(([^,()]+), \\1\)', 'one', s)
        # conj_eml on real constants
        s = re.sub(r'conj_eml\(zero\)', 'zero', s)
        s = re.sub(r'conj_eml\(one\)', 'one', s)
        s = re.sub(r'conj_eml\(half\)', 'half', s)
        s = re.sub(r'conj_eml\(five\)', 'five', s)
        s = re.sub(r'conj_eml\(pi\)', 'pi', s)
        if s == prev:
            break
    return s


# ============================================================
# Constant Optimization (Nelder-Mead)
# ============================================================

def optimize_constants(formula_str, pset, var_data, targets, num_vars):
    """Extract numeric constants from GP formula and optimize via Nelder-Mead.
    
    Returns (optimized_formula_str, optimized_mse) or (formula_str, None) on failure.
    """
    # Find all numeric constants like (1.23+0j)
    pattern = r'\((-?[0-9]+\.?[0-9]*)\+0j\)'
    matches = list(re.finditer(pattern, formula_str))
    if not matches:
        return formula_str, None

    original_vals = [float(m.group(1)) for m in matches]

    def eval_with_constants(const_vals):
        s = formula_str
        for m, val in zip(reversed(matches), reversed(const_vals)):
            s = s[:m.start()] + f"({val}+0j)" + s[m.end():]
        try:
            tree = gp.PrimitiveTree.from_string(s, pset)
            func = gp.compile(expr=tree, pset=pset)
            pred = func(*var_data)
            pred = np.asarray(pred, dtype=complex)
            if pred.shape != targets.shape:
                return 1e10
            err = pred - targets
            mse = float(np.mean(np.abs(err) ** 2))
            return mse if np.isfinite(mse) else 1e10
        except (ValueError, FloatingPointError, OverflowError,
                ZeroDivisionError, TypeError, MemoryError, Exception):
            return 1e10

    try:
        result = scipy_minimize(eval_with_constants, original_vals,
                                method="Nelder-Mead",
                                options={"maxiter": 500, "xatol": 1e-6})
        if result.fun < eval_with_constants(original_vals):
            s = formula_str
            opt_vals = list(result.x)
            for m, val in zip(reversed(matches), reversed(opt_vals)):
                s = s[:m.start()] + f"({val:.6f}+0j)" + s[m.end():]
            return s, result.fun
    except Exception:
        pass
    return formula_str, None


# ============================================================
# CSV Loader
# ============================================================

def load_csv(path):
    """Load complex data from CSV.

    Auto-detects format:
    - 4 columns: z_real, z_imag, target_real, target_imag (1 variable)
    - 6 columns: z0_real, z0_imag, z1_real, z1_imag, target_real, target_imag (2 variables)
    - 3 columns: z_real, z_imag, target_real (1 variable, target_imag=0)
    
    Returns (var_list, targets, num_vars) where var_list is a list of arrays.
    """
    rows = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        for row in reader:
            rows.append([float(x) for x in row])

    if not rows:
        return [], np.array([]), 0

    ncols = len(rows[0])
    rows = np.array(rows)

    if ncols >= 6:
        # 2 variables
        z0 = rows[:, 0] + 1j * rows[:, 1]
        z1 = rows[:, 2] + 1j * rows[:, 3]
        targets = rows[:, 4] + 1j * rows[:, 5]
        return [z0, z1], targets, 2
    elif ncols >= 4:
        # 1 variable
        z = rows[:, 0] + 1j * rows[:, 1]
        targets = rows[:, 2] + 1j * rows[:, 3]
        return [z], targets, 1
    elif ncols >= 3:
        # 1 variable, real target
        z = rows[:, 0] + 1j * rows[:, 1]
        targets = rows[:, 2] + 0j
        return [z], targets, 1
    else:
        raise ValueError(f"CSV has {ncols} columns, need at least 3")


# ============================================================
# Main GP Runner
# ============================================================

def run_gp(var_data, targets, num_vars=1, pop=300, gen=40, runs=10,
           max_depth=8, seed=None, verbose=True):
    """Run GP symbolic regression with eml★ primitives.

    Parameters
    ----------
    var_data : list of arrays, each shape (n,), dtype complex
        e.g. [z] for 1 variable, [z0, z1] for 2 variables
    targets : array, shape (n,), dtype complex
    num_vars : int — number of input variables
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
    if not isinstance(var_data, list):
        var_data = [np.asarray(var_data, dtype=complex)]
    else:
        var_data = [np.asarray(v, dtype=complex) for v in var_data]
    targets = np.asarray(targets, dtype=complex)
    pset = _setup_pset(num_vars)

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
                         pset=pset, var_data=var_data, targets=targets)
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
            print(f"{status}{star_flag} ({elapsed:.1f}s)", end="")

        # Optimize constants in best formula
        if best_mse > 1e-20:
            opt_pset = _setup_pset(num_vars)
            opt_formula, opt_mse = optimize_constants(
                formula_str, opt_pset, var_data, targets, num_vars)
            if opt_mse is not None and opt_mse < best_mse:
                if verbose:
                    print(f" -> OPT {opt_mse:.2e}", end="")
                formula_str = simplify_formula(opt_formula)
                best_mse = opt_mse
                has_star = "eml_star" in formula_str or "conj_eml" in formula_str

        if verbose:
            print()  # newline

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
# Pareto Multi-Objective (NSGA-II)
# ============================================================

def _eval_pareto(individual, pset, var_data, targets):
    """Evaluate for Pareto: returns (mse, size) tuple."""
    try:
        func = gp.compile(expr=individual, pset=pset)
        pred = func(*var_data)
        pred = np.asarray(pred, dtype=complex)
        if pred.shape != targets.shape:
            return (float('inf'), float('inf'))
        err = pred - targets
        mse = float(np.mean(np.abs(err) ** 2))
        if not np.isfinite(mse):
            return (float('inf'), float('inf'))
        return (mse, float(len(individual)))
    except (ValueError, FloatingPointError, OverflowError,
            ZeroDivisionError, TypeError, MemoryError):
        return (float('inf'), float('inf'))


def run_gp_pareto(var_data, targets, num_vars=1, pop=500, gen=100,
                   max_depth=8, seed=None, verbose=True):
    """Run GP with Pareto multi-objective: minimize MSE AND formula size.
    
    Returns a Pareto front: list of (formula, mse, size) sorted by MSE.
    """
    if not isinstance(var_data, list):
        var_data = [np.asarray(var_data, dtype=complex)]
    else:
        var_data = [np.asarray(v, dtype=complex) for v in var_data]
    targets = np.asarray(targets, dtype=complex)
    pset = _setup_pset(num_vars)

    # Multi-objective fitness: minimize both MSE and size
    if not hasattr(creator, "FitnessPareto"):
        creator.create("FitnessPareto", base.Fitness, weights=(-1.0, -1.0))
    if not hasattr(creator, "IndividualPareto"):
        creator.create("IndividualPareto", gp.PrimitiveTree,
                       fitness=creator.FitnessPareto)

    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=4)
    toolbox.register("individual", tools.initIterate,
                     creator.IndividualPareto, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", _eval_pareto,
                     pset=pset, var_data=var_data, targets=targets)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
    toolbox.decorate("mate",
                     gp.staticLimit(key=operator.attrgetter("height"),
                                    max_value=max_depth))
    toolbox.decorate("mutate",
                     gp.staticLimit(key=operator.attrgetter("height"),
                                    max_value=max_depth))

    if verbose:
        print(f"Pareto GP: pop={pop}, gen={gen}, depth<={max_depth}")

    population = toolbox.population(n=pop)
    hof = tools.ParetoFront()

    start = time.time()
    algorithms.eaMuPlusLambda(population, toolbox,
                              mu=pop, lambda_=pop,
                              cxpb=0.7, mutpb=0.2, ngen=gen,
                              halloffame=hof, verbose=False)
    elapsed = time.time() - start

    # Extract Pareto front
    pareto = []
    for ind in hof:
        mse = ind.fitness.values[0]
        size = int(ind.fitness.values[1])
        formula = simplify_formula(str(ind))
        has_star = "eml_star" in formula or "conj_eml" in formula
        if np.isfinite(mse):
            pareto.append({
                'formula': formula,
                'mse': mse,
                'size': size,
                'has_eml_star': has_star,
            })

    pareto.sort(key=lambda r: r['mse'])

    # Remove duplicates
    seen = set()
    unique = []
    for p in pareto:
        key = (round(p['mse'], 10), p['size'])
        if key not in seen:
            seen.add(key)
            unique.append(p)
    pareto = unique

    if verbose:
        print(f"Done in {elapsed:.1f}s. Pareto front: {len(pareto)} solutions\n")
        print(f"{'MSE':<14} {'Size':<6} {'eml★':<6} Formula")
        print("-" * 80)
        for p in pareto[:15]:
            star = "YES" if p['has_eml_star'] else "no"
            tag = " <<<< EXACT" if p['mse'] < 1e-20 else ""
            print(f"{p['mse']:<14.4e} {p['size']:<6} {star:<6} {p['formula']}{tag}")

    return pareto


# ============================================================
# ADF: Automatically Defined Functions
# ============================================================

def find_common_subtrees(results, min_count=2):
    """Find sub-expressions that appear in multiple good formulas."""
    subtrees = {}
    for r in results:
        f = r['formula']
        for match in re.finditer(
            r'(eml|eml_star|conj_eml|add|sub|mul|ln|log10|div|sin|cos|exp|pow|arcsin|arccos|arctan)\([^()]*\)', f
        ):
            sub = match.group()
            if len(sub) > 5 and sub != f:
                subtrees[sub] = subtrees.get(sub, 0) + 1

    common = [(expr, count) for expr, count in
              sorted(subtrees.items(), key=lambda x: -x[1])
              if count >= min_count]
    return common[:10]


def _try_compile_subtree(expr_str, var_data, num_vars):
    """Try to compile a subtree expression and evaluate it on data.
    
    Returns the computed array if successful, None otherwise.
    """
    try:
        pset = _setup_pset(num_vars)
        tree = gp.PrimitiveTree.from_string(expr_str, pset)
        func = gp.compile(expr=tree, pset=pset)
        result = func(*var_data)
        result = np.asarray(result, dtype=complex)
        
        if result.shape != var_data[0].shape:
            return None
        if not np.all(np.isfinite(result)):
            return None
        # Check it's not trivially constant
        if np.std(np.abs(result)) < 1e-10:
            return None
        # Check it's not identical to an existing variable
        for v in var_data:
            if np.allclose(result, v, atol=1e-10):
                return None
        return result
    except Exception:
        return None


def run_gp_with_adf(var_data, targets, num_vars=1, pop=500, gen=100, runs=5,
                     rounds=5, max_depth=8, seed=42, verbose=True):
    """Run GP with self-expanding variables.

    Each round:
    1. Run GP with current variables
    2. Find common sub-expressions in best formulas
    3. Evaluate them on the data
    4. Add useful ones as new variables for the next round
    5. Stop when no improvement or no new variables
    """
    if not isinstance(var_data, list):
        var_data = [np.asarray(var_data, dtype=complex)]
    else:
        var_data = [np.asarray(v, dtype=complex) for v in var_data]
    targets = np.asarray(targets, dtype=complex)

    all_results = []
    best_mse_ever = float('inf')
    adf_names = []  # track what was added

    for round_idx in range(rounds):
        round_gen = gen * (round_idx + 1)

        if verbose:
            print(f"\n{'='*60}")
            print(f"  Round {round_idx + 1}/{rounds} | vars={num_vars} "
                  f"| pop={pop} gen={round_gen}")
            if adf_names:
                print(f"  Added variables: {adf_names}")
            print(f"{'='*60}")

        results = run_gp(var_data, targets, num_vars=num_vars,
                        pop=pop, gen=round_gen, runs=runs,
                        max_depth=max_depth,
                        seed=seed + round_idx * 100 if seed else None,
                        verbose=verbose)
        all_results.extend(results)

        # Check improvement
        round_best = min(r['mse'] for r in results)
        improved = round_best < best_mse_ever * 0.95  # 5% improvement threshold
        best_mse_ever = min(best_mse_ever, round_best)

        if round_best < 1e-20:
            if verbose:
                print(f"\n*** EXACT SOLUTION FOUND ***")
            break

        # Find common subtrees
        good = [r for r in results if r['mse'] < float('inf')]
        common = find_common_subtrees(good, min_count=2)

        if verbose and common:
            print(f"\nCommon subtrees (candidates for new variables):")
            for expr, count in common[:5]:
                print(f"  [{count}x] {expr}")

        # Try to promote best subtrees to new variables
        added_any = False
        for expr, count in common[:3]:  # try top 3
            new_col = _try_compile_subtree(expr, var_data, num_vars)
            if new_col is not None:
                var_data.append(new_col)
                num_vars += 1
                adf_name = f"v{num_vars - 1}={expr}"
                adf_names.append(adf_name)
                added_any = True
                if verbose:
                    print(f"  -> NEW VARIABLE z{num_vars - 1} = {expr}")
                break  # one new variable per round

        if not added_any and not improved:
            if verbose:
                print(f"\nNo new variables found and no improvement. Stopping.")
            break
        elif not added_any:
            if verbose:
                print(f"\nNo compilable subtrees. Continuing with more gens.")

    # Sort all results
    all_results.sort(key=lambda r: r['mse'])

    if verbose:
        print(f"\n{'='*60}")
        print(f"  FINAL RESULTS ({round_idx + 1} rounds, {len(all_results)} runs)")
        print(f"{'='*60}")
        print(f"Best MSE: {all_results[0]['mse']:.4e}")
        print(f"Formula: {all_results[0]['formula']}")
        print(f"Variables used: {num_vars} ({len(adf_names)} added)")
        if adf_names:
            print(f"Derived variables:")
            for name in adf_names:
                print(f"  {name}")
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
        var_data, targets, num_vars = load_csv(csv_path)
        print(f"Loaded {len(targets)} points, {num_vars} variable(s)")
        print(f"ADF mode: {rounds} rounds\n")

        results = run_gp_with_adf(var_data, targets, num_vars=num_vars,
                                   pop=1000, gen=100,
                                   runs=5, rounds=rounds, seed=42)

        out_path = csv_path.replace(".csv", "_adf_results.txt")
        with open(out_path, "w") as f:
            for r in results:
                f.write(f"MSE={r['mse']:.4e}  eml_star={r['has_eml_star']}  "
                        f"{r['formula']}\n")
        print(f"\nResults saved to {out_path}")

    elif len(sys.argv) > 1 and sys.argv[1] == "--pareto":
        # Pareto mode
        if len(sys.argv) < 3:
            print("Usage: python3 discover_gp.py --pareto data.csv "
                  "[--pop 500] [--gen 100]")
            sys.exit(1)

        csv_path = sys.argv[2]
        pop = 500
        gen = 100

        i = 3
        while i < len(sys.argv) - 1:
            if sys.argv[i] == "--pop":
                pop = int(sys.argv[i + 1])
            elif sys.argv[i] == "--gen":
                gen = int(sys.argv[i + 1])
            i += 2

        print(f"Loading {csv_path}...")
        var_data, targets, num_vars = load_csv(csv_path)
        print(f"Loaded {len(targets)} points, {num_vars} variable(s)")
        print(f"Pareto mode: pop={pop}, gen={gen}\n")

        pareto = run_gp_pareto(var_data, targets, num_vars=num_vars,
                                pop=pop, gen=gen, seed=42)

        out_path = csv_path.replace(".csv", "_pareto.txt")
        with open(out_path, "w") as f:
            for p in pareto:
                f.write(f"MSE={p['mse']:.4e}  size={p['size']}  "
                        f"eml_star={p['has_eml_star']}  {p['formula']}\n")
        print(f"\nPareto front saved to {out_path}")

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
        var_data, targets, num_vars = load_csv(csv_path)
        print(f"Loaded {len(targets)} points, {num_vars} variable(s)")
        print(f"Settings: pop={pop}, gen={gen}, runs={runs}\n")

        results = run_gp(var_data, targets, num_vars=num_vars,
                        pop=pop, gen=gen, runs=runs)

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

        results = run_gp([z], targets, num_vars=1, pop=200, gen=30, runs=3,
                         max_depth=6, seed=42)
