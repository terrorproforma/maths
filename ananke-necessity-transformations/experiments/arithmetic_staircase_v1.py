"""Expose the Diophantine skeleton of the classical-memory staircase."""

from __future__ import annotations

import json
from math import pi, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ananke import (
    approximation_record_sequence,
    continued_fraction,
    convergents,
    karpelevich_boundary_radius,
    nearest_root_of_unity,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "arithmetic_staircase_v1.json"
ROOT_DISTANCE_PLOT = ROOT / "results" / "root_approximation_staircase_v1.png"
KARPELEVICH_PLOT = ROOT / "results" / "karpelevich_gap_staircase_v1.png"


def _fraction_dict(fraction) -> dict[str, object]:
    return {
        "numerator": fraction.numerator,
        "denominator": fraction.denominator,
        "value": float(fraction),
    }


def main() -> None:
    phi = (1.0 + sqrt(5.0)) / 2.0
    current_turns = 0.73 / (2.0 * pi)
    noble_turns = 1.0 / (8.0 + 1.0 / phi)
    current_coefficients = continued_fraction(current_turns, 12)
    noble_coefficients = (0, 8) + (1,) * 10
    current_convergents = convergents(current_coefficients)
    noble_convergents = convergents(noble_coefficients)

    maximum_root_order = 350
    orders = np.arange(2, maximum_root_order + 1)
    current_root_distances = np.asarray(
        [nearest_root_of_unity(current_turns, int(order)).root_of_unity_distance for order in orders]
    )
    noble_root_distances = np.asarray(
        [nearest_root_of_unity(noble_turns, int(order)).root_of_unity_distance for order in orders]
    )

    figure, axis = plt.subplots(figsize=(9, 5.5))
    axis.step(orders, current_root_distances, where="post", label="Current 0.73-radian phase")
    axis.step(orders, noble_root_distances, where="post", label=r"Noble target $[0;8,\overline{1}]$")
    axis.set_yscale("log")
    axis.set_xlabel("Maximum classical cycle order")
    axis.set_ylabel("Distance to nearest available root of unity")
    axis.set_title("Arithmetic skeleton of finite-cycle mimicry")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(ROOT_DISTANCE_PLOT, dpi=180)
    plt.close(figure)

    maximum_karpelevich_order = 60
    karpelevich_orders = np.arange(2, maximum_karpelevich_order + 1)
    current_gaps = np.asarray(
        [
            1.0 - karpelevich_boundary_radius(int(order), 2.0 * pi * current_turns)
            for order in karpelevich_orders
        ]
    )
    noble_gaps = np.asarray(
        [
            1.0 - karpelevich_boundary_radius(int(order), 2.0 * pi * noble_turns)
            for order in karpelevich_orders
        ]
    )
    figure, axis = plt.subplots(figsize=(9, 5.5))
    axis.step(karpelevich_orders, current_gaps, where="post", label="Current phase")
    axis.step(karpelevich_orders, noble_gaps, where="post", label="Noble target")
    axis.set_yscale("log")
    axis.set_xlabel("Classical hidden-state count N")
    axis.set_ylabel(r"Radial gap $1-\rho_N(\theta)$")
    axis.set_title("Karpelevič gap plateaus inherit continued-fraction arithmetic")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(KARPELEVICH_PLOT, dpi=180)
    plt.close(figure)

    current_records = approximation_record_sequence(current_turns, maximum_root_order)
    noble_records = approximation_record_sequence(noble_turns, maximum_root_order)
    at_241_current = nearest_root_of_unity(current_turns, 241)
    at_241_noble = nearest_root_of_unity(noble_turns, 241)

    result = {
        "experiment": "ANANKE arithmetic staircase v1",
        "current_phase": {
            "angle_radians": 0.73,
            "turns": current_turns,
            "continued_fraction": list(current_coefficients),
            "convergents": [_fraction_dict(value) for value in current_convergents],
            "best_approximant_change_records": [
                {"first_available_order": order, **approximant.to_dict()}
                for order, approximant in current_records
            ],
        },
        "noble_design_target": {
            "definition": "[0; 8, overline{1}] = 1/(8 + 1/phi)",
            "angle_radians": 2.0 * pi * noble_turns,
            "turns": noble_turns,
            "continued_fraction": list(noble_coefficients),
            "convergents": [_fraction_dict(value) for value in noble_convergents],
            "best_approximant_change_records": [
                {"first_available_order": order, **approximant.to_dict()}
                for order, approximant in noble_records
            ],
        },
        "separation": {
            "angle_difference_radians": abs(0.73 - 2.0 * pi * noble_turns),
            "angle_difference_degrees": abs(0.73 - 2.0 * pi * noble_turns) * 180.0 / pi,
            "order_241_current_nearest_root": at_241_current.to_dict(),
            "order_241_noble_nearest_root": at_241_noble.to_dict(),
            "noble_to_current_root_distance_ratio_at_241": (
                at_241_noble.root_of_unity_distance
                / at_241_current.root_of_unity_distance
            ),
        },
        "design_hypothesis": (
            "For a fixed near-identity phase sector, choosing a noble continued-"
            "fraction tail should delay exceptionally good rational approximants "
            "and therefore make finite periodic classical mimicry asymptotically "
            "more expensive. This is established here as an arithmetic diagnostic, "
            "not yet as an optimality theorem for the full noisy Karpelevič test."
        ),
        "pass": bool(
            current_coefficients[:6] == (0, 8, 1, 1, 1, 1)
            and abs(0.73 - 2.0 * pi * noble_turns) < 0.001
            and at_241_noble.root_of_unity_distance
            > 20.0 * at_241_current.root_of_unity_distance
        ),
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
