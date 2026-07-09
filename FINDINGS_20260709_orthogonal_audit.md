# FINDINGS 2026-07-09 — Orthogonal audit of the boundary quartet: core CONFIRMED (#039 wall, #040 chirality strengthened, #041 detuning law), two #042 readings DOWNGRADED on evidence (anchor = window artifact; switch as observed = window-dependent), floor REFINED (distribution-dependent)

## What
Anthony's request: "make sure we are not hallucinating." Orthogonal-axis
audit of the whole boundary sequence: break the parameters every previous
test held fixed — the measurement window (A), the shared kappa/delta=0.2
(B), the winding-grid type behind the blur floor (C), and the kappa-
independence of the wall (D). Auditor predictions announced before code;
one was again half-refuted (the switch's window-robustness).

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu, 2026-07-09)
```
cd ~/Desktop/oxieml-star && timeout 250 python3 kernel_orthogonal_audit.py
```

## Raw result (machine output, identical to sandbox)
A. WINDOW AUDIT: widening the window [1.05, 200 -> 800 -> 2000]:
   dip(phi=0) at x = 179.26 -> 696.63 -> 1708.61 (tracks the edge);
   dip(phi=135) at x = 1.17 -> 696.63 -> 1708.61 (ALSO tracks the edge).
   -> The far ANCHOR is a WINDOW ARTIFACT (the #042 caution executed);
   AND the phi=135 basin flip, as observed at window [1.05,200], is
   WINDOW-DEPENDENT: at wider windows the minimum sits at the far edge
   at both phases. [Auditor prediction "the switch survives widening" —
   REFUTED.]
B. KAPPA AUDIT: chiral ratio law jump_ow/jump_rec = x^(-c) machine-exact
   (1.1e-16 / 2.2e-16 / 1.1e-16) at kappa = 0.05 / 0.2 / 1.0; phase
   drift at x=2 = +0.9929 / +3.9714 / +19.8572 deg — LINEAR in kappa
   (arg x^(-c) = (kappa/2delta) ln x); reciprocal frozen at every kappa.
   -> #040 CONFIRMED and STRENGTHENED by an explicit linear drift law.
C. FLOOR AUDIT: geometric (log-uniform) winding grids saturate at all
   three spreads (rel. change 128->256 = 1.6% / 1.2% / 1.0%; floor value
   GROWS with spread: 0.0484 / 0.1159 / 0.3020 — consistent with the
   detuning-builds law #041). LINEAR grid does NOT saturate up to N=256
   (0.0116 -> 0.0083 -> 0.0068, rel. change 17%).
   -> The incompressible floor is REAL for log-uniform winding
   distributions but is DISTRIBUTION-DEPENDENT, not an absolute law.
   #042-C wording refined accordingly.
D. WALL AUDIT: truncation wall x*(N=30) = 0.990636 (kappa=0.2) and
   0.987198 (kappa=1.0) — near |x|=1 at both.
   -> #039 boundary CONFIRMED dimensionless, not a parameter accident.

## Verdict
The core of the quartet holds under orthogonal variation: the wall is
dimensionless (#039), the chiral tear law is exact at every kappa with a
linear drift law (#040, strengthened), and the detuning-relief mechanism
is confirmed (floor value tracks spread). Two peripheral READINGS of
#042 are downgraded on evidence: (i) the "anchored position" was
window-relative; (ii) the "topological switch", as observed, was a
feature of the [1.05,200] window. The floor is real but belongs to
log-uniform winding distributions. The registry corrected itself by
machine — the healthiest possible outcome of the audit.

## New hypothesis traced [CONJECTURE, not tested]
At large x each term w_k x^(-(1+c_k)) * x becomes a PURE PHASOR rotating
in ln x (offsets purely imaginary => unit modulus): the relief should be
QUASI-PERIODIC IN LOG SCALE, with alignment dips recurring indefinitely;
any finite window catches one of them (which is exactly what panels A of
#041/#042 saw). Proper framing needs an estimator in the ln x domain
over several decades — this is the #044 candidate.

## Status
- Panels A-D: [ESTABLISHED machine] (run 2026-07-09, identical to
  sandbox, no hardcoded verdict).
- Registry impact: #039 unchanged; #040 unchanged (strengthened); #041
  law unchanged, its "position" wording now understood as window-
  relative; #042 stands WITH its graved caution executed — the caution
  paragraph was the load-bearing part. No entry is invalidated; two
  interpretive sentences are demoted, on machine evidence, by this
  entry.
- Log-quasi-periodicity: [CONJECTURE], traced above.
- Says nothing about nature. Shared FORM, never identity.

## Opens (traced, not started)
- #044: log-periodicity framing — estimator in ln x over >= 4 decades;
  is the relief quasi-periodic with period set by the winding spread?
- Floor law: WHY log-uniform distributions saturate and linear ones do
  not (extreme-winding dominance conjecture from #042 still open).
- Linear-grid decay law: exponent of the continuing decay.
- Paper v3: the boundary section should inherit the downgrades if/when
  #043+#044 are written in (never before).

## Traces
- kernel_orthogonal_audit.py (harness, sandbox-tested 2026-07-08,
  machine-run 2026-07-09)
- FINDINGS_20260708_position_steering.md (#042, whose caution this
  executes)
- This file: FINDINGS_20260709_orthogonal_audit.md
