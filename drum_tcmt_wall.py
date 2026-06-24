#!/usr/bin/env python3
"""
drum_tcmt_wall.py  --  eml / eml(star) project, oxieml-star

CLAIM UNDER TEST
----------------
The DRUM non-reciprocal exceptional point, taken at the level of its actual
physical model (Temporal Coupled Mode Theory, two discrete counter-propagating
modes CW/CCW), CANNOT produce a genuine anti-holomorphic structure
log(z1 - conj(z2)). The Jordan-block cross propagator lives in TIME t and
FREQUENCY omega only -- both REAL variables. The target shape log(z1 - conj z2)
is obtainable ONLY by grafting 2D-CFT spatial propagators 1/(z-w) that the
device does not realize. That graft is the SPARC encoding trap (cf. the SPARC
galaxy artefact and spacetime_trap.py for a massless field).

CONCLUSION sought: TCMT route = WALL (real-trapped / artefact), NOT the target.

STATUS: [DERIVATION] until executed on the M920q AND certified by verify_exact.py.
This witness reproduces the exact Wirtinger d/d(zbar) test transparently; the
repo-standard authority remains verify_exact.py / judge_v2.py on Anthony's
machine. The marker printed here is indicative, the judge is the verdict.

Wirtinger convention:  z = x + i y ,  d/d(zbar) = 1/2 ( d/dx + i d/dy ).
A function is HOL (no independent anti) iff  d f / d(zbar) == 0.
"""

import sympy as sp


def dbar(expr, x, y):
    """Exact Wirtinger anti-holomorphic derivative wrt z = x + i*y."""
    return sp.simplify(sp.Rational(1, 2) * (sp.diff(expr, x) + sp.I * sp.diff(expr, y)))


def line(c="-", n=72):
    print(c * n)


# ===========================================================================
# 1. DRUM effective 2x2 Hamiltonian (TCMT), modes (CW, CCW).
#    Non-reciprocal EP realised experimentally: beta_21 = 0, beta_12 != 0,
#    i.e. only CW <- CCW coupling survives  ->  upper-triangular Jordan block.
# ===========================================================================
line("=")
print("1. DRUM non-reciprocal EP Hamiltonian (TCMT, 2 discrete modes)")
line("=")

t = sp.symbols("t", real=True)             # PHYSICAL: time  (REAL)
w = sp.symbols("omega", real=True)         # PHYSICAL: frequency (REAL)
lam = sp.symbols("lambda")                 # complex eigenvalue  omega0 - i*gamma
k1 = sp.symbols("kappa1")                   # non-reciprocal coupling, != 0

H = sp.Matrix([[lam, k1], [0, lam]])
print("H_ep =")
sp.pprint(H)
print("\neigenvalues :", list(H.eigenvals().keys()),
      "  (degenerate -> coalescence)")
print("diagonalizable? :", H.is_diagonalizable(),
      "  -> Jordan block, NON-reducible (Naimark lock by construction)")

# ===========================================================================
# 2. Exact time propagator e^{-iHt}. Cross term carries the Jordan factor t.
#    H = lam*I + k1*N , N=[[0,1],[0,0]], N^2=0  =>  e^{-iHt}=e^{-i lam t}(I - i k1 t N)
# ===========================================================================
line("=")
print("2. Exact cross propagator  e^{-iHt}[0,1]  (the physical observable)")
line("=")

U = (-sp.I * H * t).exp()
U = sp.simplify(U)
print("e^{-iHt} =")
sp.pprint(U)
cross_t = sp.simplify(U[0, 1])
print("\ncross amplitude  <CW| e^{-iHt} |CCW>  in TIME :", cross_t)
print("   -> linear-in-t Jordan factor (source of any log). VARIABLE = t (REAL).")

G_w = k1 / (w - lam) ** 2
print("\ncross Green function in FREQUENCY :", G_w,
      "  (double pole = Jordan signature). VARIABLE = omega (REAL).")

# ===========================================================================
# 3. HONEST test: in the device's OWN variables there is no complex z whose
#    zbar is independent. We make this explicit two ways.
# ===========================================================================
line("=")
print("3. Wirtinger test in the device's own variables")
line("=")

x, y = sp.symbols("x y", real=True)
z = x + sp.I * y

# 3a. The only single-variable transcendental the Jordan factor yields, when its
#     REAL spectral variable is (naively) promoted to a complex z, is log(z).
f_logz = sp.log(z)
d_logz = dbar(f_logz, x, y)
print("3a. naive promotion of the spectral variable to z, f = log(z):")
print("    d/d(zbar) log(z) =", d_logz,
      " ->", "HOL" if d_logz == 0 else "has anti")
print("    => a single-sector log is holomorphic. No anti. (half-chiral wall)")

# 3b. The double pole, same story.
f_pole = 1 / (z - lam) ** 2
d_pole = dbar(f_pole, x, y)
print("\n3b. double pole f = 1/(z-lambda)^2:")
print("    d/d(zbar) =", d_pole, " ->", "HOL" if d_pole == 0 else "has anti")

# ===========================================================================
# 4. THE GRAFT (SPARC trap). To get the target one must INTRODUCE a second,
#    spatial, complex variable z2 and a 2D-CFT cross propagator 1/(z1 - conj z2).
#    The anti is then NON-zero -- but it was CREATED by the graft, not forced
#    by the DRUM, whose model (section 1-2) contains no such spatial z.
# ===========================================================================
line("=")
print("4. The graft that fabricates the target  =  SPARC artefact")
line("=")

x1, y1, x2, y2 = sp.symbols("x1 y1 x2 y2", real=True)
z1 = x1 + sp.I * y1
z2b = x2 - sp.I * y2                        # conj(z2)
f_target = sp.log(z1 - z2b)
d_target = sp.simplify(sp.Rational(1, 2) * (sp.diff(f_target, x2) + sp.I * sp.diff(f_target, y2)))
print("grafted f = log(z1 - conj z2)  [2D-CFT cross propagator]:")
print("    d/d(zbar2) =", d_target, "  (!= 0  -> genuine-anti SHAPE)")
print("    BUT z1, z2 are 2D spatial coordinates the DRUM-TCMT model does")
print("    NOT contain (sections 1-2 have only real t, real omega).")
print("    => the anti is an ENCODING CHOICE, not physics. SPARC trap.")

# ===========================================================================
# VERDICT (indicative marker; authority = verify_exact.py on the M920q)
# ===========================================================================
line("=")
print("VERDICT [DERIVATION, marker]")
line("=")
print("DRUM-TCMT non-reciprocal EP:")
print("  - device variables = {t, omega}, both REAL; cross propagator = t-Jordan")
print("    factor / double pole; single-sector log => HOL (half-chiral wall).")
print("  - target log(z1 - conj z2) reachable ONLY by grafting a spatial z2")
print("    absent from the model => SPARC encoding artefact, NOT forced anti.")
print("  => TCMT route is a WALL. The target is unreachable at the modal level.")
print("  => to escape the trap one must drop TCMT and work at the FIELD level")
print("     (1+1D in the ring) where space is physical -- separate test (step 2).")
print()
print("Repo-standard certification: also pass  log(z), 1/(z-lambda)^2  and the")
print("grafted log(z1-conj z2) to verify_exact.py and confirm the three labels.")
