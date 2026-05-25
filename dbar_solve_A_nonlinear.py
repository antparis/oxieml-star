#!/usr/bin/env python3
"""
dbar_solve_A_nonlinear.py — B1 / voie A, FORME 3 (terrain inconnu).
Nonlinear forced-mirror law: df/dzbar = f^2  (Wirtinger, z param, integrate zbar).
This is the OPEN case: unlike df/dzbar=z*f (linear, known gaussian-type solution),
a nonlinear dbar-equation may NOT have a clean closed form. Goal: probe whether
SymPy can solve it at all, and if so, whether the solution genuinely carries zbar.
Also tries df/dzbar = f*(1-f) as a second nonlinear probe.
NO data, NO PySR — exact symbolic resolution only.
[CONJECTURE] until SymPy returns something + we inspect it. If SymPy fails to
solve, that itself is the finding: method A hits a wall on nonlinear dbar-laws.
"""
import sympy as sp

z, zb = sp.symbols('z zb')

def try_equation(label, rhs_func):
    print(f"\n========== {label} ==========")
    fz = sp.Function('f')
    # rhs_func takes fz(zb) and returns the right-hand side
    ode = sp.Eq(sp.Derivative(fz(zb), zb), rhs_func(fz(zb)))
    print("Equation: df/dzbar =", rhs_func(sp.Symbol('f')))
    try:
        sol = sp.dsolve(ode, fz(zb))
        print("SymPy solution:")
        print(sol)
        # Inspect: does the solution carry zbar genuinely (not only via C1)?
        rhs_sol = sol.rhs if hasattr(sol, 'rhs') else sol
        has_zb = rhs_sol.has(zb)
        print(f"Solution contains zbar symbol: {has_zb}")
        if has_zb:
            print("-> mirror present in closed form (promising).")
        else:
            print("-> WARNING: no zbar in solution; trivial/holomorphic-in-disguise.")
        return sol
    except Exception as e:
        print(f"SymPy FAILED to solve in closed form: {type(e).__name__}: {e}")
        print("-> FINDING: method A hits a wall on this nonlinear dbar-law.")
        return None

# Probe 1: df/dzbar = f^2
try_equation("PROBE 1: df/dzbar = f^2", lambda F: F**2)

# Probe 2: df/dzbar = f*(1-f)  (logistic-type)
try_equation("PROBE 2: df/dzbar = f*(1-f)", lambda F: F*(1-F))

print("\n=== DONE ===")
print("If a closed form with zbar emerged: candidate for the judge (certify df/dzbar).")
print("If SymPy failed: voie A insufficient for nonlinear laws -> need alternative.")
