"""Solver-neutral physical diagnostics."""

from .convergence import observed_order_equal_ratio, richardson_extrapolate
from .ejecta import bernoulli_unbound_mask, geodesic_unbound_mask
from .fluxes import shell_integral
from .horizon import christodoulou_mass, dimensionless_spin, irreducible_mass
from .jet import luminosity_containing_angle, sustained_crossing_time
from .magnetic import alfven_speed, mri_quality_factor

__all__ = [
    "alfven_speed",
    "bernoulli_unbound_mask",
    "christodoulou_mass",
    "dimensionless_spin",
    "geodesic_unbound_mask",
    "irreducible_mass",
    "luminosity_containing_angle",
    "mri_quality_factor",
    "observed_order_equal_ratio",
    "richardson_extrapolate",
    "shell_integral",
    "sustained_crossing_time",
]
