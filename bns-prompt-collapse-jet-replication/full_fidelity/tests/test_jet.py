from __future__ import annotations

import math

import numpy as np

from bnsjet.diagnostics.jet import (
    hemispheric_asymmetry,
    luminosity_containing_angle,
    sustained_crossing_time,
)


def test_sustained_crossing_time() -> None:
    time = np.arange(0.0, 1.1, 0.1)
    signal = np.array([0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 2], dtype=float)
    assert math.isclose(sustained_crossing_time(time, signal, 1.0, 0.3), 0.6)


def test_luminosity_containing_angle_north() -> None:
    theta = np.array([0.05, 0.10, 0.20, 2.9])
    luminosity = np.array([4.0, 3.0, 3.0, 100.0])
    weights = np.ones(4)
    angle = luminosity_containing_angle(theta, luminosity, weights, hemisphere="north", fraction=0.7)
    assert math.isclose(angle, 0.10)


def test_asymmetry_bounds() -> None:
    assert math.isclose(hemispheric_asymmetry(3.0, 1.0), 0.5)
    assert math.isclose(hemispheric_asymmetry(0.0, 0.0), 0.0)
