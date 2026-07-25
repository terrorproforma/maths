#!/usr/bin/env python3
"""Exact verification of the block-game claims of Section 6 (Beyond chains).

Self-contained: standard library only (no solver, no floating point in any
decision).  Every claim is discharged by exhaustive depth-first search over
ALL schedules of the block, in exact scaled-integer arithmetic with sound
pruning, so each printed number is a proved property of a finite game.

A block is a list of columns (row_p, row_q, x_p, d_p, d_q) over rows
A = 0, H1 = 1, H2 = 2 and a dump row TRASH = 3; every weight not listed on
a column's two support rows equals eta.  A schedule assigns each column to
exactly one row.  Heights start at a given bank state and evolve by
    height_i += d_ij * x_ij      (every row, every column)
    height_r -= d_rj             (the row r receiving column j).

Two exact routines:

  threat(block, bank, deny_first)
      min over ALL schedules of max prefix |height|.  With deny_first the
      first column may not go to A: this is the forced branch of the
      budget-lemma hypothesis, so the returned value is the height every
      schedule of that branch must reach.

  exits(block, bank, c, a_thr, h_thr, conjunctive)
      min over schedules whose every prefix satisfies |height| <= c of
          max(endA - a_thr, endH1 - h_thr)   (disjunctive; default)
          min(endA - a_thr, endH1 - h_thr)   (conjunctive)
      A nonnegative disjunctive value certifies that EVERY c-legal
      schedule exits with A >= a_thr or H1 >= h_thr.  A negative
      conjunctive value exhibits the failure of two-sided pinning.

Run:  python3 verify_block_games.py
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction as F

ETA = F(1, 1000)
ROWS = ("A", "H1", "H2", "TRASH")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


# ---------------------------------------------------------------- scaling

def _tables(block, bank, eta, extra=()):
    """Exact integer tables: all quantities share one LCM denominator."""
    n = len(block)
    dx = [[F(0)] * n for _ in range(4)]
    dd = [[eta] * n for _ in range(4)]
    for j, (rp, rq, xp, dp, dq) in enumerate(block):
        dd[rp][j], dd[rq][j] = dp, dq
        dx[rp][j], dx[rq][j] = dp * xp, dq * (1 - xp)
    dens = {v.denominator for row in dx + dd for v in row}
    dens |= {F(b).denominator for b in bank}
    dens |= {F(e).denominator for e in extra}
    L = math.lcm(*dens)
    return ([[int(v * L) for v in r] for r in dx],
            [[int(v * L) for v in r] for r in dd],
            [int(F(b) * L) for b in bank], L)


# ---------------------------------------------------------------- threat

def threat(block, bank, deny_first=False, eta=ETA):
    """min over all schedules of max prefix |height|, exact."""
    n = len(block)
    dx, dd, h0, L = _tables(block, bank, eta)

    def greedy():
        """Myopic schedule, used only as an initial incumbent."""
        h, peak = list(h0), max(abs(v) for v in h0)
        for j in range(n):
            for i in range(4):
                h[i] += dx[i][j]
            opts = range(1, 4) if (deny_first and j == 0) else range(4)
            best_r, best_m = None, None
            for r in opts:
                m = max(abs(h[r] - dd[r][j]),
                        max((abs(h[i]) for i in range(4) if i != r)))
                if best_m is None or m < best_m:
                    best_m, best_r = m, r
            h[best_r] -= dd[best_r][j]
            peak = max(peak, best_m)
        return peak

    best = greedy()
    nodes = 0

    def rec(j, h, run):
        nonlocal best, nodes
        nodes += 1
        if j == n:
            if run < best:
                best = run
            return
        h2 = [h[i] + dx[i][j] for i in range(4)]
        opts = []
        for r in (range(1, 4) if (deny_first and j == 0) else range(4)):
            hv = h2[r] - dd[r][j]
            m = run
            for i in range(4):
                v = hv if i == r else h2[i]
                a = -v if v < 0 else v
                if a > m:
                    m = a
            if m < best:
                opts.append((m, r, hv))
        opts.sort()
        for m, r, hv in opts:
            if m >= best:            # incumbent may have improved
                break
            h3 = h2[:]
            h3[r] = hv
            rec(j + 1, h3, m)

    rec(0, list(h0), max(abs(v) for v in h0))
    return F(best, L), nodes


# ----------------------------------------------------------------- exits

def exits(block, bank, c, a_thr, h_thr, conjunctive=False, eta=ETA):
    """min over c-legal schedules of max/min(endA - a_thr, endH1 - h_thr)."""
    n = len(block)
    dx, dd, h0, L = _tables(block, bank, eta, extra=(c, a_thr, h_thr))
    ci, ai, hi = int(F(c) * L), int(F(a_thr) * L), int(F(h_thr) * L)

    sdx = [[0] * (n + 1) for _ in range(4)]
    sdd = [[0] * (n + 1) for _ in range(4)]
    for i in range(4):
        for j in range(n - 1, -1, -1):
            sdx[i][j] = sdx[i][j + 1] + dx[i][j]
            sdd[i][j] = sdd[i][j + 1] + dd[i][j]

    combine = min if conjunctive else max
    best = None
    nodes = 0

    def rec(j, h):
        nonlocal best, nodes
        nodes += 1
        if j == n:
            obj = combine(h[0] - ai, h[1] - hi)
            if best is None or obj < best:
                best = obj
            return
        if best is not None:
            # end_i cannot fall below height + all future gains - all future costs
            fA = h[0] + sdx[0][j] - sdd[0][j] - ai
            fH = h[1] + sdx[1][j] - sdd[1][j] - hi
            if combine(fA, fH) >= best:
                return
        h2 = [h[i] + dx[i][j] for i in range(4)]
        for r in range(4):
            hv = h2[r] - dd[r][j]
            ok = True
            for i in range(4):
                v = hv if i == r else h2[i]
                if (v if v >= 0 else -v) > ci:
                    ok = False
                    break
            if ok:
                h3 = h2[:]
                h3[r] = hv
                rec(j + 1, h3)

    if max(abs(v) for v in h0) <= ci:
        rec(0, list(h0))
    return (None if best is None else F(best, L)), nodes


# ------------------------------------------------------------------ data

def load(name):
    with open(os.path.join(DATA, name)) as fh:
        rec = json.load(fh)
    return [(int(c[0]), int(c[1]), F(c[2]), F(c[3]), F(c[4]))
            for c in rec["inst"]]


def main() -> None:
    ok = True

    # (i) super-threat block: forced branch above 3/2, legal escape below 0.7
    blk = load("attack_g50_h45_k14.json")
    bank = (F(1, 2), F(9, 20), F(0), F(0))
    tf, n1 = threat(blk, bank, deny_first=True)
    tr, n2 = threat(blk, bank)
    print(f"(i)   super-threat block at bank (1/2, 9/20):")
    print(f"        forced branch = {float(tf):.9f} > 3/2 "
          f"[{n1:,} nodes]")
    print(f"        free schedule = {float(tr):.9f} < 0.70 "
          f"[{n2:,} nodes]")
    ok &= tf > F(3, 2) and tr < F(7, 10)

    # (ii) cold shaper: every c-legal schedule banks 0.25 + t at c = 1.35
    blk = load("xshaper_c135_th25.json")
    zero = (F(0), F(0), F(0), F(0))
    t, n3 = exits(blk, zero, F(27, 20), F(1, 4), F(1, 4))
    print(f"(ii)  cold shaper at c = 27/20, thresholds 1/4:")
    print(f"        exit margin = {float(t):+.9f} >= 0  =>  every legal "
          f"schedule exits with a bank >= {float(F(1,4)+t):.6f} "
          f"[{n3:,} nodes]")
    ok &= t is not None and t >= 0

    # (iii) two ladder stages at c = 1.48 lift a bank 0.31 -> 0.43 -> 0.55
    blk = load("xladder_g148_s1.json")
    print(f"(iii) ladder stages at c = 37/25 (same block, translated bank):")
    for entry, nxt in ((F(31, 100), F(43, 100)), (F(43, 100), F(55, 100))):
        t2, n4 = exits(blk, (entry, F(0), F(0), F(0)), F(37, 25),
                       nxt, F(31, 100))
        print(f"        entry ({float(entry):.2f}, 0): margin = "
              f"{float(t2):+.9f} >= 0  =>  every legal schedule exits with "
              f"A >= {float(nxt):.2f} or H1 >= 0.31 [{n4:,} nodes]")
        ok &= t2 is not None and t2 >= 0

    # (iv) a 0.65 bank fires above budget 1.60 (monotone in the bank, so
    #      any larger bank fires too)
    blk = load("lowh_g20_h0.json")
    t3, n5 = threat(blk, (F(13, 20), F(0), F(0), F(0)), deny_first=True)
    print(f"(iv)  firing block at bank (0.65, 0):")
    print(f"        forced branch = {float(t3):.9f} = {t3} > 8/5 "
          f"[{n5:,} nodes]")
    ok &= t3 > F(8, 5)

    # (v) conjunctive pinning fails: no block pins BOTH banks
    blk = load("conj_c130_a15_bm15.json")
    t4, n6 = exits(blk, zero, F(13, 10), F(3, 20), F(-3, 20),
                   conjunctive=True)
    print(f"(v)   best conjunctive pin found, c = 13/10:")
    print(f"        two-sided margin = {float(t4):+.9f} < 0  =>  some legal "
          f"schedule wrecks a bank [{n6:,} nodes]")
    ok &= t4 is not None and t4 < 0

    print("\nblock-game claims verified exactly" if ok else
          "\n*** A CLAIM FAILED ***")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
