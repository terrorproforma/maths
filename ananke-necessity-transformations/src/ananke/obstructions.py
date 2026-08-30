"""Obstruction certificates for candidate realization classes.

The v0 certificate uses a Perron--Frobenius fact: every eigenvalue of modulus one
of a finite stochastic matrix is a root of unity. Therefore, an observable
unit-modulus mode with an irrational phase cannot occur in any exact finite-state
classical stochastic realization.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

import numpy as np
from numpy.typing import NDArray

from .process import LinearProcess

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class RootOfUnityApproximation:
    """Best bounded-denominator root-of-unity approximation to one eigenvalue."""

    eigenvalue_real: float
    eigenvalue_imaginary: float
    modulus: float
    phase_turns: float
    numerator: int
    denominator: int
    phase_error_turns: float
    eigenvalue_distance: float


def best_root_of_unity_approximation(
    eigenvalue: complex,
    maximum_order: int = 10_000,
) -> RootOfUnityApproximation:
    """Approximate a unit-circle eigenvalue by ``exp(2π i p/q)``.

    This is diagnostic, not an exact proof from floating-point data. No finite
    precision observation can establish irrationality of a phase.
    """

    if maximum_order < 1:
        raise ValueError("maximum_order must be positive")

    value = complex(eigenvalue)
    modulus = abs(value)
    if modulus == 0.0:
        raise ValueError("zero has no phase")

    normalized = value / modulus
    phase_turns = float((np.angle(normalized) / (2.0 * np.pi)) % 1.0)
    rational = Fraction(phase_turns).limit_denominator(maximum_order)
    rational_turns = float(rational)
    phase_error = abs(phase_turns - rational_turns)
    phase_error = min(phase_error, 1.0 - phase_error)
    root = np.exp(2j * np.pi * rational_turns)

    return RootOfUnityApproximation(
        eigenvalue_real=float(value.real),
        eigenvalue_imaginary=float(value.imag),
        modulus=float(modulus),
        phase_turns=phase_turns,
        numerator=int(rational.numerator),
        denominator=int(rational.denominator),
        phase_error_turns=float(phase_error),
        eigenvalue_distance=float(abs(normalized - root)),
    )


def peripheral_phase_report(
    process: LinearProcess,
    *,
    modulus_tolerance: float = 1e-8,
    maximum_order: int = 10_000,
) -> dict[str, list[dict[str, Any]]]:
    """Report non-real peripheral eigenmodes of every declared transformation."""

    if modulus_tolerance < 0.0:
        raise ValueError("modulus_tolerance must be non-negative")

    report: dict[str, list[dict[str, Any]]] = {}
    for symbol in process.alphabet:
        entries: list[dict[str, Any]] = []
        eigenvalues = np.linalg.eigvals(process.transitions[symbol])
        for eigenvalue in eigenvalues:
            if abs(abs(eigenvalue) - 1.0) > modulus_tolerance:
                continue
            if abs(eigenvalue.imag) <= modulus_tolerance:
                continue
            approximation = best_root_of_unity_approximation(
                complex(eigenvalue),
                maximum_order=maximum_order,
            )
            entries.append(
                {
                    "eigenvalue": [
                        approximation.eigenvalue_real,
                        approximation.eigenvalue_imaginary,
                    ],
                    "modulus": approximation.modulus,
                    "phase_radians_principal": float(np.angle(eigenvalue)),
                    "phase_turns": approximation.phase_turns,
                    "best_root_of_unity_order_at_most": maximum_order,
                    "nearest_root_numerator": approximation.numerator,
                    "nearest_root_denominator": approximation.denominator,
                    "phase_error_turns": approximation.phase_error_turns,
                    "eigenvalue_distance": approximation.eigenvalue_distance,
                }
            )
        report[symbol] = entries
    return report


def rational_radian_phase_is_not_root_of_unity(angle: Fraction) -> dict[str, Any]:
    """Return an exact analytic certificate for a nonzero rational radian angle.

    If ``exp(i r)`` were a root of unity for nonzero rational ``r``, then
    ``n r = 2π k`` for integers ``n > 0`` and nonzero ``k``. This would make
    ``π = n r / (2 k)`` rational, contradicting the irrationality of π.
    """

    exact = Fraction(angle)
    if exact == 0:
        return {
            "certified": False,
            "reason": "The zero angle gives eigenvalue 1, which is a root of unity.",
        }

    return {
        "certified": True,
        "angle_radians": {
            "numerator": exact.numerator,
            "denominator": exact.denominator,
        },
        "conclusion": "exp(i * angle) is not a root of unity",
        "proof": (
            "Assume exp(i r) has finite order n. Then n r = 2 pi k for an "
            "integer k. Since r is nonzero, k is nonzero, so pi = n r/(2 k) "
            "would be rational. This contradicts the irrationality of pi."
        ),
    }


def finite_classical_channel_obstruction_from_rational_angles(
    process: LinearProcess,
    exact_angles: dict[str, Fraction],
    *,
    spectral_match_tolerance: float = 1e-8,
    maximum_order_diagnostic: int = 10_000,
) -> dict[str, Any]:
    """Certify failure of exact finite-state classical channel realization.

    The certificate assumes each alphabet symbol is meant to be a normalized
    classical channel in any candidate classical realization. A minimal process
    transition is a quotient of the corresponding higher-dimensional channel,
    so its spectrum must be contained in the channel spectrum. Finite stochastic
    matrices can have only roots of unity on the unit circle.
    """

    unknown = set(exact_angles) - set(process.alphabet)
    if unknown:
        raise ValueError(f"exact_angles contains unknown symbols: {sorted(unknown)}")

    diagnostics = peripheral_phase_report(
        process,
        maximum_order=maximum_order_diagnostic,
    )
    certificates: dict[str, Any] = {}
    all_certified = True

    for symbol, angle in exact_angles.items():
        target_candidates = [
            np.exp(1j * float(angle)),
            np.exp(-1j * float(angle)),
        ]
        eigenvalues = np.linalg.eigvals(process.transitions[symbol]).astype(complex)
        spectral_distance = min(
            abs(eigenvalue - target)
            for eigenvalue in eigenvalues
            for target in target_candidates
        )
        phase_certificate = rational_radian_phase_is_not_root_of_unity(angle)
        matched = bool(spectral_distance <= spectral_match_tolerance)
        certified = bool(matched and phase_certificate["certified"])
        all_certified = all_certified and certified
        certificates[symbol] = {
            "spectral_mode_matches_declared_angle": matched,
            "minimum_spectral_distance": float(spectral_distance),
            "analytic_phase_certificate": phase_certificate,
            "classical_finite_channel_obstructed": certified,
        }

    return {
        "assumption": (
            "Each operation is represented classically by a finite nonnegative "
            "stochastic matrix, and the extracted minimal transition is its quotient."
        ),
        "perron_frobenius_fact": (
            "Every unit-modulus eigenvalue of a finite stochastic matrix is a root of unity."
        ),
        "floating_point_diagnostics": diagnostics,
        "symbol_certificates": certificates,
        "finite_classical_realization_obstructed": all_certified,
        "scope": (
            "This excludes exact finite-state classical stochastic realizations. "
            "It does not exclude infinite-state models or finite approximations."
        ),
    }
