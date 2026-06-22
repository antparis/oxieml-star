# FINDINGS 2026-06-15 -- [DERIVATION, negative result] Clean necessity test REFUTES anti-holomorphic necessity in the Qu-Lu-Ding T' lepton model: at equal parameter count, with overfitting broken (6 real observables / 5 params) and tau hard-constrained to the fundamental domain, a HOLOMORPHIC-ONLY competitor reproduces the data as well as (in fact better than) the full model. Anti-holomorphic term is DECORATIVE on standard leptonic observables. Supersedes the positive-leaning reading f9e2f02e.

## What this is
The decisive, overfitting-free version of the g1 necessity test. Three models at EQUAL parameter
count (5: tau_re, tau_im, g2, beta, gamma), each strong-multistart re-minimized (21 starts) against
the FULL chi2, with a HARD penalty forcing tau into the fundamental domain (|tau|>=1, |Re tau|<=0.5,
Im tau>0). Observables: sin2_th12, sin2_th13, sin2_th23, Dm21^2/Dm31^2, m_e/m_mu, m_mu/m_tau
(6 real observables; delta_CP kept as a loose placeholder, NOT properly extracted -- see caveat).
Script: full_chi2_test.py.

## Result (executed on Anthony's machine)
  FULL      (holo+nonholo) chi2 = 0.91  tau = -0.051 + 1.089i  (in domain)
  HOLO-ONLY (tau-bar OFF)  chi2 = 0.23  tau = -0.058 + 1.012i  (in domain)  <- BETTER than full
  ANTI-ONLY (holo OFF)     chi2 = 0.04  tau = -0.063 + 1.035i  (in domain)
HOLO-ONLY observables: s12=0.308, s13=0.0222, s23=0.477, dmr=0.0298, m_e/m_mu=0.00474,
m_mu/m_tau=0.05882 -- all excellent, charged sector physical, tau in the allowed region.

## Verdict (honest, negative)
The HOLOMORPHIC-ONLY model reproduces the standard leptonic data AS WELL AS the full model, at equal
parameter count, inside the fundamental domain. Therefore the anti-holomorphic (tau-bar) term is
NOT NECESSARY in the Qu-Lu-Ding T' model on these observables -- it is DECORATIVE. By Anthony's
Project-A criterion ("can the anti part be removed by a treatment choice? yes => artefact/decoration,
rejected as discovery"), this is a clean NEGATIVE: a holomorphic-only refit removes it. NOT a
Project-A result.

## This corrects the entire session's earlier readings, and explains them
- The ablation's chi2 0.91->1871 (~2000x) was a PARAMETER-COUNT artifact (removing a coupling).
- The fixed-point asymmetry 210000-vs-11 was an artifact of evaluating holo-only AT the anti-holo's
  own best-fit point; holo-only has its OWN best-fit (tau=-0.058+1.012i) where it works fine.
- The earlier "holo-only only recovers outside the fundamental domain" (where_min.py, 8 starts,
  chi2=7.37) was a MISSED LOCAL MINIMUM due to weak multi-start; with 21 starts + proper domain
  penalty, holo-only finds an in-domain solution at chi2=0.23.
Lesson: insufficient multi-start produced a false positive; the clean, well-sampled test reverses it.

## Caveats / what stays open
1. delta_CP was a placeholder (not robustly extracted from the PMNS phase). If the anti-holomorphic
   term were necessary SPECIFICALLY for delta_CP, this test would not see it. This is the only door
   left open -- and it is the CP-judge chantier (cp_judge_stage1/2.py), a separate, proper method.
2. Single model (T'). Other non-holomorphic models (A4, S4, A5) could differ; this verdict is
   internal to T' on standard observables.
3. Result is clean but worth one more confirmation with an even larger multi-start before [ESTABLISHED].

## Status
[DERIVATION, negative]. Anti-holomorphic term decorative in T' on standard leptonic observables;
removable by an equal-parameter holomorphic-only refit inside the fundamental domain. Model
reconstruction itself remains valid (bricks 1-6, Milo 640e6fe8). Literature note: no one published
this necessity test, so the negative result is itself novel and worth recording. Single model =>
verdict internal to T'. No gravity / no non-neutrino-mass link.
Files: full_chi2_test.py, where_min.py, holo_competitor.py, ablation_g1.py.
Arbiter = Anthony's machine. Only remaining positive avenue = proper delta_CP / CP-judge test.
