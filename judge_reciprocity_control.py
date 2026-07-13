#!/usr/bin/env python3
"""JUDGE -- reciprocal-dissipative controls (Fable 5's C0/C1) vs the one-way
kernel, and vs our own historical 'decoy' -- SymPy exact, house convention:
M (mirror) = swap z_i <-> zbar_i WITHIN each point, then I -> -I (never
.conjugate() on independent symbols). S (exchange) = swap point labels 1<->2.
Exchange-Hermiticity test: Delta = K - M(S(K)).
Fable 5's proposed alternative (plain reciprocity, no conjugation):
R = K - S(K).
STATUS: [HEURISTIC sandbox] until run on Anthony's machine.
"""
import sympy as sp

z1, z1b, z2, z2b = sp.symbols('z1 z1b z2 z2b')
eta, kappa, delta, Omega, g, beta, kdecoy, m = sp.symbols(
    'eta kappa delta Omega g beta k m', positive=True)
I = sp.I
N = 3  # truncation order for the formal power series

def S(expr):
    """Exchange the two points (1<->2)."""
    return expr.subs({z1: z2, z2: z1, z1b: z2b, z2b: z1b}, simultaneous=True)

def M(expr):
    """Mirror: swap z<->zbar WITHIN each point, then flip literal I -> -I."""
    e = expr.subs({z1: z1b, z1b: z1, z2: z2b, z2b: z2}, simultaneous=True)
    return sp.expand(e.xreplace({sp.I: -sp.I}))

X, Y = z1*z2b, z2*z1b

def report(name, K):
    Delta = sp.expand(K - M(S(K)))
    R = sp.expand(K - S(K))
    c_delta = sp.simplify(Delta.coeff(z1*z2b))
    c_R = sp.simplify(R.coeff(z1*z2b))
    print(f"\n=== {name} ===")
    print(f"  Delta = K - M(S(K)):  X^1 coeff = {c_delta}")
    print(f"    -> exchange-Hermitian (Delta==0)?  {sp.simplify(Delta)==0}")
    print(f"  R = K - S(K):         X^1 coeff = {c_R}")
    print(f"    -> plainly reciprocal (R==0)?      {sp.simplify(R)==0}")
    return sp.simplify(Delta)==0, sp.simplify(R)==0

results = {}

# ---- 0. Historical decoy (our own certified case, sanity check) -----------
K_decoy = sum(kdecoy*X**mm/mm for mm in range(1, N+1))
results['decoy'] = report("DECOY: -k*sum X^m/m  (reproducing-kernel, single direction, real coeff)", K_decoy)

# ---- C0: damped reciprocal oscillators (Fable 5) ---------------------------
def chi(mm):
    wm2 = (mm*delta)**2
    return 1/(wm2 - Omega**2 - I*kappa*Omega)
K0 = eta**2/2 * sum(chi(mm)*(X**mm + Y**mm) for mm in range(1, N+1))
results['C0'] = report("C0: damped reciprocal oscillators (Fable 5)", K0)

# ---- C1: paired-doublet construction matching (m+a)^-2 (Fable 5) ----------
Nmat = sp.Matrix([[I, 1], [1, -I]])
Am_sym = (-kappa/2 - I*m*delta)*sp.eye(2) + g*Nmat
print("\n=== C1 structural checks ===")
print("  A_m symmetric (A_m^T == A_m)?", sp.simplify(Am_sym - Am_sym.T) == sp.zeros(2))
Am1 = Am_sym.subs(m, 1)
Herm_part = sp.simplify((Am1 + Am1.H)/2)
print("  Hermitian part eigenvalues (expect -kappa/2 +/- g):", list(Herm_part.eigenvals().keys()))

bvec = sp.exp(-I*sp.pi/4)/2 * sp.Matrix([1, I])
Mmat = -I*Omega*sp.eye(2) - Am_sym
Minv = sp.simplify(Mmat.inv())
green_expr = sp.simplify((bvec.T * Minv * bvec)[0])
claimed = g/(kappa/2 + I*(m*delta - Omega))**2
check = sp.simplify(green_expr - claimed)
print("  Green's function b^T(-iOmega I - A_m)^-1 b  vs claimed g/[kappa/2+i(m*delta-Omega)]^2")
print("  difference (expect 0):", check)

green0 = sp.simplify(green_expr.subs(Omega, 0))
K1 = eta**2 * sum(green0.subs(m, mm)*(X**mm + Y**mm) for mm in range(1, N+1))
results['C1'] = report("C1: paired-doublet reciprocal-dissipative kernel (Fable 5)", K1)

# ---- Genuine one-way kernel (our real object, single direction, complex a)
a = -I*beta   # beta = kappa/(2 delta)
K_oneway = sum(X**mm/(mm+a)**2 for mm in range(1, N+1))
results['oneway'] = report("ONE-WAY: sum X^m/(m+a)^2, a=-i*beta  (genuine, single direction)", K_oneway)

# ---- Summary table ----------------------------------------------------------
print("\n" + "="*66)
print(f"{'case':10s} {'Delta==0 (exch-Herm)':22s} {'R==0 (plain recip)':20s}")
for name, (d0, r0) in results.items():
    print(f"{name:10s} {str(d0):22s} {str(r0):20s}")
print("="*66)
