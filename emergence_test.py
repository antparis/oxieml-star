#!/usr/bin/env python3
"""
emergence_test.py
Does PySR fabricate conjugation from a STRICTLY HOLOMORPHIC toolbox?
One complex input z. Toolbox: +,-,*,/,exp,log,sin,cos. Nothing else
(no my_real, my_imag, my_conj, eml, emlstar).
Targets: holo z**2 (MUST pass, positive control) ; anti conj(z) (MUST fail) ;
mixte z*conj(z) (MUST fail). Judge verify_exact.py is the arbiter; MSE indicative.
"""
import argparse, json, os
import numpy as np
from datetime import datetime, timezone

N_SAMPLES = 2000
DHW = np.pi - 0.05
SEED = 42

def sample_z(rng, n):
    re = rng.uniform(-DHW, DHW, size=n)
    im = rng.uniform(-DHW, DHW, size=n)
    z = (re + 1j*im).astype(np.complex128)
    bad = np.abs(z) < 0.1
    while np.any(bad):
        k = int(bad.sum())
        z[bad] = (rng.uniform(-DHW, DHW, size=k) + 1j*rng.uniform(-DHW, DHW, size=k))
        bad = np.abs(z) < 0.1
    return z

def target_fn(name, z):
    if name == "holo":  return z**2
    if name == "anti":  return np.conj(z)
    if name == "mixte": return z*np.conj(z)
    raise ValueError(name)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True, choices=["holo","anti","mixte"])
    p.add_argument("--niterations", type=int, default=200)
    args = p.parse_args()

    rng = np.random.default_rng(SEED)
    z = sample_z(rng, N_SAMPLES)
    y = target_fn(args.target, z).astype(np.complex128)
    X = z.reshape(-1, 1).astype(np.complex128)
    assert X.shape == (N_SAMPLES, 1)
    assert X.dtype == np.complex128 and y.dtype == np.complex128

    from pysr import PySRRegressor
    binary_ops = ["+", "-", "*", "/"]
    unary_ops  = ["sin", "cos", "exp", "log"]

    output_dir = f"pysr_output_emergence_{args.target}"
    json_out   = f"emergence_{args.target}_result.json"
    print(f"[emergence] target={args.target} N={N_SAMPLES} X.shape={X.shape} x0<->z", flush=True)
    print(f"[emergence] unary={unary_ops} binary={binary_ops}", flush=True)
    print(f"[emergence] FORBIDDEN: my_real,my_imag,my_conj,eml,emlstar", flush=True)

    model = PySRRegressor(
        niterations=args.niterations,
        population_size=500,
        binary_operators=binary_ops,
        unary_operators=unary_ops,
        maxsize=30,
        parsimony=0.001,
        parallelism="serial",
        deterministic=False,
        random_state=SEED,
        precision=64,
        output_directory=output_dir,
        progress=True,
        verbosity=1,
    )
    model.fit(X, y)

    eqs = model.equations_
    loss_col = "loss" if "loss" in eqs.columns else "Loss"
    eq_col   = "equation" if "equation" in eqs.columns else "Equation"
    cx_col   = "complexity" if "complexity" in eqs.columns else "Complexity"
    best = eqs.loc[eqs[loss_col].idxmin()]
    pareto = [{"complexity": int(r[cx_col]), "loss": float(r[loss_col]),
               "equation": str(r[eq_col])} for _, r in eqs.iterrows()]
    result = {
        "status": "complete", "target": args.target,
        "best_equation": str(best[eq_col]), "best_mse": float(best[loss_col]),
        "complexity": int(best[cx_col]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n_samples": N_SAMPLES,
        "toolbox": {"binary": binary_ops, "unary": unary_ops,
                    "forbidden": ["my_real","my_imag","my_conj","eml","emlstar"]},
        "full_pareto_front": pareto,
        "notes": "Strictly holomorphic toolbox. Judge verify_exact.py is the arbiter; MSE indicative.",
    }
    with open(json_out + ".tmp", "w") as f:
        json.dump(result, f, indent=2)
    os.replace(json_out + ".tmp", json_out)
    print(f"[result] {json_out}", flush=True)
    print(f"[result] best_equation: {result['best_equation']}", flush=True)
    print(f"[result] best_mse: {result['best_mse']}", flush=True)
    print(f"[result] complexity: {result['complexity']}", flush=True)

if __name__ == "__main__":
    main()
