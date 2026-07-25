#!/usr/bin/env python3
"""Exact full-instance certificates for the paper-2 main theorem.

Instance (depth k, N blocks, detector share p, off-support weight eta):
rows B, A_1, H_1, ..., A_N, H_N; block b = detector J_b on {A_b, B}
(x_A = 1-p, weights 1,1) followed by chain columns C_2..C_k on {A_b, H_b}
(weights d_j with d_k = 1, splits x_j on the balance solution).

Certificate (generalized budget lemma): every integral assignment has some
row-prefix discrepancy at least
    LB(k, d, p, eta, N) = min( tau(k,d) - p - (k(N-1)+1) eta ,
                               N p - N(k-1) eta ).
Bookkeeping: fresh rows enter block b no lower than -k(N-1) eta; within the
block, A_b is on-support everywhere while H_b can absorb J_b once (one more
eta); the A-side heights (dev_j, term_A) each lose exactly p relative to
the p = 0 idealization and term_H loses nothing; the accumulator gains p
per forced detector and can be relieved by at most N(k-1) eta-dumps.

The per-block heights and legality are delegated to verify() from
verify_chain_certificate (exact rationals, asserts every inequality and
the helper end-height identity). This script adds the instance-level
arithmetic and produces exact rational kappa lower bounds, including deep
rungs with geometric rational weights d_j = r^{k-j} (so the balance splits
x_{j+1} = d_j/d_{j+1} = r stay rational).

Targets: monotone rungs, k=4 >= 7/6 + margin (the paper-1 promise), and
the k=25 rung above 1.27 (within 0.008 of the limit 1 + W(1/e)).
"""

from __future__ import annotations

from fractions import Fraction as F

from verify_chain_certificate import verify


def instance_bound(k: int, dws, p: F, eta: F, N: int) -> tuple[F, F]:
    """(tau, exact instance lower bound) for the (k, d, p, eta, N) family."""
    tau = verify(list(dws))                    # asserts the block certificate
    forcing = tau - p - (k * (N - 1) + 1) * eta
    accumulator = N * p - N * (k - 1) * eta
    return tau, min(forcing, accumulator)


def geometric(k: int, r: F):
    """d_j = r^(k-j) for j = 2..k-1 (rational geometric chain, d_k = 1)."""
    return [r ** (k - j) for j in range(2, k)]


def main() -> None:
    W_LIMIT = 1.2784645427610738          # 1 + W(1/e), display only
    cases = [
        ("k=3  d=5/12           ", 3, [F(5, 12)], F(1, 100), 300),
        ("k=4  d=(9/25,3/5)     ", 4, [F(9, 25), F(3, 5)], F(1, 100), 300),
        ("k=5  d=(1/3,10/21,7/10)", 5, [F(1, 3), F(10, 21), F(7, 10)],
         F(1, 100), 300),
        ("k=7  geometric-ish    ", 7,
         [F(3, 10), F(2, 5), F(11, 20), F(7, 10), F(17, 20)], F(1, 100), 300),
        ("k=12 r=22/25          ", 12, geometric(12, F(22, 25)),
         F(1, 100), 300),
        ("k=25 r=473/500        ", 25, geometric(25, F(473, 500)),
         F(1, 1000), 3000),
        ("k=40 r=967/1000       ", 40, geometric(40, F(967, 1000)),
         F(1, 1000), 3000),
    ]
    print("exact full-instance kappa lower bounds "
          "(per-case p, N; eta = 1/(10^4 kN)):\n")
    prev = F(0)
    for name, k, dws, p, N in cases:
        eta = F(1, 10 ** 4 * k * N)
        tau, lb = instance_bound(k, dws, p, eta, N)
        assert lb > prev, f"rungs not monotone at {name}"
        prev = lb
        print(f"{name}: tau = {float(tau):.9f}   "
              f"instance LB = {float(lb):.9f}   "
              f"(m = {2*N+1}, n = {k*N}, p = {p})")
        print(f"    tau exactly   = {tau.numerator}/{tau.denominator}")
        print(f"    LB exactly    = {lb.numerator}/{lb.denominator}")
        assert tau <= 1 + dws[0], f"{name}: design inadmissible (x_2 > 1)"
    assert lb > F(127, 100), "deepest rung should exceed 1.27"
    tau4, lb4 = instance_bound(4, [F(9, 25), F(3, 5)],
                               F(1, 100), F(1, 10 ** 4 * 4 * 300), 300)
    assert lb4 > F(7, 6), "k=4 rung must beat 7/6 (paper-1 promise)"
    print(f"\nall rungs monotone; k=4 beats 7/6; deepest rung "
          f"{float(prev):.6f} is within {W_LIMIT - float(prev):.6f} "
          f"of 1 + W(1/e) = {W_LIMIT:.6f}")
    print("kappa certificate verified exactly")


if __name__ == "__main__":
    main()
