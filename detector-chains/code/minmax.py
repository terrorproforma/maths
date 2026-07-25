#!/usr/bin/env python3
"""Exact tooling for the machine-dependent prefix-discrepancy constant kappa.

An instance is a list of columns; each column is
    (row_p, row_q, x_p, d_p, d_q)
with row indices, fractional split (x_p on row_p, 1-x_p on row_q), and the
two support weights. All off-support weights are a global eta.

min_max_discrepancy(inst, m): float MILP (HiGHS) minimizing the maximum
prefix discrepancy over integral assignments — the value the adversary can
guarantee. This is the quantity kappa asks about (divided by D = max weight).

feasible_at(inst, m, budget): exact scaled-integer feasibility MILP at a
rational budget, for confirming float results.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import lcm

import numpy as np
from scipy.optimize import LinearConstraint, milp
from scipy.sparse import lil_matrix

ETA = F(1, 1000)


def tables(inst, m, eta=ETA):
    """Return (dx, dd) Fraction tables of shape m x n."""
    n = len(inst)
    dx = [[F(0)] * n for _ in range(m)]
    dd = [[eta] * n for _ in range(m)]
    for j, (rp, rq, xp, dp, dq) in enumerate(inst):
        assert 0 <= xp <= 1 and rp != rq
        dd[rp][j] = F(dp)
        dd[rq][j] = F(dq)
        dx[rp][j] = F(dp) * F(xp)
        dx[rq][j] = F(dq) * (1 - F(xp))
    return dx, dd


def max_weight(inst, eta=ETA) -> F:
    return max([eta] + [max(F(c[3]), F(c[4])) for c in inst])


def min_max_discrepancy(inst, m, eta=ETA) -> float:
    """Float MILP: min over assignments of max prefix |Delta|."""
    n = len(inst)
    dx, dd = tables(inst, m, eta)
    nvar = m * n + 1          # y variables + c
    C = m * n                 # index of c

    def idx(i, j):
        return i * n + j

    cons = []
    col = lil_matrix((n, nvar))
    for j in range(n):
        for i in range(m):
            col[j, idx(i, j)] = 1
    cons.append(LinearConstraint(col.tocsr(), 1, 1))

    pre = lil_matrix((2 * m * n, nvar))
    lo = np.full(2 * m * n, -np.inf)
    hi = np.zeros(2 * m * n)
    r = 0
    for i in range(m):
        run = F(0)
        for t in range(n):
            run += dx[i][t]
            # sum_{j<=t} dd*y - c <= run   and   -sum dd*y - c <= -run
            for j in range(t + 1):
                pre[r, idx(i, j)] = float(dd[i][j])
                pre[r + 1, idx(i, j)] = -float(dd[i][j])
            pre[r, C] = -1.0
            pre[r + 1, C] = -1.0
            hi[r] = float(run)
            hi[r + 1] = float(-run)
            r += 2
    cons.append(LinearConstraint(pre.tocsr(), lo, hi))

    obj = np.zeros(nvar)
    obj[C] = 1.0
    integ = np.ones(nvar)
    integ[C] = 0
    bounds = np.array([[0, 1]] * (m * n) + [[0, np.inf]])
    res = milp(c=obj, integrality=integ,
               bounds=(bounds[:, 0], bounds[:, 1]), constraints=cons)
    if res.status != 0:
        raise RuntimeError(res.message)
    return float(res.fun)


def feasible_at(inst, m, budget: F, eta=ETA) -> bool:
    """Exact scaled-integer feasibility: any assignment with all |Delta| <= budget?"""
    n = len(inst)
    dx, dd = tables(inst, m, eta)
    scale = lcm(budget.denominator,
                *[v.denominator for row in dx for v in row],
                *[v.denominator for row in dd for v in row])
    DX = [[int(v * scale) for v in row] for row in dx]
    DD = [[int(v * scale) for v in row] for row in dd]
    B = int(budget * scale)
    nvar = m * n

    def idx(i, j):
        return i * n + j

    cons = []
    col = lil_matrix((n, nvar))
    for j in range(n):
        for i in range(m):
            col[j, idx(i, j)] = 1
    cons.append(LinearConstraint(col.tocsr(), 1, 1))

    pre = lil_matrix((m * n, nvar))
    lo = np.zeros(m * n)
    hi = np.zeros(m * n)
    r = 0
    for i in range(m):
        run = 0
        for t in range(n):
            run += DX[i][t]
            for j in range(t + 1):
                pre[r, idx(i, j)] = -DD[i][j]
            lo[r] = -B - run
            hi[r] = B - run
            r += 1
    cons.append(LinearConstraint(pre.tocsr(), lo, hi))

    res = milp(c=np.zeros(nvar), integrality=np.ones(nvar),
               bounds=(0, 1), constraints=cons)
    return res.status == 0          # 0 = optimal found = feasible


def paper_instance():
    """The 11x15 instance from the paper. Rows: 0=B, then (A_k,H_k)=(2k-1,2k)."""
    inst = []
    for k in range(1, 6):
        A, H = 2 * k - 1, 2 * k
        inst.append((A, 0, F(19, 24), F(1), F(1)))          # J_k: A gets 19/24, B 5/24
        inst.append((A, H, F(1, 2), F(1, 2), F(1)))          # K_k
        inst.append((A, H, F(23, 48), F(1), F(1)))           # L_k
    return inst, 11


if __name__ == "__main__":
    inst, m = paper_instance()
    v = min_max_discrepancy(inst, m)
    print(f"paper 11x15 true min-max = {v:.6f}  (certificate lower bound 619/600 = {619/600:.6f})")
    print("feasible at 619/600?", feasible_at(inst, m, F(619, 600)))
    print("feasible at 1?      ", feasible_at(inst, m, F(1)))
