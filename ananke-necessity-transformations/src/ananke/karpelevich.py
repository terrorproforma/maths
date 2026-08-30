"""Finite-state stochastic spectral obstructions.

For an n-state row-stochastic matrix every eigenvalue lies in the Karpelevič
region Theta_n. The radial boundary implementation follows the algebraic formula
of Kirkland, Laffey and Šmigoc (2020). Finite-data reports combine:

* an analytic Dmitriev--Dynkin tangent-wedge certificate; and
* a convergence-checked numerical distance to the full Karpelevič boundary.

The latter is deliberately labelled numerical: floating-point global
minimisation is evidence, not an interval-arithmetic proof.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import gcd, pi, sin, sqrt, tan
from typing import Iterable

import numpy as np

TWO_PI = 2.0 * pi


@lru_cache(maxsize=None)
def farey_sequence(order: int) -> tuple[Fraction, ...]:
    """Return the Farey sequence of positive integer ``order``."""

    n = int(order)
    if n < 1:
        raise ValueError("Farey order must be positive")
    a, b, c, d = 0, 1, 1, n
    sequence = [Fraction(0, 1)]
    while c <= n:
        sequence.append(Fraction(c, d))
        multiplier = (n + b) // d
        a, b, c, d = c, d, multiplier * c - a, multiplier * d - b
    return tuple(sequence)


@lru_cache(maxsize=None)
def _farey_values(order: int) -> tuple[float, ...]:
    return tuple(float(value) for value in farey_sequence(order))


def _farey_neighbours(
    order: int,
    phase_turns: float,
    *,
    endpoint_tolerance: float = 2e-14,
) -> tuple[Fraction, Fraction]:
    turns = float(phase_turns % 1.0)
    sequence = farey_sequence(order)
    values = _farey_values(order)
    index = bisect_right(values, turns)
    if index <= 0:
        return sequence[0], sequence[1]
    if index >= len(sequence):
        return sequence[-2], sequence[-1]
    if abs(values[index - 1] - turns) <= endpoint_tolerance:
        return sequence[index - 1], sequence[index - 1]
    if abs(values[index] - turns) <= endpoint_tolerance:
        return sequence[index], sequence[index]
    return sequence[index - 1], sequence[index]


def _solve_l0(r1: int, d1: int, s1: int) -> int:
    for l0 in range(d1):
        numerator = r1 + l0 * s1
        if numerator % d1 == 0:
            rhat = numerator // d1
            if 0 <= rhat < s1:
                return l0
    raise ArithmeticError(
        f"failed Karpelevič modular solve: r1={r1}, d1={d1}, s1={s1}"
    )


def _positive_unit_interval_root(
    coefficient_a: float,
    exponent_a: int,
    coefficient_b: float,
    exponent_b: int,
    constant_c: float,
) -> float:
    """Solve A*x^a - B*x^b - C = 0 for its selected root in (0,1]."""

    degree = max(exponent_a, exponent_b)
    coefficients = np.zeros(degree + 1, dtype=float)
    coefficients[0] = -constant_c
    coefficients[exponent_a] += coefficient_a
    coefficients[exponent_b] -= coefficient_b
    while coefficients.size > 1 and abs(coefficients[-1]) < 1e-15:
        coefficients = coefficients[:-1]

    roots = np.polynomial.polynomial.polyroots(coefficients)
    candidates = sorted(
        float(root.real)
        for root in roots
        if abs(root.imag) <= 2e-7
        and root.real > 1e-12
        and root.real <= 1.0 + 2e-8
    )
    if candidates:
        return min(1.0, candidates[0])

    def polynomial(value: float) -> float:
        return (
            coefficient_a * value**exponent_a
            - coefficient_b * value**exponent_b
            - constant_c
        )

    grid = np.linspace(0.0, 1.0, 4097)
    previous_x = 0.0
    previous_f = polynomial(previous_x)
    for current_x in grid[1:]:
        x = float(current_x)
        current_f = polynomial(x)
        if abs(current_f) < 1e-12 and x > 1e-10:
            return min(1.0, x)
        if previous_f * current_f < 0.0:
            low, high = previous_x, x
            low_value = previous_f
            for _ in range(100):
                midpoint = 0.5 * (low + high)
                midpoint_value = polynomial(midpoint)
                if low_value * midpoint_value <= 0.0:
                    high = midpoint
                else:
                    low = midpoint
                    low_value = midpoint_value
            return 0.5 * (low + high)
        previous_x = x
        previous_f = current_f
    raise ArithmeticError("no Karpelevič radial root found in (0,1]")


@lru_cache(maxsize=250_000)
def _boundary_radius_cached(order: int, wrapped_angle: float) -> float:
    n = int(order)
    if n < 2:
        raise ValueError("Karpelevič order must be at least two")
    phase_turns = (wrapped_angle / TWO_PI) % 1.0
    if phase_turns <= 2e-14 or phase_turns >= 1.0 - 2e-14:
        return 1.0

    left, right = _farey_neighbours(n, phase_turns)
    if left == right:
        return 1.0
    p, q = left.numerator, left.denominator
    r, s = right.numerator, right.denominator
    theta = TWO_PI * phase_turns

    # The radial theorem is stated for q < s. Conjugation handles q > s.
    if q > s:
        p, q, r, s = s - r, s, q - p, q
        phase_turns = 1.0 - phase_turns
        theta = TWO_PI * phase_turns
    if q >= s:
        raise ArithmeticError(f"invalid Farey orientation: {p}/{q}, {r}/{s}")

    d = n // q
    delta = gcd(d, s)
    s1 = s // delta
    d1 = d // delta
    r1 = r // delta
    j0 = r % delta
    l0 = _solve_l0(r1, d1, s1)
    theta_hat = (theta + TWO_PI * l0) / d1

    coefficient_a = sin(q * d1 * theta_hat)
    coefficient_b = sin(s1 * theta_hat - TWO_PI * j0 / (delta * d1))
    constant_c = sin(
        (q * d1 - s1) * theta_hat + TWO_PI * j0 / (delta * d1)
    )
    rho_hat = _positive_unit_interval_root(
        coefficient_a,
        s1,
        coefficient_b,
        q * d1,
        constant_c,
    )
    return float(np.clip(rho_hat**d1, 0.0, 1.0))


def karpelevich_boundary_radius(order: int, angle_radians: float) -> float:
    """Return the radial boundary of Theta_order at a polar angle."""

    return _boundary_radius_cached(int(order), float(angle_radians % TWO_PI))


def karpelevich_contains(
    value: complex,
    order: int,
    *,
    tolerance: float = 1e-10,
) -> bool:
    """Test radial membership in a finite stochastic eigenvalue region."""

    z = complex(value)
    n = int(order)
    if n == 1:
        return abs(z - 1.0) <= tolerance
    if n < 1:
        raise ValueError("order must be positive")
    if abs(z) > 1.0 + tolerance:
        return False
    boundary = karpelevich_boundary_radius(n, float(np.angle(z)))
    return bool(abs(z) <= boundary + tolerance)


@dataclass(frozen=True)
class BoundaryDistanceResult:
    order: int
    distance: float
    closest_angle_radians: float
    closest_point: complex
    coarse_points: int

    def to_dict(self) -> dict[str, object]:
        return {
            "order": self.order,
            "distance": self.distance,
            "closest_angle_radians": self.closest_angle_radians,
            "closest_point": [self.closest_point.real, self.closest_point.imag],
            "coarse_points": self.coarse_points,
        }


def _boundary_point(order: int, angle: float) -> complex:
    radius = karpelevich_boundary_radius(order, angle)
    return complex(radius * np.exp(1j * angle))


def _golden_section_minimum(
    objective,
    low: float,
    high: float,
    *,
    iterations: int = 80,
) -> tuple[float, float]:
    ratio = (sqrt(5.0) - 1.0) / 2.0
    left = high - ratio * (high - low)
    right = low + ratio * (high - low)
    left_value = float(objective(left))
    right_value = float(objective(right))
    for _ in range(iterations):
        if left_value < right_value:
            high = right
            right = left
            right_value = left_value
            left = high - ratio * (high - low)
            left_value = float(objective(left))
        else:
            low = left
            left = right
            left_value = right_value
            right = low + ratio * (high - low)
            right_value = float(objective(right))
    return (left, left_value) if left_value <= right_value else (right, right_value)


def distance_to_karpelevich_region(
    value: complex,
    order: int,
    *,
    coarse_points: int = 384,
    local_candidates: int = 8,
) -> BoundaryDistanceResult:
    """Numerically minimise Euclidean distance to Theta_order."""

    if coarse_points < 32:
        raise ValueError("coarse_points must be at least 32")
    z = complex(value)
    n = int(order)
    if n == 1:
        return BoundaryDistanceResult(1, float(abs(z - 1.0)), 0.0, 1.0 + 0.0j, coarse_points)
    if karpelevich_contains(z, n):
        angle = float(np.angle(z) % TWO_PI)
        return BoundaryDistanceResult(n, 0.0, angle, z, coarse_points)

    angles = np.linspace(0.0, TWO_PI, coarse_points, endpoint=False)
    distances = np.asarray(
        [abs(z - _boundary_point(n, float(angle))) for angle in angles],
        dtype=float,
    )
    candidate_indices = np.argsort(distances)[: min(local_candidates, coarse_points)]
    step = TWO_PI / coarse_points
    best_distance = float("inf")
    best_angle = 0.0

    def objective(angle: float) -> float:
        return abs(z - _boundary_point(n, float(angle % TWO_PI)))

    for index in candidate_indices:
        centre = float(angles[int(index)])
        angle, distance = _golden_section_minimum(
            objective,
            centre - step,
            centre + step,
        )
        if distance < best_distance:
            best_distance = distance
            best_angle = angle % TWO_PI
    closest = _boundary_point(n, best_angle)
    return BoundaryDistanceResult(
        n,
        float(best_distance),
        float(best_angle),
        closest,
        coarse_points,
    )


def dmitriev_dynkin_wedge_distance(value: complex, order: int) -> float:
    """Distance outside the analytic tangent wedge at eigenvalue one.

    A necessary condition for an n-state stochastic eigenvalue is
    |Im(lambda)| <= cot(pi/n) * (1 - Re(lambda)).
    """

    n = int(order)
    z = complex(value)
    if n < 2:
        return float(abs(z - 1.0))
    cotangent = 1.0 / tan(pi / n)
    numerator = abs(z.imag) + cotangent * (z.real - 1.0)
    return 0.0 if numerator <= 0.0 else float(numerator / sqrt(1.0 + cotangent**2))


@dataclass(frozen=True)
class StochasticOrderTest:
    order: int
    disk_radius: float
    analytic_wedge_distance: float
    excluded_analytically: bool
    numerical_distance_fine: float
    numerical_distance_coarse: float
    numerical_resolution_delta: float
    convergence_guarded_distance: float
    excluded_by_full_region_numerically: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "order": self.order,
            "disk_radius": self.disk_radius,
            "analytic_wedge_distance": self.analytic_wedge_distance,
            "excluded_analytically": self.excluded_analytically,
            "numerical_distance_fine": self.numerical_distance_fine,
            "numerical_distance_coarse": self.numerical_distance_coarse,
            "numerical_resolution_delta": self.numerical_resolution_delta,
            "convergence_guarded_distance": self.convergence_guarded_distance,
            "excluded_by_full_region_numerically": self.excluded_by_full_region_numerically,
        }


@dataclass(frozen=True)
class FiniteStateExclusionReport:
    point_estimate: complex
    confidence_disk_radius: float
    confidence_level: float
    hankel_rank_lower_bound: int
    maximum_order_tested: int
    analytic_excluded_through: int
    numerical_excluded_through: int
    analytic_classical_state_lower_bound: int
    numerical_classical_state_lower_bound: int
    tests: tuple[StochasticOrderTest, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "point_estimate": [self.point_estimate.real, self.point_estimate.imag],
            "confidence_disk_radius": self.confidence_disk_radius,
            "confidence_level": self.confidence_level,
            "hankel_rank_lower_bound": self.hankel_rank_lower_bound,
            "maximum_order_tested": self.maximum_order_tested,
            "analytic_excluded_through": self.analytic_excluded_through,
            "numerical_excluded_through": self.numerical_excluded_through,
            "analytic_classical_state_lower_bound": self.analytic_classical_state_lower_bound,
            "numerical_classical_state_lower_bound": self.numerical_classical_state_lower_bound,
            "tests": [test.to_dict() for test in self.tests],
            "interpretation": (
                "Any exact finite-state classical stochastic realization must have "
                "at least the reported number of hidden states, conditional on the "
                "declared interface, selected rank, and bootstrap confidence disk."
            ),
            "numerical_caveat": (
                "The analytic lower bound uses a rigorous necessary half-plane. "
                "The sharper full-region result uses floating-point Karpelevič "
                "boundary minimisation with a two-resolution convergence guard; "
                "it is not an interval-arithmetic proof."
            ),
        }


def exclude_finite_stochastic_orders(
    point_estimate: complex,
    confidence_disk_radius: float,
    *,
    confidence_level: float,
    hankel_rank_lower_bound: int,
    maximum_order: int = 30,
    coarse_points: int = 256,
    convergence_safety_factor: float = 6.0,
    absolute_numerical_guard: float = 2e-8,
) -> FiniteStateExclusionReport:
    """Test a complex confidence disk against nested stochastic regions."""

    if confidence_disk_radius < 0.0:
        raise ValueError("confidence_disk_radius must be non-negative")
    if hankel_rank_lower_bound < 1:
        raise ValueError("hankel rank lower bound must be positive")
    if maximum_order < 2:
        raise ValueError("maximum_order must be at least two")

    z = complex(point_estimate)
    tests: list[StochasticOrderTest] = []
    analytic_through = 1
    numerical_through = 1
    analytic_contiguous = True
    numerical_contiguous = True

    for order in range(2, maximum_order + 1):
        wedge = dmitriev_dynkin_wedge_distance(z, order)
        excluded_analytic = wedge > confidence_disk_radius
        if analytic_contiguous and excluded_analytic:
            analytic_through = order
        else:
            analytic_contiguous = False

        if karpelevich_contains(z, order):
            coarse_distance = fine_distance = delta = guarded = 0.0
            excluded_numerical = False
        else:
            coarse = distance_to_karpelevich_region(
                z,
                order,
                coarse_points=coarse_points,
            ).distance
            fine = distance_to_karpelevich_region(
                z,
                order,
                coarse_points=2 * coarse_points,
            ).distance
            coarse_distance = float(coarse)
            fine_distance = float(fine)
            delta = abs(fine_distance - coarse_distance)
            guarded = max(
                0.0,
                min(coarse_distance, fine_distance)
                - convergence_safety_factor * delta
                - absolute_numerical_guard,
            )
            excluded_numerical = guarded > confidence_disk_radius

        if numerical_contiguous and excluded_numerical:
            numerical_through = order
        else:
            numerical_contiguous = False

        tests.append(
            StochasticOrderTest(
                order=order,
                disk_radius=float(confidence_disk_radius),
                analytic_wedge_distance=float(wedge),
                excluded_analytically=bool(excluded_analytic),
                numerical_distance_fine=float(fine_distance),
                numerical_distance_coarse=float(coarse_distance),
                numerical_resolution_delta=float(delta),
                convergence_guarded_distance=float(guarded),
                excluded_by_full_region_numerically=bool(excluded_numerical),
            )
        )
        if karpelevich_contains(z, order):
            break

    return FiniteStateExclusionReport(
        point_estimate=z,
        confidence_disk_radius=float(confidence_disk_radius),
        confidence_level=float(confidence_level),
        hankel_rank_lower_bound=int(hankel_rank_lower_bound),
        maximum_order_tested=int(maximum_order),
        analytic_excluded_through=int(analytic_through),
        numerical_excluded_through=int(numerical_through),
        analytic_classical_state_lower_bound=max(
            int(hankel_rank_lower_bound), analytic_through + 1
        ),
        numerical_classical_state_lower_bound=max(
            int(hankel_rank_lower_bound), numerical_through + 1
        ),
        tests=tuple(tests),
    )


def boundary_points(order: int, angles: Iterable[float]) -> np.ndarray:
    return np.asarray(
        [_boundary_point(order, float(angle)) for angle in angles],
        dtype=complex,
    )
