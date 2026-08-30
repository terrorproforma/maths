#!/usr/bin/env python3
"""Exact algebraic checks for the explicit Geometric Unity Shiab substitute.

This verifier does four things without external packages:

1. Checks the form-degree typing of draft equation (9.3) in d=14.
2. Verifies exact Clifford identities selecting the commutator/Jordan
   contraction pattern that reproduces the Einstein tensor on the geometric
   Riemann-curvature subspace.
3. Builds a rational algebraic Weyl tensor and verifies that the selected
   contraction annihilates it.
4. Records the remaining source-level ambiguity: the full U(64,64)-adjoint
   extension, invariant-tensor normalisations, metric dependence, and
   boundary/adjoint domains are not fixed by these algebraic identities.

The calculation uses a small exact Cl(4) model because the Clifford identities
are dimension-independent. The d=14 representation dimensions are checked
separately by exact integer formulas.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Callable, Dict, List, Tuple

Multivector = Dict[int, Fraction]
Metric = List[int]
Tensor4 = Callable[[int, int, int, int], Fraction]


def blade_mul(a: int, b: int, metric: Metric) -> Tuple[int, Fraction]:
    """Multiply ordered Clifford basis blades represented by bit masks."""
    sign = 1
    n = len(metric)
    for i in range(n):
        if (a >> i) & 1:
            for j in range(n):
                if (b >> j) & 1 and i > j:
                    sign *= -1
    common = a & b
    for i in range(n):
        if (common >> i) & 1:
            sign *= metric[i]
    return a ^ b, Fraction(sign)


def mv_add(a: Multivector, b: Multivector) -> Multivector:
    out: defaultdict[int, Fraction] = defaultdict(Fraction)
    for key, value in a.items():
        out[key] += value
    for key, value in b.items():
        out[key] += value
    return {key: value for key, value in out.items() if value}


def mv_scale(a: Multivector, scalar: Fraction | int) -> Multivector:
    scalar = Fraction(scalar)
    return {key: value * scalar for key, value in a.items() if value * scalar}


def mv_mul(a: Multivector, b: Multivector, metric: Metric) -> Multivector:
    out: defaultdict[int, Fraction] = defaultdict(Fraction)
    for blade_a, coeff_a in a.items():
        for blade_b, coeff_b in b.items():
            blade, sign = blade_mul(blade_a, blade_b, metric)
            out[blade] += coeff_a * coeff_b * sign
    return {key: value for key, value in out.items() if value}


def commutator(a: Multivector, b: Multivector, metric: Metric) -> Multivector:
    return mv_add(mv_mul(a, b, metric), mv_scale(mv_mul(b, a, metric), -1))


def anticommutator(a: Multivector, b: Multivector, metric: Metric) -> Multivector:
    return mv_add(mv_mul(a, b, metric), mv_mul(b, a, metric))


def vector(index: int) -> Multivector:
    return {1 << index: Fraction(1)}


def gamma_upper(index: int, metric: Metric) -> Multivector:
    return mv_scale(vector(index), metric[index])


def gamma_bivector_lower(a: int, b: int, metric: Metric) -> Multivector:
    return mv_scale(commutator(vector(a), vector(b), metric), Fraction(1, 2))


def gamma_bivector_upper(a: int, b: int, metric: Metric) -> Multivector:
    return mv_scale(gamma_bivector_lower(a, b, metric), metric[a] * metric[b])


def metric_value(a: int, b: int, metric: Metric) -> Fraction:
    return Fraction(metric[a]) if a == b else Fraction(0)


def scalar_curvature(ricci: List[List[Fraction]], metric: Metric) -> Fraction:
    return sum(Fraction(metric[i]) * ricci[i][i] for i in range(len(metric)))


def riemann_from_ricci(
    a: int,
    b: int,
    c: int,
    d: int,
    ricci: List[List[Fraction]],
    metric: Metric,
) -> Fraction:
    """Ricci/scalar part of an algebraic Riemann tensor, with zero Weyl part."""
    n = len(metric)
    g = lambda i, j: metric_value(i, j, metric)
    scalar = scalar_curvature(ricci, metric)
    value = (
        g(a, c) * ricci[b][d]
        - g(a, d) * ricci[b][c]
        - g(b, c) * ricci[a][d]
        + g(b, d) * ricci[a][c]
    ) / Fraction(n - 2)
    value -= scalar * (
        g(a, c) * g(b, d) - g(a, d) * g(b, c)
    ) / Fraction((n - 1) * (n - 2))
    return value


def spin_curvature(
    c: int,
    d: int,
    riemann: Tensor4,
    metric: Metric,
) -> Multivector:
    """F_cd = (1/4) R_cd ab gamma^ab."""
    n = len(metric)
    out: Multivector = {}
    for a in range(n):
        for b in range(n):
            coefficient = riemann(c, d, a, b)
            if coefficient:
                out = mv_add(
                    out,
                    mv_scale(
                        gamma_bivector_upper(a, b, metric),
                        Fraction(1, 4) * coefficient,
                    ),
                )
    return out


def ricci_from_riemann(riemann: Tensor4, metric: Metric) -> List[List[Fraction]]:
    n = len(metric)
    ricci = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for b in range(n):
        for d in range(n):
            ricci[b][d] = sum(
                Fraction(metric[a]) * riemann(a, b, a, d)
                for a in range(n)
            )
    return ricci


def clifford_ricci_contraction(
    riemann: Tensor4,
    metric: Metric,
) -> List[Multivector]:
    """A_d = sum_c [gamma^c, F_cd]."""
    n = len(metric)
    result: List[Multivector] = []
    for d in range(n):
        component: Multivector = {}
        for c in range(n):
            component = mv_add(
                component,
                commutator(
                    gamma_upper(c, metric),
                    spin_curvature(c, d, riemann, metric),
                    metric,
                ),
            )
        result.append(component)
    return result


def clifford_scalar_contraction(
    riemann: Tensor4,
    metric: Metric,
) -> Multivector:
    """B = sum_cd {gamma^cd, F_cd}."""
    n = len(metric)
    result: Multivector = {}
    for c in range(n):
        for d in range(n):
            result = mv_add(
                result,
                anticommutator(
                    gamma_bivector_upper(c, d, metric),
                    spin_curvature(c, d, riemann, metric),
                    metric,
                ),
            )
    return result


def expected_ricci_clifford(
    ricci: List[List[Fraction]],
    metric: Metric,
) -> List[Multivector]:
    n = len(metric)
    expected: List[Multivector] = []
    for d in range(n):
        component: Multivector = {}
        for b in range(n):
            if ricci[d][b]:
                component = mv_add(
                    component,
                    mv_scale(gamma_upper(b, metric), ricci[d][b]),
                )
        expected.append(component)
    return expected


def expected_einstein_clifford(
    ricci: List[List[Fraction]],
    metric: Metric,
) -> List[Multivector]:
    n = len(metric)
    scalar = scalar_curvature(ricci, metric)
    expected: List[Multivector] = []
    for d in range(n):
        component: Multivector = {}
        for b in range(n):
            coefficient = ricci[d][b] - Fraction(1, 2) * scalar * metric_value(d, b, metric)
            if coefficient:
                component = mv_add(
                    component,
                    mv_scale(gamma_upper(b, metric), coefficient),
                )
        expected.append(component)
    return expected


def selected_einstein_contraction(
    riemann: Tensor4,
    metric: Metric,
) -> List[Multivector]:
    """Ricci commutator plus one-half scalar anticommutator.

    With the conventions used here:
        A_d = Ric_d^b gamma_b,
        B = -R 1,
    hence A_d + (1/2) B gamma_d is the Einstein tensor in Clifford form.
    """
    ricci_part = clifford_ricci_contraction(riemann, metric)
    scalar_part = clifford_scalar_contraction(riemann, metric)
    output: List[Multivector] = []
    for d, component in enumerate(ricci_part):
        correction = mv_scale(
            mv_mul(scalar_part, vector(d), metric),
            Fraction(1, 2),
        )
        output.append(mv_add(component, correction))
    return output


def pair_index_sign(
    a: int,
    b: int,
    pairs: List[Tuple[int, int]],
) -> Tuple[int | None, int]:
    if a == b:
        return None, 0
    if a < b:
        return pairs.index((a, b)), 1
    return pairs.index((b, a)), -1


def epsilon4(a: int, b: int, c: int, d: int) -> int:
    values = [a, b, c, d]
    if len(set(values)) < 4:
        return 0
    inversions = sum(
        values[i] > values[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


def build_exact_weyl_tensor(metric: Metric) -> Tensor4:
    """Construct a nonzero exact algebraic Weyl tensor in four dimensions."""
    n = len(metric)
    if n != 4:
        raise ValueError("the exact Weyl witness is implemented for n=4")
    pairs = list(combinations(range(n), 2))
    matrix = [[Fraction(0) for _ in pairs] for _ in pairs]
    for i in range(len(pairs)):
        for j in range(i, len(pairs)):
            value = Fraction(((i + 2) * (j + 3) + i - j) % 7 - 3)
            matrix[i][j] = matrix[j][i] = value

    def raw(a: int, b: int, c: int, d: int) -> Fraction:
        i, sign_i = pair_index_sign(a, b, pairs)
        j, sign_j = pair_index_sign(c, d, pairs)
        if sign_i == 0 or sign_j == 0 or i is None or j is None:
            return Fraction(0)
        return sign_i * sign_j * matrix[i][j]

    bianchi_defect = (
        raw(0, 1, 2, 3)
        + raw(0, 2, 3, 1)
        + raw(0, 3, 1, 2)
    )

    def algebraic(a: int, b: int, c: int, d: int) -> Fraction:
        return raw(a, b, c, d) - bianchi_defect * Fraction(
            epsilon4(a, b, c, d), 3
        )

    ricci = ricci_from_riemann(algebraic, metric)

    def weyl(a: int, b: int, c: int, d: int) -> Fraction:
        return algebraic(a, b, c, d) - riemann_from_ricci(
            a, b, c, d, ricci, metric
        )

    return weyl


def form_degree_checks(dimension: int = 14) -> dict:
    input_degree = 2
    star_input = dimension - input_degree
    ricci_like = 1 + star_input
    scalar_inner = 2 + star_input
    scalar_inner_star = dimension - scalar_inner
    scalar_outer = 1 + scalar_inner_star
    scalar_outer_star = dimension - scalar_outer
    return {
        "dimension": dimension,
        "input_degree": input_degree,
        "star_input_degree": star_input,
        "ricci_like_output_degree": ricci_like,
        "scalar_inner_degree": scalar_inner,
        "scalar_inner_star_degree": scalar_inner_star,
        "scalar_outer_degree": scalar_outer,
        "scalar_like_output_degree": scalar_outer_star,
        "target_degree": dimension - 1,
        "pass": ricci_like == dimension - 1 and scalar_outer_star == dimension - 1,
    }


def hodge_square_sign(dimension: int, timelike: int, degree: int) -> int:
    exponent = degree * (dimension - degree) + timelike
    return -1 if exponent % 2 else 1


def build_results() -> dict:
    metric: Metric = [1, 1, 1, 1]

    ricci_values = [
        [2, 1, 0, 0],
        [1, 3, 1, 0],
        [0, 1, 4, 2],
        [0, 0, 2, 5],
    ]
    ricci = [
        [Fraction(value) for value in row]
        for row in ricci_values
    ]

    def ricci_riemann(a: int, b: int, c: int, d: int) -> Fraction:
        return riemann_from_ricci(a, b, c, d, ricci, metric)

    scalar = scalar_curvature(ricci, metric)
    ricci_contraction = clifford_ricci_contraction(ricci_riemann, metric)
    scalar_contraction = clifford_scalar_contraction(ricci_riemann, metric)
    einstein_contraction = selected_einstein_contraction(ricci_riemann, metric)

    exact_weyl = build_exact_weyl_tensor(metric)
    weyl_ricci = ricci_from_riemann(exact_weyl, metric)
    weyl_ricci_contraction = clifford_ricci_contraction(exact_weyl, metric)
    weyl_scalar_contraction = clifford_scalar_contraction(exact_weyl, metric)
    weyl_einstein_contraction = selected_einstein_contraction(exact_weyl, metric)

    degree_checks = form_degree_checks(14)

    dimension = 14
    riemann_dimension = dimension**2 * (dimension**2 - 1) // 12
    weyl_dimension = (dimension + 2) * (dimension + 1) * dimension * (dimension - 3) // 12
    symmetric_two_dimension = dimension * (dimension + 1) // 2

    checks = {
        "equation_9_3_form_degrees_close_in_d14": degree_checks["pass"],
        "ricci_commutator_identity": ricci_contraction == expected_ricci_clifford(ricci, metric),
        "scalar_jordan_identity": scalar_contraction == {0: -scalar},
        "einstein_tensor_identity": einstein_contraction == expected_einstein_clifford(ricci, metric),
        "weyl_witness_is_ricci_free": all(
            value == 0 for row in weyl_ricci for value in row
        ),
        "weyl_annihilated_by_ricci_contraction": all(
            component == {} for component in weyl_ricci_contraction
        ),
        "weyl_annihilated_by_scalar_contraction": weyl_scalar_contraction == {},
        "weyl_annihilated_by_selected_einstein_map": all(
            component == {} for component in weyl_einstein_contraction
        ),
        "d14_riemann_decomposition_dimensions": (
            riemann_dimension == weyl_dimension + symmetric_two_dimension
        ),
        "d14_expected_einstein_rank": symmetric_two_dimension == 105,
        "d14_expected_weyl_kernel_dimension": weyl_dimension == 3080,
    }

    return {
        "schema_version": "1.0.0",
        "project": "TP-02 independent Geometric Unity reconstruction",
        "phase": "Phase 3B explicit Shiab typing and Clifford-Einstein selection",
        "source_targets": {
            "draft_equation": "Geometric Unity working draft v1.0, eq. (9.3), pp. 42-43",
            "oxford_page": "official 2013 Oxford lecture transcript and supplementary PowerPoint",
        },
        "degree_checks": degree_checks,
        "hodge_square_signs_signature_7_7": {
            "degree_2": hodge_square_sign(14, 7, 2),
            "degree_14": hodge_square_sign(14, 7, 14),
            "degree_1": hodge_square_sign(14, 7, 1),
        },
        "clifford_selection": {
            "ricci_operation": "commutator of gamma^c with spin curvature F_cd",
            "scalar_operation": "anticommutator/Jordan contraction of gamma^cd with F_cd",
            "outer_operation": "scalar multiplication of the gamma-valued one-form",
            "exact_identities": [
                "[gamma^c,F_cd] = Ric_d^b gamma_b",
                "{gamma^cd,F_cd} = -R 1",
                "E_d = [gamma^c,F_cd] + 1/2 {gamma^cd,F_cd} gamma_d = G_d^b gamma_b",
            ],
        },
        "dimension_14": {
            "algebraic_riemann": riemann_dimension,
            "weyl": weyl_dimension,
            "symmetric_two_tensors": symmetric_two_dimension,
            "expected_einstein_map_rank_on_riemann_subspace": symmetric_two_dimension,
            "expected_kernel_on_riemann_subspace": weyl_dimension,
        },
        "checks": checks,
        "all_pass": all(checks.values()),
        "source_completeness": {
            "explicit_substitute_typed_at_form_degree_level": True,
            "einstein_pattern_fixed_on_geometric_riemann_subspace": True,
            "unique_full_adjoint_extension": False,
            "unique_invariant_tensor_normalisation": False,
            "unique_metric_or_observation_derivative_of_phi_i": False,
            "unique_boundary_and_formal_adjoint_domain": False,
            "unique_full_hessian_or_principal_symbol": False,
        },
        "verdict": {
            "positive": "The explicit substitute can be typed and its Einstein contraction pattern is exactly reproducible on the geometric Riemann sector.",
            "negative": "The official sources still do not define a unique U(64,64)-adjoint extension or complete variational data, so no unique full spectrum follows.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    root = args.root.resolve()
    result = build_results()
    output = root / "results" / "shiab_einstein_pattern.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
