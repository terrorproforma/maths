#!/usr/bin/env python3
"""Exact rational (Fraction) full-instance lower bounds breaking 1 + W(1/e):

Certifies three progressively stronger families of support-2, strictly positive
machine-dependent chairman instances, all with D = max d_{ij} = 1:

  1. L-level Fresh Cascade (A -> H_1 -> ... -> H_L):
       supremum = 1 + 1/e  approx 1.3678794412   (beats 1 + W(1/e) approx 1.27846454)
  2. L-level 2-Row Ping-Pong Cascade (A <-> H, only 2 fresh rows per block!):
       supremum = 1 + W(1) approx 1.5671432904   (Omega constant + 1)
  3. Recursive Binary-Tree Splitting + Ping-Pong:
       supremum = 1 + ln 2 approx 1.6931471806

Every certificate re-derives from scratch in exact fractions.Fraction arithmetic:
  - Every split x_j in [0, 1] and every weight d_j in (0, 1];
  - Every prefix deviation height along every level of every branch;
  - Every active-row drain and passive-row gain;
  - Every binary-split lower bound on BOTH child rows (including off-support dumps);
  - Exact worst-case eta off-support bookkeeping across all N blocks;
  - Final accumulator discrepancy LB_B = N*p - (total_cols - N)*eta.

Standard library only (fractions.Fraction).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass
class ChainLevel:
    dws: list[F]
    xs: list[F]
    drain: F
    gain: F
    min_dev: F


def build_and_verify_level(alpha_in: F, c: F, k: int, r: F) -> ChainLevel:
    """Construct geometric chain level of depth k (k-1 columns) with ratio r,
    starting active height alpha_in, deviation target c, and verify every inequality exactly.
    """
    assert k >= 3 and F(0) < r < F(1)
    dws = [r ** (k - j) for j in range(2, k)] + [F(1)]
    d2 = dws[0]
    x2 = (c - alpha_in) / d2
    assert F(0) <= x2 <= F(1), (
        f"Inadmissible x2={float(x2):.6f} (c={float(c)}, alpha_in={float(alpha_in)}, d2={float(d2)})"
    )
    xs = [x2] + [r] * (k - 2)
    for dj, xj in zip(dws, xs):
        assert F(0) < dj <= F(1)
        assert F(0) <= xj <= F(1)

    drain = F(0)
    min_dev = None
    for dj, xj in zip(dws, xs):
        dev = alpha_in - drain + dj * xj
        min_dev = dev if min_dev is None else min(min_dev, dev)
        drain += dj * (F(1) - xj)
    gain = sum(F(1) - xj for xj in xs)
    assert min_dev == c, f"min_dev={min_dev} != c={c}"
    return ChainLevel(dws=dws, xs=xs, drain=drain, gain=gain, min_dev=min_dev)


def choose_r_rational(gap: F, k: int, denom: int = 2000) -> F:
    """Choose a rational r = num/denom in (0, 1) with r^(k-2) >= gap (adaptive denom)."""
    m = k - 2
    assert F(0) < gap < F(1)
    approx = float(gap) ** (1.0 / m)
    while True:
        num = max(1, int(math.floor(approx * denom)))
        while num < denom and F(num, denom) ** m < gap:
            num += 1
        if num < denom:
            return F(num, denom)
        denom *= 4
        assert denom <= 10**9, f"gap={float(gap)} too close to 1 for k={k}"


def certify_fresh_cascade(c: F, L: int, k_per_level: int, p: F, N: int, eta: F) -> tuple[F, int, int]:
    """Certify an L-level fresh cascade (A -> H_1 -> ... -> H_L) full instance."""
    alpha = F(1)
    levels: list[ChainLevel] = []
    for _ in range(L):
        gap = c - alpha
        if gap <= 0:
            break
        r = choose_r_rational(gap, k_per_level)
        lvl = build_and_verify_level(alpha, c, k_per_level, r)
        levels.append(lvl)
        alpha = lvl.gain

    assert alpha >= c, f"Fresh cascade did not reach c={float(c)}: alpha_L={float(alpha):.6f}"

    block_cols = 1 + sum(len(lvl.dws) for lvl in levels)
    total_cols = N * block_cols
    rows_per_block = len(levels) + 1
    total_rows = 1 + N * rows_per_block

    # Re-simulate worst-case lower bounds with (p, eta) included:
    # A enters at 1 - p - total_cols * eta; each H_r enters Level r+1 at >= lvl_r.gain - total_cols * eta.
    forcing_lb = min(c - p - total_cols * eta, alpha - total_cols * eta)
    accum_lb = N * p - (total_cols - N) * eta
    return min(forcing_lb, accum_lb), total_rows, total_cols


def certify_pingpong(c: F, k_lev: int, p: F, N: int, eta: F, max_levels: int = 250) -> tuple[F, int, int, int]:
    """Certify a 2-row ping-pong cascade (A <-> H) full instance."""
    a_cur, h_cur = F(1), F(0)
    levels: list[tuple[str, ChainLevel]] = []
    active = "A"
    for _ in range(max_levels):
        val_act = a_cur if active == "A" else h_cur
        gap = c - val_act
        if gap <= 0:
            break
        r = choose_r_rational(gap, k_lev)
        lvl = build_and_verify_level(val_act, c, k_lev, r)
        if active == "A":
            a_cur -= lvl.drain
            h_cur += lvl.gain
        else:
            h_cur -= lvl.drain
            a_cur += lvl.gain
        levels.append((active, lvl))
        if max(a_cur, h_cur) >= c:
            break
        active = "H" if active == "A" else "A"

    peak = max(a_cur, h_cur)
    assert peak >= c, f"Ping-pong did not reach c={float(c)}: peak={float(peak):.6f}"

    block_cols = 1 + sum(len(lvl.dws) for _, lvl in levels)
    total_cols = N * block_cols
    total_rows = 1 + 2 * N

    # Re-simulate exact adversarial lower bounds with (p, eta):
    a_real = F(1) - p - total_cols * eta
    h_real = -total_cols * eta
    worst_forcing = None
    for act, lvl in levels:
        drain = F(0)
        if act == "A":
            for dj, xj in zip(lvl.dws, lvl.xs):
                dev = a_real - drain + dj * xj
                worst_forcing = dev if worst_forcing is None else min(worst_forcing, dev)
                drain += dj * (F(1) - xj)
            a_real -= drain
            h_real += lvl.gain
        else:
            for dj, xj in zip(lvl.dws, lvl.xs):
                dev = h_real - drain + dj * xj
                worst_forcing = dev if worst_forcing is None else min(worst_forcing, dev)
                drain += dj * (F(1) - xj)
            h_real -= drain
            a_real += lvl.gain
    forcing_lb = min(worst_forcing, max(a_real, h_real))
    accum_lb = N * p - (total_cols - N) * eta
    return min(forcing_lb, accum_lb), len(levels), total_rows, total_cols


def certify_binary_tree(c: F, k_split: int, k_pp: int, p: F, N: int, eta: F) -> tuple[F, int, int, int, int]:
    """Certify a Recursive Binary-Tree Splitting + Ping-Pong full instance.
    Splits automatically until h_ideal clears the ping-pong threshold c - exp(-(c-1)) + 0.02.
    """
    h_ideal = F(1)
    split_levels: list[tuple[ChainLevel, F]] = []
    pp_thresh = float(c) - math.exp(-(float(c) - 1.0)) + 0.02
    while float(h_ideal) < pp_thresh:
        gap = c - h_ideal
        assert F(0) < gap < F(1)
        r = choose_r_rational(gap, k_split)
        lvl = build_and_verify_level(h_ideal, c, k_split, r)
        a_end = h_ideal - lvl.drain
        h_end = lvl.gain
        x_split = (F(1) + h_end - a_end) / 2
        assert F(0) <= x_split <= F(1)
        h_next = a_end + x_split
        assert h_next == h_end + (F(1) - x_split)
        assert h_next > h_ideal
        split_levels.append((lvl, x_split))
        h_ideal = h_next
        assert len(split_levels) <= 80, "Too many splits"
    tree_depth = len(split_levels)

    a_c, h_c = h_ideal, F(0)
    pp_levels: list[tuple[str, ChainLevel]] = []
    act = "A"
    for _ in range(120):
        va = a_c if act == "A" else h_c
        gap = c - va
        if gap <= 0:
            break
        r = choose_r_rational(gap, k_pp)
        lvl = build_and_verify_level(va, c, k_pp, r)
        if act == "A":
            a_c -= lvl.drain
            h_c += lvl.gain
        else:
            h_c -= lvl.drain
            a_c += lvl.gain
        pp_levels.append((act, lvl))
        if max(a_c, h_c) >= c:
            break
        act = "H" if act == "A" else "A"
    assert max(a_c, h_c) >= c

    pp_cols = sum(len(lvl.dws) for _, lvl in pp_levels)

    def subtree_size(d: int) -> tuple[int, int]:
        if d == 0:
            return 1, pp_cols
        sr, sc = subtree_size(d - 1)
        return 1 + 2 * sr, k_split + 2 * sc

    sub_rows, sub_cols = subtree_size(tree_depth)
    block_rows = 1 + sub_rows
    block_cols = 1 + sub_cols
    total_rows = 1 + N * block_rows
    total_cols = N * block_cols

    # Choose eta small enough relative to total_cols if caller passed None, else use caller's eta
    if eta is None:
        eta = F(1, 10**6 * total_cols)

    h_real = F(1) - p - total_cols * eta
    worst_forcing = None
    for lvl, x_split in split_levels:
        drain = F(0)
        for dj, xj in zip(lvl.dws, lvl.xs):
            dev = h_real - drain + dj * xj
            worst_forcing = dev if worst_forcing is None else min(worst_forcing, dev)
            drain += dj * (F(1) - xj)
        left_h = (h_real - drain) + x_split
        right_h = (lvl.gain - total_cols * eta) + (F(1) - x_split)
        h_real = min(left_h, right_h)

    a_r, h_r = h_real, -total_cols * eta
    for act_l, lvl in pp_levels:
        drain = F(0)
        if act_l == "A":
            for dj, xj in zip(lvl.dws, lvl.xs):
                dev = a_r - drain + dj * xj
                worst_forcing = dev if worst_forcing is None else min(worst_forcing, dev)
                drain += dj * (F(1) - xj)
            a_r -= drain
            h_r += lvl.gain
        else:
            for dj, xj in zip(lvl.dws, lvl.xs):
                dev = h_r - drain + dj * xj
                worst_forcing = dev if worst_forcing is None else min(worst_forcing, dev)
                drain += dj * (F(1) - xj)
            h_r -= drain
            a_r += lvl.gain
    forcing_lb = min(worst_forcing, max(a_r, h_r))
    accum_lb = N * p - (total_cols - N) * eta
    return min(forcing_lb, accum_lb), tree_depth, len(pp_levels), total_rows, total_cols


def main() -> None:
    print("Reference constants:")
    print(f"  Prior best (detector-chains): 1 + W(1/e) = 1.2784645428")
    print(f"  Theorem 1 (Fresh cascade)   : 1 + 1/e    = {1 + math.exp(-1):.10f}")
    print(f"  Theorem 2 (2-row ping-pong) : 1 + W(1)   = 1.5671432904")
    print(f"  Theorem 3 (Binary tree)     : 1 + ln 2   = {1 + math.log(2):.10f}\n")

    print("=== 1. L-level Fresh Cascade (limit 1 + 1/e = 1.367879) ===")
    fresh_cases = [
        ("L=2, k=16, c=1.32", F(132, 100), 2, 16, F(1, 100), 200),
        ("L=3, k=35, c=1.35", F(135, 100), 3, 35, F(1, 500), 800),
        ("L=8, k=90, c=1.365", F(1365, 1000), 8, 90, F(1, 1000), 1500),
    ]
    for name, c, L, k, p, N in fresh_cases:
        eta = F(1, 10**6 * N * L * k)
        lb, m, n = certify_fresh_cascade(c, L, k, p, N, eta)
        assert lb > F(128, 100)
        print(f"  {name:20s}: certified full-instance LB = {float(lb):.9f}  (m={m}, n={n})")

    print("\n=== 2. 2-Row Ping-Pong Cascade (limit 1 + W(1) = 1.567143) ===")
    pp_cases = [
        ("c=1.40, k=10", F(140, 100), 10, F(1, 200), 320),
        ("c=1.50, k=15", F(150, 100), 15, F(1, 500), 800),
        ("c=1.55, k=25", F(155, 100), 25, F(1, 1000), 1600),
        ("c=1.562, k=40", F(1562, 1000), 40, F(1, 2000), 3200),
    ]
    for name, c, k, p, N in pp_cases:
        eta = F(1, 10**7 * N * k)
        lb, nlev, m, n = certify_pingpong(c, k, p, N, eta)
        assert lb > F(137, 100)
        print(f"  {name:15s}: certified full-instance LB = {float(lb):.9f}  (levels={nlev}, m={m}, n={n})")

    print("\n=== 3. Recursive Binary-Tree Splitting + Ping-Pong (limit 1 + ln 2 = 1.693147) ===")
    tree_cases = [
        ("c=1.60, k=16", F(160, 100), 16, 16, F(1, 500), 850),
        ("c=1.65, k=25", F(165, 100), 25, 25, F(1, 1000), 1700),
        ("c=1.67, k=35", F(167, 100), 35, 35, F(1, 2000), 3400),
        ("c=1.682, k=50", F(1682, 1000), 50, 50, F(1, 2000), 3400),
    ]
    best_lb = F(0)
    for name, c, ks, kp, p, N in tree_cases:
        lb, D, nlev, m, n = certify_binary_tree(c, ks, kp, p, N, None)
        assert lb > F(157, 100)
        best_lb = max(best_lb, lb)
        print(f"  {name:15s}: certified full-instance LB = {float(lb):.9f}  (tree depth D={D}, leaf pp={nlev} lvls, m={m}, n={n})")

    assert best_lb > F(168, 100)
    print("\nALL THREE FAMILIES VERIFIED EXACTLY IN fractions.Fraction!")
    print(f"Strongest certified finite-instance lower bound: kappa >= {float(best_lb):.9f} "
          f"(approaching 1 + ln 2 = {1 + math.log(2):.6f}).")


if __name__ == "__main__":
    main()
