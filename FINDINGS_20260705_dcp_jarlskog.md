# FINDINGS 2026-07-05 — delta_CP (Jarlskog) on the T' lepton model: eml* DECORATIVE

**Status:** [HEURISTIC] — single model (Qu-Lu-Ding T'), executed on Anthony's machine.
Internal necessity test only; NOT a statement about nature.

## Question
The only open neutrino door. Real observables (masses/angles) were already closed
(eml* decorative, FINDINGS_20260623b). delta_CP is the single natively-complex
observable of the sector: does cutting the anti-holomorphic part (mode='holo',
Y2pp -> c_holo only, Dirac sector MD) kill CP violation (Jarlskog J -> 0)?

## Exact command
cd ~/Desktop/oxieml-star && setsid nohup python3 -u cp_dcp_test.py > cp_dcp_run_20260705.log 2>&1

Script: cp_dcp_test.py (184 lines, sha256 09f29ce5086ea2406becb56ceaca037b7051517970fbfbd37b95cdde8b7d3cc1).
Full log: cp_dcp_run_20260705.log. Process ran to clean completion (exit "Fini").

## Raw result (this machine)
Per-mode in-domain multistart scan (21 starts each), J read at each mode's own best fit:
    full     chi2=0.91  tau=-0.0514+1.0895i  J=-8.130898e-03
    holo     chi2=0.23  tau=-0.0579+1.0125i  J=+3.021078e-02
    nonholo  chi2=0.04  tau=-0.0627+1.0352i  J=-2.685558e-02
Anchor check: chi2 per mode reproduces FINDINGS_20260623b exactly (0.91/0.23/0.04).

[L2] common tau (full best fit), modes swapped on Y2pp:
    full J=-8.130898e-03 ; holo J=-3.449908e-02 ; nonholo J=-1.323804e-02

[NULL] Re(tau)=0, full best fit otherwise: J = +0.000e+00 (exact zero).

[ORTHOGONAL AXIS] sweep Re(tau) at fixed Im/g2/beta/gamma (full best fit):
J is ODD in Re(tau) with J(0)=0 (machine check: True), peaking ~2.1e-02 at |Re tau|~0.15-0.30.

## Reading
Cutting eml* does NOT kill J: |J_holo| ~ 3.7 x |J_full|, same order, sign flip
(sign is convention/ordering dependent; magnitude is the invariant statement).
The NULL control and the odd sweep localize the CP phase entirely in Re(tau),
i.e. in q = exp(2 pi i tau) — present identically in BOTH eml and eml* pieces.
eml* is therefore NOT the carrier of CP violation; it is a co-occupant of the
same phase source. This confirms the prior auditor prediction [DERIVATION,
2026-06-23]: at the "gCP NO" best fit all couplings are real, the only phase
source is q, shared by both sectors.

Verdict: **eml* DECORATIVE for delta_CP.** Door closed.

## Audit reserves (applied, all clean)
1. Majorana phases: out of scope by construction (J is a Dirac invariant; eigh
   on M M-dagger discards Majorana phases; nothing here reads them).
2. Absolute threshold 1e-6 in holo_kills: not triggered (J_full ~ 8e-3 >> 1e-6).
3. Mass-ordering crossing between modes: would break sweep oddness; sweep is
   clean-odd at atol 1e-9 -> no spurious column swap.

## L1 (documented limit, unchanged)
Me_b (charged leptons) carries a residual anti-holomorphic Maass piece
(qb = exp(-2 pi i conj tau)) in ALL modes. The cut removes eml* from the
Dirac sector MD only. The test probes the necessity of eml* in MD — which is
the question asked — not a global removal of all anti from the model.

## Consequence
This was the LAST open door of the neutrino sector (the only natively-complex
observable). The neutrino sector is now closed at every level: real observables
(20260623b) + delta_CP (this file). Useful failure, structural not budget:
the model's CP phase lives in Re(tau), shared holo/anti — the anti cannot be
forced by CP here.

## Known separate debt (not touched here)
Stale hardcoded VERDICT lines ("anti NECESSARY") in full_chi2_test.py and
ablation_g1*.py remain false and uncorrected; separate dated-backup fix pending.
