# FINDINGS 2026-06-11 -- CP-judge Stage 1 VALIDATED (executed): Jarlskog + commutator calibrated

## What this is
First EXECUTED brick of the CP-aware judge (a NEW layer, distinct from the Wirtinger
judge verify_exact.py). Origin: deep-research blueprint identified that CP physicality
is a REPHASING-INVARIANT property (Jarlskog J, Bernabeu-Branco-Gronau commutator trace),
NOT a Wirtinger d/dzbar property. Applying d/dzbar naively to a mass-matrix phase gives
FALSE POSITIVES (a removable phase looks "conjugate-dependent"). So CP needs its own layer.
This Stage 1 calibrates that layer on cases with KNOWN answers, before any Delta(54) claim.

## File
cp_judge_stage1.py (74 lines). Run: python3 cp_judge_stage1.py

## Tests and RESULT (executed on Anthony's machine, all PASS)
- TEST 1 Jarlskog: J = c12 c13^2 c23 s12 s13 s23 sin(delta); J(delta=0)=0 exactly. PASS.
- TEST 2 two-generation: Tr[Hu,Hd]^3 = 0 identically (single 2-gen phase always
  removable; judge does NOT false-positive). SPARC test in CP form. PASS.
- TEST 3 three-generation commutator (numeric): Im Tr[Hu,Hd]^3 = 7.35e8 at delta=1.0,
  = 0.0 at delta=0 (cleanly separates FORCED from conserved). PASS.
STAGE 1 VALIDATED.

## Status: [ESTABLISHED] (executed + matches known closed-form answers)
CP-detection core (Jarlskog + Hermitian commutator trace) calibrated. Certifies
CP-conserving cases as removable and CP-violating as forced, on SM/CKM and 2-gen
references where the answer is known analytically.

## Method notes (for reuse)
- Force c^2+s^2=1 via trig_reduce(): SymPy does not auto-apply it.
- Do NOT form the full symbolic 3x3 commutator cube with symbolic masses (timeout);
  use numeric evaluation for the 3-gen commutator (blueprint Part D.6).

## NEXT (cold session, do NOT rush)
- Stage 2: rephasing certifier (PL M PR, differentiate w.r.t. phase symbols) on real
  mass matrices; reproduce known physical-phase count before trusting on Delta(54).
- Stage 3 (delicate): discrete-group gCP module. WARNING: a naive diagonal-phase
  rephasing check is WRONG for Delta(54) (type-I group). Must use generalized-CP
  consistency X rho*(g) X^-1 = rho(u(g)) + twisted Frobenius-Schur indicator. Without
  it, the judge wrongly declares the omega=e^(2pi i/3) Clebsch-Gordan phases removable.
- Stage 4: apply to Bora et al. Delta(54) (arXiv:2305.08963) -- test whether their omega
  phases are physical beyond the fitted PMNS delta (their papers do not address this).

## Pointer
First execution after the structural no-go (FINDINGS_20260610c). Opens the CP /
natively-complex front -- the refuge the no-go left open (intrinsic U(1) phase).
