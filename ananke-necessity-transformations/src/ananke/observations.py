"""Finite-shot observations for sequential scalar processes.

The exact behavioural oracle of ANANKE v0 is replaced by independent binomial
experiments. Repeated occurrences of the same operation word in a Hankel block
reuse the same empirical estimate, preserving the identity H[u,v] = f(uv).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import Iterable, Mapping, Sequence

import numpy as np

from .hankel import HankelData
from .process import LinearProcess
from .words import validate_word, words_upto


@dataclass(frozen=True)
class ShotDataset:
    """Binomial observations indexed by operation words."""

    alphabet: tuple[str, ...]
    successes: Mapping[str, int]
    trials: Mapping[str, int]

    def __post_init__(self) -> None:
        alphabet = tuple(self.alphabet)
        if not alphabet:
            raise ValueError("alphabet must not be empty")
        if len(set(alphabet)) != len(alphabet):
            raise ValueError("alphabet symbols must be unique")
        if any(len(symbol) != 1 for symbol in alphabet):
            raise ValueError("the current word encoding requires one-character symbols")

        successes = {str(word): int(value) for word, value in self.successes.items()}
        trials = {str(word): int(value) for word, value in self.trials.items()}
        if set(successes) != set(trials):
            raise ValueError("successes and trials must have identical word keys")
        if not successes:
            raise ValueError("the dataset must contain at least one measured word")

        for word, success_count in successes.items():
            validate_word(word, alphabet)
            trial_count = trials[word]
            if trial_count <= 0:
                raise ValueError(f"trials for word {word!r} must be positive")
            if success_count < 0 or success_count > trial_count:
                raise ValueError(f"successes for word {word!r} must lie in [0,trials]")

        object.__setattr__(self, "alphabet", alphabet)
        object.__setattr__(self, "successes", successes)
        object.__setattr__(self, "trials", trials)

    @property
    def words(self) -> tuple[str, ...]:
        return tuple(sorted(self.successes, key=lambda word: (len(word), word)))

    @property
    def total_trials(self) -> int:
        return int(sum(self.trials.values()))

    def require_words(self, required_words: Iterable[str]) -> None:
        missing = sorted(
            set(required_words) - set(self.successes),
            key=lambda word: (len(word), word),
        )
        if missing:
            preview = missing[:12]
            suffix = "" if len(missing) <= 12 else f" … and {len(missing)-12} more"
            raise KeyError(f"dataset is missing required words: {preview}{suffix}")

    def empirical_rate(self, word: str) -> float:
        if word not in self.successes:
            raise KeyError(f"word {word!r} is absent")
        return float(self.successes[word] / self.trials[word])

    def posterior_mean(
        self,
        word: str,
        *,
        prior_success: float = 0.5,
        prior_failure: float = 0.5,
    ) -> float:
        """Beta-binomial posterior mean; defaults to Jeffreys smoothing."""

        if prior_success <= 0.0 or prior_failure <= 0.0:
            raise ValueError("beta prior parameters must be positive")
        if word not in self.successes:
            raise KeyError(f"word {word!r} is absent")
        return float(
            (self.successes[word] + prior_success)
            / (self.trials[word] + prior_success + prior_failure)
        )

    def parametric_resample(
        self,
        rng: np.random.Generator,
        *,
        prior_success: float = 0.5,
        prior_failure: float = 0.5,
    ) -> "ShotDataset":
        """Plug-in parametric bootstrap at the original word shot counts."""

        if not isinstance(rng, np.random.Generator):
            raise TypeError("rng must be numpy.random.Generator")
        successes = {
            word: int(
                rng.binomial(
                    self.trials[word],
                    self.posterior_mean(
                        word,
                        prior_success=prior_success,
                        prior_failure=prior_failure,
                    ),
                )
            )
            for word in self.words
        }
        return ShotDataset(self.alphabet, successes, dict(self.trials))

    def to_dict(self, *, include_counts: bool = False) -> dict[str, object]:
        result: dict[str, object] = {
            "alphabet": list(self.alphabet),
            "word_count": len(self.successes),
            "total_trials": self.total_trials,
            "minimum_trials_per_word": min(self.trials.values()),
            "maximum_trials_per_word": max(self.trials.values()),
        }
        if include_counts:
            result["successes"] = dict(self.successes)
            result["trials"] = dict(self.trials)
        return result


def simulate_shot_dataset(
    process: LinearProcess,
    words: Sequence[str],
    shots_per_word: int | Mapping[str, int],
    rng: np.random.Generator,
) -> ShotDataset:
    """Simulate independent binomial observations of selected words."""

    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng must be numpy.random.Generator")
    ordered_words = tuple(dict.fromkeys(str(word) for word in words))
    if not ordered_words:
        raise ValueError("at least one word is required")

    if isinstance(shots_per_word, Mapping):
        requested = {str(word): int(count) for word, count in shots_per_word.items()}
        missing = set(ordered_words) - set(requested)
        if missing:
            raise ValueError(f"shots mapping misses words: {sorted(missing)}")
        trials = {word: requested[word] for word in ordered_words}
    else:
        count = int(shots_per_word)
        trials = {word: count for word in ordered_words}

    successes: dict[str, int] = {}
    for word in ordered_words:
        validate_word(word, process.alphabet)
        if trials[word] <= 0:
            raise ValueError(f"shots for word {word!r} must be positive")
        probability = process.behavior(word)
        if probability < -1e-12 or probability > 1.0 + 1e-12:
            raise ValueError(
                f"process behaviour for word {word!r} is {probability}, not a probability"
            )
        probability = float(np.clip(probability, 0.0, 1.0))
        successes[word] = int(rng.binomial(trials[word], probability))

    return ShotDataset(process.alphabet, successes, trials)


def simulate_words_upto(
    process: LinearProcess,
    max_length: int,
    shots_per_word: int | Mapping[str, int],
    rng: np.random.Generator,
) -> ShotDataset:
    return simulate_shot_dataset(
        process,
        words_upto(process.alphabet, max_length),
        shots_per_word,
        rng,
    )


def build_empirical_hankel(
    dataset: ShotDataset,
    max_prefix_length: int,
    max_suffix_length: int,
    *,
    prior_success: float = 0.5,
    prior_failure: float = 0.5,
) -> HankelData:
    """Build H[u,v] and shifted blocks from one estimate per unique word."""

    if max_prefix_length < 0 or max_suffix_length < 0:
        raise ValueError("prefix and suffix lengths must be non-negative")
    prefixes = tuple(words_upto(dataset.alphabet, max_prefix_length))
    suffixes = tuple(words_upto(dataset.alphabet, max_suffix_length))
    required = {prefix + suffix for prefix in prefixes for suffix in suffixes}
    required.update(
        prefix + symbol + suffix
        for symbol in dataset.alphabet
        for prefix in prefixes
        for suffix in suffixes
    )
    dataset.require_words(required)

    def estimate(word: str) -> float:
        return dataset.posterior_mean(
            word,
            prior_success=prior_success,
            prior_failure=prior_failure,
        )

    matrix = np.array(
        [[estimate(prefix + suffix) for suffix in suffixes] for prefix in prefixes],
        dtype=float,
    )
    shifts = {
        symbol: np.array(
            [
                [estimate(prefix + symbol + suffix) for suffix in suffixes]
                for prefix in prefixes
            ],
            dtype=float,
        )
        for symbol in dataset.alphabet
    }
    return HankelData(dataset.alphabet, prefixes, suffixes, matrix, shifts)


def binomial_cross_entropy(
    predicted_probability: float,
    successes: int,
    trials: int,
    *,
    clipping: float = 1e-9,
) -> float:
    """Average negative binomial log likelihood per trial, omitting constants."""

    if trials <= 0 or successes < 0 or successes > trials:
        raise ValueError("invalid binomial counts")
    if clipping <= 0.0 or clipping >= 0.5:
        raise ValueError("clipping must lie in (0,0.5)")
    probability = float(np.clip(predicted_probability, clipping, 1.0 - clipping))
    failures = trials - successes
    return float(
        -(successes * log(probability) + failures * log(1.0 - probability))
        / trials
    )


@dataclass(frozen=True)
class PredictiveScore:
    mean_cross_entropy: float
    standard_error_across_words: float
    mean_brier_score: float
    minimum_raw_prediction: float
    maximum_raw_prediction: float
    probability_violation_count: int
    words: tuple[str, ...]
    per_word_cross_entropy: tuple[float, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "mean_cross_entropy": self.mean_cross_entropy,
            "standard_error_across_words": self.standard_error_across_words,
            "mean_brier_score": self.mean_brier_score,
            "minimum_raw_prediction": self.minimum_raw_prediction,
            "maximum_raw_prediction": self.maximum_raw_prediction,
            "probability_violation_count": self.probability_violation_count,
            "word_count": len(self.words),
        }


def score_process_on_dataset(
    process: LinearProcess,
    dataset: ShotDataset,
    words: Sequence[str],
    *,
    clipping: float = 1e-9,
) -> PredictiveScore:
    """Score sequence predictions on finite held-out data."""

    ordered_words = tuple(dict.fromkeys(str(word) for word in words))
    if not ordered_words:
        raise ValueError("at least one validation word is required")
    dataset.require_words(ordered_words)

    losses: list[float] = []
    brier: list[float] = []
    raw_predictions: list[float] = []
    violations = 0
    for word in ordered_words:
        raw = float(process.behavior(word))
        raw_predictions.append(raw)
        if raw < 0.0 or raw > 1.0:
            violations += 1
        probability = float(np.clip(raw, clipping, 1.0 - clipping))
        successes = dataset.successes[word]
        trials = dataset.trials[word]
        losses.append(
            binomial_cross_entropy(probability, successes, trials, clipping=clipping)
        )
        brier.append(float((probability - successes / trials) ** 2))

    loss_array = np.asarray(losses, dtype=float)
    standard_error = (
        float(np.std(loss_array, ddof=1) / np.sqrt(loss_array.size))
        if loss_array.size > 1
        else 0.0
    )
    return PredictiveScore(
        mean_cross_entropy=float(np.mean(loss_array)),
        standard_error_across_words=standard_error,
        mean_brier_score=float(np.mean(brier)),
        minimum_raw_prediction=float(min(raw_predictions)),
        maximum_raw_prediction=float(max(raw_predictions)),
        probability_violation_count=violations,
        words=ordered_words,
        per_word_cross_entropy=tuple(float(value) for value in losses),
    )
