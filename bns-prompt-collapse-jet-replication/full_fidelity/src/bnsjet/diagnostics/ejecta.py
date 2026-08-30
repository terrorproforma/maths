"""Unbound-ejecta criteria and weighted summaries."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

ArrayLike = npt.ArrayLike


def geodesic_unbound_mask(covariant_u_t: ArrayLike, *, outward_velocity: ArrayLike | None = None) -> npt.NDArray[np.bool_]:
    """Return the geodesic unbound mask ``u_t < -1``.

    An optional outward-velocity condition can be supplied to reject inward-moving
    material that is formally unbound at the extraction instant.
    """

    u_t = np.asarray(covariant_u_t, dtype=np.float64)
    if np.any(~np.isfinite(u_t)):
        raise ValueError("u_t must be finite")
    mask = u_t < -1.0
    if outward_velocity is not None:
        velocity = np.asarray(outward_velocity, dtype=np.float64)
        if velocity.shape != u_t.shape:
            velocity = np.broadcast_to(velocity, u_t.shape)
        mask &= velocity > 0.0
    return mask


def bernoulli_unbound_mask(
    covariant_u_t: ArrayLike,
    specific_enthalpy: ArrayLike,
    *,
    asymptotic_enthalpy: float = 1.0,
    outward_velocity: ArrayLike | None = None,
) -> npt.NDArray[np.bool_]:
    """Return a Bernoulli-type unbound mask ``h u_t < -h_infinity``."""

    u_t = np.asarray(covariant_u_t, dtype=np.float64)
    enthalpy = np.asarray(specific_enthalpy, dtype=np.float64)
    u_t, enthalpy = np.broadcast_arrays(u_t, enthalpy)
    if np.any(~np.isfinite(u_t)) or np.any(~np.isfinite(enthalpy)):
        raise ValueError("u_t and enthalpy must be finite")
    if np.any(enthalpy <= 0) or asymptotic_enthalpy <= 0:
        raise ValueError("Specific enthalpy must be positive")
    mask = enthalpy * u_t < -float(asymptotic_enthalpy)
    if outward_velocity is not None:
        velocity = np.broadcast_to(np.asarray(outward_velocity, dtype=np.float64), u_t.shape)
        mask &= velocity > 0.0
    return mask


def weighted_distribution(
    values: ArrayLike,
    weights: ArrayLike,
    bins: ArrayLike,
    *,
    mask: ArrayLike | None = None,
    normalise: bool = False,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Return a finite, non-negative weighted histogram."""

    samples = np.asarray(values, dtype=np.float64)
    sample_weights = np.asarray(weights, dtype=np.float64)
    samples, sample_weights = np.broadcast_arrays(samples, sample_weights)
    selected = np.ones(samples.shape, dtype=bool)
    if mask is not None:
        selected &= np.broadcast_to(np.asarray(mask, dtype=bool), samples.shape)
    selected &= np.isfinite(samples) & np.isfinite(sample_weights)
    if np.any(sample_weights[selected] < 0):
        raise ValueError("Distribution weights must be non-negative")
    histogram, edges = np.histogram(
        samples[selected],
        bins=np.asarray(bins, dtype=np.float64),
        weights=sample_weights[selected],
    )
    histogram = histogram.astype(np.float64)
    if normalise:
        total = float(histogram.sum())
        if total > 0:
            histogram /= total
    return histogram, edges
