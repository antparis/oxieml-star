#!/usr/bin/env python3
"""
drum_field_sparc.py  --  eml / eml(star) project, oxieml-star

CLAIM UNDER TEST
----------------
The DRUM at the FIELD level (1+1D field in the ring, not the 2-mode TCMT) carries
no genuine anti-holomorphic structure either. Three branches, all closed:

 (a) Real light-cone  u = s - v t (CW),  w = s + v t (CCW): u, w are two REAL,
     INDEPENDENT variables and w != conj(u). Chirality here is FACTORIZATION on
     real coordinates, NOT Wirtinger anti-holomorphy (which needs zbar = conj z).
     Encoding z = u (real) gives conj(z) = z, hence eml = eml(star): SPARC option A.

 (b) Wick rotation t -> -i tau_E makes z = s + v tau_E genuinely complex and
     w = conj(z); the Wirtinger test then applies. BUT Wick is an ERASABLE
     treatment choice (the DRUM lives in real time). SPARC: reverts to (a) in
     real time, forced only under thermal / KMS periodicity -- absent in a
     passive DRUM.

 (c) Non-Hermiticity (gain/loss) puts the complex in the TEMPORAL EXPONENT:
     e^{-i lambda t} with lambda = omega0 - i gamma is HOLOMORPHIC in t
     (d/d zbar = 0). The loss gamma is a PARAMETER in the exponent, NOT an
     independent zbar dependence. Identical mechanism to the Yang-Mills NH LCFT
     wall (commit 07792fd): complex frequency creates no spatial anti-holomorphy.

CONCLUSION: DRUM closed entirely (modal AND field). Derived 7th sieve condition:
the COMPLEXITY CARRIER must be SPATIAL-anti-holomorphic, not a temporal exponent.

STATUS: [DERIVATION] until executed on the M920q and certified by verify_exact.py.
Wirtinger convention: z = x + i y, d/d zbar = 1/2 (d/dx + i d/dy).
"""

import sympy as sp


def dbar(expr, x, y):
    """Exact Wirtinger anti-holomorphic derivative wrt z = x + i*y."""
    return sp.simplify(sp.Rational(1, 2) * (sp.diff(expr, x) + sp.I * sp.diff(expr, y)))


def line(c="=", n=72):
    print(c * n)


# ===========================================================================
line()
print("(a) real light-cone: the two movers are NOT complex conjugates")
line()
s, t, v = sp.symbols("s t v", real=True, positive=True)
u = s - v * t                      # CW mover argument
w = s + v * t                      # CCW mover argument
print("u = s - v t      :", u, "   conj(u) =", sp.conjugate(u))
print("w = s + v t      :", w)
print("w - conj(u)      :", sp.simplify(w - sp.conjugate(u)),
      "  != 0  ->  (u, w) is NOT (z, zbar)")
print("=> chirality here = factorization on REAL coords, not Wirtinger anti.")
print("=> encoding z = u (real): conj(z) = z, eml = eml(star)  [SPARC option A].")

# ===========================================================================
print()
line()
print("(c) non-Hermitian loss lives in the EXPONENT, not in zbar")
line()
x, y = sp.symbols("x y", real=True)
z = x + sp.I * y
w0, gam = sp.symbols("omega0 gamma", real=True)
lam = w0 - sp.I * gam               # complex eigenvalue, loss gamma
f_exp = sp.exp(-sp.I * lam * z)      # temporal factor, t promoted to complex z
d_exp = dbar(f_exp, x, y)
print("f = exp(-i*lambda*z),  lambda = omega0 - i*gamma  (complex):")
print("    d/d zbar f =", d_exp, " ->", "HOL" if d_exp == 0 else "has anti")
print("=> gamma is a PARAMETER in the exponent, NOT an independent zbar.")
print("=> a complex (non-Hermitian) frequency creates NO anti-holomorphy.")
print("   (identical to the Yang-Mills NH LCFT wall, commit 07792fd)")

# ===========================================================================
print()
line()
print("(b) Wick rotation makes it complex -- but that is a treatment CHOICE")
line()
tauE = sp.symbols("tau_E", real=True)
zc = s + v * tauE                   # after Wick  t -> -i tau_E
print("z = s + v*tau_E  (Euclidean),  conj(z) = s - v*tau_E  -> Wirtinger valid.")
print("=> but Wick is ERASABLE; reverts to (a) in real time.")
print("   SPARC: forced only under thermal/KMS periodicity (absent in passive DRUM).")

# ===========================================================================
print()
line()
print("VERDICT [DERIVATION, marker]")
line()
print("DRUM field level (1+1D):")
print("  (a) real light-cone     -> SPARC artefact if encoded (eml = eml*)")
print("  (b) Wick                -> erasable choice (no KMS forcing in passive DRUM)")
print("  (c) non-Hermiticity     -> complex in temporal exponent, HOL, no zbar")
print("=> DRUM CLOSED entirely (modal AND field). Chiral cell: still empty.")
print()
print("=> 7th sieve condition (forcing_filter.py):")
print("   complexity_carrier == SPATIAL-anti-holomorphic, NOT temporal-exponent.")
print("   Eliminates upfront (no simulation): Hatano-Nelson, YM NH LCFT,")
print("   PT free-fermion, DRUM -- all carry complexity in a temporal/spectral")
print("   exponent of a real variable.")
print()
print("=> live door: non-equilibrium two-bath steady state, where the complex")
print("   can enter the SPATIAL correlator via stationary currents. To be framed")
print("   next, with its own SPARC test (physical current vs gauge).")
print()
print("Repo-standard: pass exp(-i*lambda*z) to verify_exact.py and confirm HOL.")
