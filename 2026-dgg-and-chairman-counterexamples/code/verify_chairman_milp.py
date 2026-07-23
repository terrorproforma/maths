#!/usr/bin/env python3
"""Independent MILP infeasibility check for the chairman counterexample.

Requires NumPy and SciPy.  All rational data are multiplied by 6000 before
being passed to HiGHS, so the model matrix and bounds are integral.
"""

from __future__ import annotations

from fractions import Fraction as F

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

from verify_chairman_certificate import COLUMNS, ROWS, build_instance

SCALE = 6000


def main() -> None:
    x, d = build_instance()
    m, n = len(ROWS), len(COLUMNS)
    nvar = m * n

    def index(i: int, j: int) -> int:
        return i * n + j

    # One equality per column, followed by one interval constraint for every
    # row/prefix pair.
    nrows = n + m * n
    A = lil_matrix((nrows, nvar), dtype=float)
    lower = np.empty(nrows, dtype=float)
    upper = np.empty(nrows, dtype=float)

    row = 0
    for j in range(n):
        for i in range(m):
            A[row, index(i, j)] = 1
        lower[row] = upper[row] = 1
        row += 1

    for i, row_name in enumerate(ROWS):
        for t in range(n):
            fractional_prefix = F(0)
            for j in range(t + 1):
                col_name = COLUMNS[j]
                coefficient = d[row_name, col_name]
                fractional_prefix += coefficient * x[row_name, col_name]
                scaled_coefficient = coefficient * SCALE
                assert scaled_coefficient.denominator == 1
                A[row, index(i, j)] = int(scaled_coefficient)

            scaled_fractional = fractional_prefix * SCALE
            assert scaled_fractional.denominator == 1
            centre = int(scaled_fractional)
            lower[row] = centre - SCALE
            upper[row] = centre + SCALE
            row += 1

    assert row == nrows
    result = milp(
        c=np.zeros(nvar),
        integrality=np.ones(nvar, dtype=int),
        bounds=Bounds(np.zeros(nvar), np.ones(nvar)),
        constraints=LinearConstraint(A.tocsr(), lower, upper),
        options={"time_limit": 60.0, "mip_rel_gap": 0.0},
    )

    print(result.message)
    print(f"HiGHS status code: {result.status}")
    if result.success:
        raise AssertionError("MILP found a discrepancy-good assignment")
    if result.status != 2:
        raise RuntimeError("solver did not return a proof of infeasibility")
    print("MILP independently certifies infeasibility")


if __name__ == "__main__":
    main()
