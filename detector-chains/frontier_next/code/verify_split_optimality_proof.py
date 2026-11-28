#!/usr/bin/env python3
"""Exact verification of Theorem 7 (Resolution of Open Problem 3 of detector-chains):
Split optimality and admissibility separation for depth-k detector chains.

Theorem: For every depth k >= 3 and every nondecreasing weight vector
0 < d_2 <= d_3 <= ... <= d_{k-1} <= d_k = 1,
    max_{x in [0,1]^{k-1}} min{ dev_2(x), ..., dev_{k-1}(x), term_A(x), term_H(x) }
        = min{ tau_bal(d), 1 + d_2 },
where
    tau_bal(d) = (d_2 * (k - 1 - R) + 1) / (1 + d_2),   R = sum_{j=2}^{k-1} d_j / d_{j+1}.

Proof (dual linear combination identity, valid for ALL x in R^{k-1}):
Set alpha_j = 1/d_j - 1/d_{j+1} >= 0 for j = 2..k-1, alpha_k = 1, beta = 1.
Then sum_{j=2}^{k-1} alpha_j * dev_j(x) + term_A(x) + term_H(x)
    == 1/d_2 + (k - 1) - R  (identically in x!),
and sum(alpha_j) + beta = 1/d_2 + 1 = (1 + d_2) / d_2.
Dividing gives min{dev_2, ..., dev_{k-1}, term_A, term_H} <= tau_bal(d).
Moreover min <= dev_2(x) = 1 + d_2 * x_2 <= 1 + d_2 on [0,1]^{k-1}.

Matching primal witnesses in [0,1]^{k-1}:
  - Admissible (tau_bal(d) <= 1 + d_2): balance split x_2 = (tau_bal - 1)/d_2 in [0,1],
    x_{j+1} = d_j / d_{j+1} in (0,1] achieves all heights == tau_bal(d).
  - Inadmissible (tau_bal(d) > 1 + d_2): capped split x_2 = 1,
    x_{j+1} = d_j / d_{j+1} in (0,1] achieves all A-side heights == 1 + d_2
    and term_H = k - 2 - R > 1 + d_2.

Standard library only (fractions.Fraction).
"""

from __future__ import annotations

import random
from fractions import Fraction as F


def compute_heights(d: list[F], x: list[F]) -> tuple[list[F], F]:
    """Compute exact p=0 heights [dev_2, ..., dev_{k-1}, term_A] and term_H.
    d and x are 0-indexed lists of length k-1 corresponding to j = 2..k, with d[-1] = 1.
    """
    assert len(d) == len(x) and len(d) >= 2
    assert d[-1] == F(1)
    a_heights: list[F] = []
    drain = F(0)
    for dj, xj in zip(d, x):
        a_heights.append(F(1) - drain + dj * xj)
        drain += dj * (F(1) - xj)
    term_h = sum(F(1) - xj for xj in x)
    return a_heights, term_h


def verify_weight_vector(dws: list[F], rng: random.Random) -> tuple[bool, F, F]:
    """Verify dual identity (on random non-box x too!) and primal optimality."""
    d = list(dws) + [F(1)]
    k = len(d) + 1
    assert all(F(0) < d[i] <= d[i + 1] for i in range(len(d) - 1))

    R = sum(d[i] / d[i + 1] for i in range(len(d) - 1))
    tau_bal = (d[0] * (k - 1 - R) + F(1)) / (F(1) + d[0])
    cap = F(1) + d[0]

    # Dual weights alpha_2..alpha_k, beta = 1
    alphas = [F(1) / d[i] - F(1) / d[i + 1] for i in range(len(d) - 1)] + [F(1)]
    beta = F(1)
    assert all(a >= 0 for a in alphas)
    weight_sum = sum(alphas) + beta
    assert weight_sum == (F(1) + d[0]) / d[0]

    # Check the algebraic identity on 3 arbitrary (even out-of-box!) split vectors x
    rhs = F(1) / d[0] + (k - 1) - R
    assert rhs / weight_sum == tau_bal
    for _ in range(3):
        x_test = [F(rng.randint(-10, 20), 7) for _ in range(k - 1)]
        a_h, t_h = compute_heights(d, x_test)
        lhs = sum(a * h for a, h in zip(alphas, a_h)) + beta * t_h
        assert lhs == rhs, f"Dual identity failed: {lhs} != {rhs}"

    # Check primal witness achieves min(tau_bal, cap) inside [0,1]^{k-1}
    ratios = [d[i] / d[i + 1] for i in range(len(d) - 1)]
    assert all(F(0) < r <= F(1) for r in ratios)

    admissible = tau_bal <= cap
    if admissible:
        x2 = (tau_bal - F(1)) / d[0]
        assert F(0) <= x2 <= F(1), f"Admissible x2 out of [0,1]: {x2}"
        x_opt = [x2] + ratios
        a_h, t_h = compute_heights(d, x_opt)
        assert all(h == tau_bal for h in a_h) and t_h == tau_bal
        return True, tau_bal, tau_bal
    else:
        x_opt = [F(1)] + ratios
        a_h, t_h = compute_heights(d, x_opt)
        assert all(h == cap for h in a_h)
        assert t_h == (k - 2) - R and t_h > cap
        return False, tau_bal, cap


def main() -> None:
    rng = random.Random(20261128)
    adm_count = 0
    inadm_count = 0

    explicit = [
        [F(1, 3)],
        [F(5, 12)],
        [F(1, 10), F(1, 5)],
        [F(9, 25), F(3, 5)],
        [F(1, 2), F(1, 2), F(1, 2)],
        [F(1, 100), F(1, 100), F(1, 100), F(1, 100)],
        [F(1, 3), F(10, 21), F(7, 10)],
    ]
    for dws in explicit:
        adm, _, _ = verify_weight_vector(dws, rng)
        adm_count += int(adm)
        inadm_count += int(not adm)

    for _ in range(3000):
        k = rng.randint(3, 12)
        dws = sorted(F(rng.randint(1, 50), 50) for _ in range(k - 2))
        adm, _, _ = verify_weight_vector(dws, rng)
        adm_count += int(adm)
        inadm_count += int(not adm)

    total = adm_count + inadm_count
    print(f"Verified exact dual identity and primal attainment on {total} weight vectors (k=3..12):")
    print(f"  admissible   (opt == tau_bal) : {adm_count}")
    print(f"  inadmissible (opt == 1 + d_2) : {inadm_count}")
    print("Theorem 7 (Open Problem 3 split optimality & separation) verified exactly.")


if __name__ == "__main__":
    main()
