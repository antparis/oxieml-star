#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
forcing_filter.py  --  Layer-3 orthogonal-axis sieve (eml / eml-star project)

PURPOSE
-------
Upstream NECESSARY-CONDITIONS sieve for the ENTANGLED_CHIRAL_ANTI target.
It inverts the pipeline: instead of judging a given f a posteriori, it takes
the structural attributes of a *forcing mechanism* and ELIMINATES those that
are geometrically confined to the factorizable sub-cube, BEFORE any simulation.

ROLE
----
DISCOVERER / orienter only. It never confirms a candidate. It returns either:
    REJECTED(reasons)         -> fails >=1 necessary condition; do not simulate.
    SURVIVES                  -> pass the closed form to the SymPy judge
                                 (verify_exact.py / nonseparable_judge.py),
                                 which is the SOLE certification authority.
Status of any SURVIVES verdict: [HEURISTIC]. Never [ESTABLISHED].

NECESSARY CONDITIONS for ENTANGLED_CHIRAL_ANTI (all from established laws)
-------------------------------------------------------------------------
  1. multi_field            >=2 fields (single-field confined to factorizable)   [DERIVATION]
  2. reality_relaxed_nongauge   reality relaxed, NOT gauge-removable             master law
  3. unpaired               zbar not self-conjugate (non-paired)                 master law
  4. transcendental         log/exp argument, not algebraic                      master law
  5. nonfactorizable        d_z d_zbar log f != 0                                master law (judge)
  6. naimark_irreducible    explicit L-R interaction, Naimark-irreducible        commit 9019436
  7. spatial_carrier        complexity in the SPATIAL anti sector, NOT a
                            temporal/spectral exponent of a real variable        FINDINGS_20260624 (DRUM)

A ternary attribute can be True / False / None(=UNKNOWN).
  - False on a necessary condition  -> contributes a rejection reason.
  - None (UNKNOWN)                   -> cannot eliminate; left to the judge.
Conditions 5 and 6 are typically UNKNOWN upstream, so the sieve mostly
discriminates on the structural attributes 1-4 and 7 that are readable without
any Wirtinger computation. Condition 7 distinguishes a complex SPATIAL variable
(z = x+iy geometric, candidate-compatible) from a complex frequency/eigenvalue
that merely sits in a temporal exponent e^{-i lambda t} (HOL: lambda is a
parameter, not an independent zbar). It sharpens the invariant: "non-Hermitian"
is necessary but NOT sufficient -- the non-Hermiticity must enter the spatial
anti sector, not a temporal exponent.

CALIBRATION
-----------
The sieve must re-reject the certified walls, each for the correct reason, and
let the target survive. The self-test at the bottom enforces this. Wall
attributes below are transcribed from the research history (commits / FINDINGS
noted); they are NOT re-certified here. If an attribute is disputed, the sieve
changes.
"""

from dataclasses import dataclass, field
from typing import Optional, List

# The seven necessary conditions, in report order. True is required to survive.
NECESSARY = [
    ("multi_field",             "single-field -> factorizable sub-cube"),
    ("reality_relaxed_nongauge","reality respected or gauge-removable -> mirror-locked"),
    ("unpaired",                "paired/self-conjugate zbar -> real-trapped"),
    ("transcendental",          "algebraic argument -> not the transcendental target"),
    ("nonfactorizable",         "d_z d_zbar log f = 0 -> separable wall"),
    ("naimark_irreducible",     "reducible L-R interaction -> basis-removable"),
    ("spatial_carrier",         "complexity in a temporal/spectral exponent -> HOL, not spatial anti"),
]


@dataclass
class Mechanism:
    """A physical/mathematical forcing mechanism described by structural attributes.

    Each attribute is True / False / None(UNKNOWN). 'source' documents provenance.
    """
    name: str
    multi_field: Optional[bool] = None
    reality_relaxed_nongauge: Optional[bool] = None
    unpaired: Optional[bool] = None
    transcendental: Optional[bool] = None
    nonfactorizable: Optional[bool] = None
    naimark_irreducible: Optional[bool] = None
    spatial_carrier: Optional[bool] = None
    source: str = ""


def sieve(m: Mechanism):
    """Apply the necessary-conditions elimination filter.

    Returns (verdict, reasons) where verdict in {"REJECTED", "SURVIVES"}.
    A condition explicitly False is a rejection reason; UNKNOWN never rejects.
    """
    reasons: List[str] = []
    for attr, why in NECESSARY:
        val = getattr(m, attr)
        if val is False:
            reasons.append(f"{attr} is False: {why}")
    if reasons:
        return "REJECTED", reasons
    # No necessary condition is explicitly violated.
    unknowns = [a for a, _ in NECESSARY if getattr(m, a) is None]
    note = ("pass closed form to judge (verify_exact.py / nonseparable_judge.py); "
            f"UNKNOWN left to judge: {unknowns}" if unknowns
            else "all necessary conditions met structurally; judge must still certify")
    return "SURVIVES", [note]


# ---------------------------------------------------------------------------
# CALIBRATION SET: certified walls + the target.
# ---------------------------------------------------------------------------

WALLS = [
    Mechanism(
        name="Kirsch elasticity (Kolosov-Muskhelishvili)",
        multi_field=True,                  # two potentials phi, psi
        reality_relaxed_nongauge=False,    # stress tensor real -> reality respected
        unpaired=False,                    # psi tied to conj(phi) by free-traction BC
        transcendental=True,               # log terms
        nonfactorizable=None,
        naimark_irreducible=None,
        spatial_carrier=True,              # genuine spatial z (elastic plane), but paired
        source="commit b9de06a [ESTABLISHED]: eml-star forced by BC but stays paired/real",
    ),
    Mechanism(
        name="Yang-Mills non-Hermitian LCFT (arXiv:2603.19006)",
        multi_field=True,
        reality_relaxed_nongauge=True,     # genuinely non-Hermitian
        unpaired=False,                    # radial/dilatation log, paired sectors
        transcendental=True,
        nonfactorizable=False,             # factorizes (multiplicative vertex)
        naimark_irreducible=False,
        spatial_carrier=False,             # complex anomalous dim in exponent of real var
        source="commit 07792fd: real/module-trapped",
    ),
    Mechanism(
        name="Hatano-Nelson non-Hermitian hopping",
        multi_field=False,                 # single-particle
        reality_relaxed_nongauge=False,    # gauge-removable (imaginary similarity transf.)
        unpaired=None,
        transcendental=None,
        nonfactorizable=None,
        naimark_irreducible=None,
        spatial_carrier=False,             # complex spectrum (spectral exponent), removable
        source="history: gauge wall (imaginary similarity transformation)",
    ),
    Mechanism(
        name="PT-symmetric free-fermion LCFT (Io-Huang-Hsieh, arXiv:2602.02649)",
        multi_field=True,                  # L/R fermions
        reality_relaxed_nongauge=True,
        unpaired=False,                    # symmetric sectors -> cross-log paired
        transcendental=True,
        nonfactorizable=None,
        naimark_irreducible=False,
        spatial_carrier=False,             # PT eigenvalues -> spectral exponent
        source="commit b775917: REAL_TRAPPED",
    ),
    Mechanism(
        name="Gravitational anomaly c_L != c_R route (M-IV hunt)",
        multi_field=True,
        reality_relaxed_nongauge=True,
        unpaired=True,
        transcendental=True,
        nonfactorizable=False,             # reaches only separable walls
        naimark_irreducible=False,         # needs explicit Naimark-irreducible L-R
        spatial_carrier=None,
        source="commit 9019436: separable wall, anomaly eliminated as direct route",
    ),
    Mechanism(
        name="DRUM non-reciprocal EP (modal + field, Light:Sci.Appl. 2026)",
        multi_field=True,                  # CW/CCW modes
        reality_relaxed_nongauge=True,     # non-Hermitian, non-removable at the EP (Jordan)
        unpaired=None,                     # unidirectional coupling, not analysed -> UNKNOWN
        transcendental=True,               # Jordan-block log
        nonfactorizable=None,
        naimark_irreducible=True,          # Jordan block non-diagonalizable, by construction
        spatial_carrier=False,             # complex frequency in temporal exponent (HOL)
        source="commits 8e1ee51 + this: SPARC-closed modal AND field; sole rejection is cond.7",
    ),
]

TARGET = Mechanism(
    name="ENTANGLED_CHIRAL_ANTI (target, e.g. 1 + pi*log z1 + phi*log conj(z2))",
    multi_field=True,
    reality_relaxed_nongauge=True,
    unpaired=True,
    transcendental=True,
    nonfactorizable=True,
    naimark_irreducible=True,
    spatial_carrier=True,                  # complex must live in the spatial anti sector
    source="master law + commit 20204b2 (cross-discriminant operational) + FINDINGS_20260624",
)


def _selftest():
    """Calibration: every wall must be REJECTED, the target must SURVIVE."""
    ok = True
    print("=== CALIBRATION on certified walls ===")
    for w in WALLS:
        verdict, reasons = sieve(w)
        passed = (verdict == "REJECTED")
        ok = ok and passed
        print(f"[{'OK ' if passed else 'FAIL'}] {verdict:9s} | {w.name}")
        for r in reasons:
            print(f"            - {r}")
    print("\n=== TARGET ===")
    verdict, reasons = sieve(TARGET)
    passed = (verdict == "SURVIVES")
    ok = ok and passed
    print(f"[{'OK ' if passed else 'FAIL'}] {verdict:9s} | {TARGET.name}")
    for r in reasons:
        print(f"            - {r}")
    print("\nCALIBRATION:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if _selftest() else 1)
