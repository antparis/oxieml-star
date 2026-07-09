# FINDINGS 2026-07-10 — Closed-form floors (#050): the floors of the whole #046-#048 campaign are now COMPUTED, not simulated — three hand-derived closed forms (Ci/Si integrals and the sinc), matched to 10^-7..10^-9, and two hidden identities compressing four graved shapes into three canonical measures

## What
The theorem's (#049) predictive power taken at its word: hand-derive
mu_hat for the canonical winding measures and predict the floors to all
digits by pure integration — no choir. During the derivation, TWO HIDDEN
IDENTITIES surfaced and were announced as falsifiable predictions before
code.

## Closed forms (hand-derived, machine-faced by this run)
On [a, b] = [1/300, 1/3]:
 - log-uniform  dmu = dnu/(nu L), L = ln(b/a):
       mu_hat(u) = [Ci(bu) - Ci(au) + i(Si(bu) - Si(au))] / L
 - inverse-square  dmu = dnu/(nu^2 Z), Z = 1/a - 1/b (by parts):
       mu_hat(u) = [e^{iau}/a - e^{ibu}/b + iu(DCi + iDSi)] / Z
 - uniform  dmu = dnu/(b-a):
       mu_hat(u) = (e^{ibu} - e^{iau}) / (iu(b-a))   — the SINC.

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-10)
```
cd ~/Desktop/oxieml-star && timeout 300 python3 kernel_closed_floors_test.py
```

## Raw result (machine output, identical to sandbox)
A+B. CLOSED FORM vs N = 32768 midpoint quantile choir, roughness window:
   log-uniform    : 0.04764907 vs 0.04764907   rel.diff 3.6e-09
   inverse-square : 0.00565563 vs 0.00565562   rel.diff 6.0e-07
   uniform (sinc) : 0.06533857 vs 0.06533857   rel.diff 9.0e-10
   — agreement far beyond the announced >= 5 digits: THE THEOREM
   COMPUTES FLOORS BY PURE INTEGRATION.
C. HIDDEN IDENTITIES (announced before code, faced against graved data):
   I1: foam big-slow (w ~ 1/nu on log-uniform grid) has effective
       measure dnu/nu^2 = EXACTLY the linear-in-delta measure. The
       independently graved 0.00568 (#047, foam, N=64) and 0.00567
       (#048-F, linear limit) are ONE measure's transform — closed form
       0.00566. Two tests, days apart, had measured the same object
       without knowing it.
   I2: foam big-fast (w ~ nu) has effective measure dnu (uniform); its
       transform is the pure SINC. Graved limit 0.06536; closed form
       0.06534. The big-fast foam floor is a sinc contrast.
   Reference: log-uniform closed 0.04765 vs graved 0.04766 (#048-F) and
   0.047649 (#049 companion).
D. RECIPROCAL: mu = delta_0 -> mu_hat = 1 identically -> contrast 0 —
   Corollary C1 of the theorem, no computation needed.

## Verdict — the campaign compresses
The floors of #046, #047 and #048 — dozens of machine measurements — are
now the VALUES OF THREE FORMULAS written with two-century-old functions
(sine/cosine integrals and the cardinal sine). Four graved shapes
collapse into three canonical measures (I1, I2). The compression chain
of the arc completes: four shapes -> three measures -> one law (#048) ->
one theorem (#049) -> three formulas (#050). Good theories end with
fewer things than they started with. And the inverse problem (Anthony's
second pick) now has its dictionary: three closed forms to fit against a
measured relief.

## Status
- Closed forms: [DERIVATION] hand-derived -> machine-faced to
  10^-7..10^-9 by this run: promoted alongside the theorem.
- Hidden identities I1, I2: [ESTABLISHED machine] (announced before
  code, confirmed against independently graved data).
- Graved reference values quoted in panel C are DATA TARGETS from
  #047/#048, not hardcoded verdicts.
- scipy.special.sici used (present in the PySR stack).
- Says nothing about nature. Shared FORM, never identity.

## Opens (traced, not started)
- INVERSE PROBLEM (Anthony's pick, next test): fit the closed forms to
  a "measured" relief from a finite choir; recover the measure's
  parameters; frame the identifiability limits (modulus-only data:
  reflection ambiguity nu -> a+b-nu leaves |mu_hat| invariant — to be
  faced).
- Fourth canonical form: the q-family's warped measures (closed forms
  via incomplete gamma?) — completeness, low priority.
- v3 material: the arc #039-#050 now ends on formulas; DSI prior-art
  FINDINGS still required before any v3 wording.

## Traces
- kernel_closed_floors_test.py (harness; derivations in the docstring)
- PROOF_20260710_fourier_floor_theorem.md (#049, the theorem applied)
- FINDINGS_20260709_size_vs_speed.md, FINDINGS_20260710_fourier_floor_law.md
  (#047/#048, whose graved values are recovered by computation)
- This file: FINDINGS_20260710_closed_floors.md
