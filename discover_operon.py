#!/usr/bin/env python3
"""
discover_operon.py
Operon + eml★ Integration for galaxy rotation curves.
Encodes complex z = radius + i*V_bar as real features.
Detects eml★ usage via anti-holomorphic feature columns.

All code and comments in English.
"""

import os
import glob
import json
import numpy as np

from pyoperon.sklearn import SymbolicRegressor


def build_features(radius, vbar):
    """
    Expand complex z = radius + i*V_bar into real columns.
    
    Columns 0-4: standard complex features
    Columns 5-6: holomorphic exp(z) components
    Column 7: anti-holomorphic marker = -Im(exp(z)) = Im(exp(conj(z)))
              This is the ONLY column that carries conjugation information.
    """
    x = radius.astype(float)
    y = vbar.astype(float)

    # Clamp exp to avoid overflow
    x_safe = np.clip(x, -500, 500)

    features = np.column_stack([
        x,                                    # 0: r
        y,                                    # 1: vbar
        x**2 + y**2,                          # 2: |z|^2
        x**2 - y**2,                          # 3: Re(z^2)
        2 * x * y,                            # 4: Im(z^2)
        np.exp(x_safe) * np.cos(y),           # 5: Re(exp(z))
        np.exp(x_safe) * np.sin(y),           # 6: Im(exp(z))
        -np.exp(x_safe) * np.sin(y),          # 7: Im(exp(conj(z))) = -Im(exp(z))
    ])

    return features


FEATURE_NAMES = ['r', 'vbar', 'mod2', 're_z2', 'im_z2',
                 're_expz', 'im_expz', 'im_exp_conjz']


def detect_emlstar(formula_str, n_features_with, n_features_without):
    """
    Detect if the formula uses anti-holomorphic features.
    Operon names variables X1..Xn (1-indexed).
    The eml★ column is the last one (index n_features_with in 1-indexed).
    """
    emlstar_var = f'X{n_features_with}'
    return emlstar_var in formula_str


def run_operon(csv_path, pop=1000, gen=500, runs=3):
    """
    Run Operon twice on the same data:
    - With all features (allows eml★ detection)
    - Without anti-holomorphic feature (column 7 removed)
    Best of multiple runs kept.
    """
    print(f"\nProcessing: {os.path.basename(csv_path)}")

    # Load CSV
    data = np.genfromtxt(csv_path, delimiter=',', skip_header=1)
    if data.ndim < 2 or data.shape[1] < 3:
        print(f"  Skipping: bad format ({data.shape})")
        return None

    radius = data[:, 0]
    vbar = data[:, 1]
    y = data[:, 2]  # V_obs target

    if len(y) < 5:
        print(f"  Skipping: too few points ({len(y)})")
        return None

    # Build features
    X_full = build_features(radius, vbar)       # 8 columns (0-7)
    X_no_eml = X_full[:, :7]                    # 7 columns (0-6, no conj)

    n_with = X_full.shape[1]
    n_without = X_no_eml.shape[1]

    # Check for NaN/Inf
    if np.any(~np.isfinite(X_full)) or np.any(~np.isfinite(y)):
        print(f"  Skipping: NaN/Inf in data")
        return None

    best_mse_with = float('inf')
    best_formula_with = ""
    best_mse_without = float('inf')
    best_formula_without = ""

    seeds = [42, 123, 789][:runs]

    for seed in seeds:
        # Run WITH eml★ features
        try:
            reg_with = SymbolicRegressor(
                allowed_symbols='add,sub,mul,div,constant,variable,sin,cos,exp,log,square,pow',
                population_size=pop,
                generations=gen,
                max_length=30,
                max_depth=8,
                n_threads=1,
                optimizer='lm',
                random_state=seed
            )
            reg_with.fit(X_full, y)
            pred = reg_with.predict(X_full)
            mse = float(np.mean((y - pred) ** 2))
            if mse < best_mse_with:
                best_mse_with = mse
                best_formula_with = reg_with.get_model_string(reg_with.model_, 10)
        except Exception as e:
            print(f"  Run with (seed={seed}) error: {e}")

        # Run WITHOUT eml★ features
        try:
            reg_without = SymbolicRegressor(
                allowed_symbols='add,sub,mul,div,constant,variable,sin,cos,exp,log,square,pow',
                population_size=pop,
                generations=gen,
                max_length=30,
                max_depth=8,
                n_threads=1,
                optimizer='lm',
                random_state=seed
            )
            reg_without.fit(X_no_eml, y)
            pred = reg_without.predict(X_no_eml)
            mse = float(np.mean((y - pred) ** 2))
            if mse < best_mse_without:
                best_mse_without = mse
                best_formula_without = reg_without.get_model_string(reg_without.model_, 10)
        except Exception as e:
            print(f"  Run without (seed={seed}) error: {e}")

    # Detect eml★
    uses_emlstar = detect_emlstar(best_formula_with, n_with, n_without)

    improvement = 0.0
    if best_mse_without > 0:
        improvement = (best_mse_without - best_mse_with) / best_mse_without * 100

    result = {
        'file': os.path.basename(csv_path),
        'mse_with': best_mse_with,
        'mse_without': best_mse_without,
        'improvement': improvement,
        'uses_emlstar': uses_emlstar,
        'formula_with': best_formula_with,
        'formula_without': best_formula_without,
        'n_points': len(y)
    }

    print(f"  Points:        {len(y)}")
    print(f"  MSE with:      {best_mse_with:.6e}")
    print(f"  MSE without:   {best_mse_without:.6e}")
    print(f"  Improvement:   {improvement:+.2f}%")
    print(f"  eml★ detected: {uses_emlstar}")
    print(f"  Formula:       {best_formula_with[:80]}...")

    return result


def run_operon_batch(csv_dir="data", pattern="sparc_*.csv"):
    """Run Operon on all matching CSVs."""
    csv_files = sorted(glob.glob(os.path.join(csv_dir, pattern)))
    if not csv_files:
        print(f"No files matching {pattern} in {csv_dir}")
        return []

    print(f"Found {len(csv_files)} files")
    results = []

    for csv_path in csv_files:
        try:
            res = run_operon(csv_path, pop=500, gen=200, runs=2)
            if res:
                results.append(res)
        except Exception as e:
            print(f"Error on {csv_path}: {e}")

    # Save
    with open("operon_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Summary
    n_eml = sum(1 for r in results if r['uses_emlstar'])
    print(f"\n{'='*60}")
    print(f"OPERON BATCH COMPLETE")
    print(f"Galaxies: {len(results)}")
    print(f"eml★ detected: {n_eml} ({100*n_eml/len(results):.1f}%)")
    print(f"{'='*60}")

    return results


if __name__ == "__main__":
    import sys
    print("=== Operon + eml★ Integration ===\n")

    if len(sys.argv) > 1:
        # Single file mode
        result = run_operon(sys.argv[1])
    else:
        # Batch mode
        run_operon_batch(csv_dir="data", pattern="sparc_*.csv")
