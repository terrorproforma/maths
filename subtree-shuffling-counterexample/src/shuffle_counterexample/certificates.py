"""Closed formulas for the inverse coefficient and shuffle separator total."""

from __future__ import annotations

from math import comb, factorial

import sympy as sp


def gamma(m: int) -> int:
    """Coefficient [A^(2m+1) C^m] of the first component of G^{-1}."""

    if m < 0:
        raise ValueError("m must be nonnegative")
    return (-1) ** m * 2**m * comb(3 * m + 1, m)


def alpha_vector(m: int) -> tuple[int, ...]:
    """Leaf-type vector for the degree-seven, 15-variable inverse coefficient."""

    if m < 0:
        raise ValueError("m must be nonnegative")
    return (2 * m + 1, 0, m, *([0] * 11), 15 * m)


def separator_total(m: int) -> int:
    """Exact total sum of the tree separator w_m."""

    if m < 1:
        raise ValueError("The tree separator is indexed by m >= 1")
    return factorial(7) ** (3 * m) * gamma(m)


def internal_vertex_count(m: int) -> int:
    if m < 1:
        raise ValueError("m must be positive")
    return 3 * m


def leaf_count(m: int) -> int:
    return 18 * m + 1


def max_internal_vertices_without_path(d: int, p: int) -> int:
    """Maximum full d-ary internal count when no root-to-vertex path has length p."""

    if d < 2 or p < 1:
        raise ValueError("d >= 2 and p >= 1 are required")
    if p == 1:
        return 0
    return (d ** (p - 1) - 1) // (d - 1)


def first_fully_covered_k(d: int = 7, p: int = 15) -> int:
    return max_internal_vertices_without_path(d, p) + 1


def truncated_inverse_coefficient(max_m: int) -> dict[int, int]:
    """Cross-check gamma by formal fixed-point iteration in A.

    On the target plane B=0, the hidden coordinate satisfies
        r = A/(1+2 C r^2),
    and x = r/(1+6 C r^2).
    """

    if max_m < 0:
        raise ValueError("max_m must be nonnegative")
    a, c = sp.symbols("A C")
    order = 2 * max_m + 4
    r = a
    for _ in range(max_m + 4):
        r = sp.series(a / (1 + 2 * c * r**2), a, 0, order).removeO().expand()
    x_series = sp.series(r / (1 + 6 * c * r**2), a, 0, order).removeO().expand()
    return {
        m: int(sp.expand(x_series).coeff(a, 2 * m + 1).coeff(c, m))
        for m in range(max_m + 1)
    }


def verify_coefficient_formula(max_m: int = 5) -> dict[str, object]:
    direct = truncated_inverse_coefficient(max_m)
    expected = {m: gamma(m) for m in range(max_m + 1)}
    assert direct == expected

    for m in range(1, max_m + 1):
        alpha = alpha_vector(m)
        assert len(alpha) == 15
        assert sum(alpha) == leaf_count(m)
        assert leaf_count(m) == 6 * internal_vertex_count(m) + 1
        assert separator_total(m) != 0

    threshold = first_fully_covered_k()
    assert threshold == 113_037_178_809
    assert threshold % 3 == 0

    return {
        "checked_m": max_m,
        "coefficients": direct,
        "first_fully_covered_k": threshold,
        "first_fully_covered_m": threshold // 3,
    }
