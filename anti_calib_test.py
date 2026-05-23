#!/usr/bin/env python3
"""
MIXTE tool calibration on a KNOWN anti-holomorphic target.
Target D1: f(z) = conj(z)^2   (anti-holomorphic, known closed form)
Control  : f(z) = z^2         (holomorphic positive control)
Negative : D1 with shuffled targets (must be REJECTED at MSE)
Pipeline : PySR (MIXTE operators) -> SymPy judge (verify_exact, MIXTE).
Calibration only, NOT a discovery (classes known in advance).
"""
import os
os.environ.setdefault("JULIA_NUM_GC_THREADS", "1")
import json, argparse
import numpy as np, pandas as pd

DATA = "data"
MSE_VALID_MAX = 1e-3
LIGHT_CONFIG = dict(
    niterations=60, population_size=100, precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    maxsize=16, maxdepth=8, verbosity=1,
    deterministic=False, parallelism="multithreading",
)
CASES = {
    "anti":    ("data/calib_anti.csv",      "anti-holomorphic"),
    "holo":    ("data/calib_holo.csv",      "holomorphic"),
    "shuffle": ("data/calib_anti_shuf.csv", "anti-holomorphic"),  # neg ctrl: expect MSE>=1e-3
}

def gen():
    os.makedirs(DATA, exist_ok=True)
    rng = np.random.default_rng(0)
    # native complex sample, away from 0 (log/branch safety)
    z = rng.uniform(-1.0, 1.0, 400) + 1j*rng.uniform(-1.0, 1.0, 400)
    z = z[np.abs(z) > 0.15]
    def save(name, zz, tt):
        with open(f"{DATA}/{name}.csv","w") as f:
            f.write("z_real,z_imag,target_real,target_imag\n")
            for a,b in zip(zz,tt): f.write(f"{a.real},{a.imag},{b.real},{b.imag}\n")
        print(f"  {name}: {len(zz)} pts")
    anti = np.conj(z)**2
    holo = z**2
    save("calib_anti", z, anti)
    save("calib_holo", z, holo)
    # negative control: same z, but targets shuffled -> no functional relation
    perm = rng.permutation(len(z))
    save("calib_anti_shuf", z, anti[perm])
    print("Done: 3 calibration datasets")

def run_one(which):
    csv_path, expected = CASES[which]
    if not os.path.exists(csv_path):
        raise SystemExit(f"missing {csv_path}; run with --gen first")
    from pysr_stacking import build_operators
    from verify_exact import certify
    from pysr import PySRRegressor
    df = pd.read_csv(csv_path)
    z = (df.iloc[:,0].values + 1j*df.iloc[:,1].values).astype(np.complex128)
    y = (df.iloc[:,2].values + 1j*df.iloc[:,3].values).astype(np.complex128)
    binary_ops, unary_ops, sympy_maps = build_operators([])
    print(f"[{which}] expected: {expected}  (shuffle should FAIL at MSE)")
    model = PySRRegressor(**LIGHT_CONFIG, binary_operators=binary_ops,
        unary_operators=unary_ops, extra_sympy_mappings=sympy_maps)
    model.fit(z.reshape(-1,1), y)
    y_pred = model.predict(z.reshape(-1,1))
    mse = float(np.mean(np.abs(y - y_pred)**2))
    best_eq = str(model.get_best()["equation"])
    verdict, expr, dfdzbar = certify(best_eq)
    out = {"dataset":which,"best_equation":best_eq,"mse":mse,
           "judge_verdict":verdict,"judge_dfdzbar":str(dfdzbar),
           "expected_verdict":expected}
    with open(f"calib_result_{which}.json","w") as fh: json.dump(out,fh,indent=2)
    print(f"[{which}] eq={best_eq}")
    print(f"[{which}] MSE={mse:.3e} (valid if < {MSE_VALID_MAX:g})")
    print(f"[{which}] verdict={verdict} (expected {expected})")
    print(f"[{which}] -> calib_result_{which}.json")

def report():
    a = json.load(open("calib_result_anti.json"))
    h = json.load(open("calib_result_holo.json"))
    s = json.load(open("calib_result_shuffle.json"))
    print("="*60); print("ANTI CALIBRATION REPORT (MIXTE tool)"); print("="*60)
    av = a["judge_verdict"]=="anti-holomorphic" and a["mse"]<MSE_VALID_MAX
    hv = h["judge_verdict"]=="holomorphic"      and h["mse"]<MSE_VALID_MAX
    sv = s["mse"]>=MSE_VALID_MAX  # neg control must FAIL at MSE
    print(f"anti   : eq={a['best_equation']}  MSE={a['mse']:.3e}  verdict={a['judge_verdict']}  {'OK' if av else 'FAIL'}")
    print(f"holo   : eq={h['best_equation']}  MSE={h['mse']:.3e}  verdict={h['judge_verdict']}  {'OK' if hv else 'FAIL'}")
    print(f"shuffle: MSE={s['mse']:.3e}  (neg ctrl, must be >= 1e-3)  {'OK' if sv else 'FAIL'}")
    print("-"*60)
    if av and hv and sv:
        print("RESULT: PASS [HEURISTIC] - MIXTE tool calibrated. Detects anti, holo, rejects noise.")
    else:
        print("RESULT: FAIL - tool not behaving as expected. Investigate before proceeding.")
    print("="*60)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", action="store_true")
    ap.add_argument("--which", choices=list(CASES.keys()))
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.gen: gen()
    elif a.which: run_one(a.which)
    elif a.report: report()
    else: ap.print_help()
if __name__ == "__main__":
    main()
