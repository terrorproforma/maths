"""False-positive and in-region calibration for the v1 obstruction test."""

from __future__ import annotations

import json
from math import pi
from pathlib import Path

import numpy as np

from ananke import (
    bootstrap_transition_eigenmode,
    classical_cycle_process,
    exclude_finite_stochastic_orders,
    karpelevich_boundary_radius,
    karpelevich_contains,
    select_hankel_rank,
    simulate_shot_dataset,
    words_upto,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "calibration_v1.json"


def _single_cycle_case(damping: float, seed: int) -> dict[str, object]:
    process = classical_cycle_process(
        3,
        damping=damping,
        response_probabilities=np.array([0.17, 0.63, 0.89]),
    )
    words = words_upto(process.alphabet, 9)
    validation_words = tuple(word for word in words if len(word) >= 6)
    dataset = simulate_shot_dataset(
        process,
        words,
        10_000,
        np.random.default_rng(seed),
    )
    rank = select_hankel_rank(
        dataset,
        max_prefix_length=2,
        max_suffix_length=2,
        validation_words=validation_words,
        candidate_ranks=range(1, 4),
    )
    target = complex((1.0 - damping) * np.exp(2j * pi / 3.0))
    eigenmode = bootstrap_transition_eigenmode(
        dataset,
        max_prefix_length=2,
        max_suffix_length=2,
        retained_rank=3,
        symbol="a",
        repetitions=300,
        confidence_level=0.99,
        rng=np.random.default_rng(seed + 1_000),
        target=target,
    )
    exclusion = exclude_finite_stochastic_orders(
        eigenmode.point_estimate,
        eigenmode.confidence_disk_radius,
        confidence_level=0.99,
        hankel_rank_lower_bound=3,
        maximum_order=4,
        coarse_points=128,
    )
    order_three_test = next(test for test in exclusion.tests if test.order == 3)
    return {
        "damping": damping,
        "selected_rank": rank.selected_rank,
        "target_eigenvalue": [target.real, target.imag],
        "point_estimate": [
            eigenmode.point_estimate.real,
            eigenmode.point_estimate.imag,
        ],
        "confidence_disk_radius": eigenmode.confidence_disk_radius,
        "target_inside_confidence_disk": bool(
            abs(eigenmode.point_estimate - target)
            <= eigenmode.confidence_disk_radius
        ),
        "target_inside_Theta_3": karpelevich_contains(target, 3),
        "incorrectly_excludes_three_states": (
            order_three_test.excluded_by_full_region_numerically
        ),
        "classical_state_lower_bound": (
            exclusion.numerical_classical_state_lower_bound
        ),
    }


def main() -> None:
    paper_angle = 7.0 * pi / 12.0
    paper_value = 0.9 * complex(np.exp(1j * paper_angle))
    paper_validation = {
        "value": [paper_value.real, paper_value.imag],
        "Theta_5_boundary_radius": karpelevich_boundary_radius(5, paper_angle),
        "Theta_6_boundary_radius": karpelevich_boundary_radius(6, paper_angle),
        "inside_Theta_5": karpelevich_contains(paper_value, 5),
        "inside_Theta_6": karpelevich_contains(paper_value, 6),
    }

    exact_cycle = _single_cycle_case(0.0, 4_001)
    damped_cycle = _single_cycle_case(0.12, 4_101)

    process = classical_cycle_process(
        3,
        response_probabilities=np.array([0.17, 0.63, 0.89]),
    )
    words = words_upto(process.alphabet, 9)
    validation_words = tuple(word for word in words if len(word) >= 6)
    target = complex(np.exp(2j * pi / 3.0))
    monte_carlo_repetitions = 100
    false_exclusions = 0
    wrong_rank_selections = 0
    confidence_radii: list[float] = []

    for repetition in range(monte_carlo_repetitions):
        dataset = simulate_shot_dataset(
            process,
            words,
            10_000,
            np.random.default_rng(10_000 + repetition),
        )
        rank = select_hankel_rank(
            dataset,
            max_prefix_length=2,
            max_suffix_length=2,
            validation_words=validation_words,
            candidate_ranks=range(1, 4),
        )
        wrong_rank_selections += int(rank.selected_rank != 3)
        eigenmode = bootstrap_transition_eigenmode(
            dataset,
            max_prefix_length=2,
            max_suffix_length=2,
            retained_rank=3,
            symbol="a",
            repetitions=100,
            confidence_level=0.99,
            rng=np.random.default_rng(20_000 + repetition),
            target=target,
        )
        confidence_radii.append(eigenmode.confidence_disk_radius)
        exclusion = exclude_finite_stochastic_orders(
            eigenmode.point_estimate,
            eigenmode.confidence_disk_radius,
            confidence_level=0.99,
            hankel_rank_lower_bound=3,
            maximum_order=3,
            coarse_points=64,
        )
        order_three_test = next(test for test in exclusion.tests if test.order == 3)
        false_exclusions += int(
            order_three_test.excluded_by_full_region_numerically
        )

    monte_carlo = {
        "datasets": monte_carlo_repetitions,
        "shots_per_word": 10_000,
        "bootstrap_repetitions_per_dataset": 100,
        "confidence_level": 0.99,
        "false_exclusions_of_true_three_state_model": false_exclusions,
        "empirical_false_exclusion_rate": (
            false_exclusions / monte_carlo_repetitions
        ),
        "wrong_rank_selections": wrong_rank_selections,
        "median_confidence_disk_radius": float(np.median(confidence_radii)),
    }

    result = {
        "experiment": "ANANKE v1 stochastic calibration",
        "published_boundary_example_reproduction": paper_validation,
        "exact_three_cycle": exact_cycle,
        "damped_three_cycle": damped_cycle,
        "monte_carlo_boundary_calibration": monte_carlo,
        "pass": bool(
            not paper_validation["inside_Theta_5"]
            and paper_validation["inside_Theta_6"]
            and not exact_cycle["incorrectly_excludes_three_states"]
            and not damped_cycle["incorrectly_excludes_three_states"]
            and wrong_rank_selections == 0
            and false_exclusions <= 3
        ),
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
