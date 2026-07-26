#!/usr/bin/env python3
"""Exact witness for the composition barrier of Section 6.

Section 6 reports that a machine assembled from components with
stage-level guarantees at budget 1.35 nevertheless admits a schedule whose
maximum prefix discrepancy is far below that budget -- indeed below the
plain depth-4 chain instance of Section 5.  That is a statement about one
explicit schedule, so it is certified by replaying the schedule: any single
assignment's maximum prefix discrepancy is an upper bound on the instance's
min-max.  Everything here is exact (Fraction), standard library only.

The machine.  Global rows are the accumulator B = 0 and the shared working
rows A = 1, H1 = 2, H2 = 3.  One super-block concatenates five component
blocks -- cold shaper, two bank-lifting ladder stages, and two firing
blocks -- rationalized to the /50400 grid (their guarantees are re-proved
at that grid in verify_block_games.py's companions); the two firing blocks
have their leading column replaced by a detector on {A, B} of share
1 - 1/25, which is the only coupling to the accumulator.  The instance is
19 such super-blocks: 4 rows, 1273 columns, off-support weight 1/100000.

The schedule.  The floor rule of Section 6: relieve the taller support row
unless that would push it below -1/2; else relieve the other support row;
else dump on the row whose resulting height is smallest in absolute value.

Run:  python3 verify_composition_failure.py
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
ETA = F(1, 100000)
P_DET = F(1, 25)
N_SB = 19
GMAP = (1, 2, 3, 3)          # local A, H1, H2, TRASH -> global rows
THETA = F(1, 2)
M = 4


def load(name):
    with open(os.path.join(DATA, name)) as fh:
        rec = json.load(fh)
    return [(int(c[0]), int(c[1]), F(c[2]), F(c[3]), F(c[4]))
            for c in rec["inst"]]


def remap(block, detector=False):
    out = []
    for j, (rp, rq, xp, dp, dq) in enumerate(block):
        if detector and j == 0:
            out.append((1, 0, 1 - P_DET, F(1), F(1)))
        else:
            out.append((GMAP[rp], GMAP[rq], xp, dp, dq))
    return out


def build():
    sb = (remap(load("r_shaper.json"))
          + remap(load("r_stageA.json"))
          + remap(load("r_stageB.json"))
          + remap(load("r_gfire.json"), detector=True)
          + remap(load("r_hfire.json"), detector=True))
    return sb * N_SB


def floor_rule(inst, eta=ETA, theta=THETA):
    """Replay the floor rule exactly; return (peak, per-row peaks)."""
    n = len(inst)
    dx = [[F(0)] * n for _ in range(M)]
    dd = [[eta] * n for _ in range(M)]
    for j, (rp, rq, xp, dp, dq) in enumerate(inst):
        dd[rp][j], dd[rq][j] = dp, dq
        dx[rp][j], dx[rq][j] = dp * xp, dq * (1 - xp)

    h = [F(0)] * M
    peak = F(0)
    rowpeak = [F(0)] * M
    prev_B = F(0)
    vent = (None, F(0), F(0), F(0))       # (column, before, after, drop)
    for j, (rp, rq, _, _, _) in enumerate(inst):
        for i in range(M):
            h[i] += dx[i][j]
        a, b = (rp, rq) if h[rp] >= h[rq] else (rq, rp)
        if h[a] - dd[a][j] >= -theta:
            r = a
        elif h[b] - dd[b][j] >= -theta:
            r = b
        else:
            cands = [i for i in range(M) if i not in (rp, rq)]
            r = min(cands, key=lambda i: abs(h[i] - dd[i][j])) if cands else a
        h[r] -= dd[r][j]
        if prev_B - h[0] > vent[3]:       # largest prefix-to-prefix relief on B
            vent = (j, prev_B, h[0], prev_B - h[0])
        prev_B = h[0]
        for i in range(M):
            av = abs(h[i])
            if av > rowpeak[i]:
                rowpeak[i] = av
            if av > peak:
                peak = av
    return peak, rowpeak, vent


def main() -> None:
    inst = build()
    peak, rowpeak, vent = floor_rule(inst)
    names = ("B", "A", "H1", "H2")
    print(f"assembled machine: {M} rows, {len(inst)} columns, "
          f"{N_SB} super-blocks, eta = 1/100000")
    print(f"floor-rule schedule: max prefix discrepancy = "
          f"{peak.numerator}/{peak.denominator} = {float(peak):.6f}")
    print("  per-row peaks: " + "  ".join(
        f"{names[i]}={float(rowpeak[i]):.6f}" for i in range(M)))
    j, before, after, drop = vent
    print(f"  accumulator venting: at column {j} the prefix height falls "
          f"{before.numerator}/{before.denominator} -> "
          f"{after.numerator}/{after.denominator}")
    print(f"    (net relief {drop.numerator}/{drop.denominator} = "
          f"{float(drop):.6f}; that column is granted to the accumulator "
          f"itself, whose weight there is 1)")
    chain4 = F(103, 85)
    print(f"\ncomparison: the depth-4 chain block forces {float(chain4):.6f} "
          f"(tau = 103/85)")
    ok = peak < chain4
    print(f"the assembled machine is WEAKER than the plain depth-4 chain: "
          f"{ok}")
    print("\nNote: this is a witness, so it bounds the instance's min-max "
          "from ABOVE;\nno exhaustive search over the 4^1273 schedules is "
          "claimed or needed.")
    print("composition-failure witness verified exactly" if ok else
          "*** WITNESS DOES NOT ESTABLISH THE CLAIM ***")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
