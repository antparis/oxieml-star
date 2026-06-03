#!/usr/bin/env python3
"""
hermite_test.py — eml-star detection test on Hermite-Gauss spatial modes.
Pipeline robustness check OUTSIDE Landau: cartesian polynomial structure
H_m(x)*H_n(y) with x=Re(z), y=Im(z), re-expressed in (z, zbar).
Polynomial part ONLY (no Gaussian, which would add trivial zbar dependence).
z = transverse spatial position (NOT time/frequency -> no Kramers-Kronig oracle).
zbar-degree of mode (m,n) = m+n. Modes chosen for a clean degree ladder 1->2->3->4.
Expected: judge verify_exact.py finds df/dzbar != 0 with growing zbar-degree.
This is a VALIDATION of pipeline robustness (degree known a priori = control),
NOT a discovery. Run on Anthony's machine. HEURISTIQUE until judge certifies.
"""
import os, json, sys
import numpy as np
import sympy

try:
    from pysr import PySRRegressor
except Exception as e:
    print("PySR import failed:", e); sys.exit(1)

MODES   = [(1,0), (2,0), (3,0), (2,2)]   # expected zbar-degree 1,2,3,4
N_PTS   = 1500
SEED    = 42
NITER   = 80
POP     = 300
MAXSIZE = 35
PARSIMONY = 0.001
OUTDIR  = "pysr_output_hermite"

def hermite_poly_func(m, n):
    z, zb = sympy.symbols('z zb')
    x = (z + zb)/2
    y = (z - zb)/(2*sympy.I)
    expr = sympy.expand(sympy.hermite(m, x) * sympy.hermite(n, y))
    print(f"[m={m},n={n}] symbolic poly (z, zb): {expr}", flush=True)
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

def run_mode(m, n):
    f, expr = hermite_poly_func(m, n)
    y = f(z, np.conjugate(z)).astype(np.complex128)
    ymax = np.max(np.abs(y))
    if ymax > 0:
        y = y / ymax
    X = z.reshape(-1, 1).astype(np.complex128)
    print(f"[m={m},n={n}] y imag_nonzero_frac={np.mean(np.abs(y.imag)>1e-12):.3f}", flush=True)
    model = PySRRegressor(
        niterations=NITER, population_size=POP, maxsize=MAXSIZE,
        parsimony=PARSIMONY, precision=64,
        elementwise_loss="loss(y, yhat) = abs(y - yhat)^2",
        binary_operators=binary_operators, unary_operators=unary_operators,
        extra_sympy_mappings=extra_sympy,
        parallelism="multithreading", deterministic=False,
        verbosity=1, output_directory=OUTDIR, run_id=f"hermite_m{m}n{n}",
    )
    model.fit(X, y)
    best = model.get_best()
    return str(best["equation"]), float(best["loss"]), str(expr)

results = {}
for (m, n) in MODES:
    print(f"\n===== HERMITE-GAUSS MODE (m={m},n={n}), expected zbar-deg={m+n} =====", flush=True)
    eq, mse, expr = run_mode(m, n)
    results[f"m{m}n{n}"] = {
        "m": m, "n": n,
        "symbolic_target": expr,
        "expected_zbar_degree": m + n,
        "best_equation": eq,
        "best_mse": mse,
        "mse_below_1e-3": bool(mse < 1e-3),
    }
    print(f"[m={m},n={n}] best_mse={mse:.6g} eq={eq}", flush=True)

with open("hermite_result.json", "w") as fh:
    json.dump(results, fh, indent=2)
print("\n=== SUMMARY ===")
print(json.dumps(results, indent=2))
print("=== wrote hermite_result.json ===")
print("\nNEXT: run verify_exact.py on each best_equation to certify dF/dzbar per mode.")
