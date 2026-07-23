#!/usr/bin/env python3
"""Reconstruct the integer SSUF certificate from its rational family."""

from __future__ import annotations

from fractions import Fraction
from math import lcm


def L(*values: Fraction) -> int:
    scale = 1
    for value in values:
        scale = lcm(scale, value.denominator)
    return scale


def main() -> None:
    # Normalized maximum demand D=1.  Cheap-path probabilities are r,q,r.
    b = Fraction(2, 3)  # middle demand
    r = Fraction(1, 3)
    q = Fraction(2, 5)

    # Cost preservation forces at least two cheap paths when 2r+q>1.
    cheap_mass = 2 * r + q
    assert cheap_mass == Fraction(16, 15) > 1

    # Additive load needed by the three possible cheap pairs.
    pair_12_or_23 = 1 + b * (1 - q) - r
    pair_13 = 2 - 2 * r - b * q
    assert pair_12_or_23 == pair_13 == Fraction(16, 15)

    # Choose the smallest convenient scale making this displayed instance
    # integral.  The resulting maximum demand is 15 and every critical pair
    # exceeds x+D by exactly one unit.
    quantities = [
        b,
        r,
        b * q,
        1 - r,
        b * (1 - q),
        1 + r + b * q,
        2 * r + b * q,
        r + b * q,
    ]
    scale = L(*quantities)
    assert scale == 15

    d1, d2, d3 = scale, int(scale * b), scale
    x = {
        "s->t1": int(scale * (1 - r)),
        "s->t2": int(scale * b * (1 - q)),
        "s->u": int(scale * (1 + r + b * q)),
        "u->t3": int(scale * (1 - r)),
        "u->v": int(scale * (2 * r + b * q)),
        "v->t1": int(scale * r),
        "v->w": int(scale * (r + b * q)),
        "w->t2": int(scale * b * q),
        "w->t3": int(scale * r),
    }
    expected = {
        "s->t1": 10,
        "s->t2": 6,
        "s->u": 24,
        "u->t3": 10,
        "u->v": 14,
        "v->t1": 5,
        "v->w": 9,
        "w->t2": 4,
        "w->t3": 5,
    }
    assert x == expected

    # Give each expensive integral path total cost 30.
    common_path_cost = lcm(d1, d2, d3)
    costs = {
        "s->t1": common_path_cost // d1,
        "s->t2": common_path_cost // d2,
        "u->t3": common_path_cost // d3,
    }
    assert common_path_cost == 30
    assert costs == {"s->t1": 2, "s->t2": 3, "u->t3": 2}

    fractional_cost = int(common_path_cost * (3 - cheap_mass))
    integral_good_cost = 2 * common_path_cost
    assert fractional_cost == 58
    assert integral_good_cost == 60

    print(f"normalized demands: (1, {b}, 1)")
    print(f"cheap probabilities: ({r}, {q}, {r})")
    print(f"violated triangle mass: {cheap_mass}")
    print(f"required additive coefficient for every cheap pair: {pair_13}")
    print(f"integer demands: {(d1, d2, d3)}")
    print(f"integer fractional loads: {x}")
    print(f"nonzero per-unit costs: {costs}")
    print(f"cost gap: {fractional_cost} < {integral_good_cost}")


if __name__ == "__main__":
    main()
