#!/usr/bin/env python3
"""Exact verification of the improved-split remark (Remark 'improved').

Three-column block in the p -> 0 idealization: hypothesis banks +1 on A;
detector column K has weights (d, 1) and split x2; column L has weights (1, 1)
and split x3. Balance solution x3 = d, x2 = (1-d)/(1+d) makes the three
violation heights equal to tau(d) = 1 + d(1-d)/(1+d).

Checks, in exact rational arithmetic (standard library only):
  1. for d = 5/12: all three heights equal 239/204 > 7/6, and the real-path
     legality values stay within tau;
  2. tau(d) formula matches the three heights for a sample of rational d;
  3. boundary optimality: tau(d) <= 4 - 2*sqrt(2) for a fine rational grid,
     via the equivalent square comparison (no floating point):
     tau(d) <= 4 - 2 sqrt2  <=>  (4 - tau(d))^2 >= 8   for tau(d) <= 4.
"""

from __future__ import annotations

from fractions import Fraction as F


def heights(d: F, x2: F, x3: F):
    v1 = 1 + d * x2
    vA = 1 - d * (1 - x2) + x3
    vH = (1 - x2) + (1 - x3)
    return v1, vA, vH


def balanced(d: F):
    x2 = (1 - d) / (1 + d)
    x3 = d
    return x2, x3


def tau(d: F) -> F:
    return 1 + d * (1 - d) / (1 + d)


def main() -> None:
    # 1. rational witness d = 5/12
    d = F(5, 12)
    x2, x3 = balanced(d)
    v = heights(d, x2, x3)
    assert x2 == F(7, 17) and x3 == F(5, 12)
    assert v[0] == v[1] == v[2] == F(239, 204), v
    assert F(239, 204) > F(7, 6)
    # real-path legality (col1 -> A, K -> A, L -> H exhibit)
    t = F(239, 204)
    h_after_K = 1 - x2                      # H gains on compliant K
    a_after_K = -d * (1 - x2)               # A relief
    assert h_after_K <= t and abs(a_after_K) <= t
    a_final = a_after_K + x3                # L -> H: A denied, gains x3
    h_final = h_after_K - x3                # H receives L: drops 1*(1-(1-x3))
    assert abs(a_final) <= t and abs(h_final) <= t
    print(f"d = 5/12: all three heights = 239/204 = {float(t):.6f} > 7/6  ✓")

    # 2. formula consistency on a sample
    for dd in (F(1, 3), F(2, 5), F(5, 12), F(3, 7), F(1, 2)):
        x2, x3 = balanced(dd)
        v = heights(dd, x2, x3)
        assert v[0] == v[1] == v[2] == tau(dd), dd
    print("balance formula verified on rational sample  ✓")

    # 3. optimality: tau(d) <= 4 - 2*sqrt(2), i.e. (4 - tau)^2 >= 8, exact
    worst = F(0)
    for num in range(1, 1000):
        dd = F(num, 1000)
        tt = tau(dd)
        assert tt < 4 and (4 - tt) ** 2 >= 8, f"optimality violated at d={dd}"
        worst = max(worst, tt)
    print(f"grid check: max tau = {float(worst):.6f} <= 4 - 2*sqrt(2) "
          f"= 1.171573  ✓")
    print("improved-split certificate verified exactly")


if __name__ == "__main__":
    main()
