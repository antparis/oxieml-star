#!/usr/bin/env python3
"""B2 shear calibration, config sized for the target (not heavy stacking)."""
import os
os.environ.setdefault("JULIA_NUM_GC_THREADS", "1")
import json, argparse
import numpy as np, pandas as pd

CSV_HOLO = "data/b2_holo_control.csv"
CSV_SHEAR = "data/b2_shear.csv"
JSON_HOLO = "b2_light_result_holo.json"
JSON_SHEAR = "b2_light_result_shear.json"
MSE_VALID_MAX = 1e-3
LIGHT_CONFIG = dict(
    niterations=80, population_size=100, precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    maxsize=18, maxdepth=8, verbosity=1,
    deterministic=False, parallelism="multithreading",
)

def run_one(which):
    csv_path = CSV_SHEAR if which == "shear" else CSV_HOLO
    out_json = JSON_SHEAR if which == "shear" else JSON_HOLO
    expected = "anti-holomorphic" if which == "shear" else "holomorphic"
    if not os.path.exists(csv_path):
        raise SystemExit(f"missing {csv_path}; run b2_shear_run.py --gen first")
    from pysr_stacking import build_operators
    from verify_exact import certify
    from pysr import PySRRegressor
    df = pd.read_csv(csv_path)
    z = (df.iloc[:, 0].values + 1j * df.iloc[:, 1].values).astype(np.complex128)
    y = (df.iloc[:, 2].values + 1j * df.iloc[:, 3].values).astype(np.complex128)
    binary_ops, unary_ops, sympy_maps = build_operators([])
    print(f"[{which}] config: pop=100, niter=80, maxsize=18, multithreading")
    print(f"[{which}] expected judge verdict: {expected}")
    model = PySRRegressor(**LIGHT_CONFIG, binary_operators=binary_ops,
        unary_operators=unary_ops, extra_sympy_mappings=sympy_maps)
    model.fit(z.reshape(-1, 1), y)
    y_pred = model.predict(z.reshape(-1, 1))
    mse = float(np.mean(np.abs(y - y_pred) ** 2))
    best_eq = str(model.get_best()["equation"])
    verdict, expr, dfdzbar = certify(best_eq)
    result = {"dataset": which, "best_equation": best_eq, "mse": mse,
        "judge_verdict": verdict, "judge_dfdzbar": str(dfdzbar),
        "expected_verdict": expected}
    with open(out_json, "w") as fh:
        json.dump(result, fh, indent=2)
    print(f"[{which}] best_equation : {best_eq}")
    print(f"[{which}] MSE           : {mse:.3e}   (valid if < {MSE_VALID_MAX:g})")
    print(f"[{which}] JUDGE verdict : {verdict}   (expected: {expected})")
    print(f"[{which}] df/dzbar      : {dfdzbar}")
    print(f"[{which}] -> wrote {out_json}")

def report():
    holo = json.load(open(JSON_HOLO))
    shear = json.load(open(JSON_SHEAR))
    hv = holo["judge_verdict"] == "holomorphic"
    sv = shear["judge_verdict"] == "anti-holomorphic"
    hm = holo["mse"] < MSE_VALID_MAX
    sm = shear["mse"] < MSE_VALID_MAX
    print("="*60)
    print("B2 LIGHT CALIBRATION REPORT")
    print("="*60)
    print(f"D0 holo : eq={holo['best_equation']}")
    print(f"          MSE={holo['mse']:.3e} {'OK' if hm else 'FAIL'} | verdict={holo['judge_verdict']} {'OK' if hv else 'FAIL'}")
    print(f"D1 shear: eq={shear['best_equation']}")
    print(f"          MSE={shear['mse']:.3e} {'OK' if sm else 'FAIL'} | verdict={shear['judge_verdict']} {'OK' if sv else 'FAIL'}")
    print("-"*60)
    if hv and sv and hm and sm:
        print("RESULT: PASS [HEURISTIC] - calibration OK (NOT a discovery).")
    elif not (hv and sv):
        print("RESULT: FAIL - no discrimination (artefact). Do NOT proceed.")
    else:
        print("RESULT: INCONCLUSIVE - verdicts ok but MSE >= 1e-3.")
    print("="*60)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--which", choices=["holo", "shear"])
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.which: run_one(a.which)
    elif a.report: report()
    else: ap.print_help()

if __name__ == "__main__":
    main()
