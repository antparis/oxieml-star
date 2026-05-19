#!/usr/bin/env python3
"""
test_lensing_C_kids1000.py — KiDS-1000 SOM-gold lensing stacking with PySR.

Run instruction (real-time monitoring with unbuffered stdout):
  python3 -u test_lensing_C_kids1000.py 2>&1 | tee lensing_test_C_kids1000_log.txt
"""

import gc
import json
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

SOURCE_FITS = os.path.join("data", "KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits")
LENS_CSV = os.path.join("data", "lens_catalog.csv")

OUTPUT_CSV = os.path.join("data", "lensing_test_C_kids1000_stacked.csv")
OUTPUT_DIR = "pysr_output_lensing_C_kids1000"
JSON_OUT = "lensing_test_C_kids1000_result.json"

Z_B_MIN = 0.3
ANGULAR_MATCH_ARCMIN = 10.0
R_MIN_ARCMIN = 0.5
R_MAX_ARCMIN = 10.0
R_MIN_DEG = R_MIN_ARCMIN / 60.0
R_MAX_DEG = R_MAX_ARCMIN / 60.0
N_BINS = 20
N_EFF_MIN = 100.0

NUMPY_SEED = 42
PYTHON_RANDOM_SEED = 42
PYSR_RANDOM_STATE = 42

PYSR_NITERATIONS = 200
PYSR_POPULATION_SIZE = 300
PYSR_MAXSIZE = 20
PYSR_PARSIMONY = 0.001

STATE_WRITE_INTERVAL_SEC = 30
EMLSTAR_LOG_EPS = 1e-30
SOURCE_COLS = ["RAJ2000", "DECJ2000", "e1", "e2", "weight", "Z_B", "fitclass", "MASK"]


def load_lenses():
    if not os.path.exists(LENS_CSV):
        print(f"[error] missing lens catalog: {LENS_CSV}", flush=True)
        sys.exit(1)
    df = pd.read_csv(LENS_CSV)
    for required in ("RAJ2000", "DECJ2000"):
        if required not in df.columns:
            raise RuntimeError(f"lens catalog missing column: {required}")
    ra = np.asarray(df["RAJ2000"].to_numpy(), dtype=np.float64)
    dec = np.asarray(df["DECJ2000"].to_numpy(), dtype=np.float64)
    print(f"[lenses] loaded {len(df)} lenses from {LENS_CSV}", flush=True)
    return ra, dec


def load_sources_filtered():
    if not os.path.exists(SOURCE_FITS):
        print(f"[error] missing source FITS: {SOURCE_FITS}", flush=True)
        sys.exit(1)

    hdul = fits.open(SOURCE_FITS, memmap=True)
    try:
        data = hdul[1].data
        for required in SOURCE_COLS:
            if required not in data.columns.names:
                raise RuntimeError(f"source catalog missing column: {required}")

        ra = np.asarray(data["RAJ2000"], dtype=np.float64)
        dec = np.asarray(data["DECJ2000"], dtype=np.float64)
        e1 = np.asarray(data["e1"], dtype=np.float64)
        e2 = np.asarray(data["e2"], dtype=np.float64)
        weight = np.asarray(data["weight"], dtype=np.float64)
        zb = np.asarray(data["Z_B"], dtype=np.float64)
        fitclass = np.asarray(data["fitclass"], dtype=np.int64)
        mask = np.asarray(data["MASK"], dtype=np.int64)
    finally:
        hdul.close()
        del hdul
    gc.collect()

    n_total = int(ra.size)
    print(f"[sources] loaded {n_total} rows from {SOURCE_FITS}", flush=True)

    counts = {"n_total": n_total}

    keep = (fitclass == 0)
    counts["after_fitclass_eq_0"] = int(keep.sum())
    print(f"[filter] fitclass == 0: {counts['after_fitclass_eq_0']}", flush=True)

    keep &= (mask == 0)
    counts["after_mask_eq_0"] = int(keep.sum())
    print(f"[filter] MASK == 0: {counts['after_mask_eq_0']}", flush=True)

    keep &= (weight > 0)
    counts["after_weight_gt_0"] = int(keep.sum())
    print(f"[filter] weight > 0: {counts['after_weight_gt_0']}", flush=True)

    keep &= (zb > Z_B_MIN)
    counts["after_zb_gt_0p3"] = int(keep.sum())
    print(f"[filter] Z_B > {Z_B_MIN}: {counts['after_zb_gt_0p3']}", flush=True)

    ra = ra[keep]
    dec = dec[keep]
    e1 = e1[keep]
    e2 = e2[keep]
    weight = weight[keep]
    del zb, fitclass, mask, keep
    gc.collect()

    return ra, dec, e1, e2, weight, counts


def match_and_stack(lens_ra, lens_dec, src_ra, src_dec, src_e1, src_e2, src_weight):
    lens_sc = SkyCoord(ra=lens_ra * u.deg, dec=lens_dec * u.deg, frame="icrs")
    src_sc = SkyCoord(ra=src_ra * u.deg, dec=src_dec * u.deg, frame="icrs")
    radius = ANGULAR_MATCH_ARCMIN * u.arcmin
    print(f"[match] running search_around_sky, radius={ANGULAR_MATCH_ARCMIN} arcmin", flush=True)
    idx_lens, idx_src, sep, _ = search_around_sky(lens_sc, src_sc, radius)
    n_pairs_total = int(idx_lens.size)
    print(f"[match] total pairs within radius: {n_pairs_total}", flush=True)

    if n_pairs_total == 0:
        raise RuntimeError("no (lens, source) pairs within match radius")

    n_lens_with_sources = int(np.unique(idx_lens).size)
    print(f"[match] lenses with >=1 source: {n_lens_with_sources}/{lens_ra.size}", flush=True)

    dra = src_ra[idx_src] - lens_ra[idx_lens]
    ddec = src_dec[idx_src] - lens_dec[idx_lens]
    dz = (dra + 1j * ddec).astype(np.complex128)
    r = np.abs(dz)
    phi = np.angle(dz)
    gamma = (src_e1[idx_src] + 1j * src_e2[idx_src]).astype(np.complex128)
    gamma_rot = gamma * np.exp(-2j * phi)
    w = src_weight[idx_src]

    edges = np.logspace(np.log10(R_MIN_DEG), np.log10(R_MAX_DEG), N_BINS + 1)
    bin_idx = np.searchsorted(edges, r, side="right") - 1
    valid_mask = (bin_idx >= 0) & (bin_idx < N_BINS)
    n_pairs_in_range = int(valid_mask.sum())
    print(f"[match] pairs inside log-r range [{R_MIN_DEG:.6f}, {R_MAX_DEG:.6f}] deg: {n_pairs_in_range}", flush=True)

    r_centers_all = np.array([float(np.sqrt(edges[k] * edges[k + 1])) for k in range(N_BINS)], dtype=np.float64)

    n_per_bin = np.zeros(N_BINS, dtype=np.int64)
    sum_w = np.zeros(N_BINS, dtype=np.float64)
    n_eff = np.zeros(N_BINS, dtype=np.float64)
    means = np.zeros(N_BINS, dtype=np.complex128)
    have_data = np.zeros(N_BINS, dtype=bool)

    for k in range(N_BINS):
        in_bin = valid_mask & (bin_idx == k)
        n_k = int(in_bin.sum())
        n_per_bin[k] = n_k
        if n_k == 0:
            continue
        wk = w[in_bin]
        gk = gamma_rot[in_bin]
        sw = float(wk.sum())
        sw2 = float((wk * wk).sum())
        if sw <= 0.0 or sw2 <= 0.0:
            continue
        sum_w[k] = sw
        n_eff[k] = (sw * sw) / sw2
        means[k] = complex(np.sum(wk * gk) / sw)
        have_data[k] = True

    keep_bin = have_data & (n_eff >= N_EFF_MIN)
    n_bins_kept = int(keep_bin.sum())
    print(f"[stack] bins kept (N_eff >= {N_EFF_MIN}): {n_bins_kept}/{N_BINS}", flush=True)
    if n_bins_kept < 3:
        raise RuntimeError(f"Too few bins kept ({n_bins_kept}) for symbolic regression.")

    r_kept = r_centers_all[keep_bin]
    gamma_rot_kept = means[keep_bin]
    n_kept = n_per_bin[keep_bin]
    sum_w_kept = sum_w[keep_bin]
    n_eff_kept = n_eff[keep_bin]

    stats = {
        "n_pairs_total": int(n_pairs_total),
        "n_pairs_in_r_range": int(n_pairs_in_range),
        "n_lens_with_sources": int(n_lens_with_sources),
        "n_bins_defined": int(N_BINS),
        "n_bins_kept": int(n_bins_kept),
        "n_eff_threshold": float(N_EFF_MIN),
        "r_min_deg": float(R_MIN_DEG),
        "r_max_deg": float(R_MAX_DEG),
        "r_min_arcmin": float(R_MIN_ARCMIN),
        "r_max_arcmin": float(R_MAX_ARCMIN),
        "bin_centers_arcmin_all": [float(c * 60.0) for c in r_centers_all],
        "n_per_bin_all": [int(n) for n in n_per_bin],
        "n_eff_all": [float(x) for x in n_eff],
        "sum_w_all": [float(x) for x in sum_w],
        "kept_mask": [bool(x) for x in keep_bin],
    }

    out_df = pd.DataFrame({
        "r_arcmin": r_kept * 60.0,
        "n_per_bin": n_kept,
        "n_eff": n_eff_kept,
        "sum_w": sum_w_kept,
        "re_gamma_rot": gamma_rot_kept.real,
        "im_gamma_rot": gamma_rot_kept.imag,
    })
    os.makedirs("data", exist_ok=True)
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"[stack] wrote {n_bins_kept} bins to {OUTPUT_CSV}", flush=True)

    return r_kept, gamma_rot_kept, n_kept, sum_w_kept, n_eff_kept, stats


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
                                {"complexity": int(row[cx_col]), "loss": float(row[loss_col]), "equation": str(row[eq_col])}
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

    lens_ra, lens_dec = load_lenses()
    src_ra, src_dec, src_e1, src_e2, src_weight, filter_counts = load_sources_filtered()

    print(f"[ok] retained {src_ra.size} sources after filters", flush=True)

    r_arr, gamma_rot_arr, n_per_bin, sum_w, n_eff, stack_stats = match_and_stack(
        lens_ra, lens_dec, src_ra, src_dec, src_e1, src_e2, src_weight)

    del src_ra, src_dec, src_e1, src_e2, src_weight
    gc.collect()

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
        {"complexity": int(row[cx_col]), "loss": float(row[loss_col]), "equation": str(row[eq_col])}
        for _, row in eqs.iterrows()
    ]

    best_row = eqs.loc[eqs[loss_col].idxmin()]
    best_equation = str(best_row[eq_col])
    best_loss = float(best_row[loss_col])
    best_complexity = int(best_row[cx_col])

    low_cx = eqs[eqs[cx_col] <= 7].sort_values(loss_col).head(3)
    low_complexity_candidates = [
        {"complexity": int(row[cx_col]), "loss": float(row[loss_col]), "equation": str(row[eq_col])}
        for _, row in low_cx.iterrows()
    ]

    anti_holo_tokens = ["emlstar", "my_conj", "conj"]
    anti_holomorphic_detected = any(t in best_equation for t in anti_holo_tokens)
    non_holo_operators = ["emlstar", "my_conj", "my_imag", "my_abs2"]
    best_equation_holomorphic_only = not any(t in best_equation for t in non_holo_operators)

    print(f"[result] best_equation: {best_equation}", flush=True)
    print(f"[result] best_loss: {best_loss:.6e}", flush=True)
    print(f"[result] best_complexity: {best_complexity}", flush=True)
    print(f"[result] anti_holomorphic_detected: {anti_holomorphic_detected}", flush=True)
    print(f"[result] best_equation_holomorphic_only: {best_equation_holomorphic_only}", flush=True)

    stacking_stats = dict(stack_stats)
    stacking_stats["filter_counts"] = filter_counts

    result = {
        "status": "complete",
        "test_name": "lensing_C_kids1000",
        "best_equation": best_equation,
        "best_mse": best_loss,
        "complexity": best_complexity,
        "anti_holomorphic_detected": bool(anti_holomorphic_detected),
        "best_equation_holomorphic_only": bool(best_equation_holomorphic_only),
        "low_complexity_candidates": low_complexity_candidates,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "seeds_used": {
            "numpy": int(NUMPY_SEED),
            "python_random": int(PYTHON_RANDOM_SEED),
            "pysr_random_state": int(PYSR_RANDOM_STATE),
        },
        "full_pareto_front": pareto,
        "feature_mapping": {"x0": "r_deg (real, im=0)"},
        "stacking_stats": stacking_stats,
        "source_fits": SOURCE_FITS,
        "lens_csv": LENS_CSV,
        "output_csv": OUTPUT_CSV,
        "output_dir": OUTPUT_DIR,
        "source_selection": {
            "filter_order": ["fitclass == 0", "MASK == 0", "weight > 0", f"Z_B > {Z_B_MIN}"],
            "z_b_min": float(Z_B_MIN),
        },
        "angular_match_arcmin": float(ANGULAR_MATCH_ARCMIN),
        "angular_separation_method": "astropy.coordinates.search_around_sky, ICRS frame, great-circle distance",
        "toolbox": {
            "binary_operators": list(binary_ops),
            "unary_operators": list(unary_ops),
        },
        "emlstar_eps": float(EMLSTAR_LOG_EPS),
        "rotation_definition": "gamma_rot = gamma * exp(-2j * phi), phi = angle(dz). exp(-2i*phi) = (conj(dz)/|dz|)^2 contains conjugation; therefore phi is NOT passed to PySR.",
        "stacking_weighting": "Lensfit-weighted mean: <gamma_rot>_bin = sum(w * gamma_rot) / sum(w). N_eff = (sum w)^2 / sum(w^2). Bins with N_eff < 100 dropped.",
        "anti_circularity_note": "Only r = |dz| (real, im=0) is given to PySR as x0. dz and phi are never passed.",
        "notes": "deterministic=False + parallelism=multithreading; seeds logged for traceability only. Inspect full Pareto front and low_complexity_candidates before any scientific claim.",
    }

    tmp_path = JSON_OUT + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(result, f, indent=2)
    os.replace(tmp_path, JSON_OUT)
    print(f"[result] wrote {JSON_OUT}", flush=True)


if __name__ == "__main__":
    main()
