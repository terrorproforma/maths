#!/usr/bin/env python3
"""Concrete instance whose min-max prefix discrepancy exceeds 7/6.

Blocks of depth-4 chains (d = (9/25, 3/5), tau = 103/85 ~ 1.2118) plus the
global accumulator B. p = 1/50, N = 59 blocks -> Np = 59/50 = 1.18 > 7/6.
m = 119 rows, n = 236 columns.

Checks (exact scaled-integer MILP):
  budget 7/6      -> expect INFEASIBLE  (min-max > 7/6)
  budget 1.19     -> expect FEASIBLE    (sanity: above the guarantee)
"""

from __future__ import annotations

from fractions import Fraction as F

from minmax import feasible_at

P = F(1, 50)
N = 59
D2, D3 = F(9, 25), F(3, 5)
TAU = F(103, 85)
ETA = F(1, 100000)

# balance solution for k=4 chain
X2 = (TAU - 1) / D2          # (tau-1)/d2
X3 = D2 / D3
X4 = D3                      # d3/d4, d4 = 1


def build():
    inst = []
    for i in range(1, N + 1):
        A, H = 2 * i - 1, 2 * i
        inst.append((A, 0, 1 - P, F(1), F(1)))       # col1: {A, B}
        inst.append((A, H, X2, D2, F(1)))            # col2
        inst.append((A, H, X3, D3, F(1)))            # col3
        inst.append((A, H, X4, F(1), F(1)))          # col4 (terminal)
    return inst, 2 * N + 1


if __name__ == "__main__":
    inst, m = build()
    print(f"instance: m={m}, n={len(inst)}; tau={TAU}={float(TAU):.6f}, "
          f"Np={float(N*P):.4f}, budget target 7/6={float(F(7,6)):.6f}")
    f76 = feasible_at(inst, m, F(7, 6), eta=ETA)
    print("feasible at 7/6?", f76, "(expect False -> min-max > 7/6)")
    f119 = feasible_at(inst, m, F(119, 100), eta=ETA)
    print("feasible at 1.19?", f119, "(expect True)")
    if not f76 and f119:
        print("CONFIRMED: concrete instance forces prefix discrepancy > 7/6")
