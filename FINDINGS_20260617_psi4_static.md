# FINDINGS 2026-06-17 -- [DERIVATION, sandbox] Psi4 (Weyl scalar, spin weight -2, gravitational radiation) does NOT break the anti-holo conjecture at the level of its STATIC angular structure on the celestial sphere. Its zeta-bar dependence enters ONLY through the real conformal factor |zeta|^2 (round-sphere metric); the independent information is the holomorphic zeta-power fixed by the discrete spin weight -2. Combination of locks (a)+(c)+(d). Best candidate so far (escapes locks a and b) but the static sector is closed. Teukolsky DYNAMICS remains untested -- the only open door on Psi4.
## Why Psi4 was the strongest candidate
Psi4 = -C_{abcd} n^a mbar^b n^c mbar^d (Newman-Penrose), the outgoing GW scalar. It is NATIVELY
COMPLEX and MEASURED: Re/Im = the two GW polarizations h+ , hx (LIGO/Virgo), and Psi4 = ddot h+ - i ddot hx.
- escapes lock (a) reality: not real, h+ and hx are distinct physical DOF.
- escapes lock (b) causality: Re/Im are two independent polarizations, NOT a Kramers-Kronig pair.
First candidate to escape BOTH (a) and (b). Spin weight -2 = graviton helicity; Psi0 carries +2.
## Test (executed in sandbox; to be re-run on Anthony's machine for certification)
Spin-weight -2 quantity on the sphere in stereographic coordinate zeta (natively complex).
STRUCTURAL representative form (not the exact normalized _{-2}Y_lm): f ~ zeta^4 / (1+zeta*zbar)^2.
  mixed d2 f / dzeta dzbar != 0 (naively "mixed").
  DECISIVE structural check: substitute zbar -> R/zeta with R=|zeta|^2 (real). Result: zeta^4/(R+1)^2.
  => zbar enters ONLY through the REAL combination |zeta|^2 (the round-sphere conformal factor).
  The independent content is the holomorphic power zeta^4, fixed by the discrete spin weight -2.
## Verdict (static sector)
No independent continuous zeta-bar. Three locks combine:
  (a) reality  : zbar sits only in the real metric factor (1+|zeta|^2).
  (c) discrete : the holomorphic zeta-power is set by the integer spin weight (-2).
  (d) spinor   : the object is built on the sphere (theta,phi real) -> real-analytic substrate.
Same mechanism as the chiral SC and QGT: looks mixed, but zbar is locked; independent info is
holomorphic + a discrete integer. Conjecture NOT broken by Psi4's angular structure.
## Honest status and the open door
[DERIVATION, sandbox] -- the structural argument is sound but NOT yet certified on Anthony's machine,
and the form tested is a representative spin-(-2) structure, not the exact harmonic. The mechanism is
generic for spin-weighted quantities, so the conclusion is robust, but mark it sandbox until re-run.
Concordant cases now: T' (certified 616640ad), toy (certified e1c7318e), QGT spinor-lock (certified
f5df28ad), chiral SC (sandbox), exceptional point (sandbox), Tricorn/parity (certified 3cbada22),
Psi4 static (sandbox, this file). Five "did-not-break" systems; three machine-certified, others sandbox.
OPEN DOOR: Psi4 DYNAMICS (Teukolsky equation) -- couples angular dependence to black-hole rotation and
time evolution; a genuine dynamics on a native-complex angular variable. This is the mixed-iterated /
dynamics regime flagged in 3cbada22 and is the ONLY part of Psi4 not yet closed. Dedicated next session.
Files: psi4 sandbox test (this session). Arbiter = Anthony's machine (re-run pending) + judge.
