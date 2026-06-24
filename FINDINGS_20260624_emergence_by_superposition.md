# FINDINGS 2026-06-24 -- [ESTABLISHED, tool structure] Emergence by superposition: additive layering of two distinct fields produces the cross-coupling; product layering stays a wall

## M-IV bench, orthogonal axis on how layers are STACKED

**Question.** Does reaching the target (cross-coupling, d_z1 d_z2b log f != 0) require an
explicit coupling term g*z1*z2b, or can it EMERGE from stacking factorized layers (each a wall)?

**Bench (layers_bench.py, symbolic-exact d = d_z1 d_z2b log f).**
  PRODUCT   exp(z1)*exp(z2b)            d = 0                       -> WALL
  PRODUCT   (z1^2 z2b)*(z1 z2b^3)       d = 0                       -> WALL
  SUM       z1 + z2b                    d = -1/(z1+z2b)^2           -> EMERGES (target-type)
  SUM       exp(z1) + exp(z2b)          d = -exp(z1+z2b)/(...)^2    -> EMERGES
  SUM       z1*z2b + 1                  d = (z1*z2b+1)^-2           -> EMERGES
  TRAP      z + zbar (one field)        full_conj invariant=True    -> REAL_TRAPPED (=2 Re z, wall)
  INTERF.   z1 + a*z2b                  d = -a/(z1+a z2b)^2         -> weight ~ a; a=0 decouples
Command: cd ~/Desktop/oxieml-star && python3 layers_bench.py

**Mechanism.** log(product) = sum of separate logs -> separates -> wall. log(sum) does NOT
separate -> the cross term survives -> d != 0. So additive SUPERPOSITION of two channels
creates the cross-coupling with NO explicit g. Multiplicative stacking never does.

**The distinction that decides wall vs emergence.** SUM of two DISTINCT fields (z1 + z2b)
emerges; SUM of one field with its OWN reflection (z + zbar = 2 Re z) is real-trapped. This is
the one-field/two-field law seen through superposition: two genuinely distinct things added ->
crossing; one thing plus its mirror -> trapped.

**Consequence for the hunt (refined target class).** The target no longer requires an exotic
explicit left-right coupling. ANY additive superposition of two distinct channels carries the
cross term: interferometers, two-path amplitudes, two-bath / two-temperature steady states,
two interfering resonances. This is a MUCH larger candidate class -- structures physicists see
everywhere (interference) but never read as cross anti-holomorphic emergence.

**Remaining lock (physical, not testable on a toy form).** The two channels must be genuinely
DISTINCT and non-reducible to one another (Naimark-irreducible). If one channel reduces to the
other's reflection, the sum collapses to z+zbar = real-trapped. The emergence is necessary, not
sufficient: the discriminant says "cross term present"; only the physical system decides whether
the two channels are truly independent.

**Status.** [ESTABLISHED] for the tool structure (symbolic-exact, reproducible, identical to
nonseparable_judge). NOT yet a physical discovery: no real system with two non-reducible
interfering channels has been fed to the judge. The chiral cell remains EMPTY.

**Symmetry ledger update.** New crossing MECHANISM mapped: additive superposition (sum) of two
distinct channels, alongside the explicit-coupling mechanism. Product/temperature/scale remain
surface buttons (walls or weight modulation only). chiral cell: still empty. Next physical hunt:
a real two-channel interfering system (non-Hermitian / out-of-equilibrium) whose two channels are
non-reducible -> feed its closed-form cross correlator to nonseparable_judge.
