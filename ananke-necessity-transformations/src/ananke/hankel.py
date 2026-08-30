"""Hankel construction and spectral extraction of a minimal linear process."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

import numpy as np
from numpy.typing import NDArray

from .process import LinearProcess
from .words import words_upto

FloatArray = NDArray[np.float64]
Behaviour = Callable[[str], float]


@dataclass(frozen=True)
class HankelData:
    """A finite block of the behavioural Hankel operator and its shifts."""

    alphabet: tuple[str, ...]
    prefixes: tuple[str, ...]
    suffixes: tuple[str, ...]
    matrix: FloatArray
    shifts: Mapping[str, FloatArray]


@dataclass(frozen=True)
class SpectralExtraction:
    """Result of a finite Hankel spectral realization."""

    process: LinearProcess
    singular_values: FloatArray
    retained_rank: int
    threshold: float
    prefix_coordinates: FloatArray
    suffix_coordinates: FloatArray
    factorization_error: float
    shifted_factorization_errors: Mapping[str, float]


def build_hankel(
    behaviour: Behaviour,
    alphabet: tuple[str, ...],
    max_prefix_length: int,
    max_suffix_length: int,
) -> HankelData:
    """Construct ``H[u,v] = f(uv)`` and ``H_a[u,v] = f(uav)``."""

    prefixes = tuple(words_upto(alphabet, max_prefix_length))
    suffixes = tuple(words_upto(alphabet, max_suffix_length))

    matrix = np.array(
        [[behaviour(prefix + suffix) for suffix in suffixes] for prefix in prefixes],
        dtype=float,
    )
    shifts = {
        symbol: np.array(
            [
                [
                    behaviour(prefix + symbol + suffix)
                    for suffix in suffixes
                ]
                for prefix in prefixes
            ],
            dtype=float,
        )
        for symbol in alphabet
    }

    return HankelData(
        alphabet=tuple(alphabet),
        prefixes=prefixes,
        suffixes=suffixes,
        matrix=matrix,
        shifts=shifts,
    )


def extract_minimal_process(
    hankel: HankelData,
    *,
    rank: int | None = None,
    relative_tolerance: float = 1e-10,
    absolute_tolerance: float = 1e-12,
) -> SpectralExtraction:
    """Extract a minimal linear realization from a finite Hankel block.

    In exact arithmetic, a sufficiently rich Hankel block of rank ``n`` yields
    an ``n``-dimensional realization. With noisy data, rank selection becomes a
    statistical model-selection problem; v0 exposes the threshold explicitly.
    """

    if relative_tolerance < 0.0 or absolute_tolerance < 0.0:
        raise ValueError("tolerances must be non-negative")

    left, singular_values, right_transpose = np.linalg.svd(
        hankel.matrix,
        full_matrices=False,
    )
    if singular_values.size == 0:
        raise ValueError("the Hankel matrix is empty")

    threshold = max(
        float(absolute_tolerance),
        float(relative_tolerance * singular_values[0]),
    )
    detected_rank = int(np.count_nonzero(singular_values > threshold))
    retained_rank = detected_rank if rank is None else int(rank)

    if retained_rank <= 0:
        raise ValueError("retained rank must be positive")
    if retained_rank > min(hankel.matrix.shape):
        raise ValueError("retained rank exceeds the Hankel block dimensions")

    root_singular = np.diag(np.sqrt(singular_values[:retained_rank]))
    prefix_coordinates = left[:, :retained_rank] @ root_singular
    suffix_coordinates = root_singular @ right_transpose[:retained_rank, :]

    prefix_pseudoinverse = np.linalg.pinv(prefix_coordinates)
    suffix_pseudoinverse = np.linalg.pinv(suffix_coordinates)

    transitions = {
        symbol: prefix_pseudoinverse
        @ shifted
        @ suffix_pseudoinverse
        for symbol, shifted in hankel.shifts.items()
    }

    try:
        empty_prefix_index = hankel.prefixes.index("")
        empty_suffix_index = hankel.suffixes.index("")
    except ValueError as error:
        raise ValueError("prefix and suffix sets must include the empty word") from error

    process = LinearProcess(
        alphabet=hankel.alphabet,
        initial=prefix_coordinates[empty_prefix_index, :],
        transitions=transitions,
        final=suffix_coordinates[:, empty_suffix_index],
    )

    factorization_error = float(
        np.linalg.norm(
            hankel.matrix - prefix_coordinates @ suffix_coordinates,
            ord="fro",
        )
    )
    shifted_errors = {
        symbol: float(
            np.linalg.norm(
                hankel.shifts[symbol]
                - prefix_coordinates
                @ transitions[symbol]
                @ suffix_coordinates,
                ord="fro",
            )
        )
        for symbol in hankel.alphabet
    }

    return SpectralExtraction(
        process=process,
        singular_values=singular_values,
        retained_rank=retained_rank,
        threshold=threshold,
        prefix_coordinates=prefix_coordinates,
        suffix_coordinates=suffix_coordinates,
        factorization_error=factorization_error,
        shifted_factorization_errors=shifted_errors,
    )
