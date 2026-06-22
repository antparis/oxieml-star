# FINDINGS 2026-06-16 -- [CONJECTURE] Anti-holomorphic structure (independent, continuous z-bar dependence) appears in THEORETICAL FORMS but never as independent information in RAW MEASURED observables of nature. In measured data, z-bar is always a MIRROR: forced either by reality (real field => Hermitian-locked) or by causality (Kramers-Kronig-locked). Genuine "native complexity" in measured systems is carried HOLOMORPHICALLY (poles, branch cuts, windings) or DISCRETELY (chirality sign, monodromy), not by independent z-bar.

## Statement of the conjecture
The eml-star tool tests for a CONTINUOUS, INDEPENDENT dependence on z-bar (Wirtinger d/d(zbar) != 0,
not removable by an equal-count holomorphic refit). Conjecture: this kind of structure is a property
of theoretical forms / models, NOT of raw measured fields. In measured data the conjugate part is
always determined (mirror) by one of:
  (a) reality-lock: the underlying field is real => Hermitian symmetry forces the conjugate
      (SPARC galaxies, EHT visibilities, sky intensity);
  (b) causality-lock: Kramers-Kronig ties Im to Re of any causal response (n+ik, sigma_xy(omega));
  (c) phase-blindness: the measurement records magnitude only (ARPES/BQPI gap), so phase/chirality
      is not in the data at all.
Independent complex information that IS present is carried holomorphically (branch points, poles,
phase windings) or discretely (a sign, a monodromy/permutation), neither of which is a continuous
z-bar dependence detectable by the Wirtinger judge.

## Tests this session that FAILED to break it (each a serious candidate that should have)
1. Chiral superconductor (p+ip / p-ip), executed in sandbox:
   - k-domain order parameter Delta(k) ~ kx -+ i ky: anti-holo IS non-removable, BUT the band
     structure (real Sr2RuO4 tight-binding) does NOT change the verdict => it REDUCES to the toy
     model (e1c7318e). Feeding the theoretical form = calibration, not discovery (like Kirsch).
   - omega-domain measured object sigma_xy(omega): causal => holomorphic in omega => judge sees
     HOLO/causal. Chirality is encoded in the SIGN of sigma_xy, invisible to d/d(zbar). DECORATIVE.
   => no new anti-holo discovery reachable via the chiral SC.
2. Non-Hermitian exceptional point, executed in sandbox:
   - eigenvalue E(g) = sqrt(kappa^2 - g^2): symbolically dE/d(conj g) = 0 => HOLOMORPHIC in the
     control parameter (a branch cut, not anti-holomorphy). HOLO-only beats FULL.
   - the physical EP signature is eigenvalue BRAIDING on a loop = a DISCRETE monodromy (sheet swap),
     again not a continuous z-bar dependence.
   => conjecture not broken; Wirtinger judge is the wrong instrument for discrete/topological info.

## Independent precedent (already traced, May 2026) consistent with the conjecture
KiDS-1000 gravitational lensing, 268,722 source-lens pairs (MEASURED data): physical 1/r signal at
complexity 5; anti-holo eml-star only at complexity >=14 (interpolation); at complexity 11 a pure
holomorphic formula beats the anti-holo one => anti-holo DECORATIVE on measured lensing data. KiDS
is reality-locked (sky observable is real), so it illustrates rather than tests the conjecture, but
it is a third consistent case.

## Status and what would refute it
[CONJECTURE] -- three consistent cases (chiral SC, exceptional point, KiDS) are NOT a proof. The
conjecture is FALSIFIABLE: a single measured system whose raw observable carries an independent,
continuous z-bar dependence not removable by an equal-count holomorphic refit, and not reducible to
reality-lock / causality-lock / a discrete sign, would break it and would BE the Plateau-B discovery.
Best remaining candidate to attempt a break: the quantum geometric tensor / Berry curvature, where
the imaginary part (Berry curvature) is claimed to be an independently MEASURED quantity. To test next.

## Consequence for the project (honest reframing)
The eml-star tool is a reliable CERTIFIER (it correctly adjudicates necessary vs decorative on any
given form: T' decorative 616640ad, toy necessary e1c7318e). It is NOT a discoverer of z-bar in raw
nature, because -- if this conjecture holds -- there is no independent z-bar to find in raw measured
fields. The conjecture itself, if it survives further tests, is a publishable negative/structural
result: "where anti-holomorphic necessity lives (forms) and why it is absent from raw measurement."
Files: sandbox tests this session (chiral SC reduction, exceptional point); precedent KiDS (May 2026).
Arbiter for any future "break": execution on Anthony's machine + SymPy judge. NOT established; a
falsifiable navigation conjecture.

## UPDATE 2026-06-16 -- fourth lock identified (QGT test), conjecture reinforced, still [CONJECTURE]
Tested the quantum geometric tensor / Berry curvature (Qi-Wu-Zhang two-band Chern insulator) as the
last serious break candidate. Result: does NOT break the conjecture, and exposes a FOURTH lock.
- Level 1: Berry curvature F(k) is REAL-valued (max|Im|=0) => reality-lock (a), trivial SPARC case.
- Level 2/3 [SANDBOX, to be confirmed by the judge]: the complex Bloch data (projector element
  P01(k)=u0*conj(u1)) is genuinely complex (max|Im|~0.43) BUT is built from the d-vector
  (sin kx, sin ky, m+cos kx+cos ky), i.e. from REAL momenta kx,ky taken SEPARATELY through real
  trig functions. So P01 is a real-analytic function of (kx,ky) that happens to be complex-valued:
  d/d(zbar) != 0 AND d/dz != 0, "mixed" but NOT from independent chirality -- the generic
  real-analytic case. This is a NEW failure mode, distinct from (a)-(c):
  (d) REAL-ANALYTIC / SPINOR-LOCK: when the complex object is built from REAL arguments (coordinates,
      momenta) taken separately, its z-bar dependence is the generic artifact of a complex-valued
      real-analytic function, NOT independent anti-holomorphy. This is the SPARC trap one level up:
      not the FIELD that is real (as in a), but the ARGUMENT. A naive d/d(zbar) judge would FALSE-
      POSITIVE here, and the equal-count necessity test would also mis-call "necessary" -- caught
      only by inspecting the structure (real argument), not the verdict.

## Four concordant cases, four distinct locks (NOT yet an exhaustion proof)
  chiral SC -> causality-lock (omega) / reduces to toy (k);  exceptional point -> holomorphic branch
  + discrete monodromy (c);  KiDS -> reality-lock (a);  QGT -> reality-lock (a) for F, spinor-lock
  (d) for the Bloch data. No measured object yet carries independent continuous z-bar.

## What is required to upgrade [CONJECTURE] -> [DERIVATION] (Milo's two conditions, accepted)
  1. Anthony's SymPy judge must explicitly confirm lock (d) on the QGT P01(k) (structural verdict,
     not just the sandbox argument).
  2. Verify no QGT object escapes spinor-lock -- in particular check whether any natively-complex
     formulation (rather than one built from real kx,ky) exists.
  PLUS, for a true theorem (beyond four cases): a GENERAL argument that every measured complex
  observable must fall into (a)-(d). Four concordant cases are evidence, not exhaustion.
Status remains [CONJECTURE / open]. Sandbox results, NOT certified on Anthony's machine yet.
