# FINDINGS 2026-06-14 -- CP Stage 3 (GAP gCP module): Delta(54) is TYPE-I -- REPRODUCTION of known result, tool calibrated

## What this is
First execution of the Stage-3 generalized-CP (gCP) module using GAP (the proper tool,
as the blueprint recommended -- SymPy alone is mis-equipped). Goal: decide whether the
flavor group Delta(54) of the Bora et al. models forces CP violation (type-I) or allows
it to be removed (type-II), via the Chen-Fallbacher class-inverting-automorphism test.
Files: GAP scripts /tmp/cp_test2.g (Delta(27) calibration), /tmp/cp_delta54.g (Delta(54)).

## Method (Chen-Fallbacher arXiv:1402.0507)
A group allows physical CP conservation (type-II/III) iff it has a class-inverting
automorphism (an auto u with u(C) ~ C^-1 for every conjugacy class C). No such auto
-> TYPE-I -> CP is geometrically forced by the group structure. Implemented in GAP:
enumerate AutomorphismGroup(G), test each auto against all conjugacy class representatives.

## Results (executed on Anthony's machine, GAP 4.12.1)
- CALIBRATION Delta(27) = SmallGroup(27,3): 11 conjugacy classes, |Aut|=432,
  class-inverting auto EXISTS = false -> TYPE-I. Matches known literature
  (Chen-Fallbacher: Delta(27) is the type-I textbook example). CALIBRATION OK.
- Delta(54) = SmallGroup(54,8) = ((C3xC3):C3):C2: 10 conjugacy classes, |Aut|=432,
  class-inverting auto EXISTS = false -> TYPE-I (CP geometrically forced by group).

## Status: [ESTABLISHED-userrun] BUT this is a REPRODUCTION, NOT a discovery
The result "Delta(54) is type-I" is ALREADY IN THE LITERATURE and our calculation
reproduces it:
- Chen-Fallbacher et al. (arXiv:1402.0507, Nucl.Phys.B 883, 2014): the gCP/type-I framework.
- Ding-Zhou and related (arXiv:1510.03188, 2015): used GAP to show Delta(3n^2) groups
  generally have NO class-inverting automorphism except Z3 and A4. Delta(54) is in this
  series. So "Delta(54) type-I" has been known ~10 years.
- Generalized-CP literature explicitly: "Delta(54) leads to the known structure of
  calculable phases obtained with Delta(27)."
What we have is a CALIBRATED TOOL (capacity), not new physics. Per Anthony's own rule:
reproducing a known result = capability, not revelation.

## What is calibrated and reusable
The GAP class-inverting test is now validated (correct on the Delta(27) known case) and
can classify any SmallGroup as type-I/II. This is a genuine usable capability.

## The ONLY potentially-open question (NOT yet verified, do NOT claim novelty)
The group Delta(54) is type-I, but a CONCRETE MODEL using only a SUBSET of irreps might
escape: the literature (arXiv:1510.03188) notes that "if a model contains only a subset
of irreps for which an automorphism exchanges each with its complex conjugate, one can
impose generalized CP." So the precise question "does the Bora et al. field content
(which specific irreps) inherit the type-I obstruction, or use a CP-allowing subset?" is
NOT answered by the abstract-group calculation. Whether THIS is new requires checking if
anyone has analyzed the Bora model's representation content under the gCP angle.
Status of that sub-question: [CONJECTURE, novelty UNVERIFIED -- check literature first].

## UPDATE 2026-06-14 (b) -- rigorous Bickerstaff-Damhus confirmation + a method lesson
Pushed the test to the proper Chen-Fallbacher / Bickerstaff-Damhus criterion (GAP):
- Aut(Delta54) has 45 involutions; ZERO of them are class-inverting.
- => Delta(54) is TYPE-I, confirmed by the STRONG criterion (no class-inverting
  involution -> no physical global generalized CP). Still a REPRODUCTION of known
  result, but now certified by the correct test, not just the conjugacy-class test.

## METHOD LESSON (important, traced to avoid repeating)
An intermediate run found 216 automorphisms that conjugate all four triplets at the
CHARACTER level, and a buggy twisted-Frobenius-Schur computation returned eps_u = 1/3
for triplets -- an IMPOSSIBLE value (the indicator must be 0 or +-1). That 1/3 was the
tell of a bug (the auto used was not constrained to be an involution; the BD indicator
is only defined for involutions). Corrected by first filtering involutions, then testing
class-inverting. LESSON: "an automorphism conjugates the triplets" is NECESSARY but NOT
SUFFICIENT for physical CP; the sufficient condition is a class-inverting INVOLUTION
(Bickerstaff-Damhus). Do not conflate the two.

## What is settled vs open
- SETTLED [ESTABLISHED-userrun]: Delta(54) abstract group is type-I (0 class-inverting
  involutions / 45). No physical global gCP.
- OPEN [not decided]: whether the SPECIFIC Bora field content (subset of irreps: triplets
  for matter, singlets for Higgs, <=1 doublet) escapes the global obstruction. The global
  test does NOT decide this; a RESTRICTED test (auto conjugating only the present irreps)
  is needed, and must be built carefully -- counting doublets is a literature heuristic,
  the rigorous check is existence of an auto conjugating the actual content.
