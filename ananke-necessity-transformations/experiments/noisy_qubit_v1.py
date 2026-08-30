"""ANANKE v1: finite-shot extraction and classical-state lower bounds."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ananke import (
    bootstrap_hankel_singular_values,
    bootstrap_rank_stability,
    bootstrap_transition_eigenmode,
    exclude_finite_stochastic_orders,
    qubit_rotation_process,
    select_hankel_rank,
    simulate_shot_dataset,
    words_upto,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "noisy_qubit_v1.json"


def _complex_pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def main() -> None:
    process = qubit_rotation_process()
    maximum_word_length = 9
    shots_per_word = 10_000
    data_seed = 12_345
    all_words = words_upto(process.alphabet, maximum_word_length)
    validation_words = tuple(word for word in all_words if len(word) >= 8)

    dataset = simulate_shot_dataset(
        process,
        all_words,
        shots_per_word,
        np.random.default_rng(data_seed),
    )
    rank_selection = select_hankel_rank(
        dataset,
        max_prefix_length=3,
        max_suffix_length=3,
        validation_words=validation_words,
        candidate_ranks=range(1, 9),
    )
    rank_stability = bootstrap_rank_stability(
        dataset,
        max_prefix_length=3,
        max_suffix_length=3,
        validation_words=validation_words,
        candidate_ranks=range(1, 9),
        repetitions=100,
        rng=np.random.default_rng(22_222),
    )
    singular_values = bootstrap_hankel_singular_values(
        dataset,
        max_prefix_length=3,
        max_suffix_length=3,
        number_of_values=8,
        repetitions=300,
        confidence_level=0.99,
        rng=np.random.default_rng(31_337),
    )

    exact_x_mode = complex(np.exp(0.73j))
    eigenmode = bootstrap_transition_eigenmode(
        dataset,
        max_prefix_length=3,
        max_suffix_length=3,
        retained_rank=rank_selection.selected_rank,
        symbol="x",
        repetitions=600,
        confidence_level=0.99,
        rng=np.random.default_rng(333),
        target=exact_x_mode,
    )
    exclusion = exclude_finite_stochastic_orders(
        eigenmode.point_estimate,
        eigenmode.confidence_disk_radius,
        confidence_level=eigenmode.confidence_level,
        hankel_rank_lower_bound=rank_selection.selected_rank,
        maximum_order=30,
        coarse_points=128,
    )

    rank_four_probability = rank_stability.probabilities.get(4, 0.0)
    true_mode_error = float(abs(eigenmode.point_estimate - exact_x_mode))
    result = {
        "experiment": "ANANKE noisy qubit v1",
        "claim_tested": (
            "Finite-shot sequential probabilities can recover a stable minimal "
            "predictive rank, attach uncertainty to a similarity-invariant mode, "
            "and force a lower bound on any exact finite classical realization."
        ),
        "data": {
            "seed": data_seed,
            "alphabet": list(process.alphabet),
            "maximum_word_length": maximum_word_length,
            "measured_word_count": len(all_words),
            "shots_per_word": shots_per_word,
            "total_trials": dataset.total_trials,
            "hankel_prefix_length": 3,
            "hankel_suffix_length": 3,
            "validation_word_lengths": [8, 9],
            "validation_word_count": len(validation_words),
        },
        "rank_selection": rank_selection.to_dict(),
        "rank_stability": rank_stability.to_dict(),
        "singular_value_bootstrap": singular_values.to_dict(),
        "x_eigenmode_bootstrap": eigenmode.to_dict(include_samples=False),
        "exact_reference": {
            "x_mode": _complex_pair(exact_x_mode),
            "point_estimate_error": true_mode_error,
            "exact_mode_inside_reported_confidence_disk": bool(
                true_mode_error <= eigenmode.confidence_disk_radius
            ),
        },
        "finite_classical_state_exclusion": exclusion.to_dict(),
        "pass": bool(
            rank_selection.selected_rank == 4
            and rank_four_probability >= 0.90
            and true_mode_error <= eigenmode.confidence_disk_radius
            and exclusion.analytic_classical_state_lower_bound >= 9
            and exclusion.numerical_classical_state_lower_bound >= 9
        ),
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
