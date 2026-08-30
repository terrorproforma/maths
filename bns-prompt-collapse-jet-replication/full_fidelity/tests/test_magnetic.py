from __future__ import annotations

import math

import numpy as np

from bnsjet.diagnostics.magnetic import alfven_speed, magnetisation, mri_quality_factor


def test_alfven_speed_and_quality() -> None:
    speed = alfven_speed(1.0, 3.0, 1.0)
    assert np.isclose(speed, 0.5)
    quality = mri_quality_factor(1.0, 3.0, 1.0, math.pi, 0.1)
    assert np.isclose(quality, 10.0)
    assert np.isclose(magnetisation(1.0, 2.0), 0.5)
