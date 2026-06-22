# FINDINGS 2026-06-18 -- [ESTABLISHED sandbox->machine, TOOLING] judge_v2.py: a validated EXTENSION of the exact judge that encodes the distinctions this session forced us to make by hand. It does NOT replace verify_exact.py (unchanged, authoritative single-field judge; dated backup verify_exact.py.bak_20260618 kept). judge_v2 adds three capabilities, each validated on known cases on Anthony's machine, and each ABLE TO RETURN NO (a stricter tool, not a more permissive one): (1) TWO-FIELD Wirtinger mode -- independent symbols z,zbar,w,wbar, the four derivatives, and automatic classification holo-holo (squeezing) / cross-conjugate z*conj(w) (weak-value type) / mixed; (2) REPHASING test -- z->e^{ia}z, w->e^{ib}w, invariant => physical, phase survives => decorative (the CP/Jarlskog + weak-value lesson); (3) MIXED-DERIVATIVE discriminant d^2/dz dzbar -- zero => separable (independent), nonzero => entangled. All 13 self-validation cases pass, INCLUDING the NO cases (decorative cross term -> rephasing inv=False; z+zbar -> separable). Rationale: a better judge must be MORE SEVERE (able to say 'decorative', 'known', 'separable'), never more complaisant -- guard against the SPARC-type self-deception (tuning until the hoped-for result appears).
## Why these three (grounded in this session, not arbitrary)
 - two-field: the whole weak-value thread is f(z,w) with z,w PHYSICALLY independent; the old judge
   only handled f(z,zbar). We did the 4 derivatives by hand repeatedly; now automated.
 - rephasing: the old judge says 'anti-holomorphic' but not 'decorative vs physical'. That is decided
   by rephasing invariance, NOT by d/dzbar (CP phase decorative; weak value invariant; van Cittert-
   Zernike 2-point phase decorative). Now a built-in test.
 - mixed derivative: separable vs entangled (spinor-lock discriminant), in our notes since session 5,
   now in the classifier.
## Validation (executed on Anthony's machine, judge_v2.py self-test)
 - [0] single-field reproduction: z->holo, zbar->anti, |z|^2->anti, conj(conj(z))->holo (trap). All OK.
 - [1] two-field: z*w->holo-holo, z*wbar->cross-conjugate, zbar*w->cross-conjugate, zbar*wbar->mixed. All OK.
 - [2] rephasing: z*wbar->inv=False (decorative), |z|^2->inv=True, |zw|^2->inv=True. All OK (incl. NO).
 - [3] mixed-deriv: z+zbar->separable, z*zbar->entangled, exp(z*zbar)->entangled. All OK (incl. NO).
## Auditor discipline
verify_exact.py NOT modified (pivot file): judge_v2 is a separate extension, must reproduce the
original exactly on single-field cases (it does). Each new test designed to be able to FAIL/say NO,
so the tool stays an arbiter not a yes-machine. A v2 found a discovery only if it can refuse one.
## Status
[ESTABLISHED sandbox->machine, TOOLING] judge_v2 validated (13/13, including NO cases). This is a
CAPABILITY upgrade (faster, stricter classification of what we already understand), NOT a discovery
and NOT new physics. It will let future cases be triaged automatically: holo/anti, decorative/physical,
separable/entangled, single/two-field. Reconnects: rephasing (CP/Jarlskog, weak value 232398dd);
mixed-derivative discriminant (session 5 f5df28ad); two-field criterion (b992c1ae).
Files: judge_v2.py (new), verify_exact.py (unchanged), verify_exact.py.bak_20260618 (backup).
Arbiter = Anthony's machine (self-validation done); verify_exact.py remains the single-field authority.
