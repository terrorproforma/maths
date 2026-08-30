"""Finite-dimensional linear process descriptions.

A process is represented as

    f(a_1 ... a_k) = alpha @ B[a_1] @ ... @ B[a_k] @ omega.

The vectors and matrices are coordinates, not observables. An invertible change
of coordinates leaves every value of ``f`` unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
from numpy.typing import NDArray

from .words import validate_word

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class LinearProcess:
    """A real finite-dimensional linear realization of sequential behaviour."""

    alphabet: tuple[str, ...]
    initial: FloatArray
    transitions: Mapping[str, FloatArray]
    final: FloatArray

    def __post_init__(self) -> None:
        alphabet = tuple(self.alphabet)
        if not alphabet:
            raise ValueError("alphabet must not be empty")
        if len(set(alphabet)) != len(alphabet):
            raise ValueError("alphabet symbols must be unique")
        if any(len(symbol) != 1 for symbol in alphabet):
            raise ValueError("the v0 implementation requires one-character symbols")

        initial = np.asarray(self.initial, dtype=float).reshape(-1).copy()
        final = np.asarray(self.final, dtype=float).reshape(-1).copy()
        if initial.size == 0:
            raise ValueError("process dimension must be positive")
        if final.shape != initial.shape:
            raise ValueError("initial and final vectors must have the same dimension")
        if not np.all(np.isfinite(initial)) or not np.all(np.isfinite(final)):
            raise ValueError("initial and final vectors must contain finite values")

        transitions: dict[str, FloatArray] = {}
        for symbol in alphabet:
            if symbol not in self.transitions:
                raise ValueError(f"missing transition for symbol {symbol!r}")
            matrix = np.asarray(self.transitions[symbol], dtype=float).copy()
            expected_shape = (initial.size, initial.size)
            if matrix.shape != expected_shape:
                raise ValueError(
                    f"transition {symbol!r} has shape {matrix.shape}; "
                    f"expected {expected_shape}"
                )
            if not np.all(np.isfinite(matrix)):
                raise ValueError(f"transition {symbol!r} contains non-finite values")
            transitions[symbol] = matrix

        extra = set(self.transitions) - set(alphabet)
        if extra:
            raise ValueError(f"transitions contain symbols outside the alphabet: {sorted(extra)}")

        object.__setattr__(self, "alphabet", alphabet)
        object.__setattr__(self, "initial", initial)
        object.__setattr__(self, "final", final)
        object.__setattr__(self, "transitions", transitions)

    @property
    def dimension(self) -> int:
        """Coordinate dimension of this particular realization."""

        return int(self.initial.size)

    def row_after(self, word: str) -> FloatArray:
        """Return the internal row state after applying ``word``."""

        validate_word(word, self.alphabet)
        row = self.initial.copy()
        for symbol in word:
            row = row @ self.transitions[symbol]
        return row

    def behavior(self, word: str) -> float:
        """Evaluate the observable scalar behaviour for ``word``."""

        return float(self.row_after(word) @ self.final)

    def gauge_transform(self, coordinate_map: FloatArray) -> "LinearProcess":
        """Return an observationally equivalent invertible coordinate change.

        For an invertible matrix ``S`` the transformed realization is

            alpha' = alpha S,
            B'_a   = S^{-1} B_a S,
            omega' = S^{-1} omega.

        Every word probability is therefore exactly unchanged, up to numerical
        roundoff.
        """

        matrix = np.asarray(coordinate_map, dtype=float)
        expected = (self.dimension, self.dimension)
        if matrix.shape != expected:
            raise ValueError(f"coordinate_map has shape {matrix.shape}; expected {expected}")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("coordinate_map contains non-finite values")
        if np.linalg.matrix_rank(matrix) != self.dimension:
            raise ValueError("coordinate_map must be invertible")

        transformed = {
            symbol: np.linalg.solve(matrix, transition @ matrix)
            for symbol, transition in self.transitions.items()
        }
        return LinearProcess(
            alphabet=self.alphabet,
            initial=self.initial @ matrix,
            transitions=transformed,
            final=np.linalg.solve(matrix, self.final),
        )

    def pad_with_unreachable_hidden_dynamics(
        self,
        hidden_transitions: Mapping[str, FloatArray],
        hidden_final: FloatArray | None = None,
    ) -> "LinearProcess":
        """Add a dynamically active but unreachable hidden subsystem.

        The hidden initial state is exactly zero and transitions are block
        diagonal. The extra coordinates may have arbitrary internal dynamics,
        but no experiment beginning from the declared preparation can reach
        them. The observable behaviour is unchanged.
        """

        if set(hidden_transitions) != set(self.alphabet):
            raise ValueError("hidden_transitions must contain exactly the process alphabet")

        first = np.asarray(hidden_transitions[self.alphabet[0]], dtype=float)
        if first.ndim != 2 or first.shape[0] != first.shape[1] or first.shape[0] == 0:
            raise ValueError("hidden transitions must be non-empty square matrices")
        hidden_dimension = first.shape[0]

        checked: dict[str, FloatArray] = {}
        for symbol in self.alphabet:
            matrix = np.asarray(hidden_transitions[symbol], dtype=float).copy()
            if matrix.shape != (hidden_dimension, hidden_dimension):
                raise ValueError("all hidden transitions must have the same square shape")
            if not np.all(np.isfinite(matrix)):
                raise ValueError("hidden transitions must contain finite values")
            checked[symbol] = matrix

        if hidden_final is None:
            hidden_final_array = np.ones(hidden_dimension, dtype=float)
        else:
            hidden_final_array = np.asarray(hidden_final, dtype=float).reshape(-1).copy()
            if hidden_final_array.shape != (hidden_dimension,):
                raise ValueError("hidden_final has the wrong dimension")

        padded_transitions: dict[str, FloatArray] = {}
        for symbol in self.alphabet:
            visible = self.transitions[symbol]
            hidden = checked[symbol]
            padded_transitions[symbol] = np.block(
                [
                    [visible, np.zeros((self.dimension, hidden_dimension))],
                    [np.zeros((hidden_dimension, self.dimension)), hidden],
                ]
            )

        return LinearProcess(
            alphabet=self.alphabet,
            initial=np.concatenate([self.initial, np.zeros(hidden_dimension)]),
            transitions=padded_transitions,
            final=np.concatenate([self.final, hidden_final_array]),
        )
