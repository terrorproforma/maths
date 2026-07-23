#!/usr/bin/env python3
"""Exact rational verifier for the Liu--Reis Conjecture 19 certificate.

The script checks the matrix construction and each inequality in the forcing
proof.  It uses only fractions.Fraction and therefore has no numerical error.
"""

from __future__ import annotations

from fractions import Fraction as F
from typing import Dict, List, Tuple

ETA = F(1, 1000)
ROWS = ["B"] + [name for k in range(1, 6) for name in (f"A{k}", f"H{k}")]
COLUMNS = [name for k in range(1, 6) for name in (f"J{k}", f"K{k}", f"L{k}")]


def build_instance() -> Tuple[Dict[Tuple[str, str], F], Dict[Tuple[str, str], F]]:
    x = {(i, j): F(0) for i in ROWS for j in COLUMNS}
    d = {(i, j): ETA for i in ROWS for j in COLUMNS}

    for k in range(1, 6):
        A, H = f"A{k}", f"H{k}"
        J, K, L = f"J{k}", f"K{k}", f"L{k}"

        x[A, J], x["B", J] = F(19, 24), F(5, 24)
        d[A, J] = d["B", J] = F(1)

        x[A, K], x[H, K] = F(1, 2), F(1, 2)
        d[A, K], d[H, K] = F(1, 2), F(1)

        x[A, L], x[H, L] = F(23, 48), F(25, 48)
        d[A, L] = d[H, L] = F(1)

    return x, d


def check_matrix() -> None:
    x, d = build_instance()
    assert len(ROWS) == 11
    assert len(COLUMNS) == 15
    for j in COLUMNS:
        assert sum(x[i, j] for i in ROWS) == 1
        assert sum(x[i, j] > 0 for i in ROWS) == 2
    assert min(d.values()) == ETA > 0
    assert max(d.values()) == 1


def check_forcing_inequalities() -> None:
    # Before block k, a fresh detector row may have received at most 3(k-1)
    # previous off-support assignments, each of weight ETA.
    for k in range(1, 6):
        previous = 3 * (k - 1)
        start = -previous * ETA

        # Suppose J_k is not assigned to A_k.  A_k gains 19/24.
        after_J_A = start + F(19, 24)
        # H_k can lose one extra ETA if J_k is assigned there.
        after_J_H = start - ETA

        # If K_k is not assigned to A_k, A_k gains 1/4 and already violates.
        violation_at_K = after_J_A + F(1, 4)
        assert violation_at_K > 1

        # Thus K_k must be assigned to A_k.
        after_K_A = after_J_A - F(1, 4)
        after_K_H = after_J_H + F(1, 2)

        # If L_k is assigned to H_k, then A_k is unassigned and gains 23/48.
        violation_if_L_to_H = after_K_A + F(23, 48)
        # If L_k is not assigned to H_k, H_k is unassigned and gains 25/48.
        violation_if_L_not_to_H = after_K_H + F(25, 48)

        assert violation_if_L_to_H > 1
        assert violation_if_L_not_to_H > 1

        print(
            f"block {k}: K-witness={violation_at_K}, "
            f"L->H witness={violation_if_L_to_H}, "
            f"L!->H witness={violation_if_L_not_to_H}"
        )

    # Every discrepancy-good assignment must therefore send every J_k to A_k.
    # Row B gains 5/24 on each J_k.  It can lose at most ETA on each of the ten
    # K/L columns if all of them are assigned off support to B.
    accumulator = 5 * F(5, 24) - 10 * ETA
    assert accumulator == F(619, 600)
    assert accumulator > 1
    print(f"final accumulator lower bound = {accumulator}")


def main() -> None:
    check_matrix()
    check_forcing_inequalities()
    print("chairman certificate verified exactly")


if __name__ == "__main__":
    main()
