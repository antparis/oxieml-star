# FINDINGS 2026-06-21b -- Audit of Kimi's physical target proposals (Task C): NEGATIVE

## Status
[ESTABLISHED] judge verdicts (sandbox, to re-run on machine) + [DERIVATION] SPARC
examination via literature. Net result: NO new solid physical candidate from Task C.

## What Kimi proposed (NOT what Milo's stale summary says)
Kimi's actual deliverable proposed: Candidate 1 non-reciprocal coupled modes (TOP),
Candidate 2 Stokeslet/Stokes flow (HIGH), Candidate 3 SUSY F-term Polonyi (MODERATE,
self-rejected), Candidate 4 Kirchhoff plate (MODERATE, "essentially Kirsch"). It
REJECTED Kerr Psi_4, Teukolsky modes, NH-QM symmetric EP, chiral p-wave vortices,
skyrmions (all module-trapped or holomorphic). NOTE: a stale Milo summary wrongly
listed "Kerr Psi_4, chiral CFT, SUSY Kahler" as Kimi's proposals -- those were the
ORIGINAL briefing leads, not Kimi's output. Kimi rejected Kerr.

## Candidate 1 -- non-reciprocal coupled modes -- REJECTED (SPARC artefact)
Formula: f = (z + sqrt(z^2 + 4*zbar))/2, eigenvalue of H = [[z, zbar],[1,0]].
JUDGE VERDICT (sandbox): anti-holomorphic, NOT module-trapped. Kimi's math claims
verified: df/dzbar = 1/sqrt(z^2+4zbar) != 0; eigenvalue eq E^2 - z*E - zbar = 0 holds.
So mathematically it IS irreducible anti.

SPARC EXAMINATION (literature, decisive): the z-bar in the return coupling is POSED
ad hoc, NOT forced by physics. Real non-reciprocal systems do NOT produce a return
coupling equal to the conjugate of the diagonal control parameter:
 - Magneto-optical non-reciprocity gives imaginary antisymmetric off-diagonal
   gyrotropy terms (ik, -ik conjugate of each other) -- broken hermiticity, not a
   zbar-dependence of the control parameter.
 - Optomechanical non-reciprocity requires m12 != m21 -- asymmetry of REAL coupling
   amplitudes, no zbar at all.
No real system poses return-coupling = zbar(control). Kimi built H = [[z,zbar],[1,0]]
specifically to manufacture an irreducible zbar. This is the SPARC trap in new clothes:
the anti comes from Kimi's hand, not from a physical equation. Replacing the return
coupling by its true physical nature (an independent parameter w) gives
(z+sqrt(z^2+4w))/2 -- a TWO-FIELD system, not an irreducible single-field anti.
=> REJECTED as encoding artefact.

## Candidate 2 -- Stokeslet -- LIKELY Kirsch in disguise (not audited on judge yet)
v = z/zbar - 1 - log(z*zbar). Kimi admits same biharmonic structure as Kirsch
(zbar*f(z) term forced by biharmonic eq). Its "physically different" defense
(fluid velocity vs elastic displacement) is the forbidden analogy move: same equation,
same zbar*f(z) term => same class, NOT a new discovery. Value = confirmation of
biharmonic universality, not a finding. (Kirsch already ESTABLISHED in project.)

## Candidates 3, 4 -- self-rejected, correctly
3 SUSY F-term: auxiliary field, not directly observable; physical observables
(gravitino mass) are module-trapped. Kimi rated "theoretical interest only".
4 Kirchhoff plate: Kimi says "essentially Kirsch". Duplicate.

## Net verdict on Task C: NEGATIVE
No new solid physical candidate. Candidate 1 is a SPARC artefact (confirmed by
literature), Candidate 2 is known Kirsch class, 3-4 self-rejected. Kimi's REJECTION
list, however, is sound (Kerr, Teukolsky, p-wave, skyrmions all correctly walled).

## Why this is a GOOD result (pipeline worked as designed)
The judge did its job (math anti confirmed on Candidate 1); the SPARC examination
caught the artefact the judge cannot see. Without the physical examination one might
have mistaken Candidate 1 for a discovery. The discipline bit: judge for math,
SPARC/physics for legitimacy, never conflate them. A diagnosed failure is a result.

## RULE reinforced
An external AI proposing a Hamiltonian with zbar written into it is the prime SPARC
risk. Always ask: is the zbar DERIVED from a physical equation, or POSED? Candidate 1
was posed. The judge says anti; only the physics says forced-vs-encoded.

## Files
new_physical_targets_proposal.md (Kimi, audited), this FINDINGS.
