"""Small physical examples used by the first ANANKE experiment."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .process import LinearProcess

FloatArray = NDArray[np.float64]


def _rotation_x(angle: float) -> FloatArray:
    cosine = float(np.cos(angle))
    sine = float(np.sin(angle))
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, cosine, -sine],
            [0.0, sine, cosine],
        ],
        dtype=float,
    )


def _rotation_z(angle: float) -> FloatArray:
    cosine = float(np.cos(angle))
    sine = float(np.sin(angle))
    return np.array(
        [
            [cosine, -sine, 0.0],
            [sine, cosine, 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def _homogeneous_bloch_map(rotation: FloatArray) -> FloatArray:
    return np.block(
        [
            [np.ones((1, 1)), np.zeros((1, 3))],
            [np.zeros((3, 1)), rotation],
        ]
    )


def qubit_rotation_process(
    theta_x: float = 0.73,
    theta_z: float = 1.11,
    initial_bloch: FloatArray | None = None,
    measurement_axis: FloatArray | None = None,
) -> LinearProcess:
    """Return a one-qubit prepare-transform-measure process.

    The physical column state is ``s = (1, r_x, r_y, r_z)``. The two operations
    are unitary rotations around the x and z axes. The returned ``LinearProcess``
    uses the transposed row-state convention required by the generic extractor.
    """

    if initial_bloch is None:
        initial_bloch_array = np.array([0.23, -0.41, 0.71], dtype=float)
    else:
        initial_bloch_array = np.asarray(initial_bloch, dtype=float).reshape(-1)
    if initial_bloch_array.shape != (3,):
        raise ValueError("initial_bloch must have exactly three components")
    if np.linalg.norm(initial_bloch_array) > 1.0 + 1e-12:
        raise ValueError("initial_bloch lies outside the Bloch ball")

    if measurement_axis is None:
        measurement_axis_array = np.array([0.4, 0.7, -0.2], dtype=float)
    else:
        measurement_axis_array = np.asarray(measurement_axis, dtype=float).reshape(-1)
    if measurement_axis_array.shape != (3,):
        raise ValueError("measurement_axis must have exactly three components")
    norm = float(np.linalg.norm(measurement_axis_array))
    if norm == 0.0:
        raise ValueError("measurement_axis must be non-zero")
    measurement_axis_array = measurement_axis_array / norm

    physical_column_maps = {
        "x": _homogeneous_bloch_map(_rotation_x(theta_x)),
        "z": _homogeneous_bloch_map(_rotation_z(theta_z)),
    }

    initial_row = np.concatenate([[1.0], initial_bloch_array])
    final_column = np.concatenate([[0.5], 0.5 * measurement_axis_array])
    row_transitions = {
        symbol: matrix.T for symbol, matrix in physical_column_maps.items()
    }

    return LinearProcess(
        alphabet=("x", "z"),
        initial=initial_row,
        transitions=row_transitions,
        final=final_column,
    )
