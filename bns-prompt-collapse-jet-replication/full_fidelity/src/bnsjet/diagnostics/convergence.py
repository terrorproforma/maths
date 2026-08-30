"""Grid-convergence utilities."""

from __future__ import annotations

import math


def observed_order_equal_ratio(
    coarse: float,
    medium: float,
    fine: float,
    refinement_ratio: float,
) -> float:
    """Estimate observed order for three equally ratioed resolutions.

    The estimate is meaningful only in an asymptotic regime. A sign change or
    vanishing difference is rejected rather than converted into a spurious order.
    """

    ratio = float(refinement_ratio)
    if not math.isfinite(ratio) or ratio <= 1:
        raise ValueError("refinement_ratio must be finite and greater than one")
    numerator = float(coarse) - float(medium)
    denominator = float(medium) - float(fine)
    if denominator == 0 or numerator == 0 or numerator / denominator <= 0:
        raise ValueError("Differences must be non-zero and have the same sign")
    return math.log(abs(numerator / denominator)) / math.log(ratio)


def richardson_extrapolate(
    medium: float,
    fine: float,
    refinement_ratio: float,
    observed_order: float,
) -> float:
    """Return the zero-spacing Richardson extrapolation from medium and fine values."""

    ratio = float(refinement_ratio)
    order = float(observed_order)
    denominator = ratio**order - 1.0
    if not math.isfinite(denominator) or abs(denominator) < 1.0e-15:
        raise ValueError("Invalid refinement ratio/order for Richardson extrapolation")
    return float(fine) + (float(fine) - float(medium)) / denominator


def grid_convergence_index(
    medium: float,
    fine: float,
    refinement_ratio: float,
    observed_order: float,
    *,
    safety_factor: float = 1.25,
) -> float:
    """Return a relative Grid Convergence Index for the fine solution."""

    fine_value = float(fine)
    if fine_value == 0:
        raise ValueError("Fine solution must be non-zero for relative GCI")
    denominator = float(refinement_ratio) ** float(observed_order) - 1.0
    if denominator <= 0:
        raise ValueError("Invalid denominator for GCI")
    return safety_factor * abs((fine_value - float(medium)) / fine_value) / denominator
