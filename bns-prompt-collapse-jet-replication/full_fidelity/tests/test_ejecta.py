from __future__ import annotations

import numpy as np

from bnsjet.diagnostics.ejecta import (
    bernoulli_unbound_mask,
    geodesic_unbound_mask,
    weighted_distribution,
)


def test_unbound_masks() -> None:
    u_t = np.array([-1.2, -1.0, -0.9])
    outward = np.array([1.0, 1.0, 1.0])
    assert geodesic_unbound_mask(u_t, outward_velocity=outward).tolist() == [True, False, False]
    enthalpy = np.array([1.0, 1.2, 1.2])
    assert bernoulli_unbound_mask(u_t, enthalpy).tolist() == [True, True, True]


def test_weighted_distribution_normalises() -> None:
    histogram, edges = weighted_distribution(
        [0.1, 0.2, 0.8],
        [1.0, 1.0, 2.0],
        [0.0, 0.5, 1.0],
        normalise=True,
    )
    assert np.allclose(histogram, [0.5, 0.5])
    assert np.allclose(edges, [0.0, 0.5, 1.0])
