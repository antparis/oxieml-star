# FINDINGS 2026-06-23 — Orthogonal-axis LCFT sweep (systematic)

**Status:** [ESTABLISHED] for the 12 judge verdicts · [DERIVATION/LIMIT] for the structural conclusion.

## What was tested

Systematic application of the **orthogonal axis** (conformal spin `s = h - hbar`) to the
full set of resolved, parity-broken (or spinful-log candidate) LCFT two-point closed forms,
certified in a single run by `judge_v2` against an independent Wirtinger oracle.

Target of the axis: a **spinful** (`h != hbar`, `hbar != 0`) **UNPAIRED** log operator
(`b != bbar`) — the only corner escaping the three walls (real / module / observable).

Established criterion replayed (FINDINGS_20260622r) for
`f = z^(-2h) * zbar^(-2hbar) * (a + b*log z + bbar*log zbar)`:
- paired log (`b = bbar` -> `log|z|^2`) -> MODULE_TRAPPED (transcendental but removable)
- unpaired log (`b != bbar`) -> genuine ANTI (requires physical parity breaking)

## Exact command

```
cd ~/Desktop/oxieml-star && python3 lcft_orthogonal_sweep.py; echo "EXIT=$?"
```

## Raw result (judge_v2, this machine)

```
judge vs oracle: 12/12 agree
EXIT=0
chiral cell filled by any swept form: NO -- cell remains EMPTY
```

| id                | judge          | physical source                          |
|-------------------|----------------|------------------------------------------|
| ctrl_holo         | HOL            | control                                  |
| ctrl_anti         | ANTI           | control                                  |
| ctrl_real         | REAL_TRAPPED   | control (SPARC)                          |
| ctrl_module       | MODULE_TRAPPED | control (eml0 phase)                     |
| tmg_left          | HOL            | TMG/NMG/GMG t(z) log partner of T        |
| tmg_parity_img    | ANTI           | parity image (half-chiral wall)          |
| tmg_full_local    | MODULE_TRAPPED | TMG full local (spinful prefactor)       |
| jordan_r2_scalar  | REAL_TRAPPED   | universal rank-2 Jordan (scalar)         |
| jordan_r2_spin    | MODULE_TRAPPED | universal rank-2 Jordan (spinful)        |
| ttbar_r3_c0       | REAL_TRAPPED   | TTbar rank-3 Jordan c=0                   |
| target_unpaired   | ANTI           | TARGET spinful-unpaired (no phys.)       |
| target_asym       | ANTI           | TARGET spinful-asymmetric (no phys.)     |

All 12 judge verdicts equal the independent oracle. **[ESTABLISHED]**

## Structural conclusion — [DERIVATION/LIMIT]

The physically-realized logarithm in every resolved candidate appears **either** as
`log|z|^2` (paired -> MODULE_TRAPPED, or REAL_TRAPPED if scalar) **or** as chiral-pure
`log z` (stress-tensor Jordan sector, `hbar = 0` -> HOL). Consequences:

1. **The whole 3D/4D massive-gravity family closes as one block.** TMG/NMG/GMG/extended
   and tricritical NMG / 4d critical gravity all carry the log operator in the same sector:
   the Jordan partner of the stress tensor `T(z)`, weight `(2,0)`, `hbar = 0` -> holomorphic.
   TMG was not isolated; it is the representative of a uniformly-failing family.
2. **The universal rank-2 Jordan block pairs the log.** `<O_i O_j> = c/|x|^(2D) [[log|x|^2,1],[1,0]]`
   gives `log|z|^2` (paired) -> MODULE_TRAPPED (spinful prefactor) or REAL_TRAPPED (scalar).
3. **Rank-3 TTbar at c=0** is dimension `(4,4)`, spin 0, log paired -> REAL_TRAPPED.

The spinful-unpaired ANTI target (`target_unpaired`, `target_asym`) is a **genuine** form,
certified ANTI, but is **not produced by any resolved physical LCFT swept here**.

**Deep cause (DERIVATION):** the reality condition on the full boundary correlator pairs the
two logarithms mechanically; the parity that desymmetrizes the log (TMG) lodges the whole
log operator in a single chiral sector. "Spinful" and "unpaired log" are in structural tension
in resolved LCFTs.

**Chiral cell remains EMPTY.** Same observable wall reached from an independent angle
(3D gravity vs modular forms vs Zwegers completion).

## Remaining open door (not closed by this sweep)

A **resolved** LCFT whose log operator is itself **spinful** (`hbar != 0`) and **not** the
stress-tensor partner. Reconnaissance suggests the boundary reality condition pairs the logs,
so the door is probably closed — but no closed form has yet certified this. Next reconnaissance.

## Holo / anti ledger update

- holo confirmed: tmg_left (stress-tensor log sector), ctrl_holo.
- anti confirmed (form-level, not physically forced in measurable observable):
  tmg_parity_img (half-chiral wall), target_unpaired, target_asym.
- walls reconfirmed: REAL_TRAPPED (jordan_r2_scalar, ttbar_r3_c0), MODULE_TRAPPED
  (tmg_full_local, jordan_r2_spin).

## Files

- `lcft_orthogonal_sweep.py` (harness, sha256 below)
- this trace
