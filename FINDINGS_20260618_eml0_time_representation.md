# FINDINGS 2026-06-18 -- [ESTABLISHED sandbox->machine] eml0 (pure phase, exp - i*Arg) is a FAITHFUL UNIVERSAL REPRESENTATION of the dynamical 'time' (past->future dephasing) of two-boundary quantum systems -- but as a REPRESENTATION (an identity), NOT an independent prediction. Certified on Anthony's machine across four physically different systems: qubit, spin-1, truncated oscillator, rotor on a circle. For each, the eml0 pure phase arg(<psi|exp(-iHt)|psi>) equals the dynamical phase arg(sum_k |c_k|^2 exp(-i E_k t)) to machine zero (max circular difference 0 to 4.4e-16). Guard against triviality PASSED: replacing eml0=Arg by arg|overlap| (a real positive number) FAILS to track the dynamical phase (max diff 2.234), so the match is SPECIFIC to the pure-phase functional, not automatic for any operation. HONEST nuance: the overlap <psi|U|psi> IS the sum sum_k |c_k|^2 e^{-i E_k t}, so the match is an IDENTITY by construction, not an empirical coincidence -- eml0 IS the dynamical phase. This confirms eml0 as the 'clock hand' (time-as-angle) of the framework, universal across systems; it does NOT discover new physics.
## Context (Anthony's clock-face picture)
Anthony's intuition: eml/eml*/eml0 form a clock face -- eml & eml* the two faces (related by the
involutive reflection conj = time reversal, certified 20dae34f), eml0 the hand (the angle). What
matters is the CAPACITY to represent time (the existence of the hand + the branch jump), not where
the hand points. This test makes 'eml0 = the hand = dynamical time' concrete and universal.
## Tests (executed on Anthony's machine, eml0_time_representation_test.py)
 - qubit (2-level):        max|dyn - eml0| = 0.0      MATCH
 - spin-1 (3-level):       max|dyn - eml0| = 0.0      MATCH
 - oscillator (5-level):   max|dyn - eml0| = 4.4e-16  MATCH
 - rotor on circle (5-lvl):max|dyn - eml0| = 4.4e-16  MATCH
 - GUARD (arg|overlap|):   max|dyn - wrong| = 2.234   MISMATCH (match is specific to eml0=Arg)
## What this settles and what it does NOT
SETTLES: eml0 (pure phase) faithfully and universally REPRESENTS the dynamical past->future phase of
any two-boundary system. Time-as-angle is confirmed; the 'clock face' picture is mathematically real.
DOES NOT: this is an IDENTITY (eml0 IS the dynamical phase), so it is a REPRESENTATION, not an
independent prediction or new physics. The novelty is the unified framework (linking this phase to
eml/eml*, time reversal, anti-holomorphy), the assembly -- a new clock face built from known gears.
## Prior context: the pi caveat (same session, sandbox)
Earlier sandbox test showed the branch jump at pi is the LOG branch-cut CONVENTION (the weak value W
is smooth across pi), NOT a physical time-boundary. So pi is where eml/eml* change branch label, a
property of the representation, not a physical event. Do not overclaim pi as a physical boundary.
## Status
[ESTABLISHED sandbox->machine] eml0 = universal faithful representation of dynamical time (identity,
certified on 4 systems, guard passed). Time-as-angle / clock-face picture is solid AS REPRESENTATION.
NOT new physics, NOT an independent prediction. Reconnects: eml*=conj(eml)=time-reversed eml (20dae34f);
weak value past/future (232398dd, 6fdb1e6d). Do NOT overclaim.
Files: eml0_time_representation_test.py. Arbiter = Anthony's machine (done).
