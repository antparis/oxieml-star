# FINDINGS 2026-06-22f -- Two-band superconductor candidate FAILS the SPARC test (observable wall)

## Status
[ESTABLISHED] negative result (sandbox judge corrected + literature, to replay on machine).
The two-band superconductor composite-vortex candidate (best physical candidate since
Kirsch) FAILS the SPARC test: its anti-holomorphy lives in the SUM Psi1+Psi2 (a mathematical
construction), but every NATIVE physical observable (interband phase difference, Leggett
mode, coupling energy) is real-trapped or module-trapped. The z̄ was POSED by our writing,
not FORCED by physics. New wall (observable wall, distinct from the galaxy encoding wall).

## Two preceding confirmations this session
1. Candidate survives the FIXED judge (FINDINGS 0622e): the sum (z/|z|)^n1+(z/|z|)^n2 with
   n1!=n2 is genuinely anti (R/f depends on z,zbar, unlike |z|^(is) which had R/f=0). So the
   anti of the SUM is real, not a blind-spot artefact.
2. Literature (web_search 2026-06-22): states with different winding L1!=L2 EXIST and are
   STABLE (arXiv:1205.2022 mesoscopic, arXiv:2408.13584 rings); fractional vortices OBSERVED
   experimentally (SQUID imaging, Nb bilayer). So reservations 1 (eta=0) and 3 (stability)
   are partially lifted -- these states are physically realizable.

## The decisive SPARC test on the NATIVE observable (the missing piece)
The physical observable in two-band SC is NOT the sum Psi1+Psi2. What is measured is the
INTERBAND PHASE DIFFERENCE Phi1-Phi2 (Leggett mode, seen in MgB2 Raman; arXiv:1512.08121
shows the mode lives in Phi1-Phi2), the fractional flux, vortex-core states. With
Phi_j = n_j*theta, theta=arg(z)=(1/2i)log(z/zbar):
  [1] Phi1-Phi2 = dn*theta (the measured angle)      -> REAL-TRAPPED (= conj, mirror-locked)
  [2] exp(i(Phi1-Phi2)) = (z/zbar)^(dn/2)            -> MODULE-TRAPPED (reducible)
  [3] cos(Phi1-Phi2) (coupling energy, free energy)  -> REAL-TRAPPED (mirror-locked)
  [4] (reminder) the SUM Psi1+Psi2 we tested before  -> anti-holomorphic
Every native observable is real-trapped or module-trapped. Only the non-observable SUM is anti.

## Verdict
The candidate FAILS SPARC. Subtler than the galaxy wall: order parameters ARE natively
complex (not a forced encoding), but the observable carrying the anti (the sum) is NOT a
physical observable -- it is our choice of writing. What nature measures (phase differences,
flux, energies) is real or reducible. The z̄ is in our paper, not in the physics. Answers the
project's core test "is z̄ derived by physics or posed?" -> POSED here.

## Honest counter-note (do not over-bury)
One narrow theoretical escape remains: a DIFFERENT native complex observable (e.g. a two-point
correlation function, or a vortex-core observable) could in principle carry the winding
difference irreducibly. But the standard observables (phase difference, Leggett, energy) are
all mirror-locked/module. The escape is narrow and speculative; not pursued now.

## Walls status after this session
- Galaxies/SPARC, MHD-Hall: sealed (real-data encoding/mirror walls).
- Aharonov-Bohm real-power, inverse-square |z|^(is): sealed (module-trapped).
- Two-band superconductor: NEW wall -- math anti in non-observable sum; native observables
  mirror-locked/module. Best physical candidate since Kirsch now downgraded.

## Standing
The chiral cell remains empty: no physical system yet has FORCED, transcendental,
non-reducible anti-holomorphy in a measurable observable. Genuine physical anti so far:
Landau elasticity, Kirsch (traction-free boundary) -- both algebraic, both in genuine
physical fields. The transcendental forced case is still unfound.

## Files
superconductor_retest_fixed_judge.py (survives fixed judge), this FINDINGS.
Builds on FINDINGS_20260621e (original candidate), 0622e (fixed judge).
