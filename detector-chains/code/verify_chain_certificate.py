#!/usr/bin/env python3
"""Exact rational verification of depth-k chain forcing certificates.

Chain gadget over rows {A, H}: hypothesis column banks 1 on A (p -> 0 ideal);
columns 2..k-1 designated to A with weights d_2..d_{k-1}; terminal weights 1.
Balance solution: x_{j+1} = d_j / d_{j+1} (with d_k := 1),
x_2 = (tau - 1)/d_2, tau = (d_2 (k-1-R) + 1)/(1+d_2),
R = sum_{j=2}^{k-1} d_j/d_{j+1}.

verify(dws) recomputes everything in Fractions and checks EVERY inequality of
the forcing argument:
  dev_j >= tau, term_A >= tau, term_H >= tau,
  legality: partial H sums <= tau, all x in [0,1], all d in (0,1].
Returns exact tau.
"""

from __future__ import annotations

from fractions import Fraction as F


def verify(dws: list[F]) -> F:
    k = len(dws) + 2                      # chain depth
    d = [None, None] + [F(x) for x in dws] + [F(1)]   # d[2..k], d[k]=1
    R = sum(d[j] / d[j + 1] for j in range(2, k))
    tau = (d[2] * (k - 1 - R) + 1) / (1 + d[2])

    x = [None, None] + [F(0)] * (k - 1)
    x[2] = (tau - 1) / d[2]
    for j in range(3, k + 1):
        x[j] = d[j - 1] / d[j]

    for j in range(2, k + 1):
        assert 0 <= x[j] <= 1, f"x_{j}={x[j]} out of range"
        assert 0 < d[j] <= 1, f"d_{j} out of range"

    # banked values along compliant hypothesis path
    drain = F(0)          # A's cumulative relief
    hsum = F(0)           # H's cumulative gain
    for j in range(2, k):
        dev = 1 - drain + d[j] * x[j]
        assert dev >= tau, f"dev_{j} = {dev} < tau"
        drain += d[j] * (1 - x[j])
        hsum += 1 - x[j]
        assert hsum <= tau, f"legality at col {j}: {hsum} > tau"
    term_A = 1 - drain + 1 * x[k]
    term_H = hsum + (1 - x[k])
    assert term_A >= tau, f"term_A = {term_A} < tau"
    assert term_H >= tau, f"term_H = {term_H} < tau"

    # real-path legality exhibit: cols 2..k-1 -> A, terminal -> H
    a_real, h_real = F(0), F(0)
    for j in range(2, k):
        a_real -= d[j] * (1 - x[j])
        h_real += 1 - x[j]
        assert abs(a_real) <= tau and h_real <= tau
    a_real += x[k]                        # terminal to H: A denied, gains x_k
    h_real -= x[k]                        # H receives weight 1: drop 1-(1-x_k)=x_k
    assert abs(a_real) <= tau and abs(h_real) <= tau
    assert h_real == tau - 1, f"helper end {h_real} != tau-1"   # exact identity
    return tau


if __name__ == "__main__":
    cases = {
        "k=3 paper-style d=1/3 (gives 7/6)": [F(1, 3)],
        "k=3 d=5/12 (beats 7/6)": [F(5, 12)],
        "k=4 geometric d=(9/25,3/5)": [F(9, 25), F(3, 5)],
        "k=5 d=(1/3,10/21,7/10)": [F(1, 3), F(10, 21), F(7, 10)],
        "k=7 geometric-ish": [F(3, 10), F(2, 5), F(11, 20), F(7, 10), F(17, 20)],
    }
    print(f"targets: 7/6 = {float(F(7,6)):.6f}, 4-2*sqrt2 = 1.171573, "
          f"1+W(1/e) = 1.278465\n")
    for name, dws in cases.items():
        tau = verify(dws)
        print(f"{name}:  tau = {tau} = {float(tau):.6f}   "
              f"{'> 7/6 ✓' if tau > F(7,6) else '= 7/6' if tau == F(7,6) else '< 7/6'}")
