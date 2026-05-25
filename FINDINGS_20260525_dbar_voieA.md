# FINDINGS 2026-05-25 — Method B1-A: solving forced-mirror Wirtinger laws

## What was tested
Dirac-style approach (method B1, voie A): write a law df/dzbar = G(z,zbar,f),
solve in CLOSED FORM with SymPy dsolve (NO data, NO PySR), inspect the solution.
Scripts: dbar_solve_A.py, dbar_solve_A_nonlinear.py, dbar_solve_A_coupled.py.
Cross-reproduced on PC Linux and Mac/Grok (identical SymPy solutions).

## Results [DERIVATION] (exact symbolic, residual=0 where checked)
- df/dzbar = z*f       -> f = h(z)*exp(z*zbar)   [residual 0; = Landau gaussian, derived from a law]
- df/dzbar = f^2       -> f = -1/(C1+zbar)        [zbar only, z passive: disguised ODE, trivial]
- df/dzbar = f*(1-f)   -> f = 1/(C1*exp(-zbar)+1) [zbar only: disguised ODE, trivial]
- df/dzbar = z*f^2     -> f = -1/(C1+z*zbar)      [z*zbar = |z|^2: radial, Landau-family, NOT new]
- df/dzbar = zbar*f^2  -> f = -2/(C1+zbar^2)      [z passive: trivial]
- df/dzbar = z*zbar*f  -> f = C1*exp(z*zbar^2/2)  [|z|^2 * zbar: asymmetric mixed, only non-trivial form]

## Honest verdict
METHOD VALIDATED: SymPy solves dbar-laws (linear, nonlinear, coupled) in closed form.
BUT no DISCOVERY: every solution is fully determined by the equation WE chose.
Solving a self-chosen law never surprises -- the answer is in the question.
A real "Dirac moment" needs a law NOT chosen for its answer.
Status: [DERIVATION] for the method; NOT a discovery.

## Next directions identified (not yet tested)
1. Physics-imposed law (needs a real system: Landau/TBG family).
2. MULTIPLE simultaneous constraints (compatibility forces the solution, not our choice).
3. INVERSION: start from eml-star itself, find which law it satisfies.
