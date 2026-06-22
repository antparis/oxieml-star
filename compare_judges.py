#!/usr/bin/env python3
"""Compare the current judge vs Kimi's hardened judge on the bench gold controls.
Reveals where Kimi's numeric screen diverges -- expected ONLY on phase-of-modulus;
any OTHER divergence (esp. genuine anti -> module) is a numeric false positive."""
import sympy as sp
from judge_v2 import z, zbar, certify_1field as judge_current
from hardened_judge_KIMI import certify_1field_hardened as judge_kimi

# Pull the gold controls from cnative_bench (reuse its list)
import cnative_bench as cb

golds = cb.gold_controls()
print("="*92)
print(f"{'CASE':<46}{'CURRENT':<18}{'KIMI hardened':<18}{'DIVERGE?'}")
print("="*92)
diverge = []
for name, expr in golds:
    try:
        jc, _ = judge_current(expr)
    except Exception as e:
        jc = f"ERR:{type(e).__name__}"
    try:
        jk = judge_kimi(expr)
    except Exception as e:
        jk = f"ERR:{type(e).__name__}"
    d = "" if jc == jk else "  <-- DIVERGE"
    if jc != jk:
        diverge.append((name, jc, jk))
    print(f"{name[:44]:<46}{jc:<18}{jk:<18}{d}")
print("="*92)
print(f"Divergences: {len(diverge)}")
for n, jc, jk in diverge:
    print(f"   {n[:50]}: current={jc} kimi={jk}")
print("\nKEY: any divergence that is NOT a phase-of-modulus case, especially")
print("genuine-anti -> module-trapped, is a NUMERIC FALSE POSITIVE from Kimi's screen.")
print("="*92)
