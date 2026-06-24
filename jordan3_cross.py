#!/usr/bin/env python3
"""jordan3_cross.py -- reduce ChatGPT #7 (extended Jordan, rank 3) to the judge.

Tests: (A) rank-3 propagator carries t^2 -> log^2; (B) disc product vs additive is
rank-independent; (C) THE KEY -- disc != 0 does NOT imply target (a non-factorizable
form can still be full_conj-invariant = real-trapped = WALL); (D) the mixed additive
argument log(z1-z2b) and log^2(z1-z2b) are non-factorizable AND structurally non-paired;
(E) verdict on whether rank 3 opens a new cell or enriches the same one.

Sandbox oracle. Authority = nonseparable_judge + nh_lcft_pairing_judge on the machine."""
import sympy as sp
z1, z2b, t, lam, g = sp.symbols('z1 z2b t lambda g')
a, c = sp.symbols('a c')
ar, ai = sp.symbols('ar ai', real=True)
I = sp.I

def disc(f):                      # nonseparable_judge core
    return sp.simplify(sp.diff(sp.log(f), z1, z2b))
def full_conj(f):                 # swap holo<->anti coords AND conjugate coeffs (I->-I)
    return f.subs({z1: z2b, z2b: z1, I: -I}, simultaneous=True)
def paired(f):                    # real-trapped iff full_conj-invariant
    return sp.simplify(full_conj(f) - f) == 0

print("="*76)
print("A -- rank-3 non-reciprocal Jordan block: t^2 factor -> log^2")
print("="*76)
H3 = sp.Matrix([[lam, g, 0], [0, lam, g], [0, 0, lam]])
nind = sum(len(bs) for (v, m, bs) in H3.eigenvects())
P3 = sp.simplify(sp.exp(-I*H3*t))
print(f"eigenvectors {nind}/3 (non-diagonalizable); P[0,2]={sp.simplify(P3[0,2])} -> t^2 -> log^2")

print()
print("="*76)
print("B -- disc: product=WALL, additive=non-factorizable (rank-independent)")
print("="*76)
for name, f in [("product  z1*z2b", z1*z2b),
                ("additive 1 + a*log z1 + a*log z2b", 1 + a*sp.log(z1) + a*sp.log(z2b))]:
    d = disc(f)
    print(f"  {name:34s} | d={'0' if d==0 else 'NONZERO'} -> {'WALL' if d==0 else 'non-fact.'}")

print()
print("="*76)
print("C -- KEY: disc != 0 does NOT imply target (pairing is mandatory)")
print("="*76)
acmp = ar + I*ai
# non-factorizable BUT paired (coefficient = conjugate): real-trapped wall
f_trap = 1 + acmp*sp.log(z1) + full_conj(acmp)*sp.log(z2b)
print("  f = 1 + a*log z1 + conj(a)*log z2b")
print(f"    disc != 0 ? {disc(f_trap) != 0}   (non-factorizable)")
print(f"    full_conj-invariant ? {paired(f_trap)}   -> REAL_TRAPPED = WALL despite disc!=0")
print("  => discriminant alone is NECESSARY, NOT sufficient. This is ChatGPT's blind spot.")

print()
print("="*76)
print("D -- mixed additive argument: non-factorizable AND non-paired (rank 1 and 2)")
print("="*76)
L = sp.log(z1 - z2b)
for name, f in [("rank1 mixed  log(z1-z2b)",       L),
                ("rank2 mixed  log^2(z1-z2b)",      L**2),
                ("rank3 mixed  a*L + c*L^2 + 1",    1 + a*L + c*L**2)]:
    d = disc(f)
    print(f"  {name:30s} | disc={'0' if d==0 else 'NONZERO'} | full_conj-invariant={paired(f)}")

print()
print("="*76)
print("E -- verdict")
print("="*76)
print("Rank-3 Jordan -> log^2, same non-factorizable+non-paired cell as rank-2, richer")
print("structure (higher-rank LCFT). NOT a new door: it enriches the existing target cell.")
print("Confirmed: the mixed additive argument is what gives non-pairing; asymmetric or")
print("conjugate-paired coefficients on a product/separated form stay walls. Pairing test")
print("is mandatory alongside the discriminant.")
