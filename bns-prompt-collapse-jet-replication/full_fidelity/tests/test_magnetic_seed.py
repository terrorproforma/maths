from __future__ import annotations

import numpy as np

from bnsjet.magnetic_seed import azimuthal_vector_potential, rescale_amplitude_for_peak_field


def test_pressure_confined_seed() -> None:
    radius = np.array([1.0, 2.0, 3.0])
    pressure = np.array([0.5, 1.5, 2.5])
    potential = azimuthal_vector_potential(
        radius,
        pressure,
        pressure_cut=1.0,
        amplitude=2.0,
        exponent=2.0,
    )
    assert np.allclose(potential, [0.0, 2.0, 40.5])
    assert rescale_amplitude_for_peak_field(1.0e14, 1.0e15, 2.0) == 20.0
