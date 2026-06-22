# FINDINGS 2026-06-22m -- eml-mod: a FOURTH operator of a DIFFERENT TYPE (global transformation / modularity)

## Status
[ESTABLISHED] (sandbox numeric, mpmath dps=30; to replay on machine). eml-mod, a modularity-
defect detector, is LEGITIMATE: it separates objects the local grid (eml/eml*/eml0) confounds
(genuine theta vs false theta, both "holomorphic" to the grid). BUT it is of a DIFFERENT
NATURE -- a GLOBAL transformation operator, numeric, certificatory -- NOT a 4th local
autonomous eml. Honest framing: "4th operator of a different type", not "4th eml on equal footing".

## Definition (candidate 1, agreed)
eml-mod measures the MODULARITY DEFECT under S: tau -> -1/tau:
  delta_S(f) = f(-1/tau) - (c tau + d)^k f(tau),   for S: tau->-1/tau the weight factor is (-i tau)^k.
Three verdicts (the trio the local grid confounds):
  delta_S = 0                 -> MODULAR        (genuine theta)
  delta_S = Eichler period    -> MOCK-MODULAR   (mock theta; intermediate, needs completion)
  delta_S = smooth cocycle    -> QUANTUM-MODULAR (false theta; Zagier quantum modular form)

## Legitimacy test PASSED (numeric, nome q=e^{i pi tau}, weight k=1/2)
  tau      delta_S(genuine theta3)   delta_S(false theta)
  1.0i     8.5e-32                   0.0 (S fixed point, trivial)
  1.3i     1.3e-31                   0.209
  2.0i     1.8e-31                   0.611
  0.7i     7.0e-32                   0.244
  0.5i     4.0e-32                   0.432
Genuine theta: delta_S ~ machine-eps (MODULAR) at all points. False theta: delta_S = O(1)
(NON-modular). eml-mod SEPARATES them where the local grid put both in "holomorphic".
=> legitimacy criterion met for the genuine/false pair. (Mock theta = period defect, a third
intermediate type, requires the completion; deferred, but genuine/false separation suffices.)

## Nature: WHY eml-mod is NOT a 4th local eml
The three eml (eml/eml*/eml0) are LOCAL & autonomous: feed f(z,zbar), they compute a
derivative or modulus at a symbolic point, classify. eml-mod CANNOT compute delta_S from f
alone symbolically -- applying tau->-1/tau to a q-series does not simplify; it needs the
function's transformation behavior, evaluated NUMERICALLY at points. It is a GLOBAL
transformation operator (relates f(tau) to f(-1/tau)), CERTIFICATORY (verifies/classifies a
known transformation law), numeric not symbolic-exact. Different design from the eml family.

## Caveat caught (rigor note)
A FIRST manual encoding used the WRONG nome convention (q=e^{2 pi i tau} instead of
q=e^{i pi tau}) and produced a SPURIOUS defect delta=0.125 for genuine theta3 (which must be
modular). Diagnosed (not a convergence issue -- sum stable from N=10) and corrected using
mpmath's native jtheta (guaranteed law). This very error CONFIRMS eml-mod's different nature:
a local operator cannot mis-encode a transformation law; eml-mod depends on an external law
and is fragile to convention. Lesson logged.

## Significance
eml-mod closes the blind spot found in FINDINGS_20260622l (grid blind to false-modularity).
It is a transformation-based detector complementing the three local detectors:
  eml   : holomorphic (df/dzbar=0)         [local, autonomous, symbolic]
  eml*  : anti-holo (judge_v2 4-label)     [local, autonomous, symbolic]
  eml0  : pure phase (|f| const)           [local, autonomous, symbolic]
  eml-mod: modularity defect under S       [GLOBAL, certificatory, numeric]
The first three answer "how does zbar enter f locally"; eml-mod answers "how does f transform
globally". Together they map both local structure AND global transformation.

## Honest status
[ESTABLISHED] for genuine/false separation (numeric). NOT promoted to an equal 4th eml: it is
a different-type operator. Mock-theta period case deferred. Numeric (needs a convergence-safe
point off the S fixed point; tau=i is degenerate). To replay on machine + formalize as a
distinct module (eml_mod.py) if adopted, clearly labeled as transformation/certificatory.

## Files
this FINDINGS (sandbox numeric). Builds on 0622l (grid blindness to modularity), 0622j (grid).
