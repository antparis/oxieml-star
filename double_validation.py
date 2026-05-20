#!/usr/bin/env python3
"""
double_validation.py
Cross-validation of anti-holomorphic detection via two independent bridges.

Hypothesis (Monnerot, 2026): the anti-holomorphic structure of a map can be
detected by PySR through two formally equivalent but conceptually distinct
operator routes:

  Route A (native anti-holomorphic):  toolbox = {eml, emlstar}
  Route B (real-part bridge):         toolbox = {eml, my_real}

Neither toolbox is given conj() directly, so each route has exactly ONE door
to anti-holomorphy:
  - Route A reaches it via emlstar(x,y) = exp(conj(x)) - log(conj(y)).
  - Route B reaches it via my_real(z) = Re(z), since conj(z) = 2*Re(z) - z.

If both routes flag Tricorn (conj(z)^2 + c) as anti-holomorphic and both
leave Mandelbrot (z^2 + c) holomorphic, the two bridges agree -> the
detection is route-independent.

Operator definitions are copied verbatim from pysr_stacking.py to guarantee
consistency with the published paper (v8).

Author: Anthony Monnerot, 2026.
"""
import os
import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime

try:
    from pysr import PySRRegressor
except ImportError:
    print("ERROR: PySR not installed. pip install pysr")
    exit(1)

# ============================================================
# CONFIGURATION
# ============================================================
DATA_DIR = "data"
OUTPUT_JSON = "double_validation_result.json"

DATASETS = {
    "mandelbrot": "fractal_mandelbrot.csv",   # z -> z^2 + c        (holomorphic)
    "tricorn":    "fractal_tricorn.csv",      # z -> conj(z)^2 + c  (anti-holomorphic)
}

# Operator definitions copied verbatim from pysr_stacking.py (paper v8).
# eml     : holomorphic    exp(x) - log(y)
# emlstar : anti-holomorphic  exp(conj(x)) - log(conj(y))
# my_real : Re(z) cast to complex
EML_DEF     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR_DEF = "emlstar(x, y) = exp(conj(x)) - log(conj(y) + (1e-30 + 0im))"
MYREAL_DEF  = "my_real(z) = complex(real(z))"

# Two toolboxes. CRITICAL: no my_conj in either, so each route has exactly
# one anti-holomorphic door (emlstar for A, my_real for B).
TOOLBOXES = {
    "A_emlstar": dict(
        binary_operators=["+", "-", "*", "/", EML_DEF, EMLSTAR_DEF],
        unary_operators=["cos", "sin", "exp", "log"],
        marker="emlstar",   # token whose presence => anti-holomorphic
    ),
    "B_re": dict(
        binary_operators=["+", "-", "*", "/", EML_DEF],
        unary_operators=["cos", "sin", "exp", "log", MYREAL_DEF],
        marker="my_real",   # token whose presence => anti-holomorphic (via 2Re-z)
    ),
}

# SymPy mappings for the custom operators (required by PySR). Copied verbatim
# from pysr_stacking.py (lines 170-172) to guarantee consistency with paper v8.
import sympy
EXTRA_SYMPY_MAPPINGS = {
    "eml": lambda x, y: sympy.exp(x) - sympy.log(y),
    "emlstar": lambda x, y: sympy.exp(sympy.conjugate(x)) - sympy.log(sympy.conjugate(y)),
    "my_real": lambda z: sympy.re(z),
}

# PySR config. Deterministic + serial for full reproducibility (paper v8 §4.1).
PYSR_BASE = dict(
    niterations=100,
    population_size=50,
    precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    verbosity=0,
    deterministic=True,
    parallelism="serial",
    random_state=42,
    maxsize=20,
    maxdepth=8,
)


# ============================================================
# HELPERS
# ============================================================
def load_dataset(csv_name):
    """Load a fractal CSV. Returns X (N,1 complex) and y (N, complex)."""
    df = pd.read_csv(os.path.join(DATA_DIR, csv_name))
    z = df["z_real"].values + 1j * df["z_imag"].values
    y = df["target_real"].values + 1j * df["target_imag"].values
    X = z.reshape(-1, 1).astype(np.complex128)
    y = y.astype(np.complex128)
    return X, y


def run_pysr(X, y, toolbox):
    """Run one PySR fit with the given toolbox. Returns (best_eq_str, best_mse)."""
    # Only pass the sympy mappings for operators actually used in this toolbox.
    all_ops = " ".join(toolbox["binary_operators"] + toolbox["unary_operators"])
    mappings = {name: fn for name, fn in EXTRA_SYMPY_MAPPINGS.items()
                if name in all_ops}
    model = PySRRegressor(
        binary_operators=toolbox["binary_operators"],
        unary_operators=toolbox["unary_operators"],
        extra_sympy_mappings=mappings,
        **PYSR_BASE,
    )
    model.fit(X, y)
    best_eq = str(model.get_best()["equation"])
    best_mse = float(model.get_best()["loss"])
    return best_eq, best_mse


def detect_anti_holomorphic(equation_str, marker):
    """A formula is anti-holomorphic if it contains the toolbox's marker token."""
    return marker in equation_str


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=list(DATASETS.keys()))
    args = parser.parse_args()

    results = {
        "timestamp": datetime.now().isoformat() + "+00:00",
        "pysr_config": {k: v for k, v in PYSR_BASE.items()
                        if k not in ("elementwise_loss",)},
        "toolbox_A": "{eml, emlstar} (native anti-holomorphic, no conj, no Re)",
        "toolbox_B": "{eml, my_real} (real-part bridge, no conj, no emlstar)",
        "runs": {},
    }

    for ds_name in args.datasets:
        csv_name = DATASETS[ds_name]
        print(f"\n{'='*60}\nDATASET: {ds_name}  ({csv_name})\n{'='*60}")
        X, y = load_dataset(csv_name)
        results["runs"][ds_name] = {}

        for tb_name, toolbox in TOOLBOXES.items():
            print(f"\n--- Toolbox {tb_name} ---")
            eq, mse = run_pysr(X, y, toolbox)
            anti = detect_anti_holomorphic(eq, toolbox["marker"])
            verdict = "ANTI-HOLOMORPHIC" if anti else "holomorphic"
            print(f"  best eq : {eq}")
            print(f"  MSE     : {mse:.3e}")
            print(f"  verdict : {verdict}  (marker '{toolbox['marker']}' "
                  f"{'found' if anti else 'absent'})")
            results["runs"][ds_name][tb_name] = {
                "best_equation": eq,
                "best_mse": mse,
                "anti_holomorphic": bool(anti),
                "marker": toolbox["marker"],
            }

    # Summary table
    print(f"\n{'='*60}\nSUMMARY\n{'='*60}")
    print(f"{'Dataset':<14}{'Route A (eml*)':<22}{'Route B (Re)':<22}")
    for ds_name in args.datasets:
        a = results["runs"][ds_name]["A_emlstar"]
        b = results["runs"][ds_name]["B_re"]
        va = "anti" if a["anti_holomorphic"] else "holo"
        vb = "anti" if b["anti_holomorphic"] else "holo"
        cell_a = "{}  (MSE {:.1e})".format(va, a["best_mse"])
        cell_b = "{}  (MSE {:.1e})".format(vb, b["best_mse"])
        print("{:<14}{:<22}{:<22}".format(ds_name, cell_a, cell_b))

    # Cross-validation verdict
    agree = all(
        results["runs"][ds]["A_emlstar"]["anti_holomorphic"]
        == results["runs"][ds]["B_re"]["anti_holomorphic"]
        for ds in args.datasets
    )
    results["routes_agree"] = bool(agree)
    print(f"\nRoutes agree on all datasets: {agree}")

    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
