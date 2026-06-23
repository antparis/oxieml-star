# FINDINGS 2026-06-23 — Anchor: chiral-cross discriminant separates target from walls

Status: [ESTABLISHED] (executed on Anthony's machine, EXIT=0, exact Wirtinger).

## What was tested
Master discriminant d_z1 d_z2bar log f on four two-mode forms, to confirm it
separates the ENTANGLED_CHIRAL_ANTI target from separable/half-chiral walls
before launching the non-Hermitian reconnaissance.

## Command
python3 anchor_target_vs_wall.py

## Raw result
target 1+pi*log z1+phi*log z2b -> d = -GoldenRatio*pi/(z1*z2b*(pi*log z1+phi*log z2b+1)^2) -> NON-FACTORIZABLE (target)
wall product z1^pi*z2b^phi     -> d = 0 -> FACTORIZABLE (wall)
wall exp e^{i pi z1+i phi z2b} -> d = 0 -> FACTORIZABLE (wall)
holo control z1^2*z2^3         -> d = 0 -> HOL (no anti)
judge agree: pass criterion met (only row 1 non-factorizable).

## Meaning
Capability, not discovery: the cross-chiral factorization test is operational and
discriminant. The target form is a known construct; recovering its classification
sets the tool, it does not fill the chiral cell. Cell remains EMPTY.
Next: reconnaissance of a closed-form ENTANGLED_CHIRAL_ANTI in a non-Hermitian /
doubled (Keldysh) representation, measurable as a complex holonomy before modulus.
