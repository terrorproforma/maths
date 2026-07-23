#!/usr/bin/env python3
"""Search the two-parameter repeated forcing-gadget family.

For a decision column J use fractions x_A=1-p and x_B=p.  The two detector
columns use the fixed K data and L fractions x_A=1-q, x_H=q.  Ignoring the
small off-support safety weight eta, local forcing requires

    p < 1/4,  q > 1/2,  p+q < 3/4.

N repetitions defeat the accumulator bound when N*p-2N*eta>1.
"""

from __future__ import annotations

from fractions import Fraction as F


def main(max_denominator: int = 96, repetitions: int = 5, eta: F = F(1, 1000)) -> None:
    values = sorted({F(a, b) for b in range(1, max_denominator + 1) for a in range(b + 1)})
    feasible = []
    for p in values:
        for q in values:
            if not (F(1, repetitions) < p < F(1, 4)):
                continue
            if not (F(1, 2) < q and p + q < F(3, 4)):
                continue
            accumulator = repetitions * p - 2 * repetitions * eta
            if accumulator <= 1:
                continue
            # Worst block is the fifth, with twelve preceding off-support hits.
            k_witness = -12 * eta + (1 - p) + F(1, 4)
            l_to_h_witness = -12 * eta + (F(3, 4) - p) + (1 - q)
            l_not_h_witness = -13 * eta + F(1, 2) + q
            margin = min(k_witness, l_to_h_witness, l_not_h_witness, accumulator) - 1
            if margin > 0:
                feasible.append((margin, p, q, accumulator))

    feasible.sort(reverse=True)
    print("margin\tp\tq\taccumulator")
    for row in feasible[:20]:
        print("\t".join(str(v) for v in row))

    chosen = (F(5, 24), F(25, 48))
    assert any(p == chosen[0] and q == chosen[1] for _, p, q, _ in feasible)
    print(f"published choice p={chosen[0]}, q={chosen[1]}")


if __name__ == "__main__":
    main()
