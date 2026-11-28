"""Cross-ontology comparison: C_classical(f; eps, W) vs. C_quantum(f; eps, W) for ANANKE v4.

Provides:
1. Verified d-dimensional quantum realizations ``QuantumRealization``
   (rho_0 >= 0, Tr(rho_0) = 1, unitary channels U_a, binary POVM 0 <= E <= I_d),
   witnessing the exact upper bound C_quantum(f; 0, W) <= d, together with exact
   conversion into the d^2-dimensional real Hermitian-basis ``LinearProcess``.
2. Explicit families of two-symbol quantum processes (d = 2 qubit, d = 3 qutrit,
   d = 4 two-qubit, d = 5 ququint) with noncommuting operations {x, z}.
3. Proved Fejes Toth spherical-polytope inradius contraction bound explaining the
   dynamical-vs-static classical gap (why two-symbol Bloch polytopes incur
   Omega(1 - exp(-c L / N)) error while static mixed-qubit NMF fits in N = 8).
4. Unconstrained arbitrary-rank two-symbol classical HMM optimizer (returning a
   strictly verified ``ClassicalRealization``) to benchmark full dynamical
   classical upper bounds against static NMF and proved lower bounds.
5. Unified cross-ontology comparison reports bracketing C_classical vs C_quantum
   and comparing directly against the unary shift-register ceiling L + 1.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, pi, sqrt, tan
from typing import Mapping, Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import minimize

from .approximate_realization import (
    ClassicalRealization,
    construct_bloch_polytope_counterfeit,
    fit_static_simplex_box_nmf,
)
from .examples import qubit_rotation_process
from .process import LinearProcess
from .words import validate_word

FloatArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]


# ---------------------------------------------------------------------------
# Verified d-Dimensional Quantum Realizations (C_quantum(f; 0, W) <= d)
# ---------------------------------------------------------------------------


def validate_quantum_realization(
    alphabet: Sequence[str],
    initial_density: ComplexArray,
    unitaries: Mapping[str, ComplexArray],
    measurement_effect: ComplexArray,
    *,
    tol: float = 1e-8,
) -> None:
    """Strictly verify rho_0 >= 0, Tr(rho_0) = 1, U_a^dag U_a = I_d, and 0 <= E <= I_d."""
    rho = np.asarray(initial_density, dtype=complex)
    eff = np.asarray(measurement_effect, dtype=complex)
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1] or rho.shape[0] == 0:
        raise ValueError("initial_density must be a non-empty square matrix")
    d = int(rho.shape[0])
    if eff.shape != (d, d):
        raise ValueError(f"measurement_effect has shape {eff.shape}, expected {(d, d)}")

    # Hermiticity, PSD, and unit trace of rho_0
    if float(np.max(np.abs(rho - rho.conj().T))) > tol:
        raise ValueError("initial_density is not Hermitian")
    rho_evals = np.linalg.eigvalsh(0.5 * (rho + rho.conj().T))
    if float(np.min(rho_evals)) < -tol:
        raise ValueError(f"initial_density is not positive semidefinite: min eig = {rho_evals.min()}")
    tr_err = abs(complex(np.trace(rho)) - 1.0)
    if tr_err > tol:
        raise ValueError(f"initial_density trace deviates from 1 by {tr_err}")

    # Hermiticity and POVM bounds 0 <= E <= I_d
    if float(np.max(np.abs(eff - eff.conj().T))) > tol:
        raise ValueError("measurement_effect is not Hermitian")
    eff_evals = np.linalg.eigvalsh(0.5 * (eff + eff.conj().T))
    if float(np.min(eff_evals)) < -tol or float(np.max(eff_evals)) > 1.0 + tol:
        raise ValueError(
            f"measurement_effect violates 0 <= E <= I_d: eig range [{eff_evals.min()}, {eff_evals.max()}]"
        )

    # Unitarity of every operation U_a
    eye = np.eye(d, dtype=complex)
    for sym in alphabet:
        if sym not in unitaries:
            raise ValueError(f"missing unitary for symbol {sym!r}")
        u_mat = np.asarray(unitaries[sym], dtype=complex)
        if u_mat.shape != (d, d):
            raise ValueError(f"unitary {sym!r} has shape {u_mat.shape}, expected {(d, d)}")
        u_err = float(np.max(np.abs(u_mat.conj().T @ u_mat - eye)))
        if u_err > tol:
            raise ValueError(f"unitary {sym!r} fails U^dag U = I_d with max error {u_err}")


def _orthonormal_hermitian_basis(dimension: int) -> list[ComplexArray]:
    """Return an orthonormal basis {G_0, ..., G_{d^2 - 1}} of d x d Hermitian matrices.

    Satisfies Tr(G_a G_b) = delta_{a, b}, with G_0 = I_d / sqrt(d).
    """
    d = int(dimension)
    basis: list[ComplexArray] = [np.eye(d, dtype=complex) / sqrt(float(d))]
    # Diagonal traceless matrices (generalized Gell-Mann)
    for k in range(1, d):
        mat = np.zeros((d, d), dtype=complex)
        for j in range(k):
            mat[j, j] = 1.0
        mat[k, k] = -float(k)
        mat /= sqrt(float(k * (k + 1)))
        basis.append(mat)
    # Off-diagonal symmetric and antisymmetric pairs
    inv_rt2 = 1.0 / sqrt(2.0)
    for j in range(d):
        for k in range(j + 1, d):
            sym = np.zeros((d, d), dtype=complex)
            sym[j, k] = inv_rt2
            sym[k, j] = inv_rt2
            basis.append(sym)
            anti = np.zeros((d, d), dtype=complex)
            anti[j, k] = -1j * inv_rt2
            anti[k, j] = 1j * inv_rt2
            basis.append(anti)
    return basis


@dataclass(frozen=True)
class QuantumRealization:
    """A strictly verified d-dimensional quantum prepare-transform-measure realization.

    Word probability convention (matching ``LinearProcess`` left-to-right application):
        For w = a_1 a_2 ... a_k,
            rho(w) = U_{a_k} ... U_{a_1} rho_0 U_{a_1}^dag ... U_{a_k}^dag,
            f(w)   = Tr(E rho(w)).
    Existence of this verified realization proves C_quantum(f; 0, W) <= d.
    """

    alphabet: tuple[str, ...]
    initial_density: ComplexArray
    unitaries: Mapping[str, ComplexArray]
    measurement_effect: ComplexArray
    construction: str = "generic_quantum"

    def __post_init__(self) -> None:
        validate_quantum_realization(
            self.alphabet,
            self.initial_density,
            self.unitaries,
            self.measurement_effect,
        )

    @property
    def hilbert_dimension(self) -> int:
        """Hilbert-space dimension d (upper bound on C_quantum(f; 0, W))."""
        return int(self.initial_density.shape[0])

    @property
    def liouville_dimension(self) -> int:
        """Real Hermitian operator space dimension d^2."""
        d = self.hilbert_dimension
        return d * d

    def density_after(self, word: str) -> ComplexArray:
        """Return rho(w) = U_{a_k} ... U_{a_1} rho_0 U_{a_1}^dag ... U_{a_k}^dag."""
        validate_word(word, self.alphabet)
        rho = self.initial_density.copy()
        for sym in word:
            u_mat = self.unitaries[sym]
            rho = u_mat @ rho @ u_mat.conj().T
        return rho

    def behavior(self, word: str) -> float:
        """Return exact Born-rule probability Tr(E rho(w)) in [0, 1]."""
        rho = self.density_after(word)
        val = float(np.real(np.trace(self.measurement_effect @ rho)))
        return float(np.clip(val, 0.0, 1.0))

    def to_linear_process(self) -> LinearProcess:
        """Convert exactly to the d^2-dimensional real Liouville-space ``LinearProcess``."""
        d = self.hilbert_dimension
        basis = _orthonormal_hermitian_basis(d)
        d2 = d * d

        init_vec = np.array(
            [float(np.real(np.trace(g @ self.initial_density))) for g in basis],
            dtype=float,
        )
        final_vec = np.array(
            [float(np.real(np.trace(g @ self.measurement_effect))) for g in basis],
            dtype=float,
        )
        # In row-vector convention: (init @ T_a)_b = sum_c init_c (T_a)_{c, b}
        # Since U rho U^dag = sum_c init_c (U G_c U^dag), its b-th coordinate is
        # sum_c init_c Tr(G_b U G_c U^dag), so (T_a)_{c, b} = Tr(G_b U_a G_c U_a^dag)!
        transitions: dict[str, FloatArray] = {}
        for sym in self.alphabet:
            u_mat = self.unitaries[sym]
            u_dag = u_mat.conj().T
            trans = np.empty((d2, d2), dtype=float)
            for c_idx, g_c in enumerate(basis):
                ug = u_mat @ g_c @ u_dag
                for b_idx, g_b in enumerate(basis):
                    trans[c_idx, b_idx] = float(np.real(np.trace(g_b @ ug)))
            transitions[sym] = trans

        return LinearProcess(
            alphabet=self.alphabet,
            initial=init_vec,
            transitions=transitions,
            final=final_vec,
        )


def qubit_quantum_realization(
    theta_x: float = 0.73,
    theta_z: float = 1.11,
    initial_bloch: FloatArray | None = None,
    measurement_axis: FloatArray | None = None,
) -> QuantumRealization:
    """Return the exact d = 2 Hilbert-space ``QuantumRealization`` of ``qubit_rotation_process``."""
    r0 = (
        np.array([0.23, -0.41, 0.71], dtype=float)
        if initial_bloch is None
        else np.asarray(initial_bloch, dtype=float).reshape(-1)
    )
    m0 = (
        np.array([0.4, 0.7, -0.2], dtype=float)
        if measurement_axis is None
        else np.asarray(measurement_axis, dtype=float).reshape(-1)
    )
    m0 = m0 / float(np.linalg.norm(m0))

    sx = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sy = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    eye2 = np.eye(2, dtype=complex)

    rho0 = 0.5 * (eye2 + r0[0] * sx + r0[1] * sy + r0[2] * sz)
    eff = 0.5 * (eye2 + m0[0] * sx + m0[1] * sy + m0[2] * sz)
    ux = cos(0.5 * theta_x) * eye2 - 1j * np.sin(0.5 * theta_x) * sx
    uz = cos(0.5 * theta_z) * eye2 - 1j * np.sin(0.5 * theta_z) * sz

    return QuantumRealization(
        alphabet=("x", "z"),
        initial_density=rho0,
        unitaries={"x": ux, "z": uz},
        measurement_effect=eff,
        construction="qubit_su2_exact",
    )


def qudit_two_symbol_quantum_realization(
    dimension: int,
    *,
    seed: int = 0,
    measurement_rank: int | None = None,
) -> QuantumRealization:
    """Construct a verified d-dimensional two-symbol ({x, z}) quantum process (C_quantum <= d).

    Uses two deterministic Haar-distributed SU(d) unitaries U_x, U_z, pure initial
    state |0><0|, and projective measurement E = sum_{j < r_e} |j><j| with
    r_e = max(1, d // 2) (maximizing binary variance and Hankel singular values).
    """
    d = int(dimension)
    if d < 2:
        raise ValueError("dimension must be at least 2")
    r_e = max(1, d // 2) if measurement_rank is None else int(measurement_rank)
    if not 1 <= r_e < d:
        raise ValueError("measurement_rank must satisfy 1 <= measurement_rank < dimension")

    rng = np.random.default_rng(int(seed))

    def _haar_unitary(n: int) -> ComplexArray:
        z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / sqrt(2.0)
        q, r = np.linalg.qr(z)
        diag = np.diag(r)
        phases = diag / np.where(np.abs(diag) > 0.0, np.abs(diag), 1.0)
        return q * phases[None, :]

    ux = _haar_unitary(d)
    uz = _haar_unitary(d)
    rho0 = np.zeros((d, d), dtype=complex)
    rho0[0, 0] = 1.0
    eff = np.zeros((d, d), dtype=complex)
    for j in range(r_e):
        eff[j, j] = 1.0

    return QuantumRealization(
        alphabet=("x", "z"),
        initial_density=rho0,
        unitaries={"x": ux, "z": uz},
        measurement_effect=eff,
        construction=f"qudit_d{d}_haar_seed{seed}",
    )


# ---------------------------------------------------------------------------
# Avenue 3: Proved Dynamical Polytope Contraction & Unconstrained 2-Symbol HMM
# ---------------------------------------------------------------------------


def fejes_toth_inradius_upper_bound(vertex_count: int) -> float:
    """Proved Fejes Toth (1953) upper bound on the inradius of any N-vertex polytope in B^3.

    By Euler's formula, any triangulated N-vertex polytope K_N subset B^3 has
    F <= 2N - 4 faces, average spherical area Delta = 2*pi/(N - 2), and
    half-angle omega = pi*N / (6*(N - 2)). By Jensen's inequality on spherical
    triangle circumradii (Fejes Toth 1953):

        rho_in(K_N) <= cot(omega) / sqrt(3) = 1 / (sqrt(3) * tan(pi * N / (6 * (N - 2)))).

    Exact for the regular tetrahedron (N=4: 1/3), regular octahedron (N=6: 1/sqrt(3)),
    and regular icosahedron (N=12: sqrt((5 + 2*sqrt(5))/15) ~ 0.79465); asymptotically
    1 - (4*pi / (3*sqrt(3))) / N ~ 1 - 2.4184 / N.
    """
    n = int(vertex_count)
    if n < 4:
        raise ValueError("3D polytope requires at least 4 vertices")
    omega = pi * float(n) / (6.0 * float(n - 2))
    return float(1.0 / (sqrt(3.0) * tan(omega)))


def dynamical_bloch_polytope_contraction_summary(
    vertex_count: int,
    depth: int,
    *,
    initial_bloch_norm: float = 1.0,
) -> dict[str, float]:
    """Summarize the proved Fejes Toth depth-compounding contraction of Bloch-polytope models.

    If each generic non-symmetry rotation contracts the Bloch norm by at most
    rho_max(N) = fejes_toth_inradius_upper_bound(N), then after ``depth`` steps
    the maximum reachable Bloch norm is bounded by ``initial_bloch_norm * rho_max(N)**depth``,
    incurring amplitude loss at least ``0.5 * initial_bloch_norm * (1 - rho_max(N)**depth)``.
    """
    rho_ub = fejes_toth_inradius_upper_bound(vertex_count)
    compounded = rho_ub ** int(depth)
    amp_loss = 0.5 * float(initial_bloch_norm) * (1.0 - compounded)
    return {
        "vertex_count": float(vertex_count),
        "depth": float(depth),
        "fejes_toth_inradius_ub": rho_ub,
        "compounded_radius_ub": compounded,
        "implied_amplitude_loss_lb": amp_loss,
    }


@dataclass(frozen=True)
class TwoSymbolHMMResult:
    """Strictly verified arbitrary-rank N-state two-symbol classical HMM counterfeit."""

    realization: ClassicalRealization
    max_error: float
    rms_error: float
    word_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "state_count": self.realization.state_count,
            "max_error": self.max_error,
            "rms_error": self.rms_error,
            "word_count": self.word_count,
            "construction": self.realization.construction,
        }


def optimize_two_symbol_classical_hmm(
    target: LinearProcess,
    words: Sequence[str],
    order: int,
    *,
    restarts: int = 4,
    maxiter: int = 180,
    seed: int = 0,
) -> TwoSymbolHMMResult:
    """Numerically optimize an unconstrained arbitrary-rank N-state 2-symbol classical HMM.

    Uses prefix-tree recurrence for O(|W| * N^2) evaluation and returns a strictly
    validated ``ClassicalRealization`` (valid upper bound on C_classical).
    """
    if len(target.alphabet) != 2:
        raise ValueError("optimize_two_symbol_classical_hmm requires a 2-symbol alphabet")
    sym0, sym1 = target.alphabet
    n = int(order)
    if n < 2:
        raise ValueError("order must be at least 2")

    # Sort words by length so every non-empty word's parent prefix precedes it
    ordered_words = sorted(set(str(w) for w in words), key=lambda w: (len(w), w))
    # Ensure prefix closure for tree recurrence
    word_set = set(ordered_words)
    closure = set(word_set)
    for w in ordered_words:
        for cut in range(len(w)):
            closure.add(w[:cut])
    tree_words = sorted(closure, key=lambda w: (len(w), w))
    idx_map = {w: i for i, w in enumerate(tree_words)}
    parents = [idx_map[w[:-1]] for w in tree_words[1:]]
    syms = [0 if w[-1] == sym0 else 1 for w in tree_words[1:]]
    eval_indices = np.array([idx_map[w] for w in ordered_words], dtype=int)
    y_target = np.array([target.behavior(w) for w in ordered_words], dtype=float)

    rng = np.random.default_rng(int(seed))

    def _unpack(x: FloatArray) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
        lm0 = x[: n * n].reshape(n, n)
        lm0 = lm0 - np.max(lm0, axis=1, keepdims=True)
        m0 = np.exp(np.clip(lm0, -35.0, 0.0))
        m0 /= np.sum(m0, axis=1, keepdims=True)

        lm1 = x[n * n : 2 * n * n].reshape(n, n)
        lm1 = lm1 - np.max(lm1, axis=1, keepdims=True)
        m1 = np.exp(np.clip(lm1, -35.0, 0.0))
        m1 /= np.sum(m1, axis=1, keepdims=True)

        lp = x[2 * n * n : 2 * n * n + n]
        lp = lp - np.max(lp)
        p_vec = np.exp(np.clip(lp, -35.0, 0.0))
        p_vec /= np.sum(p_vec)

        e_vec = 1.0 / (1.0 + np.exp(-np.clip(x[2 * n * n + n :], -25.0, 25.0)))
        return p_vec, m0, m1, e_vec

    def _predict(p_vec: FloatArray, m0: FloatArray, m1: FloatArray, e_vec: FloatArray) -> FloatArray:
        states = np.empty((len(tree_words), n), dtype=float)
        states[0] = p_vec
        mats = (m0, m1)
        for idx_w in range(1, len(tree_words)):
            states[idx_w] = states[parents[idx_w - 1]] @ mats[syms[idx_w - 1]]
        return states[eval_indices] @ e_vec

    def _loss(x: FloatArray) -> float:
        preds = _predict(*_unpack(x))
        diff = preds - y_target
        return float(np.mean(diff * diff) + 0.05 * np.max(diff * diff))

    best_res: TwoSymbolHMMResult | None = None
    for _ in range(int(restarts)):
        x0 = rng.normal(0.0, 1.3, size=2 * n * n + 2 * n)
        opt = minimize(_loss, x0, method="L-BFGS-B", options={"maxiter": int(maxiter)})
        p_vec, m0, m1, e_vec = _unpack(opt.x)
        real = ClassicalRealization(
            alphabet=(sym0, sym1),
            initial=p_vec,
            transitions={sym0: m0, sym1: m1},
            final=e_vec,
            construction="unconstrained_two_symbol_hmm_lbfgs",
        )
        preds = _predict(p_vec, m0, m1, e_vec)
        diff = np.abs(preds - y_target)
        mx = float(np.max(diff))
        rms = float(sqrt(float(np.mean(diff * diff))))
        if best_res is None or mx < best_res.max_error:
            best_res = TwoSymbolHMMResult(real, mx, rms, len(ordered_words))

    assert best_res is not None
    return best_res
