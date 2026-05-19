#!/usr/bin/env python3
"""
eml_star_decomposition.py — Run A v2

Test whether PySR can reconstruct emlstar(z, w) symbolically using only
elementary operators, with z AND w as free complex inputs.

Two phases:
  Phase 1 (strict):     toolbox excludes my_conj, eml, emlstar.
  Phase 2 (conj-aided): toolbox includes my_conj; eml, emlstar still excluded.

Run instructions (real-time monitoring with unbuffered stdout):

  python3 -u eml_star_decomposition.py --phase 1 2>&1 | tee eml_star_decomp_log_phase1.txt
  python3 -u eml_star_decomposition.py --phase 2 2>&1 | tee eml_star_decomp_log_phase2.txt

Phase 2 must be launched manually after Phase 1 completes.
"""

import argparse
import json
import os
import random
import sys
import threading
from datetime import datetime, timezone

import numpy as np
import pandas as pd

N_SAMPLES = 2000
DOMAIN_HALF_WIDTH = np.pi - 0.05
W_MIN_MODULUS = 0.1

NUMPY_SEED = 42
PYTHON_RANDOM_SEED = 42
PYSR_RANDOM_STATE = 42

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "eml_star_target_zw.csv")

PYSR_NITERATIONS = 200
PYSR_POPULATION_SIZE = 500
PYSR_MAXSIZE = 30
PYSR_PARSIMONY = 0.001

STATE_WRITE_INTERVAL_SEC = 30

EMLSTAR_LOG_EPS = 1e-30


# Verbatim quote from pysr_stacking.py line 135:
#     emlstar(x, y) = exp(conj(x)) - log(conj(y) + (1e-30 + 0im))
def emlstar_eval(z, w):
    """emlstar(z, w) = exp(conj(z)) - log(conj(w) + 1e-30)."""
    return np.exp(np.conj(z)) - np.log(np.conj(w) + EMLSTAR_LOG_EPS)


def _sample_z(rng, n):
    re = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=n)
    im = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=n)
    return re + 1j * im


def _sample_w(rng, n):
    re = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=n)
    im = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=n)
    w = re + 1j * im
    bad = np.abs(w) < W_MIN_MODULUS
    while np.any(bad):
        k = int(bad.sum())
        re_new = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=k)
        im_new = rng.uniform(-DOMAIN_HALF_WIDTH, DOMAIN_HALF_WIDTH, size=k)
        w[bad] = re_new + 1j * im_new
        bad = np.abs(w) < W_MIN_MODULUS
    return w


def generate_data():
    rng = np.random.default_rng(NUMPY_SEED)
    z = _sample_z(rng, N_SAMPLES)
    w = _sample_w(rng, N_SAMPLES)

    assert np.all(np.abs(z.real) <= DOMAIN_HALF_WIDTH), "z Re guard violated"
    assert np.all(np.abs(z.imag) <= DOMAIN_HALF_WIDTH), "z Im guard violated"
    assert np.all(np.abs(w.real) <= DOMAIN_HALF_WIDTH), "w Re guard violated"
    assert np.all(np.abs(w.imag) <= DOMAIN_HALF_WIDTH), "w Im guard violated"
    assert np.all(np.abs(w) >= W_MIN_MODULUS), "w modulus guard violated"

    y = emlstar_eval(z, w)

    os.makedirs(DATA_DIR, exist_ok=True)
    df = pd.DataFrame({
        "re_z": z.real,
        "im_z": z.imag,
        "re_w": w.real,
        "im_w": w.imag,
        "re_y": y.real,
        "im_y": y.imag,
    })
    df.to_csv(DATA_FILE, index=False)
    print(f"[data] wrote {N_SAMPLES} samples to {DATA_FILE}", flush=True)
    return z, w, y


def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"[error] {DATA_FILE} missing. Run --phase 1 first.", flush=True)
        sys.exit(1)
    df = pd.read_csv(DATA_FILE)
    re_z = df["re_z"].to_numpy()
    im_z = df["im_z"].to_numpy()
    re_w = df["re_w"].to_numpy()
    im_w = df["im_w"].to_numpy()
    re_y = df["re_y"].to_numpy()
    im_y = df["im_y"].to_numpy()
    z = re_z + 1j * im_z
    w = re_w + 1j * im_w
    y = re_y + 1j * im_y

    assert np.all(np.abs(z.real) <= DOMAIN_HALF_WIDTH), "loaded z Re guard violated"
    assert np.all(np.abs(z.imag) <= DOMAIN_HALF_WIDTH), "loaded z Im guard violated"
    assert np.all(np.abs(w.real) <= DOMAIN_HALF_WIDTH), "loaded w Re guard violated"
    assert np.all(np.abs(w.imag) <= DOMAIN_HALF_WIDTH), "loaded w Im guard violated"
    assert np.all(np.abs(w) >= W_MIN_MODULUS), "loaded w modulus guard violated"

    print(f"[data] loaded {len(z)} samples from {DATA_FILE}", flush=True)
    return z, w, y


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
                        complexity_col = "Complexity" if "Complexity" in df.columns else "complexity"
                        loss_col = "Loss" if "Loss" in df.columns else "loss"
                        eq_col = "Equation" if "Equation" in df.columns else "equation"
                        partial = {
                            "status": "running",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "source_csv": latest,
                            "pareto_front": [
                                {
                                    "complexity": int(row[complexity_col]),
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


def run_phase(phase):
    assert phase in (1, 2)

    random.seed(PYTHON_RANDOM_SEED)
    np.random.seed(NUMPY_SEED)

    if phase == 1:
        z, w, y = generate_data()
    else:
        z, w, y = load_data()

    from pysr import PySRRegressor
    import sympy

    my_conj = "my_conj(z) = conj(z)"
    my_real = "my_real(z) = complex(real(z))"
    my_imag = "my_imag(z) = complex(imag(z))"

    unary_ops = ["sin", "cos", "exp", "log", my_real, my_imag]
    if phase == 2:
        unary_ops.append(my_conj)

    binary_ops = ["+", "-", "*", "/"]

    extra_sympy_mappings = {
        "my_real": lambda x: sympy.re(x),
        "my_imag": lambda x: sympy.im(x),
    }
    if phase == 2:
        extra_sympy_mappings["my_conj"] = lambda x: sympy.conjugate(x)

    output_dir = f"pysr_output_phase{phase}"
    json_out = f"eml_star_decomp_result_phase{phase}.json"

    X = np.column_stack([z, w]).astype(np.complex128)
    y_target = y.astype(np.complex128)

    assert X.shape == (len(z), 2), f"unexpected X.shape={X.shape}"
    assert X.dtype == np.complex128, f"unexpected X.dtype={X.dtype}"
    assert y_target.dtype == np.complex128, f"unexpected y.dtype={y_target.dtype}"

    print(f"[pysr] phase={phase}", flush=True)
    print(f"[pysr] N={len(z)} X.shape={X.shape} X.dtype={X.dtype} y.dtype={y_target.dtype}", flush=True)
    print(f"[pysr] x0 <-> z, x1 <-> w", flush=True)
    print(f"[pysr] unary_operators={unary_ops}", flush=True)
    print(f"[pysr] binary_operators={binary_ops}", flush=True)
    print(f"[pysr] forbidden=eml, emlstar{', my_conj' if phase == 1 else ''}", flush=True)
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
        output_directory=output_dir,
        progress=True,
        verbosity=1,
    )

    stop_event = threading.Event()
    writer = threading.Thread(
        target=state_writer,
        args=(output_dir, json_out, stop_event, STATE_WRITE_INTERVAL_SEC),
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

    result = {
        "status": "complete",
        "phase": int(phase),
        "best_equation": str(best_row[eq_col]),
        "best_mse": float(best_row[loss_col]),
        "complexity": int(best_row[cx_col]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "seeds_used": {
            "numpy": int(NUMPY_SEED),
            "python_random": int(PYTHON_RANDOM_SEED),
            "pysr_random_state": int(PYSR_RANDOM_STATE),
        },
        "full_pareto_front": pareto,
        "n_samples": int(len(z)),
        "data_file": str(DATA_FILE),
        "output_dir": str(output_dir),
        "phase_toolbox": {
            "binary_operators": list(binary_ops),
            "unary_operators": list(unary_ops),
            "forbidden": ["eml", "emlstar"] + ([] if phase == 2 else ["my_conj"]),
        },
        "feature_mapping": {"x0": "z", "x1": "w"},
        "domain_guards": {
            "z_re_abs_max": float(DOMAIN_HALF_WIDTH),
            "z_im_abs_max": float(DOMAIN_HALF_WIDTH),
            "w_re_abs_max": float(DOMAIN_HALF_WIDTH),
            "w_im_abs_max": float(DOMAIN_HALF_WIDTH),
            "w_modulus_min": float(W_MIN_MODULUS),
        },
        "emlstar_eps": float(EMLSTAR_LOG_EPS),
        "notes": "deterministic=False + parallelism=multithreading; seeds logged for traceability only.",
    }

    tmp_path = json_out + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(result, f, indent=2)
    os.replace(tmp_path, json_out)

    print(f"[result] wrote {json_out}", flush=True)
    print(f"[result] best_equation: {result['best_equation']}", flush=True)
    print(f"[result] best_mse: {result['best_mse']}", flush=True)
    print(f"[result] complexity: {result['complexity']}", flush=True)

    if phase == 1:
        print("Phase 1 complete. Run with --phase 2 to launch Phase 2.", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="emlstar(z, w) symbolic decomposition (two-phase PySR run)"
    )
    parser.add_argument("--phase", type=int, required=True, choices=[1, 2],
                        help="Run phase: 1 (strict) or 2 (conj-aided)")
    args = parser.parse_args()
    run_phase(args.phase)


if __name__ == "__main__":
    main()
