"""Similarity-invariant fingerprints of extracted process transformations."""

from __future__ import annotations

from itertools import product
from typing import Any

import numpy as np
from numpy.typing import NDArray

from .process import LinearProcess

ComplexArray = NDArray[np.complex128]


def _complex_pair(value: complex, zero_tolerance: float = 1e-12) -> list[float]:
    real = 0.0 if abs(value.real) < zero_tolerance else float(value.real)
    imaginary = 0.0 if abs(value.imag) < zero_tolerance else float(value.imag)
    return [real, imaginary]


def _sorted_eigenvalues(matrix: NDArray[np.float64]) -> ComplexArray:
    values = np.linalg.eigvals(matrix).astype(complex)
    order = np.lexsort((np.round(values.imag, 12), np.round(values.real, 12)))
    return values[order]


def transition_fingerprint(matrix: NDArray[np.float64]) -> dict[str, Any]:
    """Return basic invariants under arbitrary invertible similarity."""

    dimension = matrix.shape[0]
    fixed_rank = np.linalg.matrix_rank(matrix - np.eye(dimension), tol=1e-10)
    characteristic = np.poly(matrix).astype(complex)
    return {
        "trace": _complex_pair(complex(np.trace(matrix))),
        "determinant": _complex_pair(complex(np.linalg.det(matrix))),
        "eigenvalues": [_complex_pair(value) for value in _sorted_eigenvalues(matrix)],
        "characteristic_polynomial": [
            _complex_pair(value) for value in characteristic
        ],
        "fixed_space_dimension": int(dimension - fixed_rank),
    }


def trace_word_fingerprint(
    process: LinearProcess,
    max_word_length: int = 3,
) -> dict[str, list[float]]:
    """Return traces of all transition words through a chosen length.

    Traces of words are unchanged by a simultaneous similarity transform of the
    entire transition tuple. The finite list is a fingerprint, not a claim of a
    complete invariant for arbitrary matrix tuples.
    """

    if max_word_length < 1:
        raise ValueError("max_word_length must be at least one")

    result: dict[str, list[float]] = {}
    for length in range(1, max_word_length + 1):
        for symbols in product(process.alphabet, repeat=length):
            word = "".join(symbols)
            matrix = np.eye(process.dimension)
            for symbol in word:
                matrix = matrix @ process.transitions[symbol]
            result[word] = _complex_pair(complex(np.trace(matrix)))
    return result


def process_fingerprint(
    process: LinearProcess,
    max_trace_word_length: int = 3,
) -> dict[str, Any]:
    """Return a coordinate-independent finite fingerprint of a process tuple."""

    stacked_fixed_constraints = np.vstack(
        [
            process.transitions[symbol] - np.eye(process.dimension)
            for symbol in process.alphabet
        ]
    )
    common_fixed_dimension = int(
        process.dimension
        - np.linalg.matrix_rank(stacked_fixed_constraints, tol=1e-10)
    )

    return {
        "dimension": process.dimension,
        "transitions": {
            symbol: transition_fingerprint(process.transitions[symbol])
            for symbol in process.alphabet
        },
        "common_fixed_space_dimension": common_fixed_dimension,
        "trace_words": trace_word_fingerprint(
            process,
            max_word_length=max_trace_word_length,
        ),
    }
