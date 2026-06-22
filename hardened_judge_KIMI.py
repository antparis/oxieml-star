#!/usr/bin/env python3
"""
HARDENED certify_1field — Anti-holomorphic structure detection with numeric fallback.

Blind spots fixed:
- Phase-only moduli (e.g., z*exp(i|z|²)): L is imaginary, fails symbolic L_real check
- Complex moduli (e.g., z*exp((a+ib)|z|²)): L has non-zero imaginary part
- Numeric fallback uses rotation-oracle criterion (Rf/f depends only on z)

Author: adversarial-testing analysis
Requires: sympy, numpy
"""

import sympy as sp
import random
import numpy as np

# ─── SYMBOLS ─────────────────────────────────────────────────────────────
z, zbar = sp.symbols("z zbar")

# ─── FULL CONJUGATION ────────────────────────────────────────────────────

def full_conj(expr):
    """
    Full complex conjugation in Wirtinger calculus.
    Swaps z↔z̄ AND replaces i→−i.

    This is the proper complex conjugation when z and z̄ are treated
    as independent symbols.
    """
    tmp = sp.Symbol("tmp_conj")
    e = expr.subs(sp.I, tmp)
    e = e.subs({z: zbar, zbar: z}, simultaneous=True)
    return e.subs(tmp, -sp.I)

# ─── SYMBOLIC MODULE-TRAPPED CHECK ──────────────────────────────────────

def is_module_trapped(expr):
    """
    Symbolic check for module-trapped functions.

    A function f(z,z̄) is module-trapped if it can be written as:
        f(z,z̄) = holo(z) · M(|z|²)
    where holo(z) is holomorphic and M is real-valued.

    The test computes L = z̄·(∂f/∂z̄)/f and checks:
    1. L is real:  L − full_conj(L) == 0
    2. L is scale-invariant:  L(tz, z̄/t) − L == 0

    LIMITATION: This misses phase-only moduli M = exp(i·θ(|z|²))
    because L is purely imaginary (fails condition 1).
    """
    expr = sp.expand(expr)
    dfdzbar = sp.simplify(sp.diff(expr, zbar))
    dfdz = sp.simplify(sp.diff(expr, z))
    if dfdzbar == 0 or dfdz == 0:
        return False
    try:
        L = sp.simplify(zbar * dfdzbar / expr)
        L_real = sp.simplify(L - full_conj(L)) == 0
        t = sp.symbols("t", positive=True)
        prod_only = sp.simplify(L.subs({z: t*z, zbar: zbar/t}) - L) == 0
        return bool(L_real and prod_only)
    except Exception:
        return False

# ─── NUMERIC FALLBACK UTILITIES ──────────────────────────────────────────

def _numeric_dfdzbar(f_func, z_val, eps=1e-6):
    """
    Numerical Wirtinger derivative ∂f/∂z̄ via central differences.

    ∂f/∂z̄ = ½(∂f/∂x + i·∂f/∂y)  where  z = x + iy,  z̄ = x − iy
    """
    x, y = z_val.real, z_val.imag
    fp_x = f_func(x + eps + 1j*y)
    fm_x = f_func(x - eps + 1j*y)
    fp_y = f_func(x + 1j*(y + eps))
    fm_y = f_func(x + 1j*(y - eps))
    dfdx = (fp_x - fm_x) / (2 * eps)
    dfdy = (fp_y - fm_y) / (2 * eps)
    return 0.5 * (dfdx + 1j * dfdy)


def _numeric_dfdz(f_func, z_val, eps=1e-6):
    """
    Numerical Wirtinger derivative ∂f/∂z via central differences.

    ∂f/∂z = ½(∂f/∂x − i·∂f/∂y)  where  z = x + iy,  z̄ = x − iy
    """
    x, y = z_val.real, z_val.imag
    fp_x = f_func(x + eps + 1j*y)
    fm_x = f_func(x - eps + 1j*y)
    fp_y = f_func(x + 1j*(y + eps))
    fm_y = f_func(x + 1j*(y - eps))
    dfdx = (fp_x - fm_x) / (2 * eps)
    dfdy = (fp_y - fm_y) / (2 * eps)
    return 0.5 * (dfdx - 1j * dfdy)


def _numeric_rotation_ratio(f_func, z_val, eps=1e-6):
    """
    Compute the rotation ratio Rf/f at a point z_val.

    Rf = z·∂f/∂z − z̄·∂f/∂z̄

    For module-trapped f = holo(z)·M(|z|²):
        Rf/f = z·holo'/holo   (depends only on z, not on z̄)
    """
    f_val = f_func(z_val)
    if abs(f_val) < 1e-15:
        return None
    dfdz = _numeric_dfdz(f_func, z_val, eps)
    dfdzbar = _numeric_dfdzbar(f_func, z_val, eps)
    Rf = z_val * dfdz - np.conj(z_val) * dfdzbar
    return Rf / f_val


def _numeric_d_g_dzbar(g_func, z_val, eps=1e-6):
    """
    Numerical Wirtinger derivative ∂g/∂z̄ of a complex-valued function g(z).

    Uses central differences for robustness.
    """
    x, y = z_val.real, z_val.imag
    g_px = g_func(x + eps + 1j*y)
    g_mx = g_func(x - eps + 1j*y)
    g_py = g_func(x + 1j*(y + eps))
    g_my = g_func(x + 1j*(y - eps))
    dgdx = (g_px - g_mx) / (2 * eps)
    dgdy = (g_py - g_my) / (2 * eps)
    return 0.5 * (dgdx + 1j * dgdy)


def _numeric_module_rotation(f_func, num_points=5, eps=1e-5, threshold=5e-2):
    """
    Numeric screen: check if ∂(Rf/f)/∂z̄ ≈ 0 at multiple random points.

    Theory:
    ------
    For f = holo(z)·M(|z|²), the rotation operator gives:
        Rf/f = z·holo'/holo
    which depends ONLY on z (not on z̄). Therefore:
        ∂(Rf/f)/∂z̄ = 0    (module-rotation invariant)

    This condition holds for ALL module-trapped functions, including
    those with complex phase moduli that the symbolic L_real check misses.

    Parameters
    ----------
    f_func : callable
        Function f(z) → complex (zbar is treated as conj(z) for evaluation).
    num_points : int
        Number of random test points.
    eps : float
        Finite-difference step size.
    threshold : float
        Tolerance for declaring ∂(Rf/f)/∂z̄ ≈ 0.

    Returns
    -------
    bool : True if a super-majority of test points satisfy the condition.
    """
    rng = random.Random(42)
    successes = 0
    total = 0
    for _ in range(num_points):
        # Random point away from origin and likely singularities
        zv = (rng.gauss(0, 1) + 1j * rng.gauss(0, 1)) * 0.8 + 0.5 + 0.5j
        try:
            ratio_func = lambda zv: _numeric_rotation_ratio(f_func, zv, eps)
            deriv = _numeric_d_g_dzbar(ratio_func, zv, eps)
            if deriv is not None and abs(deriv) < threshold:
                successes += 1
            total += 1
        except Exception:
            total += 1  # count as failure
    return successes >= max(1, int(0.7 * total)) if total > 0 else False


def _expr_to_numeric_func(expr, param_defaults=None):
    """
    Convert a sympy expression in z,zbar to a callable f(z).

    For numerical evaluation, z̄ is replaced by conj(z).
    """
    if param_defaults:
        expr = expr.subs(param_defaults)
    # Replace zbar with conjugate(z) for numerical evaluation
    expr_num = expr.subs(zbar, sp.conjugate(z))
    return sp.lambdify(z, expr_num, "numpy")


def numeric_module_trapped_screen(expr, param_defaults=None, num_points=5):
    """
    NUMERIC SCREEN: catch module-trapped functions that the symbolic judge misses.

    Blind spots addressed:
    - Phase-only moduli:  z·exp(i·|z|²)  (L is imaginary, fails L_real)
    - Complex moduli:     z·exp((a+ib)·|z|²)  (L has non-zero imaginary part)

    Returns True if the expression appears to be module-trapped by the
    rotation-oracle criterion (Rf/f depends only on z).
    """
    try:
        f_func = _expr_to_numeric_func(expr, param_defaults)
        return _numeric_module_rotation(f_func, num_points=num_points)
    except Exception:
        return False  # screen fails → fall back to symbolic decision


# ─── HARDENED CERTIFICATION ──────────────────────────────────────────────

def certify_1field_hardened(expr, param_defaults=None):
    """
    Certify anti-holomorphic structure with numeric fallback.

    Classification hierarchy:
    1. Symbolic holomorphic check (∂f/∂z̄ == 0) → "holomorphic"
    2. Symbolic real-trapped check (f == full_conj(f)) → "real-trapped"
    3. Symbolic module-trapped check (L real + scale-invariant) → "module-trapped"
    4. NUMERIC FALLBACK: rotation-oracle screen → "module-trapped"
       (Only runs if ∂f/∂z ≠ 0, to avoid re-classifying pure anti-holomorphic)
    5. Default → "anti-holomorphic"

    Parameters
    ----------
    expr : sympy.Expr
        Complex-valued function in z, zbar (treated as independent symbols).
    param_defaults : dict, optional
        Substitutions for any free symbols other than z, zbar.
        Example: {A: 1+2*I, B: 3-I, c: 0.5+0.5*I}
        Required when expr contains symbols other than z and zbar.

    Returns
    -------
    str : One of "holomorphic", "real-trapped", "module-trapped", "anti-holomorphic"
    """
    expr = sp.expand(expr)
    dfdzbar = sp.simplify(sp.diff(expr, zbar))
    if dfdzbar == 0:
        return "holomorphic"
    dfdz = sp.simplify(sp.diff(expr, z))
    if sp.simplify(expr - full_conj(expr)) == 0:
        return "real-trapped"
    if is_module_trapped(expr):
        return "module-trapped"
    # ─── Numeric fallback: catch phase-only / complex moduli ────────────
    # Guard: pure anti-holomorphic (∂f/∂z == 0) stays anti-holomorphic;
    #        numeric screen only helps when BOTH derivatives are non-zero.
    if dfdz != 0 and numeric_module_trapped_screen(expr, param_defaults):
        return "module-trapped"
    return "anti-holomorphic"


# ─── BACKWARD-COMPATIBLE ALIAS ──────────────────────────────────────────

certify_1field = certify_1field_hardened


# ─── SELF-TEST ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Running self-test suite...\n")

    # Parameters for vortex test
    A_sym, B_sym, c_sym = sp.symbols("A_sym B_sym c_sym")
    _PARAM_DEFAULTS = {
        A_sym: 1 + 2*sp.I,
        B_sym: 3 - 1*sp.I,
        c_sym: sp.Rational(1, 2) + sp.I/2
    }

    tests = [
        # Must-stay-anti cases
        ("vortex_N1", A_sym*sp.log(z-c_sym) + B_sym*sp.log(zbar-c_sym),
         "anti-holomorphic"),
        ("z*exp(zbar)", z*sp.exp(zbar), "anti-holomorphic"),
        ("sin(z)+cos(zbar)", sp.sin(z) + sp.cos(zbar), "anti-holomorphic"),
        ("z+zbar**2", z + zbar**2, "anti-holomorphic"),

        # Phase-only modulus (blindspot fixes)
        ("z*exp(I*|z|²)", z*sp.exp(sp.I*z*zbar), "module-trapped"),
        ("z*exp(I*sin(|z|²))", z*sp.exp(sp.I*sp.sin(z*zbar)), "module-trapped"),
        ("z*exp(-I*|z|²)", z*sp.exp(-sp.I*z*zbar), "module-trapped"),

        # Complex modulus (blindspot fixes)
        ("z*exp((1+I)|z|²)", z*sp.exp((1+sp.I)*z*zbar), "module-trapped"),
        ("zbar*exp(I*|z|²)", zbar*sp.exp(sp.I*z*zbar), "module-trapped"),

        # Standard module-trapped
        ("z*exp(|z|²)", z*sp.exp(z*zbar), "module-trapped"),
        ("z²·z̄", z**2*zbar, "module-trapped"),

        # Holomorphic
        ("z²", z**2, "holomorphic"),
        ("exp(z)", sp.exp(z), "holomorphic"),

        # Real-trapped
        ("z+z̄", z + zbar, "real-trapped"),
        ("|z|²", z*zbar, "real-trapped"),

        # Pure anti-holomorphic (dfdz == 0 guard)
        ("z̄³", zbar**3, "anti-holomorphic"),
        ("exp(z̄)", sp.exp(zbar), "anti-holomorphic"),
    ]

    passed = 0
    failed = 0
    for name, expr, expected in tests:
        result = certify_1field_hardened(expr, _PARAM_DEFAULTS)
        status = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"  {status} {name:<25} → {result}")

    print(f"\n{'='*50}")
    print(f"Self-test: {passed} passed, {failed} failed")
    if failed == 0:
        print("All tests passed!")
