#!/usr/bin/env python3
"""
significance_metric.py
Quantify HOW MUCH the anti-holomorphic hypothesis beats the holomorphic one,
instead of merely checking whether a marker appears in the formula.

Why
---
The v6 detector verdict = "the anti-door marker is present in the best
equation". That is binary and can be misleading: a marker may appear while
contributing nothing. For a real-data claim we need a magnitude: does adding
the anti-holomorphic door actually reduce the error, and by how much?

Method
------
For each dataset, run PySR THREE times on the SAME data, changing only the
toolbox:
  - HOLO_PURE : {+,-,*,/, cos,sin,exp,log}        no anti door at all
  - A_emlstar : HOLO_PURE + {eml, emlstar}        anti via eml*
  - B_re      : HOLO_PURE + {eml, my_real}        anti via Re
Let MSE_holo, MSE_A, MSE_B be the best losses.

Significance (per anti route r):
    sig_r = log10( MSE_holo / MSE_r )
Interpretation:
  - target truly anti  -> holo-pure cannot fit -> MSE_holo high, MSE_r tiny
    -> sig_r large (>> 0).
  - target truly holo  -> all three fit equally -> MSE_holo ~ MSE_r
    -> sig_r ~ 0.
A threshold (default 6 decades) flags a *significant* anti-holomorphic
advantage. The threshold is reported, not hard-coded into the verdict, so it
can be tuned per noise regime (combine with noise_robustness.py).

This is the magnitude test the binary marker check was missing. Note it is a
necessary complement, not a replacement, of the exact SymPy judge: PySR gives
the magnitude, the judge gives the certified nature.

Operators and PySR config copied verbatim from double_validation_v6.py.

Usage
-----
    python3 -u significance_metric.py
    python3 -u significance_metric.py --datasets anti_conj_linear holo_control
    python3 -u significance_metric.py --threshold 6 --niter 100

WARNING: cost = len(datasets) * 3 toolboxes PySR runs, ~2-3 min each.
Default 9 datasets = 27 runs (~60-80 min). Do NOT run in parallel with
double_validation_v6.py (shared CPU).

Author: Anthony Monnerot, 2026.
"""
import os
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
OUTPUT_JSON = "significance_result.json"

DATASETS = {
    "anti_conj_linear": "anti_conj_linear.csv",
    "anti_mod_squared": "anti_mod_squared.csv",
    "anti_mixed_deg3":  "anti_mixed_deg3.csv",
    "holo_control":     "holo_control.csv",
    "anti_conj_cube":   "anti_conj_cube.csv",
    "anti_exp_conj":    "anti_exp_conj.csv",
    "anti_re_z2":       "anti_re_z2.csv",
    "holo_exp":         "holo_exp.csv",
    "holo_trap_inv":    "holo_trap_inv.csv",
}

EML_DEF     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR_DEF = "emlstar(x, y) = exp(conj(x)) - log(conj(y) + (1e-30 + 0im))"
MYREAL_DEF  = "my_real(z) = complex(real(z))"

# Three toolboxes. HOLO_PURE is the baseline (no anti door whatsoever).
TOOLBOXES = {
    "HOLO_PURE": dict(
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["cos", "sin", "exp", "log"],
        marker=None,
    ),
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

EXTRA_SYMPY_MAPPINGS = {
    "eml": lambda x, y: sympy.exp(x) - sympy.log(y),
    "emlstar": lambda x, y: sympy.exp(sympy.conjugate(x)) - sympy.log(sympy.conjugate(y)),
    "my_real": lambda z: sympy.re(z),
}


def make_pysr_base(niter):
    return dict(
        niterations=niter,
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
    print(msg, flush=True)


def load_dataset(csv_name):
    df = pd.read_csv(os.path.join(DATA_DIR, csv_name))
    z = df["z_real"].values + 1j * df["z_imag"].values
    y = df["target_real"].values + 1j * df["target_imag"].values
    X = z.reshape(-1, 1).astype(np.complex128)
    y = y.astype(np.complex128)
    return X, y


def run_pysr(X, y, toolbox, pysr_base):
    all_ops = " ".join(toolbox["binary_operators"] + toolbox["unary_operators"])
    mappings = {name: fn for name, fn in EXTRA_SYMPY_MAPPINGS.items()
                if name in all_ops}
    model = PySRRegressor(
        binary_operators=toolbox["binary_operators"],
        unary_operators=toolbox["unary_operators"],
        extra_sympy_mappings=mappings,
        **pysr_base,
    )
    model.fit(X, y)
    best_eq = str(model.get_best()["equation"])
    best_mse = float(model.get_best()["loss"])
    return best_eq, best_mse


def safe_sig(mse_holo, mse_anti):
    """log10(MSE_holo / MSE_anti), guarded against zeros/negatives."""
    floor = 1e-300
    return float(np.log10(max(mse_holo, floor) / max(mse_anti, floor)))


def save_json(results):
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", default=list(DATASETS.keys()))
    parser.add_argument("--threshold", type=float, default=6.0,
                        help="decades of MSE gain to flag significant anti")
    parser.add_argument("--niter", type=int, default=100)
    parser.add_argument("--resume", action="store_true",
                        help="skip runs already present in the JSON")
    parser.add_argument("--force", action="store_true",
                        help="ignore any existing JSON and restart from scratch")
    args = parser.parse_args()

    pysr_base = make_pysr_base(args.niter)

    # Checkpoint: reuse the result JSON itself as the state file. A run is
    # 'done' if (ds_name, tb_name) already has an entry. --resume picks up
    # where a crash left off; --force ignores it. Same fixed niter budget for
    # ALL toolboxes so the significance ratio stays comparable.
    results = None
    if args.resume and not args.force and os.path.exists(OUTPUT_JSON):
        try:
            with open(OUTPUT_JSON) as f:
                results = json.load(f)
            log(f"Resuming from {OUTPUT_JSON}; completed runs will be skipped.")
        except (json.JSONDecodeError, OSError):
            results = None
    if results is None:
        results = {
            "timestamp": datetime.now().isoformat() + "+00:00",
            "note": "significance = log10(MSE_holo_pure / MSE_anti) per route.",
            "threshold_decades": args.threshold,
            "niterations": args.niter,
            "runs": {},
        }

    total = len(args.datasets) * len(TOOLBOXES)
    done = 0

    for ds_name in args.datasets:
        csv_name = DATASETS[ds_name]
        log(f"\n{'='*60}\nDATASET: {ds_name}\n{'='*60}")
        X, y = load_dataset(csv_name)
        results["runs"].setdefault(ds_name, {})
        for tb_name, toolbox in TOOLBOXES.items():
            done += 1
            # Checkpoint skip: this (dataset, toolbox) already computed.
            if tb_name in results["runs"].get(ds_name, {}):
                log(f"[{done}/{total}] {ds_name} - {tb_name}: already done, skipping.")
                continue
            log(f"\n[{done}/{total}] {ds_name} - {tb_name} (PySR...)")
            eq, mse = run_pysr(X, y, toolbox, pysr_base)
            log(f"  eq={eq}")
            log(f"  MSE={mse:.3e}")
            results["runs"][ds_name][tb_name] = {
                "best_equation": eq, "best_mse": mse,
                "marker": toolbox["marker"],
                "marker_present": bool(toolbox["marker"] and toolbox["marker"] in eq),
            }
            save_json(results)

    # Significance table
    log(f"\n{'='*84}\nSIGNIFICANCE  (sig = log10(MSE_holo_pure / MSE_anti); "
        f"threshold = {args.threshold:g} decades)\n{'='*84}")
    log("{:<18}{:<14}{:<14}{:<14}{:<14}".format(
        "Dataset", "MSE_holo", "sig_A(eml*)", "sig_B(Re)", "significant?"))
    for ds_name in args.datasets:
        r = results["runs"][ds_name]
        if not all(k in r for k in TOOLBOXES):
            log("{:<18}{}".format(ds_name, "incomplete"))
            continue
        mse_holo = r["HOLO_PURE"]["best_mse"]
        sig_a = safe_sig(mse_holo, r["A_emlstar"]["best_mse"])
        sig_b = safe_sig(mse_holo, r["B_re"]["best_mse"])
        flag = "YES" if max(sig_a, sig_b) >= args.threshold else "no"
        r_sig = {"sig_A": sig_a, "sig_B": sig_b, "significant_anti": flag == "YES"}
        results["runs"][ds_name]["significance"] = r_sig
        log("{:<18}{:<14}{:<14}{:<14}{:<14}".format(
            ds_name, f"{mse_holo:.1e}", f"{sig_a:+.1f}", f"{sig_b:+.1f}", flag))
    save_json(results)
    log(f"\nFull results written to {OUTPUT_JSON}")
    log("sig >> 0  => anti-holomorphic structure is genuinely needed to fit.")
    log("sig ~ 0   => marker (if any) is cosmetic; holo fits just as well.")


if __name__ == "__main__":
    main()
