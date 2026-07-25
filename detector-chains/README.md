# Detector chains: a Lambert-W lower bound for machine-dependent chairman assignment

**Author:** Angus Muffatti (AI-assisted; see the disclosure in the manuscript).
**Status:** working draft with exact certificates. Not yet peer reviewed, not yet on arXiv.
Companion to [`../chairman-counterexample/`](../chairman-counterexample/), which refutes
Liu–Reis Conjectures 19 and 21 and proves `κ ≥ 4 − 2√2`.

## The result

For machine-dependent weights, let `κ` be the supremum over finite instances of the
minimum over integral assignments of the maximum row/prefix discrepancy, divided by
`D = max d_ij`. Replacing the companion paper's three-column detector by a **chain** of
`k − 1` detector columns and optimizing exactly gives the closed form

```
τ(k) = max over admissible d of  [ d(k − 1 − (k − 2)·d^(1/(k−2))) + 1 ] / (1 + d)
```

with `τ(3) = 4 − 2√2` and

```
lim τ(k) = 1 + W(1/e) ≈ 1.2784645        (W = Lambert W)
```

attained where `ln d* = −(1 + d*)`, at which point `τ = 1 + d*`. Hence
**κ ≥ 1 + W(1/e)**. Every rung is certified in exact rational arithmetic; the deepest
explicit instance (depth 40) forces prefix discrepancy ≥ 1.272743.

The second half of the manuscript reports exactly verified *block-game* results beyond
chains (forced values above 3/2 at stated bank states, bank-manufacturing "shaper"
blocks) together with the measured reasons none of them compose into instances: entry
pollution, accumulator venting, and the failure of conjunctive bank pinning. We
conjecture `κ < ∞` and sketch a scheduler-side route to a matching upper bound.

## Verify

```bash
python3 code/verify_chain_certificate.py    # exact: chain block certificates, all depths
python3 code/verify_kappa_certificate.py    # exact: full-instance bounds, 7 rungs to depth 40
python3 code/verify_block_games.py          # exact: Section 6 block games (stdlib only, no solver)
python3 code/beat_76_instance.py            # independent MILP: 119x236 instance beats 7/6
```

The first three need only the Python standard library and are exhaustive: the block-game
checker searches *all* schedules of each block by branch-and-bound in scaled-integer
arithmetic, so its printed margins are proved properties of finite games, not samples.
`beat_76_instance.py` needs `numpy` + `scipy` (HiGHS) and confirms one concrete instance
by mixed-integer infeasibility.

Expected: seven monotone rungs ending `1.272743`; five block-game claims verified
(`1.687669747`, `0.693059556`, `+0.058804594`, `+0.122824202`, `1.630000000`,
`−0.324240741`); `INFEASIBLE at 7/6`, `feasible at 1.19`.

## Build the paper

```bash
make paper
```

## Contents

- `paper/` — manuscript (`kappa_chains.tex`) and bibliography.
- `code/` — exact verifiers and the independent MILP check.
- `data/` — the block instances used in Section 6, as rational JSON.

## Honest scope

Proof-grade here: the chain closed form, the Lambert-W limit, `κ ≥ 1 + W(1/e)`, and every
number in the certificate table. Exactly verified but **local**: the block games of
Section 6 are statements about single blocks at stated entry states, and they are *not*
lower bounds on `κ` — assembling them into instances is exactly what fails, measurably,
and is reported as such. Superseded intermediate findings from the research sessions
(including two retracted floating-point results) are documented in the private notes and
summarized in the manuscript's disclosure section.
