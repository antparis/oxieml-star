# FINDINGS 2026-06-15 -- [HEURISTIC, positive-leaning, NOT established] g1 ablation, CORRECTED reading: equal-parameter holomorphic-only competitor recovers only OUTSIDE the fundamental domain of tau -> signal toward anti-holomorphic necessity, but test must be finalized with the FULL chi2 (neutrino + charged-lepton + delta_CP) before any verdict. Supersedes the over-claimed and the over-dismissed earlier readings.

## Why this note exists (corrects two earlier errors in the same session)
- ERROR 1 (over-claim): the first ablation (g1=0, M_e fixed) gave chi2 0.91 -> 1871 (~2000x) and was read as "anti-holo necessary, strong signal". That ~2000x is partly a PARAMETER-COUNT artifact (removing a coupling), not by itself proof of necessity. Traced in FINDINGS_20260615_ablation_g1.md / Milo bef7d7a5 -- that note's RED FLAG already warned of this.
- ERROR 2 (over-dismiss): the equal-parameter test (holo-only vs anti-only vs full, all 5 params re-minimized) gave chi2 = 0.0 for all three, which was hastily read as "test fails / anti-holo not necessary". That conclusion was PREMATURE: chi2=0 with 5 params / 4 observables can be reached at UNPHYSICAL points, so the raw number does not decide anything until one checks WHERE the minimum sits.

## The decisive check (executed on Anthony's machine, where_min.py)
Re-minimize FULL and HOLO-ONLY (equal 5 params), then inspect whether the minimum is PHYSICAL
(tau in fundamental domain |tau|>=1 & |Re tau|<=0.5; charged masses ascending):
  FULL (holo+nonholo): chi2_nu = 0.64  tau = -0.085 + 1.086i   in fundamental domain: YES
  HOLO-ONLY (tau-bar OFF): chi2_nu = 7.37  tau = 0.011 + 0.625i  in fundamental domain: NO (|tau|<1)
Also: at the PHYSICAL best-fit (fixed params), cutting the anti-holo gives chi2 ~ 210000 vs ~11 full
(no-minimization check) -- a huge asymmetry at the physical point.

## Reading (honest, hedged)
- HOLO-ONLY does NOT recover cleanly: its best reachable point lies OUTSIDE the fundamental
  domain of tau (|tau|<1), i.e. a modular-forbidden configuration. So the holomorphic-only model
  approaches the data only by leaving the physically allowed region. This is a signal TOWARD the
  anti-holomorphic term being necessary -- consistent with the 210000-vs-11 asymmetry at fixed params.
- This is NOT an established result. It is a positive-leaning HEURISTIC.

## Why NOT established yet (open issues, all real)
1. The chi2 here constrains only 4 NEUTRINO observables. The minimizer still abuses the freedom in
   beta/gamma: even the FULL fit reached chi2_nu=0.64 with an ABSURD charged sector (m_e/m_mu=0.223
   vs phys 0.0047; m_mu/m_tau=0.019 vs phys 0.0588). So fit quality on neutrinos is bought by
   wrecking charged leptons -- the test is polluted until charged-lepton observables are in the chi2.
2. Reduced multi-start (8 starts). HOLO-ONLY's 7.37 is an UPPER BOUND on its minimum, not proven global.
3. The clean test requires the FULL chi2: neutrino mixing (3 angles) + both Dm^2 + delta_CP +
   m_e/m_mu + m_mu/m_tau (>= 8 observables) so #obs > #params, removing the overfitting that lets
   any variant reach chi2=0, AND enforcing tau in the fundamental domain as a hard constraint.

## Next action (to reach a verdict)
Build the FULL chi2 (all neutrino + charged-lepton + delta_CP observables, NuFIT sigmas, charged
ratios at their published tight sigmas), restrict tau to the fundamental domain, then re-run FULL vs
HOLO-ONLY vs ANTI-ONLY at equal parameter count with strong multi-start. THEN:
  - HOLO-ONLY stays bad (in-domain) while FULL is good => anti-holomorphic term NECESSARY [candidate ESTABLISHED].
  - HOLO-ONLY recovers in-domain with sane masses => anti-holo DECORATIVE [honest negative].

## Context
Literature search (this session) found NO published paper performs this necessity/ablation test in
non-holomorphic modular flavor models; all are construct-and-fit (presence). So a clean version of
this test would be genuinely novel. Model reconstruction itself is solid: bricks 1-6 reproduce
Qu-Lu-Ding Table 2 (FINDINGS_20260615_brick56_calibrated, Milo 640e6fe8).

## Status
[HEURISTIC, positive-leaning, NOT established]. Holo-only recovers only outside the fundamental
domain (signal toward necessity), but verdict suspended until the full-observable, domain-constrained
test is run. Code verified bug-free (three modes give distinct matrices; wt2 triplet coeffs match
notebook). Single model => at most internal necessity to THIS model, not nature. No gravity / no
non-neutrino-mass link.
Files: ablation_g1.py, ablation_g1_robust.py, holo_competitor.py, where_min.py.
Arbiter = Anthony's machine + (pending) full-observable domain-constrained test.
