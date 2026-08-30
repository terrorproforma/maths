"""Surface-flux integration helpers."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

ArrayLike = npt.ArrayLike


def shell_integral(
    radial_flux_density: ArrayLike,
    proper_area_weights: ArrayLike,
    *,
    mask: ArrayLike | None = None,
) -> float:
    """Integrate a radial flux density over an extraction surface.

    ``proper_area_weights`` must already include the coordinate quadrature and
    induced proper-area measure. This explicit interface prevents accidental use
    of ``r**2 sin(theta)`` when a curved or non-spherical surface is intended.
    """

    flux = np.asarray(radial_flux_density, dtype=np.float64)
    weights = np.asarray(proper_area_weights, dtype=np.float64)
    if flux.shape != weights.shape:
        raise ValueError(f"Flux and weights must have equal shape: {flux.shape} != {weights.shape}")
    if np.any(~np.isfinite(flux)) or np.any(~np.isfinite(weights)):
        raise ValueError("Flux and weights must be finite")
    if np.any(weights < 0):
        raise ValueError("Proper-area weights must be non-negative")

    if mask is not None:
        selected = np.asarray(mask, dtype=bool)
        if selected.shape != flux.shape:
            raise ValueError("Mask must have the same shape as the flux")
        flux = np.where(selected, flux, 0.0)
        weights = np.where(selected, weights, 0.0)
    return float(np.sum(flux * weights, dtype=np.float64))


def outward_only(flux: ArrayLike) -> npt.NDArray[np.float64]:
    """Return a copy with inward flux set to zero."""

    values = np.asarray(flux, dtype=np.float64)
    if np.any(~np.isfinite(values)):
        raise ValueError("Flux values must be finite")
    return np.maximum(values, 0.0)


def hemispheric_integrals(
    radial_flux_density: ArrayLike,
    proper_area_weights: ArrayLike,
    polar_angle_rad: ArrayLike,
) -> tuple[float, float]:
    """Return north and south surface integrals using ``theta = pi/2`` as equator."""

    flux = np.asarray(radial_flux_density, dtype=np.float64)
    weights = np.asarray(proper_area_weights, dtype=np.float64)
    theta = np.asarray(polar_angle_rad, dtype=np.float64)
    if theta.shape != flux.shape:
        theta = np.broadcast_to(theta, flux.shape)
    north = shell_integral(flux, weights, mask=theta < np.pi / 2.0)
    south = shell_integral(flux, weights, mask=theta > np.pi / 2.0)
    return north, south
