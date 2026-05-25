#!/usr/bin/env python3
"""
dbar_invert.py — B1, direction 3: INVERSION.
Instead of choosing a law and solving for f, take the project's OWN operators
(eml, emlstar, eml0) and ask: which Wirtinger law df/dzbar = ? does each satisfy?
If an operator obeys a simple non-trivial law we had not written, that is a
property of OUR object we did not know. NO data, NO PySR. Pure symbolic.
[CONJECTURE] until inspected. z, zbar independent (Wirtinger).
"""
import sympy as sp

z, zb = sp.symbols('z zb')

def invert(label, f):
    print(f"\n========== {label} ==========")
    print("f          =", f)
    dfz  = sp.simplify(sp.diff(f, z))
    dfzb = sp.simplify(sp.diff(f, zb))
    print("df/dz      =", dfz)
    print("df/dzbar   =", dfzb)
    # Try to express df/dzbar as a simple function of f, z, zbar.
    # Report the raw derivative; the law is df/dzbar = (that expression).
    holo = (dfzb == 0)
    print("holomorphic (df/dzbar==0):", holo)
    return dfz, dfzb

# eml diagonal: exp(z) - log(z)  (holomorphic)
invert("eml(z) = exp(z) - log(z)", sp.exp(z) - sp.log(z))

# emlstar canonical mixed: exp(z) - log(conj z) = exp(z) - log(zbar)
invert("emlstar(z) = exp(z) - log(zbar)", sp.exp(z) - sp.log(zb))

# eml0 (argument-type): if eml0 isolates imaginary/arg part. Test log(zbar) alone.
invert("log(zbar) [anti-holo core]", sp.log(zb))

# combination eml + emlstar
invert("eml + emlstar = 2exp(z) - log(z) - log(zbar)",
       2*sp.exp(z) - sp.log(z) - sp.log(zb))

# product structure: emlstar * z (does coupling appear?)
invert("z * emlstar = z*(exp(z) - log(zbar))",
       z*(sp.exp(z) - sp.log(zb)))

print("\n=== DONE ===")
print("Look for any operator whose df/dzbar is a SIMPLE law we had not written.")
print("Especially: does df/dzbar couple z and zbar, or depend on f itself?")
