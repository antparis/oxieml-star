#!/usr/bin/env python3
"""Weak value as a candidate for INDEPENDENT anti-holomorphic structure.
W = <phi|A|psi> / <phi|psi>  (qubit). |psi> = past (prepared, holomorphic),
<phi| = future (post-selected, anti-holomorphic). Two physically independent states.
Protocol: (2) cross-conjugate? (2b) mixed derivative? (4) rephasing-invariant?
(3) collapse phi=psi -> real? + Project-A caveat (post-selection is a choice).
Run on Anthony's machine. Arbiter = this execution + the open physical question."""
import sympy as sp
import numpy as np

print("="*78)
print("WEAK VALUE  W = <phi|A|psi> / <phi|psi>   (past=psi holo, future=phi anti)")
print("="*78)

# symbolic: psi components (holo), phi-conjugate components fc=phi* (anti), A Hermitian
ps0,ps1 = sp.symbols('ps0 ps1')
fc0,fc1 = sp.symbols('fc0 fc1')
a00,a11 = sp.symbols('a00 a11', real=True)
a01 = sp.symbols('a01'); a10 = sp.conjugate(a01)
num = fc0*(a00*ps0 + a01*ps1) + fc1*(a10*ps0 + a11*ps1)
den = fc0*ps0 + fc1*ps1
W = num/den

print("\n[STEP 2 cross-conjugate] W uses ps (=psi, holo) and fc (=phi*, anti).")
print("  d/d(psi*) : psi* absent => holomorphic in the PAST.")
print("  phi (unconjugated) absent => purely anti-holomorphic in the FUTURE.")
print("  => cross-conjugate z*conj(w): holo past, anti future, two independent states.")

mixed = sp.simplify(sp.diff(W, ps0, fc0))
print(f"\n[STEP 2b mixed derivative] d2W/d ps0 d fc0 != 0 : {mixed != 0}")
print("  => past and future entangled through the overlap <phi|psi> (the 'present').")

al, be = sp.symbols('alpha beta', real=True)
Wp = W.subs({ps0:sp.exp(sp.I*al)*ps0, ps1:sp.exp(sp.I*al)*ps1,
             fc0:sp.exp(-sp.I*be)*fc0, fc1:sp.exp(-sp.I*be)*fc1})
print(f"\n[STEP 4 rephasing-invariant] W unchanged under global rephasing of psi & phi: {sp.simplify(Wp-W)==0}")
print("  => the anti-holo phase is NOT a rephasing artefact (beats van Cittert-Zernike).")

rng = np.random.default_rng(0)
A = np.array([[0.4, 0.7+0.3j],[0.7-0.3j, -0.2]])   # Hermitian observable
def wv(psi, phi): return (phi.conj() @ A @ psi)/(phi.conj() @ psi)

print("\n[STEP 3 collapse phi=psi -> real expectation (lock a)]")
for _ in range(3):
    psi = rng.standard_normal(2)+1j*rng.standard_normal(2)
    Wc = wv(psi, psi)
    print(f"   phi=psi: W = {Wc:.4f}  (|Im| = {abs(Wc.imag):.1e})")

print("\n[generic phi != psi -> genuinely complex, anti-holo alive]")
for _ in range(3):
    psi = rng.standard_normal(2)+1j*rng.standard_normal(2)
    phi = rng.standard_normal(2)+1j*rng.standard_normal(2)
    Wg = wv(psi, phi)
    print(f"   W = {Wg:.4f}  (Im = {Wg.imag:+.3f})")

print("\n[STEP 4 Project-A caveat] can a CHOICE of post-selection make W real?")
psi = np.array([1.0+0j, 0.5j]); found=False
for _ in range(20000):
    phi = rng.standard_normal(2)+1j*rng.standard_normal(2)
    if abs(wv(psi,phi).imag) < 1e-3: found=True; break
print(f"   a post-selection giving real W exists: {found}")
print("   => post-selection is a CHOICE; whether that is a gauge choice (decorative) or a")
print("      physical experiment (real) is THE open question, not settled by algebra.")

print("\n"+"="*78)
print("Known physics (not simulated): Re(W) and Im(W) have DISTINCT measured effects")
print("(Aharonov-Albert-Vaidman: pointer position vs momentum) => Im(W) is not a mere reflection.")
print("STATUS: strongest structural candidate so far; sole open lock = Project-A (post-selection).")
print("="*78)
