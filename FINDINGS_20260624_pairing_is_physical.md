# FINDINGS 2026-06-24 -- [DERIVATION] Pairing is physical for two distinct fields; layers_bench reformulated (self-correction)

## Self-correction (a diagnosed error is a result)

While adding a full_conj pairing test to layers_bench, I introduced and then caught a conceptual bug.
The naive full_conj swap z1<->z2b is NOT the reality involution for two DISTINCT fields: it identifies
z2b as conj(z1), which is valid only for ONE field (z<->zb). For two distinct fields A (holo, z1) and
B (anti, z2b), the true reality involution sends z1->conj(z1) and z2b->z2 -- variables ABSENT from the
form. So the swap wrongly forced z1+z2b to be full_conj-invariant and mislabeled it REAL_TRAPPED,
contradicting FINDINGS_20260624_emergence_by_superposition. The swap version was NOT committed.

## What is algebraically decidable vs physical

Algebraically decidable on the symbolic form:
  (1) non-factorizable: d = d_z1 d_z2b log f != 0  (robust).
  (2) EXPLICIT pairing: a separated form with complex conjugate coefficients
      (alpha*u(z1) + conj(alpha)*u(z2b)) is full_conj-invariant with complex coeffs -> REAL_TRAPPED.

NOT algebraically decidable: for two distinct fields, whether z1+z2b is real-trapped or a genuine
crossing depends on whether the two channels are reality-related -- a PHYSICAL question, not readable
from the form. This is exactly the "remaining lock" of the emergence FINDINGS.

## layers_bench reformulation (three verdicts, two-field forms)

  d == 0                                 -> WALL (factorizes)
  d != 0, full_conj-invariant, has I     -> WALL (real-trapped: explicit conjugate coefficients)
  d != 0, full_conj-invariant, no I      -> PHYSICAL (non-factorizable; pairing is a physical question)
  d != 0, NOT full_conj-invariant        -> CANDIDATE (non-factorizable AND not explicitly paired)
One field (z, zb): true involution z<->zb; z+zb -> REAL_TRAPPED.

Command: cd ~/Desktop/oxieml-star && python3 layers_bench.py
Regression checks PASS: counterexample 1+a*log z1+conj(a)*log z2b -> WALL; z1+z2b -> PHYSICAL.

## Correction note on FINDINGS_20260624_emergence_by_superposition

The emergence FINDINGS labeled z1+z2b "EMERGES -> target-type" on the discriminant alone. Corrected:
z1+z2b is PHYSICAL -- non-factorizable, but pairing is undecidable on the form. The emergence FINDINGS
already stated "necessary, not sufficient" with a physical lock, so its spirit holds; only the
"target-type" label was too strong. Not reverted; superseded by this nuance.

## What still holds

The discriminant alone is necessary, NOT sufficient (counterexample with conj coeffs is real-trapped).
The mixed additive argument log(z1-z2b) is not explicitly paired -> CANDIDATE (the robust target route).

## Limit

f.has(I) is a PROXY for "explicit complex conjugate coefficients", robust on the bench cases, not a
general proof. Authority on any real form: nonseparable_judge + nh_lcft_pairing_judge on the machine.

## Status

[DERIVATION]. layers_bench reformulated and regression-tested in sandbox; to confirm on the machine.
Chiral cell still EMPTY. Bottleneck unchanged: a real device's closed-form correlator.
