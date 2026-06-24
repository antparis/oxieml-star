# FINDINGS 2026-06-24 -- [DERIVATION] Audit of ChatGPT meta-methods; rank-3 Jordan = same cell; discriminant alone insufficient

## Audit of ChatGPT's 7 proposed meta-methods

All 7 converge on the non-Hermitian / Jordan-block sector -- our current verdict, reached
independently. External convergence is a signal, NOT a proof (convergence != proof).

Reformulations of existing acquis (useful vocabulary, no new door):
  #1 representation incompatibility = our Naimark/unpaired lock in categorical language; converges
     on the indecomposable module = the Jordan block.
  #3 factorization obstructions = our layer-3 / forcing_filter, verbatim ("discriminant then minimal system").
  #4 forbidden witness = the cross discriminant IS already this witness. Redundant.
  #6 impossibility theorem = what we do by sieving; real value: a precise theorem to prove
     ("tensor product of independent sectors => factorizable"), upgrading our single-field law.

Conceptually new but speculative:
  #2 obligatory channel = breaking crossing symmetry to force a single OPE channel with log(z-bar).
     Non-explored angle, but NOT reducible to a closed form now; still points to the non-Hermitian door.

Concrete testable contributions:
  #5 log*log cross term -- tested (chatgpt_probes.py): with "1+" the additive form is non-factorizable;
     the log*log term keeps it non-factorizable. Confirms the target form, under the pairing caveat below.
  #7 extended Jordan (rank >= 3) -- reduced below.

Revised ranking by real utility: #7 > #6 (as a proof program) > #2 > #5 > {#1,#3,#4} reformulations.
(ChatGPT ranked #1 first; demoted because it is our Naimark lock renamed, converging on the known candidate.)

## Rank-3 Jordan reduction (jordan3_cross.py)

Command: cd ~/Desktop/oxieml-star && python3 jordan3_cross.py

EXACT: order-3 non-reciprocal Jordan block, 1 eigenvector/3 (non-diagonalizable); cross propagator
P[0,2] = -g^2 t^2 exp(-i lambda t)/2 -> t^2 factor -> log^2 (higher-rank LCFT).
Mixed-argument forms log(z1-z2b), log^2(z1-z2b), 1+a*L+c*L^2 : all disc != 0 AND full_conj non-invariant.

VERDICT: rank-3 -> log^2 lands in the SAME non-factorizable + non-paired cell as rank-2. It ENRICHES
the existing target cell (higher rank), it does NOT open a new door. Consistent with global convergence.

## KEY result: the discriminant alone is NECESSARY, NOT sufficient

Counterexample (exact, branch-independent): f = 1 + a*log(z1) + conj(a)*log(z2b)
  - disc = d_z1 d_z2b log f != 0   -> non-factorizable
  - full_conj-invariant = True     -> REAL_TRAPPED = WALL
So d != 0 does NOT imply target. The pairing test (full_conj) is MANDATORY alongside the discriminant.
The non-pairing comes robustly from a MIXED additive argument (z1 - z2b), whose argument changes under
the holo<->anti swap; conjugate-paired coefficients on a separated/product form stay walls.

## Debt on our own tool

layers_bench.py (committed 813743b) tests ONLY the discriminant. The counterexample above shows it has
the SAME blind spot as ChatGPT: it would mislabel 1 + a*log z1 + conj(a)*log z2b as target-type.
ACTION: extend layers_bench.py with the full_conj pairing test (target = disc != 0 AND non-paired).

## Status

Rank-3 result and counterexample [ESTABLISHED on certification] -- exact algebra + discriminant +
full_conj, to confirm with nonseparable_judge / nh_lcft_pairing_judge on the machine. Audit ranking
[DERIVATION]. Chiral cell still EMPTY. Bottleneck unchanged: a real device's closed-form correlator.

## Symmetry ledger update

Target criterion sharpened: non-factorizable (disc!=0) AND non-paired (full_conj) -- BOTH required.
Rank-3 Jordan = same cell, richer (log^2). layers_bench debt logged. Walls unchanged. Cell empty.
