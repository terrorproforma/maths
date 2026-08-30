from __future__ import annotations

import math

import numpy as np

from bnsjet.diagnostics.horizon import (
    christodoulou_mass,
    dimensionless_spin,
    horizon_angular_frequency,
    irreducible_mass,
)


def test_nonspinning_horizon() -> None:
    mass = 2.5
    area = 16.0 * math.pi * mass**2
    assert np.isclose(irreducible_mass(area), mass)
    assert np.isclose(christodoulou_mass(area, 0.0), mass)
    assert np.isclose(dimensionless_spin(area, 0.0), 0.0)
    assert np.isclose(horizon_angular_frequency(area, 0.0), 0.0)


def test_kerr_horizon_recovers_mass_and_spin() -> None:
    mass = 3.0
    spin = 0.7
    angular_momentum = spin * mass**2
    irreducible = mass * math.sqrt((1.0 + math.sqrt(1.0 - spin**2)) / 2.0)
    area = 16.0 * math.pi * irreducible**2
    assert np.isclose(christodoulou_mass(area, angular_momentum), mass)
    assert np.isclose(dimensionless_spin(area, angular_momentum), spin)


def test_invalid_horizon_area_rejected() -> None:
    with np.testing.assert_raises(ValueError):
        irreducible_mass(0.0)
