# FINDINGS 2026-06-22s -- TMG / chiral-gravity LCFT does NOT fill the chiral cell

Status: [ESTABLISHED] for the four judge verdicts (executed + certified on machine).
        [DERIVATION/LIMIT] for the conclusion (chiral cell empty; spinful vs unpaired-log tension).

## Question
Live frontier: find a CLOSED-FORM spinful correlator of a PARITY-BROKEN LCFT carrying
an UNPAIRED log(zbar), pass it to judge_v2 (CERTIFIER mode). The structurally-correct
solved candidate is topologically massive gravity (TMG) at the chiral point.

## Literature inputs
- Generic LOCAL (bulk) LCFT is parity-symmetric: the chiral-halves rule replaces each
  log(z) by log|z|^2 and each power by |z|^(2mu), giving equal h=hbar and equal Jordan
  level (Flohr, hep-th/0111228) -> PAIRED -> module/real-trapped. No escape.
- TMG at mu*l=1 is dual to a c=0 LCFT with c_L=0, c_R=3l/G, b=-3l/G (Skenderis-Taylor-van
  Rees 0906.4926). Parity broken: c_L != c_R. The stress-tensor log partner t has weight
  (h,hbar)=(2,0): the Jordan cell sits in ONE chiral sector. Standard c=0 LCFT 2-point
  <t(z)t(0)> ~ (theta - 2b log z)/z^4 -> function of z only.

## Exact command
    cd ~/Desktop/oxieml-star && python3 certify_tmg_lcft.py
sha256(certify_tmg_lcft.py) = 95aaa34ec968be4a972395332ba3d3203be9972a1cb436fd216938b425455707

## Raw result (judge_v2 on machine)
4/4 judge == oracle == expected.
  TMG chiral-left   (theta-2b log z)/z^4        (h,hbar)=(2,0) -> holomorphic    PASS
  TMG parity-image  (theta-2b log zbar)/zbar^4  (h,hbar)=(0,2) -> anti-holo      PASS  (chiral half)
  TMG full-local    zbar^-2*(...)/z^4           (h!=hbar)      -> module-trapped PASS
  TARGET unpaired   z^-2 zbar^-1 (1+log zbar)   (NOT in TMG)   -> anti-holo      PASS

## Conclusion -- [DERIVATION/LIMIT]
The only SOLVED parity-broken LCFT (TMG / chiral gravity) does NOT fill the chiral cell.
Its transcendental log sits on a weight-(2,0) sector:
  - chiral correlator  = HOLOMORPHIC (eml), log z;
  - parity image       = pure ANTI but a chiral half (observable wall);
  - full local         = MODULE-trapped (holomorphic log x spinful removable power).
The qualifying escape form (spinful prefactor h!=hbar both nonzero  x  UNPAIRED log zbar)
is real and judge-anti, but TMG does not produce it.

STRUCTURAL TENSION (the sharpened wall): "spinful" (both weights nonzero) and "unpaired
log" (parity broken) pull in opposite directions in solved LCFTs. The parity breaking that
desymmetrizes the log puts the whole logarithmic operator into ONE chiral sector.
Having both simultaneously seems to require an UNSOLVED object (integer quantum Hall bulk
transition: no closed form). Same observable wall as the Zwegers / mock-modular route
(FINDINGS 20260622i "escapes wall formal") and the 2026-06-16 conjecture, reached from an
independent angle (3D gravity vs modular forms). Chiral cell remains EMPTY.

## Files
certify_tmg_lcft.py (this repo).
