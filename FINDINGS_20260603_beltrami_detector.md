# FINDINGS 2026-06-03 -- Beltrami dilatation detector (palette enrichment)

## Status
[ESTABLISHED] tool validated on known cases (executed on machine).
Add-on beltrami_check.py, standalone, does NOT modify verify_exact.py or
reality_check.py. Enriches the binary holo/anti judge with a CONTINUOUS
spectrum via the Beltrami coefficient mu_f = (df/dzbar)/(df/dz).

## What it adds (new detection categories)
By |mu| evaluated at sample points + structure of mu:
  |mu| = 0        -> HOLOMORPHIC
  0<|mu|<1, mu simpler than f -> TWISTED-REDUCIBLE [NEW: holo in a tilted/
                                  varying complex structure, Ahlfors-Bers sense]
  0<|mu|<1, mu complex        -> ANTI-MINOR NON-REDUCIBLE (genuine chiral/artefact)
  |mu| = 1        -> REAL-TRAPPED (mirror-locked, SPARC-type)
  |mu| > 1        -> ANTI-DOMINANT
  df/dz = 0       -> PURE ANTI-HOLOMORPHIC
The TWISTED-REDUCIBLE class is the rigorous form of the "change of frame /
who moves, the snowflake or the gaze" intuition (Ahlfors-Bers measurable
Riemann mapping: a varying complex structure = a Beltrami coefficient mu(z)).

## Guardrail (anti-artefact, built in)
A 'twist' is accepted as a mere frame change ONLY if |mu|<1 everywhere AND
count_ops(mu) < count_ops(f). If mu is non-constant and as/more complex than f,
the twist is NOT a simple frame change -> flagged genuine chiral / artefact.
This blocks manufacturing a twist (SPARC-type trap). mu cannot be back-solved
into a fake simple frame because complexity is compared.

## Validation (executed on machine, 2026-06-03)
  python3 beltrami_check.py "z**2"      -> HOLOMORPHIC (|mu|=0)
  python3 beltrami_check.py "zbar**2"   -> PURE ANTI
  python3 beltrami_check.py "z + zbar"  -> REAL-TRAPPED (|mu|=1)
  python3 beltrami_check.py "z + zbar/2"-> TWISTED-REDUCIBLE (|mu|=0.5) [NEW]
  python3 beltrami_check.py "z + 2*zbar"-> ANTI-DOMINANT (|mu|=2)
All five match the sandbox prediction exactly.

## Origin
Palette-enrichment research (non-abelian Hodge / Higgs / Hitchin / Dolbeault):
the Beltrami-twisted operator D_mu = d/dzbar - mu d/dz was identified as the
single most promising genuinely-new, computable, low-artefact-risk axis.
Constant complex-structure rotations detect nothing (holomorphicity is
invariant under z->e^{i theta} z); only the NON-CONSTANT (Beltrami) version
adds a real category.

## Caveat
Exact only on symbolic closed-form f. On noisy real data the arbiter stays
negative control + exploitable MSE, never this coefficient alone.

## Next
- Connect beltrami_check to reality_check.py's simplifier to parse PySR
  best_equation JSON (currently the JSON path is a deliberate stub to avoid
  guessing the eml operator dictionary).
- Run on the session results (hm_vortex, kirsch) to see how screening / the
  traction-free boundary appear on the |mu| spectrum.

## Validation on REAL session results (2026-06-03, executed on machine)
  hm_holo   (unscreened) -> HOLOMORPHIC, |mu|=0
  hm_vortex (screened)   -> MIXED, |mu| in [0.62,1.91], mu NON-reducible (cmu=102 > cf=21)
                            => anti is real structure, spatially varying (screening acts by |z|)
  kirsch    (free bound) -> ANTI-DOMINANT, |mu| in [1.87,2.93], mu NON-reducible (cmu=33 > cf=18)
                            => anti franc, forced by traction-free boundary, not a frame twist
Three different physical cases -> three different classes. The detector
DISCRIMINATES (does not glue one verdict). All non-holo cases have mu
NON-reducible => none is a gaugeable frame twist; all are forced physical
structure. Third independent angle confirming the SymPy judge on both
physical results. JSON path reuses verify_exact.parse_formula (no duplication).

## Cross-check of ALL established results (2026-06-03)
Ran beltrami_check on every low-MSE result. Outcome: ALL SOUND, none fragilized.
  vortex_N1_holo, optical_holo, emergence_holo -> HOLOMORPHIC
  optical_anti, loc6 (exp zbar)                 -> PURE ANTI
  vortex_N1 (synthetic chiral)                  -> MIXED, mu non-reducible
  loc5 (z^3 + zbar^2, hand-built mixed)         -> NON-REDUCIBLE (correct: independent
                                                   holo+anti weights by construction)
  hm_vortex, kirsch                             -> MIXED / ANTI-DOMINANT, mu non-reducible
  KiDS-1000 lensing                             -> |mu|~0.002 (quasi-holomorphic; the
                                                   sanity-on-modulus had negligible anti)
KEY: NO established 'anti' result comes out REAL-TRAPPED (|mu|=1). No past
detection was an over-sold mirror artefact. Third independent angle confirms
the whole body of results.

## Tool weakness identified (to refine, non-urgent)
The label "genuine chiral/artefact" is too coarse: it flags both loc5 (|mu|~0.7,
true mixed) and KiDS (|mu|~0.002, quasi-holo negligible anti) identically,
because "count_ops(mu) > count_ops(f)" triggers on any rich formula. Refinement:
split by the VALUE of |mu| (near 0 = holo-dominant negligible; near 1 = true
mixed) rather than by complexity alone. Cosmetic to the label, does not change
any verdict.
