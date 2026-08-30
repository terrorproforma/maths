"""Validation-target loading and deterministic metric comparison."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .errors import ConfigurationError, ValidationFailure
from .io import load_document
from .schema import project_schema, validate_against_schema


@dataclass(frozen=True)
class MetricResult:
    metric_id: str
    passed: bool
    blocking: bool
    observed: Any
    target: Any
    method: str
    detail: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_targets(path: str | Path) -> dict[str, Any]:
    """Load and validate a target-metrics document."""

    targets = load_document(path)
    validate_against_schema(
        targets,
        project_schema("targets.schema.json"),
        document_name=f"validation targets {Path(path)}",
    )
    identifiers = [metric["id"] for metric in targets["metrics"]]
    if len(identifiers) != len(set(identifiers)):
        raise ConfigurationError("Validation metric identifiers must be unique")
    return targets


def _as_finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigurationError(f"{label} must be numeric, got {value!r}")
    number = float(value)
    if not math.isfinite(number):
        raise ConfigurationError(f"{label} must be finite, got {number}")
    return number


def compare_metric(metric: dict[str, Any], observed: Any) -> MetricResult:
    """Compare one observed value against one target declaration."""

    comparison = metric["comparison"]
    method = str(comparison["method"])
    target = metric.get("target")
    passed = False
    detail = ""

    if method == "exact":
        tolerance = float(comparison.get("absolute_tolerance", 0.0))
        observed_number = _as_finite_number(observed, metric["id"])
        target_number = _as_finite_number(target, f"{metric['id']} target")
        error = abs(observed_number - target_number)
        passed = error <= tolerance
        detail = f"absolute error {error:.9g} <= {tolerance:.9g}"
    elif method == "absolute":
        tolerance = float(comparison["absolute_tolerance"])
        observed_number = _as_finite_number(observed, metric["id"])
        target_number = _as_finite_number(target, f"{metric['id']} target")
        error = abs(observed_number - target_number)
        passed = error <= tolerance
        detail = f"absolute error {error:.9g} <= {tolerance:.9g}"
    elif method == "relative":
        tolerance = float(comparison["relative_tolerance"])
        observed_number = _as_finite_number(observed, metric["id"])
        target_number = _as_finite_number(target, f"{metric['id']} target")
        denominator = max(abs(target_number), 1.0e-300)
        error = abs(observed_number - target_number) / denominator
        passed = error <= tolerance
        detail = f"relative error {error:.9g} <= {tolerance:.9g}"
    elif method == "factor":
        factor = float(comparison["factor_tolerance"])
        observed_number = _as_finite_number(observed, metric["id"])
        target_number = _as_finite_number(target, f"{metric['id']} target")
        if observed_number <= 0 or target_number <= 0:
            raise ConfigurationError("Factor comparison requires positive values")
        ratio = max(observed_number / target_number, target_number / observed_number)
        passed = ratio <= factor
        detail = f"symmetric factor {ratio:.9g} <= {factor:.9g}"
    elif method == "lower_bound":
        tolerance = float(comparison.get("absolute_tolerance", 0.0))
        observed_number = _as_finite_number(observed, metric["id"])
        target_number = _as_finite_number(target, f"{metric['id']} target")
        passed = observed_number + tolerance >= target_number
        detail = f"{observed_number:.9g} + {tolerance:.9g} >= {target_number:.9g}"
    elif method == "upper_bound":
        tolerance = float(comparison.get("absolute_tolerance", 0.0))
        observed_number = _as_finite_number(observed, metric["id"])
        target_number = _as_finite_number(target, f"{metric['id']} target")
        passed = observed_number <= target_number + tolerance
        detail = f"{observed_number:.9g} <= {target_number:.9g} + {tolerance:.9g}"
    elif method == "interval_overlap":
        if not (
            isinstance(target, list)
            and len(target) == 2
            and isinstance(observed, (list, tuple))
            and len(observed) == 2
        ):
            raise ConfigurationError("Interval comparison requires two-element target and observation")
        target_low, target_high = map(float, target)
        observed_low, observed_high = map(float, observed)
        if target_low > target_high or observed_low > observed_high:
            raise ConfigurationError("Intervals must be ordered low to high")
        overlap = min(target_high, observed_high) - max(target_low, observed_low)
        passed = overlap >= 0
        detail = f"interval overlap width {max(overlap, 0.0):.9g}"
    else:
        raise ConfigurationError(f"Unsupported comparison method: {method}")

    return MetricResult(
        metric_id=str(metric["id"]),
        passed=passed,
        blocking=bool(metric["blocking"]),
        observed=observed,
        target=target,
        method=method,
        detail=detail,
    )


def validate_observations(
    targets: dict[str, Any],
    observations: dict[str, Any],
    *,
    fail_on_missing: bool = True,
) -> list[MetricResult]:
    """Validate observed metrics and raise if a blocking target fails."""

    results: list[MetricResult] = []
    for metric in targets["metrics"]:
        identifier = str(metric["id"])
        if identifier not in observations:
            result = MetricResult(
                metric_id=identifier,
                passed=not fail_on_missing,
                blocking=bool(metric["blocking"]),
                observed=None,
                target=metric.get("target"),
                method=str(metric["comparison"]["method"]),
                detail="observation is missing",
            )
        else:
            result = compare_metric(metric, observations[identifier])
        results.append(result)

    failed = [result.metric_id for result in results if result.blocking and not result.passed]
    if failed:
        raise ValidationFailure(f"Blocking validation metrics failed: {', '.join(failed)}")
    return results
