#!/usr/bin/env python3
"""
test_lensing_A.py — Lensing pipeline validation with PySR multi-feature
complex inputs on real KiDS-1000 DEIMOS shape catalog.

Run instruction (real-time monitoring with unbuffered stdout):
  python3 -u test_lensing_A.py 2>&1 | tee lensing_test_A_log.txt
"""

import json
import math
import os
import random
import sys
import threading
from datetime import datetime, timezone

import numpy as np
import pandas as pd

import astropy.units as u
from astropy.coordinates import SkyCoord, search_around_sky
from astropy.io import fits

SOURCE_FITS = os.path.join("data", "DEIMOS_GAMA_rband_shape_catalogue_size_0.5.fits")
LENS_CSV = os.path.join("data", "lens_catalog.csv")

OUTPUT_CSV = os.path.join("data", "lensing_test_A.csv")
OUTPUT_DIR = "pysr_output_lensing_A"
JSON_OUT = "lensing_test_A_result.json"

ANGULAR_MATCH_ARCMIN = 10.0
N_PAIRS = 5000

NUMPY_SEED = 42
PYTHON_RANDOM_SEED = 42
PYSR_RANDOM_STATE = 42

PYSR_NITERATIONS = 100
PYSR_POPULATION_SIZE = 300
PYSR_MAXSIZE = 20
PYSR_PARSIMONY = 0.001

STATE_WRITE_INTERVAL_SEC = 30
EMLSTAR_LOG_EPS = 1e-30


def build_pairs():
    if not os.path.exists(SOURCE_FITS):
        print(f"[error] missing source catalog: {SOURCE_FITS}", flush=True)
        sys.exit(1)
    if not os.path.exists(LENS_CSV):
        print(f"[error] missing lens catalog: {LENS_CSV}", flush=True)
        sys.exit(1)

    lens_df = pd.read_csv(LENS_CSV)
    for required in ("RAJ2000", "DECJ2000"):
        if required not in lens_df.columns:
            raise RuntimeError(f"lens catalog missing column: {required}")
    lens_ra = lens_df["RAJ2000"].to_numpy()
    lens_dec = lens_df["DECJ2000"].to_numpy()
    n_lens = len(lens_df)
    print(f"[pairs] loaded {n_lens} lenses from {LENS_CSV}", flush=True)

    with fits.open(SOURCE_FITS) as hdul:
        sdata = hdul[1].data
        for required in ("RA_GAMA", "DEC_GAMA", "e1", "e2"):
            if required not in sdata.columns.names:
                raise RuntimeError(f"source catalog missing column: {required}")
        source_ra = np.array(sdata["RA_GAMA"], dtype=np.float64)
        source_dec = np.array(sdata["DEC_GAMA"], dtype=np.float64)
        source_e1 = np.array(sdata["e1"], dtype=np.float64)
        source_e2 = np.array(sdata["e2"], dtype=np.float64)
    n_source = len(source_ra)
    print(f"[pairs] loaded {n_source} sources from {SOURCE_FITS}", flush=True)

    lens_sc = SkyCoord(ra=lens_ra * u.deg, dec=lens_dec * u.deg, frame="icrs")
    source_sc = SkyCoord(ra=source_ra * u.deg, dec=source_dec * u.deg, frame="icrs")
    radius = ANGULAR_MATCH_ARCMIN * u.arcmin
    idx_lens, idx_source, sep, _ = search_around_sky(lens_sc, source_sc, radius)
    sep_arcmin = sep.to(u.arcmin).value
    n_pairs_total = len(idx_lens)
    print(f"[pairs] {n_pairs_total} pairs within {ANGULAR_MATCH_ARCMIN} arcmin", flush=True)

    if n_pairs_total == 0:
        raise RuntimeError("no pairs found within match radius")

    pairs = pd.DataFrame({
        "lens_idx": idx_lens.astype(np.int64),
        "source_idx": idx_source.astype(np.int64),
        "ra_lens": lens_ra[idx_lens],
        "dec_lens": lens_dec[idx_lens],
        "ra_source": source_ra[idx_source],
        "dec_source": source_dec[idx_source],
        "sep_arcmin": sep_arcmin,
        "e1": source_e1[idx_source],
        "e2": source_e2[idx_source],
    })
    return pairs, n_lens, n_source


def stratified_sample(pairs, n_target, seed):
    rng = np.random.default_rng(seed)
    by_lens = pairs.groupby("lens_idx")
    n_active = by_lens.ngroups
    quota = math.ceil(n_target / n_active)
    print(f"[pairs] stratified: n_active={n_active} quota={quota}", flush=True)

    parts = []
    for _, group in by_lens:
        m = len(group)
        if m <= quota:
            parts.append(group)
        else:
            picks = rng.choice(m, size=quota, replace=False)
            parts.append(group.iloc[picks])
    pooled = pd.concat(parts, ignore_index=True)
    pooled = pooled.sample(frac=1.0, random_state=seed).reset_index(drop=True)

    if len(pooled) > n_target:
        pooled = pooled.iloc[:n_target].reset_index(drop=True)
    return pooled


def generate_data():
    pairs, n_lens, n_source = build_pairs()
    sampled = stratified_sample(pairs, N_PAIRS, NUMPY_SEED)
    n_sampled = len(sampled)
    print(f"[pairs] sampled {n_sampled} pairs", flush=True)

    re_dz = (sampled["ra_source"] - sampled["ra_lens"]).to_numpy()
    im_dz = (sampled["dec_source"] - sampled["dec_lens"]).to_numpy()
    dz = (re_dz + 1j * im_dz).astype(np.complex128)

    gamma = (sampled["e1"].to_numpy() + 1j * sampled["e2"].to_numpy()).astype(np.complex128)

    target_real = (sampled["e1"].to_numpy() ** 2 + sampled["e2"].to_numpy() ** 2)
    target = (target_real + 0j).astype(np.complex128)

    out_df = pd.DataFrame({
        "re_dz": dz.real,
        "im_dz": dz.imag,
        "re_gamma": gamma.real,
        "im_gamma": gamma.imag,
        "re_target": target.real,
        "im_target": target.imag,
    })
    os.makedirs("data", exist_ok=True)
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"[data] wrote {n_sampled} rows to {OUTPUT_CSV}", flush=True)

    return dz, gamma, target, {
        "n_lens_total": int(n_lens),
        "n_source_total": int(n_source),
        "n_pairs_total": int(len(pairs)),
        "n_pairs_sampled": int(n_sampled),
        "angular_match_arcmin": float(ANGULAR_MATCH_ARCMIN),
    }


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

    dz, gamma, target, dataset_stats = generate_data()

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

    X = np.column_stack([dz, gamma]).astype(np.complex128)
    y_target = target.astype(np.complex128)

    assert X.shape == (len(dz), 2), f"unexpected X.shape={X.shape}"
    assert X.dtype == np.complex128, f"unexpected X.dtype={X.dtype}"
    assert y_target.dtype == np.complex128, f"unexpected y.dtype={y_target.dtype}"

    print(f"[pysr] X.shape={X.shape} X.dtype={X.dtype} y.dtype={y_target.dtype}", flush=True)
    print(f"[pysr] x0 <-> dz (lens-source angular separation, deg)", flush=True)
    print(f"[pysr] x1 <-> gamma (source ellipticity e1+ie2)", flush=True)
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

    x0_used = "x0" in best_equation
    x1_used = "x1" in best_equation
    if x1_used and not x0_used:
        specificity = "OK"
    elif x0_used and x1_used:
        specificity = "AMBIGUOUS"
    else:
        specificity = "FAIL"

    print(f"[result] best_equation: {best_equation}", flush=True)
    print(f"[result] best_loss: {best_loss:.6e}", flush=True)
    print(f"[result] best_complexity: {best_complexity}", flush=True)
    print(f"[result] x0_used={x0_used} x1_used={x1_used}", flush=True)
    print(f"[result] specificity_check: {specificity}", flush=True)

    result = {
        "status": "complete",
        "test_name": "lensing_A",
        "best_equation": best_equation,
        "best_mse": best_loss,
        "complexity": best_complexity,
        "x0_used_in_best": bool(x0_used),
        "x1_used_in_best": bool(x1_used),
        "specificity_check": specificity,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "seeds_used": {
            "numpy": int(NUMPY_SEED),
            "python_random": int(PYTHON_RANDOM_SEED),
            "pysr_random_state": int(PYSR_RANDOM_STATE),
        },
        "full_pareto_front": pareto,
        "feature_mapping": {"x0": "dz_deg", "x1": "gamma"},
        "dataset_stats": dataset_stats,
        "source_fits": SOURCE_FITS,
        "lens_csv": LENS_CSV,
        "output_csv": OUTPUT_CSV,
        "output_dir": OUTPUT_DIR,
        "toolbox": {
            "binary_operators": list(binary_ops),
            "unary_operators": list(unary_ops),
        },
        "emlstar_eps": float(EMLSTAR_LOG_EPS),
        "angular_separation_method": "astropy.coordinates.search_around_sky, ICRS frame, great-circle distance",
        "notes": "deterministic=False + parallelism=multithreading; seeds logged for traceability only.",
    }

    tmp_path = JSON_OUT + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(result, f, indent=2)
    os.replace(tmp_path, JSON_OUT)
    print(f"[result] wrote {JSON_OUT}", flush=True)


if __name__ == "__main__":
    main()
