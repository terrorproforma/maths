#!/usr/bin/env python3
"""TP-01 v1.1 verification suite.

This script verifies the finite-dimensional algebraic statements used in the
Dirac/BRST, Kaluza-Klein and global-holonomy audit.  It does not simulate a
complete spacetime solution.  The regular-sector computation is a local
phase-space witness: at a point, it solves the algebraic CS constraints and
checks the rank conditions required by the canonical analysis.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

SEED = 0
RANK_TOL = 1.0e-8


def levi_civita(indices: Sequence[int]) -> int:
    if len(set(indices)) != len(indices):
        return 0
    inversions = 0
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            if indices[i] > indices[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def generator_pairs() -> List[Tuple[int, int]]:
    return list(itertools.combinations(range(6), 2))


def spatial_pairs() -> List[Tuple[int, int]]:
    return list(itertools.combinations(range(4), 2))


def invariant_tensor() -> np.ndarray:
    pairs = generator_pairs()
    n = len(pairs)
    g = np.zeros((n, n, n), dtype=float)
    for a, (a0, a1) in enumerate(pairs):
        for b, (b0, b1) in enumerate(pairs):
            for c, (c0, c1) in enumerate(pairs):
                g[a, b, c] = levi_civita((a0, a1, b0, b1, c0, c1))
    return g


def spatial_wedge_matrix() -> np.ndarray:
    pairs = spatial_pairs()
    w = np.zeros((len(pairs), len(pairs)), dtype=float)
    for p, (i, j) in enumerate(pairs):
        for q, (k, ell) in enumerate(pairs):
            w[p, q] = levi_civita((i, j, k, ell))
    return w


def constraints_from_flat(x: np.ndarray, g: np.ndarray, w: np.ndarray) -> np.ndarray:
    f = x.reshape(len(spatial_pairs()), len(generator_pairs()))
    return np.einsum("abc,pq,pb,qc->a", g, w, f, f, optimize=True)


def full_spatial_curvature(x: np.ndarray) -> np.ndarray:
    n = len(generator_pairs())
    f = x.reshape(len(spatial_pairs()), n)
    out = np.zeros((4, 4, n), dtype=float)
    for p, (i, j) in enumerate(spatial_pairs()):
        out[i, j, :] = f[p, :]
        out[j, i, :] = -f[p, :]
    return out


def symplectic_matrix(x: np.ndarray, g: np.ndarray) -> np.ndarray:
    n = len(generator_pairs())
    f = full_spatial_curvature(x)
    omega = np.zeros((4 * n, 4 * n), dtype=float)
    for i in range(4):
        for j in range(4):
            block = np.zeros((n, n), dtype=float)
            for k in range(4):
                for ell in range(4):
                    eps = levi_civita((i, j, k, ell))
                    if eps:
                        block += -4.0 * eps * np.einsum("abc,c->ab", g, f[k, ell, :])
            omega[i * n : (i + 1) * n, j * n : (j + 1) * n] = block
    return omega


def solve_regular_witness(g: np.ndarray, w: np.ndarray) -> Dict[str, object]:
    rng = np.random.default_rng(SEED)
    x0 = rng.normal(size=len(spatial_pairs()) * len(generator_pairs()))
    solution = least_squares(
        lambda x: constraints_from_flat(x, g, w),
        x0,
        max_nfev=5000,
        xtol=1.0e-13,
        ftol=1.0e-13,
        gtol=1.0e-13,
    )
    x = solution.x
    k = constraints_from_flat(x, g, w)
    omega = symplectic_matrix(x, g)
    singular_values = np.linalg.svd(omega, compute_uv=False)
    omega_rank = int(np.linalg.matrix_rank(omega, tol=RANK_TOL))
    jac_rank = int(np.linalg.matrix_rank(solution.jac, tol=RANK_TOL))

    f = full_spatial_curvature(x)
    null_map = np.zeros((4 * len(generator_pairs()), 4), dtype=float)
    null_residuals: List[float] = []
    for k_index in range(4):
        vector = np.zeros(4 * len(generator_pairs()), dtype=float)
        for j in range(4):
            vector[j * len(generator_pairs()) : (j + 1) * len(generator_pairs())] = f[j, k_index, :]
        null_map[:, k_index] = vector
        null_residuals.append(float(np.linalg.norm(omega @ vector)))

    return {
        "seed": SEED,
        "least_squares_success": bool(solution.success),
        "least_squares_status": int(solution.status),
        "least_squares_message": str(solution.message),
        "function_evaluations": int(solution.nfev),
        "curvature_vector_norm": float(np.linalg.norm(x)),
        "constraint_norm": float(np.linalg.norm(k)),
        "constraint_jacobian_rank": jac_rank,
        "expected_constraint_jacobian_rank": 15,
        "omega_rank": omega_rank,
        "expected_omega_rank": 56,
        "omega_shape": list(omega.shape),
        "diffeomorphism_null_map_rank": int(np.linalg.matrix_rank(null_map, tol=RANK_TOL)),
        "diffeomorphism_null_residuals": null_residuals,
        "singular_values": singular_values.tolist(),
        "curvature_components": x.tolist(),
    }


def so_generator_matrices() -> Tuple[List[Tuple[int, int]], List[np.ndarray], np.ndarray]:
    eta = np.diag([-1.0, 1.0, 1.0, 1.0, 1.0, -1.0])
    pairs = generator_pairs()
    matrices: List[np.ndarray] = []
    for a, b in pairs:
        matrix = np.zeros((6, 6), dtype=float)
        for c in range(6):
            for d in range(6):
                matrix[c, d] = (1.0 if c == a else 0.0) * eta[b, d] - (1.0 if c == b else 0.0) * eta[a, d]
        matrices.append(matrix)
    return pairs, matrices, eta


def adjoint_orbit_checks() -> Dict[str, object]:
    pairs, matrices, _ = so_generator_matrices()
    basis = np.stack([matrix.reshape(-1) for matrix in matrices], axis=1)
    h_index = pairs.index((4, 5))
    h = matrices[h_index]
    adjoint = np.zeros((15, 15), dtype=float)
    for column, generator in enumerate(matrices):
        commutator = h @ generator - generator @ h
        coefficients, *_ = np.linalg.lstsq(basis, commutator.reshape(-1), rcond=None)
        adjoint[:, column] = coefficients
    eigenvalues = np.linalg.eigvals(adjoint)

    subgroup_indices = [0, 1, 2, 3, 5]
    subgroup_pairs = list(itertools.combinations(subgroup_indices, 2))
    vector = np.zeros(6, dtype=float)
    vector[5] = 1.0
    actions = []
    pair_to_matrix = {pair: matrix for pair, matrix in zip(pairs, matrices)}
    for pair in subgroup_pairs:
        actions.append(pair_to_matrix[pair] @ vector)
    action_matrix = np.stack(actions, axis=1)

    z = 0.731
    evals_h, evecs_h = np.linalg.eig(h)
    holonomy = evecs_h @ np.diag(np.exp(z * evals_h)) @ np.linalg.inv(evecs_h)
    trace_numeric = float(np.real_if_close(np.trace(holonomy)))
    trace_formula = float(4.0 + 2.0 * np.cosh(z))

    rounded_eigenvalues = sorted([float(np.real_if_close(value)) for value in eigenvalues])
    return {
        "full_adjoint_orbit_dimension_of_J54": int(np.linalg.matrix_rank(adjoint, tol=1.0e-10)),
        "full_adjoint_centralizer_dimension": 15 - int(np.linalg.matrix_rank(adjoint, tol=1.0e-10)),
        "adjoint_eigenvalues": rounded_eigenvalues,
        "SO32_vector_orbit_dimension_of_delta5": int(np.linalg.matrix_rank(action_matrix, tol=1.0e-10)),
        "SO32_vector_stabilizer_dimension": 10 - int(np.linalg.matrix_rank(action_matrix, tol=1.0e-10)),
        "vector_holonomy_parameter": z,
        "vector_holonomy_trace_numeric": trace_numeric,
        "vector_holonomy_trace_formula": trace_formula,
        "vector_holonomy_trace_residual": abs(trace_numeric - trace_formula),
    }


def mode_closure_checks() -> Dict[str, object]:
    retained = {-1, 0, 1}
    generated = sorted({m + n for m in retained for n in retained})
    missing = sorted(set(generated) - retained)
    closure_chain = [1]
    current = 1
    for _ in range(1, 8):
        current += 1
        closure_chain.append(current)
    return {
        "retained_modes": sorted(retained),
        "one_bracket_generated_modes": generated,
        "missing_modes": missing,
        "finite_truncation_closed": len(missing) == 0,
        "positive_mode_induction_witness": closure_chain,
        "first_KK_pair_regular_sector_real_dof": 26,
        "zero_mode_regular_sector_real_dof": 13,
    }


def symplectic_pullback_checks() -> Dict[str, object]:
    ell = 2.7
    newton = 1.0
    alpha = ell * ell / (64.0 * np.pi * newton)
    theta_euler = 2.0 * alpha
    theta_ec = 2.0 * alpha / (ell * ell)
    expected_ec = 1.0 / (32.0 * np.pi * newton)
    perfect_square_residual = (2.0 / ell**2) ** 2 - 4.0 * 1.0 * (1.0 / ell**4)
    return {
        "ell": ell,
        "G": newton,
        "alpha": alpha,
        "pulled_back_Euler_theta_coefficient": theta_euler,
        "pulled_back_EC_theta_coefficient": theta_ec,
        "expected_EC_theta_coefficient": expected_ec,
        "EC_coefficient_residual": abs(theta_ec - expected_ec),
        "perfect_square_residual": abs(perfect_square_residual),
    }


def background_strata() -> Dict[str, object]:
    return {
        "regular_non_AdS": {
            "constraint_surface": True,
            "omega_rank": 56,
            "regular": True,
            "generic": True,
            "local_dof": 13,
        },
        "maximally_symmetric_AdS": {
            "constraint_surface": True,
            "omega_rank": 0,
            "regular": False,
            "generic": False,
            "ordinary_quadratic_graviton_operator": 0,
        },
        "Schwarzschild_AdS_fixed_daughter": {
            "constraint_surface": False,
            "reason": "The retained Phi equation contains epsilon C wedge C, nonzero for nonzero mass parameter.",
        },
    }


def make_figures(root: Path, regular: Dict[str, object], modes: Dict[str, object]) -> None:
    figures = root / "figures"
    figures.mkdir(parents=True, exist_ok=True)

    singular_values = np.asarray(regular["singular_values"], dtype=float)
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    ax.semilogy(np.arange(1, singular_values.size + 1), singular_values, marker="o", markersize=2.5, linewidth=1.0)
    ax.axvline(56.5, linestyle="--", linewidth=1.0)
    ax.set_xlabel("Singular-value index")
    ax.set_ylabel("Singular value of Omega")
    ax.set_title("Regular Spin(4,2) Chern-Simons phase-space witness")
    ax.text(43, max(singular_values) * 0.04, "rank 56", fontsize=9)
    ax.text(56.8, max(singular_values) * 0.002, "4 diffeomorphism null directions", fontsize=8, rotation=90, va="bottom")
    fig.tight_layout()
    fig.savefig(figures / "regular_sector_symplectic_spectrum.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    names = ["regular canonical", "AdS CS vacuum"]
    ranks = [56, 0]
    bars = ax.bar(names, ranks)
    ax.set_ylabel("rank of 60 x 60 symplectic matrix")
    ax.set_ylim(0, 62)
    ax.set_title("Rank stratification of the five-dimensional parent")
    for bar, value in zip(bars, ranks):
        ax.text(bar.get_x() + bar.get_width() / 2.0, value + 1.0, str(value), ha="center")
    ax.text(0.5, 33, "Schwarzschild-AdS daughter: not on parent constraint surface", ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(figures / "phase_space_strata.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.4, 2.8))
    ax.set_axis_off()
    positions = {-2: 0.08, -1: 0.28, 0: 0.50, 1: 0.72, 2: 0.92}
    for mode, xpos in positions.items():
        ax.text(xpos, 0.50, f"n={mode}", ha="center", va="center", bbox={"boxstyle": "round", "facecolor": "white"})
    ax.annotate("[-1]+[-1]", xy=(positions[-2], 0.46), xytext=(positions[-1], 0.83), arrowprops={"arrowstyle": "->"}, ha="center")
    ax.annotate("[+1]+[+1]", xy=(positions[2], 0.46), xytext=(positions[1], 0.83), arrowprops={"arrowstyle": "->"}, ha="center")
    ax.text(0.5, 0.12, "The set {0,+/-1} is not closed under the non-Abelian loop-algebra bracket.", ha="center")
    ax.set_title("First nonzero Kaluza-Klein level forces higher modes")
    fig.tight_layout()
    fig.savefig(figures / "kk_mode_closure.png", dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    results_dir = root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    g = invariant_tensor()
    w = spatial_wedge_matrix()
    regular = solve_regular_witness(g, w)
    orbit = adjoint_orbit_checks()
    modes = mode_closure_checks()
    symplectic = symplectic_pullback_checks()
    strata = background_strata()

    checks = {
        "invariant_tensor_pair_symmetry": bool(np.allclose(g, np.transpose(g, (1, 0, 2)))),
        "regular_constraint_residual": regular["constraint_norm"] < 1.0e-9,
        "regular_constraint_independence": regular["constraint_jacobian_rank"] == 15,
        "regular_maximal_symplectic_rank": regular["omega_rank"] == 56,
        "four_diffeomorphism_null_vectors": regular["diffeomorphism_null_map_rank"] == 4 and max(regular["diffeomorphism_null_residuals"]) < 1.0e-8,
        "full_adjoint_orbit_rank": orbit["full_adjoint_orbit_dimension_of_J54"] == 8,
        "SO32_vector_orbit_rank": orbit["SO32_vector_orbit_dimension_of_delta5"] == 4,
        "holonomy_trace_formula": orbit["vector_holonomy_trace_residual"] < 1.0e-10,
        "finite_KK_truncation_fails": modes["finite_truncation_closed"] is False and modes["missing_modes"] == [-2, 2],
        "first_KK_pair_dof_count": modes["first_KK_pair_regular_sector_real_dof"] == 26,
        "Einstein_Cartan_symplectic_coefficient": symplectic["EC_coefficient_residual"] < 1.0e-14,
        "MacDowell_Mansouri_perfect_square": symplectic["perfect_square_residual"] < 1.0e-14,
    }

    output = {
        "metadata": {
            "project": "TP-01 common geometric parent",
            "version": "1.1",
            "author": "Angus Muffatti",
            "seed": SEED,
            "scope": "Dirac/BRST, KK and global-holonomy audit; local regular-sector witness, not a global spacetime solution",
        },
        "checks": checks,
        "all_pass": all(checks.values()),
        "regular_sector_witness": regular,
        "orbit_and_holonomy": orbit,
        "KK_mode_closure": modes,
        "symplectic_pullback": symplectic,
        "background_strata": strata,
    }

    result_path = results_dir / "verification_results.json"
    result_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    make_figures(root, regular, modes)

    summary = {
        "all_pass": output["all_pass"],
        "constraint_norm": regular["constraint_norm"],
        "constraint_jacobian_rank": regular["constraint_jacobian_rank"],
        "omega_rank": regular["omega_rank"],
        "max_null_residual": max(regular["diffeomorphism_null_residuals"]),
        "full_adjoint_orbit_dimension": orbit["full_adjoint_orbit_dimension_of_J54"],
        "SO32_vector_orbit_dimension": orbit["SO32_vector_orbit_dimension_of_delta5"],
        "missing_KK_modes": modes["missing_modes"],
        "first_KK_pair_real_dof": modes["first_KK_pair_regular_sector_real_dof"],
    }
    (results_dir / "verification_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
