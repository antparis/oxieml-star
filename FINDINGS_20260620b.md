# FINDINGS 2026-06-20b -- judge_v2 extended to 4 labels (MODULE_TRAPPED added)

## What was done
Extended judge_v2.certify_1field from 3 labels (holomorphic / real-trapped /
anti-holomorphic) to 4 by adding MODULE_TRAPPED, the reducible category where the
anti-holomorphic dependence is carried entirely by a real radial modulus
(Aharonov-Bohm / Hecke category): f = holo(z) * real_modulus(|z|^2), e.g.
z^a*zbar^b = z^(a-b)*|z|^(2b).

## Criterion (the key point)
A naive criterion "|mu| constant" (mu = (dfdzbar/dfdz)) was REJECTED: it
over-captures ADDITIVE genuine anti. Counter-example caught in sandbox:
vortex_N1 = A*log(z-c) + B*log(zbar-c) has |mu| = |B/A| constant (because
|z-c| = |zbar-c|), yet it is genuinely chiral, NOT module-trapped. z+0.3*zbar
fails the same way. Had the |mu| criterion shipped, the project's reference
chiral example would have been mislabeled module-trapped.

The CORRECT criterion is factorization, tested via the log-derivative:
  L = zbar * dlog(f)/dzbar = zbar * (df/dzbar) / f
If f = h(z)*m(z*zbar) then L = (z*zbar)*m'/m, which is REAL and a function of the
product z*zbar ONLY. Test:
  - L_real   : L - full_conj(L) == 0
  - prod_only: L is invariant under z->t*z, zbar->zbar/t  (so depends on z*zbar only)
  module-trapped  <=>  L_real AND prod_only.
Additive holo+anti sums fail prod_only -> stay anti-holomorphic. Multiplicative
monomials z^a*zbar^b pass -> module-trapped. The criterion is an iff: if L is real
and product-only, integrating gives f = h(z)*M(|z|^2) with M real.

## Exact commands
    python3 judge_v2.py            # self-test, all OK incl. vortex_N1 -> anti
    python3 cnative_bench.py       # C-native bench against the 4-label judge

## Raw result (executed on Anthony's ThinkCentre M920q)
Self-test: all blocks OK; the 4 MODULE-TRAP cases (z^1.7*zbar^-0.7, z^(1+r2)*zbar^(-r2/2),
z^2*zbar, z/zbar) -> module-trapped; vortex_N1 -> anti-holomorphic; z+0.3*zbar -> anti.
Bench: PASS 323/323, FAIL 0, errors 0. Cross-tab diagonal:
    HOL            -> 68 holomorphic
    ANTI           -> 64 anti-holomorphic
    MIXED          -> 47 anti-holomorphic   (genuine mixed IS anti; no separate label)
    MODULE_TRAPPED -> 70 module-trapped
    REAL_TRAPPED   -> 74 real-trapped
Zero ANTI and zero MIXED leaked into module-trapped (the dangerous error). Report:
cnative_bench_report_20260620T094814Z.json. judge sha256
36b289571224dc9c034d3f01a0c091d3730885e3ca6308dc8f10f0fbd383feab.

## Bench changes
cnative_bench.py: PROJECT[MODULE_TRAPPED] changed from "anti-holomorphic" to
"module-trapped"; crosstab judge_labels gained a "module-trapped" column. Backup
cnative_bench.py.bak_20260620. NOTE: the bench's "Reading:" footer text is now
stale (still says MODULE collapses into anti) -- cosmetic print, to be updated.

## Status
[ESTABLISHED] judge_v2 4-label single-field calibrated on the C-native bench:
323/323, zero anti/mixed leaked to module, vortex_N1 (reference chiral) stays anti.
[DERIVATION] factorization criterion is an iff (integration argument), sound on the
algebraic corpus (monomials, sums, log).

## Known limitations (measured / explicit)
- The bench's reference oracle detects module via INTEGER-k division (e/(z*zbar)^k
  holomorphic); the judge uses the general real-exponent log-derivative factorization.
  They agree on the current corpus (integer-k module only). Fractional-exponent module
  (z^1.7*zbar^-0.7) is exercised only in the judge self-test, NOT in the bench random
  corpus. To fully calibrate the general criterion: add fractional-exponent generators
  and a general reference test.
- Transcendental shadow (Maass incomplete-Gamma) NOT yet tested against the module
  criterion. That is the next target now that the MODULE_TRAPPED label exists.
