#!/usr/bin/env python3
"""
skfem_check.py -- minimal install-check for scikit-fem.

Solves the Poisson problem  -Laplace(u) = 1  on the unit square (0,1)x(0,1)
with u = 0 on the boundary. Known analytic max(u) ~ 0.073671 (centre value).
Pass criterion: |max(u) - 0.073671| < 0.005.

Nothing fancy: confirms skfem + numpy + a sparse solve work end-to-end.
"""
import numpy as np
from skfem import MeshTri, Basis, ElementTriP1, BilinearForm, LinearForm, condense, solve
from skfem.helpers import dot, grad

mesh = MeshTri().refined(5)               # 33x33 grid
basis = Basis(mesh, ElementTriP1())

@BilinearForm
def a(u, v, w):
    return dot(grad(u), grad(v))

@LinearForm
def L(v, w):
    return 1.0 * v

A = a.assemble(basis)
b = L.assemble(basis)
u = solve(*condense(A, b, D=basis.get_dofs()))

umax = float(u.max())
expected = 0.073671
err = abs(umax - expected)
print(f"skfem version : {__import__('skfem').__version__}")
print(f"DoFs          : {basis.N}")
print(f"max(u)        : {umax:.6f}")
print(f"expected      : {expected:.6f}")
print(f"abs error     : {err:.2e}")
print("RESULT        :", "PASS" if err < 5e-3 else "FAIL")
