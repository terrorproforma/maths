from __future__ import annotations

import math

import numpy as np

from bnsjet.diagnostics.fluxes import hemispheric_integrals, outward_only, shell_integral


def test_shell_integral() -> None:
    flux = np.array([1.0, 2.0, -1.0])
    weights = np.array([0.5, 0.5, 1.0])
    assert math.isclose(shell_integral(flux, weights), 0.5)
    assert math.isclose(shell_integral(outward_only(flux), weights), 1.5)


def test_hemispheric_integrals() -> None:
    theta = np.array([0.2, 1.0, 2.0, 2.9])
    flux = np.ones(4)
    weights = np.array([1.0, 2.0, 3.0, 4.0])
    north, south = hemispheric_integrals(flux, weights, theta)
    assert math.isclose(north, 3.0)
    assert math.isclose(south, 7.0)
