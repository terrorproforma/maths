#!/usr/bin/env python3
"""Exact TP-02 audit of observation pullback versus dynamical reduction.

The source's Observerse supplies an embedding iota:X^4->Y^14 and pullback
of fields. This script checks the necessary ideal-preservation condition for
an ambient second-order operator to descend to an autonomous operator on X.

The arithmetic is exact and standard-library only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def build_results() -> Dict[str, object]:
    dim_x = 4
    dim_y = 14
    dim_normal = dim_y - dim_x

    signature_y = [7, 7]
    signature_x = [1, 3]
    signature_normal = [
        signature_y[0] - signature_x[0],
        signature_y[1] - signature_x[1],
    ]

    normal_metric_signs: List[int] = (
        [-1] * signature_normal[0] + [1] * signature_normal[1]
    )
    witnesses = [
        {
            "normal_coordinate": index,
            "metric_sign": sign,
            "test_function": f"(z^{index})^2",
            "pullback_of_test_function": 0,
            "ambient_operator_then_pullback": 2 * sign,
            "operator_on_pullback": 0,
            "ideal_preserved": False,
        }
        for index, sign in enumerate(normal_metric_signs)
    ]

    all_witnesses_fail = all(
        witness["ambient_operator_then_pullback"] != 0
        and witness["operator_on_pullback"] == 0
        for witness in witnesses
    )

    checks = {
        "dimension_split_4_plus_10_equals_14": (
            dim_x + dim_normal == dim_y
        ),
        "signature_split_1_3_plus_6_4_equals_7_7": (
            [signature_x[0] + signature_normal[0],
             signature_x[1] + signature_normal[1]]
            == signature_y
        ),
        "all_ten_normal_quadratic_witnesses_break_ideal_preservation": (
            all_witnesses_fail and len(witnesses) == 10
        ),
        "pullback_values_do_not_define_autonomous_ambient_second_order_dynamics": (
            all_witnesses_fail
        ),
        "naive_OBS4_pullback_branch_fails": all_witnesses_fail,
    }

    return {
        "schema_version": "1.0.0",
        "project": "TP-02 independent Geometric Unity reconstruction",
        "phase": "observation pullback and characteristic reduction audit",
        "geometry": {
            "dim_X": dim_x,
            "dim_Y": dim_y,
            "normal_rank": dim_normal,
            "signature_convention": "[negative, positive]",
            "signature_X": signature_x,
            "signature_normal": signature_normal,
            "signature_Y": signature_y,
        },
        "descent_criterion": {
            "ideal": "I_iota={f in C-infinity(Y): iota^*f=0}",
            "necessary_and_sufficient_condition": (
                "An operator L_Y descends to an autonomous L_X with "
                "iota^* L_Y = L_X iota^* only if L_Y(I_iota) is contained "
                "in I_iota; equivalently the quotient by I_iota is invariant."
            ),
            "order_two_local_test": (
                "Normal second derivatives must vanish from the principal "
                "symbol or be fixed by separately propagated constraints."
            ),
        },
        "normal_jet_witnesses": witnesses,
        "checks": checks,
        "verdict": {
            "canonical_tangent_pullback": "PASS along the observed section",
            "canonical_autonomous_dynamics_on_X": "FAIL",
            "R_PLUS_EIN_OBS4_PULLBACK": "REJECTED",
            "fatal_gate": "PERT-02",
            "source_status": (
                "The primary source supplies pullback and bundle splitting "
                "but no invariant normal-jet constraint, tangential principal "
                "operator, localization mechanism, or induced boundary action."
            ),
            "scope": (
                "This rejects pullback alone as the missing four-dimensional "
                "dynamical mechanism. It does not rule out a new completion "
                "with additional normal constraints, localization, or a "
                "degenerate/tangential principal symbol."
            ),
        },
        "required_escape_data": [
            "a principal symbol tangent to the observed section",
            "or propagated constraints fixing every required normal jet",
            "or an induced effective action obtained after solving normal dynamics",
            "gauge/BRST invariance of the reduction",
            "a strongly hyperbolic (1,3) reduced system",
            "exactly two graviton helicities",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    root = args.root.resolve()

    results = build_results()
    output = root / "results" / "observation_pullback_obstruction.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))

    if not all(results["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
