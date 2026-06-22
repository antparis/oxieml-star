#!/usr/bin/env python3
"""PySR on GW data: reconstruct A33 from z=h22. Tests HOLO vs ANTI features
+ SHUFFLE control, on the 3 precessing sims. Formulas saved for SymPy judge.
PySR works on real/imag parts; the judge (verify_exact.py) decides anti-holo."""
import numpy as np
from pysr import PySRRegressor
import json, time

D = np.load('gw_pysr_data.npz')
PREC = ['p0161','p0163','p0164']
OUT = {}

def make_xy(tag, mode):
    z = D[tag+'_z']; A = D[tag+'_A33']
    x_re, x_im = z.real, z.imag
    if mode == 'holo':
        X = np.column_stack([x_re, x_im])           # z = x_re + i x_im
    elif mode == 'anti':
        X = np.column_stack([x_re, -x_im])          # conj(z) = x_re - i x_im
    elif mode == 'shuffle':
        p = np.random.default_rng(0).permutation(len(z))
        X = np.column_stack([x_re, x_im]); A = A[p]  # break time-corr
    y = A.real                                       # target: Re(A33)
    return X, y
def run(tag, mode):
    X, y = make_xy(tag, mode)
    m = PySRRegressor(
        niterations=80, population_size=60, populations=15,
        binary_operators=["+","-","*","/"],
        unary_operators=["exp","log","sin","cos"],
        maxsize=25, deterministic=True, parallelism="serial",
        random_state=0, progress=False, verbosity=0,
        model_selection="accuracy",
    )
    t0=time.time(); m.fit(X, y); dt=time.time()-t0
    best = m.get_best()
    return {"equation": str(best["equation"]), "loss": float(best["loss"]),
            "complexity": int(best["complexity"]), "seconds": round(dt,1)}

print("PySR GW run start", time.strftime("%H:%M:%S"), flush=True)
for tag in PREC:
    for mode in ["holo","anti","shuffle"]:
        print(f"-> {tag} {mode} ...", flush=True)
        OUT[f"{tag}_{mode}"] = run(tag, mode)
        with open("gw_pysr_results.json","w") as f: json.dump(OUT, f, indent=2)
        r = OUT[f"{tag}_{mode}"]
        print(f"   loss={r['loss']:.3e} cplx={r['complexity']} ({r['seconds']}s): {r['equation']}", flush=True)
print("DONE", time.strftime("%H:%M:%S"), flush=True)
