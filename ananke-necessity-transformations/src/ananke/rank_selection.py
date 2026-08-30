"""Held-out statistical rank selection for finite behavioural Hankel data."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .hankel import SpectralExtraction, extract_minimal_process
from .observations import (
    PredictiveScore,
    ShotDataset,
    build_empirical_hankel,
    score_process_on_dataset,
)


@dataclass(frozen=True)
class RankCandidate:
    rank: int
    extraction: SpectralExtraction
    score: PredictiveScore
    paired_mean_excess_loss: float
    paired_standard_error: float
    within_one_standard_error: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "rank": self.rank,
            "score": self.score.to_dict(),
            "paired_mean_excess_loss": self.paired_mean_excess_loss,
            "paired_standard_error": self.paired_standard_error,
            "within_one_standard_error": self.within_one_standard_error,
            "factorization_error": self.extraction.factorization_error,
            "shifted_factorization_errors": dict(
                self.extraction.shifted_factorization_errors
            ),
        }


@dataclass(frozen=True)
class RankSelectionResult:
    selected_rank: int
    best_predictive_rank: int
    one_standard_error_threshold: float
    candidates: tuple[RankCandidate, ...]
    singular_values: tuple[float, ...]

    @property
    def selected_extraction(self) -> SpectralExtraction:
        for candidate in self.candidates:
            if candidate.rank == self.selected_rank:
                return candidate.extraction
        raise RuntimeError("selected rank is absent from candidates")

    def to_dict(self) -> dict[str, object]:
        return {
            "selected_rank": self.selected_rank,
            "best_predictive_rank": self.best_predictive_rank,
            "one_standard_error_threshold": self.one_standard_error_threshold,
            "singular_values": list(self.singular_values),
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "selection_rule": (
                "Smallest candidate whose mean held-out cross entropy is no more "
                "than one across-word standard error above the predictive winner."
            ),
        }


def select_hankel_rank(
    dataset: ShotDataset,
    *,
    max_prefix_length: int,
    max_suffix_length: int,
    validation_words: Sequence[str],
    candidate_ranks: Sequence[int],
    clipping: float = 1e-9,
) -> RankSelectionResult:
    """Fit each rank to the empirical Hankel block and score longer words."""

    ranks = tuple(sorted(set(int(rank) for rank in candidate_ranks)))
    if not ranks or ranks[0] <= 0:
        raise ValueError("candidate_ranks must contain positive integers")
    hankel = build_empirical_hankel(
        dataset,
        max_prefix_length=max_prefix_length,
        max_suffix_length=max_suffix_length,
    )
    maximum_rank = min(hankel.matrix.shape)
    if ranks[-1] > maximum_rank:
        raise ValueError(
            f"candidate rank {ranks[-1]} exceeds Hankel block maximum {maximum_rank}"
        )

    preliminary: list[tuple[int, SpectralExtraction, PredictiveScore]] = []
    for rank in ranks:
        extraction = extract_minimal_process(hankel, rank=rank)
        score = score_process_on_dataset(
            extraction.process,
            dataset,
            validation_words,
            clipping=clipping,
        )
        preliminary.append((rank, extraction, score))

    best_rank, _, best_score = min(
        preliminary,
        key=lambda item: (item[2].mean_cross_entropy, item[0]),
    )
    threshold = (
        best_score.mean_cross_entropy + best_score.standard_error_across_words
    )
    best_losses = np.asarray(best_score.per_word_cross_entropy, dtype=float)

    candidates: list[RankCandidate] = []
    for rank, extraction, score in preliminary:
        differences = np.asarray(score.per_word_cross_entropy) - best_losses
        paired_mean = float(np.mean(differences))
        paired_se = (
            float(np.std(differences, ddof=1) / np.sqrt(differences.size))
            if differences.size > 1
            else 0.0
        )
        candidates.append(
            RankCandidate(
                rank=rank,
                extraction=extraction,
                score=score,
                paired_mean_excess_loss=paired_mean,
                paired_standard_error=paired_se,
                within_one_standard_error=bool(
                    score.mean_cross_entropy <= threshold + 1e-15
                ),
            )
        )

    selected_rank = min(
        candidate.rank
        for candidate in candidates
        if candidate.within_one_standard_error
    )
    return RankSelectionResult(
        selected_rank=selected_rank,
        best_predictive_rank=best_rank,
        one_standard_error_threshold=float(threshold),
        candidates=tuple(candidates),
        singular_values=tuple(
            float(value) for value in np.linalg.svd(hankel.matrix, compute_uv=False)
        ),
    )


@dataclass(frozen=True)
class RankStabilityResult:
    repetitions: int
    successful_repetitions: int
    failures: int
    frequencies: dict[int, int]
    probabilities: dict[int, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "repetitions": self.repetitions,
            "successful_repetitions": self.successful_repetitions,
            "failures": self.failures,
            "frequencies": {str(rank): count for rank, count in self.frequencies.items()},
            "probabilities": {
                str(rank): probability for rank, probability in self.probabilities.items()
            },
        }


def bootstrap_rank_stability(
    dataset: ShotDataset,
    *,
    max_prefix_length: int,
    max_suffix_length: int,
    validation_words: Sequence[str],
    candidate_ranks: Sequence[int],
    repetitions: int,
    rng: np.random.Generator,
) -> RankStabilityResult:
    """Bootstrap the complete rank-selection procedure."""

    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    counts: Counter[int] = Counter()
    failures = 0
    for _ in range(repetitions):
        try:
            result = select_hankel_rank(
                dataset.parametric_resample(rng),
                max_prefix_length=max_prefix_length,
                max_suffix_length=max_suffix_length,
                validation_words=validation_words,
                candidate_ranks=candidate_ranks,
            )
        except (ValueError, np.linalg.LinAlgError, FloatingPointError):
            failures += 1
            continue
        counts[result.selected_rank] += 1

    successful = repetitions - failures
    probabilities = (
        {rank: count / successful for rank, count in sorted(counts.items())}
        if successful
        else {}
    )
    return RankStabilityResult(
        repetitions=repetitions,
        successful_repetitions=successful,
        failures=failures,
        frequencies=dict(sorted(counts.items())),
        probabilities=probabilities,
    )
