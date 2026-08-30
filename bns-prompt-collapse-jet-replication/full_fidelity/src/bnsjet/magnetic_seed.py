"""Pressure-confined poloidal magnetic-field seed utilities.

The exact target normalisation/cutoff must come from the authors' artifacts. These
functions provide a tested implementation once those parameters are supplied; they
do not choose them.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

ArrayLike = npt.ArrayLike


def azimuthal_vector_potential(
    cylindrical_radius: ArrayLike,
    pressure: ArrayLike,
    *,
    pressure_cut: float,
    amplitude: float,
    exponent: float = 2.0,
) -> npt.NDArray[np.float64]:
    """Return ``A_phi = A_b * varpi^2 * max(P-P_cut, 0)^n``.

    This common pressure-confined form yields a poloidal seed when curled in the
    adopted coordinates. The coordinate curl and metric factors remain the
    responsibility of the production solver.
    """

    radius = np.asarray(cylindrical_radius, dtype=np.float64)
    fluid_pressure = np.asarray(pressure, dtype=np.float64)
    radius, fluid_pressure = np.broadcast_arrays(radius, fluid_pressure)
    if np.any(~np.isfinite(radius)) or np.any(~np.isfinite(fluid_pressure)):
        raise ValueError("Radius and pressure must be finite")
    if np.any(radius < 0) or pressure_cut < 0 or exponent <= 0:
        raise ValueError("Require radius >= 0, pressure_cut >= 0 and exponent > 0")
    excess = np.maximum(fluid_pressure - float(pressure_cut), 0.0)
    return float(amplitude) * radius**2 * excess**float(exponent)


def rescale_amplitude_for_peak_field(
    current_peak_field: float,
    target_peak_field: float,
    current_amplitude: float,
) -> float:
    """Linearly rescale vector-potential amplitude to a target peak field."""

    current = float(current_peak_field)
    target = float(target_peak_field)
    amplitude = float(current_amplitude)
    if not np.isfinite(current) or current <= 0:
        raise ValueError("current_peak_field must be finite and positive")
    if not np.isfinite(target) or target <= 0:
        raise ValueError("target_peak_field must be finite and positive")
    if not np.isfinite(amplitude):
        raise ValueError("current_amplitude must be finite")
    return amplitude * target / current
