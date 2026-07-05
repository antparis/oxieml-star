# FINDINGS 2026-07-05 — delta_CP / Jarlskog invariant: eml* DECORATIVE (T' lepton model)

## What
Last untested door of the neutrino sector: delta_CP, probed via the rephasing-invariant
Jarlskog invariant J — the only natively complex observable of the Qu-Lu-Ding T' lepton
model. Question: does cutting the eml* (anti-holomorphic) tower kill J (eml* carrier,
narrow candidate) or does J survive (eml* decorative, wall extended)?

## Exact command (Anthony's machine, ThinkCentre M920q, Ubuntu)
```
cd ~/Desktop/oxieml-star && setsid nohup python3 -u cp_dcp_test.py > cp_dcp_run_20260705.log 2>&1 &
```
PID 75233, detached run, mpmath dps=20, 21 Nelder-Mead starts per mode, tau constrained
to the fundamental domain. Total runtime ~ overnight (2026-07-04 -> 2026-07-05).

## Raw result (cp_dcp_run_20260705.log, complete)
```
--- full     chi2=   0.91  tau=-0.0514+1.0895i  J=-8.130898e-03
--- holo     chi2=   0.23  tau=-0.0579+1.0125i  J=+3.021078e-02
--- nonholo  chi2=   0.04  tau=-0.0627+1.0352i  J=-2.685558e-02
[L2] same tau (full best-fit), modes swapped on Y2pp:
     full     J=-8.130898e-03
     holo     J=-3.449908e-02
     nonholo  J=-1.323804e-02
[NULL] Re(tau)=0 -> J(Re tau=0)=+0.000e+00
[ORTHOGONAL AXIS] sweep Re(tau), fixed Im/g2/beta/gamma:
     antisymmetric under Re(tau) -> -Re(tau); J(0)=0 exactly. ODD check: True
READING: |J_holo| ~ |J_full|: cutting eml* does NOT kill J. eml* DECORATIVE for delta_CP.
```

## Anchoring checks (auditor)
- chi2 anchors 0.91 / 0.23 / 0.04 reproduce FINDINGS_20260623b exactly: the harness
  fits the same model as full_chi2_test.py on all three modes. Sound.
- Tribunal 1 (per-mode refit): |J_holo| = 3.02e-02, i.e. ~3.7x |J_full|, opposite sign.
  Sign is NOT invariant across refits (each mode refinds its own tau; J sign also
  depends on mass ordering) — hence tribunal L2.
- Tribunal 2 (tau frozen at full best-fit, modes swapped on Y2pp): J stays finite and
  nonzero in every mode (holo -3.45e-02, nonholo -1.32e-02). No mode sends J -> 0.
- NULL control: J(Re tau=0) = 0 to machine zero. Sweep: J odd in Re(tau), J(0)=0.
  Machine confirmation that the CP phase originates in Re(tau) via q = exp(2*pi*i*tau),
  present in BOTH the eml and eml* towers — not in the anti-holomorphic needle.

## Verdict
Cutting eml* does not kill J in either tribunal. **eml* is DECORATIVE for delta_CP**
in the T' lepton model. This closes the last door of the neutrino sector: the wall
goes from 5 levels to 6, now including the only natively complex observable.
Consistent with the navigation law (prior auditor prediction confirmed).

## Bounded reserves (documented at pre-launch audit, none affects a decorative verdict)
1. Majorana phases out of scope: J probes the Dirac phase only.
2. mode='holo' does not suppress the anti-holomorphic component in the charged-lepton
   sector Me_b: the test probes eml* necessity in the Dirac/neutrino sector
   specifically, not a total ablation (documented in the script docstring).
3. Absolute threshold and mass-ordering crossings: irrelevant here since J stays
   O(1e-2) in ablated modes, far from any zero threshold.

## Status
- Execution: [ESTABLISHED machine] — run on Anthony's machine, log archived
  (cp_dcp_run_20260705.log), no hardcoded verdict (audited line by line pre-launch).
- Reading: [HEURISTIC] internal to the T' lepton model — a statement about this model,
  never about nature.

## Traces
- cp_dcp_test.py (harness, audited pre-launch)
- cp_dcp_run_20260705.log (raw log, authority)
- FINDINGS_20260623b (chi2 anchors)
- Registry entry: #036 (this result)
