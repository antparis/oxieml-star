# FINDINGS 2026-06-18 -- [ESTABLISHED sandbox->machine] The eml/eml* pair ENCODES the past/future symmetry, which reclassifies the weak-value Project-A caveat. eml* is defined from eml by CONJUGATION, and in QM complex conjugation IS time reversal (T anti-unitary). Certified on Anthony's machine: swapping past<->future (psi<->phi) equals conjugation equals the eml<->eml* operation [wv(phi,psi)==conj(wv(psi,phi)) for all samples]. The jump eml<->eml* is an INVOLUTION (conj o conj = identity), i.e. a reflection with NO intrinsic direction: eml->eml* and eml*->eml are the SAME operation. So holo(past) and anti(future) are CO-FUNDAMENTAL by construction of the pair. Consequence: the 'does Im(W) exist before the sorting?' worry is ill-posed -- it secretly privileges the past. Anti-holo is introduced by post-selection EXACTLY as holo is introduced by preparation; asking 'which exists before' presupposes a time arrow. The asymmetry that fed the doubt is in the time-oriented QUESTION, not in the object.
## Tests (executed on Anthony's machine, eml_time_symmetry_test.py)
 - W holomorphic in psi (past, bare), anti-holomorphic in phi (future, phi* only). [structure]
 - swap psi<->phi == conjugation == eml<->eml* : wv(phi,psi)==conj(wv(psi,phi)) : True. [certified]
   => the eml<->eml* jump IS the past<->future / time-reversal operation.
 - involution: conj o conj = identity : True. [certified] The jump is a REFLECTION with no direction;
   eml->eml* and eml*->eml are the same operation. The 'hand' (anti vs holo) emerges from the
   reflection; the DIRECTION (which side is 'future') is an external choice (our time arrow).
 - pre-postselection state depends only on psi (holo), d/d(phi*)=0 (no anti before sorting), BUT
   pre-preparation there is no psi (no holo before preparing). Symmetric => 'before' question ill-posed.
## What this settles and what it does NOT
SETTLES (level 1, laws symmetric): holo(past) and anti(future) are co-fundamental by the very
construction of eml/eml*. Internal-coherence argument: accepting eml (holo, past/preparation) as
real forces accepting eml* (anti, future/post-selection) as equally real, on pain of breaking the
founding symmetry. The 'lottery / selection artefact' worry is dissolved: it was an asymmetric question.
DOES NOT SETTLE (level 2): whether NATURE realizes post-selection as physical. That is the quantum
measurement problem (a century-old open problem), out of scope. This is internal coherence of the
framework, NOT an external proof.
## Status
[ESTABLISHED sandbox->machine] for the structural facts (conjugation=time reversal=eml<->eml* swap;
involution; ill-posedness of the 'before' question). The Plateau-B claim for the weak value remains
[CONJECTURE, strong]: support is now serious and convergent (T-odd 6fdb1e6d; decoherence preserves /
dissipation kills 6fdb1e6d; symmetry of the eml/eml* pair, here), and nothing in the STRUCTURE opposes
it -- the only remaining obstacle is the measurement problem, an open question of physics, not a flaw
of the framework. Do NOT overclaim: strong candidate, not a proof.
Reconnects: eml*=conj(eml)=time-reversed eml; eml0=exp-i*Arg (pure phase) = overlap <phi|psi> = present.
Files: eml_time_symmetry_test.py (this); weak_value_test.py (232398dd); weak_value_pointer_test.py (6fdb1e6d).
Arbiter = Anthony's machine (done) + the measurement problem (out of scope).
