# AUDIT 2026-07-11 — Oriented coincidence bell + chiral binary code (decision-rhythm germ)

Auditor: Cowork sandbox instance. I did NOT write the harness
(kernel_oriented_bell_test.py, 124 lines, from the mother instance) and I
have NOT seen its source — only Anthony's run output. This audit therefore
certifies the CLAIMS (reproduced independently from my own #052 machinery),
NOT the source code. Status of every item below: [HEURISTIC sandbox].

## 1. Independent reproduction — PASS, three-way convergence

Rebuilt the four panels from my #052 relief machinery (band [1/300,1/3],
N=64 ballast, window [0.05,5.3], reference nu_r=0.15 r=10). Results match
Anthony's machine to the digit:
- [A] bell sign: one-way +1 (|D|max 0.131), mirror -1, symmetric choir
  mute (3.6e-15, no orientation).
- [B] J3 antisymmetry: max |D + D_mirror| = 3.55e-15 (exact zero).
- [C] binary message in orientation, residual-vote decode: BER 0.000 at
  0% / 1% / 5% noise (my 'EML*' 32-bit run).
- [D] reciprocal (all nu=0): contrast 0 -> bell refuses.
Third independent implementation (his machine / mother / this sandbox) —
convergent. The claims are real as stated.

## 2. Adversarial audit — what is NEW vs what is #052 re-dressed

This is the deflationary core. The harness is internally sound but its
novelty is narrower than the panel names suggest.

[B] J3 (D_mirror = -D) is a COROLLARY of the #052 law, hand-provable:
D(u) = -2 Im s(u) sin(((a+b)/2 - nu_r)u); the mirror sends s -> conj(s),
hence Im s -> -Im s, hence D -> -D. Clean, judge-targetable (call it J3),
but it is a consequence of the already-graved #052 mechanism, not
independent physics. The exact 0.00 is a re-confirmation of #052.

[C] binary code is an APPLICATION of #052 panel D. "bit=1 -> choir,
bit=0 -> mirror, decode by residual vote" is exactly #052's mirror
discriminator used per symbol. BER 0 at 5% is EXPECTED — #052 already
dissolved the mirror (40/40 discrimination). This demonstrates the
instrument can carry bits; it is not a new law. CAUTION (claim-scale
brake, mandatory): do not read [C] as "a communication system was
discovered." It is #052 used as a channel.

[A] the oriented bell = a THRESHOLD on the #052 continuous readout: the
"bell sign" is sign(net signed area of D), and its flip under mirror is
just J3. The eml0 / modulus-wall reading (my framing) is the
INTERPRETATION of that threshold as a decision surface; the harness
realizes the decision as a sign, which is legitimate but is
thresholded-#052, not a new mechanism.

Net: the germ is a COROLLARY (J3) + an APPLICATION (binary channel,
decision threshold) of #052. Genuinely useful, internally consistent,
predicted-then-confirmed (my rhythm framing's P-dec called the
orientation-selective decision before this run) — but instrument-scale,
and arguably a corollary of #052 rather than a standalone law. Whether it
earns its own registry number or a corollary note under #052 is for the
mother instance / Anthony to arbitrate; my auditor position is: corollary,
unless there is independent content I cannot see in the unseen source.

## 3. Prior-art gate — now DONE (the harness flagged it PENDING), deflationary

The generic ideas are all walls:
- Decision-by-timing / first-arrival-decides: RACE LOGIC (UCSB, ISCA'14)
  and temporal computing (NIST) compute by the timing of wavefronts;
  first arrival is the decision. [race logic ISCA'14; NIST temporal
  computing]
- Pulse-timing decision hardware: RAPID SINGLE FLUX QUANTUM (RSFQ)
  superconducting pulse logic, arbiters, schedulers — decisions by pulse
  arrival/coincidence. [Wikipedia RSFQ; SFQ crossbar scheduler]
- Chirality / orientation from counter-propagating waves: the SAGNAC
  interferometer and the laser/fibre-optic GYROSCOPE sense rotation
  (an orientation) from counter-propagating beams; "chiral laser
  gyroscopes breaking the lock-in limit" is current (Nature 2026).
  [Sagnac effect; laser gyroscope]

SAGNAC IS THE CLOSEST NEIGHBOR and must be cited prominently in any
write-up: it already reads an orientation from counter-propagating
(counter-winding) waves. The ONLY non-generic thread left after this gate:
the eml-star bell reads orientation from MODULUS-ONLY relief data plus a
known reference note, in LOGARITHMIC scale, from a SELF-GENERATED
(hierarchy-free) chiral rendezvous — where Sagnac needs phase-sensitive
interferometric readout and an external rotation. That distinction is the
sole "apparently new" candidate (only allowed word, and only after this
gate), and it is INSTRUMENT-scale, not revolution-scale.

## 4. What I could not audit

- The 124-line source (unseen): I cannot check for hardcoded verdicts or
  rigged clauses. The 21/21 PASS should be taken as Anthony's machine
  output, cross-checked by my independent reproduction of the CLAIMS, but
  the SOURCE itself still wants a read (mother instance or a paste to me).
- Judge certification of J3 (D_mirror = -D exact) in SymPy — not run here;
  it is a one-line corollary of the #052 mechanism and should be trivial.

## 5. Recommendation

Grave nothing new as a standalone law on this alone. Options for the
mother instance: (a) a COROLLARY note under #052 (J3 antisymmetry +
"the instrument carries an orientation bit / decision threshold"), with
the race-logic/SFQ/Sagnac gate recorded; or (b) if independent content
exists in the source I have not seen, a germ number with the deflationary
gate attached and Sagnac cited. Either way: no novelty claim beyond
"apparently new", Sagnac cited, claim-scale = instrument. The project's
main gate (v3 re-read, then deposit) is untouched by this thread.
