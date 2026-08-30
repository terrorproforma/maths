"""Quasi-local black-hole diagnostics in geometrised units G = c = 1."""

from __future__ import annotations

import math

import numpy as np
import numpy.typing as npt

ArrayLike = npt.ArrayLike


def irreducible_mass(area: ArrayLike) -> npt.NDArray[np.float64]:
    """Return irreducible mass ``sqrt(A / (16*pi))``.

    Parameters may be scalars or arrays. Non-positive and non-finite areas are
    rejected because silently propagating them would hide horizon-finder failure.
    """

    values = np.asarray(area, dtype=np.float64)
    if np.any(~np.isfinite(values)) or np.any(values <= 0):
        raise ValueError("Horizon area must be finite and strictly positive")
    return np.sqrt(values / (16.0 * math.pi))


def christodoulou_mass(area: ArrayLike, angular_momentum: ArrayLike) -> npt.NDArray[np.float64]:
    """Return Christodoulou mass from horizon area and angular momentum.

    ``M^2 = M_irr^2 + J^2 / (4 M_irr^2)``.
    """

    irreducible = irreducible_mass(area)
    momentum = np.asarray(angular_momentum, dtype=np.float64)
    if np.any(~np.isfinite(momentum)):
        raise ValueError("Angular momentum must be finite")
    return np.sqrt(irreducible**2 + momentum**2 / (4.0 * irreducible**2))


def dimensionless_spin(area: ArrayLike, angular_momentum: ArrayLike) -> npt.NDArray[np.float64]:
    """Return signed dimensionless spin ``chi = J / M^2``."""

    mass = christodoulou_mass(area, angular_momentum)
    momentum = np.asarray(angular_momentum, dtype=np.float64)
    spin = momentum / mass**2
    if np.any(np.abs(spin) > 1.0 + 1.0e-8):
        raise ValueError("Computed horizon spin violates the Kerr bound")
    return spin


def horizon_angular_frequency(
    area: ArrayLike,
    angular_momentum: ArrayLike,
) -> npt.NDArray[np.float64]:
    """Return Kerr-equivalent horizon angular frequency.

    In geometrised units ``Omega_H = chi / (2 M (1 + sqrt(1-chi^2)))``.
    """

    mass = christodoulou_mass(area, angular_momentum)
    spin = dimensionless_spin(area, angular_momentum)
    radical = np.sqrt(np.maximum(0.0, 1.0 - spin**2))
    return spin / (2.0 * mass * (1.0 + radical))
