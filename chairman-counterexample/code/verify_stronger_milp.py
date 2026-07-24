#!/usr/bin/env python3
"""Independent MILP check for the 49x72 instance of the 9/8 corollary.

Builds the concrete balanced instance (N, p, a, q, eta) =
(24, 1/20, 11/30, 19/30, 1/10000), scales all data by 30000 so every
coefficient is an integer, and asks HiGHS whether any integral assignment
keeps every row/prefix discrepancy within 9/8.  Expected: infeasible.

Requires NumPy and SciPy (HiGHS via scipy.optimize.milp).
"""

from __future__ import annotations

from fractions import Fraction as F

import numpy as np
from scipy.optimize import LinearConstraint, milp
from scipy.sparse import lil_matrix

from verify_stronger_bound import build_concrete

SCALE = 30000
BUDGET = F(9, 8)


def main() -> None:
    N, p, eta = 24, F(1, 20), F(1, 10000)
    a, q = F(11, 30), F(19, 30)
    rows, cols, x, d = build_concrete(N, p, a, q, eta)
    m, n = len(rows), len(cols)
    nvar = m * n

    def idx(i: int, j: int) -> int:
        return i * n + j

    # exact integer coefficient tables
    dx = np.zeros((m, n), dtype=np.int64)   # SCALE * d_ij * x_ij
    dd = np.zeros((m, n), dtype=np.int64)   # SCALE * d_ij
    for i, ri in enumerate(rows):
        for j, cj in enumerate(cols):
            v1 = d[ri, cj] * x[ri, cj] * SCALE
            v2 = d[ri, cj] * SCALE
            assert v1.denominator == 1 and v2.denominator == 1
            dx[i, j] = int(v1)
            dd[i, j] = int(v2)
    budget = BUDGET * SCALE
    assert budget.denominator == 1
    B = int(budget)

    constraints = []

    # one row per column
    col_mat = lil_matrix((n, nvar))
    for j in range(n):
        for i in range(m):
            col_mat[j, idx(i, j)] = 1
    constraints.append(LinearConstraint(col_mat.tocsr(), 1, 1))

    # prefix discrepancy: |sum_{j<=t} dx[i,j] - dd[i,j]*y_ij| <= B
    pre_mat = lil_matrix((m * n, nvar))
    lo = np.zeros(m * n)
    hi = np.zeros(m * n)
    r = 0
    for i in range(m):
        run = 0
        for t in range(n):
            run += dx[i, t]
            for j in range(t + 1):
                pre_mat[r, idx(i, j)] = -dd[i, j]
            lo[r] = -B - run
            hi[r] = B - run
            r += 1
    constraints.append(LinearConstraint(pre_mat.tocsr(), lo, hi))

    res = milp(
        c=np.zeros(nvar),
        integrality=np.ones(nvar),
        bounds=(0, 1),
        constraints=constraints,
    )
    print(res.message)
    if res.status == 2:
        print("MILP independently certifies infeasibility at budget 9/8")
    else:
        raise SystemExit(f"UNEXPECTED: status={res.status} (feasible?)")


if __name__ == "__main__":
    main()
