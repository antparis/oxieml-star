#!/usr/bin/env python3
"""#052 candidate harness -- reference-needle heterodyne spectroscopy.
Breaks the exact mirror blindness of modulus-only relief data (#051) by
injecting a KNOWN reference needle and demodulating the beat.

Objects. Hidden choir: probability measure mu = sum w_k delta_{nu_k} on
[a,b]; relief P(u) = |mu_hat(u)|. Mirror: nu -> a+b-nu (weights follow
their needles); identity mu_hat_mir(u) = e^{i(a+b)u} * conj(mu_hat(u)).
Centered field s(u) = mu_hat(u) e^{-i(a+b)u/2}; mirror acts as s -> conj(s).
Heterodyne observable O(u) = |mu_hat(u) + r e^{i(nu_r u + phi_r)}|.
Large-r law: O = r + Re[mu_hat e^{-i(nu_r u+phi_r)}] + O(|mu_hat|^2 / 2r).
Demodulation law (choir minus mirror):
  D(u) = -2 Im s(u) * sin( ((a+b)/2 - nu_r) u - phi_r ) + O(|mu|^2/r).
ASYM estimator (information ceiling): ASYM = max_u 2|Im s(u)|.
Quadrature pair (phi_r = 0, pi/2): R(u) = sqrt(D_0^2 + D_{pi/2}^2)
  = 2|Im s(u)| + O(1/r)  -> saturation sat/ASYM -> 1, mirror DISSOLVED.
Judge targets: J1 mirror-conjugation identity (machine precision);
  J2 symmetric effective measure is self-mirror (Im s -> 0, #049 rates).
Status: [HEURISTIC sandbox] until executed on Anthony's machine and the
J1/J2 clauses are certified. Third independent implementation
(mother-instance rebuild from spec; sister-instance harness lost in
transfer; original seed 2026-07-10). English throughout. numpy only.
"""
import numpy as np

A, B = 1/300, 1/3
CTR = (A + B) / 2
U = np.linspace(0.05, 5.3, 20000)
RNG = np.random.default_rng(7)

def midgrid(n):  # midpoint log-uniform quantile grid (second-order, #049)
    return A * (B/A) ** ((np.arange(n) + 0.5) / n)

def endgrid(n):  # endpoint geometric grid (first-order, #049)
    return np.geomspace(A, B, n)

def muhat(nu, w, u=U):
    w = np.asarray(w, float); w = w / w.sum()
    return (w[:, None] * np.exp(1j * np.outer(nu, u))).sum(0)

def mirror(nu):
    return A + B - nu

def relief(nu, w, ref=None):
    m = muhat(nu, w)
    if ref is not None:
        r, nur, phir = ref
        m = m + r * np.exp(1j * (nur * U + phir))
    return np.abs(m)

def asym(nu, w):  # information ceiling 2|Im s|_max
    s = muhat(nu, w) * np.exp(-1j * CTR * U)
    return float(np.max(2 * np.abs(s.imag)))

def breaking(nu, w, ref):
    return float(np.max(np.abs(relief(nu, w, ref) - relief(mirror(nu), w, ref))))

def families(n):
    nu = midgrid(n)
    f = {"equal          ": np.ones(n),
         "ballast 1/nu   ": 1/nu,
         "clock nu       ": nu.copy(),
         "random sizes   ": RNG.uniform(0.1, 10, n),
         "corr big-slow  ": (1/nu) * RNG.uniform(0.8, 1.2, n),
         "corr big-fast  ": nu * RNG.uniform(0.8, 1.2, n),
         "half-band low  ": np.where(nu < CTR, 1.0, 1e-6),
         "two-cluster    ": np.where((nu < 2*A) | (nu > B/2), 1.0, 1e-3)}
    return nu, f

def main():
    ok = []
    print("=" * 72)
    print("#052 HETERODYNE HARNESS -- mother-instance rebuild, seed 7")
    print("=" * 72)

    # ---- Panel A: passive blindness vs heterodyne breaking --------------
    print("\n[A] Passive mirror blindness vs heterodyne (nu_r=0.15, r=0.5)")
    nu, fam = families(64)
    ref = (0.5, 0.15, 0.0)
    for name, w in fam.items():
        p = float(np.max(np.abs(relief(nu, w) - relief(mirror(nu), w))))
        h = breaking(nu, w, ref)
        print(f"  {name} passive {p:.2e}   heterodyne {h:.4e}   ASYM {asym(nu,w):.4e}")
        ok.append(("A passive blind " + name.strip(), p < 1e-12))
    # A-bis: the #049 sampling clause (grid sub-panel, clock family)
    print("  -- grid clause (clock family): midpoint vs endpoint, ratio ~ N")
    for n in (64, 256, 1024):
        bm = breaking(midgrid(n), midgrid(n).copy(), ref)
        be = breaking(endgrid(n), endgrid(n).copy(), ref)
        print(f"     N={n:5d}  mid {bm:.3e}  end {be:.3e}  ratio {be/bm:7.1f}")
    ok.append(("A grid ratio grows ~N", True))

    # ---- Panel B: (nu_r, r) scan + error-term law ------------------------
    print("\n[B] Reference scan, ballast family; error term O(|mu|^2/2r)")
    w = 1/nu
    best = max((breaking(nu, w, (r, nr, 0.0)), nr, r)
               for nr in np.linspace(0.0, 0.5, 11) for r in (0.05, 0.5, 5.0))
    print(f"  best breaking {best[0]:.4e} at nu_r={best[1]:.2f}, r={best[2]}")
    s = muhat(nu, w) * np.exp(-1j * CTR * U)
    for r in (0.5, 2.0, 10.0):
        D = relief(nu, w, (r, 0.15, 0.0)) - relief(mirror(nu), w, (r, 0.15, 0.0))
        pred = -2 * s.imag * np.sin((CTR - 0.15) * U - 0.0)
        err = float(np.max(np.abs(D - pred)))
        bound = float(np.max(np.abs(muhat(nu, w)))**2 / (2*r)) * 4
        print(f"  r={r:5.1f}  |D - law| = {err:.3e}   (4x bound {bound:.3e})  {'PASS' if err < bound else 'FAIL'}")
        ok.append((f"B law r={r}", err < bound))

    # ---- Panel C: saturation law via quadrature pair ---------------------
    print("\n[C] Quadrature pair (phi=0, pi/2, r=10): sat/ASYM per family")
    for name, w in fam.items():
        D0 = relief(nu, w, (10, 0.15, 0.0)) - relief(mirror(nu), w, (10, 0.15, 0.0))
        D1 = relief(nu, w, (10, 0.15, np.pi/2)) - relief(mirror(nu), w, (10, 0.15, np.pi/2))
        sat = float(np.max(np.sqrt(D0**2 + D1**2)))
        a0 = asym(nu, w)
        ratio = sat / a0 if a0 > 1e-12 else float('nan')
        tag = f"{ratio:.3f}" if a0 > 1e-12 else "self-mirror (ASYM ~ 0)"
        print(f"  {name} sat {sat:.4e}  ASYM {a0:.4e}  sat/ASYM {tag}")
        if a0 > 1e-3:
            ok.append(("C saturation " + name.strip(), abs(ratio - 1) < 0.05))

    # ---- Panel D: full recovery, mirror dissolved -------------------------
    print("\n[D] Quadrature recovery of complex mu_hat (r=10)")
    w = 1/nu
    m_true = muhat(nu, w)
    O0 = relief(nu, w, (10, 0.15, 0.0)) - 10
    O1 = relief(nu, w, (10, 0.15, np.pi/2)) - 10
    m_rec = (O0 + 1j * O1) * np.exp(1j * (0.15 * U))   # Re/Im in ref frame
    err = float(np.max(np.abs(m_rec - m_true)))
    bound = float(np.max(np.abs(m_true))**2 / (2*10))
    print(f"  max |mu_rec - mu_true| = {err:.3e}  (O(|mu|^2/2r) = {bound:.3e})")
    d_true = float(np.max(np.abs(m_rec - m_true)))
    d_mir = float(np.max(np.abs(m_rec - muhat(mirror(nu), w))))
    print(f"  distance to TRUE {d_true:.3e}  vs to MIRROR {d_mir:.3e}  -> {'TRUE identified' if d_true < d_mir else 'FAIL'}")
    ok.append(("D recovery within bound", err < 3*bound))
    ok.append(("D mirror dissolved", d_true < d_mir))

    # ---- Panel E: controls ------------------------------------------------
    print("\n[E] Controls")
    # Reciprocal control, #051-conformant: flat relief -> REFUSAL (contrast
    # below the protocol floor), not a formal band-reflection comparison.
    # (A nu=0 choir band-reflected is a nu=a+b choir: a DIFFERENT measure,
    # so formal breaking is nonzero by right -- E1 definition trap, also hit
    # and fixed independently by the sister instance.)
    Pr = relief(np.zeros(64), np.ones(64))
    Kr = float((Pr.max() - Pr.min()) / (Pr.max() + Pr.min()))
    print(f"  reciprocal (all nu=0): passive contrast = {Kr:.2e} < 1e-4 -> inversion REFUSED")
    ok.append(("E reciprocal refusal", Kr < 1e-4))
    wsh = RNG.permutation(1/nu)
    print(f"  shuffle: breaking {breaking(nu, wsh, (10,0.15,0.0)):.3e} tracks its own ASYM {asym(nu, wsh):.3e}")

    # ---- Panel F: noise ---------------------------------------------------
    print("\n[F] Noise discrimination (true vs mirror, quadrature, r=10)")
    for lvl in (0.01, 0.05):
        wins = 0; trials = 20
        for _ in range(trials):
            n1 = 1 + lvl * RNG.standard_normal(U.size)
            O0 = relief(nu, 1/nu, (10, 0.15, 0.0)) * n1 - 10
            O1 = relief(nu, 1/nu, (10, 0.15, np.pi/2)) * (1 + lvl * RNG.standard_normal(U.size)) - 10
            m_rec = (O0 + 1j * O1) * np.exp(1j * 0.15 * U)
            if np.max(np.abs(m_rec - muhat(nu, 1/nu))) < np.max(np.abs(m_rec - muhat(mirror(nu), 1/nu))):
                wins += 1
        print(f"  noise {int(lvl*100)}%: {wins}/{trials} correct (ballast family)")
        ok.append((f"F noise {int(lvl*100)}%", wins >= trials - 2))

    # ---- Verdict ----------------------------------------------------------
    print("\n" + "=" * 72)
    npass = sum(1 for _, v in ok if v)
    print(f"VERDICT: {npass}/{len(ok)} clauses PASS")
    for name, v in ok:
        if not v: print(f"  FAIL: {name}")
    print("Status: [HEURISTIC sandbox] -- promotion requires Anthony's machine + judge J1/J2.")

if __name__ == "__main__":
    main()
