#!/usr/bin/env python3
"""Exact sign-convention audit for Geometric Unity draft sections 5--7.

The script uses 2x2 rational matrices and an inner derivation d(M)=[D,M].
A claimed algebraic identity must hold in every representation, so one exact
counterexample is sufficient to disprove the printed transformation law.

This is a source-consistency audit, not a test of the full dynamics.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import List, Tuple

Matrix = List[List[Fraction]]
GroupElement = Tuple[Matrix, Matrix]


def matrix(rows) -> Matrix:
    return [[Fraction(value) for value in row] for row in rows]


def add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def subtract(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def negate(a: Matrix) -> Matrix:
    return [[-entry for entry in row] for row in a]


def scale(c: Fraction, a: Matrix) -> Matrix:
    return [[c * entry for entry in row] for row in a]


def multiply(a: Matrix, b: Matrix) -> Matrix:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def inverse_2x2(a: Matrix) -> Matrix:
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if determinant == 0:
        raise ValueError("matrix is singular")
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def equal(a: Matrix, b: Matrix) -> bool:
    return all(a[i][j] == b[i][j] for i in range(len(a)) for j in range(len(a[0])))


def zero_like(a: Matrix) -> Matrix:
    return [[Fraction(0) for _ in row] for row in a]


def commutator(a: Matrix, b: Matrix) -> Matrix:
    return subtract(multiply(a, b), multiply(b, a))


def conjugate(a: Matrix, h: Matrix) -> Matrix:
    return multiply(multiply(inverse_2x2(h), a), h)


def serialize(a: Matrix):
    return [[str(entry) for entry in row] for row in a]


D = matrix([[0, 1], [0, 0]])
A0 = matrix([[1, 0], [0, -1]])


def exterior_derivative(a: Matrix) -> Matrix:
    """Exact derivation represented by [D,a]."""
    return commutator(D, a)


def covariant_derivative_a0(h: Matrix) -> Matrix:
    return add(exterior_derivative(h), commutator(A0, h))


def ordinary_right_gauge_action(a_connection: Matrix, epsilon: Matrix) -> Matrix:
    epsilon_inverse = inverse_2x2(epsilon)
    return add(
        multiply(multiply(epsilon_inverse, a_connection), epsilon),
        multiply(epsilon_inverse, exterior_derivative(epsilon)),
    )


def semidirect_product(g1: GroupElement, g2: GroupElement) -> GroupElement:
    """Printed right semidirect-product convention."""
    epsilon1, a1 = g1
    epsilon2, a2 = g2
    return multiply(epsilon1, epsilon2), add(conjugate(a1, epsilon2), a2)


def affine_right_action(alpha: Matrix, g: GroupElement) -> Matrix:
    """Action on alpha=A-A0 corresponding to draft equation (6.2)."""
    epsilon, a = g
    return add(
        add(
            conjugate(alpha, epsilon),
            multiply(inverse_2x2(epsilon), covariant_derivative_a0(epsilon)),
        ),
        a,
    )


def connection_right_action(a_connection: Matrix, g: GroupElement) -> Matrix:
    epsilon, a = g
    return add(ordinary_right_gauge_action(a_connection, epsilon), a)


def tau_minus(h: Matrix) -> GroupElement:
    """Draft equation (6.4): the actual stabilizer of A0."""
    return h, negate(multiply(inverse_2x2(h), covariant_derivative_a0(h)))


def tau_plus(h: Matrix) -> GroupElement:
    """Alternative sign: repairs T_minus equivariance but not stabilization."""
    return h, multiply(inverse_2x2(h), covariant_derivative_a0(h))


def torsion_minus(g: GroupElement) -> Matrix:
    """Literal draft equation (7.3)."""
    epsilon, a = g
    return subtract(a, multiply(inverse_2x2(epsilon), covariant_derivative_a0(epsilon)))


def torsion_plus(g: GroupElement) -> Matrix:
    """Minimal repair compatible with the printed stabilizer convention."""
    epsilon, a = g
    return add(a, multiply(inverse_2x2(epsilon), covariant_derivative_a0(epsilon)))


def group_equal(g1: GroupElement, g2: GroupElement) -> bool:
    return equal(g1[0], g2[0]) and equal(g1[1], g2[1])


def build_results() -> dict:
    epsilon = matrix([[1, 1], [0, 1]])
    h = matrix([[2, 0], [1, 1]])
    a = matrix([[0, 1], [1, 0]])
    g = (epsilon, a)

    g1 = (matrix([[1, 1], [0, 1]]), matrix([[0, 1], [1, 0]]))
    g2 = (matrix([[2, 1], [1, 1]]), matrix([[1, 0], [0, -1]]))
    g3 = (matrix([[1, 0], [1, 1]]), matrix([[1, 1], [0, 1]]))

    associative_left = semidirect_product(semidirect_product(g1, g2), g3)
    associative_right = semidirect_product(g1, semidirect_product(g2, g3))

    zero = matrix([[0, 0], [0, 0]])
    action_left = affine_right_action(affine_right_action(zero, g1), g2)
    action_right = affine_right_action(zero, semidirect_product(g1, g2))

    tau_minus_product = semidirect_product(tau_minus(g1[0]), tau_minus(g2[0]))
    tau_minus_of_product = tau_minus(multiply(g1[0], g2[0]))
    tau_plus_product = semidirect_product(tau_plus(g1[0]), tau_plus(g2[0]))
    tau_plus_of_product = tau_plus(multiply(g1[0], g2[0]))

    transformed_minus = torsion_minus(semidirect_product(g, tau_minus(h)))
    expected_minus = conjugate(torsion_minus(g), h)
    minus_residual = subtract(transformed_minus, expected_minus)
    predicted_minus_residual = scale(
        Fraction(-2), multiply(inverse_2x2(h), covariant_derivative_a0(h))
    )

    transformed_plus = torsion_plus(semidirect_product(g, tau_minus(h)))
    expected_plus = conjugate(torsion_plus(g), h)
    plus_residual = subtract(transformed_plus, expected_plus)

    transformed_minus_tau_plus = torsion_minus(semidirect_product(g, tau_plus(h)))
    expected_minus_tau_plus = conjugate(torsion_minus(g), h)
    minus_tau_plus_residual = subtract(transformed_minus_tau_plus, expected_minus_tau_plus)

    tau_minus_stabilizer_residual = subtract(connection_right_action(A0, tau_minus(h)), A0)
    tau_plus_stabilizer_residual = subtract(connection_right_action(A0, tau_plus(h)), A0)

    checks = {
        "printed_semidirect_product_is_associative_in_exact_test": group_equal(associative_left, associative_right),
        "printed_affine_formula_is_a_right_action_in_exact_test": equal(action_left, action_right),
        "printed_tau_minus_is_a_homomorphism_in_exact_test": group_equal(tau_minus_product, tau_minus_of_product),
        "printed_tau_minus_stabilizes_A0": equal(tau_minus_stabilizer_residual, zero),
        "printed_T_minus_is_equivariant_under_tau_minus": equal(minus_residual, zero),
        "T_minus_failure_matches_minus_2_h_inverse_dA0_h": equal(minus_residual, predicted_minus_residual),
        "repaired_T_plus_is_equivariant_under_tau_minus": equal(plus_residual, zero),
        "alternative_tau_plus_is_a_homomorphism_in_exact_test": group_equal(tau_plus_product, tau_plus_of_product),
        "printed_T_minus_is_equivariant_under_tau_plus": equal(minus_tau_plus_residual, zero),
        "alternative_tau_plus_stabilizes_A0": equal(tau_plus_stabilizer_residual, zero),
    }

    return {
        "schema_version": "1.0.0",
        "project": "TP-02 independent Geometric Unity reconstruction",
        "phase": "inhomogeneous gauge-group sign audit",
        "source_equations": {
            "right_affine_action": "draft eq. (6.2)",
            "tilted_stabilizer": "draft eq. (6.4), used again in eq. (6.13)",
            "augmented_torsion": "draft eq. (7.3)",
            "claimed_equivariance": "draft Lemma 7.2 and eq. (7.4)",
            "source_warning": "draft footnote 7 says section 6 may contain conflicting conventions",
        },
        "exact_test_data": {
            "D": serialize(D),
            "A0": serialize(A0),
            "epsilon": serialize(epsilon),
            "h": serialize(h),
            "a": serialize(a),
        },
        "checks": checks,
        "printed_equivariance_counterexample": {
            "T_minus_after_right_tau_minus_action": serialize(transformed_minus),
            "Ad_h_inverse_T_minus": serialize(expected_minus),
            "residual": serialize(minus_residual),
            "predicted_residual_minus_2_h_inverse_dA0_h": serialize(predicted_minus_residual),
        },
        "repair_A": {
            "description": "Keep the printed right action and stabilizing tau_minus; reverse the connection-difference order, equivalently use T_plus=a+epsilon^{-1}d_A0 epsilon.",
            "residual": serialize(plus_residual),
            "equivariant": equal(plus_residual, zero),
            "tau_still_stabilizes_A0": equal(tau_minus_stabilizer_residual, zero),
        },
        "repair_B": {
            "description": "Keep printed T_minus but flip tau to tau_plus.",
            "equivariance_residual": serialize(minus_tau_plus_residual),
            "equivariant": equal(minus_tau_plus_residual, zero),
            "A0_stabilizer_residual": serialize(tau_plus_stabilizer_residual),
            "stabilizes_A0": equal(tau_plus_stabilizer_residual, zero),
        },
        "verdict": {
            "printed_equations_mutually_consistent": False,
            "minimal_source_compatible_repair": "Keep the right action and stabilizer; use T_plus or reverse the ordered affine difference.",
            "scope": "A repairable sign inconsistency in the printed source, not a no-go theorem against every repaired Geometric Unity model.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    result = build_results()
    out = root / "results" / "inhomogeneous_group_sign_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

    required_true = [
        "printed_semidirect_product_is_associative_in_exact_test",
        "printed_affine_formula_is_a_right_action_in_exact_test",
        "printed_tau_minus_is_a_homomorphism_in_exact_test",
        "printed_tau_minus_stabilizes_A0",
        "T_minus_failure_matches_minus_2_h_inverse_dA0_h",
        "repaired_T_plus_is_equivariant_under_tau_minus",
        "alternative_tau_plus_is_a_homomorphism_in_exact_test",
        "printed_T_minus_is_equivariant_under_tau_plus",
    ]
    required_false = [
        "printed_T_minus_is_equivariant_under_tau_minus",
        "alternative_tau_plus_stabilizes_A0",
    ]
    if not all(result["checks"][key] for key in required_true):
        raise SystemExit(1)
    if not all(not result["checks"][key] for key in required_false):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
