# FINDINGS 2026-06-16 -- [HEURISTIC / calibration] Tool validated on the "necessary" verdict: a toy model with a natively complex observable f(z)=a*z+b*conj(z) is genuinely anti-holomorphic-necessary -- no equal-parameter holomorphic model can fit it, and the judge certifies df/dzbar=b!=0. Mirror of the T' "decorative" verdict; together they validate BOTH faces of the pipeline.

## Purpose
After the T' negative result (anti-holo DECORATIVE, holo-only refit recovers), we needed to confirm
the pipeline can also detect the OPPOSITE verdict: a case where anti-holo is genuinely NECESSARY.
This is calibration of the "yes" face. Synthetic BY CONSTRUCTION -- NOT a discovery in nature.

## Construction and the lesson behind it
Attempt 1 (failed, in sandbox): observable = moduli / eigenvalues (REAL quantities). Holo-only
refit succeeded => not necessary. This re-confirms Anthony's navigation law: a real observable is
mirror-locked and never forces anti-holomorphy.
Attempt 2 (succeeded): observable = the COMPLEX FIELD VALUE itself f(z)=a*z+b*conj(z), b independent
of a. A natively complex, chiral observable. No holomorphic function can reproduce conj(z)
dependence on a 2D sample.

## Results (executed on Anthony's machine)
Equal-parameter-count (4 real params each), 30-start:
  FULL      (a*z + b*conj z)   chi2 = 1.6e-19   recovered a=1.300-0.400i, b=0.800+0.600i (truth exact)
  HOLO-ONLY (a*z + c)          chi2 = 103       (fails)
  HOLO-ONLY (a*z + d*z^2)      chi2 = 92        (fails)
=> anti-holomorphic structure NECESSARY (holo-only cannot fit at equal param count).
Judge (SymPy, exact): f=a*z+b*conj(z), df/dzbar = b = 0.8+0.6i != 0 => ANTI-HOLOMORPHIC: True.

## Both pipeline roles concur on a "necessary" case
- Necessity test (equal-count refit): holo-only fails => not removable.
- Certifier (df/dzbar): != 0 => formula is anti-holomorphic.
First "yes, necessary" case of the session where both roles agree. Complements T' (both said
"decorative/no"). The tool now demonstrably distinguishes BOTH verdicts.

## Status and honest limits
[HEURISTIC / calibration]. This is Plateau A (tool calibration on the "yes" verdict), NOT Plateau B
(discovery in real data). The data is synthetic, designed to be anti-holomorphic; the value is that
the pipeline correctly identifies necessity when the observable is natively complex, and correctly
identified decorativeness on T'. KEY takeaway reinforced: anti-holo necessity REQUIRES a natively
complex observable (phase/complex amplitude/chirality), never a real quantity (mass, angle, modulus)
-- this is exactly why neutrinos (real observables) gave "decorative" and why the next real targets
must be natively complex (chiral superconductor Kerr signal n_xy, causal response n+ik).
Files: toy_necessity.py, data/toy_necessity.csv.
Arbiter = Anthony's machine + SymPy judge. NOT a discovery; a two-faced calibration of the tool.
