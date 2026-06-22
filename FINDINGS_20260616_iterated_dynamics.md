# FINDINGS 2026-06-16 -- [ESTABLISHED on these forms] Iterated anti-holomorphic dynamics splits into two regimes. PURE anti-holo iteration (Tricorn) => PARITY LOCK (e): alternates pure-ANTI (odd) / pure-HOLO (even), mixed derivative = 0 throughout, never independent z-bar. MIXED iteration (holo+anti per step) => algebraic entanglement (mixed != 0, genuine z^2*zbar coupling, not real, not separable) NOT reducible to locks (a)/separability, BUT reducibility to spinor-lock (d) depends on PHYSICAL realization, which algebra cannot decide. Anthony's intuition on the Tricorn ("very particular data") localized correctly: iterated dynamics is a genuinely new regime relative to the four static locks.
## Context
The four conjecture locks (a reality, b causality, c discrete, d spinor) all concern STATIC objects
(field, response, eigenvalue, Bloch state). Iterated dynamics (a process, not a frozen field) was
untested. The Tricorn z -> conj(z)^2 + c is the canonical anti-holomorphic dynamics.
## Results (executed on Anthony's machine, iterated_dynamics_test.py)
(1) PURE: w -> conj(w)^2 + c. Iter 1 ANTI, iter 2 HOLO, iter 3 ANTI, iter 4 HOLO; mixed d2/dz dzbar
    = 0 at every iteration. => two conjugations cancel pairwise; the state is purely holo or purely
    anti by PARITY of composition. NEW LOCK (e) PARITY: pure anti-holo iteration never produces
    independent z-bar, it alternates. (The Tricorn, Anthony's case, falls under lock e.)
(2) MIXED: w -> conj(w)^2 + w + c. Iter 1 separable (mixed=0), iter 2 mixed d2/dz dzbar = 4z != 0.
    Reducibility checks on iter 2:
      reality-lock (a)? f == conj(f): FALSE  => not a disguised real quantity (unlike |w|^2).
      separable? mixed==0: FALSE            => genuine cross-coupling, term 2*z^2*zbar.
    => MIXED iteration creates algebraic z/zbar entanglement that is NOT reducible to (a) or to a
       separable holo+anti split. Whether it falls under spinor-lock (d) depends ENTIRELY on the
       PHYSICAL realization: if z,zbar come from a real (x,y) substrate => lock d (decorative); if
       z,zbar are genuinely independent (native-complex variable) => potentially NEW irreducible
       structure. ALGEBRA CANNOT DECIDE -- only a physical mixed-dynamics system can.
## Consequence (the sharpened map)
If a Plateau-B (anti-holo necessity in measured nature) exists, this localizes its form: a MIXED
iterated dynamics carried by a NATIVELY-COMPLEX variable (z,zbar genuinely independent, not a real
substrate). The deciding test is then physical, not algebraic: is the substrate real (=> lock d) or
natively complex (=> possibly new)? OPEN QUESTION: does a real physical system with mixed iterated
anti-holomorphic dynamics on a native-complex variable exist? Pure anti-holo dynamics is closed
(lock e). Static objects are closed (locks a-d).
## Status and limits
[ESTABLISHED on these forms] -- the algebra is certified on Anthony's machine. But these are
THEORETICAL FORMS (abstract iterations), the known side of the conjecture. They do NOT exhibit a
measured physical system; until one is identified, mixed iterated dynamics stays "theoretical form".
Lock (e) parity is established for pure anti-holo iteration. The mixed-iteration irreducibility is a
[CONJECTURE]-level open lead, decidable only by physical realization.
Files: iterated_dynamics_test.py. Arbiter = execution on Anthony's machine (done) + physical question (open).
