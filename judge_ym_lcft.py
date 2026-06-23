# Certifier: Yang-Mills non-Hermitian LCFT two-point forms (arXiv:2603.19006v1)
# under the eml / eml-star lens. Physical |x^2| (real spacetime interval) -> z*zbar.
# Mode: CERTIFIER (closed forms), not discoverer. Arbiter = judge_v2 on this machine.
# No shuffle / MSE: symbolic closed-form certification only.
import sympy as sp
from judge_v2 import z, zbar, certify_1field, full_conj, is_module_trapped

# All physical constants are REAL: Delta (conformal dim), a = Re(lambda),
# omega = Im(lambda), r, m (Jordan-block constants), A, B (real-observable coeffs).
D, a, r, w, m, A, B = sp.symbols('Delta a r omega m A B', real=True, positive=True)
u = z*zbar  # |x^2| = |z|^2

forms = [
    ("EP_Eq53    r - omega*m*log|x^2|       (Jordan rank-2, real correlator)",
        u**(-D - a) * (r - w*m*sp.log(u))),
    ("cross_Eq47 |x^2|^(-Delta-a-i*omega)   (PT-broken cross-correlator)",
        u**(-D - a - sp.I*w)),
    ("G00_Eq49   cos/sin(omega*log|x^2|)    (PT-broken real observable)",
        u**(-D - a) * (A*sp.cos(w*sp.log(u)) - B*sp.sin(w*sp.log(u)))),
]

print("# Certifier: Yang-Mills non-Hermitian LCFT forms  (|x^2| -> z*zbar)")
print("# judge = judge_v2.certify_1field ; arbiter = this run\n")
for name, f in forms:
    label, dfdzbar = certify_1field(f)
    print("[%s]  %s" % (label, name))
    print("      d f / d zbar == 0 ?       %s" % (sp.simplify(dfdzbar) == 0))
    print("      f - full_conj(f) == 0 ?   %s" % (sp.simplify(f - full_conj(f)) == 0))
    print("      is_module_trapped(f) ?    %s\n" % is_module_trapped(f))

print("# Framed expectation: EP real-trapped, cross module-trapped, G00 real-trapped.")
print("# None anti-holomorphic => non-Hermitian YM LCFT does NOT fill the eml-star chiral cell.")
