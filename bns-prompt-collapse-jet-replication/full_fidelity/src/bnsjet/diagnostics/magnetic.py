"""Magnetic-energy and MRI-resolution diagnostics."""

from __future__ import annotations

import math

import numpy as np
import numpy.typing as npt

ArrayLike = npt.ArrayLike


def alfven_speed(
    magnetic_four_vector_squared: ArrayLike,
    rest_mass_density: ArrayLike,
    specific_enthalpy: ArrayLike,
) -> npt.NDArray[np.float64]:
    """Return relativistic Alfvén speed ``sqrt(b^2 / (rho*h + b^2))``."""

    b_squared = np.asarray(magnetic_four_vector_squared, dtype=np.float64)
    density = np.asarray(rest_mass_density, dtype=np.float64)
    enthalpy = np.asarray(specific_enthalpy, dtype=np.float64)
    b_squared, density, enthalpy = np.broadcast_arrays(b_squared, density, enthalpy)
    if np.any(~np.isfinite(b_squared)) or np.any(~np.isfinite(density)) or np.any(~np.isfinite(enthalpy)):
        raise ValueError("MRI inputs must be finite")
    if np.any(b_squared < 0) or np.any(density <= 0) or np.any(enthalpy <= 0):
        raise ValueError("Require b^2 >= 0, rho > 0 and h > 0")
    return np.sqrt(b_squared / (density * enthalpy + b_squared))


def fastest_mri_wavelength(
    magnetic_four_vector_squared: ArrayLike,
    rest_mass_density: ArrayLike,
    specific_enthalpy: ArrayLike,
    angular_frequency: ArrayLike,
) -> npt.NDArray[np.float64]:
    """Return the local MRI wavelength proxy ``2*pi*v_A/|Omega|``."""

    speed = alfven_speed(magnetic_four_vector_squared, rest_mass_density, specific_enthalpy)
    omega = np.asarray(angular_frequency, dtype=np.float64)
    omega = np.broadcast_to(omega, speed.shape)
    if np.any(~np.isfinite(omega)) or np.any(np.abs(omega) <= 0):
        raise ValueError("Angular frequency must be finite and non-zero")
    return 2.0 * math.pi * speed / np.abs(omega)


def mri_quality_factor(
    magnetic_four_vector_squared: ArrayLike,
    rest_mass_density: ArrayLike,
    specific_enthalpy: ArrayLike,
    angular_frequency: ArrayLike,
    proper_cell_length: ArrayLike,
) -> npt.NDArray[np.float64]:
    """Return number of proper cells per fastest-growing MRI wavelength."""

    wavelength = fastest_mri_wavelength(
        magnetic_four_vector_squared,
        rest_mass_density,
        specific_enthalpy,
        angular_frequency,
    )
    spacing = np.asarray(proper_cell_length, dtype=np.float64)
    spacing = np.broadcast_to(spacing, wavelength.shape)
    if np.any(~np.isfinite(spacing)) or np.any(spacing <= 0):
        raise ValueError("Proper cell length must be finite and positive")
    return wavelength / spacing


def magnetisation(
    magnetic_four_vector_squared: ArrayLike,
    rest_mass_density: ArrayLike,
) -> npt.NDArray[np.float64]:
    """Return ``sigma = b^2 / rho`` in the supplied consistent unit convention."""

    b_squared = np.asarray(magnetic_four_vector_squared, dtype=np.float64)
    density = np.asarray(rest_mass_density, dtype=np.float64)
    b_squared, density = np.broadcast_arrays(b_squared, density)
    if np.any(b_squared < 0) or np.any(density <= 0):
        raise ValueError("Require b^2 >= 0 and rho > 0")
    return b_squared / density
