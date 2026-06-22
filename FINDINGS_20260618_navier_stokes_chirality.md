# FINDINGS 2026-06-18 -- [ESTABLISHED sandbox->machine, NEGATIVE RESULT + TOOL LIMITATION] Real Navier-Stokes solutions do NOT hide independent anti-holomorphic chirality, AND the Beltrami sieve has a periodicity blind spot (found by a control). Two results. (A) NAVIER-STOKES WALL: tested four exact NS solutions (Lamb-Oseen, Burgers, Taylor-Green, Kovasznay) with the conjugate velocity w=vx-i*vy, control = ideal point vortex (w=-iGamma/2pi z, HOLO, mu=0). Viscous VORTICES (Lamb-Oseen, Burgers) are MODULE-TRAPPED: their breaking factor is a real radial Gaussian exp(-|z|^2/...), |mu| is RADIAL (d/dtheta=0), reducible -- same category as Aharonov-Bohm (the anti is carried entirely by a real function of |z|^2=z*zbar). DIRECTIONAL flows (Taylor-Green, Kovasznay) initially looked like candidates (|mu| direction-dependent), but FELL to the periodicity control (B). So: NO independent chiral anti-holomorphic structure in these Navier-Stokes solutions; viscosity breaks holomorphy only through real radial moduli or periodic patterns, both reducible. The wall holds for real Navier-Stokes. (B) TOOL LIMITATION (the important find): the Beltrami sieve (|mu| direction-dependent => chiral, established 2026-06-04) has a PERIODICITY BLIND SPOT. Control [P]: a periodic but ACHIRAL standing-wave stream function psi=cos(x)cos(y) ALSO shows direction-dependent |mu| -- so passing Beltrami does NOT distinguish chirality from mere spatial periodicity. Control [P2]: a travelling wave exp(i(x+y)), chiral BY CONSTRUCTION, shows RADIAL |mu| -- so the sieve even MISSES genuine chirality on periodic systems. The Beltrami sieve is unreliable on periodic fields (false positive on achiral-periodic, false negative on chiral-periodic). This blind spot was caught by the control BEFORE it could validate Taylor-Green/Kovasznay as a false discovery.
## Auditor note (the guard worked)
The session nearly produced a false discovery: Taylor-Green and Kovasznay passed the Beltrami sieve
and looked like the first physically-realized independent chiral anti. The periodicity control [P]
(an achiral periodic field that ALSO passes) revealed the pass was an artefact. Lesson reaffirmed: a
sieve must be validated against a control that SHOULD fail; on periodic systems Beltrami does not
discriminate periodicity from chirality. Earlier mistakes this thread (mirror test too weak, plain
ANTI verdict meaningless until split mirror/module/independent) were also corrected before tracing.
## Tests (executed on Anthony's machine via sandbox-verified scripts)
 - CONTROL point vortex w: HOLO (mu=0). [certified]
 - Lamb-Oseen, Burgers: |mu| RADIAL (d/dtheta=0) -> module-trapped, reducible. [certified]
 - Taylor-Green, Kovasznay: |mu| direction-dependent BUT periodicity control [P] also direction-dep
   -> artefact, not chirality. real-trap test: not real (False); mixed-deriv: entangled (but moot
   given the periodicity artefact). [certified]
 - CONTROL [P] achiral standing wave cos(x)cos(y): direction-dependent (FALSE POSITIVE -> sieve flaw).
 - CONTROL [P2] travelling wave exp(i(x+y)) (chiral): RADIAL (FALSE NEGATIVE -> sieve flaw). [certified]
## What this answers (Anthony's question: does a viscous/non-potential flow hide independent anti?)
NO for the tested Navier-Stokes solutions. Vortices = module-trapped (radial |z|^2 factor, like
Aharonov-Bohm). Directional/periodic flows = periodicity artefact, not chirality. The wall holds for
real Navier-Stokes. The genuine yield is a TOOL finding: Beltrami |mu| is not a reliable chirality
test on periodic systems and needs a periodicity-aware refinement before reuse on periodic fields.
## Status
[ESTABLISHED sandbox->machine, NEGATIVE RESULT] Navier-Stokes solutions hide no independent chiral
anti (vortices module-trapped; directional flows periodicity-artefact). [TOOL LIMITATION] Beltrami
sieve has a periodicity blind spot (false pos on achiral-periodic, false neg on chiral-periodic),
demonstrated by controls. Reconnects: module-trapped category + Beltrami criterion (2026-06-04);
navigation law (independent anti needs natively complex object); calibration bench (a87d9104);
potential-flow negative (958e64d5). Next: a periodicity-aware chirality test; or natively-complex
non-fluid systems. Files: sandbox scripts (Beltrami sieve + periodicity controls). Arbiter = Anthony's machine.
