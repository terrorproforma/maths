from __future__ import annotations

import unittest
from math import pi

import numpy as np

from ananke import karpelevich_boundary_radius


class KarpelevichGeometryV1Tests(unittest.TestCase):
    def test_sampled_regions_are_nested_and_conjugation_symmetric(self) -> None:
        for angle in np.linspace(0.0, 2.0 * pi, 31, endpoint=False):
            previous = 0.0
            for order in range(2, 16):
                radius = karpelevich_boundary_radius(order, float(angle))
                conjugate = karpelevich_boundary_radius(
                    order,
                    float((-angle) % (2.0 * pi)),
                )
                self.assertGreaterEqual(radius + 1e-9, previous)
                self.assertAlmostEqual(radius, conjugate, places=9)
                previous = radius


if __name__ == "__main__":
    unittest.main()
