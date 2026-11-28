#!/usr/bin/env python3
"""Independent HiGHS MILP verification (allowing ALL off-support assignments!) of:

  1. Ultra-compact m = 3, n = 33 full instance: INFEASIBLE at budget 1.0 (kappa_3 > 1, m* = 3).
  2. Dirty-helper m = 3, n = 74 full instance: INFEASIBLE at budget 1.0 (kappa_3 > 1).
  3. High-c m = 3 full instance: INFEASIBLE at budget 1.08 (beats prior m = 4 limit 1.079253!).
  4. New m = 4 full instances: INFEASIBLE at budget 1.20 and 1.24 (limit c_4** = 1.266249).
  5. New m = 6 full instance: INFEASIBLE at budget 1.32 (limit c_6* = 1.362560).
  6. New m = 8 full instance: INFEASIBLE at budget 1.37 > 1 + 1/e (limit c_8* = 1.412195).
  7. Obstruction check: 2-row pre-column + sequential ping-pong from (1.20, 0) at c = 1.70
     is FEASIBLE (verifying the explicit escape schedule).

Requires numpy + scipy (HiGHS). Uses exact band-diagonal state-variable formulation:
  sum_i y_{i,j} = 1,  s_{i,j} - s_{i,j-1} + d_{i,j} y_{i,j} = d_{i,j} x_{i,j},  |s_{i,j}| <= budget.
"""

from __future__ import annotations

import math
import time
from fractions import Fraction as F

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


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


def build_pp(a0: F, h0: F, c_val: F, k_first: int, k_rest: int, max_lev: int = 150):
    a_c, h_c = a0, h0
    levs = []
    act = "A"
    for lev in range(max_lev):
        va = a_c if act == "A" else h_c
        gap = c_val - va
        if gap <= 0:
            break
        ku = k_first if lev == 0 else k_rest
        r_lev = choose_r(gap, ku)
        ae, pg, dL, xL = build_level(va, c_val, ku, r_lev)
        if act == "A":
            a_c, h_c = ae, h_c + pg
        else:
            h_c, a_c = ae, a_c + pg
        levs.append((act, dL, xL))
        if max(a_c, h_c) >= c_val:
            return levs
        act = "H" if act == "A" else "A"
    raise AssertionError("Ping-pong failed")


def solve_milp_feas(cols, m: int, budget: float, init_s: list[float] | None = None) -> tuple[bool, float]:
    t0 = time.time()
    n = len(cols)
    nvars = 2 * m * n
    integrality = np.zeros(nvars)
    integrality[: m * n] = 1
    lb = np.zeros(nvars)
    ub = np.ones(nvars)
    lb[m * n :] = -budget
    ub[m * n :] = budget
    A = lil_matrix((n + m * n, nvars))
    b = np.zeros(n + m * n)
    r_idx = 0
    for j in range(n):
        for i in range(m):
            A[r_idx, i * n + j] = 1.0
        b[r_idx] = 1.0
        r_idx += 1
    for i in range(m):
        s0 = 0.0 if init_s is None else init_s[i]
        for j in range(n):
            x_ij, d_ij = cols[j][i]
            A[r_idx, m * n + i * n + j] = 1.0
            if j > 0:
                A[r_idx, m * n + i * n + (j - 1)] = -1.0
            A[r_idx, i * n + j] = d_ij
            b[r_idx] = d_ij * x_ij + (s0 if j == 0 else 0.0)
            r_idx += 1
    res = milp(
        c=np.zeros(nvars),
        integrality=integrality,
        bounds=Bounds(lb, ub),
        constraints=LinearConstraint(A.tocsc(), b, b),
    )
    return bool(res.success), time.time() - t0


def add_col(cols, m: int, eta: float, entries: dict[int, tuple[float, float]]) -> None:
    col = [(0.0, eta)] * m
    for idx, val in entries.items():
        col[idx] = val
    cols.append(col)


def check_1_m3_ultracompact() -> None:
    m, eta = 3, 1e-6
    c_des = F(1002, 1000)
    u, p1, k1 = F(995, 1000), F(17, 50), 10
    r1 = choose_r(c_des - (F(1) - p1), k1, denom=10000)
    _, term_A, d1, x1 = build_level(F(1) - p1, c_des, k1, r1)
    delta = term_A - F(int(term_A))
    xc = delta + F(1, 200)
    pp2 = build_pp(u + p1 - F(1), delta - xc, c_des, 4, 4, max_lev=20)

    cols = []
    add_col(cols, m, eta, {0: (float(u), 1.0), 1: (float(1 - u), eta)})
    add_col(cols, m, eta, {0: (float(p1), 1.0), 2: (float(1 - p1), 1.0)})
    for dj, xj in zip(d1, x1):
        add_col(cols, m, eta, {2: (float(xj), float(dj)), 1: (float(1 - xj), 1.0)})
    add_col(cols, m, eta, {2: (float(xc), eta), 1: (float(1 - xc), 1.0)})
    for act, dL, xL in pp2:
        for dj, xj in zip(dL, xL):
            if act == "A":
                add_col(cols, m, eta, {0: (float(xj), float(dj)), 1: (float(1 - xj), 1.0)})
            else:
                add_col(cols, m, eta, {1: (float(xj), float(dj)), 0: (float(1 - xj), 1.0)})

    assert len(cols) == 33
    feas, dt = solve_milp_feas(cols, m, 1.0)
    assert feas is False
    print(f"[1] Ultra-compact m=3, n={len(cols)} (cleaned helper): MILP INFEASIBLE at 1.0 ({dt:.3f}s) OK")


def check_m3_dirty(tag: str, budget: F, u: F, p1: F, k1f: int, k1r: int, k2f: int, k2r: int) -> None:
    m, eta = 3, 1e-6
    c_des = budget + F(2, 1000)
    pp1 = build_pp(F(1) - p1, F(0), c_des, k1f, k1r)
    pp2 = build_pp(u + p1 - F(1), -budget, c_des, k2f, k2r)
    cols = []
    add_col(cols, m, eta, {0: (float(u), 1.0), 1: (float(1 - u), eta)})
    add_col(cols, m, eta, {0: (float(p1), 1.0), 2: (float(1 - p1), 1.0)})
    for act, dL, xL in pp1:
        for dj, xj in zip(dL, xL):
            if act == "A":
                add_col(cols, m, eta, {2: (float(xj), float(dj)), 1: (float(1 - xj), 1.0)})
            else:
                add_col(cols, m, eta, {1: (float(xj), float(dj)), 2: (float(1 - xj), 1.0)})
    for act, dL, xL in pp2:
        for dj, xj in zip(dL, xL):
            if act == "A":
                add_col(cols, m, eta, {0: (float(xj), float(dj)), 1: (float(1 - xj), 1.0)})
            else:
                add_col(cols, m, eta, {1: (float(xj), float(dj)), 0: (float(1 - xj), 1.0)})
    feas, dt = solve_milp_feas(cols, m, float(budget))
    assert feas is False
    print(f"{tag} m=3, n={len(cols)} (pp1={len(pp1)}, pp2={len(pp2)}): MILP INFEASIBLE at {float(budget):.2f} ({dt:.3f}s) OK")


def check_even_m(tag: str, m: int, budget: F, u: F, p1: F, kb: int, kf: int) -> None:
    eta = 1e-6
    q = (m - 2) // 2
    c_des = budget + F(2, 1000)
    pp_blk = build_pp(F(1) - p1, F(0), c_des, kb, kb)
    pp_fin = build_pp(u + q * p1 - F(1), F(0), c_des, kf, kf)
    cols = []
    add_col(cols, m, eta, {0: (float(u), 1.0), 1: (float(1 - u), eta)})
    for r in range(q):
        iA, iH = 2 + 2 * r, 3 + 2 * r
        add_col(cols, m, eta, {0: (float(p1), 1.0), iA: (float(1 - p1), 1.0)})
        for act, dL, xL in pp_blk:
            for dj, xj in zip(dL, xL):
                if act == "A":
                    add_col(cols, m, eta, {iA: (float(xj), float(dj)), iH: (float(1 - xj), 1.0)})
                else:
                    add_col(cols, m, eta, {iH: (float(xj), float(dj)), iA: (float(1 - xj), 1.0)})
    for act, dL, xL in pp_fin:
        for dj, xj in zip(dL, xL):
            if act == "A":
                add_col(cols, m, eta, {0: (float(xj), float(dj)), 1: (float(1 - xj), 1.0)})
            else:
                add_col(cols, m, eta, {1: (float(xj), float(dj)), 0: (float(1 - xj), 1.0)})
    feas, dt = solve_milp_feas(cols, m, float(budget))
    assert feas is False
    print(f"{tag} m={m}, n={len(cols)} (q={q}, blk={len(pp_blk)}, fin={len(pp_fin)}): "
          f"MILP INFEASIBLE at {float(budget):.2f} ({dt:.3f}s) OK")


def check_7_obstruction_escape() -> None:
    c_des = F(1702, 1000)
    d0, x0 = 0.60, 0.45
    pp1 = build_pp(F(87, 100), F(55, 100), c_des, 35, 35, max_lev=120)
    pp2 = build_pp(F(147, 100), F(-45, 100), c_des, 20, 20, max_lev=80)
    cols = [[(x0, d0), (1.0 - x0, 1.0)]]
    for pp in [pp2, pp1]:
        for act, dL, xL in pp:
            for dj, xj in zip(dL, xL):
                cols.append([(float(xj), float(dj)), (float(1 - xj), 1.0)] if act == "A"
                            else [(float(1 - xj), 1.0), (float(xj), float(dj))])
    feas, dt = solve_milp_feas(cols, 2, 1.70, init_s=[1.20, 0.0])
    assert feas is True
    print(f"[7] Obstruction check (2-row pre-col + pp2+pp1 from (1.20,0) at c=1.70, n={len(cols)}): "
          f"MILP FEASIBLE (escape confirmed, {dt:.3f}s) OK")


def main() -> None:
    print("Running independent HiGHS MILP checks (off-support assignments allowed):\n")
    check_1_m3_ultracompact()
    check_m3_dirty("[2] Compact dirty-helper", F(1, 1), F(995, 1000), F(78, 100), 4, 4, 7, 4)
    check_m3_dirty("[3] High-c (beats old m=4!)", F(108, 100), F(995, 1000), F(80, 100), 18, 14, 18, 14)
    check_even_m("[4a] New m=4 ladder", 4, F(120, 100), F(995, 1000), F(52, 100), 12, 12)
    check_even_m("[4b] New m=4 ladder", 4, F(124, 100), F(995, 1000), F(48, 100), 22, 16)
    check_even_m("[5]  New m=6 ladder", 6, F(132, 100), F(995, 1000), F(35, 100), 18, 18)
    check_even_m("[6]  New m=8 ladder (>1+1/e)", 8, F(137, 100), F(995, 1000), F(27, 100), 20, 20)
    check_7_obstruction_escape()
    print("\nALL 8 INDEPENDENT MILP CHECKS PASSED.")


if __name__ == "__main__":
    main()
