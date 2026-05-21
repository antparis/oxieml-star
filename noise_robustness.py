#!/usr/bin/env python3
"""
noise_robustness.py
Calibration tool: measure the FALSE-POSITIVE rate of the anti-holomorphic
detector when fed HOLOMORPHIC targets corrupted by growing Gaussian noise.

Why
---
On clean synthetic data the detector reaches ~1e-32 and never misfires.
Real data are noisy. The danger: PySR may prefer a formula that uses the
anti-holomorphic door (emlstar or my_real) just to absorb noise, yielding a
spurious "anti" verdict on a target that is in fact holomorphic. This script
maps the noise level at which that starts to happen, so we know the regime in
which an "anti" verdict on real data is trustworthy.

Method
------
For each holomorphic target f (e.g. z^2+c, exp(z), 1/z):
  for each relative noise level s in LEVELS:
    repeat REPS times with independent noise seeds:
      y_noisy = f(z) + s * rms(|f(z)|) * (N(0,1)+i N(0,1))/sqrt(2)
      run PySR with Route A (eml*) and Route B (Re)
      a verdict of "anti" is a FALSE POSITIVE (the target is holomorphic)
  report false-positive rate per (target, level, route).

A robust detector should keep FP rate ~0 up to some noise level, then rise.
That knee is the reliability boundary.

Operators, toolboxes and PySR config are copied verbatim from
double_validation_v6.py to keep verdicts comparable.

Usage
-----
    python3 -u noise_robustness.py                       # defaults
    python3 -u noise_robustness.py --targets holo_control exp
    python3 -u noise_robustness.py --levels 0 0.05 0.1 0.2 --reps 5
    python3 -u noise_robustness.py --niter 60            # faster calibration

WARNING: cost = len(targets) * len(levels) * reps * 2 toolboxes PySR runs,
~2-3 min each. Defaults below = 1*5*3*2 = 30 runs (~60-90 min). Do NOT run
in parallel with double_validation_v6.py (shared CPU).

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
OUTPUT_JSON = "noise_robustness_result.json"
OUTPUT_CSV = "noise_robustness_curve.csv"

N = 200
SAMPLE_SEED = 42
C = -0.7 + 0.27015j

# Holomorphic targets ONLY (any "anti" verdict here is a false positive).
HOLO_TARGETS = {
    "holo_control": lambda z: z ** 2 + C,   # z^2+c
    "exp":          lambda z: np.exp(z),     # exp(z)
    "inv":          lambda z: 1.0 / z,       # 1/z
}
CLIP_ORIGIN = {"inv"}

# Operator definitions copied verbatim from double_validation_v6.py.
EML_DEF     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR_DEF = "emlstar(x, y) = exp(conj(x)) - log(conj(y) + (1e-30 + 0im))"
MYREAL_DEF  = "my_real(z) = complex(real(z))"

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


def sample_z(seed):
    rng = np.random.default_rng(seed)
    re = rng.uniform(-1.0, 1.0, N)
    im = rng.uniform(-1.0, 1.0, N)
    return re + 1j * im


def add_noise(t, frac, seed):
    """Add complex Gaussian noise at relative level `frac` of the signal rms."""
    rng = np.random.default_rng(seed)
    rms = np.sqrt(np.mean(np.abs(t) ** 2))
    sigma = frac * rms
    noise = sigma * (rng.standard_normal(t.shape)
                     + 1j * rng.standard_normal(t.shape)) / np.sqrt(2.0)
    return t + noise


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


def save_json(results):
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", default=list(HOLO_TARGETS.keys()))
    parser.add_argument("--levels", nargs="+", type=float,
                        default=[0.0, 0.01, 0.05, 0.1, 0.2])
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--niter", type=int, default=100)
    parser.add_argument("--resume", action="store_true",
                        help="skip runs already present in the JSON")
    parser.add_argument("--force", action="store_true",
                        help="ignore any existing JSON and restart from scratch")
    args = parser.parse_args()

    pysr_base = make_pysr_base(args.niter)

    # Checkpoint: reuse the result JSON as the state file (same fixed niter
    # budget for both routes so false-positive rates stay comparable).
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
            "note": "false positives: HOLOMORPHIC targets + Gaussian noise; "
                    "an 'anti' verdict is a false positive.",
            "levels": args.levels,
            "reps": args.reps,
            "niterations": args.niter,
            "runs": {},
        }

    total = len(args.targets) * len(args.levels) * args.reps * len(TOOLBOXES)
    done = 0
    curve_rows = []

    for tname in args.targets:
        fn = HOLO_TARGETS[tname]
        results["runs"].setdefault(tname, {})
        for s in args.levels:
            level_key = f"{s:g}"
            results["runs"][tname].setdefault(level_key, {})
            # Recompute fp_count from any results already on disk (correct
            # resume: the rate must reflect all reps, not only this session).
            fp_count = {tb: 0 for tb in TOOLBOXES}
            for tb in TOOLBOXES:
                for entry in results["runs"][tname][level_key].get(tb, []):
                    if entry.get("false_positive"):
                        fp_count[tb] += 1
            for rep in range(args.reps):
                z = sample_z(SAMPLE_SEED + rep)   # vary sample per rep
                if tname in CLIP_ORIGIN:
                    small = np.abs(z) < 0.1
                    if np.any(small):
                        z[small] = 0.1 * np.exp(1j * np.angle(z[small]))
                t = fn(z)
                t = add_noise(t, s, seed=1000 + rep)  # independent noise seed
                X = z.reshape(-1, 1).astype(np.complex128)
                y = t.astype(np.complex128)
                for tb_name, toolbox in TOOLBOXES.items():
                    done += 1
                    # Checkpoint skip: this (target, level, rep, toolbox) done.
                    existing = results["runs"][tname][level_key].get(tb_name, [])
                    if any(e.get("rep") == rep for e in existing):
                        log(f"[{done}/{total}] {tname} noise={level_key} "
                            f"rep={rep} - {tb_name}: already done, skipping.")
                        continue
                    log(f"\n[{done}/{total}] {tname} noise={level_key} "
                        f"rep={rep} - {tb_name} (PySR...)")
                    eq, mse = run_pysr(X, y, toolbox, pysr_base)
                    anti = toolbox["marker"] in eq
                    if anti:
                        fp_count[tb_name] += 1
                    log(f"  eq={eq}")
                    log(f"  MSE={mse:.3e}  verdict="
                        f"{'ANTI (FALSE POSITIVE)' if anti else 'holo (correct)'}")
                    results["runs"][tname][level_key].setdefault(tb_name, [])
                    results["runs"][tname][level_key][tb_name].append({
                        "rep": rep, "best_equation": eq,
                        "best_mse": mse, "false_positive": bool(anti),
                    })
                    save_json(results)
            for tb_name in TOOLBOXES:
                rate = fp_count[tb_name] / args.reps
                curve_rows.append({
                    "target": tname, "noise_level": s,
                    "route": tb_name, "fp_rate": rate,
                    "reps": args.reps,
                })

    pd.DataFrame(curve_rows).to_csv(OUTPUT_CSV, index=False)

    log(f"\n{'='*72}\nFALSE-POSITIVE CURVE (anti verdict on holomorphic target)\n{'='*72}")
    log("{:<14}{:<12}{:<12}{:<10}".format("Target", "Noise", "Route", "FP_rate"))
    for row in curve_rows:
        log("{:<14}{:<12}{:<12}{:<10}".format(
            row["target"], f"{row['noise_level']:g}",
            row["route"], f"{row['fp_rate']:.2f}"))
    log(f"\nCurve written to {OUTPUT_CSV}")
    log(f"Full log written to {OUTPUT_JSON}")
    log("Reliability boundary = highest noise level where FP_rate stays 0.")


if __name__ == "__main__":
    main()
