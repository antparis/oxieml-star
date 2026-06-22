# FINDINGS 2026-06-10c -- Bargmann last refuge tested: STRUCTURAL NO-GO sealed, project pivots to writing

## Turning point
This is the most important result of the session. The last structural refuge
(Bargmann reproducing kernel) was tested. The no-go is now sealed on three fronts.
The chiral cell (forced + transcendental + physical + non-reducible) is STRUCTURALLY
EMPTY in the perimeter of physical observables. Project pivots: search -> writing.

## GW arc (recap)
GW precessing-binary mode asymmetry A_lm: REAL, control-validated (precessing >>
aligned ~8 orders), 0163 (2,2) anomaly = spin-exchange physics. BUT mirror-locked:
h=h_+ - i h_x packages two REAL polarisations, so h_{l,-m}=(-1)^l conj(h_{l,m}) is
a REALITY condition. PySR test (z=h22, mode 3,3, holo vs anti vs shuffle, 3 sims) =
NEGATIVE: holo~anti, shuffle uncasse. -> "packaging theorem": complex observables
repackaging REAL fields are mirror-locked. GW joins the closed set.

## Bargmann reproducing kernel K(z,wbar)=exp(z*wbar) -- SymPy judge
- dK/dwbar = z*exp(z*wbar) != 0          -> ANTI-HOLOMORPHIC (yes)
- all d^n/dwbar^n != 0                    -> TRANSCENDENTAL, escapes Balk
                                            (not finite-order polyanalytic)
- does NOT factor as |w|^2k * holo        -> NON-REDUCIBLE (z,w independent)
- contrast Landau: Landau transcendence lives in e^{-|w|^2} (REAL module, mirror);
  Bargmann's is in wbar PURE (z != wbar). KEY DIFFERENCE.
=> FIRST object to pass anti + transcendental + non-reducible (3/4 criteria).
BUT FAILS the 4th "forced by PHYSICS": K is the Hilbert-space reproducing kernel
(resolution of identity of coherent states), NOT a measured observable. Depends on
choice of complexification (Bargmann vs anti-Bargmann) -> convention, not law.
Reducibility test (forced version): change complexification -> wbar becomes w.
Removable. NOT forced.

## Verdict: [ESTABLISHED] -- STRUCTURAL NO-GO (closure theorem, conditional on ellipticity)
The chiral cell is empty in the physical-observable perimeter, and we know WHY:
- FRONT 1 (mirror theorem): real frozen scalar fields -> anti is forced reflection
  of holo. Closed.
- FRONT 2 (packaging theorem, NEW): complex observables repackaging real fields
  (GW strain, Newman-Penrose/Teukolsky, S-matrix) satisfy O_{-k}=(phase)conj(O_k)
  -> mirror-locked. Closed.
- FRONT 3 (Vekua/Balk): any zbar dependence from an elliptic operator is either
  polynomial-in-zbar with holo coeffs (Balk -> module-trapped) or absorbable in a
  real module e^{s(z)} (Vekua similarity -> mirror/gauge). No irreducible
  transcendental in zbar. Closed.
- ONLY escape (Bargmann kernel) = Hilbert structure, convention-dependent, not forced.

CLOSURE STATEMENT: any anti-holomorphic transcendental non-reducible object is
either (a) Hilbert-space structure (reproducing kernel, complexification-convention-
dependent), or (b) nonexistent as a forced physical observable.

## Caveat (honesty)
No-go CONDITIONAL on ellipticity. A non-elliptic equation or an infinite-order
d/dzbar operator would formally escape Vekua/Balk. None found physically realised.
"All known elliptic systems closed" != "all physics closed". State as conditional
theorem with explicit hypotheses.

## Strategic pivot (from deep-research report 2026-06-10)
End of search phase. Begin writing, 3 coordinated citable objects:
(i)   THEOREM (J. Math. Phys. or SIGMA): Stone-Weierstrass density of {eml,eml*,1}
      + closure/no-go theorem (mirror + packaging + Vekua-Balk).
(ii)  PIPELINE (SciPost Phys. Codebases or JOSS): PySR + SymPy Wirtinger judge,
      negative controls + shuffle. NOTE: JOSS needs >=6 months public history ->
      open the public repo NOW to keep that option.
(iii) CARTOGRAPHY (SciPost Phys. Community Reports): rejection corpus (Kirsch,
      Landau, Aharonov-Bohm, SPARC, Hasegawa-Mima/Wakatani, EHT, GW) with
      reproducible criteria (module-trapped, mirror-locked, packaging, encoding).

## holo/anti ledger -- FINAL state of search phase
- NO forced physical anti-holomorphic transcendental found. Chiral cell EMPTY,
  now WITH a closure theorem explaining why.
- Bargmann kernel = math-pass, physics-fail (convention). Documented.
- The negative is UNDERSTOOD and DEMONSTRATED, not merely observed. A no-go is a
  POSITIVE result, not a failure.

## Refs (deep-research report)
Vekua similarity (Generalized Analytic Functions 1962; arXiv:2009.02052). Balk
polyanalytic (1991). Boyle et al. arXiv:1409.4431 (GW reality). Coulomb-gas
log|z|=1/2(log z+log zbar) arXiv:2309.09016. No-go methodology arXiv:2103.03491.

## Pointer
Caps the GW arc (2aba64c2, FINDINGS_20260610b) and the whole search phase.
Strategic report archived separately in MILO.
