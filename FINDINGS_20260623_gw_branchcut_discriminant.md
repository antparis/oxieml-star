# FINDINGS 2026-06-23 — GW branch-cut discriminant: the GW front closes by CAUSALITY

**Status:** [ESTABLISHED] 7/7 judge verdicts (this machine) · [DERIVATION] causality-wall conclusion.

## What was tested

Discriminant for the Kerr/Psi4 discovery target (QNM Green-function branch cut). z == omega,
zbar == omega-bar. Question: is the branch cut (Price tail from curvature backscattering) genuine
eml* (independent log omega-bar), or eml (holomorphic in omega) + a de Rham/residue period?

## Exact command

cd ~/Desktop/oxieml-star && python3 gw_branchcut_discriminant.py; echo "EXIT=$?"

## Raw result (judge_v2, this machine) — 7/7 agree, EXIT=0

qnm_pole  1/(w-w_c)                HOL            QNM resonance pole (omega-singularity)
branch_cut_log  log(w-w_c)         HOL            Price-tail branch cut (omega-singularity)
branch_power (w-w_c)^(1/2)         HOL            fractional branch (omega-singularity)
two_pole +-m (Kerr split)          HOL            spin-split +m/-m poles (still omega-only)
power_spectrum |G|^2               REAL_TRAPPED   measured power spectrum (real)
ctrl_eml_star  log(w-bar)          ANTI           eml* signature (forbidden by causality)
ctrl_holo  w^2                     HOL            holomorphic control (eml)

## Conclusion — [DERIVATION]

The GW front closes by CAUSALITY. Every causal Green-function object (resonance poles, branch cut,
fractional branch, spin-split +-m poles) is HOLOMORPHIC in omega -> eml + de Rham/residue PERIOD
obstruction, NOT eml*. The retarded G(omega) is analytic in the upper half plane (Titchmarsh), so
poles and cuts are omega-singularities, never an independent omega-bar dependence. The measured
power spectrum |G|^2 is REAL_TRAPPED. The eml* signature log(omega-bar) is detectable by the tool
but FORBIDDEN by causality. This is the analogue of the reality lock that closed the modular front:
modular front closed by REALITY, GW front closes by CAUSALITY.

Branch cut = holomorphic-period wall (eml + de Rham period), not the chiral cell.

## Holo / anti ledger update

- eml (holo) confirmed: QNM poles, branch cut, fractional branch, spin-split poles, w^2.
- eml* (anti) reference: log(omega-bar) caught as ANTI but causality-forbidden in G.
- Walls: |G|^2 -> REAL_TRAPPED; causal G -> HOL + de Rham period (gauge-immune but holomorphic).
- ANTI forced + measurable + gauge-invariant: still ZERO. Chiral cell EMPTY.
- New closure: GW front = causality wall (Titchmarsh), structurally analogous to modular reality wall.

## Files
- gw_branchcut_discriminant.py (harness)
- this trace
