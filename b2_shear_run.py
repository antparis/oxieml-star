#!/usr/bin/env python3
"""
b2_shear_run.py

B2 target -- planar harmonic mappings, Clunie--Sheil-Small shear.
STAGE 1 CALIBRATION: detect that the pipeline (PySR + exact judge) separates
the holomorphic part h from the anti-holomorphic part conj(g) of
        f = h + conj(g),
on a case whose closed form is KNOWN and injected on purpose.

This is a calibration, NOT a discovery. Its only job: confirm the detector
discriminates a genuinely non-holomorphic mapping (D1) from a purely
holomorphic control (D0). If D0 also comes out anti-holomorphic, or D1 comes
out holomorphic, the test FAILS (artefact, SPARC lesson).

Calibration case:  phi(z) = z,  omega(z) = z
    h(z) = -log(1 - z)
    g(z) = -z - log(1 - z)
    D1 (shear):  f = h(z) + conj(g(z))   -> ANTI-HOLOMORPHIC expected
    D0 (control): f = h(z)               -> HOLOMORPHIC      expected

Reuses, WITHOUT modification:
    pysr_stacking.build_operators   (exact eml/emlstar/my_conj operator set)
    pysr_stacking.PYSR_BASE         (exact complex PySR hyperparameters)
    verify_exact.certify            (the official exact judge -- the ARBITER)

One PySR round per process (Julia GC segfault workaround).

Workflow on the target machine:
    python3 b2_shear_run.py --gen           # write both CSVs (no PySR)
    python3 b2_shear_run.py --which holo    # PySR on D0, certify -> JSON
    python3 b2_shear_run.py --which shear   # PySR on D1, certify -> JSON
    python3 b2_shear_run.py --report        # read both JSONs, PASS/FAIL

Author: pipeline by Anthony Monnerot. Harness drafted under audit.
"""
import os
# Belt-and-suspenders: match the documented Julia GC workaround.
os.environ.setdefault("JULIA_NUM_GC_THREADS", "1")

import json
import argparse
import numpy as np
import pandas as pd

DATA_DIR = "data"
CSV_HOLO = os.path.join(DATA_DIR, "b2_holo_control.csv")
CSV_SHEAR = os.path.join(DATA_DIR, "b2_shear.csv")
JSON_HOLO = "b2_result_holo.json"
JSON_SHEAR = "b2_result_shear.json"

MSE_VALID_MAX = 1e-3   # project rule: MSE >= 1e-3 invalidates the claim


# ----------------------------------------------------------------------
# Closed-form ground truth (injected on purpose for calibration)
# ----------------------------------------------------------------------
def h(z):
    return -np.log(1.0 - z)


def g(z):
    return -z - np.log(1.0 - z)


def f_shear(z):                 # D1: genuine harmonic mapping h + conj(g)
    return h(z) + np.conj(g(z))


def f_holo(z):                  # D0: pure holomorphic control
    return h(z)


def sample_disk(n, r_max, seed):
    rng = np.random.default_rng(seed)
    rad = r_max * np.sqrt(rng.uniform(0.0, 1.0, size=n))   # area-uniform
    th = rng.uniform(0.0, 2.0 * np.pi, size=n)
    return rad * np.exp(1j * th)


def write_csv(path, z, fv):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as fh:
        fh.write("z_real,z_imag,f_real,f_imag\n")
        for zi, fi in zip(z, fv):
            fh.write(f"{zi.real:.16e},{zi.imag:.16e},"
                     f"{fi.real:.16e},{fi.imag:.16e}\n")


def gen(n, r_max, seed):
    z = sample_disk(n, r_max, seed)
    for vec in (z, f_shear(z), f_holo(z)):
        assert np.all(np.isfinite(vec)), "non-finite values generated"
    write_csv(CSV_SHEAR, z, f_shear(z))
    write_csv(CSV_HOLO, z, f_holo(z))
    print(f"[gen] wrote {n} rows each:")
    print(f"      D1 shear   -> {CSV_SHEAR}   (expected: anti-holomorphic)")
    print(f"      D0 control -> {CSV_HOLO}    (expected: holomorphic)")
    print(f"      |z| <= {r_max}  (log singularity at z=1 avoided)")


# ----------------------------------------------------------------------
# One PySR round + certification (one dataset per process)
# ----------------------------------------------------------------------
def run_one(which):
    csv_path = CSV_SHEAR if which == "shear" else CSV_HOLO
    out_json = JSON_SHEAR if which == "shear" else JSON_HOLO
    expected = "anti-holomorphic" if which == "shear" else "holomorphic"

    if not os.path.exists(csv_path):
        raise SystemExit(f"missing {csv_path}; run --gen first")

    # Reuse the project's exact operator set, hyperparameters, and judge.
    from pysr_stacking import build_operators, PYSR_BASE
    from verify_exact import certify
    from pysr import PySRRegressor

    df = pd.read_csv(csv_path)
    z = (df.iloc[:, 0].values + 1j * df.iloc[:, 1].values).astype(np.complex128)
    y = (df.iloc[:, 2].values + 1j * df.iloc[:, 3].values).astype(np.complex128)

    binary_ops, unary_ops, sympy_maps = build_operators([])  # no discovered bricks

    model = PySRRegressor(
        **PYSR_BASE,
        binary_operators=binary_ops,
        unary_operators=unary_ops,
        extra_sympy_mappings=sympy_maps,
    )
    model.fit(z.reshape(-1, 1), y)

    y_pred = model.predict(z.reshape(-1, 1))
    mse = float(np.mean(np.abs(y - y_pred) ** 2))
    best_eq = str(model.get_best()["equation"])

    # The ARBITER: exact symbolic certification (not the PySR marker).
    verdict, expr, dfdzbar = certify(best_eq)

    result = {
        "dataset": which,
        "csv": csv_path,
        "best_equation": best_eq,
        "mse": mse,
        "judge_verdict": verdict,
        "judge_dfdzbar": str(dfdzbar),
        "expected_verdict": expected,
        "mse_valid_max": MSE_VALID_MAX,
    }
    with open(out_json, "w") as fh:
        json.dump(result, fh, indent=2)

    print(f"[{which}] best_equation : {best_eq}")
    print(f"[{which}] MSE           : {mse:.3e}   (valid if < {MSE_VALID_MAX:g})")
    print(f"[{which}] JUDGE verdict : {verdict}   (expected: {expected})")
    print(f"[{which}] df/dzbar      : {dfdzbar}")
    print(f"[{which}] -> wrote {out_json}")
    print(f"[{which}] re-check independently: "
          f"python3 verify_exact.py --formula \"{best_eq}\"")


# ----------------------------------------------------------------------
# Combined decision (reads both JSONs)
# ----------------------------------------------------------------------
def report():
    for p in (JSON_HOLO, JSON_SHEAR):
        if not os.path.exists(p):
            raise SystemExit(f"missing {p}; run --which holo and --which shear first")

    holo = json.load(open(JSON_HOLO))
    shear = json.load(open(JSON_SHEAR))

    def ok_mse(r):
        return r["mse"] < MSE_VALID_MAX

    holo_verdict_ok = (holo["judge_verdict"] == "holomorphic")
    shear_verdict_ok = (shear["judge_verdict"] == "anti-holomorphic")
    holo_mse_ok = ok_mse(holo)
    shear_mse_ok = ok_mse(shear)

    print("=" * 64)
    print("B2 CALIBRATION REPORT  (Clunie--Sheil-Small shear)")
    print("=" * 64)
    print(f"D0 control (pure h):")
    print(f"    eq      = {holo['best_equation']}")
    print(f"    MSE     = {holo['mse']:.3e}   {'OK' if holo_mse_ok else 'FAIL (>=1e-3)'}")
    print(f"    verdict = {holo['judge_verdict']}   "
          f"{'OK' if holo_verdict_ok else 'FAIL (expected holomorphic)'}")
    print(f"D1 shear (h + conj(g)):")
    print(f"    eq      = {shear['best_equation']}")
    print(f"    MSE     = {shear['mse']:.3e}   {'OK' if shear_mse_ok else 'FAIL (>=1e-3)'}")
    print(f"    verdict = {shear['judge_verdict']}   "
          f"{'OK' if shear_verdict_ok else 'FAIL (expected anti-holomorphic)'}")
    print("-" * 64)

    discriminates = (holo_verdict_ok and shear_verdict_ok)
    recovers = (holo_mse_ok and shear_mse_ok)

    if discriminates and recovers:
        print("RESULT: PASS [HEURISTIC] -- pipeline calibrated.")
        print("        Detector separates holo (D0) from anti-holo (D1),")
        print("        both recovered with MSE < 1e-3.")
        print("        This is a CALIBRATION, not a discovery. Next: real")
        print("        target (omega giving h,g known only as integrals).")
    elif not discriminates:
        print("RESULT: FAIL -- no discrimination (ARTEFACT, SPARC lesson).")
        print("        D0 and/or D1 misclassified. Do NOT proceed to open targets.")
    else:
        print("RESULT: INCONCLUSIVE -- correct verdicts but MSE >= 1e-3 on")
        print("        at least one dataset: PySR did not recover the form.")
        print("        Increase budget / restarts before any claim.")
    print("=" * 64)


def main():
    ap = argparse.ArgumentParser(description="B2 Clunie--Sheil-Small shear calibration")
    ap.add_argument("--gen", action="store_true", help="generate both CSV datasets only")
    ap.add_argument("--which", choices=["holo", "shear"], help="run one PySR round + certify")
    ap.add_argument("--report", action="store_true", help="combine both JSONs into PASS/FAIL")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--rmax", type=float, default=0.7)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    if args.gen:
        gen(args.n, args.rmax, args.seed)
    elif args.which:
        run_one(args.which)
    elif args.report:
        report()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
