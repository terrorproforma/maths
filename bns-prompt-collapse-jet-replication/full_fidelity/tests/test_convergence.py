from __future__ import annotations

import math

from bnsjet.diagnostics.convergence import (
    grid_convergence_index,
    observed_order_equal_ratio,
    richardson_extrapolate,
)


def test_second_order_sequence() -> None:
    exact = 2.0
    coarse = exact + 4.0
    medium = exact + 1.0
    fine = exact + 0.25
    order = observed_order_equal_ratio(coarse, medium, fine, 2.0)
    assert math.isclose(order, 2.0)
    extrapolated = richardson_extrapolate(medium, fine, 2.0, order)
    assert math.isclose(extrapolated, exact)
    assert grid_convergence_index(medium, fine, 2.0, order) > 0
