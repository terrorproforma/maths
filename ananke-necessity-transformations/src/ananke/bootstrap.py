"""Bootstrap uncertainty for finite-data ANANKE invariants."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .hankel import extract_minimal_process
from .observations import ShotDataset, build_empirical_hankel


def _complex_pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def select_transition_eigenvalue(
    matrix: np.ndarray,
    *,
    target: complex | None = None,
    positive_imaginary: bool = True,
    imaginary_tolerance: float = 1e-9,
) -> complex:
    """Select a non-real eigenmode, or match the eigenvalue nearest ``target``."""

    values = np.linalg.eigvals(np.asarray(matrix, dtype=float)).astype(complex)
    if values.size == 0:
        raise ValueError("matrix has no eigenvalues")
    if target is not None:
        target_value = complex(target)
        return complex(min(values, key=lambda value: abs(value - target_value)))
    candidates = (
        [value for value in values if value.imag > imaginary_tolerance]
        if positive_imaginary
        else [value for value in values if abs(value.imag) > imaginary_tolerance]
    )
    if not candidates:
        raise ValueError("transition has no selectable non-real eigenmode")
    return complex(max(candidates, key=lambda value: (abs(value.imag), abs(value))))


@dataclass(frozen=True)
class EigenmodeBootstrapResult:
    symbol: str
    retained_rank: int
    point_estimate: complex
    target_used_for_matching: complex
    confidence_level: float
    confidence_disk_radius: float
    modulus_interval: tuple[float, float]
    phase_interval_radians: tuple[float, float]
    repetitions: int
    successful_repetitions: int
    failures: int
    samples: tuple[complex, ...]

    def to_dict(self, *, include_samples: bool = False) -> dict[str, object]:
        result: dict[str, object] = {
            "symbol": self.symbol,
            "retained_rank": self.retained_rank,
            "point_estimate": _complex_pair(self.point_estimate),
            "point_modulus": float(abs(self.point_estimate)),
            "point_phase_radians": float(np.angle(self.point_estimate)),
            "target_used_for_matching": _complex_pair(self.target_used_for_matching),
            "confidence_level": self.confidence_level,
            "confidence_disk_radius": self.confidence_disk_radius,
            "modulus_interval": list(self.modulus_interval),
            "phase_interval_radians": list(self.phase_interval_radians),
            "repetitions": self.repetitions,
            "successful_repetitions": self.successful_repetitions,
            "failures": self.failures,
            "method": (
                "Plug-in parametric bootstrap over binomial word counts; fixed "
                "rank; nearest-eigenvalue matching; centered complex disk."
            ),
        }
        if include_samples:
            result["samples"] = [_complex_pair(value) for value in self.samples]
        return result


def bootstrap_transition_eigenmode(
    dataset: ShotDataset,
    *,
    max_prefix_length: int,
    max_suffix_length: int,
    retained_rank: int,
    symbol: str,
    repetitions: int,
    confidence_level: float,
    rng: np.random.Generator,
    target: complex | None = None,
) -> EigenmodeBootstrapResult:
    """Bootstrap one similarity-invariant transition eigenvalue at fixed rank."""

    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must lie in (0,1)")
    if symbol not in dataset.alphabet:
        raise ValueError(f"unknown symbol {symbol!r}")

    point_hankel = build_empirical_hankel(
        dataset,
        max_prefix_length=max_prefix_length,
        max_suffix_length=max_suffix_length,
    )
    point_extraction = extract_minimal_process(point_hankel, rank=retained_rank)
    point = select_transition_eigenvalue(
        point_extraction.process.transitions[symbol],
        target=target,
    )
    matching_target = point if target is None else complex(target)

    samples: list[complex] = []
    failures = 0
    for _ in range(repetitions):
        try:
            resampled = dataset.parametric_resample(rng)
            hankel = build_empirical_hankel(
                resampled,
                max_prefix_length=max_prefix_length,
                max_suffix_length=max_suffix_length,
            )
            extraction = extract_minimal_process(hankel, rank=retained_rank)
            value = select_transition_eigenvalue(
                extraction.process.transitions[symbol],
                target=point,
            )
            if not np.isfinite(value.real) or not np.isfinite(value.imag):
                raise FloatingPointError("non-finite eigenvalue")
        except (ValueError, np.linalg.LinAlgError, FloatingPointError):
            failures += 1
            continue
        samples.append(value)

    minimum_successes = max(20, int(np.ceil(repetitions / 2)))
    if len(samples) < minimum_successes:
        raise RuntimeError(
            f"only {len(samples)} of {repetitions} bootstrap replicates succeeded"
        )

    array = np.asarray(samples, dtype=complex)
    disk_radius = float(np.quantile(np.abs(array - point), confidence_level))
    alpha = 1.0 - confidence_level
    lower = alpha / 2.0
    upper = 1.0 - lower
    modulus_interval = (
        float(np.quantile(np.abs(array), lower)),
        float(np.quantile(np.abs(array), upper)),
    )
    point_phase = float(np.angle(point))
    unwrapped = point_phase + np.angle(array / point)
    phase_interval = (
        float(np.quantile(unwrapped, lower)),
        float(np.quantile(unwrapped, upper)),
    )
    return EigenmodeBootstrapResult(
        symbol=symbol,
        retained_rank=retained_rank,
        point_estimate=point,
        target_used_for_matching=matching_target,
        confidence_level=confidence_level,
        confidence_disk_radius=disk_radius,
        modulus_interval=modulus_interval,
        phase_interval_radians=phase_interval,
        repetitions=repetitions,
        successful_repetitions=len(samples),
        failures=failures,
        samples=tuple(samples),
    )


@dataclass(frozen=True)
class SingularValueBootstrapResult:
    point_estimates: tuple[float, ...]
    intervals: tuple[tuple[float, float], ...]
    confidence_level: float
    repetitions: int
    successful_repetitions: int
    failures: int

    def to_dict(self) -> dict[str, object]:
        return {
            "point_estimates": list(self.point_estimates),
            "intervals": [list(interval) for interval in self.intervals],
            "confidence_level": self.confidence_level,
            "repetitions": self.repetitions,
            "successful_repetitions": self.successful_repetitions,
            "failures": self.failures,
        }


def bootstrap_hankel_singular_values(
    dataset: ShotDataset,
    *,
    max_prefix_length: int,
    max_suffix_length: int,
    number_of_values: int,
    repetitions: int,
    confidence_level: float,
    rng: np.random.Generator,
) -> SingularValueBootstrapResult:
    """Bootstrap leading empirical Hankel singular values."""

    if number_of_values <= 0 or repetitions <= 0:
        raise ValueError("number_of_values and repetitions must be positive")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must lie in (0,1)")
    point_hankel = build_empirical_hankel(
        dataset,
        max_prefix_length=max_prefix_length,
        max_suffix_length=max_suffix_length,
    )
    point = np.linalg.svd(point_hankel.matrix, compute_uv=False)
    count = min(number_of_values, point.size)
    samples: list[np.ndarray] = []
    failures = 0
    for _ in range(repetitions):
        try:
            hankel = build_empirical_hankel(
                dataset.parametric_resample(rng),
                max_prefix_length=max_prefix_length,
                max_suffix_length=max_suffix_length,
            )
            values = np.linalg.svd(hankel.matrix, compute_uv=False)[:count]
            if not np.all(np.isfinite(values)):
                raise FloatingPointError("non-finite singular values")
        except (ValueError, np.linalg.LinAlgError, FloatingPointError):
            failures += 1
            continue
        samples.append(values)
    if not samples:
        raise RuntimeError("all singular-value bootstrap replicates failed")
    matrix = np.vstack(samples)
    alpha = 1.0 - confidence_level
    intervals = tuple(
        (
            float(np.quantile(matrix[:, index], alpha / 2.0)),
            float(np.quantile(matrix[:, index], 1.0 - alpha / 2.0)),
        )
        for index in range(count)
    )
    return SingularValueBootstrapResult(
        point_estimates=tuple(float(value) for value in point[:count]),
        intervals=intervals,
        confidence_level=confidence_level,
        repetitions=repetitions,
        successful_repetitions=len(samples),
        failures=failures,
    )
