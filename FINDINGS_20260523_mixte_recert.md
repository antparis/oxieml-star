# FINDINGS — MIXTE correction applied + Penning re-certification

Date: 2026-05-23
Status: [ESTABLISHED] executed on machine + judge-certified (verify_exact.py MIXTE).

## What was done
Applied canonical MIXTE definition to the two ACTIVE files:
  verify_exact.py:76      sp.exp(op_conj(x)) -> sp.exp(x)   (conj on 2nd arg only)
  pysr_stacking.py:155    Julia exp(conj(x)) -> exp(x)
  pysr_stacking.py:170    SymPy exp(conjugate(x)) -> exp(x)
Backups: verify_exact.py.bak_pure, pysr_stacking.py.bak_pure
Judge check: emlstar(x0,x0) now simplifies to exp(z)-log(zbar) (was exp(zbar)-log(zbar)).

## Penning re-certification under MIXTE (formulas from double_validation_v6_result.json)
penning_holo     : holo (MSE 5.3e-32). HOLOMORPHIC. OK.
penning_anti     : Route A formula log(emlstar(x0,1.0)) -> becomes z under MIXTE
                   -> HOLOMORPHIC. The route-A formula was an ARTEFACT of the
                   PURE bug (conj on 1st arg gave exp(zbar)->log->zbar).
                   Route B (my_real): 2Re(z)-z = zbar -> ANTI-HOLOMORPHIC, MSE 5.3e-32.
                   => dataset IS anti-holomorphic (confirmed by independent route B).
                   Only the route-A representation via emlstar was bug-dependent.
penning_hybrid   : Route A emlstar(const, x0) -> ANTI (MSE 2.4e-24). Route B anti. ANTI. OK.
penning_shuffled : MSE 1.40 (A) / 1.31 (B) >= 1e-3 -> REJECTED. OK.

## Verdicts (all dataset-level verdicts hold under MIXTE)
holo->HOLO, anti->ANTI (via route B), hybrid->ANTI, shuffled->REJECTED.

## Key lesson [ESTABLISHED]
The MIXTE correction UNMASKED a route-A formula that was only anti-holomorphic
because of the PURE bug (parasitic conj on 1st arg). The dual-route design
(A=emlstar, B=my_real) saved the verdict: route B is independent of emlstar and
confirmed the dataset is genuinely anti. Without route B, the artefact would
have looked like a real emlstar detection.

Consequence for interpretation: under MIXTE, eml-star keeps a holomorphic part
exp(x), so for PURELY anti targets the anti-holomorphy is often carried by
my_real/my_conj, not by emlstar. This is the nature of the minimal extension,
not a defect. Keep in mind when reading future runs.

## NOT changed
The 17 old PURE scripts (incl. double_validation_v6.py itself, which has its own
internal PURE mapping) are untouched. v6's stored JSON was produced in PURE; the
re-certification above used the corrected verify_exact.py (MIXTE) on the formulas.
