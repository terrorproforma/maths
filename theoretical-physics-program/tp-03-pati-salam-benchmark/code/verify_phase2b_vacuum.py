#!/usr/bin/env python3
"""Verify the TP-03 Phase 2B Pati--Salam vacuum and threshold spectrum.

The active high-scale branch is PS1-MM.  It keeps the full PS1 field content
but chooses an explicitly declared, bounded moment-map potential for
Delta_R ~ (10,1,3), while Phi1 and Phi15 are inert positive-mass spectators
at the Pati--Salam breaking scale.

All reported Hessian eigenvalues are obtained both from the analytic
multiplet formulas and from an independently assembled 60x60 real Hessian.
The gauge-boson mass matrix is assembled from explicit SU(4) and SU(2)
generators.  No random fitted data are used.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import numpy as np


def su_n_generators(n: int) -> List[np.ndarray]:
    """Hermitian fundamental generators with tr(T_a T_b)=delta_ab/2."""
    generators: List[np.ndarray] = []
    for i in range(n):
        for j in range(i + 1, n):
            symmetric = np.zeros((n, n), dtype=np.complex128)
            symmetric[i, j] = symmetric[j, i] = 0.5
            generators.append(symmetric)

            antisymmetric = np.zeros((n, n), dtype=np.complex128)
            antisymmetric[i, j] = -0.5j
            antisymmetric[j, i] = 0.5j
            generators.append(antisymmetric)

    for k in range(1, n):
        diagonal = np.zeros((n, n), dtype=np.complex128)
        diagonal[np.arange(k), np.arange(k)] = 1.0
        diagonal[k, k] = -float(k)
        diagonal *= 1.0 / math.sqrt(2.0 * k * (k + 1.0))
        generators.append(diagonal)

    gram = np.array(
        [[np.trace(left @ right).real for right in generators] for left in generators]
    )
    if np.max(np.abs(gram - 0.5 * np.eye(n * n - 1))) > 1.0e-12:
        raise ArithmeticError("generator normalization failed")
    return generators


def symmetric_tensor_basis(n: int) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
    """Orthonormal embedding Sym^2(C^n) -> C^n tensor C^n."""
    columns: List[np.ndarray] = []
    pairs: List[Tuple[int, int]] = []
    for i in range(n):
        for j in range(i, n):
            vector = np.zeros(n * n, dtype=np.complex128)
            if i == j:
                vector[i * n + j] = 1.0
            else:
                vector[i * n + j] = 1.0 / math.sqrt(2.0)
                vector[j * n + i] = 1.0 / math.sqrt(2.0)
            columns.append(vector)
            pairs.append((i, j))
    embedding = np.stack(columns, axis=1)
    if np.max(np.abs(embedding.conj().T @ embedding - np.eye(len(columns)))) > 1.0e-12:
        raise ArithmeticError("symmetric-tensor basis is not orthonormal")
    return embedding, pairs


def symmetric_representation_generator(
    fundamental_generator: np.ndarray,
    embedding: np.ndarray,
    n: int,
) -> np.ndarray:
    full = np.kron(fundamental_generator, np.eye(n)) + np.kron(
        np.eye(n), fundamental_generator
    )
    return embedding.conj().T @ full @ embedding


def realify_hermitian(matrix: np.ndarray) -> np.ndarray:
    """Real symmetric matrix A_R with z†Az=(1/2)q^T A_R q."""
    return np.block(
        [
            [matrix.real, -matrix.imag],
            [matrix.imag, matrix.real],
        ]
    )


def build_representation() -> Dict[str, object]:
    su4_fundamental = su_n_generators(4)
    su2_fundamental = su_n_generators(2)
    u4, pairs4 = symmetric_tensor_basis(4)
    u2, pairs2 = symmetric_tensor_basis(2)

    su4_10 = [
        symmetric_representation_generator(generator, u4, 4)
        for generator in su4_fundamental
    ]
    su2_3 = [
        symmetric_representation_generator(generator, u2, 2)
        for generator in su2_fundamental
    ]

    total_su4 = [np.kron(generator, np.eye(3)) for generator in su4_10]
    total_su2r = [np.kron(np.eye(10), generator) for generator in su2_3]

    su4_singlet_index = pairs4.index((3, 3))
    su2_highest_index = pairs2.index((0, 0))
    vacuum_index = su4_singlet_index * 3 + su2_highest_index
    highest = np.zeros(30, dtype=np.complex128)
    highest[vacuum_index] = 1.0

    return {
        "su4_generators": total_su4,
        "su2r_generators": total_su2r,
        "pairs4": pairs4,
        "pairs2": pairs2,
        "vacuum_index": vacuum_index,
        "highest": highest,
    }


REPRESENTATION = build_representation()


def moment_maps(vector: np.ndarray) -> Tuple[float, float, float]:
    su4 = REPRESENTATION["su4_generators"]
    su2r = REPRESENTATION["su2r_generators"]
    assert isinstance(su4, list) and isinstance(su2r, list)
    norm = float(np.vdot(vector, vector).real)
    mu4 = np.array([np.vdot(vector, generator @ vector).real for generator in su4])
    mur = np.array([np.vdot(vector, generator @ vector).real for generator in su2r])
    return norm, float(mu4 @ mu4), float(mur @ mur)


def analytic_scalar_spectrum(
    lambda_delta: float,
    kappa4: float,
    kappa_r: float,
    v_r: float,
    m_phi1_sq: float,
    m_phi15_sq: float,
) -> List[Tuple[str, int, float]]:
    lambda_eff = lambda_delta - 1.5 * kappa4 - kappa_r
    return [
        ("Goldstones", 9, 0.0),
        ("(6,1)_{4/3}", 12, 2.0 * kappa4 * v_r**2),
        ("(6,1)_{1/3}", 12, (2.0 * kappa4 + kappa_r) * v_r**2),
        ("(6,1)_{-2/3}", 12, (2.0 * kappa4 + 2.0 * kappa_r) * v_r**2),
        ("(3,1)_{-1/3}", 6, (kappa4 + kappa_r) * v_r**2),
        ("(3,1)_{-4/3}", 6, (kappa4 + 2.0 * kappa_r) * v_r**2),
        ("(1,1)_{-2}", 2, 2.0 * kappa_r * v_r**2),
        ("Delta radial (1,1)_0", 1, 2.0 * lambda_eff * v_r**2),
        ("Phi1 spectator real modes", 8, m_phi1_sq),
        ("Phi15 spectator real modes", 120, m_phi15_sq),
    ]


def delta_real_hessian(
    lambda_delta: float,
    kappa4: float,
    kappa_r: float,
    v_r: float,
) -> np.ndarray:
    """Assemble the canonical 60x60 Hessian at Delta=v_r/sqrt(2)|44,+1>."""
    lambda_eff = lambda_delta - 1.5 * kappa4 - kappa_r
    mass_parameter_sq = lambda_eff * v_r**2

    vacuum_index = int(REPRESENTATION["vacuum_index"])
    q = np.zeros(60)
    q[vacuum_index] = v_r

    matrices4 = [
        realify_hermitian(generator)
        for generator in REPRESENTATION["su4_generators"]  # type: ignore[index]
    ]
    matrices_r = [
        realify_hermitian(generator)
        for generator in REPRESENTATION["su2r_generators"]  # type: ignore[index]
    ]

    q_norm_sq = float(q @ q)
    hessian = (
        -mass_parameter_sq * np.eye(60)
        + lambda_delta
        * (q_norm_sq * np.eye(60) + 2.0 * np.outer(q, q))
    )

    for coupling, matrices in ((kappa4, matrices4), (kappa_r, matrices_r)):
        for matrix in matrices:
            aq = matrix @ q
            moment = float(q @ aq)
            hessian -= coupling * (
                2.0 * np.outer(aq, aq) + moment * matrix
            )
    return 0.5 * (hessian + hessian.T)


def expected_delta_eigenvalues(
    lambda_delta: float,
    kappa4: float,
    kappa_r: float,
    v_r: float,
) -> List[float]:
    lambda_eff = lambda_delta - 1.5 * kappa4 - kappa_r
    values: List[float] = []
    for multiplicity, value in (
        (9, 0.0),
        (12, 2.0 * kappa4 * v_r**2),
        (12, (2.0 * kappa4 + kappa_r) * v_r**2),
        (12, (2.0 * kappa4 + 2.0 * kappa_r) * v_r**2),
        (6, (kappa4 + kappa_r) * v_r**2),
        (6, (kappa4 + 2.0 * kappa_r) * v_r**2),
        (2, 2.0 * kappa_r * v_r**2),
        (1, 2.0 * lambda_eff * v_r**2),
    ):
        values.extend([value] * multiplicity)
    return sorted(values)


def gauge_mass_matrix(g4: float, g_r: float, v_r: float) -> np.ndarray:
    generators = (
        REPRESENTATION["su4_generators"] + REPRESENTATION["su2r_generators"]  # type: ignore[operator]
    )
    couplings = [g4] * 15 + [g_r] * 3
    highest = REPRESENTATION["highest"]
    assert isinstance(highest, np.ndarray)
    vacuum = (v_r / math.sqrt(2.0)) * highest

    matrix = np.zeros((18, 18))
    for a, generator_a in enumerate(generators):
        for b, generator_b in enumerate(generators):
            anticommutator = generator_a @ generator_b + generator_b @ generator_a
            matrix[a, b] = (
                couplings[a]
                * couplings[b]
                * np.vdot(vacuum, anticommutator @ vacuum).real
            )
    return 0.5 * (matrix + matrix.T)


def broken_gauge_directions(v_r: float) -> np.ndarray:
    """Return the real tangent vectors generated by all 18 SU4xSU2R generators."""
    generators = (
        REPRESENTATION["su4_generators"] + REPRESENTATION["su2r_generators"]  # type: ignore[operator]
    )
    highest = REPRESENTATION["highest"]
    assert isinstance(highest, np.ndarray)
    vacuum = (v_r / math.sqrt(2.0)) * highest
    columns = []
    for generator in generators:
        delta = 1j * generator @ vacuum
        columns.append(
            np.concatenate(
                [math.sqrt(2.0) * delta.real, math.sqrt(2.0) * delta.imag]
            )
        )
    return np.stack(columns, axis=1)


def random_moment_map_scan(samples: int = 20000, seed: int = 20260831) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    max4 = 0.0
    maxr = 0.0
    max_combined = 0.0
    for _ in range(samples):
        vector = rng.normal(size=30) + 1j * rng.normal(size=30)
        vector /= np.linalg.norm(vector)
        norm, mu4_sq, mur_sq = moment_maps(vector)
        max4 = max(max4, mu4_sq / norm**2)
        maxr = max(maxr, mur_sq / norm**2)
        max_combined = max(max_combined, mu4_sq / 1.5 + mur_sq)
    return {
        "samples": samples,
        "seed": seed,
        "max_mu4_sq_over_norm4": max4,
        "analytic_bound_mu4": 1.5,
        "max_muR_sq_over_norm4": maxr,
        "analytic_bound_muR": 1.0,
        "max_normalized_combined_diagnostic": max_combined,
    }


def cluster_eigenvalues(values: Sequence[float], tolerance: float = 1.0e-9) -> List[Dict[str, float]]:
    sorted_values = sorted(float(value) for value in values)
    clusters: List[Dict[str, float]] = []
    for value in sorted_values:
        if not clusters or abs(value - clusters[-1]["value"]) > tolerance:
            clusters.append({"value": value, "multiplicity": 1})
        else:
            clusters[-1]["multiplicity"] += 1
    return clusters


def build_results() -> Dict[str, object]:
    benchmark = {
        "v_R": 1.0,
        "lambda_Delta": 2.0,
        "kappa_4": 0.4,
        "kappa_R": 0.3,
        "m_Phi1_sq": 2.2,
        "m_Phi15_sq": 3.3,
        "g_4": 0.570,
        "g_R": 0.540,
    }
    v_r = benchmark["v_R"]
    lambda_delta = benchmark["lambda_Delta"]
    kappa4 = benchmark["kappa_4"]
    kappa_r = benchmark["kappa_R"]
    lambda_eff = lambda_delta - 1.5 * kappa4 - kappa_r

    highest = REPRESENTATION["highest"]
    assert isinstance(highest, np.ndarray)
    norm, mu4_sq, mur_sq = moment_maps(highest)

    hessian = delta_real_hessian(lambda_delta, kappa4, kappa_r, v_r)
    numerical_eigenvalues = np.linalg.eigvalsh(hessian)
    expected_eigenvalues = np.array(
        expected_delta_eigenvalues(lambda_delta, kappa4, kappa_r, v_r)
    )

    gauge_matrix = gauge_mass_matrix(benchmark["g_4"], benchmark["g_R"], v_r)
    gauge_eigenvalues = np.linalg.eigvalsh(gauge_matrix)
    expected_gauge = sorted(
        [0.0] * 9
        + [0.5 * benchmark["g_4"] ** 2 * v_r**2] * 6
        + [0.5 * benchmark["g_R"] ** 2 * v_r**2] * 2
        + [
            (
                1.5 * benchmark["g_4"] ** 2
                + benchmark["g_R"] ** 2
            )
            * v_r**2
        ]
    )

    broken = broken_gauge_directions(v_r)
    broken_rank = int(np.linalg.matrix_rank(broken, tol=1.0e-10))
    goldstone_residual = float(np.max(np.abs(hessian @ broken)))

    physical_spectrum = analytic_scalar_spectrum(
        lambda_delta,
        kappa4,
        kappa_r,
        v_r,
        benchmark["m_Phi1_sq"],
        benchmark["m_Phi15_sq"],
    )
    physical_positive = [
        mass_sq
        for label, multiplicity, mass_sq in physical_spectrum
        if label != "Goldstones"
        for _ in range(multiplicity)
    ]

    # The declared PS1-MM benchmark is block diagonal at the high scale:
    # the exact Delta_R Hessian plus positive spectator blocks for the two
    # complex bidoublets.  Construct the actual 188x188 real matrix rather
    # than inferring the final count only from a ledger.
    full_hessian = np.zeros((188, 188))
    full_hessian[:60, :60] = hessian
    full_hessian[60:68, 60:68] = benchmark["m_Phi1_sq"] * np.eye(8)
    full_hessian[68:, 68:] = benchmark["m_Phi15_sq"] * np.eye(120)
    full_eigenvalues = np.linalg.eigvalsh(full_hessian)
    expected_full_eigenvalues = np.array(
        sorted(
            expected_delta_eigenvalues(lambda_delta, kappa4, kappa_r, v_r)
            + [benchmark["m_Phi1_sq"]] * 8
            + [benchmark["m_Phi15_sq"]] * 120
        )
    )

    checks = {
        "highest_weight_norm": abs(norm - 1.0) < 1.0e-12,
        "su4_moment_map_bound_saturated": abs(mu4_sq - 1.5) < 1.0e-12,
        "su2r_moment_map_bound_saturated": abs(mur_sq - 1.0) < 1.0e-12,
        "boundedness_condition": lambda_eff > 0.0 and kappa4 > 0.0 and kappa_r > 0.0,
        "delta_hessian_matches_analytic_spectrum": (
            float(np.max(np.abs(numerical_eigenvalues - expected_eigenvalues))) < 1.0e-10
        ),
        "goldstone_count_is_nine": int(np.sum(np.abs(numerical_eigenvalues) < 1.0e-10)) == 9,
        "broken_generator_rank_is_nine": broken_rank == 9,
        "goldstone_subspace_matches_broken_orbit": goldstone_residual < 1.0e-10,
        "all_physical_scalar_masses_positive": min(physical_positive) > 0.0,
        "full_scalar_hessian_shape_is_188": full_hessian.shape == (188, 188),
        "full_scalar_hessian_matches_analytic_spectrum": (
            float(np.max(np.abs(full_eigenvalues - expected_full_eigenvalues))) < 1.0e-10
        ),
        "full_scalar_hessian_has_nine_goldstones": int(
            np.sum(np.abs(full_eigenvalues) < 1.0e-10)
        ) == 9,
        "full_scalar_hessian_has_179_positive_modes": int(
            np.sum(full_eigenvalues > 1.0e-10)
        ) == 179,
        "gauge_mass_matrix_matches_analytic_spectrum": (
            float(np.max(np.abs(gauge_eigenvalues - np.array(expected_gauge)))) < 1.0e-10
        ),
        "massless_gauge_count_su4_su2r_is_nine": int(
            np.sum(np.abs(gauge_eigenvalues) < 1.0e-10)
        )
        == 9,
        "total_real_scalar_count": sum(multiplicity for _, multiplicity, _ in physical_spectrum)
        == 188,
        "total_physical_scalar_count": (
            sum(multiplicity for _, multiplicity, _ in physical_spectrum) - 9
        )
        == 179,
    }

    random_scan = random_moment_map_scan()

    return {
        "schema_version": "1.0.0",
        "project": "TP-03 Pati-Salam benchmark",
        "phase": "2B scalar invariant and vacuum audit",
        "branch": "PS1-MM",
        "field_content": {
            "Phi1": "(1,2,2), independent complex scalar, 8 real components",
            "Phi15": "(15,2,2), independent complex scalar, 120 real components",
            "DeltaR": "(10,1,3), independent complex scalar, 60 real components",
            "total_real_components": 188,
        },
        "delta_potential": (
            "V=-m_Delta^2 r + lambda_Delta r^2 "
            "-kappa_4 sum_A(mu_4^A)^2 -kappa_R sum_i(mu_R^i)^2"
        ),
        "analytic_global_bound": (
            "sum_A(mu_4^A)^2 <= (3/2) r^2 and "
            "sum_i(mu_R^i)^2 <= r^2; equality is simultaneous on the "
            "highest-weight coherent orbit."
        ),
        "boundedness_and_global_minimum": {
            "conditions": [
                "kappa_4 > 0",
                "kappa_R > 0",
                "lambda_eff=lambda_Delta-(3/2)kappa_4-kappa_R > 0",
                "m_Delta^2 > 0",
            ],
            "vacuum_norm": "r=v_R^2/2=m_Delta^2/(2 lambda_eff)",
            "unbroken_group": "SU(3)_C x SU(2)_L x U(1)_Y",
            "deeper_colour_or_charge_breaking_minimum": False,
        },
        "benchmark": benchmark,
        "lambda_eff": lambda_eff,
        "delta_hessian_clusters": cluster_eigenvalues(numerical_eigenvalues),
        "full_scalar_hessian_shape": list(full_hessian.shape),
        "full_scalar_hessian_clusters": cluster_eigenvalues(full_eigenvalues),
        "minimum_positive_scalar_mass_sq": float(
            np.min(full_eigenvalues[full_eigenvalues > 1.0e-10])
        ),
        "analytic_scalar_spectrum": [
            {"label": label, "real_multiplicity": multiplicity, "mass_sq": mass_sq}
            for label, multiplicity, mass_sq in physical_spectrum
        ],
        "gauge_hessian_clusters_su4_su2r": cluster_eigenvalues(gauge_eigenvalues),
        "analytic_gauge_spectrum": {
            "massless_SU3_plus_hypercharge": 9,
            "X_vector_leptoquarks": {
                "multiplicity_real_vectors": 6,
                "mass_sq": 0.5 * benchmark["g_4"] ** 2 * v_r**2,
            },
            "W_R_charged": {
                "multiplicity_real_vectors": 2,
                "mass_sq": 0.5 * benchmark["g_R"] ** 2 * v_r**2,
            },
            "Z_R": {
                "multiplicity_real_vectors": 1,
                "mass_sq": (
                    1.5 * benchmark["g_4"] ** 2 + benchmark["g_R"] ** 2
                )
                * v_r**2,
            },
            "hypercharge_matching": "1/g_Y^2=1/g_R^2+2/(3 g_4^2)",
        },
        "goldstone_diagnostics": {
            "broken_generator_rank": broken_rank,
            "max_hessian_times_broken_direction": goldstone_residual,
        },
        "random_moment_map_scan": random_scan,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def write_output(root: Path, result: Mapping[str, object]) -> None:
    output = root / "results" / "phase2b_vacuum_spectrum.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="TP-03 project root",
    )
    args = parser.parse_args()
    result = build_results()
    write_output(args.root.resolve(), result)
    print(
        json.dumps(
            {
                "all_pass": result["all_pass"],
                "lambda_eff": result["lambda_eff"],
                "goldstone_diagnostics": result["goldstone_diagnostics"],
            },
            indent=2,
        )
    )
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
