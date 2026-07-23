"""The supplied three-variable map and its determinant-one normalization."""

from __future__ import annotations

from typing import Iterable, Sequence

import sympy as sp

x, y, z = sp.symbols("x y z")
BASE_VARIABLES = (x, y, z)

ORIGINAL_COLLISION_POINTS = (
    (sp.Rational(0), sp.Rational(0), sp.Rational(-1, 4)),
    (sp.Rational(1), sp.Rational(-3, 2), sp.Rational(13, 2)),
    (sp.Rational(-1), sp.Rational(3, 2), sp.Rational(13, 2)),
)
ORIGINAL_COMMON_IMAGE = (
    sp.Rational(-1, 4),
    sp.Rational(0),
    sp.Rational(0),
)

NORMALIZED_COLLISION_POINTS = (
    (sp.Rational(0), sp.Rational(0), sp.Rational(-1, 8)),
    (sp.Rational(1), sp.Rational(-3, 4), sp.Rational(13, 4)),
    (sp.Rational(-1), sp.Rational(3, 4), sp.Rational(13, 4)),
)
NORMALIZED_COMMON_IMAGE = (
    sp.Rational(0),
    sp.Rational(0),
    sp.Rational(-1, 8),
)


def original_map(variables: Sequence[sp.Symbol] = BASE_VARIABLES) -> tuple[sp.Expr, ...]:
    """Return the original map F=(P,Q,R)."""

    xx, yy, zz = variables
    u = 1 + xx * yy
    p = u**3 * zz + yy**2 * u * (4 + 3 * xx * yy)
    q = yy + 3 * xx * u**2 * zz + 3 * xx * yy**2 * (4 + 3 * xx * yy)
    r = 2 * xx - 3 * xx**2 * yy - xx**3 * zz
    return tuple(map(sp.expand, (p, q, r)))


def normalized_map(variables: Sequence[sp.Symbol] = BASE_VARIABLES) -> tuple[sp.Expr, ...]:
    """Return the identity-linear determinant-one normalization G=(A,B,C)."""

    xx, yy, zz = variables
    a = xx - 3 * xx**2 * yy - xx**3 * zz
    b = (
        yy
        + 3 * xx * zz
        + 24 * xx * yy**2
        + 12 * xx**2 * yy * zz
        + 36 * xx**2 * yy**3
        + 12 * xx**3 * yy**2 * zz
    )
    c = (
        zz
        + 8 * yy**2
        + 6 * xx * yy * zz
        + 28 * xx * yy**3
        + 12 * xx**2 * yy**2 * zz
        + 24 * xx**2 * yy**4
        + 8 * xx**3 * yy**3 * zz
    )
    return tuple(map(sp.expand, (a, b, c)))


def evaluate_map(
    mapping: Sequence[sp.Expr],
    point: Sequence[sp.Expr],
    variables: Sequence[sp.Symbol] = BASE_VARIABLES,
) -> tuple[sp.Expr, ...]:
    substitutions = dict(zip(variables, point, strict=True))
    return tuple(sp.simplify(component.subs(substitutions)) for component in mapping)


def jacobian_determinant(
    mapping: Sequence[sp.Expr],
    variables: Sequence[sp.Symbol] = BASE_VARIABLES,
) -> sp.Expr:
    return sp.factor(sp.Matrix(mapping).jacobian(variables).det())


def normalized_from_original() -> tuple[sp.Expr, ...]:
    """Apply the source and target transformations used in the manuscript."""

    p, q, r = original_map((x, 2 * y, 2 * z))
    return tuple(sp.expand(component) for component in (r / 2, q / 2, p / 2))


def hidden_identity_residuals() -> tuple[sp.Expr, sp.Expr]:
    """Return the two hidden-cubic residuals; both must simplify to zero."""

    a, b, c = normalized_map()
    u = 1 + 2 * x * y
    r = x / u
    first = sp.cancel(b - y - 3 * r * c)
    second = sp.cancel(a - r + r**2 * b - 2 * r**3 * c)
    return sp.factor(first), sp.factor(second)


def verify_three_variable_maps() -> dict[str, object]:
    """Run exact symbolic checks and return a serializable report."""

    f = original_map()
    g = normalized_map()

    det_f = jacobian_determinant(f)
    det_g = jacobian_determinant(g)
    assert det_f == -2
    assert det_g == 1
    assert all(sp.expand(lhs - rhs) == 0 for lhs, rhs in zip(g, normalized_from_original(), strict=True))

    original_images = tuple(evaluate_map(f, point) for point in ORIGINAL_COLLISION_POINTS)
    normalized_images = tuple(evaluate_map(g, point) for point in NORMALIZED_COLLISION_POINTS)
    assert all(image == ORIGINAL_COMMON_IMAGE for image in original_images)
    assert all(image == NORMALIZED_COMMON_IMAGE for image in normalized_images)

    residuals = hidden_identity_residuals()
    assert residuals == (0, 0)

    return {
        "original_jacobian": str(det_f),
        "normalized_jacobian": str(det_g),
        "original_collision_count": len(original_images),
        "normalized_collision_count": len(normalized_images),
        "hidden_identity_residuals": [str(value) for value in residuals],
    }
