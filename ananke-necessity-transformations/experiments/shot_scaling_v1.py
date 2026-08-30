"""Shot-budget scaling of the finite classical-state lower bound."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt
import numpy as np

from ananke import (
    bootstrap_transition_eigenmode,
    exclude_finite_stochastic_orders,
    qubit_rotation_process,
    select_hankel_rank,
    simulate_shot_dataset,
    words_upto,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "shot_scaling_v1.json"
PLOT_PATH = ROOT / "results" / "shot_scaling_v1.png"


def _run_replicate(
    shots_per_word: int,
    replicate: int,
    all_words: list[str],
    validation_words: tuple[str, ...],
) -> dict[str, object]:
    process = qubit_rotation_process()
    data_seed = 100 + replicate
    bootstrap_seed = 1_000 + replicate
    dataset = simulate_shot_dataset(
        process,
        all_words,
        shots_per_word,
        np.random.default_rng(data_seed),
    )
    rank = select_hankel_rank(
        dataset,
        max_prefix_length=3,
        max_suffix_length=3,
        validation_words=validation_words,
        candidate_ranks=range(1, 9),
    )
    eigenmode = bootstrap_transition_eigenmode(
        dataset,
        max_prefix_length=3,
        max_suffix_length=3,
        retained_rank=rank.selected_rank,
        symbol="x",
        repetitions=100,
        confidence_level=0.95,
        rng=np.random.default_rng(bootstrap_seed),
        target=complex(np.exp(0.73j)),
    )
    exclusion = exclude_finite_stochastic_orders(
        eigenmode.point_estimate,
        eigenmode.confidence_disk_radius,
        confidence_level=0.95,
        hankel_rank_lower_bound=rank.selected_rank,
        maximum_order=25,
        coarse_points=64,
    )
    return {
        "replicate": replicate,
        "data_seed": data_seed,
        "bootstrap_seed": bootstrap_seed,
        "selected_rank": rank.selected_rank,
        "best_predictive_rank": rank.best_predictive_rank,
        "point_estimate": [
            eigenmode.point_estimate.real,
            eigenmode.point_estimate.imag,
        ],
        "confidence_disk_radius": eigenmode.confidence_disk_radius,
        "analytic_classical_state_lower_bound": (
            exclusion.analytic_classical_state_lower_bound
        ),
        "numerical_classical_state_lower_bound": (
            exclusion.numerical_classical_state_lower_bound
        ),
    }


def main() -> None:
    process = qubit_rotation_process()
    all_words = words_upto(process.alphabet, 9)
    validation_words = tuple(word for word in all_words if len(word) >= 8)
    budgets = [200, 500, 1_000, 2_000, 5_000, 10_000, 50_000]
    replicate_count = 5

    summaries: list[dict[str, object]] = []
    for shots in budgets:
        replicates = [
            _run_replicate(shots, replicate, all_words, validation_words)
            for replicate in range(replicate_count)
        ]
        analytic_bounds = [
            int(row["analytic_classical_state_lower_bound"])
            for row in replicates
        ]
        numerical_bounds = [
            int(row["numerical_classical_state_lower_bound"])
            for row in replicates
        ]
        selected_ranks = [int(row["selected_rank"]) for row in replicates]
        radii = [float(row["confidence_disk_radius"]) for row in replicates]
        summaries.append(
            {
                "shots_per_word": shots,
                "total_trials_per_replicate": shots * len(all_words),
                "replicates": replicates,
                "summary": {
                    "median_selected_rank": float(median(selected_ranks)),
                    "rank_four_frequency": selected_ranks.count(4) / replicate_count,
                    "median_confidence_disk_radius": float(median(radii)),
                    "median_analytic_classical_state_lower_bound": float(
                        median(analytic_bounds)
                    ),
                    "minimum_analytic_classical_state_lower_bound": min(analytic_bounds),
                    "maximum_analytic_classical_state_lower_bound": max(analytic_bounds),
                    "median_numerical_classical_state_lower_bound": float(
                        median(numerical_bounds)
                    ),
                    "minimum_numerical_classical_state_lower_bound": min(numerical_bounds),
                    "maximum_numerical_classical_state_lower_bound": max(numerical_bounds),
                },
            }
        )

    x = np.asarray(budgets, dtype=float)
    analytic = np.asarray(
        [
            row["summary"]["median_analytic_classical_state_lower_bound"]
            for row in summaries
        ],
        dtype=float,
    )
    numerical = np.asarray(
        [
            row["summary"]["median_numerical_classical_state_lower_bound"]
            for row in summaries
        ],
        dtype=float,
    )
    numerical_min = np.asarray(
        [
            row["summary"]["minimum_numerical_classical_state_lower_bound"]
            for row in summaries
        ],
        dtype=float,
    )
    numerical_max = np.asarray(
        [
            row["summary"]["maximum_numerical_classical_state_lower_bound"]
            for row in summaries
        ],
        dtype=float,
    )

    figure, axis = plt.subplots(figsize=(9, 5.5))
    axis.set_xscale("log")
    axis.plot(x, analytic, marker="o", label="Analytic wedge lower bound")
    numerical_line = axis.plot(
        x,
        numerical,
        marker="o",
        label="Full Karpelevič numerical lower bound",
    )[0]
    axis.fill_between(
        x,
        numerical_min,
        numerical_max,
        alpha=0.15,
        color=numerical_line.get_color(),
        label="Five-replicate range",
    )
    axis.set_xlabel("Shots per operation word")
    axis.set_ylabel("Minimum classical hidden states")
    axis.set_title("ANANKE v1: finite-data classical complexity ladder")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PLOT_PATH, dpi=180)
    plt.close(figure)

    result = {
        "experiment": "ANANKE shot scaling v1",
        "confidence_level": 0.95,
        "bootstrap_repetitions_per_dataset": 100,
        "independent_datasets_per_budget": replicate_count,
        "measured_words": len(all_words),
        "budgets": summaries,
        "interpretation": (
            "The bound is a statistical staircase rather than a smooth curve. "
            "Farey/Karpelevič regions expand in discrete geometric plateaus, and "
            "finite-sample point estimates fluctuate. Median evidence strengthens "
            "as the bootstrap disk contracts."
        ),
        "pass": bool(
            all(row["summary"]["median_selected_rank"] == 4.0 for row in summaries)
            and summaries[-1]["summary"][
                "median_numerical_classical_state_lower_bound"
            ]
            >= summaries[0]["summary"][
                "median_numerical_classical_state_lower_bound"
            ]
        ),
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
