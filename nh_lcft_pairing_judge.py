#!/usr/bin/env python3
"""Judge the log cross-correlator of the non-Hermitian PT free-fermion LCFT
(Io-Huang-Hsieh arXiv:2602.02649, eq.11 G_{-+} ~ Delta*ln|z-w|^2) against the
ENTANGLED_CHIRAL_ANTI target. Test = PAIRING/reality under full_conj (swap
holo<->anti coordinates + conjugate coefficients only). Self-contained exact,
z,w,zb,wb independent. Authority remains verify_exact.py on this machine. English only."""
import sympy as sp

z, w, zb, wb = sp.symbols('z w zb wb')
Delta = sp.symbols('Delta', positive=True)
pi, phi = sp.pi, sp.GoldenRatio
cc = 1 + sp.I  # generic complex coefficient

def mirror(G):
    # full_conj: swap holo<->anti coordinates AND conjugate coefficients only (I -> -I)
    swapped = G.subs({z: zb, zb: z, w: wb, wb: w}, simultaneous=True)
    return swapped.subs(sp.I, -sp.I)

def judge(G, name):
    anti = sp.simplify(sp.diff(G, zb)) != 0
    real_trapped = sp.simplify(G - mirror(G)) == 0
    if not anti:
        v = "HOL (no anti)"
    elif real_trapped:
        v = "PAIRED -> REAL_TRAPPED (wall)"
    else:
        v = "UNPAIRED -> genuine ENTANGLED_CHIRAL_ANTI (target)"
    print(f"{name:46s} | {v}")

print("="*92)
judge(Delta*(sp.log(z-w) + sp.log(zb-wb)),  "paper G_-+  Delta*[ln(z-w)+ln(zb-wb)]  c=cbar")
judge(pi*sp.log(z-w) + phi*sp.log(zb-wb),   "asym sectors  pi*ln(z-w)+phi*ln(zb-wb)  c!=cbar")
judge(cc*sp.log(z-w) + sp.conjugate(cc)*sp.log(zb-wb), "conj-paired  a*ln(z-w)+conj(a)*ln(zb-wb)")
judge(sp.log(z-w),                          "holo control  ln(z-w)")
print("="*92)
print("paper = REAL_TRAPPED wall (c=cbar symmetric -> paired); asym (c!=cbar) = only target-type; conj-paired = wall.")
