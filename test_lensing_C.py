#!/usr/bin/env python3
"""
test_lensing_C.py — Gravitational lensing stacking test with PySR.

Run instruction (real-time monitoring with unbuffered stdout):
  python3 -u test_lensing_C.py 2>&1 | tee lensing_test_C_log.txt
"""

import json
import os
import random
import sys
import threading
from datetime import datetime, timezone

import numpy as np
import pandas as pd

INPUT_CSV = os.path.join("data", "lensing_test_A.csv")
OUTPUT_CSV = os.path.join("data", "lensing_test_C_stacked.csv")
OUTPUT_DIR = "pysr_output_lensing_C"
JSON_OUT = "lensing_test_C_result.json"

R_MIN_ARCMIN = 0.5
R_MAX_ARCMIN = 10.0
R_MIN_DEG = R_MIN_ARCMIN / 60.0
R_MAX_DEG = R_MAX_ARCMIN / 60.0
N_BINS = 20
MIN_PER_BIN = 10

NUMPY_SEED = 42
PYTHON_RANDOM_SEED = 42
PYSR_RANDOM_STATE = 42

PYSR_NITERATIONS = 200
PYSR_POPULATION_SIZE = 300
PYSR_MAXSIZE = 20
PYSR_PARSIMONY = 0.001

STATE_WRITE_INTERVAL_SEC = 30
EMLSTAR_LOG_EPS = 1e-30


def stack_gamma_rot():
    if not os.path.exists(INPUT_CSV):
        print(f"[error] missing input: {INPUT_CSV}", flush=True)
        sys.exit(1)

    df = pd.read_csv(INPUT_CSV)
    for col in ("re_dz", "im_dz", "re_gamma", "im_gamma"):
        if col not in df.columns:
            raise RuntimeError(f"input CSV missing column: {col}")

    n_input = len(df)
    print(f"[stack] loaded {n_input} pairs from {INPUT_CSV}", flush=True)

    dz = (df["re_dz"].to_numpy() + 1j * df["im_dz"].to_numpy()).astype(np.complex128)
    gamma = (df["re_gamma"].to_numpy() + 1j * df["im_gamma"].to_numpy()).astype(np.complex128)

    r = np.abs(dz)
    phi = np.angle(dz)
    gamma_rot = gamma * np.exp(-2j * phi)

    print(f"[stack] r range: [{r.min():.6f}, {r.max():.6f}] deg = [{r.min()*60:.3f}, {r.max()*60:.3f}] arcmin", flush=True)

    edges = np.logspace(np.log10(R_MIN_DEG), np.log10(R_MAX_DEG), N_BINS + 1)
    bin_idx = np.searchsorted(edges, r, side="right") - 1
    valid_mask = (bin_idx >= 0) & (bin_idx < N_BINS)

    r_centers_all = []
    gamma_rot_means_all = []
    n_per_bin_all = []
    kept_indices = []
    for k in range(N_BINS):
        in_bin = valid_mask & (bin_idx == k)
        n_k = int(in_bin.sum())
        center_k = float(np.sqrt(edges[k] * edges[k + 1]))
        r_centers_all.append(center_k)
        n_per_bin_all.append(n_k)
        if n_k >= MIN_PER_BIN:
            mean_k = complex(np.mean(gamma_rot[in_bin]))
            gamma_rot_means_all.append(mean_k)
            kept_indices.append(k)
        else:
            gamma_rot_means_all.append(None)

    r_kept = np.array([r_centers_all[k] for k in kept_indices], dtype=np.float64)
    gamma_rot_kept = np.array([gamma_rot_means_all[k] for k in kept_indices], dtype=np.complex128)
    n_kept = np.array([n_per_bin_all[k] for k in kept_indices], dtype=np.int64)

    n_bins_kept = len(kept_indices)
    n_pairs_used = int(n_kept.sum())
    n_pairs_outside_range = int(n_input - int(valid_mask.sum()))

    print(f"[stack] kept {n_bins_kept}/{N_BINS} bins", flush=True)
    print(f"[stack] n_pairs_used: {n_pairs_used} (out of {n_input}; {n_pairs_outside_range} outside r range)", flush=True)

    if n_bins_kept < 3:
        raise RuntimeError(f"Too few bins kept ({n_bins_kept}); check data range.")

    out = pd.DataFrame({
        "r_arcmin": r_kept * 60.0,
        "n_per_bin": n_kept,
        "re_gamma_rot": gamma_rot_kept.real,
        "im_gamma_rot": gamma_rot_kept.imag,
    })
    os.makedirs("data", exist_ok=True)
    out.to_csv(OUTPUT_CSV, index=False)
    print(f"[stack] wrote {n_bins_kept} bins to {OUTPUT_CSV}", flush=True)

    stats = {
        "n_pairs_input": int(n_input),
        "n_pairs_used": int(n_pairs_used),
        "n_pairs_outside_r_range": int(n_pairs_outside_range),
        "n_bins_defined": int(N_BINS),
        "n_bins_kept": int(n_bins_kept),
        "min_per_bin_threshold": int(MIN_PER_BIN),
        "r_min_deg": float(R_MIN_DEG),
        "r_max_deg": float(R_MAX_DEG),
        "r_min_arcmin": float(R_MIN_ARCMIN),
        "r_max_arcmin": float(R_MAX_ARCMIN),
        "bin_centers_arcmin": [float(c * 60.0) for c in r_kept],
        "n_per_bin_kept": [int(n) for n in n_kept],
    }
    return r_kept, gamma_rot_kept, n_kept, stats


def state_writer(output_dir, output_path, stop_event, interval_sec):
    while not stop_event.is_set():
        try:
            if os.path.isdir(output_dir):
                candidates = [
                    os.path.join(output_dir, name)
                    for name in os.listdir(output_dir)
                    if name.startswith("hall_of_fame") and name.endswith(".csv")
                ]
                if candidates:
                    latest = max(candidates, key=os.path.getmtime)
                    df = pd.read_csv(latest)
                    if len(df) > 0:
                        cx_col = "Complexity" if "Complexity" in df.columns else "complexity"
                        loss_col = "Loss" if "Loss" in df.columns else "loss"
                        eq_col = "Equation" if "Equation" in df.columns else "equation"
                        partial = {
                            "status": "running",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "source_csv": latest,
                            "pareto_front": [
                                {
                                    "complexity": int(row[cx_col]),
                                    "loss": float(row[loss_col]),
                                    "equation": str(row[eq_col]),
                                }
                                for _, row in df.iterrows()
                            ],
                        }
                        tmp_path = output_path + ".tmp"
                        with open(tmp_path, "w") as f:
                            json.dump(partial, f, indent=2)
                        os.replace(tmp_path, output_path)
        except Exception as e:
            print(f"[state-writer] non-fatal: {e}", flush=True)
        stop_event.wait(interval_sec)


def main():
    random.seed(PYTHON_RANDOM_SEED)
    np.random.seed(NUMPY_SEED)

    r_arr, gamma_rot_arr, n_per_bin, stack_stats = stack_gamma_rot()

    from pysr import PySRRegressor
    import sympy

    eml_def = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
    emlstar_def = "emlstar(x, y) = exp(conj(x)) - log(conj(y) + (1e-30 + 0im))"
    my_conj = "my_conj(z) = conj(z)"
    my_real = "my_real(z) = complex(real(z))"
    my_imag = "my_imag(z) = complex(imag(z))"
    my_abs2 = "my_abs2(z) = z * conj(z)"

    binary_ops = ["+", "-", "*", "/", eml_def, emlstar_def]
    unary_ops = ["cos", "sin", "exp", "log", my_conj, my_real, my_imag, my_abs2]

    extra_sympy_mappings = {
        "eml": lambda x, y: sympy.exp(x) - sympy.log(y),
        "emlstar": lambda x, y: sympy.exp(sympy.conjugate(x)) - sympy.log(sympy.conjugate(y)),
        "my_conj": lambda z: sympy.conjugate(z),
        "my_real": lambda z: sympy.re(z),
        "my_imag": lambda z: sympy.im(z),
        "my_abs2": lambda z: z * sympy.conjugate(z),
    }

    X = (r_arr + 0j).reshape(-1, 1).astype(np.complex128)
    y_target = gamma_rot_arr.astype(np.complex128)

    assert X.shape == (len(r_arr), 1), f"X.shape must be (N, 1), got {X.shape}"
    assert X.dtype == np.complex128, f"unexpected X.dtype={X.dtype}"
    assert np.all(X.imag == 0), "X must be purely real (im=0); anti-circularity violated"
    assert y_target.dtype == np.complex128, f"unexpected y.dtype={y_target.dtype}"

    print(f"[pysr] X.shape={X.shape} X.dtype={X.dtype} y.dtype={y_target.dtype}", flush=True)
    print(f"[pysr] x0 <-> r (radial distance, deg, real, im=0)", flush=True)
    print(f"[pysr] anti-circularity: dz and phi NOT passed to PySR", flush=True)
    print(f"[pysr] seeds: numpy={NUMPY_SEED} python_random={PYTHON_RANDOM_SEED} pysr_random_state={PYSR_RANDOM_STATE}", flush=True)

    model = PySRRegressor(
        niterations=PYSR_NITERATIONS,
        population_size=PYSR_POPULATION_SIZE,
        binary_operators=binary_ops,
        unary_operators=unary_ops,
        extra_sympy_mappings=extra_sympy_mappings,
        maxsize=PYSR_MAXSIZE,
        parsimony=PYSR_PARSIMONY,
        parallelism="multithreading",
        deterministic=False,
        random_state=PYSR_RANDOM_STATE,
        precision=64,
        output_directory=OUTPUT_DIR,
        progress=True,
        verbosity=1,
    )

    stop_event = threading.Event()
    writer = threading.Thread(
        target=state_writer,
        args=(OUTPUT_DIR, JSON_OUT, stop_event, STATE_WRITE_INTERVAL_SEC),
        daemon=True,
    )
    writer.start()

    try:
        model.fit(X, y_target)
    finally:
        stop_event.set()
        writer.join(timeout=5)

    eqs = model.equations_
    if eqs is None or len(eqs) == 0:
        raise RuntimeError("PySR returned no equations")

    loss_col = "loss" if "loss" in eqs.columns else "Loss"
    eq_col = "equation" if "equation" in eqs.columns else "Equation"
    cx_col = "complexity" if "complexity" in eqs.columns else "Complexity"

    pareto = [
        {
            "complexity": int(row[cx_col]),
            "loss": float(row[loss_col]),
            "equation": str(row[eq_col]),
        }
        for _, row in eqs.iterrows()
    ]

    best_row = eqs.loc[eqs[loss_col].idxmin()]
    best_equation = str(best_row[eq_col])
    best_loss = float(best_row[loss_col])
    best_complexity = int(best_row[cx_col])

    anti_holo_tokens = ["emlstar", "my_conj", "conj"]
    anti_holomorphic_detected = any(t in best_equation for t in anti_holo_tokens)

    non_holo_operators = ["emlstar", "my_conj", "my_imag", "my_abs2"]
    best_equation_holomorphic_only = not any(t in best_equation for t in non_holo_operators)

    print(f"[result] best_equation: {best_equation}", flush=True)
    print(f"[result] best_loss: {best_loss:.6e}", flush=True)
    print(f"[result] best_complexity: {best_complexity}", flush=True)
    print(f"[result] anti_holomorphic_detected: {anti_holomorphic_detected}", flush=True)
    print(f"[result] best_equation_holomorphic_only: {best_equation_holomorphic_only}", flush=True)

    result = {
        "status": "complete",
        "test_name": "lensing_C",
        "best_equation": best_equation,
        "best_mse": best_loss,
        "complexity": best_complexity,
        "anti_holomorphic_detected": bool(anti_holomorphic_detected),
        "best_equation_holomorphic_only": bool(best_equation_holomorphic_only),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "seeds_used": {
            "numpy": int(NUMPY_SEED),
            "python_random": int(PYTHON_RANDOM_SEED),
            "pysr_random_state": int(PYSR_RANDOM_STATE),
        },
        "full_pareto_front": pareto,
        "feature_mapping": {"x0": "r_deg (real, im=0)"},
        "stacking_stats": stack_stats,
        "input_csv": INPUT_CSV,
        "output_csv": OUTPUT_CSV,
        "output_dir": OUTPUT_DIR,
        "toolbox": {
            "binary_operators": list(binary_ops),
            "unary_operators": list(unary_ops),
        },
        "emlstar_eps": float(EMLSTAR_LOG_EPS),
        "rotation_definition": "gamma_rot = gamma * exp(-2j * phi), phi = angle(dz). exp(-2i*phi) = (conj(dz)/|dz|)^2 contains conjugation; therefore phi is NOT passed to PySR.",
        "anti_circularity_note": "Only r = |dz| (real, im=0) is given to PySR as x0. dz and phi are never passed.",
        "notes": "Small dataset (~20 bins). Inspect full Pareto front, not just best equation. Real signal = low-complexity formula with low loss. Pure interpolation = only high-complexity formulas reach low loss.",
    }

    tmp_path = JSON_OUT + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(result, f, indent=2)
    os.replace(tmp_path, JSON_OUT)
    print(f"[result] wrote {JSON_OUT}", flush=True)


if __name__ == "__main__":
    main()
