"""ANANKE v0: extract the same core from three equivalent descriptions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from ananke import (
    build_hankel,
    extract_minimal_process,
    process_fingerprint,
    qubit_rotation_process,
    words_upto,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "qubit_v0.json"


def _random_invertible_matrix(
    rng: np.random.Generator,
    dimension: int,
    maximum_condition_number: float = 20.0,
) -> np.ndarray:
    for _ in range(10_000):
        candidate = rng.normal(size=(dimension, dimension))
        condition = np.linalg.cond(candidate)
        if np.isfinite(condition) and condition <= maximum_condition_number:
            return candidate
    raise RuntimeError("could not generate a suitably conditioned invertible matrix")


def _maximum_behaviour_difference(processes: list[Any], max_length: int) -> float:
    words = words_upto(processes[0].alphabet, max_length)
    baseline = np.array([processes[0].behavior(word) for word in words])
    differences = []
    for process in processes[1:]:
        values = np.array([process.behavior(word) for word in words])
        differences.append(float(np.max(np.abs(values - baseline))))
    return max(differences, default=0.0)


def _held_out_error(reference: Any, candidate: Any, max_length: int) -> float:
    return float(
        max(
            abs(reference.behavior(word) - candidate.behavior(word))
            for word in words_upto(reference.alphabet, max_length)
        )
    )


def _similarity_residual(
    reference: Any,
    extraction: Any,
    prefixes: tuple[str, ...],
) -> dict[str, float]:
    reference_prefix_coordinates = np.vstack(
        [reference.row_after(prefix) for prefix in prefixes]
    )
    coordinate_map, *_ = np.linalg.lstsq(
        reference_prefix_coordinates,
        extraction.prefix_coordinates,
        rcond=None,
    )

    inverse_map = np.linalg.inv(coordinate_map)
    transition_residuals = {
        symbol: float(
            np.linalg.norm(
                extraction.process.transitions[symbol]
                - inverse_map
                @ reference.transitions[symbol]
                @ coordinate_map,
                ord="fro",
            )
        )
        for symbol in reference.alphabet
    }
    initial_residual = float(
        np.linalg.norm(
            extraction.process.initial - reference.initial @ coordinate_map
        )
    )
    final_residual = float(
        np.linalg.norm(
            extraction.process.final - inverse_map @ reference.final
        )
    )
    return {
        "coordinate_map_condition_number": float(np.linalg.cond(coordinate_map)),
        "initial_residual": initial_residual,
        "final_residual": final_residual,
        "maximum_transition_residual": max(transition_residuals.values()),
        "transition_residuals": transition_residuals,
    }


def main() -> None:
    rng = np.random.default_rng(7)

    physical = qubit_rotation_process()
    coordinate_map = _random_invertible_matrix(rng, physical.dimension)
    scrambled = physical.gauge_transform(coordinate_map)

    hidden_transitions = {
        symbol: rng.normal(scale=0.35, size=(3, 3))
        for symbol in physical.alphabet
    }
    padded = physical.pad_with_unreachable_hidden_dynamics(hidden_transitions)

    descriptions = {
        "physical_pauli": physical,
        "scrambled_gauge": scrambled,
        "padded_hidden": padded,
    }

    behaviour_difference = _maximum_behaviour_difference(
        list(descriptions.values()),
        max_length=8,
    )

    extractions: dict[str, Any] = {}
    summaries: dict[str, Any] = {}
    for name, description in descriptions.items():
        hankel = build_hankel(
            description.behavior,
            description.alphabet,
            max_prefix_length=2,
            max_suffix_length=2,
        )
        extraction = extract_minimal_process(hankel)
        extractions[name] = (hankel, extraction)
        summaries[name] = {
            "declared_internal_dimension": description.dimension,
            "hankel_singular_values": [
                float(value) for value in extraction.singular_values
            ],
            "extracted_rank": extraction.retained_rank,
            "rank_threshold": extraction.threshold,
            "hankel_factorization_error": extraction.factorization_error,
            "shifted_factorization_errors": dict(
                extraction.shifted_factorization_errors
            ),
            "held_out_maximum_error_through_length_8": _held_out_error(
                physical,
                extraction.process,
                max_length=8,
            ),
            "fingerprint": process_fingerprint(extraction.process),
        }

    physical_hankel, physical_extraction = extractions["physical_pauli"]
    similarity = _similarity_residual(
        physical,
        physical_extraction,
        physical_hankel.prefixes,
    )

    result = {
        "experiment": "ANANKE qubit v0",
        "claim_tested": (
            "Observationally equivalent coordinate systems and unreachable hidden "
            "dynamics reduce to one minimal predictive process up to similarity."
        ),
        "maximum_behaviour_difference_through_length_8": behaviour_difference,
        "descriptions": summaries,
        "recovered_similarity_to_physical_model": similarity,
        "pass": bool(
            behaviour_difference < 1e-12
            and all(
                summary["extracted_rank"] == 4
                and summary["held_out_maximum_error_through_length_8"] < 1e-10
                for summary in summaries.values()
            )
            and similarity["maximum_transition_residual"] < 1e-10
        ),
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
