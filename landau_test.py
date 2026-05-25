#!/usr/bin/env python3
"""
landau_test.py — eml-star detection test on Landau-level wavefunctions.
Test (B): polynomial part ONLY (no Gaussian e^{-|z|^2/4}), m=2 fixed, n in {0,1,2}.
Symmetric gauge, Schrodinger form: poly_{n,m}(z,zbar) = z^m * L_n^{(m)}(z*zbar/2).
The zbar-degree of the polynomial equals the Landau level n.
Expected: n=0 holomorphic (judge dF/dzbar=0); n=1,2 anti-holomorphic (judge != 0).
VALIDATION test on a real physical system (electron in magnetic field),
z = spatial position (NOT time/frequency -> no Kramers-Kronig oracle).
Run on Anthony's machine. Result HEURISTIQUE until judge verify_exact.py.
"""
import os, json, sys
import numpy as np
import sympy

try:
    from pysr import PySRRegressor
except Exception as e:
    print("PySR import failed:", e); sys.exit(1)

M_FIXED = 2
LEVELS  = [0, 1, 2]
N_PTS   = 1500
SEED    = 42
NITER   = 80
POP     = 300
MAXSIZE = 30
PARSIMONY = 0.001
OUTDIR  = "pysr_output_landau"

def landau_poly_func(n, m):
    z, zb = sympy.symbols('z zb')
    u = z*zb/2
    L = sympy.assoc_laguerre(n, m, u)
    expr = sympy.expand((z**m) * L)
    print(f"[n={n}] symbolic poly (z, zb): {expr}", flush=True)
    f = sympy.lambdify((z, zb), expr, "numpy")
    return f, expr

EML     = "eml(x, y) = exp(x) - log(y + (1e-30 + 0im))"
EMLSTAR = "emlstar(x, y) = exp(conj(x)) - log(conj(y) + (1e-30 + 0im))"
binary_operators = ["+", "-", "*", "/", EML, EMLSTAR]
unary_operators  = ["cos", "sin", "exp", "log",
                    "my_conj(z) = conj(z)",
                    "my_real(z) = complex(real(z))",
                    "my_imag(z) = complex(imag(z))",
                    "my_abs2(z) = z * conj(z)"]
extra_sympy = {
    "eml":     lambda x, y: sympy.exp(x) - sympy.log(y),
    "emlstar": lambda x, y: sympy.exp(sympy.conjugate(x)) - sympy.log(sympy.conjugate(y)),
    "my_conj": lambda z: sympy.conjugate(z),
    "my_real": lambda z: sympy.re(z),
    "my_imag": lambda z: sympy.im(z),
    "my_abs2": lambda z: z * sympy.conjugate(z),
}

rng = np.random.default_rng(SEED)
r   = np.sqrt(rng.uniform(0.01, 4.0, N_PTS))
th  = rng.uniform(0, 2*np.pi, N_PTS)
z   = (r*np.cos(th) + 1j*r*np.sin(th)).astype(np.complex128)

def run_level(n):
    f, expr = landau_poly_func(n, M_FIXED)
    y = f(z, np.conjugate(z)).astype(np.complex128)
    ymax = np.max(np.abs(y))
    if ymax > 0:
        y = y / ymax
    X = z.reshape(-1, 1).astype(np.complex128)
    print(f"[n={n}] y imag_nonzero_frac={np.mean(np.abs(y.imag)>1e-12):.3f}", flush=True)
    model = PySRRegressor(
        niterations=NITER, population_size=POP, maxsize=MAXSIZE,
        parsimony=PARSIMONY, precision=64,
        elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
        binary_operators=binary_operators, unary_operators=unary_operators,
        extra_sympy_mappings=extra_sympy,
        parallelism="multithreading", deterministic=False,
        verbosity=1, output_directory=OUTDIR, run_id=f"landau_n{n}",
    )
    model.fit(X, y)
    best = model.get_best()
    return str(best["equation"]), float(best["loss"]), str(expr)

results = {}
for n in LEVELS:
    print(f"\n===== LANDAU LEVEL n={n}, m={M_FIXED} =====", flush=True)
    eq, mse, expr = run_level(n)
    results[f"n={n}"] = {
        "m": M_FIXED,
        "symbolic_target": expr,
        "expected_zbar_degree": n,
        "best_equation": eq,
        "best_mse": mse,
        "mse_below_1e-3": bool(mse < 1e-3),
    }
    print(f"[n={n}] best_mse={mse:.6g} eq={eq}", flush=True)

with open("landau_result.json", "w") as fh:
    json.dump(results, fh, indent=2)
print("\n=== SUMMARY ===")
print(json.dumps(results, indent=2))
print("=== wrote landau_result.json ===")
print("\nNEXT: run verify_exact.py on each best_equation to certify dF/dzbar per level.")
