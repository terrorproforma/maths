"""Jet launch, luminosity and opening-angle diagnostics."""

from __future__ import annotations

import math

import numpy as np
import numpy.typing as npt

ArrayLike = npt.ArrayLike


def sustained_crossing_time(
    time: ArrayLike,
    signal: ArrayLike,
    threshold: float,
    minimum_duration: float,
) -> float | None:
    """Return the first threshold crossing sustained for ``minimum_duration``.

    Samples need not be uniformly spaced, but time must be strictly increasing.
    The interval is considered sustained when every sample through the first sample
    at or beyond ``start + minimum_duration`` remains above threshold.
    """

    times = np.asarray(time, dtype=np.float64)
    values = np.asarray(signal, dtype=np.float64)
    if times.ndim != 1 or values.ndim != 1 or times.size != values.size:
        raise ValueError("time and signal must be equal-length one-dimensional arrays")
    if times.size == 0:
        return None
    if np.any(~np.isfinite(times)) or np.any(~np.isfinite(values)):
        raise ValueError("time and signal must be finite")
    if np.any(np.diff(times) <= 0):
        raise ValueError("time must be strictly increasing")
    if minimum_duration < 0:
        raise ValueError("minimum_duration must be non-negative")

    above = values >= threshold
    for start in np.flatnonzero(above):
        end_time = times[start] + minimum_duration
        end = int(np.searchsorted(times, end_time, side="left"))
        if end >= times.size:
            continue
        if bool(np.all(above[start : end + 1])):
            return float(times[start])
    return None


def luminosity_containing_angle(
    polar_angle_rad: ArrayLike,
    outward_luminosity_density: ArrayLike,
    proper_area_weights: ArrayLike,
    *,
    hemisphere: str,
    fraction: float = 0.9,
) -> float:
    """Return polar half-angle containing a fraction of outward luminosity.

    The angle is measured from the selected pole. Negative luminosity density is
    excluded, and all geometric factors must be supplied in proper-area weights.
    """

    theta = np.asarray(polar_angle_rad, dtype=np.float64)
    luminosity = np.asarray(outward_luminosity_density, dtype=np.float64)
    weights = np.asarray(proper_area_weights, dtype=np.float64)
    theta, luminosity, weights = np.broadcast_arrays(theta, luminosity, weights)
    if np.any(~np.isfinite(theta)) or np.any(~np.isfinite(luminosity)) or np.any(~np.isfinite(weights)):
        raise ValueError("Opening-angle inputs must be finite")
    if np.any(weights < 0):
        raise ValueError("Proper-area weights must be non-negative")
    if not 0 < fraction <= 1:
        raise ValueError("fraction must lie in (0, 1]")

    normalised_hemisphere = hemisphere.lower()
    if normalised_hemisphere == "north":
        selected = theta <= math.pi / 2.0
        angle_from_pole = theta
    elif normalised_hemisphere == "south":
        selected = theta >= math.pi / 2.0
        angle_from_pole = math.pi - theta
    else:
        raise ValueError("hemisphere must be 'north' or 'south'")

    contributions = np.maximum(luminosity[selected], 0.0) * weights[selected]
    angles = angle_from_pole[selected]
    total = float(contributions.sum())
    if total <= 0:
        raise ValueError("Selected hemisphere has no positive outward luminosity")

    order = np.argsort(angles, kind="stable")
    cumulative = np.cumsum(contributions[order], dtype=np.float64)
    index = int(np.searchsorted(cumulative, fraction * total, side="left"))
    index = min(index, order.size - 1)
    return float(angles[order[index]])


def hemispheric_asymmetry(north_luminosity: float, south_luminosity: float) -> float:
    """Return bounded signed asymmetry ``(N-S)/(N+S)``."""

    north = float(north_luminosity)
    south = float(south_luminosity)
    if not math.isfinite(north) or not math.isfinite(south) or north < 0 or south < 0:
        raise ValueError("Hemispheric luminosities must be finite and non-negative")
    total = north + south
    return 0.0 if total == 0 else (north - south) / total
