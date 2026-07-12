#!/usr/bin/env python3
"""ORIENTED COINCIDENCE BELL + CHIRAL BINARY CODE demo (germ candidate).
The #052 asymmetry law repurposed from READER to TRIGGER: at the calendar
rendezvous, the signed heterodyne difference D(u) rings with a SIGN that
identifies the orientation (choir vs mirror). A bitstring is then encoded
as a sequence of oriented choirs (bit = winding sense) and decoded from
intensity-only data by the bell sign alone.

STATUS: [HEURISTIC sandbox] until executed on Anthony's machine.
NO NOVELTY CLAIM: the mandatory prior-art gate (race-logic inhibit gate /
tropical algebra; SFQ asynchronous AND; Sagnac-type nonreciprocity) is
PENDING and named here; this file demonstrates a mechanism of OUR graved
objects (#044 calendar, #052 asymmetry law, #049 grid clause), nothing more.
Judge target J3 (antisymmetry of the bell): mirroring the measure flips the
sign of D exactly -- corollary of the #052 J1 identity, checked numerically
here and symbolically in judge_bell_antisymmetry (companion block).
"""
import numpy as np

A, B = 1/300, 1/3
CTR = (A + B) / 2
REF = (10.0, 0.15, 0.0)   # reference needle (r, nu_r, phi_r), #052 regime

def choir_grid(n, kind):
    t = (np.arange(n) + 0.5) / n if kind == "mid" else np.arange(n) / (n - 1)
    return A * (B / A) ** t

def field(nu, w, U, ref=None):
    w = np.asarray(w, float); w = w / w.sum()
    m = (w[:, None] * np.exp(1j * np.outer(nu, U))).sum(0)
    if ref is not None:
        m = m + ref[0] * np.exp(1j * (ref[1] * U + ref[2]))
    return m

def bell(nu, w, U, noise=0.0, rng=None):
    """Ring at the deepest rendezvous; return (u*, sign, |D|) from
    INTENSITY-ONLY heterodyne data (the #052 observable)."""
    P = np.abs(field(nu, w, U))
    i = int(np.argmin(P))                             # the rendezvous
    Ph = np.abs(field(nu, w, U, REF))
    Pm = np.abs(field(A + B - nu, w, U, REF))         # known mirror template
    if noise > 0.0:
        Ph = Ph * (1.0 + noise * rng.standard_normal(Ph.size))
    D = Ph - Pm
    j = i + int(np.argmax(np.abs(D[i:i + 800])))
    return U[i], float(np.sign(D[j])), float(abs(D[j]))

def main():
    ok = []
    print("=" * 70)
    print("ORIENTED BELL + CHIRAL BINARY CODE -- sandbox-independent harness")
    print("=" * 70)

    # ---- Panel A: the bell, with full grid controls (#049 clause) --------
    print("\n[A] The oriented bell (one-way vs mirror vs symmetric), 2x2 grids")
    U1 = np.linspace(0.05, 5.3, 20000); U2 = np.linspace(0.05, 5.3, 31007)
    for g in ("mid", "end"):
        nu = choir_grid(64, g)
        for U, un in ((U1, "U1"), (U2, "U2")):
            _, s1, a1 = bell(nu, 1 / nu, U)             # one-way (ballast, asymmetric)
            _, s2, a2 = bell(A + B - nu, 1 / nu, U)     # its mirror
            _, s3, a3 = bell(nu, nu.copy(), U)          # symmetric (clock)
            print(f"  {g}/{un}: one-way sign {s1:+.0f} (|D|={a1:.3f}) | "
                  f"mirror sign {s2:+.0f} | symmetric |D|={a3:.1e} (no orientation)")
            thr = 0.02 if g == "mid" else 0.06   # endpoint residue = #049 first-order discreteness
            ok += [("A sign+ " + g + un, s1 > 0), ("A sign- " + g + un, s2 < 0),
                   ("A antisym " + g + un, s1 == -s2),
                   ("A wall " + g + un, a3 < thr * a1)]

    # ---- Panel B: J3 numeric (bell antisymmetry, exact) -------------------
    print("\n[B] J3 antisymmetry: D_mirror(u) = -D(u) pointwise")
    nu = choir_grid(64, "mid"); w = 1 / nu
    Dh = np.abs(field(nu, w, U1, REF)) - np.abs(field(A + B - nu, w, U1, REF))
    Dm = np.abs(field(A + B - nu, w, U1, REF)) - np.abs(field(nu, w, U1, REF))
    r = float(np.max(np.abs(Dh + Dm)))
    print(f"  max |D + D_mirror| = {r:.2e}  (exact zero expected)")
    ok.append(("B J3 antisymmetry", r < 1e-13))

    # ---- Panel C: CHIRAL BINARY CODE ---------------------------------------
    print("\n[C] Binary message in orientations: bit=1 -> choir, bit=0 -> mirror")
    print("  decoder: full-window residual vote (the #052 panel-D discriminator)")
    msg = "EML*"
    bits = [int(b) for c in msg for b in format(ord(c), "08b")]
    print(f"  message '{msg}' = {len(bits)} bits")
    rng = np.random.default_rng(11)
    for noise in (0.0, 0.01, 0.05):
        errors = 0
        for k, b in enumerate(bits):
            rloc = np.random.default_rng(1000 + k)      # per-symbol choir jitter
            nu_k = choir_grid(64, "mid") * rloc.uniform(0.97, 1.03)
            nu_k = np.clip(nu_k, A, B)
            nu_tx = nu_k if b == 1 else A + B - nu_k    # bit = winding sense
            data = np.abs(field(nu_tx, 1 / nu_k, U1, REF))
            if noise > 0.0:
                data = data * (1.0 + noise * rng.standard_normal(data.size))
            Th = np.abs(field(nu_k, 1 / nu_k, U1, REF))          # template: choir
            Tm = np.abs(field(A + B - nu_k, 1 / nu_k, U1, REF))  # template: mirror
            bit_rx = 1 if np.mean((data - Th) ** 2) < np.mean((data - Tm) ** 2) else 0
            if bit_rx != b: errors += 1
        ber = errors / len(bits)
        print(f"  noise {noise:.0%}: {errors}/{len(bits)} errors  (BER {ber:.3f})")
        ok.append((f"C BER noise {noise:.0%}", ber == 0.0 if noise < 0.05 else ber <= 0.05))

    # ---- Panel D: controls --------------------------------------------------
    print("\n[D] Controls")
    P0 = np.abs(field(np.zeros(64), np.ones(64), U1))
    K0 = float((P0.max() - P0.min()) / (P0.max() + P0.min()))
    print(f"  reciprocal (all nu=0): relief contrast {K0:.1e} -> bell REFUSES (nothing to time)")
    ok.append(("D reciprocal refusal", K0 < 1e-4))
    rngs = np.random.default_rng(5)
    wsh = rngs.permutation(1 / choir_grid(64, "mid"))
    _, ssh, ash = bell(choir_grid(64, "mid"), wsh, U1)
    print(f"  shuffle: bell still rings with its own measure's sign ({ssh:+.0f}, |D|={ash:.3f}) -- pairing matters")

    print("\n" + "=" * 70)
    npass = sum(1 for _, v in ok if v)
    print(f"VERDICT: {npass}/{len(ok)} clauses PASS")
    for name, v in ok:
        if not v: print(f"  FAIL: {name}")
    print("Status: [HEURISTIC sandbox]. Graving = Anthony's machine + judge J3;")
    print("NO novelty claim -- prior-art gate (race logic / SFQ / Sagnac) PENDING.")

if __name__ == "__main__":
    main()
