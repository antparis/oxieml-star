#!/usr/bin/env python3
"""CP-judge Stage 2: rephasing certifier.
Distinguishes PHYSICAL phases (survive M -> PL M PR) from REMOVABLE ones.
This is the Kirsch test in CP form: forced phase resists rephasing, decorative
phases evaporate. Calibrated on the known physical-phase count of mixing matrices.
WARNING: this NAIVE diagonal rephasing is correct for GENERAL matrices but WRONG
for discrete type-I groups (Delta(54)) -- that needs the gCP module (Stage 3).
"""
import sympy as sp

def count_physical_phases_mixing(N):
    # known result for an NxN unitary mixing matrix
    return (N-1)*(N-2)//2

# standard PMNS/CKM
s12,s13,s23,c12,c13,c23,delta = sp.symbols('s12 s13 s23 c12 c13 c23 delta', real=True)
Ustd = sp.Matrix([
 [ c12*c13, s12*c13, s13*sp.exp(-sp.I*delta)],
 [-s12*c23 - c12*s23*s13*sp.exp(sp.I*delta), c12*c23 - s12*s23*s13*sp.exp(sp.I*delta), s23*c13],
 [ s12*s23 - c12*c23*s13*sp.exp(sp.I*delta), -c12*s23 - s12*c23*s13*sp.exp(sp.I*delta), c23*c13],
])

def jarlskog(U):
    return sp.im(U[0,0]*U[1,1]*sp.conjugate(U[0,1])*sp.conjugate(U[1,0]))

def test_rephasing_invariance():
    # pollute CKM with 6 arbitrary rephasing phases; J must be unchanged
    a1,a2,a3,b1,b2,b3 = sp.symbols('a1 a2 a3 b1 b2 b3', real=True)
    P1 = sp.diag(sp.exp(sp.I*a1), sp.exp(sp.I*a2), sp.exp(sp.I*a3))
    P2 = sp.diag(sp.exp(sp.I*b1), sp.exp(sp.I*b2), sp.exp(sp.I*b3))
    Upol = P1 * Ustd * P2
    diff = sp.simplify(jarlskog(Upol) - jarlskog(Ustd))
    print("TEST A rephasing-invariance: J(polluted)-J(std) =", diff, "(expect 0)")
    return diff == 0

# ============================================================
# MAJORANA LAYER (rephasing invariants Iij + phase count)
# ============================================================


def test_phase_count():
    expected = {2:0, 3:1, 4:3}
    ok = True
    for N, exp in expected.items():
        got = count_physical_phases_mixing(N)
        flag = "OK" if got == exp else "FAIL"
        if got != exp: ok = False
        print(f"TEST B count N={N}: {got} physical phase(s), expected {exp} [{flag}]")
    return ok


def Iij(m, i, j):
    """Majorana rephasing invariant. NOTE: TWO conjugations (on m_ij AND m_ji).
    Invariant under M -> P M P for a SYMMETRIC Majorana mass matrix."""
    return sp.im(m[i,i] * m[j,j] * sp.conjugate(m[i,j]) * sp.conjugate(m[j,i]))

def count_physical_phases_majorana(N):
    """N x N symmetric Majorana mass matrix: N(N-1)/2 physical phases
    (rephasing M -> P M P removes only N phases from N(N+1)/2 total)."""
    return N*(N-1)//2

def test_majorana_invariance():
    a,b,d = sp.symbols('a b d', complex=True)
    M = sp.Matrix([[a, b],[b, d]])  # symmetric (Majorana)
    p1,p2 = sp.symbols('p1 p2', real=True)
    P = sp.diag(sp.exp(sp.I*p1), sp.exp(sp.I*p2))
    diff = sp.simplify(Iij(P*M*P,0,1) - Iij(M,0,1))
    print("TEST C Majorana I12 rephasing-invariant: diff =", diff, "(expect 0)")
    return diff == 0


def test_phase_count_majorana():
    expected = {2:1, 3:3, 4:6}
    ok = True
    for N, exp in expected.items():
        got = count_physical_phases_majorana(N)
        flag = "OK" if got == exp else "FAIL"
        if got != exp: ok = False
        print(f"TEST E Majorana count N={N}: {got}, expected {exp} [{flag}]")
    return ok


def test_J_blind_Iij_sees():
    m1,m2,m3 = sp.symbols('m1 m2 m3', positive=True)
    al,be = sp.symbols('alpha beta', real=True)
    Pmaj = sp.diag(1, sp.exp(sp.I*al), sp.exp(sp.I*be))
    Uful = Ustd * Pmaj
    mnu = Uful * sp.diag(m1,m2,m3) * Uful.T
    num = {s12:sp.Rational(56,100), c12:sp.sqrt(1-sp.Rational(56,100)**2),
           s13:sp.Rational(15,100), c13:sp.sqrt(1-sp.Rational(15,100)**2),
           s23:sp.Rational(64,100), c23:sp.sqrt(1-sp.Rational(64,100)**2),
           m1:sp.Rational(1,100), m2:sp.Rational(3,100), m3:sp.Rational(5,100)}
    maj = {delta:0, al:sp.Rational(7,10), be:sp.Rational(11,10)}
    J  = complex(jarlskog(Uful).subs(num).subs(maj))
    I  = complex(Iij(mnu,0,1).subs(num).subs(maj))
    I0 = complex(Iij(mnu,0,1).subs(num).subs({delta:0,al:0,be:0}))
    Jd = complex(jarlskog(Uful).subs(num).subs({delta:sp.Rational(8,10),al:0,be:0}))
    print(f"TEST D J(d=0,maj)={J.real:.2e}(blind~0) I12={I.real:.2e}(sees!=0) I12(0)={I0.real:.2e}(~0) J(dirac)={Jd.real:.2e}(!=0)")
    return abs(J)<1e-9 and abs(I)>1e-10 and abs(I0)<1e-12 and abs(Jd)>1e-6

if __name__ == "__main__":
    print("="*60)
    print("CP-JUDGE STAGE 2 -- rephasing certifier (Dirac + Majorana)")
    print("="*60)
    rA = test_rephasing_invariance()
    rB = test_phase_count()
    rC = test_majorana_invariance()
    rD = test_J_blind_Iij_sees()
    rE = test_phase_count_majorana()
    print("-"*60)
    print("  Test A (Dirac J rephasing-invariant)  :", "PASS" if rA else "FAIL")
    print("  Test B (Dirac phase count 0/1/3)      :", "PASS" if rB else "FAIL")
    print("  Test C (Majorana Iij invariant)       :", "PASS" if rC else "FAIL")
    print("  Test D (J blind, I12 sees Majorana phase) :", "PASS" if rD else "FAIL")
    print("  Test E (Majorana phase count 1/3)     :", "PASS" if rE else "FAIL")
    print("-"*60)
    print("STAGE 2", "VALIDATED" if all([rA,rB,rC,rD,rE]) else "FAILED")
    print("NOTE: naive rephasing is WRONG for Delta(54) -- Stage 3 needs gCP module.")
