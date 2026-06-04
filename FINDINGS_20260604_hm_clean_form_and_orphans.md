# FINDINGS 2026-06-04 -- HM clean form (module log, NOT chiral) + two orphan scripts traced

## 1. Hasegawa-Mima screened vortex: clean closed form of the transcendental anti
[DERIVATION] (short-range analytic form + SymPy Wirtinger on machine). NOT [ESTABLISHED]:
the form comes from the K0 small-argument expansion, not a PySR-recovered+judged formula.

Object: w = -(i*Gamma/2pi rho_s) K1(|z|/rho_s) zbar/|z|, dw/dzbar = (iG/4pi rho^2) K0(|z|/rho_s).
Short-range K0(x) ~ -log(x/2) - gamma_E  =>  anti signature = (1/2) log(z*zbar) = log|z|^2.
  d/dzbar = 1/(2 zbar), d/dz = 1/(2 z), mu = z/zbar, |mu| = 1  -> MIRROR (equal weights b=conj a).
Contrast (genuine chiral): b*log(zbar), b complex, has d/dz = 0 (zbar-only). HM has NO such term.

VERDICT: HM transcendental anti is a MODULE log (log|z|^2), mirror-locked. This is the clean
closed form, reached analytically WITHOUT injecting Bessel into PySR (injecting K would be
circular: recovering a formula whose operator you planted is capability, not discovery).
Consistent with FINDINGS_20260602_hasegawa_mima.md [ESTABLISHED detectability, mirror form].
Closes the HM "clean form" question: forced + transcendental + physical + DETECTED, but
MIRROR (not chiral). The chiral cell stays empty. Script: hm_clean_form.py.

## 2. spacetime_trap.py -- traced [ESTABLISHED, symbolic part] -- the SPARC guardrail, made exact
Not a discovery candidate: it is the falsifiable DEMONSTRATION of the SPARC guardrail itself.
Part 1 (exact SymPy, authoritative): on time-encoded data z=x+i*t, d/dzbar fabricates a FALSE
"anti" verdict even for a MASSLESS field cos(x-t) with zero anti content; only the light-cone
observable d/dv=0 exposes it. Massless (3) and massive (4) BOTH give d/dzbar != 0 -> d/dzbar
cannot separate them on time-encoded data. Only natively-complex, no-time data (1)(2) give a
trustworthy d/dzbar verdict. Punchline: eml* is an OPERATOR BASIS, not a sensor. Part 3 (PySR)
NOT yet run; would illustrate the pipeline certifying the trap "anti" despite zero mass.
This is the project's central DEFENSIVE argument and was previously UNTRACED.

## 3. test_newton_emlstar.py -- traced [CONJECTURE, not yet run] -- eml* non-decorative ablation
Clean specificity test (Anthony's non-decorative criterion), NEVER executed. Fits Newton map
N(z)=(2z^3+1)/(3z^2) holomorphic WITH and WITHOUT emlstar, and control conj(N(z)) WITH/WITHOUT.
Rule: if removing emlstar breaks ONLY the anti fit (holo fine both ways), emlstar earns its
role (capability, not revelation). Native-complex data, no SPARC trap. niter=200 pop=500 ->
hours, run detached. Status stays [CONJECTURE] until executed + judged.

## Status summary
- HM clean form: [DERIVATION], module log, mirror, NOT chiral. hm_clean_form.py.
- spacetime_trap: [ESTABLISHED symbolic] SPARC guardrail exact. PySR part pending.
- newton ablation: [CONJECTURE] not run. To execute + judge.
