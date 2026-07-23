#!/usr/bin/env python3
"""Enumerate rational members of the symmetric triangle-obstruction family.

The normalized parameters are d1=d3=1, d2=b, and cheap-path probabilities
p1=p3=r, p2=q.  A strict counterexample occurs when

    2r+q > 1,       b(1-q) > r,       2r+bq < 1.

The script ranks small-denominator choices by the additive factor forced on any
no-more-expensive routing.  The supremum in this family is 9/8.
"""

from __future__ import annotations

from fractions import Fraction as F


def candidates(max_denominator: int = 48):
    values = sorted({F(a, b) for b in range(1, max_denominator + 1) for a in range(b + 1)})
    for b in values:
        if not (0 < b <= 1):
            continue
        for r in values:
            for q in values:
                if not (2 * r + q > 1):
                    continue
                if not (b * (1 - q) > r):
                    continue
                if not (2 * r + b * q < 1):
                    continue
                pair_12_or_23 = 1 + b * (1 - q) - r
                pair_13 = 2 - 2 * r - b * q
                forced_factor = min(pair_12_or_23, pair_13)
                yield forced_factor, b, r, q


def main() -> None:
    best = sorted(candidates(), reverse=True)[:20]
    print("factor\tb\tr\tq\tcheap-marginal-sum")
    for factor, b, r, q in best:
        print(f"{factor}\t{b}\t{r}\t{q}\t{2*r+q}")

    # The exact boundary optimization is attained only in the limit because
    # cost separation needs 2r+q>1.  At the boundary q=1-2r, balancing the two
    # pair overloads gives r=1-b and factor b(3-2b), maximized at b=3/4.
    b = F(3, 4)
    r = F(1, 4)
    q_boundary = F(1, 2)
    supremum = b * (3 - 2 * b)
    assert supremum == F(9, 8)
    assert 2 * r + q_boundary == 1
    print(f"family supremum = {supremum}, approached from q>1/2")


if __name__ == "__main__":
    main()
