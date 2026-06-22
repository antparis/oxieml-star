# FINDINGS 2026-06-18 -- [ESTABLISHED, sandbox->machine] Refinement of the two-field criterion (b992c1ae): a cross-conjugate coupling of TWO fields is NECESSARY but NOT SUFFICIENT. At two points the cross-conjugate coherence Gamma12 = <E1* E2> is RE-LOCKED: its modulus |Gamma12| (visibility) is rephasing-invariant but REAL => reality-lock (a); its phase arg(Gamma12) (fringe position) is REMOVABLE by a reference-phase choice (rephasing) => DECORATIVE, exactly like a 2-flavour CP phase. The first rephasing-INVARIANT (non-removable) appears only at THREE points: the CLOSURE PHASE arg(G12)+arg(G23)+arg(G31), the optical analogue of the Jarlskog invariant. Reconnects to CP/Jarlskog and EHT closure phases.
## Setup (clean van Cittert-Zernike synthetic data, physics-generated, nothing injected)
N=7 independent circular-Gaussian emitters (extended ASYMMETRIC thermal source), observed at M=3
points; coherence Gamma_ij = <E_i* E_j> emerges from propagation, not injected. The result below is
STRUCTURAL (algebraic identity under rephasing), hence robust and not a synthetic artefact.
## Results (executed on Anthony's machine)
Coherence matrix J is Hermitian (J21 = conj(J12)) -- a matrix-level mirror, but it relates DIFFERENT
elements, it does not force Gamma12 to be its own mirror.
 - |g12| = 0.664 : partial coherence (rank-2, two DOF, not collapsed), but the MODULUS is REAL => lock (a).
 - Rephasing E_j -> E_j e^{i phi_j} sends Gamma_jk -> e^{i(phi_k-phi_j)} Gamma_jk. Choosing
   phi2-phi1 = -arg(Gamma12) kills arg(Gamma12) exactly (new arg = 0.00) WITHOUT touching any physical
   data => the 2-point cross-conjugate PHASE is REMOVABLE (gauge/rephasing) => DECORATIVE.
 - Closure phase arg(G12)+arg(G23)+arg(G31) = 0.5302 rad, INVARIANT under random rephasing of all
   three fields (shifts cancel: (phi2-phi1)+(phi3-phi2)+(phi1-phi3)=0) => genuine rephasing-INVARIANT.
 - Control symmetric source: closure phase ~ 0 => the closure phase encodes SOURCE ASYMMETRY.
## Refinement of the criterion
Two independent fields with a cross-conjugate coupling are NOT enough: the cross-conjugate phase is
rephasable (decorative) and the modulus is real (lock a). The correct requirement is a REPHASING-
INVARIANT, and the first one is the CLOSURE PHASE at THREE fields/points -- the optical Jarlskog.
This is the SAME mechanism already established for CP physicality (Jarlskog, rephasing invariance,
NOT d/dz-bar) and is the quantity measured by EHT/VLBI (closure phases).
## Open question (caution, NOT concluded)
The closure phase is nonzero iff the SOURCE is asymmetric, so it encodes the structure of a SINGLE
source object => it may still be "one object seen at three points" (information about a common source),
not the meeting of three independent things. The same dilemma as before, raised one level: nonzero
coherence => common origin => possibly single-object/mirror-locked. EHT was already classified as
Hermitian symmetry V(-z)=conj V(z) (single field + conjugate). TO TEST: can a nonzero closure phase
arise from three GENUINELY INDEPENDENT contributions, or does it always encode a common source?
## Status
[ESTABLISHED, sandbox->machine] -- the rephasing identity and closure-phase invariance are structural
and certified on Anthony's machine. Refines b992c1ae (does not invalidate it). The closure-phase-
encodes-single-source caution is [CONJECTURE], the next thing to test. Reconnects to CP/Jarlskog
(rephasing invariance = physicality) and EHT.
Files: rephasing/closure VCZ test (this session). Arbiter = Anthony's machine (done) + open physical question.
