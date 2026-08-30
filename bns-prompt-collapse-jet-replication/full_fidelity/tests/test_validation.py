from __future__ import annotations

import pytest

from bnsjet.errors import ValidationFailure
from bnsjet.validation import compare_metric, validate_observations


def metric(method: str, target: object, **comparison: float) -> dict[str, object]:
    return {
        "id": "example",
        "kind": "scalar",
        "blocking": True,
        "source": "test",
        "target": target,
        "comparison": {"method": method, **comparison},
    }


def test_absolute_comparison() -> None:
    result = compare_metric(metric("absolute", 10.0, absolute_tolerance=1.0), 10.5)
    assert result.passed


def test_interval_overlap() -> None:
    result = compare_metric(metric("interval_overlap", [1.0, 3.0]), [2.5, 4.0])
    assert result.passed


def test_blocking_failure_raises() -> None:
    targets = {"metrics": [metric("exact", 2.0, absolute_tolerance=0.0)]}
    with pytest.raises(ValidationFailure):
        validate_observations(targets, {"example": 3.0})
