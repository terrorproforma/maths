"""Weighted Horner suspension and the explicit 15-variable map."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import sympy as sp

from .maps import BASE_VARIABLES, NORMALIZED_COLLISION_POINTS, normalized_map


@dataclass(frozen=True)
class HornerSuspension:
    base_variables: tuple[sp.Symbol, ...]
    base_map: tuple[sp.Expr, ...]
    component_degrees: tuple[int, ...]
    homogeneous_pieces: tuple[Mapping[int, sp.Expr], ...]
    auxiliary_variables: tuple[tuple[sp.Symbol, ...], ...]
    auxiliary_index: Mapping[tuple[int, int], int]
    prehomogeneous_variables: tuple[sp.Symbol, ...]
    prehomogeneous_nonlinear: tuple[sp.Expr, ...]
    h: sp.Symbol
    variables: tuple[sp.Symbol, ...]
    phi: tuple[sp.Expr, ...]
    h_map: tuple[sp.Expr, ...]
    degree: int


def homogeneous_component(
    expression: sp.Expr,
    variables: Sequence[sp.Symbol],
    degree: int,
) -> sp.Expr:
    poly = sp.Poly(sp.expand(expression), *variables)
    total = sp.Integer(0)
    for powers, coefficient in poly.terms():
        if sum(powers) == degree:
            monomial = sp.prod(variable**power for variable, power in zip(variables, powers, strict=True))
            total += coefficient * monomial
    return sp.expand(total)


def maximum_total_degree(expression: sp.Expr, variables: Sequence[sp.Symbol]) -> int:
    poly = sp.Poly(sp.expand(expression), *variables)
    return max((sum(powers) for powers, coefficient in poly.terms() if coefficient != 0), default=0)


def build_horner_suspension(
    base_variables: Sequence[sp.Symbol],
    mapping: Sequence[sp.Expr],
    auxiliary_prefixes: Sequence[str] | None = None,
    h_name: str = "h",
) -> HornerSuspension:
    """Construct the weighted Horner suspension from an identity-linear map.

    If G_i=X_i+sum_j K_{i,j}, the prehomogeneous nonlinear map N is

        N_{X_i}=K_{i,2}+Y_{i,3},
        N_{Y_{i,j}}=-K_{i,j}-Y_{i,j+1},
        N_{Y_{i,d_i}}=-K_{i,d_i}.

    One homogenizing variable turns every nonlinear term into degree d=max d_i.
    """

    base_variables = tuple(base_variables)
    mapping = tuple(map(sp.expand, mapping))
    if len(base_variables) != len(mapping):
        raise ValueError("The base variable and component counts must agree.")

    if auxiliary_prefixes is None:
        auxiliary_prefixes = tuple(f"u{i + 1}_" for i in range(len(mapping)))
    if len(auxiliary_prefixes) != len(mapping):
        raise ValueError("One auxiliary prefix is required per component.")

    pieces: list[dict[int, sp.Expr]] = []
    degrees: list[int] = []
    auxiliary_rows: list[tuple[sp.Symbol, ...]] = []

    for i, (variable, component) in enumerate(zip(base_variables, mapping, strict=True)):
        nonlinear = sp.expand(component - variable)
        degree = maximum_total_degree(nonlinear, base_variables)
        if degree < 2:
            raise ValueError("Every component must have a nonlinear term of degree at least two.")
        degrees.append(degree)
        pieces.append({j: homogeneous_component(nonlinear, base_variables, j) for j in range(2, degree + 1)})
        prefix = auxiliary_prefixes[i]
        auxiliary_rows.append(tuple(sp.Symbol(f"{prefix}{j}") for j in range(3, degree + 1)))

    flat_auxiliaries = tuple(variable for row in auxiliary_rows for variable in row)
    pre_variables = base_variables + flat_auxiliaries
    auxiliary_index: dict[tuple[int, int], int] = {}
    cursor = len(base_variables)
    for i, row in enumerate(auxiliary_rows):
        for j, _ in enumerate(row, start=3):
            auxiliary_index[(i, j)] = cursor
            cursor += 1

    nonlinear_components: list[sp.Expr] = []
    for i, degree in enumerate(degrees):
        first_aux = auxiliary_rows[i][0]
        nonlinear_components.append(sp.expand(pieces[i][2] + first_aux))

    for i, degree in enumerate(degrees):
        for j in range(3, degree + 1):
            current_piece = pieces[i][j]
            if j < degree:
                next_aux = pre_variables[auxiliary_index[(i, j + 1)]]
                nonlinear_components.append(sp.expand(-current_piece - next_aux))
            else:
                nonlinear_components.append(sp.expand(-current_piece))

    h = sp.Symbol(h_name)
    max_degree = max(degrees)
    substitution = {variable: variable / h for variable in pre_variables}
    homogeneous_nonlinear = tuple(
        sp.expand(h**max_degree * component.xreplace(substitution))
        for component in nonlinear_components
    )
    variables = pre_variables + (h,)
    phi = tuple(
        sp.expand(variable + component)
        for variable, component in zip(pre_variables, homogeneous_nonlinear, strict=True)
    ) + (h,)
    h_map = tuple(sp.expand(variable - image) for variable, image in zip(variables, phi, strict=True))

    return HornerSuspension(
        base_variables=base_variables,
        base_map=mapping,
        component_degrees=tuple(degrees),
        homogeneous_pieces=tuple(pieces),
        auxiliary_variables=tuple(auxiliary_rows),
        auxiliary_index=auxiliary_index,
        prehomogeneous_variables=pre_variables,
        prehomogeneous_nonlinear=tuple(nonlinear_components),
        h=h,
        variables=variables,
        phi=phi,
        h_map=h_map,
        degree=max_degree,
    )


def build_counterexample_suspension() -> HornerSuspension:
    return build_horner_suspension(
        BASE_VARIABLES,
        normalized_map(),
        auxiliary_prefixes=("a", "b", "c"),
        h_name="h",
    )


def telescoping_residuals(suspension: HornerSuspension) -> tuple[sp.Expr, ...]:
    """Check the weighted target shear against s^{-1}G(sX)."""

    s = sp.Symbol("s")
    u_outputs = tuple(
        sp.expand(variable + s * nonlinear)
        for variable, nonlinear in zip(
            suspension.prehomogeneous_variables,
            suspension.prehomogeneous_nonlinear,
            strict=True,
        )
    )
    scaled_base = {variable: s * variable for variable in suspension.base_variables}
    residuals: list[sp.Expr] = []

    for i, component in enumerate(suspension.base_map):
        lhs = u_outputs[i]
        for j in range(3, suspension.component_degrees[i] + 1):
            lhs -= s ** (j - 2) * u_outputs[suspension.auxiliary_index[(i, j)]]
        rhs = sp.expand(component.xreplace(scaled_base) / s)
        residuals.append(sp.expand(lhs - rhs))

    return tuple(residuals)


def auxiliary_jacobian(suspension: HornerSuspension) -> sp.Matrix:
    """Jacobian of the auxiliary U_s outputs with respect to auxiliary variables."""

    s = sp.Symbol("s")
    base_count = len(suspension.base_variables)
    auxiliary_variables = suspension.prehomogeneous_variables[base_count:]
    auxiliary_outputs = tuple(
        sp.expand(variable + s * nonlinear)
        for variable, nonlinear in zip(
            suspension.prehomogeneous_variables[base_count:],
            suspension.prehomogeneous_nonlinear[base_count:],
            strict=True,
        )
    )
    return sp.Matrix(auxiliary_outputs).jacobian(auxiliary_variables)


def lift_base_point(
    suspension: HornerSuspension,
    point: Sequence[sp.Expr],
) -> tuple[sp.Expr, ...]:
    substitutions = dict(zip(suspension.base_variables, point, strict=True))
    lifted: list[sp.Expr] = list(point)
    for i, degree in enumerate(suspension.component_degrees):
        for j in range(3, degree + 1):
            value = sum(
                suspension.homogeneous_pieces[i][ell]
                for ell in range(j, degree + 1)
            )
            lifted.append(sp.simplify(value.subs(substitutions)))
    lifted.append(sp.Integer(1))
    return tuple(lifted)


def evaluate(
    mapping: Sequence[sp.Expr],
    variables: Sequence[sp.Symbol],
    point: Sequence[sp.Expr],
) -> tuple[sp.Expr, ...]:
    substitutions = dict(zip(variables, point, strict=True))
    return tuple(sp.simplify(component.subs(substitutions)) for component in mapping)


def verify_counterexample_suspension() -> dict[str, object]:
    suspension = build_counterexample_suspension()
    assert len(suspension.variables) == 15
    assert suspension.degree == 7
    assert suspension.component_degrees == (4, 6, 7)
    assert telescoping_residuals(suspension) == (0, 0, 0)
    assert sp.factor(auxiliary_jacobian(suspension).det()) == 1

    for component in suspension.h_map[:-1]:
        poly = sp.Poly(component, *suspension.variables)
        assert {sum(powers) for powers, coefficient in poly.terms() if coefficient != 0} <= {7}

    lifted_points = tuple(lift_base_point(suspension, point) for point in NORMALIZED_COLLISION_POINTS)
    images = tuple(evaluate(suspension.phi, suspension.variables, point) for point in lifted_points)
    assert images[0] == images[1] == images[2]

    return {
        "dimension": len(suspension.variables),
        "degree": suspension.degree,
        "component_degrees": list(suspension.component_degrees),
        "telescoping_residuals": [str(value) for value in telescoping_residuals(suspension)],
        "auxiliary_block_determinant": str(sp.factor(auxiliary_jacobian(suspension).det())),
        "collision_count": len(images),
        "common_image": [str(value) for value in images[0]],
    }


def specialized_nilpotency_checks() -> dict[str, bool]:
    """Exact integer regression checks at two specializations.

    The proof of nilpotency is the symbolic telescoping/Cayley-Hamilton argument.
    These matrix-power checks protect the implementation from transcription errors.
    """

    suspension = build_counterexample_suspension()
    jn = sp.Matrix(suspension.prehomogeneous_nonlinear).jacobian(suspension.prehomogeneous_variables)
    jh = sp.Matrix(suspension.h_map).jacobian(suspension.variables)

    reports: dict[str, bool] = {}
    assignments_list = []
    for offset in (0, 3):
        pre_assignment = {
            variable: sp.Integer(((index + offset) % 5) - 2)
            for index, variable in enumerate(suspension.prehomogeneous_variables)
        }
        full_assignment = dict(pre_assignment)
        full_assignment[suspension.h] = sp.Integer(2 + offset)
        assignments_list.append((pre_assignment, full_assignment))

    for index, (pre_assignment, full_assignment) in enumerate(assignments_list, start=1):
        jn_value = jn.subs(pre_assignment)
        jh_value = jh.subs(full_assignment)
        reports[f"JN_specialization_{index}"] = jn_value**14 == sp.zeros(14)
        reports[f"JH_specialization_{index}"] = jh_value**15 == sp.zeros(15)

    assert all(reports.values())
    return reports
