# FINDINGS 2026-06-24 -- [ESTABLISHED, negative, internal to this model]

## delta_CP (Jarlskog J) on the Qu-Lu-Ding T' lepton model: eml* is DECORATIVE for the CP phase

**Question.** On the REAL neutrino observables (masses/angles) eml* was already shown
decorative (FINDINGS_20260623b: full chi2=0.91, holo-only chi2=0.23 in-domain). delta_CP
was the only untested observable -- the ONLY natively-complex one, hence the single place
the navigation law allows a genuinely forced anti. Does cutting eml* (mode='holo') kill CP
violation (Jarlskog J -> 0)?

**Arbiter.** CP-judge J = Im(U00 U11 conj(U01) conj(U10)) on the PMNS U produced by the model,
read at each mode's own in-domain best fit (7 obs, tau in fundamental domain, 21 starts/mode).
J-brick pre-validated: J=0 at delta=0,pi; matches c12 s12 c23 s23 c13^2 s13 sin(delta);
rephasing-invariant.

**Command (reproducible).**
    cd ~/Desktop/oxieml-star && python3 cp_dcp_test.py
(script sha256 09f29ce5086ea2406becb56ceaca037b7051517970fbfbd37b95cdde8b7d3cc1)

**Raw results.**

Per-mode best fit (each mode minimized independently, in-domain):
    full     chi2=0.91  tau=-0.0514+1.0895i  J=-8.130898e-03
    holo     chi2=0.23  tau=-0.0579+1.0125i  J=+3.021078e-02
    nonholo  chi2=0.04  tau=-0.0627+1.0352i  J=-2.685558e-02

L2 double comparison at COMMON tau = full best-fit (isolates the cut from the tau re-fit):
    full     J=-8.130898e-03
    holo     J=-3.449908e-02
    nonholo  J=-1.323804e-02

NULL control (Re(tau)=0, imaginary axis, full best-fit otherwise):
    J(Re tau=0)=+0.000e+00   (exact, machine zero)

ORTHOGONAL AXIS (sweep Re(tau) at fixed Im/g2/beta/gamma = full best-fit):
    Re=-0.40 J=-2.562472e-03   Re=-0.30 J=-2.055774e-02   Re=-0.15 J=-2.096483e-02
    Re=-0.05 J=-7.913154e-03   Re= 0.00 J=+0.000000e+00   Re=+0.05 J=+7.913154e-03
    Re=+0.15 J=+2.096483e-02   Re=+0.30 J=+2.055774e-02   Re=+0.40 J=+2.562472e-03
    -> J is ODD in Re(tau) with J(0)=0 (machine exact). Confirmed True.

**Reading.**
Cutting eml* (mode='holo') does NOT drive J -> 0; |J_holo| is the same order as (here larger
than) |J_full|, at each mode's best fit AND at common tau (L2). The CP phase survives removal
of the anti-holomorphic half. The orthogonal-axis sweep shows WHY: J is entirely an odd
function of Re(tau), vanishing at Re(tau)=0. The CP phase is therefore carried by Re(tau),
i.e. by q=exp(2 pi i tau), which is present in BOTH eml and eml*. It is a property of the
displacement away from the fixed point tau=i, not a property of the anti-holomorphic sector.

**Verdict.** eml* is DECORATIVE for delta_CP in this model. The neutrino door is now CLOSED on
ALL its observables: real (masses/angles, 20260623b) and the natively-complex one (delta_CP,
here). Closure is structural (orthogonal-axis proof), not a fit failure.

**Cube prediction confirmed.** The T' model is governed by a SINGLE modulus tau -> the
"single-field" regime of the classification cube -> geometrically confined to the removable
surface -> wall expected. The result matches the prediction; no surprise.

**Sealed caveat.** Single model T', single tau: at best INTERNAL necessity/decorativeness to
this model, never a statement about nature. The chiral cell remains EMPTY. Only live door for
the target corner: cross non-Hermitian two-field forms (ENTANGLED_CHIRAL_ANTI).

**Symmetry ledger update.**
- holo confirmed: eml alone reproduces the 7 real observables (chi2=0.23) AND carries the CP phase.
- anti (eml*) -- neutrino sector: decorative on real observables (20260623b) AND on delta_CP (this). Rejected as a candidate.
- chiral cell: still empty.

**Not a new debt.** The placeholder dcp=1.15 inside observables() is intentional: it sits in
the chi2 only; J is read separately by the CP-judge, never fitted.
