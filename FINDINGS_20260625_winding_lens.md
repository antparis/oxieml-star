# FINDINGS — winding lens: a global chirality detector complementing the local judge

**Date:** 2026-06-25
**Status:** [HEURISTIC] (sandbox; pending machine arbiter). Capability, NOT an eml* discovery.
**File:** `winding_lens.py` (self-test 9/9 in sandbox).

## Origin
Anthony's "turns/rotations at different scales" intuition. Recovered from history: the
winding/monodromy axis is the project's identified OPEN frontier (the only place a finite 4th
operator could live). New use here: winding as a global DETECTOR, not a reconstruction target.

## Results (sandbox, [HEURISTIC])
1. **Winding = global chirality lens.** Around a loop, winding(f) = signed count of enclosed
   zeros/poles. sign(+)=holo, sign(-)=anti, 0=real-trapped; module z^a zbar^b -> a-b. It is a
   topological integer, so gauge/basis/reality rotations CANNOT change it (the removability
   invariant). Only integer windings; fractional branch monodromy is NOT read by naive
   principal-branch unwrap (stays the singularity_reader's job).
2. **Re-examination of certified walls: winding CONFIRMS them** (real-trapped -> 0, separable
   -> 0, holo-no-zero -> 0, anti -> negative). One refinement: module-trapped carries a
   PROTECTED winding a-b that the local 4-label judge left blurred.
3. **Scale-dependent winding** appears for mixed holo+anti of different orders (e.g. z^2+zbar).
4. **Conjecture REFUTED, then a stronger gate found.** "scale-dependent winding <=> non-
   factorizable (D=d_z d_zbar log f != 0)" is FALSE both ways:
   - z+zbar (real-trapped): D!=0 but winding const 0 -> local discriminant FALSE POSITIVE
     (the known "ChatGPT blind spot"); winding corrects it.
   - z*(zbar+1) (factorizable): D=0 but winding scale-dependent (an off-centre zero crosses the
     loop) -> winding FALSE POSITIVE; discriminant corrects it.
   => Each catches the other's false positive. The CONJUNCTION is the keeper:
        genuine non-removable holo+anti mix  <=>  (D != 0) AND (winding scale-dependent)
   Verified 9/9 on the battery {z^2, conj^2, z*conj, z^2*conj, z+conj, z^2+conj, z+conj^2,
   z*(conj+1), exp(z)+conj}. This COMPLETES the local judge (plugs the z+zbar hole); it does
   not replace it.
5. **Noise.** Raw winding survives only to noise/signal ~ 1 (better than pointwise Wirtinger,
   not immune). For the blizzard regime, scale-bin AVERAGING recovers the coherent chirality
   when N >= (noise/signal)^2 per bin (E/B channels separate cleanly; pure-noise & B-mode nulls
   hold). KiDS (~2e5 galaxies, noise/signal ~ 1e2) is borderline -> consistent with our earlier
   inconclusive E/B (f_B ~ 0.5): we were under the per-bin threshold.

## NOT the cube replaced
Winding is a GLOBAL lens complementing the LOCAL Wirtinger judge; the cube classification stands.

## Open / next (machine)
- Validate winding_lens.py self-test on Anthony's machine (arbiter).
- Apply the conjunction gate to PHYSICAL candidates (needs 2-field f(z1,zbar2) loop framing,
  e.g. non-reciprocal EP log(z1 - zbar2)).
- Real KiDS ellipticities (e1+ie2, FITS on Mac): scale-bin averaging per the N >= (noise/sig)^2
  rule -- heavy, borderline feasible.
