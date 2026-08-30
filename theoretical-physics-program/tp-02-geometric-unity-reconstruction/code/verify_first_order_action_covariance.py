#!/usr/bin/env python3
"""Exact covariance audit for the first-order bosonic action skeleton.

The action is represented by an invariant trace pairing I=Tr(T Q).  The
source claims the Shiab/curvature factor Q transforms covariantly under the
tilted stabilizer.  This script proves that the literal printed augmented
torsion then produces a finite action defect, while the repaired plus-sign
branch is exactly invariant.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_inhomogeneous_group_signs import (
    A0,
    add,
    conjugate,
    covariant_derivative_a0,
    inverse_2x2,
    matrix,
    multiply,
    semidirect_product,
    subtract,
    tau_minus,
    torsion_minus,
    torsion_plus,
    serialize,
)


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def pairing(a, b):
    return trace(multiply(a, b))


def build_results() -> dict:
    epsilon = matrix([[1, 1], [0, 1]])
    a = matrix([[0, 1], [1, 0]])
    h = matrix([[2, 0], [1, 1]])
    q = matrix([[1, 2], [3, 4]])
    g = (epsilon, a)

    transformed_g = semidirect_product(g, tau_minus(h))
    transformed_q = conjugate(q, h)

    printed_before = pairing(torsion_minus(g), q)
    printed_after = pairing(torsion_minus(transformed_g), transformed_q)
    printed_defect = printed_after - printed_before

    repaired_before = pairing(torsion_plus(g), q)
    repaired_after = pairing(torsion_plus(transformed_g), transformed_q)
    repaired_defect = repaired_after - repaired_before

    defect_matrix = subtract(torsion_minus(transformed_g), conjugate(torsion_minus(g), h))
    predicted_defect_matrix = [
        [-2 * value for value in row]
        for row in multiply(inverse_2x2(h), covariant_derivative_a0(h))
    ]
    predicted_action_defect = pairing(predicted_defect_matrix, transformed_q)

    checks = {
        "trace_pairing_is_Ad_invariant_for_test_data": pairing(conjugate(torsion_plus(g), h), transformed_q)
        == repaired_before,
        "printed_action_is_invariant": printed_defect == 0,
        "printed_action_defect_equals_14": printed_defect == 14,
        "printed_action_defect_matches_analytic_matrix_defect": printed_defect == predicted_action_defect,
        "repaired_action_is_invariant": repaired_defect == 0,
    }

    return {
        "schema_version": "1.0.0",
        "project": "TP-02 independent Geometric Unity reconstruction",
        "phase": "first-order action covariance audit",
        "assumptions": [
            "The first-order action uses an Ad-invariant bilinear pairing.",
            "The Shiab/curvature output Q transforms covariantly under the printed tilted stabilizer.",
            "No extra affine compensator is hidden in Q.",
        ],
        "exact_test_data": {
            "A0": serialize(A0),
            "epsilon": serialize(epsilon),
            "a": serialize(a),
            "h": serialize(h),
            "Q": serialize(q),
            "Q_transformed": serialize(transformed_q),
        },
        "literal_printed_branch": {
            "action_before": str(printed_before),
            "action_after": str(printed_after),
            "defect": str(printed_defect),
            "defect_matrix": serialize(defect_matrix),
            "predicted_defect_matrix": serialize(predicted_defect_matrix),
            "verdict": "FAILS finite tilted-gauge invariance",
        },
        "repaired_plus_branch": {
            "action_before": str(repaired_before),
            "action_after": str(repaired_after),
            "defect": str(repaired_defect),
            "verdict": "PASSES the finite covariance test",
        },
        "checks": checks,
        "terminal_statement": "The literal printed action skeleton cannot be tilted-gauge invariant with a covariant Q; the plus-sign repaired branch removes this kinematic obstruction.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    result = build_results()
    output = root / "results" / "first_order_action_covariance.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

    if not result["checks"]["trace_pairing_is_Ad_invariant_for_test_data"]:
        raise SystemExit(1)
    if result["checks"]["printed_action_is_invariant"]:
        raise SystemExit(1)
    if not result["checks"]["printed_action_defect_equals_14"]:
        raise SystemExit(1)
    if not result["checks"]["printed_action_defect_matches_analytic_matrix_defect"]:
        raise SystemExit(1)
    if not result["checks"]["repaired_action_is_invariant"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
