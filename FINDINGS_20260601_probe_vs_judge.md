# FINDINGS 2026-06-01 -- antiholo_probe vs certified pipeline (roles fixed)

## Status
[HEURISTIC] classification of antiholo_probe.py (a numerical indicator).
[ESTABLISHED] role separation: probe = pre-filter, judge = sole authority.

## What antiholo_probe.py is
Written 2026-05-30. Computes anti-fraction
  A = median|df/dzbar| / (median|df/dz| + median|df/dzbar|)
by finite-difference Wirtinger derivatives on a grid. Its own docstring:
"NUMERICAL INDICATOR, not a proof; certification still requires the SymPy
judge on a fitted closed form." Runs in milliseconds.
=> STATUS [HEURISTIC]. A pre-filter, never a verdict.

## Comparison to the certified pipeline (PySR -> verify_exact -> reality_check)
  probe output  : anti-fraction A in [0,1]   (a MARKER)
  pipeline out  : exact HOLO/ANTI verdict + real/complex flag  (the JUDGE)
  probe method  : finite-difference Wirtinger on grid (approximate)
  pipeline      : symbolic regression -> EXACT SymPy d/dzbar
  GUARD-RAIL    : anti-fraction A is the SAME kind of marker the rule forbids
                  as a final verdict (like the PySR JSON 'verdict' field).
  CRITICAL GAP  : the probe does NOT separate real-trapped (|z|^2, SPARC) from
                  genuine chiral anti. A high A can come from a REAL field.
                  reality_check.py closes exactly this gap. Probe alone does
                  NOT protect against the SPARC trap.

## optical_vortex_gen.py: what it does and does NOT do
- Real physics: Laguerre-Gauss beam, charge sign = chirality = holo/anti.
- BUT it stops at anti-fraction A (probe). It NEVER calls the SymPy judge.
  => in current form it can only yield [HEURISTIC], never a certification.
- The anti here is z^l / conj(z)^|l| : a MONOMIAL = ALGEBRAIC finite-order anti
  (like Kirsch/Landau), NOT the transcendental log(zbar) of vortex_N1.
- The anti is SUSPENDED on an analysis choice (dividing the known Gaussian
  envelope), NOT forced by a physical constraint (unlike Kirsch traction-free).

## Decision
To make the optical vortex a real pipeline test (not just a probe number),
an adapter must: write 3 CSVs (anti = l<0 envelope-divided, holo = l>0,
shuf = shuffle) -> kirsch_stack.run_one -> reality_check.py, exactly like N1.
Even if it passes, the result is "ALGEBRAIC anti on an optical case": a 3rd
physical calibration of Kirsch type, NOT the transcendental jalon.
