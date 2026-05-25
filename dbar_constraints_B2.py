#!/usr/bin/env python3
"""
dbar_constraints_B2.py — B1, direction 2: MULTIPLE simultaneous constraints.
Overdetermined system: impose BOTH
    df/dzbar = A(z,zbar)*f      (mirror direction)
    df/dz    = B(z,zbar)*f      (holomorphic direction)
The solution is NOT chosen by us: the Schwarz compatibility
    d/dz(df/dzbar) = d/dzbar(df/dz)
constrains A and B. Only compatible (A,B) admit a nonzero solution.
This is the closest thing to a 'Dirac moment': the cross-condition forces
what can exist. NO data, NO PySR. Pure symbolic. [CONJECTURE] until inspected.
"""
import sympy as sp

z, zb = sp.symbols('z zb')
f = sp.Function('f')

def compatibility(A, B, label):
    print(f"\n========== {label} ==========")
    print(f"  df/dzbar = ({A}) * f")
    print(f"  df/dz    = ({B}) * f")
    # For f != 0: from the two laws, Schwarz requires
    #   d/dz (A*f) = d/dzbar (B*f)
    #   (dA/dz)*f + A*(df/dz) = (dB/dzbar)*f + B*(df/dzbar)
    #   (dA/dz)*f + A*B*f      = (dB/dzbar)*f + B*A*f
    #   => dA/dz = dB/dzbar   (the A*B terms cancel)
    cond = sp.simplify(sp.diff(A, z) - sp.diff(B, zb))
    print(f"  Schwarz compatibility (must be 0): dA/dz - dB/dzbar = {cond}")
    if cond == 0:
        print("  -> COMPATIBLE. Nonzero solution exists.")
        # Build it: f = exp(integral). With constant-like A,B, f = exp(B*z + A*zbar) form.
        # Verify a candidate when A,B are such that mixed integral is clean:
        return True
    else:
        print("  -> INCOMPATIBLE. Only f=0 survives (the constraints kill each other).")
        return False

# Case 1: A,B constants -> always compatible (trivial: f=exp(bz+a zbar))
compatibility(sp.Integer(1), sp.Integer(1), "A=1, B=1 (constants)")

# Case 2: A=z, B=zbar -> couples space to mirror. Compatible?
compatibility(z, zb, "A=z, B=zbar")

# Case 3: A=zbar, B=z -> the swapped coupling. Compatible?
compatibility(zb, z, "A=zbar, B=z")

# Case 4: A=z, B=z -> same factor both directions
compatibility(z, z, "A=z, B=z")

# Case 5: A=zbar, B=zbar
compatibility(zb, zb, "A=zbar, B=zbar")

# Case 6: A = -1/zbar (the emlstar law!), B = exp-like? Test A=-1/zbar, B=0
compatibility(-1/zb, sp.Integer(0), "A=-1/zbar (emlstar law), B=0")

print("\n=== INTERPRETATION ===")
print("COMPATIBLE cases: a nonzero f exists, forced by the cross-condition.")
print("INCOMPATIBLE cases: the two laws are mutually exclusive -> only f=0.")
print("The interesting physics is in WHICH (A,B) pairs survive: that boundary")
print("is set by Schwarz (dA/dz = dB/dzbar), NOT chosen by us.")
