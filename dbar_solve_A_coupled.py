#!/usr/bin/env python3
"""
dbar_solve_A_coupled.py — B1 / voie A, FORME 4 (z and zbar COUPLED).
The previous probes (f^2, f(1-f)) were ODEs in zbar with z passive (z only in C1).
True test: couple z and zbar inside the law, so the solution (if closed-form)
carries genuine MIXED structure, not a disguised ODE.
NO data, NO PySR — exact symbolic resolution only.
[CONJECTURE]. If SymPy fails -> wall of voie A on coupled laws (honest finding).
If it succeeds with mixed z/zbar -> first non-trivial candidate.
"""
import sympy as sp

z, zb = sp.symbols('z zb')

def try_equation(label, rhs_func):
    print(f"\n========== {label} ==========")
    fz = sp.Function('f')
    ode = sp.Eq(sp.Derivative(fz(zb), zb), rhs_func(fz(zb)))
    print("Equation: df/dzbar =", rhs_func(sp.Symbol('f')))
    try:
        sol = sp.dsolve(ode, fz(zb))
        print("SymPy solution:"); print(sol)
        rhs_sol = sol.rhs if hasattr(sol, 'rhs') else sol
        has_z  = rhs_sol.free_symbols.__contains__(z)
        has_zb = rhs_sol.has(zb)
        print(f"contains z: {has_z} | contains zbar: {has_zb}")
        if has_z and has_zb:
            print("-> MIXED z/zbar structure (genuinely non-trivial candidate).")
        elif has_zb and not has_z:
            print("-> zbar only, z passive: disguised ODE, NOT interesting.")
        else:
            print("-> no zbar: trivial/holomorphic.")
        return sol
    except Exception as e:
        print(f"SymPy FAILED: {type(e).__name__}: {e}")
        print("-> FINDING: voie A hits a wall on this coupled law.")
        return None

# z modulates the nonlinearity
try_equation("PROBE 3: df/dzbar = z * f^2", lambda F: z*F**2)
# zbar feeds the nonlinearity
try_equation("PROBE 4: df/dzbar = zb * f^2", lambda F: zb*F**2)
# |z|^2 coupling (Landau-like but density-modulated)
try_equation("PROBE 5: df/dzbar = z*zb * f", lambda F: z*zb*F)

print("\n=== DONE ===")
print("Only MIXED z/zbar closed forms are non-trivial candidates for the judge.")
