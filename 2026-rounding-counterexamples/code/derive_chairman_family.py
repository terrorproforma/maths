#!/usr/bin/env python3
"""Verify the parametric inequalities behind the chairman gadget."""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    blocks = 5
    p = Fraction(5, 24)   # accumulator share in J
    a = Fraction(1, 2)    # A-row weight in K
    q = Fraction(25, 48)  # H-row share in L
    eta = Fraction(1, 1000)

    # Ignoring the small off-support penalty, these are the three forcing
    # margins.  They must all be positive.
    margin_K_not_A = a / 2 - p
    margin_L_to_H = 1 - p - a / 2 - q
    margin_L_not_H = q - Fraction(1, 2)
    accumulator_margin = blocks * p - 1

    assert margin_K_not_A == Fraction(1, 24) > 0
    assert margin_L_to_H == Fraction(1, 48) > 0
    assert margin_L_not_H == Fraction(1, 48) > 0
    assert accumulator_margin == Fraction(1, 24) > 0

    # The first detector row can lose at most 12 eta before its block, while
    # the second can lose at most 13 eta after a possible off-support J choice.
    assert margin_K_not_A > 12 * eta
    assert margin_L_to_H > 12 * eta
    assert margin_L_not_H > 13 * eta
    assert accumulator_margin > 2 * blocks * eta

    detector = 1 + min(
        margin_L_to_H - 12 * eta,
        margin_L_not_H - 13 * eta,
    )
    accumulator = blocks * p - 2 * blocks * eta

    assert detector == Fraction(6047, 6000) > 1
    assert accumulator == Fraction(619, 600) > 1

    print(f"p={p}, a={a}, q={q}, eta={eta}, blocks={blocks}")
    print(
        "forcing margins: "
        f"K={margin_K_not_A}, L-to-H={margin_L_to_H}, "
        f"L-not-to-H={margin_L_not_H}"
    )
    print(f"detector lower bound: {detector}")
    print(f"accumulator lower bound: {accumulator}")


if __name__ == "__main__":
    main()
