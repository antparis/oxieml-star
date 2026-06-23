# FINDINGS 2026-06-24 -- Yang-Mills non-Hermitian LCFT (arXiv:2603.19006v1): spin-0 + paired-log double wall

**Status:** [ESTABLISHED] certified by judge_v2.certify_1field on this machine (run: judge_ym_lcft.py).

## What was tested
Closed-form two-point functions of the non-Hermitian Yang-Mills LCFT (Jin-Ren-Yang-Yu, analytic
continuation of Nc), under the eml / eml-star lens. Physical real interval |x^2| -> z*zbar:
  EP_Eq53    : (z zbar)^(-Delta-a) * (r - omega*m*log(z zbar))            [Jordan rank-2, real correlator]
  cross_Eq47 : (z zbar)^(-Delta-a-i*omega)                               [PT-broken cross-correlator, Eq.47]
  G00_Eq49   : (z zbar)^(-Delta-a) * (A cos(omega log zz) - B sin(omega log zz))  [PT-broken real observable]
Certifier mode (closed forms). No shuffle / MSE (symbolic certification, not data discovery).

## Exact command
  cd ~/Desktop/oxieml-star && python3 judge_ym_lcft.py

## Raw result (judge_v2, this machine)
  EP_Eq53    -> real-trapped     (df/dzbar != 0 ; f - full_conj(f) == 0 ; is_module_trapped == True)
  cross_Eq47 -> module-trapped   (df/dzbar != 0 ; f - full_conj(f) != 0 ; is_module_trapped == True)
  G00_Eq49   -> real-trapped     (df/dzbar != 0 ; f - full_conj(f) == 0 ; is_module_trapped == True)
  None anti-holomorphic (eml-star).

## Orthogonal-axis reading
EP_Eq53 expands to z^(-Delta-a) * zbar^(-Delta-a) * (r - omega*m*log z - omega*m*log zbar):
  equal exponents          -> h = hbar -> conformal spin s = 0
  equal log couplings b=bbar=-omega*m -> PAIRED log
=> EP_Eq53 sits on the simultaneous double wall of the orthogonal axis: spin-0 (real-trapped) AND
   paired-log (module-trapped). The two walls coincide; the judge returns real-trapped (tested first).

## Mechanism (why)
The YM two-point correlator is a REAL, 4D, radial object (function of the real interval |x^2|).
Reality mechanically pairs the two logs (b = bbar) and forces h = hbar. The paper's "broken PT
symmetry" is SPACETIME PT in a 4D radial correlator; it does NOT act as the 2D CHIRAL parity required
by the orthogonal axis, hence does NOT desymmetrize b != bbar. The complex anomalous dimension
lambda = a + i*omega sits in the EXPONENT: |x^2|^(-lambda) = |x^2|^(-a) * exp(-i*omega*log|x^2|) is a
log-oscillation of a REAL variable, not a log zbar. Non-Hermitian complex spectrum != spatial anti-holomorphy.

## Conclusion -- [ESTABLISHED]
Non-Hermitian Yang-Mills LCFT does NOT fill the eml-star chiral cell. CONFIRMATION of the orthogonal
axis (spin-0 + paired-log = double wall), not a discovery. eml-star target unchanged: a 2D CHIRAL
parity-broken LCFT where z = x + i*y is the native spatial coordinate and b != bbar is forced.

## Companion papers screened (same batch, out of scope)
  arXiv:2406.10135 (Faber polynomial method): numerical time-propagation tool; eml-star is spatial, not temporal.
  arXiv:2206.05384 (non-Hermitian skin effect): 1D real-space observables; no native complex 2D coordinate.

## Files
  judge_ym_lcft.py (this repo)
