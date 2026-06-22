# FINDINGS 2026-06-18 -- [CONJECTURE, strong candidate] The WEAK VALUE W = <phi|A|psi>/<phi|psi> is the strongest candidate for INDEPENDENT anti-holomorphic structure found in the whole project. It is the first physical, measured object to pass ALL structural tests: cross-conjugate (holomorphic in the PAST state |psi>, anti-holomorphic in the FUTURE state <phi|, two physically independent states), mixed-derivative != 0 (past/future entangled via the overlap <phi|psi>, the 'present'), collapse phi=psi -> real expectation (lock a), AND -- crucially -- REPHASING-INVARIANT, so its anti-holomorphic phase is NOT a rephasing artefact (unlike van Cittert-Zernike's 2-point phase). The independence here is TEMPORAL (past vs future), not spatial, so it escapes the optical-coherence exhaustion argument (which covered only spatial common-origin links). Sole remaining possible lock = Project-A: post-selection is a CHOICE.
## Why this escapes the exhaustion argument
The 2nd-order exhaustion (a link = a common structure) assumed all links are SPATIAL shared-origin
(common source/apparatus in the PAST). The weak value's link is TEMPORAL: the past state |psi>
(prepared) and the future state <phi| (post-selected) are two independent boundary conditions. There
is no shared past origin -- the anti-holomorphic content is carried by the FUTURE boundary condition.
This is the conjecture's first genuine fissure. Mathematical anchor: causality = holomorphic
(Kramers-Kronig, lock b); a FUTURE boundary condition = anti-causal = anti-holomorphic (lock b mirrored).
## Tests (executed on Anthony's machine, weak_value_test.py)
W = <phi|A|psi>/<phi|psi>, qubit, A Hermitian. |psi> past (holo), <phi| future (anti).
 - cross-conjugate: W holomorphic in psi (psi* absent), purely anti-holomorphic in phi (phi absent,
   only phi*). Exactly z*conj(w) between two INDEPENDENT states. [certified]
 - mixed derivative d2W/d ps0 d fc0 != 0 : True. Past & future entangled via overlap <phi|psi>. [certified]
 - rephasing-invariant under psi->e^{ia}psi, phi->e^{ib}phi : True. The quotient cancels global phases,
   so the anti-holo phase is NOT removable by rephasing. BEATS van Cittert-Zernike (whose 2-point phase
   WAS rephasable/decorative). [certified]
 - collapse phi=psi : W = real expectation value (|Im| ~ 1e-17), reality-lock (a). The anti-holo lives
   precisely in future != past; when future=past it collapses to the real mean. [certified]
 - generic phi != psi : W genuinely complex (Im up to ~3), anti-holo alive. [certified]
## The one open lock: Project-A (post-selection as choice)
A post-selection making W real EXISTS (found by search). So one CAN choose phi to kill Im(W). The
decisive question is NOT algebraic: is post-selecting the future a GAUGE choice (decorative, like the
CP phase) or a PHYSICAL experiment (real, like preparing a state)? Arguments FOR physical: (i) by time
symmetry, post-selecting the future is no more 'a choice' than preparing the past, which nobody calls
decorative; (ii) KNOWN PHYSICS (not simulated): Re(W) and Im(W) have DISTINCT measured effects
(Aharonov-Albert-Vaidman: pointer position vs momentum), so Im(W) is not a mere reflection of Re(W).
Argument AGAINST: post-selection DISCARDS runs (active selection), so Im(W) could be a selection
artefact (the SPARC trap in temporal form). Algebra cannot decide; physics/interpretation must.
## Status
[CONJECTURE, strongest candidate to date] -- structural tests certified on Anthony's machine; the
sole open lock (Project-A post-selection) is exactly the algebraically-undecidable point, to be
weighed by physics not maths. NOT a Plateau B yet: a strong candidate, not a proof. Do NOT overclaim.
Reconnects to: lock b (causality/holomorphy) mirrored as future/anti-holomorphy; eml0 = exp - i*Arg
(pure phase) as the natural object for the overlap <phi|psi> (the 'present') [CONJECTURE image].
Files: weak_value_test.py. Arbiter = Anthony's machine (done) + open physical question (post-selection).
