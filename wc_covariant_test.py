#!/usr/bin/env python3
# wc_covariant_test.py -- 2026-07-19 -- registry candidate #063
#
# COVARIANT RECIPROCITY WITNESS W_C -- judge certification harness.
#
# Context (registry #055-#059, paper v11 "open certification target"):
#   - Exchange S_C(A) = C^{-1} A^T C with C symmetric, PLUS sector swap
#     X <-> Y (the two conjugated-coordinate sectors X = zbar1*wbar2,
#     Y = zbar2*wbar1 of the separable two-sector class, #057b scope).
#   - Reciprocity invariant R_C = G - S_C(G) on the COMPLETE 2x2
#     transfer kernel (projection trap #059: scalar forms are blind).
#   - Raw comparative witness W = D_X - D_Y (#057): sufficient, never
#     necessary, certified in port basis C = I ONLY.
#   - Sixth-audit counter-example (v10 build trace): block-diagonal
#     C = diag(c1, c2) makes a C-reciprocal kernel
#         G21 = (c1/c2) F(X),  G12 = F(Y)
#     fire the RAW witness falsely (calibration is itself a relative
#     SIZE between channels -- grand-ledger lesson).
#   - Candidate covariant witness:  W_C = D_X - (c1/c2) D_Y.
#
# Clauses (all SymPy exact, Wirtinger convention: sector variables X, Y
# are independent symbols; c1, c2 are UNRESTRICTED nonzero complex
# symbols so every identity below is certified for COMPLEX ratio too --
# the orthogonal-axis-2 question is answered by the generality of the
# symbols, and clause J5c makes the complex ratio explicit):
#
#   J0  scope: a non-diagonal symmetric C mixes the sectors -- the
#       off-diagonal two-sector structure is NOT preserved, so W_C is
#       scoped to sector-preserving (diagonal) calibrations. [LIMITE]
#   J1a tour-6 kernel is C-reciprocal: R_C = 0 (all 4 entries).
#   J1b raw witness fires on it: W_raw != 0 for c1 != c2 (symbolic
#       nonzero + numeric guard at c1=2, c2=1).
#   J1c covariant witness is silent on it: W_C = 0 exactly.
#   J2  reduction: W_C at C = I (c1 = c2) equals W_raw identically.
#   J3  antisymmetry / covariance: W_C(S_C(G)) = -W_C(G) exactly
#       (computed on generic two-sector kernels, not on a special case).
#   J4a calibrated K_eps (add cut-free eps*X**2 to G21): R_C != 0.
#   J4b same kernel: W_C = 0 -- sufficiency-never-necessity transports.
#   J5a size law: G21 = (c1/c2)*rho*F(X), G12 = F(Y) gives
#       W_C = (c1/c2)*(rho - 1)*D exactly (D = disc F).
#   J5b at c1 = c2 this reduces to the #057 law W = (rho-1)*D, i.e.
#       max|W| = |1-rho|*|D| for rho > 0 real.
#   J5c complex-ratio instance: c1/c2 = r*exp(I*theta) substituted
#       explicitly; the law holds with the FULL complex ratio (angle
#       included) -- the witness must carry the ratio, not its modulus.
#   J6a chirality mirror: the same identities hold in the holomorphic
#       sector (non-conjugated products) -- machinery is chirality-
#       agnostic; witness formalism itself carries no chirality claim.
#   J6b shuffle guard: the deliberately WRONG witness D_X - (c2/c1) D_Y
#       does NOT vanish on the C-reciprocal kernel (protects against a
#       trivially-zero implementation).
#
# Numeric arbitration rule: every symbolic zero is double-checked by
# random complex numeric substitution (|residue| < 1e-12 required);
# every claimed nonzero must exceed 1e-6 at the guard point. No verdict
# is hardcoded: PASS/FAIL is computed per clause; exit code 0 iff all
# PASS (J0 counts as PASS when the scope obstruction IS present).

import sys
import sympy as sp

I = sp.I

# ---------------------------------------------------------------- tools
def disc_at(expr, var, u0):
    """Exact directional-limit cut discontinuity of expr(var) at var=u0."""
    eps = sp.Symbol('eps_disc', positive=True)
    above = expr.subs(var, u0 + I * eps)
    below = expr.subs(var, u0 - I * eps)
    return sp.simplify(sp.limit(above - below, eps, 0, '+'))

def is_zero(expr, subs_pool):
    """Symbolic zero + numeric guard on random complex substitutions."""
    s = sp.simplify(sp.expand(expr))
    if s != 0:
        return False
    for subs in subs_pool:
        val = complex(sp.N(expr.subs(subs), 30))
        if abs(val) > 1e-12:
            return False
    return True

def is_nonzero(expr, subs):
    val = complex(sp.N(expr.subs(subs), 30))
    return abs(val) > 1e-6

# ---------------------------------------------------------- symbols
c1, c2 = sp.symbols('c1 c2', nonzero=True)            # complex, general
rho    = sp.Symbol('rho', positive=True)              # size deviation
epsp   = sp.Symbol('epsilon', nonzero=True)           # K_eps knob
X, Y   = sp.symbols('X Y')                            # sector variables
r      = sp.Symbol('r', positive=True)                # |c1/c2|
theta  = sp.Symbol('theta', real=True)                # arg(c1/c2)

F  = lambda u: sp.log(1 - u)          # canonical cut function, cut u>1
U0 = sp.Rational(2)                    # probe point on the cut
U1 = sp.Rational(3)                    # second probe (robustness)

NUMS = [
    {c1: 2 + 3*I, c2: 1 - I, rho: sp.Rational(7, 5), epsp: sp.Rational(1, 3)},
    {c1: -1 + I/2, c2: 3 + 2*I, rho: sp.Rational(2, 7), epsp: -2},
]
GUARD = {c1: 2, c2: 1, rho: sp.Rational(7, 5), epsp: sp.Rational(1, 3)}

# ------------------------------------------------- kernel machinery
def S_C_diag(G):
    """Exchange for diagonal C = diag(c1,c2): transpose + X<->Y swap."""
    Gt = G.T
    Cm = sp.diag(c1, c2)
    Sw = (Cm.inv() * Gt * Cm).applyfunc(
        lambda e: e.subs({X: sp.Symbol('_t')}).subs({Y: X}).subs({sp.Symbol('_t'): Y}))
    return Sw

def witness(G21, G12, u0):
    DX = disc_at(G21, X, u0)
    DY = disc_at(G12, Y, u0)
    W_raw = DX - DY
    W_cov = DX - (c1 / c2) * DY
    return DX, DY, W_raw, W_cov

results = []
def clause(name, ok, note=""):
    results.append((name, bool(ok), note))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {note}" if note else ""))

print("=" * 72)
print("W_C COVARIANT WITNESS -- judge harness (#063 candidate)")
print("=" * 72)

# ---------------------------------------------------------------- J0
# Non-diagonal symmetric C mixes sectors: S_C of an off-diagonal
# two-sector kernel acquires DIAGONAL entries -> structure not preserved.
a, b, d = sp.symbols('a b d', nonzero=True)
Cnd = sp.Matrix([[a, b], [b, d]])
G_ow = sp.Matrix([[0, 0], [F(X), 0]])          # one-way kernel
S_nd = Cnd.inv() * G_ow.T * Cnd                # (no swap needed to see mixing)
mix_11 = sp.simplify(S_nd[0, 0])
mix_22 = sp.simplify(S_nd[1, 1])
j0 = (sp.simplify(mix_11) != 0) or (sp.simplify(mix_22) != 0)
clause("J0  non-diagonal C breaks the two-sector structure (scope: diagonal C)",
       j0, f"S_C(G)_11 = {mix_11}")

# ---------------------------------------------------------------- J1
G21_rec = (c1 / c2) * F(X)
G12_rec = F(Y)
G_rec = sp.Matrix([[0, G12_rec], [G21_rec, 0]])
R_C = sp.simplify(G_rec - S_C_diag(G_rec))
j1a = all(is_zero(R_C[i, j], NUMS) for i in range(2) for j in range(2))
clause("J1a tour-6 kernel is C-reciprocal: R_C = 0 (4 entries)", j1a)

DX, DY, W_raw, W_cov = witness(G21_rec, G12_rec, U0)
DX1, DY1, W_raw1, W_cov1 = witness(G21_rec, G12_rec, U1)
j1b = is_nonzero(W_raw, GUARD) and is_nonzero(W_raw1, GUARD)
clause("J1b raw witness FIRES falsely on it (c1=2,c2=1)", j1b,
       f"W_raw = {sp.simplify(W_raw)}")
j1c = is_zero(W_cov, NUMS) and is_zero(W_cov1, NUMS)
clause("J1c covariant witness is SILENT on it: W_C = 0 exactly", j1c)

# ---------------------------------------------------------------- J2
f2, g2 = sp.Function('f2'), sp.Function('g2')
# reduction is structural: W_C - W_raw = (1 - c1/c2) * D_Y -> 0 at c1=c2
red = sp.simplify((W_cov - W_raw).subs(c1, c2))
DXg = sp.Symbol('DXg'); DYg = sp.Symbol('DYg')      # generic disc symbols
red_gen = sp.simplify((DXg - (c1/c2)*DYg - (DXg - DYg)).subs(c1, c2))
j2 = (red == 0) and (red_gen == 0)
clause("J2  reduction: W_C|_{C=I} = W identically (generic discs)", j2)

# ---------------------------------------------------------------- J3
# Antisymmetry on GENERIC two-sector kernels: G21 = p*F(X), G12 = q*F(Y)
p, q = sp.symbols('p q', nonzero=True)
G_gen = sp.Matrix([[0, q * F(Y)], [p * F(X), 0]])
G_ex  = S_C_diag(G_gen)
_, _, _, Wc_G  = witness(G_gen[1, 0], G_gen[0, 1], U0)
_, _, _, Wc_SG = witness(G_ex[1, 0],  G_ex[0, 1],  U0)
NUMS_pq = [{**s, p: 1 + 2*I, q: -3 + I} for s in NUMS]
j3 = is_zero(sp.simplify(Wc_SG + Wc_G), NUMS_pq)
clause("J3  covariance: W_C(S_C(G)) = -W_C(G) exactly (generic kernel)", j3)

# ---------------------------------------------------------------- J4
G21_ke = (c1 / c2) * F(X) + epsp * X**2         # cut-free deformation
G12_ke = F(Y)
G_ke = sp.Matrix([[0, G12_ke], [G21_ke, 0]])
R_ke = sp.simplify(G_ke - S_C_diag(G_ke))
j4a = is_nonzero(R_ke[1, 0].subs({X: sp.Rational(1, 2), Y: sp.Rational(1, 3)}), GUARD)
clause("J4a calibrated K_eps is C-NON-reciprocal: R_C != 0", j4a,
       f"R_C[21] = {sp.simplify(R_ke[1,0])}")
_, _, _, Wc_ke = witness(G21_ke, G12_ke, U0)
j4b = is_zero(Wc_ke, NUMS)
clause("J4b yet W_C(K_eps) = 0 -- sufficient, NEVER necessary (transports)", j4b)

# ---------------------------------------------------------------- J5
G21_sz = (c1 / c2) * rho * F(X)
G12_sz = F(Y)
_, _, _, Wc_sz = witness(G21_sz, G12_sz, U0)
D_val = disc_at(F(X), X, U0)                     # = -2*I*pi
law = sp.simplify(Wc_sz - (c1 / c2) * (rho - 1) * D_val)
j5a = is_zero(law, NUMS)
clause("J5a size law: W_C = (c1/c2)(rho-1)*D exactly", j5a,
       f"D = {D_val}")
law_I = sp.simplify(Wc_sz.subs(c1, c2) - (rho - 1) * D_val)
j5b = is_zero(law_I, NUMS)
clause("J5b at C=I reduces to #057 law: W = (rho-1)*D, max|W|=|1-rho||D|", j5b)
subs_polar = {c1: r * sp.exp(I * theta), c2: 1}
law_pol = sp.simplify(Wc_sz.subs(subs_polar)
                      - r * sp.exp(I * theta) * (rho - 1) * D_val)
NUMS_pol = [{r: sp.Rational(3, 2), theta: sp.pi / 5, rho: sp.Rational(7, 5)},
            {r: sp.Rational(1, 3), theta: -sp.pi / 7, rho: sp.Rational(2, 7)}]
j5c = is_zero(law_pol, NUMS_pol)
clause("J5c complex ratio r*exp(I*theta): law carries the FULL ratio (angle too)", j5c)

# ---------------------------------------------------------------- J6
Xh, Yh = sp.symbols('Xh Yh')                     # holomorphic sector vars
G21_h = (c1 / c2) * F(Xh)
G12_h = F(Yh)
DXh = disc_at(G21_h, Xh, U0)
DYh = disc_at(G12_h, Yh, U0)
Wc_h = DXh - (c1 / c2) * DYh
j6a = is_zero(Wc_h, NUMS)
clause("J6a holo-sector mirror: same identity holds (chirality-agnostic tool)", j6a)
W_wrong = DX - (c2 / c1) * DY                    # deliberately wrong pairing
j6b = is_nonzero(W_wrong, GUARD)
clause("J6b shuffle guard: WRONG witness D_X-(c2/c1)D_Y does NOT vanish", j6b,
       f"W_wrong = {sp.simplify(W_wrong)}")

# ---------------------------------------------------------------- verdict
print("=" * 72)
npass = sum(1 for _, ok, _ in results if ok)
print(f"VERDICT: {npass}/{len(results)} clauses PASS")
for name, ok, _ in results:
    if not ok:
        print(f"  FAILED: {name}")
print("Status target: [ESTABLISHED machine+judge] iff all PASS on "
      "Anthony's machine.")
sys.exit(0 if npass == len(results) else 1)
