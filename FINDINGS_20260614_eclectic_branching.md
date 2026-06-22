# FINDINGS 2026-06-14 -- Eclectic [648,533] branching Delta(54)<->T' EXPLICIT (GAP). Stage 2 core groundwork.

## What this is
Explicit branching table of the eclectic group [648,533] simultaneously to its Delta(54)
(traditional flavor) and T'=SL(2,3) (modular, level 3) subgroups. This is the correspondence
needed to assign each Bora field its T' partner. File: GAP /tmp/branching_clear.g.

## Result (executed on Anthony's machine, GAP 4.12.1) -- [ESTABLISHED-userrun]
Eclectic [648,533] small irreps decompose as (Delta(54) irrep) x (T' irrep):
- ECL #1,2,3 (dim1) -> Delta54 1_1 x { T' 1, 1', 1'' }   (singlet dressed by the 3 T' singlets)
- ECL #4,5,6 (dim2) -> Delta54 2_1 x { T' 2, 2', 2'' }   (Bora's doublet dressed by 3 T' doublets)
- ECL #7   (dim3) -> Delta54 1_1 x T' 3                  (a Delta54 SINGLET is a T' TRIPLET)
- ECL #8-13 (dim3) -> Delta54 triplet (3_1 or 3_2) x { T' singlet + T' doublet }
Delta54 irreps idx: 1,2=singlets; 3-6=doublets; 7-10=triplets.
T' irreps idx: 1,2,3=singlets; 4,5,6=doublets; 7=triplet.

## KEY consequence (the real constraint)
In the eclectic group the Delta(54) and T' representations are COUPLED, not free: fixing a
field's Delta(54) irrep constrains its T' irrep. Bora's content is defined by Delta(54) irreps
{1_1,1_2, 2_1, four triplets}; the eclectic embedding then DICTATES the T' assignments, hence
the MODULAR WEIGHTS of the Maass forms that can couple them. Notably Bora's MATTER triplets
(3_1,3_2) carry T' {singlet + doublet} content (ECL #8-13).

## Status: [ESTABLISHED-userrun] for the branching table ONLY
The group-theoretic correspondence is certified. This is groundwork, NOT the invariant test.

## NEXT (cold session, the actual Stage 2 core) -- has TWO components, second is NOT GAP
1. (GAP, group level) Assign each Bora field its T' irrep via this table; check the tensor
   products [matter x matter] and [matter x matter x Yukawa] contain the trivial T' invariant.
2. (modular forms, NOT GAP) Check the level-3 polyharmonic Maass-form multiplets (Qu-Lu-Ding
   2506.19822: weights, 1/1'/3 even, 2-hat odd, E2-hat) supply that invariant WITH THE CORRECT
   TOTAL MODULAR WEIGHT. This requires building the actual Maass forms, outside GAP.
WARNING: testing only component 1 (group) and concluding "it works" would be a FALSE POSITIVE
-- the modular-weight component 2 is essential. Do NOT shortcut.
KILL CRITERION unchanged: no invariant / no weight-consistent Maass form for the 2_1 + triplet
sector -> quasi-eclectic fallback (Chen 2108.02240) or no-go.
