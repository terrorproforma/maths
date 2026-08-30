"""Arithmetic diagnostics for finite-cycle mimicry of transformation phases."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import pi

import numpy as np


@dataclass(frozen=True)
class RationalApproximant:
    """One continued-fraction or bounded-denominator phase approximant."""

    numerator: int
    denominator: int
    value: float
    absolute_error_turns: float
    root_of_unity_distance: float

    def to_dict(self) -> dict[str, object]:
        return {
            "numerator": self.numerator,
            "denominator": self.denominator,
            "value": self.value,
            "absolute_error_turns": self.absolute_error_turns,
            "root_of_unity_distance": self.root_of_unity_distance,
        }


def continued_fraction(value: float, terms: int = 12) -> tuple[int, ...]:
    """Return a finite simple continued-fraction expansion of a real number."""

    if terms <= 0:
        raise ValueError("terms must be positive")
    x = float(value)
    if not np.isfinite(x):
        raise ValueError("value must be finite")
    coefficients: list[int] = []
    for _ in range(terms):
        coefficient = int(np.floor(x))
        coefficients.append(coefficient)
        remainder = x - coefficient
        if abs(remainder) < 1e-15:
            break
        x = 1.0 / remainder
    return tuple(coefficients)


def convergents(coefficients: tuple[int, ...]) -> tuple[Fraction, ...]:
    """Return all convergents of a simple continued fraction."""

    if not coefficients:
        raise ValueError("coefficients must not be empty")
    p_minus_two, p_minus_one = 0, 1
    q_minus_two, q_minus_one = 1, 0
    result: list[Fraction] = []
    for coefficient in coefficients:
        p = coefficient * p_minus_one + p_minus_two
        q = coefficient * q_minus_one + q_minus_two
        result.append(Fraction(p, q))
        p_minus_two, p_minus_one = p_minus_one, p
        q_minus_two, q_minus_one = q_minus_one, q
    return tuple(result)


def nearest_root_of_unity(
    phase_turns: float,
    maximum_order: int,
) -> RationalApproximant:
    """Find the nearest phase fraction with denominator at most ``maximum_order``."""

    if maximum_order < 1:
        raise ValueError("maximum_order must be positive")
    turns = float(phase_turns % 1.0)
    rational = Fraction(turns).limit_denominator(int(maximum_order))
    rational_turns = float(rational)
    error = abs(turns - rational_turns)
    error = min(error, 1.0 - error)
    root_distance = abs(
        np.exp(2j * pi * turns) - np.exp(2j * pi * rational_turns)
    )
    return RationalApproximant(
        numerator=int(rational.numerator),
        denominator=int(rational.denominator),
        value=rational_turns,
        absolute_error_turns=float(error),
        root_of_unity_distance=float(root_distance),
    )


def approximation_record_sequence(
    phase_turns: float,
    maximum_order: int,
) -> tuple[tuple[int, RationalApproximant], ...]:
    """Return orders at which the best bounded-denominator approximant changes."""

    if maximum_order < 1:
        raise ValueError("maximum_order must be positive")
    records: list[tuple[int, RationalApproximant]] = []
    previous: tuple[int, int] | None = None
    for order in range(1, maximum_order + 1):
        approximant = nearest_root_of_unity(phase_turns, order)
        identity = (approximant.numerator, approximant.denominator)
        if identity != previous:
            records.append((order, approximant))
            previous = identity
    return tuple(records)
