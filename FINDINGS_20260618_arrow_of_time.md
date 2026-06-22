# FINDINGS 2026-06-18 -- [ESTABLISHED (symbolic) + NEGATIVE RESULT/DERIVATION] The reversible/irreversible boundary (the arrow of time) does NOT have a holo/anti signature that the judge detects. The eml/eml* framework captures the past/future symmetry of the REVERSIBLE phase, not thermodynamic irreversibility. Symbolic judge result (SymPy exact, t and tbar independent, the verify_exact.py method): (1) the AMPLITUDE <phi|e^{-iHt}|psi> = sum_k c_k e^{-iE_k t} is HOLOMORPHIC in time, d/dtbar = 0 (this is the eml0 object, 5e3b76ff); (2) the EXPECTATION Tr(A e^{-iHt} rho e^{+iHt}) is NOT holomorphic, d/dtbar != 0, because the U..Udagger sandwich brings in the conjugate (backward) branch carrying tbar; (3) GUARD: the tbar-dependence sits specifically in the OFF-DIAGONAL (coherence) terms (diagonal/populations carry e^{-iE(t-tbar)}). KEY POINT (why this is a negative result, not the arrow): this t/tbar split holds ALREADY for UNITARY (reversible) evolution. It is the forward/backward (past/future) phase structure -- the same holo=past / anti=future we already had for the weak value -- NOT irreversibility. The genuine arrow of time is PURITY LOSS Tr(rho^2) decreasing (information leaking to the environment): an entropic, T-odd, non-recoverable quantity that the holo/anti language does NOT capture. So: do NOT conflate 'the expectation carries tbar' (true even for reversible dynamics) with 'arrow of time'.
## Convention assumed (stated honestly, not a derived fact)
The t/tbar assignment rests on the convention that the bra / backward branch carries tbar (conjugate
= time reversal). This is consistent with the whole framework (conj = time reversal, future carries
the anti part, 20dae34f) but is an ASSUMED convention, not something derived from first principles here.
## Tests (sandbox, symbolic exact -- numeric attempts were buggy, see note)
 - [1] amplitude d/dtbar = 0 -> HOLOMORPHIC in time. [ESTABLISHED symbolic]
 - [2] expectation (sandwich) d/dtbar = I*(E1*c2*exp(...)+E2*c1*exp(...))*exp(...) != 0 -> NOT holo. [ESTABLISHED symbolic]
 - [3] GUARD: off-diagonal (coherence) terms carry the tbar-dependence; this is the NO the test can say. [ESTABLISHED symbolic]
 - reversibility (numeric, the one numeric test that was sound): unitary recovers rho_0 to 1e-16;
   Lindblad fails to recover (~0.21) -- the arrow. Purity: unitary 1.0000 preserved; Lindblad 1.0000->0.95 lost. [HEURISTIC numeric]
## Auditor note (three buggy numeric attempts -> switched to symbolic)
My numeric Wirtinger derivative was structurally wrong: perturbing a complex-valued f by complex t
gave |df/dtbar|=|df/dt| (a broken split). Two further numeric attempts had a broken monotonicity test
and a wrong object (expectation instead of amplitude). The repeated bugs were themselves a signal: I
was trying to make holo/anti say something it does not. Resolved by using the exact symbolic judge
method (t,tbar independent), which gives a reliable verdict and a clean NO on the expectation.
## What this settles (the honest answer to 'does the arrow have a holo/anti signature?')
NO. The judge sees the reversible past/future PHASE structure (amplitude holomorphic, expectation
not), but the irreversible arrow of time lives in PURITY/ENTROPY, a separate quantity outside the
holo/anti dimension. This DELIMITS the framework: it is about time SYMMETRY (reversible), not the
arrow of time (irreversible). A clean negative result that guards against overclaiming eml/eml* as
an account of irreversibility or of the measurement problem's 'why'.
## Status
[ESTABLISHED symbolic] amplitude holo / expectation non-holo in time (exact judge). [NEGATIVE
RESULT/DERIVATION] the arrow of time is NOT a holo/anti signature; it is purity loss (entropic).
Reconnects: eml0 time-as-angle (5e3b76ff); eml/eml* time-reversal symmetry (20dae34f); weak value
past/future (232398dd). Measurement-problem 'why' remains open and is NOT testable by simulation.
Files: (symbolic test in sandbox; reproducible via judge_v2 with t,tbar). Arbiter = SymPy judge.
