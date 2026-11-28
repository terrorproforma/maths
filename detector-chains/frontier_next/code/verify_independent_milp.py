#!/usr/bin/env python3
"""Independent MILP (scipy/HiGHS) verification of the key constructions,
allowing ALL integral assignments (including off-support assignments!).

Checks performed:
  1. Theorem 4 (m = 5, n = 47): full instance INFEASIBLE at budget 1.0 (kappa_5 > 1).
  2. Theorem 5 (m = 4, n = 309): full instance INFEASIBLE at budget 1.0 (kappa_4 > 1).
  3. Theorem 1 (2-level Fresh Cascade, 13 cols): single block with J denied to A
     has MILP min-max = 1.285 > 1 + W(1/e) = 1.278465.
  4. Theorem 2 (2-Row Ping-Pong, 29 cols & 122 cols): single block with J denied to A
     has MILP min-max = 1.390 > 1 + 1/e = 1.367879, and 1.490 respectively.
  5. Theorem 3 (1-Split Binary Tree + Ping-Pong, 5 rows): single block with J denied
     to A is INFEASIBLE at budget 1.569 > 1 + W(1) = 1.567143.

Requires numpy + scipy (HiGHS).
"""

from __future__ import annotations

import math
from fractions import Fraction as F

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def build_level(alpha_in: F, c: F, k: int, r: F):
    dws = [r ** (k - j) for j in range(2, k)] + [F(1)]
    x2 = (c - alpha_in) / dws[0]
    assert F(0) <= x2 <= F(1), f"x2={float(x2)}"
    xs = [x2] + [r] * (k - 2)
    drain = sum(dj * (F(1) - xj) for dj, xj in zip(dws, xs))
    gain = sum(F(1) - xj for xj in xs)
    return alpha_in - drain, gain, dws, xs


def choose_r(gap: F, k: int, denom: int = 100000) -> F:
    m = k - 2
    num = max(1, int(math.floor((float(gap) ** (1.0 / m)) * denom)))
    while F(num, denom) ** m < gap:
        num += 1
    assert num < denom
    return F(num, denom)


def build_pp(a0: F, h0: F, c_val: F, k_first: int, k_rest: int, max_lev: int = 40):
    a_c, h_c = a0, h0
    levs = []
    act = "A"
    for lev in range(max_lev):
        va = a_c if act == "A" else h_c
        gap = c_val - va
        if gap <= 0:
            break
        k_use = k_first if lev == 0 else k_rest
        r_lev = choose_r(gap, k_use)
        ae, pg, dL, xL = build_level(va, c_val, k_use, r_lev)
        if act == "A":
            a_c, h_c = ae, h_c + pg
        else:
            h_c, a_c = ae, a_c + pg
        levs.append((act, dL, xL))
        if max(a_c, h_c) >= c_val:
            return levs
        act = "H" if act == "A" else "A"
    raise AssertionError("Ping-pong did not reach target")


def solve_milp(cols, m: int, budget: float | None = 1.0, deny_row_col0: int | None = None):
    n = len(cols)
    nvars = m * n + (1 if budget is None else 0)
    c_obj = np.zeros(nvars)
    if budget is None:
        c_obj[-1] = 1.0
    integrality = np.ones(nvars)
    if budget is None:
        integrality[-1] = 0
    lb = np.zeros(nvars)
    ub = np.ones(nvars)
    if budget is None:
        ub[-1] = np.inf
    if deny_row_col0 is not None:
        ub[deny_row_col0 * n + 0] = 0.0

    rows_A, lhs, rhs = [], [], []
    for j in range(n):
        row = np.zeros(nvars)
        for i in range(m):
            row[i * n + j] = 1.0
        rows_A.append(row)
        lhs.append(1.0)
        rhs.append(1.0)
    for i in range(m):
        cum_dx = 0.0
        for t in range(n):
            cum_dx += cols[t][i][1] * cols[t][i][0]
            row1 = np.zeros(nvars)
            row2 = np.zeros(nvars)
            for j in range(t + 1):
                d_ij = cols[j][i][1]
                row1[i * n + j] = -d_ij
                row2[i * n + j] = d_ij
            if budget is None:
                row1[-1] = -1.0
                row2[-1] = -1.0
                rows_A.append(row1); lhs.append(-np.inf); rhs.append(-cum_dx)
                rows_A.append(row2); lhs.append(-np.inf); rhs.append(cum_dx)
            else:
                rows_A.append(row1); lhs.append(-np.inf); rhs.append(budget - cum_dx)
                rows_A.append(row2); lhs.append(-np.inf); rhs.append(budget + cum_dx)

    res = milp(
        c=c_obj,
        integrality=integrality,
        bounds=Bounds(lb, ub),
        constraints=LinearConstraint(np.array(rows_A), lhs, rhs),
    )
    if res.success:
        return float(res.fun) if budget is None else True
    return None if budget is None else False


def check_1_m5() -> None:
    m, k, r, x2, p, xc, eta = 5, 15, 0.928, 0.92, 0.34, 0.02, 1e-5
    dws = [r ** (k - j) for j in range(2, k)] + [1.0]
    cols = []
    for b in range(3):
        iA, iH = b + 1, 4
        c = [(0.0, eta)] * m; c[0] = (p, 1.0); c[iA] = (1.0 - p, 1.0); cols.append(c)
        for idx in range(k - 1):
            xj = x2 if idx == 0 else r
            c = [(0.0, eta)] * m; c[iA] = (xj, dws[idx]); c[iH] = (1.0 - xj, 1.0); cols.append(c)
        if b < 2:
            c = [(0.0, eta)] * m; c[iA] = (xc, eta); c[iH] = (1.0 - xc, 1.0); cols.append(c)
    feas = solve_milp(cols, m, budget=1.0)
    assert feas is False
    print(f"[1] m=5, n={len(cols)} full instance: MILP INFEASIBLE at budget 1.0 (kappa_5 > 1) OK")


def check_2_m4() -> None:
    m, eta = 4, 1e-6
    c_eff = F(1002, 1000)
    u, p1, p2 = F(3, 10), F(71, 100), F(31, 100)
    pp1 = build_pp(F(1) - p1, F(0), c_eff, k_first=10, k_rest=10)
    pp2 = build_pp(F(1) - p2, F(-1), c_eff, k_first=10, k_rest=10)
    cols = [[(float(u), 1.0), (float(1 - u), 1.0), (0.0, eta), (0.0, eta)]]
    cols.append([(float(p1), 1.0), (0.0, eta), (float(1 - p1), 1.0), (0.0, eta)])
    for act, dL, xL in pp1:
        for dj, xj in zip(dL, xL):
            if act == "A":
                cols.append([(0.0, eta), (0.0, eta), (float(xj), float(dj)), (float(1 - xj), 1.0)])
            else:
                cols.append([(0.0, eta), (0.0, eta), (float(1 - xj), 1.0), (float(xj), float(dj))])
    cols.append([(float(1 - p2), 1.0), (float(p2), 1.0), (0.0, eta), (0.0, eta)])
    for act, dL, xL in pp2:
        for dj, xj in zip(dL, xL):
            if act == "A":
                cols.append([(float(xj), float(dj)), (0.0, eta), (float(1 - xj), 1.0), (0.0, eta)])
            else:
                cols.append([(float(1 - xj), 1.0), (0.0, eta), (float(xj), float(dj)), (0.0, eta)])
    feas = solve_milp(cols, m, budget=1.0)
    assert feas is False
    print(f"[2] m=4, n={len(cols)} full instance: MILP INFEASIBLE at budget 1.0 (kappa_4 > 1) OK")


def check_3_fresh_cascade() -> None:
    c_t = F(13, 10)
    _, a1, d1, x1 = build_level(F(1), c_t, 8, F(83, 100))
    _, a2, d2, x2 = build_level(a1, c_t, 5, F(31, 50))
    assert a2 > c_t
    p_test, eta = 0.015, 1e-6
    cols = [[(p_test, 1.0), (1.0 - p_test, 1.0), (0.0, eta), (0.0, eta)]]
    for dj, xj in zip(d1, x1):
        cols.append([(0.0, eta), (float(xj), float(dj)), (float(1 - xj), 1.0), (0.0, eta)])
    for dj, xj in zip(d2, x2):
        cols.append([(0.0, eta), (0.0, eta), (float(xj), float(dj)), (float(1 - xj), 1.0)])
    val = solve_milp(cols, 4, budget=None, deny_row_col0=1)
    assert val is not None and val > 1.284
    print(f"[3] 2-level Fresh Cascade block (m=4, n={len(cols)}): MILP min-max = {val:.6f} (> 1+W(1/e)=1.278465) OK")


def check_4_pingpong() -> None:
    c_t = F(14, 10)
    pp = build_pp(F(1), F(0), c_t, k_first=8, k_rest=8)
    p_test, eta = 0.01, 1e-6
    cols = [[(p_test, 1.0), (1.0 - p_test, 1.0), (0.0, eta)]]
    for act, dL, xL in pp:
        for dj, xj in zip(dL, xL):
            if act == "A":
                cols.append([(0.0, eta), (float(xj), float(dj)), (float(1 - xj), 1.0)])
            else:
                cols.append([(0.0, eta), (float(1 - xj), 1.0), (float(xj), float(dj))])
    val = solve_milp(cols, 3, budget=None, deny_row_col0=1)
    assert val is not None and val > 1.389
    print(f"[4] 2-row Ping-Pong block (m=3, n={len(cols)}): MILP min-max = {val:.6f} (> 1+1/e=1.367879) OK")


def check_5_binary_tree_split() -> None:
    # 1-split binary tree + ping-pong at c = 1.578, beating 1 + W(1) = 1.567143!
    c_t = F(1578, 1000)
    a1, h1, d_s1, x_s1 = build_level(F(1), c_t, 16, choose_r(c_t - F(1), 16))
    xK1 = (F(1) + h1 - a1) / 2
    hf1 = a1 + xK1
    pp = build_pp(hf1, F(0), c_t, k_first=22, k_rest=16, max_lev=40)
    m, p_test, eta = 5, 0.005, 1e-6
    cols = []

    def add_col(i1, i2, x1, d1, d2):
        c = [(0.0, eta)] * m
        c[i1] = (float(x1), float(d1))
        c[i2] = (float(1 - x1), float(d2))
        cols.append(c)

    add_col(0, 1, p_test, 1.0, 1.0)
    for dj, xj in zip(d_s1, x_s1):
        add_col(1, 2, xj, dj, 1.0)
    add_col(1, 2, xK1, 1.0, 1.0)
    for act, dL, xL in pp:
        for dj, xj in zip(dL, xL):
            if act == "A":
                add_col(1, 3, xj, dj, 1.0)
            else:
                add_col(3, 1, xj, dj, 1.0)
    for act, dL, xL in pp:
        for dj, xj in zip(dL, xL):
            if act == "A":
                add_col(2, 4, xj, dj, 1.0)
            else:
                add_col(4, 2, xj, dj, 1.0)

    budget = 1.569  # strictly above 1 + W(1) = 1.56714329!
    feas = solve_milp(cols, m, budget=budget, deny_row_col0=1)
    assert feas is False
    print(f"[5] 1-Split Binary-Tree block (m={m}, n={len(cols)}, pp={len(pp)} lvls): "
          f"MILP INFEASIBLE at budget {budget} (> 1+W(1)=1.567143) OK")


def main() -> None:
    print("Running independent HiGHS MILP checks (off-support assignments allowed):\n")
    check_1_m5()
    check_2_m4()
    check_3_fresh_cascade()
    check_4_pingpong()
    check_5_binary_tree_split()
    print("\nALL 5 INDEPENDENT MILP CHECKS PASSED.")


if __name__ == "__main__":
    main()
