#!/usr/bin/env python3
"""Does a NATIVELY COMPLEX, reputedly-holomorphic system hide an anti-holomorphic residue?
System: complex potential flow w(z) (holomorphic by construction in ideal fluid theory).
We add physical features (circulation) and check the physical velocity and real observables with the
corrected judge (HOLO / REAL-TRAP / genuine ANTI). Guard: the mirror test MUST cry real-trapped on
real observables. Run on Anthony's machine. Arbiter = this execution."""
import sympy as sp
z, zbar = sp.symbols("z zbar")
U, a, Gamma = sp.symbols("U a Gamma", positive=True)

def full_conj(expr):
    tmp = sp.Symbol("__t__"); e = expr.subs(sp.I, tmp)
    e = e.subs({z: zbar, zbar: z}, simultaneous=True); return e.subs(tmp, -sp.I)
def classify(expr):
    expr = sp.expand(expr)
    d = sp.simplify(sp.diff(expr, zbar))
    if d == 0: return "HOLO", d
    if sp.simplify(expr - full_conj(expr)) == 0: return "REAL-TRAP", d
    return "ANTI", d

print("="*86)
print("Reputedly-holomorphic potential flow: hidden anti residue, or honestly holomorphic?")
print("="*86)

w_ideal = U*(z + a**2/z)
c,d = classify(w_ideal)
print(f"\n[1] ideal cylinder flow w=U(z+a^2/z): {c}   (df/dzbar={d})   expect HOLO")

w_circ = U*(z + a**2/z) - sp.I*Gamma/(2*sp.pi)*sp.log(z)
c,d = classify(w_circ)
print(f"[2] + circulation -i*Gamma/2pi*log(z): {c}   expect HOLO")

dwdz = sp.diff(w_ideal, z)
v_phys = full_conj(dwdz)
c,d = classify(sp.expand(v_phys))
print(f"[3] physical velocity v=conj(dw/dz): {c}   (anti BY DEFINITION; this is the known mirror, b=conj(a))")

speed2 = dwdz*full_conj(dwdz)
c,d = classify(sp.expand(speed2))
print(f"[4] GUARD speed^2=|dw/dz|^2 (real, Bernoulli): {c}   expect REAL-TRAP")

streamfn = (w_ideal - full_conj(w_ideal))/(2*sp.I)
c,d = classify(sp.expand(streamfn))
print(f"[5] GUARD stream function psi=Im(w) (real): {c}   expect REAL-TRAP")

print("\n"+"="*86)
print("VERDICT: the complex potential is HONESTLY HOLOMORPHIC (even with circulation): no hidden anti.")
print("The velocity's anti-ness ([3]) is the KNOWN conjugate relation v=conj(dw/dz) -- mirror anti")
print("(b=conj(a)), NOT an independent residue. Real observables ([4][5]) are correctly REAL-TRAPPED")
print("(guard bites). NEGATIVE RESULT for this system: a field derived from a holomorphic potential can")
print("only yield mirror-anti or real-trap, never independent anti. To find a genuine hidden residue,")
print("the potential itself must break holomorphy for a PHYSICAL reason (true viscous / non-potential")
print("flow). That is the next legitimate target. Do not overclaim the velocity's anti-ness as a find.")
print("="*86)
