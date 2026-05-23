#!/usr/bin/env python3
"""
Joukowski test on the calibrated MIXTE tool (PySR -> SymPy judge).
Cases (all native complex, true z->f(z)):
  holo : w = z + 1/z              -> expect HOLOMORPHIC
  anti : w = z + 1/conj(z)        -> expect ANTI-HOLOMORPHIC
  mixed: w = exp(z) + exp(conj(z))-> expect MIXED (judge: anti, d/dzbar != 0)
  shuf : anti with shuffled targets -> negative control, expect MSE >= 1e-3
NOT a discovery: statuses are known a priori (presence of conj). This validates
the tool on a realistic (aerodynamic) map, one level above the z^2 calibration.
"""
import os
os.environ.setdefault("JULIA_NUM_GC_THREADS", "1")
import json, argparse
import numpy as np, pandas as pd

DATA = "data"
MSE_VALID_MAX = 1e-3
LIGHT_CONFIG = dict(
    niterations=80, population_size=120, precision=64,
    elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
    maxsize=18, maxdepth=8, verbosity=1,
    deterministic=False, parallelism="multithreading",
)
CASES = {
    "holo":  ("data/jouk_holo.csv",  "holomorphic"),
    "anti":  ("data/jouk_anti.csv",  "anti-holomorphic"),
    "mixed": ("data/jouk_mixed.csv", "anti-holomorphic"),  # judge flags d/dzbar!=0
    "shuf":  ("data/jouk_anti_shuf.csv", "anti-holomorphic"),  # neg ctrl
}

def gen():
    os.makedirs(DATA, exist_ok=True)
    rng = np.random.default_rng(42)
    # annulus-ish region, avoid z=0 (Joukowski has 1/z)
    r = rng.uniform(0.6, 1.8, 400)
    th = rng.uniform(0.05, 2*np.pi-0.05, 400)
    z = r*np.exp(1j*th)
    z = z[np.abs(z) > 0.3]
    def save(name, zz, tt):
        with open(f"{DATA}/{name}.csv","w") as f:
            f.write("z_real,z_imag,target_real,target_imag\n")
            for a,b in zip(zz,tt): f.write(f"{a.real},{a.imag},{b.real},{b.imag}\n")
        print(f"  {name}: {len(zz)} pts")
    holo  = z + 1.0/z
    anti  = z + 1.0/np.conj(z)
    mixed = np.exp(z) + np.exp(np.conj(z))
    save("jouk_holo", z, holo)
    save("jouk_anti", z, anti)
    save("jouk_mixed", z, mixed)
    perm = rng.permutation(len(z))
    save("jouk_anti_shuf", z, anti[perm])
    print("Done: 4 Joukowski datasets")

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
    print(f"[{which}] expected: {expected}")
    model = PySRRegressor(**LIGHT_CONFIG, binary_operators=binary_ops,
        unary_operators=unary_ops, extra_sympy_mappings=sympy_maps)
    model.fit(z.reshape(-1,1), y)
    y_pred = model.predict(z.reshape(-1,1))
    mse = float(np.mean(np.abs(y - y_pred)**2))
    best_eq = str(model.get_best()["equation"])
    verdict, expr, dfdzbar = certify(best_eq)
    out = {"dataset":which,"best_equation":best_eq,"mse":mse,
           "judge_verdict":verdict,"judge_dfdzbar":str(dfdzbar),"expected_verdict":expected}
    with open(f"jouk_result_{which}.json","w") as fh: json.dump(out,fh,indent=2)
    print(f"[{which}] eq={best_eq}")
    print(f"[{which}] MSE={mse:.3e} (valid if < {MSE_VALID_MAX:g})")
    print(f"[{which}] verdict={verdict} (expected {expected})")
    print(f"[{which}] -> jouk_result_{which}.json")

def report():
    R = {k: json.load(open(f"jouk_result_{k}.json")) for k in CASES if os.path.exists(f"jouk_result_{k}.json")}
    print("="*60); print("JOUKOWSKI TEST REPORT (MIXTE tool)"); print("="*60)
    ok = True
    for k in ("holo","anti","mixed"):
        if k not in R: print(f"{k}: MISSING"); ok=False; continue
        d=R[k]; want = (d["judge_verdict"]==d["expected_verdict"]) and d["mse"]<MSE_VALID_MAX
        ok &= want
        print(f"{k:6}: eq={d['best_equation']}  MSE={d['mse']:.3e}  verdict={d['judge_verdict']}  {'OK' if want else 'FAIL'}")
    if "shuf" in R:
        s=R["shuf"]; sv = s["mse"]>=MSE_VALID_MAX; ok &= sv
        print(f"shuf  : MSE={s['mse']:.3e}  (neg ctrl, must be >= 1e-3)  {'OK' if sv else 'FAIL'}")
    print("-"*60)
    print("RESULT:", "PASS [HEURISTIC] - tool discriminates on Joukowski maps." if ok else "FAIL - investigate.")
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
