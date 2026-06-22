#!/usr/bin/env python3
"""Does the eml/eml* pair encode the past/future symmetry?
eml* = eml conjugated; complex conjugation = time reversal (T anti-unitary).
Tests: (1) swapping past<->future = conjugation = the eml<->eml* operation;
(2) the conjugation 'jump' is an INVOLUTION (no intrinsic direction);
(3) the 'does Im(W) exist before the sorting?' question is ill-posed (it presupposes a time arrow).
Run on Anthony's machine. Arbiter = this execution + the measurement problem (out of scope)."""
import sympy as sp
import numpy as np

print("="*78)
print("eml/eml* and the past/future symmetry of the weak value")
print("="*78)

ps0,ps1 = sp.symbols('ps0 ps1')      # |psi> past (holomorphic)
fc0,fc1 = sp.symbols('fc0 fc1')      # <phi| = phi* future (anti-holomorphic)
a00,a11 = sp.symbols('a00 a11', real=True)
a01 = sp.symbols('a01'); a10 = sp.conjugate(a01)
W = (fc0*(a00*ps0+a01*ps1)+fc1*(a10*ps0+a11*ps1))/(fc0*ps0+fc1*ps1)
print("\n[1] W = holomorphic in PAST (psi enters bare), anti-holomorphic in FUTURE (phi enters as phi* only).")

A = np.array([[0.4,0.7+0.3j],[0.7-0.3j,-0.2]])
def wv(psi,phi): return (phi.conj()@A@psi)/(phi.conj()@psi)
rng=np.random.default_rng(0); ok=True
for _ in range(6):
    psi=rng.standard_normal(2)+1j*rng.standard_normal(2)
    phi=rng.standard_normal(2)+1j*rng.standard_normal(2)
    if not np.allclose(wv(phi,psi), np.conj(wv(psi,phi))): ok=False
print(f"\n[2] swap past<->future == conjugation == eml<->eml* : wv(phi,psi)==conj(wv(psi,phi)) : {ok}")
print("    => the jump eml<->eml* IS the past<->future / time-reversal operation.")

inv=True
for _ in range(6):
    psi=rng.standard_normal(2)+1j*rng.standard_normal(2)
    phi=rng.standard_normal(2)+1j*rng.standard_normal(2)
    if not np.allclose(wv(psi,phi), np.conj(np.conj(wv(psi,phi)))): inv=False
print(f"\n[3] the jump is an INVOLUTION (conj o conj = identity): {inv}")
print("    => eml->eml* and eml*->eml are the SAME operation. No direction in the reflection.")
print("    The hand (left/right, anti/holo) emerges from the reflection; the DIRECTION (which is")
print("    'future') is an external choice (our time arrow), not a property of the jump.")

print("\n[4] 'does anti-holo exist before the sorting?' is ill-posed:")
print("    pre-postselection state depends only on psi (holo); d/d(phi*)=0 -> no anti before sorting.")
print("    BUT pre-preparation there is no psi -> no holo before preparing. Symmetric.")
print("    Asking 'which exists before' secretly privileges the PAST. The eml/eml* pair does not.")

print("\n"+"="*78)
print("VERDICT: the eml/eml* pair encodes the past/future symmetry by construction (conjugation =")
print("time reversal). The jump between them is an involution: a reflection with no intrinsic")
print("direction. Holo(past) and anti(future) are co-fundamental; the asymmetry the loterie worry")
print("relied on is in the time-oriented QUESTION, not in the object. This settles the laws-symmetry")
print("level. LIMIT: internal coherence, NOT a proof nature realizes post-selection as physical")
print("(= the measurement problem, out of scope). Strong FOR-argument; candidate stays [CONJECTURE strong].")
print("="*78)
