# FINDINGS 2026-06-18 -- [ESTABLISHED sandbox->machine, NEGATIVE RESULT] First honest test of Anthony's idea "take a reputedly-holomorphic system and check if it hides an anti-holomorphic residue". System chosen: complex potential flow w(z) past a cylinder (natively complex, holomorphic by ideal-fluid theory, NOT a real-field repackaging -- so SPARC-clean). Certified on Anthony's machine (holo_residue_test_flow.py) with the corrected judge (HOLO / REAL-TRAP / ANTI, full-conjugation mirror test): [1] w=U(z+a^2/z) -> HOLO (df/dzbar=0); [2] + circulation -i*Gamma/2pi*log(z) -> HOLO (circulation is still holomorphic); [3] physical velocity v=conj(dw/dz) -> ANTI, but this is the KNOWN conjugate relation (mirror anti, b=conj(a)), NOT an independent hidden residue; [4] GUARD speed^2=|dw/dz|^2 (Bernoulli pressure, real) -> REAL-TRAP; [5] GUARD stream function psi=Im(w) (real) -> REAL-TRAP. The guard BITES: real observables are correctly trapped, not mistaken for anti. VERDICT: the reputedly-holomorphic system is HONESTLY HOLOMORPHIC; no hidden independent anti-holomorphic residue. STRUCTURAL LESSON: a field DERIVED from a holomorphic potential can only yield mirror-anti (b=conj(a), the velocity) or real-trap (real observables), NEVER independent anti. This re-confirms the navigation law from inside a clean complex system. To find a genuine hidden residue, the potential ITSELF must break holomorphy for a PHYSICAL reason (true viscous / non-potential flow, Navier-Stokes vorticity) -- that is the next legitimate target.
## Why this test was SPARC-clean (the method point)
The system is natively complex (the complex potential w=phi+i*psi has intrinsic phase), reputedly
holomorphic for a PHYSICAL reason (ideal flow), not encoded-as-complex by hand. The corrected judge's
mirror test (real-trap iff f==conj(f) under full conjugation) is what makes the negative result
trustworthy: speed^2 and stream function would have been false 'anti' positives under the old judge.
## Tests (executed on Anthony's machine, holo_residue_test_flow.py)
 - [1] ideal potential -> HOLO (df/dzbar=0). [certified]
 - [2] + circulation -> HOLO. [certified]
 - [3] velocity conj(dw/dz) -> ANTI = known mirror relation, NOT a hidden residue. [certified]
 - [4] speed^2 (real) -> REAL-TRAP (guard bites). [certified]
 - [5] stream function (real) -> REAL-TRAP (guard bites). [certified]
## What this answers (Anthony's question)
For THIS reputedly-holomorphic system: NO hidden anti residue. The potential is honestly holomorphic;
its only anti-content is the well-known mirror (velocity=conj of complex velocity); real observables
are correctly real-trapped. A field built from a holomorphic potential cannot hide independent anti.
The honest next step is a system where holomorphy breaks PHYSICALLY (viscous/non-potential flow).
Do NOT overclaim the velocity's definitional anti-ness as a discovery.
## Status
[ESTABLISHED sandbox->machine, NEGATIVE RESULT] reputedly-holomorphic potential flow is honestly
holomorphic; no hidden independent anti; guard (real-trap) bites on real observables. Reconnects:
mirror theorem (real fields mirror-locked); navigation law (independent anti needs natively complex
non-potential object); calibration bench + real-trap fix (a87d9104). Next target = non-potential
viscous flow. Files: holo_residue_test_flow.py. Arbiter = Anthony's machine (done).
