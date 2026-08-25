from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.linalg import null_space


MINKOWSKI_METRIC = np.diag([1.0, -1.0, -1.0, -1.0])


def dirac_gamma_matrices() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return gamma^mu in the Dirac representation with metric (+---)."""
    zero = np.zeros((2, 2), dtype=complex)
    eye2 = np.eye(2, dtype=complex)
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    gamma0 = np.block([[eye2, zero], [zero, -eye2]])
    gammas = [gamma0]
    for sigma in (sigma1, sigma2, sigma3):
        gammas.append(np.block([[zero, sigma], [-sigma, zero]]))
    return tuple(gammas)  # type: ignore[return-value]


GAMMA = dirac_gamma_matrices()
GAMMA5 = 1j * GAMMA[0] @ GAMMA[1] @ GAMMA[2] @ GAMMA[3]
IDENTITY4 = np.eye(4, dtype=complex)
P_LEFT = 0.5 * (IDENTITY4 - GAMMA5)
P_RIGHT = 0.5 * (IDENTITY4 + GAMMA5)


def sigma(mu: int, nu: int) -> np.ndarray:
    return 0.5j * (GAMMA[mu] @ GAMMA[nu] - GAMMA[nu] @ GAMMA[mu])


def clifford_basis() -> list[np.ndarray]:
    """Complete 16-element complex Dirac-matrix basis."""
    basis: list[np.ndarray] = [IDENTITY4]
    basis.extend(GAMMA)
    basis.extend(sigma(mu, nu) for mu in range(4) for nu in range(mu + 1, 4))
    basis.extend(GAMMA5 @ GAMMA[mu] for mu in range(4))
    basis.append(GAMMA5)
    if len(basis) != 16:
        raise AssertionError("Clifford basis must contain 16 matrices")
    return basis


def matrix_span_rank(matrices: Iterable[np.ndarray], tol: float = 1.0e-11) -> int:
    cols = [np.asarray(m, dtype=complex).reshape(-1) for m in matrices]
    if not cols:
        return 0
    return int(np.linalg.matrix_rank(np.stack(cols, axis=1), tol=tol))


def lower(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    if v.shape != (4,):
        raise ValueError("four-vector must have shape (4,)")
    return MINKOWSKI_METRIC @ v


def minkowski_dot(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.asarray(a) @ MINKOWSKI_METRIC @ np.asarray(b))


def transverse_vectors(q: np.ndarray, rcond: float = 1.0e-13) -> np.ndarray:
    """Return a 4x3 basis E with q_mu E^mu_i = 0.

    The basis is Euclidean-orthonormal in component space.  It is not assumed to
    be orthonormal with respect to the indefinite Minkowski metric.  This is
    numerically robust close to light-like kinematics and is sufficient for a
    complete component decomposition.
    """
    q_lower = lower(np.asarray(q, dtype=float))
    if np.linalg.norm(q_lower) < 1.0e-15:
        raise ValueError("zero momentum has no unique longitudinal direction")
    basis = null_space(q_lower[None, :], rcond=rcond)
    if basis.shape != (4, 3):
        raise RuntimeError(f"expected a three-dimensional transverse space, got {basis.shape}")
    return np.asarray(basis, dtype=float)


def fermion_gauge_transverse_basis(q: np.ndarray) -> list[np.ndarray]:
    """Complete 48-dimensional transverse basis for a 4-vector Dirac vertex.

    Each element has shape (4,4,4): Lorentz index first, then Dirac indices.
    """
    e = transverse_vectors(q)
    cb = clifford_basis()
    out: list[np.ndarray] = []
    for i in range(3):
        for c in cb:
            out.append(np.einsum("m,ab->mab", e[:, i], c))
    return out


def vertex_span_rank(vertices: Iterable[np.ndarray], tol: float = 1.0e-11) -> int:
    cols = [np.asarray(v, dtype=complex).reshape(-1) for v in vertices]
    if not cols:
        return 0
    return int(np.linalg.matrix_rank(np.stack(cols, axis=1), tol=tol))


def max_transverse_residual(q: np.ndarray, vertices: Iterable[np.ndarray]) -> float:
    q_lower = lower(np.asarray(q, dtype=float))
    worst = 0.0
    for vertex in vertices:
        contraction = np.einsum("m,mab->ab", q_lower, vertex)
        denom = max(np.linalg.norm(vertex) * np.linalg.norm(q_lower), 1.0e-30)
        worst = max(worst, float(np.linalg.norm(contraction) / denom))
    return worst


def scalar_gauge_transverse_basis(q: np.ndarray) -> list[np.ndarray]:
    e = transverse_vectors(q)
    return [e[:, i].copy() for i in range(3)]


def chiral_yukawa_basis(orientation: str = "R_to_L", tol: float = 1.0e-11) -> list[np.ndarray]:
    """Return an independent basis for a chiral scalar-fermion-fermion vertex."""
    if orientation == "R_to_L":
        left, right = P_RIGHT, P_LEFT
    elif orientation == "L_to_R":
        left, right = P_LEFT, P_RIGHT
    else:
        raise ValueError("orientation must be 'R_to_L' or 'L_to_R'")
    candidates = [left @ c @ right for c in clifford_basis()]
    vectors = np.stack([m.reshape(-1) for m in candidates], axis=1)
    # Pivoted QR on the candidate matrix selects an independent subset.
    _, r, piv = __import__("scipy.linalg", fromlist=["qr"]).qr(vectors, mode="economic", pivoting=True)
    diag = np.abs(np.diag(r))
    rank = int(np.sum(diag > tol * max(diag[0] if diag.size else 1.0, 1.0)))
    return [candidates[int(i)] for i in piv[:rank]]


def three_gauge_fully_transverse_basis(p: np.ndarray, q: np.ndarray, r: np.ndarray) -> list[np.ndarray]:
    """Return the 27-dimensional component basis transverse on all three legs."""
    if np.linalg.norm(np.asarray(p) + np.asarray(q) + np.asarray(r)) > 1.0e-9:
        raise ValueError("three-gauge external momenta must sum to zero")
    ep, eq, er = transverse_vectors(p), transverse_vectors(q), transverse_vectors(r)
    out: list[np.ndarray] = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                out.append(np.einsum("m,n,r->mnr", ep[:, i], eq[:, j], er[:, k]))
    return out


def max_three_leg_transverse_residual(
    p: np.ndarray, q: np.ndarray, r: np.ndarray, vertices: Iterable[np.ndarray]
) -> float:
    pl, ql, rl = lower(p), lower(q), lower(r)
    worst = 0.0
    for v in vertices:
        denom = max(np.linalg.norm(v), 1.0e-30)
        c1 = np.einsum("m,mnr->nr", pl, v)
        c2 = np.einsum("n,mnr->mr", ql, v)
        c3 = np.einsum("r,mnr->mn", rl, v)
        worst = max(worst, float(np.linalg.norm(c1) / denom), float(np.linalg.norm(c2) / denom), float(np.linalg.norm(c3) / denom))
    return worst


@dataclass(frozen=True)
class TensorBasisMetrics:
    clifford_rank: int
    fermion_vertex_rank: int
    fermion_vertex_transverse_residual: float
    scalar_vertex_rank: int
    yukawa_chiral_rank: int
    three_gauge_rank: int
    three_gauge_transverse_residual: float


def evaluate_basis_metrics() -> TensorBasisMetrics:
    q = np.array([3.7, 0.4, -0.9, 1.2])
    p = np.array([2.1, 0.7, 0.2, -0.5])
    r = -(p + q)
    f_basis = fermion_gauge_transverse_basis(q)
    s_basis = scalar_gauge_transverse_basis(q)
    y_basis = chiral_yukawa_basis("R_to_L")
    g3_basis = three_gauge_fully_transverse_basis(p, q, r)
    return TensorBasisMetrics(
        clifford_rank=matrix_span_rank(clifford_basis()),
        fermion_vertex_rank=vertex_span_rank(f_basis),
        fermion_vertex_transverse_residual=max_transverse_residual(q, f_basis),
        scalar_vertex_rank=int(np.linalg.matrix_rank(np.stack(s_basis, axis=1))),
        yukawa_chiral_rank=matrix_span_rank(y_basis),
        three_gauge_rank=vertex_span_rank(g3_basis),
        three_gauge_transverse_residual=max_three_leg_transverse_residual(p, q, r, g3_basis),
    )
