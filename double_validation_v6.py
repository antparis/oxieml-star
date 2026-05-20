#!/usr/bin/env python3
"""
double_validation_v6.py
Cross-validation of anti-holomorphic detection via two independent bridges,
extended to the full 9-family synthetic battery.

Hypothesis (Monnerot, 2026): the anti-holomorphic structure of a map can be
detected by PySR through two formally equivalent but conceptually distinct
operator routes:

  Route A (native anti-holomorphic):  toolbox = {eml, emlstar}
  Route B (real-part bridge):         toolbox = {eml, my_real}

Neither toolbox is given conj() directly, so each route has exactly ONE door
to anti-holomorphy:
  - Route A reaches it via emlstar(x,y) = exp(conj(x)) - log(conj(y)).
  - Route B reaches it via my_real(z) = Re(z), since conj(z) = 2*Re(z) - z.

Battery (9 families, all labels certified by the SymPy judge, df/d(zbar)):
  anti_conj_linear : conj(z)+c           anti  (degree 1)
  anti_mod_squared : z*conj(z)=|z|^2     anti  (real-valued output)
  anti_mixed_deg3  : z*conj(z)^2         anti  (mixed)
  holo_control     : z^2+c               holo  (control)
  anti_conj_cube   : conj(z)^3           anti  (degree 3)
  anti_exp_conj    : exp(conj(z))        anti  (TRANSCENDENTAL)
  anti_re_z2       : Re(z^2)             anti  (real-valued output)
  holo_exp         : exp(z)              holo  (transcendental control)
  holo_trap_inv    : 1/z                 holo  (trap: anti*anti cancels)

Core (operators, toolboxes, PySR config, detection logic) is unchanged from
double_validation_v4.py to stay consistent with paper v8. Only DATASETS,
EXPECTED and OUTPUT_JSON were extended.

Usage:
    python3 -u double_validation_v6.py             # run all
    python3 -u double_validation_v6.py --resume    # skip completed runs
    python3 -u double_validation_v6.py --datasets holo_exp holo_trap_inv

Author: Anthony Monnerot, 2026.
"""
import os
import sys
import json
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
DATA_DIR = "data"
OUTPUT_JSON = "double_validation_v6_result.json"

DATASETS = {
    "anti_conj_linear": "anti_conj_linear.csv",  # conj(z)+c        (anti, degree 1)
    "anti_mod_squared": "anti_mod_squared.csv",  # z*conj(z)=|z|^2  (anti, real output)
    "anti_mixed_deg3":  "anti_mixed_deg3.csv",   # z*conj(z)^2      (anti, mixed)
    "holo_control":     "holo_control.csv",      # z^2+c            (holo control)
    "anti_conj_cube":   "anti_conj_cube.csv",    # conj(z)^3        (anti, degree 3)
    "anti_exp_conj":    "anti_exp_conj.csv",     # exp(conj(z))     (anti, transcendental)
    "anti_re_z2":       "anti_re_z2.csv",        # Re(z^2)          (anti, real output)
    "holo_exp":         "holo_exp.csv",          # exp(z)           (holo, transcendental)
    "holo_trap_inv":    "holo_trap_inv.csv",     # 1/z              (holo trap)
}

# Expected verdict per dataset, certified by the SymPy judge (verify_exact.py)
# via the Wirtinger derivative df/d(zbar). See --formula run, ETAPE 1.
EXPECTED = {
    "anti_conj_linear": "anti",
    "anti_mod_squared": "anti",
    "anti_mixed_deg3":  "anti",
    "holo_control":     "holo",
    "anti_conj_cube":   "anti",
    "anti_exp_conj":    "anti",
    "anti_re_z2":       "anti",
    "holo_exp":         "holo",
    "holo_trap_inv":    "holo",
}

# Operator definitions copied verbatim from pysr_stacking.py (paper v8).
EML_DEF     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR_DEF = "emlstar(x, y) = exp(conj(x)) - log(conj(y) + (1e-30 + 0im))"
MYREAL_DEF  = "my_real(z) = complex(real(z))"

# Two toolboxes. CRITICAL: no my_conj in either, so each route has exactly
# one anti-holomorphic door (emlstar for A, my_real for B).
TOOLBOXES = {
    "A_emlstar": dict(
        binary_operators=["+", "-", "*", "/", EML_DEF, EMLSTAR_DEF],
        unary_operators=["cos", "sin", "exp", "log"],
        marker="emlstar",
    ),
    "B_re": dict(
        binary_operators=["+", "-", "*", "/", EML_DEF],
        unary_operators=["cos", "sin", "exp", "log", MYREAL_DEF],
        marker="my_real",
    ),
}

# SymPy mappings for the custom operators (required by PySR). Copied verbatim
# from pysr_stacking.py to guarantee consistency with paper v8.
EXTRA_SYMPY_MAPPINGS = {
    "eml": lambda x, y: sympy.exp(x) - sympy.log(y),
    "emlstar": lambda x, y: sympy.exp(sympy.conjugate(x)) - sympy.log(sympy.conjugate(y)),
    "my_real": lambda z: sympy.re(z),
}

# PySR config. Deterministic + serial for full reproducibility (paper v8 §4.1).
# verbosity=1 + progress=True: show PySR's native generation-by-generation
# progress during each search, so a long run is never a black box (lesson
# carried over from the v5b KiDS run).
PYSR_BASE = dict(
    niterations=100,
    population_size=50,
    precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    verbosity=1,
    progress=True,
    deterministic=True,
    parallelism="serial",
    random_state=42,
    maxsize=20,
    maxdepth=8,
)


# ============================================================
# HELPERS
# ============================================================
def log(msg):
    """Print and flush immediately so progress is visible in real time."""
    print(msg, flush=True)


def load_dataset(csv_name):
    df = pd.read_csv(os.path.join(DATA_DIR, csv_name))
    z = df["z_real"].values + 1j * df["z_imag"].values
    y = df["target_real"].values + 1j * df["target_imag"].values
    X = z.reshape(-1, 1).astype(np.complex128)
    y = y.astype(np.complex128)
    return X, y


def run_pysr(X, y, toolbox):
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
    return marker in equation_str


def load_partial_results():
    """Load existing JSON if present (for --resume), else return fresh dict."""
    if os.path.exists(OUTPUT_JSON):
        try:
            with open(OUTPUT_JSON) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return None


def save_results(results):
    """Write results to disk. Called after every run (incremental save)."""
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=list(DATASETS.keys()))
    parser.add_argument("--resume", action="store_true",
                        help="skip runs already present in the JSON")
    args = parser.parse_args()

    # Fresh or resumed results
    results = None
    if args.resume:
        results = load_partial_results()
        if results is not None:
            log("Resuming from existing JSON; completed runs will be skipped.")
    if results is None:
        results = {
            "timestamp": datetime.now().isoformat() + "+00:00",
            "pysr_config": {k: v for k, v in PYSR_BASE.items()
                            if k != "elementwise_loss"},
            "toolbox_A": "{eml, emlstar} (native anti-holomorphic, no conj, no Re)",
            "toolbox_B": "{eml, my_real} (real-part bridge, no conj, no emlstar)",
            "runs": {},
        }

    total = len(args.datasets) * len(TOOLBOXES)
    done = 0

    for ds_name in args.datasets:
        csv_name = DATASETS[ds_name]
        log(f"\n{'='*60}\nDATASET: {ds_name}  ({csv_name})\n{'='*60}")
        X, y = load_dataset(csv_name)
        results["runs"].setdefault(ds_name, {})

        for tb_name, toolbox in TOOLBOXES.items():
            done += 1
            # Resume: skip if this run already exists
            if args.resume and tb_name in results["runs"].get(ds_name, {}):
                log(f"[{done}/{total}] {ds_name} - {tb_name}: already done, skipping.")
                continue

            log(f"\n[{done}/{total}] {ds_name} - Toolbox {tb_name} (running PySR...)")
            eq, mse = run_pysr(X, y, toolbox)
            anti = detect_anti_holomorphic(eq, toolbox["marker"])
            verdict = "ANTI-HOLOMORPHIC" if anti else "holomorphic"
            log(f"  best eq : {eq}")
            log(f"  MSE     : {mse:.3e}")
            log(f"  verdict : {verdict}  (marker '{toolbox['marker']}' "
                f"{'found' if anti else 'absent'})")

            results["runs"][ds_name][tb_name] = {
                "best_equation": eq,
                "best_mse": mse,
                "anti_holomorphic": bool(anti),
                "marker": toolbox["marker"],
            }
            # INCREMENTAL SAVE — after every single run
            save_results(results)
            log(f"  [saved to {OUTPUT_JSON}]")

    # Summary table
    log(f"\n{'='*72}\nSUMMARY\n{'='*72}")
    log("{:<18}{:<10}{:<24}{:<24}".format(
        "Dataset", "Expected", "Route A (eml*)", "Route B (Re)"))
    for ds_name in args.datasets:
        a = results["runs"][ds_name].get("A_emlstar")
        b = results["runs"][ds_name].get("B_re")
        exp = EXPECTED.get(ds_name, "?")
        if a is None or b is None:
            log("{:<18}{:<10}{}".format(ds_name, exp, "incomplete"))
            continue
        va = "anti" if a["anti_holomorphic"] else "holo"
        vb = "anti" if b["anti_holomorphic"] else "holo"
        # mark mismatch with expected
        ma = "" if va == exp else " !"
        mb = "" if vb == exp else " !"
        cell_a = "{}{}  (MSE {:.1e})".format(va, ma, a["best_mse"])
        cell_b = "{}{}  (MSE {:.1e})".format(vb, mb, b["best_mse"])
        log("{:<18}{:<10}{:<24}{:<24}".format(ds_name, exp, cell_a, cell_b))
    log("(' !' marks a verdict that disagrees with the judge-certified one)")

    # Cross-validation verdict (only over fully-completed datasets)
    complete = [ds for ds in args.datasets
                if "A_emlstar" in results["runs"].get(ds, {})
                and "B_re" in results["runs"].get(ds, {})]
    agree = all(
        results["runs"][ds]["A_emlstar"]["anti_holomorphic"]
        == results["runs"][ds]["B_re"]["anti_holomorphic"]
        for ds in complete
    ) if complete else False
    results["routes_agree"] = bool(agree)
    results["datasets_complete"] = complete
    save_results(results)
    log(f"\nRoutes agree on all completed datasets: {agree}")
    log(f"Results written to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
