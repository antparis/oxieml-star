# FINDINGS 2026-06-14 -- Eclectic [648,533] group-theoretic INVARIANTS exist for full Bora content. Stage 2 core, component 1 (group) PASSED.

## What this is
Component 1 of the Stage 2 core test: do the eclectic [648,533] tensor products of Bora's
field content contain the trivial invariant (i.e. can mass/Yukawa terms exist at the
group-theory level)? File: GAP /tmp/eclectic_invariants.g + /tmp/eclectic_invariants2.g.

## Result (executed on Anthony's machine, GAP 4.12.1) -- [ESTABLISHED-userrun]
Trivial irrep = ECL#1. Pair products containing trivial (direct mass terms):
  ECL#1xECL#1, ECL#2xECL#3, ECL#4xECL#4, ECL#5xECL#6, ECL#7xECL#7, ECL#8xECL#9,
  ECL#10xECL#11, ECL#12xECL#13.
KEY: ECL#4 = Bora doublet 2_1 (dressed). ECL#4 x ECL#4 contains trivial -> the
problematic 2_1 sector HAS a mass invariant. The sector that could have killed the
path survives.

Doublet sector triple invariants 2_1 x 2_1 x X (X = candidate flavon/Maass-form rep):
  X = ECL#1,2,3 (T' singlets) OR X = ECL#7 (Delta54 singlet dressed by T' TRIPLET).
Triplet matter sector (ECL#8-13) x X: closes with T' singlets (ECL#1,2,3) or T' triplets.

## What this PROVES and what it does NOT
PROVES [ESTABLISHED-userrun]: group-theoretic invariants exist for ALL Bora sectors
(singlets, doublet 2_1, matter triplets). The eclectic embedding admits mass/Yukawa
couplings. The test gives the EXACT T' representations a Maass form must carry to close
each invariant (precise target list).
DOES NOT prove: that actual level-3 polyharmonic Maass forms realize these invariants
WITH THE CORRECT TOTAL MODULAR WEIGHT. "Lock accepts a key of this shape" =/= "key exists
in the level-3 Maass-form keyring". This is component 2, NOT done, NOT GAP.

## Status
Component 1 (group invariants): [ESTABLISHED-userrun] PASSED.
Component 2 (Maass-form weight saturation): OPEN, requires modular-forms tool
(Python/SageMath, Qu-Lu-Ding 2506.19822 level-3 multiplets), NOT GAP.
Overall Stage 2 core: 1 of 2 components passed. Path ALIVE, not yet confirmed.

## NEXT (the final component)
Build the level-3 polyharmonic Maass-form multiplets; check that, for the target T'
reps identified above (singlets and T'-triplet via ECL#7), a Maass form of consistent
total modular weight exists to saturate the 2_1 and triplet invariants.
KILL CRITERION: no weight-consistent Maass form for the 2_1 + ECL#7 sector -> quasi-eclectic
fallback (Chen 2108.02240) or no-go.
