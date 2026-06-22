# FINDINGS 2026-06-22e -- judge_v2 module-trapped blind spot FIXED (L = pure-imaginary constant)

## Status
[ESTABLISHED] (machine, judge_v2 patched, 5-step protocol, code 0): the judge_v2
module-trapped criterion had a blind spot -- it missed L = pure-imaginary CONSTANT,
misclassifying |z|^(is) (inverse-square supercritical radial part, FINDINGS 0622d) as
anti?. Patched, validated with zero regression, established anti results unaffected.

## The blind spot (from FINDINGS 0622d)
is_module_trapped tested: L = zbar*dlog(f)/dzbar must be REAL and product-only.
For |z|^(is)=(z*zbar)^(is/2): L = i*s/2 (pure imaginary CONSTANT), product-only=True, but
L_real=False (full_conj flips i->-i, so L - conj(L) = i*s != 0). => fell through to
"anti-holomorphic", wrong. A constant L (no z,zbar dependence) means dlog(f)/dzbar carries
no genuine anti content; it is a modulus power (real OR imaginary exponent).

## The fix (minimal, surgical)
In is_module_trapped, final return changed from:
  return bool(L_real and prod_only)
to:
  L_const = (diff(L,z)==0 and diff(L,zbar)==0)
  L_pure_imag = (simplify(L + full_conj(L)) == 0)
  return bool((L_real or (L_const and L_pure_imag)) and prod_only)
Rationale: a constant L that is real OR pure-imaginary, with product-only, is a modulus
power -> module-trapped. backup: judge_v2.py.bak_20260622_pre_blindspot_fix (sha256 verified).

## 5-step validation protocol (all on machine, all passed)
1. BACKUP: judge_v2.py.bak_20260622_pre_blindspot_fix, sha256 identical to original.
2. DIAGNOSE (diagnose_blindspot.py, no change): confirmed |z|^(is) misclassified as anti
   (L=i*s/2, const=True, pureIm=True); confirmed NO genuine anti has the (const+pureImag)
   signature -> fix SAFE. Genuine anti (z+0.3zbar, vortex_N1) have const=False; pure anti
   (i*zbar, exp(zbar)) caught earlier by dfdz=0.
3. PATCH (patch_blindspot.py): applied, idempotent, pattern-matched the exact return line.
4. ZERO REGRESSION: judge_v2 self-validation all OK (no FAIL incl. vortex_N1, module cases);
   base C-native bench (cnative_bench.py.bak_20260621_pre_grammar) ran code 0, cross-tab
   clean, "No failures: judge == expected on every scored case" (ANTI 67, MIXED 48,
   MODULE 76, REAL 77).
5. RE-AUDIT (reaudit_after_fix.py): all established anti stay anti (Maass shadow, vortex_N1,
   z+0.3zbar, i*zbar, exp(zbar), fractals z^2+zbar / z^3+zbar^2 / z^5+zbar^3 / z^4+zbar,
   additive z^2+conj(z)); all module stay module incl. newly-caught |z|^(is). VERDICT CLEAN,
   no collateral damage.

## Note on the bench
The full cnative_bench.py (with the bridled-enriched generator added 2026-06-21) still
times out (code 124, 0 output) -- the ENRICHED GENERATOR blocks it, a SEPARATE issue from
the judge (still pending since 2026-06-21). The base bench (pre-grammar backup) finishes
fast and was used for regression testing here; the judge patch is independent of the
generator, so the base bench is the correct regression terrain.

## Files
judge_v2.py (patched), judge_v2.py.bak_20260622_pre_blindspot_fix (backup),
patch_blindspot.py, diagnose_blindspot.py, reaudit_after_fix.py,
cnative_bench_report_20260622T030226Z.json. Builds on FINDINGS_20260622d.
