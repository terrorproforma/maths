#!/usr/bin/env python3
"""Exact certificate verifier for the machine-dependent chairman example.

The proof is a finite symbolic forcing argument.  This script reconstructs the
11-by-15 rational instance and checks every inequality in that certificate
using fractions, including the worst possible effects of assignments outside
the fractional support.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "chairman_instance.json"


def F(value: str | int) -> Fraction:
    return Fraction(str(value))


def main() -> None:
    instance = json.loads(DATA.read_text(encoding="utf-8"))
    rows = tuple(instance["rows"])
    columns = tuple(instance["columns"])
    eta = F(instance["default_weight"])
    default_x = F(instance["default_fractional_entry"])
    number_of_blocks = int(instance["number_of_blocks"])

    assert len(rows) == 11
    assert len(columns) == 15
    assert number_of_blocks == 5
    assert eta == Fraction(1, 1000)

    x: Dict[Tuple[str, str], Fraction] = {
        (row, column): default_x for row in rows for column in columns
    }
    d: Dict[Tuple[str, str], Fraction] = {
        (row, column): eta for row in rows for column in columns
    }

    for k in range(1, number_of_blocks + 1):
        A, H = f"A{k}", f"H{k}"
        J, K, L = f"J{k}", f"K{k}", f"L{k}"

        x[A, J], x["B", J] = Fraction(19, 24), Fraction(5, 24)
        d[A, J], d["B", J] = Fraction(1), Fraction(1)

        x[A, K], x[H, K] = Fraction(1, 2), Fraction(1, 2)
        d[A, K], d[H, K] = Fraction(1, 2), Fraction(1)

        x[A, L], x[H, L] = Fraction(23, 48), Fraction(25, 48)
        d[A, L], d[H, L] = Fraction(1), Fraction(1)

    # Basic instance checks from the conjecture.
    for column in columns:
        assert sum(x[row, column] for row in rows) == 1
        assert sum(x[row, column] > 0 for row in rows) == 2
    assert all(weight > 0 for weight in d.values())
    assert max(d.values()) == Fraction(1)

    # At the start of block k, either fresh detector row could have received
    # every preceding column outside its support.  There are at most 12 such
    # columns, and each contributes only -eta.
    worst_previous = -12 * eta

    # Assume J_k is not assigned to A_k.  If K_k is not assigned to A_k,
    # A_k already exceeds the conjectured bound.
    k_not_to_A = worst_previous + Fraction(19, 24) + Fraction(1, 4)
    assert k_not_to_A > 1

    # Hence K_k must be assigned to A_k.  These are lower bounds immediately
    # after K_k, allowing J_k itself to have been assigned to H_k at cost eta.
    A_after_forced_K = worst_previous + Fraction(19, 24) - Fraction(1, 4)
    H_after_forced_K = worst_previous - eta + Fraction(1, 2)

    # If L_k goes to H_k, A_k is unassigned; otherwise H_k is unassigned.
    violation_if_L_to_H = A_after_forced_K + Fraction(23, 48)
    violation_if_L_not_to_H = H_after_forced_K + Fraction(25, 48)
    detector_lower_bound = min(violation_if_L_to_H, violation_if_L_not_to_H)

    assert violation_if_L_to_H == Fraction(49, 48) - 12 * eta
    assert violation_if_L_not_to_H == Fraction(49, 48) - 13 * eta
    assert detector_lower_bound == F(instance["claimed_detector_lower_bound"])
    assert detector_lower_bound > 1

    # Therefore each J_k must be assigned to A_k.  The accumulator B is then
    # unassigned on all five J-columns and gains 5/24 each time.  It can lose
    # at most eta on each of the ten detector columns.
    accumulator = number_of_blocks * Fraction(5, 24) - 2 * number_of_blocks * eta
    assert accumulator == F(instance["claimed_accumulator_lower_bound"])
    assert accumulator == Fraction(619, 600)
    assert accumulator > 1

    print("Machine-dependent chairman instance checks:")
    print(f"  rows={len(rows)}, columns={len(columns)}, D={max(d.values())}")
    print(f"  K not assigned to A: lower bound {k_not_to_A}")
    print(f"  L assigned to H:     lower bound {violation_if_L_to_H}")
    print(f"  L not assigned to H: lower bound {violation_if_L_not_to_H}")
    print(
        "\nChairman certificate verified: forced accumulator lower bound = "
        f"{accumulator} > 1"
    )


if __name__ == "__main__":
    main()
