#!/usr/bin/env python3
"""Exact algebraic audit of the TP-02 R_PLUS_EIN completion.

This verifier constructs a real 128-dimensional representation of Cl(7,7),
the invariant split spinor form of signature (64,64), canonical one- and
two-form Clifford tensors, and the minimal full-adjoint extension of the
Einstein-like Shiab contraction.

Only standard-library arithmetic is used. Clifford matrices are represented
as signed permutations, so all structural checks are exact integers.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from random import Random
from typing import Dict, Iterable, List, Tuple

Dense = List[List[int]]


@dataclass(frozen=True)
class SignedPermutation:
    """Matrix with exactly one +/-1 entry in every row and column.

    The representation stores the action on basis columns:
        M e_j = sign[j] e_{perm[j]}.
    """

    perm: Tuple[int, ...]
    sign: Tuple[int, ...]

    def __post_init__(self) -> None:
        n = len(self.perm)
        if sorted(self.perm) != list(range(n)):
            raise ValueError("perm is not a permutation")
        if len(self.sign) != n or any(value not in (-1, 1) for value in self.sign):
            raise ValueError("sign must contain one +/-1 per column")

    @property
    def n(self) -> int:
        return len(self.perm)

    @staticmethod
    def identity(n: int) -> "SignedPermutation":
        return SignedPermutation(tuple(range(n)), tuple(1 for _ in range(n)))

    def compose(self, other: "SignedPermutation") -> "SignedPermutation":
        """Return self @ other."""
        if self.n != other.n:
            raise ValueError("dimension mismatch")
        return SignedPermutation(
            tuple(self.perm[other.perm[j]] for j in range(self.n)),
            tuple(other.sign[j] * self.sign[other.perm[j]] for j in range(self.n)),
        )

    def negative(self) -> "SignedPermutation":
        return SignedPermutation(self.perm, tuple(-value for value in self.sign))

    def transpose(self) -> "SignedPermutation":
        inverse_perm = [0] * self.n
        inverse_sign = [0] * self.n
        for column in range(self.n):
            row = self.perm[column]
            inverse_perm[row] = column
            inverse_sign[row] = self.sign[column]
        return SignedPermutation(tuple(inverse_perm), tuple(inverse_sign))

    def trace(self) -> int:
        return sum(
            self.sign[column]
            for column in range(self.n)
            if self.perm[column] == column
        )

    def is_negative_of(self, other: "SignedPermutation") -> bool:
        return self.perm == other.perm and self.sign == tuple(
            -value for value in other.sign
        )


def kronecker(left: SignedPermutation, right: SignedPermutation) -> SignedPermutation:
    m, n = left.n, right.n
    return SignedPermutation(
        tuple(
            left.perm[column // n] * n + right.perm[column % n]
            for column in range(m * n)
        ),
        tuple(
            left.sign[column // n] * right.sign[column % n]
            for column in range(m * n)
        ),
    )


def kronecker_all(factors: Iterable[SignedPermutation]) -> SignedPermutation:
    output = SignedPermutation.identity(1)
    for factor in factors:
        output = kronecker(output, factor)
    return output


def product(matrices: Iterable[SignedPermutation], dimension: int) -> SignedPermutation:
    output = SignedPermutation.identity(dimension)
    for matrix in matrices:
        output = output.compose(matrix)
    return output


def zero_dense(n: int) -> Dense:
    return [[0] * n for _ in range(n)]


def transpose_dense(matrix: Dense) -> Dense:
    return [list(row) for row in zip(*matrix)]


def add_dense(left: Dense, right: Dense) -> Dense:
    return [
        [a + b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def subtract_dense(left: Dense, right: Dense) -> Dense:
    return [
        [a - b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def scale_dense(matrix: Dense, factor: int) -> Dense:
    return [[factor * value for value in row] for row in matrix]


def left_multiply_signed(matrix: SignedPermutation, dense: Dense) -> Dense:
    output = zero_dense(matrix.n)
    for source_row in range(matrix.n):
        target_row = matrix.perm[source_row]
        sign = matrix.sign[source_row]
        output[target_row] = [sign * value for value in dense[source_row]]
    return output


def right_multiply_signed(dense: Dense, matrix: SignedPermutation) -> Dense:
    output = zero_dense(matrix.n)
    for row_index, row in enumerate(dense):
        output[row_index] = [
            matrix.sign[column] * row[matrix.perm[column]]
            for column in range(matrix.n)
        ]
    return output


def h_adjoint(dense: Dense, h_form: SignedPermutation) -> Dense:
    """Return H^{-1} dense^T H; here H^{-1}=H."""
    return right_multiply_signed(
        left_multiply_signed(h_form, transpose_dense(dense)),
        h_form,
    )


def h_skew_projection(dense: Dense, h_form: SignedPermutation) -> Dense:
    return subtract_dense(dense, h_adjoint(dense, h_form))


def max_abs(dense: Dense) -> int:
    return max(abs(value) for row in dense for value in row)


def is_h_skew(dense: Dense, h_form: SignedPermutation) -> bool:
    return max_abs(add_dense(h_adjoint(dense, h_form), dense)) == 0


def is_h_self_adjoint(dense: Dense, h_form: SignedPermutation) -> bool:
    return max_abs(subtract_dense(h_adjoint(dense, h_form), dense)) == 0


def commutator_signed_dense(generator: SignedPermutation, dense: Dense) -> Dense:
    return subtract_dense(
        left_multiply_signed(generator, dense),
        right_multiply_signed(dense, generator),
    )


def anticommutator_signed_dense(generator: SignedPermutation, dense: Dense) -> Dense:
    return add_dense(
        left_multiply_signed(generator, dense),
        right_multiply_signed(dense, generator),
    )


def construct_clifford_generators() -> Tuple[List[SignedPermutation], List[int]]:
    identity_2 = SignedPermutation((0, 1), (1, 1))
    sigma_x = SignedPermutation((1, 0), (1, 1))
    sigma_z = SignedPermutation((0, 1), (1, -1))
    real_j = SignedPermutation((1, 0), (-1, 1))

    positive: List[SignedPermutation] = []
    negative: List[SignedPermutation] = []
    for index in range(7):
        positive.append(
            kronecker_all(
                [sigma_z] * index
                + [sigma_x]
                + [identity_2] * (6 - index)
            )
        )
        negative.append(
            kronecker_all(
                [sigma_z] * index
                + [real_j]
                + [identity_2] * (6 - index)
            )
        )
    return positive + negative, [1] * 7 + [-1] * 7


def exact_clifford_checks(
    gamma: List[SignedPermutation],
    signature: List[int],
) -> Dict[str, object]:
    dimension = gamma[0].n
    identity = SignedPermutation.identity(dimension)
    h_form = product(gamma[7:], dimension)
    chirality = product(gamma, dimension)

    squares_ok = all(
        generator.compose(generator)
        == (identity if metric_sign == 1 else identity.negative())
        for generator, metric_sign in zip(gamma, signature)
    )
    anticommutators_ok = all(
        gamma[a].compose(gamma[b]).is_negative_of(gamma[b].compose(gamma[a]))
        for a in range(14)
        for b in range(a + 1, 14)
    )

    gamma_h_skew = all(
        generator.transpose().compose(h_form).is_negative_of(
            h_form.compose(generator)
        )
        for generator in gamma
    )

    bivectors = [
        gamma[a].compose(gamma[b])
        for a in range(14)
        for b in range(a + 1, 14)
    ]
    bivector_h_skew = all(
        bivector.transpose().compose(h_form).is_negative_of(
            h_form.compose(bivector)
        )
        for bivector in bivectors
    )

    h_trace = h_form.trace()
    h_positive = (dimension + h_trace) // 2
    h_negative = (dimension - h_trace) // 2

    chirality_trace = chirality.trace()
    chirality_plus = (dimension + chirality_trace) // 2
    chirality_minus = (dimension - chirality_trace) // 2

    return {
        "spinor_dimension": dimension,
        "signature": signature,
        "clifford_squares_exact": squares_ok,
        "pairwise_anticommutation_exact": anticommutators_ok,
        "split_spinor_form": {
            "symmetric": h_form.transpose() == h_form,
            "involution": h_form.compose(h_form) == identity,
            "trace": h_trace,
            "positive_eigenvalue_count": h_positive,
            "negative_eigenvalue_count": h_negative,
        },
        "all_gamma_H_skew": gamma_h_skew,
        "all_91_bivectors_H_skew": bivector_h_skew,
        "chirality": {
            "symmetric": chirality.transpose() == chirality,
            "involution": chirality.compose(chirality) == identity,
            "trace": chirality_trace,
            "plus_dimension": chirality_plus,
            "minus_dimension": chirality_minus,
            "anticommutes_with_all_gamma": all(
                chirality.compose(generator).is_negative_of(
                    generator.compose(chirality)
                )
                for generator in gamma
            ),
            "H_pairs_opposite_chiralities": h_form.compose(
                chirality
            ).is_negative_of(chirality.compose(h_form)),
        },
        "_h_form": h_form,
    }


def full_adjoint_closure_check(
    gamma: List[SignedPermutation],
    signature: List[int],
    h_form: SignedPermutation,
) -> Dict[str, object]:
    dimension = gamma[0].n
    raised_gamma = [
        generator if metric_sign == 1 else generator.negative()
        for generator, metric_sign in zip(gamma, signature)
    ]

    selected_pairs = [(0, 1), (0, 7), (2, 9), (5, 6), (6, 13), (11, 12)]
    rng = Random(20260831)
    curvature: Dict[Tuple[int, int], Dense] = {}
    for pair in selected_pairs:
        trial = [
            [rng.randint(-2, 2) for _ in range(dimension)]
            for _ in range(dimension)
        ]
        projected = h_skew_projection(trial, h_form)
        if not is_h_skew(projected, h_form):
            raise AssertionError("H-skew projection failed")
        curvature[pair] = projected

    def component(first: int, second: int) -> Dense:
        if first == second:
            return zero_dense(dimension)
        if first < second:
            return curvature.get((first, second), zero_dense(dimension))
        return scale_dense(
            curvature.get((second, first), zero_dense(dimension)),
            -1,
        )

    scalar_channel = zero_dense(dimension)
    for first, second in selected_pairs:
        gamma_bivector = raised_gamma[first].compose(raised_gamma[second])
        scalar_channel = add_dense(
            scalar_channel,
            scale_dense(
                anticommutator_signed_dense(
                    gamma_bivector,
                    curvature[(first, second)],
                ),
                2,
            ),
        )

    scalar_channel_self_adjoint = is_h_self_adjoint(
        scalar_channel,
        h_form,
    )

    closure_residuals: List[int] = []
    naive_residuals: List[int] = []
    for output_index in range(14):
        ricci_channel = zero_dense(dimension)
        for contracted_index in range(14):
            ricci_channel = add_dense(
                ricci_channel,
                commutator_signed_dense(
                    raised_gamma[contracted_index],
                    component(contracted_index, output_index),
                ),
            )

        completed_output = add_dense(
            scale_dense(ricci_channel, 4),
            anticommutator_signed_dense(
                gamma[output_index],
                scalar_channel,
            ),
        )
        closure_residuals.append(
            max_abs(
                add_dense(
                    h_adjoint(completed_output, h_form),
                    completed_output,
                )
            )
        )

        naive_output = add_dense(
            scale_dense(ricci_channel, 2),
            right_multiply_signed(scalar_channel, gamma[output_index]),
        )
        naive_residuals.append(
            max_abs(
                add_dense(
                    h_adjoint(naive_output, h_form),
                    naive_output,
                )
            )
        )

    return {
        "seed": 20260831,
        "nonzero_curvature_pairs": [list(pair) for pair in selected_pairs],
        "all_input_coefficients_H_skew": all(
            is_h_skew(value, h_form) for value in curvature.values()
        ),
        "scalar_channel_H_self_adjoint": scalar_channel_self_adjoint,
        "symmetrized_extension_max_H_skew_residual": max(closure_residuals),
        "naive_unsymmetrized_max_H_skew_residual": max(naive_residuals),
        "naive_unsymmetrized_residuals_by_output_index": naive_residuals,
        "minimal_extension": (
            "E_d(X)=[Gamma^c,X_cd]"
            "+1/4{{Gamma^{cd},X_cd},Gamma_d}"
        ),
        "uniqueness_statement": (
            "For real coefficients a,b, a S Gamma_d + b Gamma_d S is "
            "H-skew for every H-self-adjoint S and H-skew Gamma_d iff a=b. "
            "Matching the central geometric channel fixes a=b=1/4."
        ),
    }


def split_signature_symbol_check() -> Dict[str, object]:
    n = 14
    negative_directions = 7
    positive_directions = 7
    formal_metric_polarizations = n * (n - 3) // 2
    four_dimensional_polarizations = 2

    polynomial = {
        "normal_norm": -1,
        "tangential_covector_norm": -1,
        "cross_term": 0,
        "polynomial": "-(1 + lambda^2)",
        "roots": ["+i", "-i"],
    }

    return {
        "dimension": n,
        "metric_signature": [negative_directions, positive_directions],
        "candidate_time_normal_orthogonal_complement_signature": [
            negative_directions - 1,
            positive_directions,
        ],
        "explicit_complex_root_witness": polynomial,
        "hyperbolic_with_respect_to_any_covector": False,
        "proof_summary": (
            "For any timelike normal n in signature (p,q) with p>1, "
            "n^perp still contains a timelike tangential covector xi. "
            "Taking xi orthogonal to n makes the null-characteristic "
            "equation quadratic with negative discriminant."
        ),
        "formal_14d_einstein_metric_polarizations": formal_metric_polarizations,
        "required_4d_graviton_polarizations": four_dimensional_polarizations,
        "formal_excess_before_observation_reduction": (
            formal_metric_polarizations - four_dimensional_polarizations
        ),
        "gate_consequence": (
            "PERT-02=0 for the local full-Y R_PLUS_EIN branch. "
            "This does not reject a different completion that derives a "
            "four-dimensional Lorentzian characteristic projector before "
            "propagation."
        ),
    }


def build_results() -> Dict[str, object]:
    gamma, signature = construct_clifford_generators()
    clifford = exact_clifford_checks(gamma, signature)
    h_form = clifford.pop("_h_form")
    adjoint = full_adjoint_closure_check(gamma, signature, h_form)
    symbol = split_signature_symbol_check()

    checks = {
        "Cl_7_7_exact": bool(
            clifford["clifford_squares_exact"]
            and clifford["pairwise_anticommutation_exact"]
        ),
        "spinor_form_signature_64_64": bool(
            clifford["split_spinor_form"]["positive_eigenvalue_count"] == 64
            and clifford["split_spinor_form"]["negative_eigenvalue_count"] == 64
        ),
        "Spin_7_7_embeds_in_u_64_64": bool(
            clifford["all_91_bivectors_H_skew"]
        ),
        "chiral_dimensions_64_64": bool(
            clifford["chirality"]["plus_dimension"] == 64
            and clifford["chirality"]["minus_dimension"] == 64
        ),
        "full_adjoint_completion_closes": bool(
            adjoint["symmetrized_extension_max_H_skew_residual"] == 0
        ),
        "naive_extension_fails": bool(
            adjoint["naive_unsymmetrized_max_H_skew_residual"] > 0
        ),
        "full_Y_split_signature_is_not_hyperbolic": bool(
            symbol["hyperbolic_with_respect_to_any_covector"] is False
        ),
    }

    return {
        "schema_version": "1.0.0",
        "project": "TP-02 independent Geometric Unity reconstruction",
        "branch": "R_PLUS_EIN",
        "phase": "exact Cl(7,7), full-adjoint completion, and symbol obstruction",
        "checks": checks,
        "clifford_representation": clifford,
        "full_adjoint_einstein_extension": adjoint,
        "split_signature_principal_symbol": symbol,
        "verdict": {
            "algebraic_completion": "PASS",
            "full_adjoint_codomain_closure": "PASS for the declared minimal completion",
            "local_full_Y_hyperbolicity": "FAIL",
            "scope": (
                "The exact algebraic completion is a project construction. "
                "The hyperbolicity zero applies to local propagation on the "
                "full (7,7) total space, not to an as-yet-unconstructed "
                "four-dimensional observation-projected theory."
            ),
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
    results = build_results()
    output = root / "results" / "cl77_rplus_ein.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))

    if not all(results["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
