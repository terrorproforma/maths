"""Multi-symbol rank-unrestricted classical obstructions for ANANKE v4.

Extends ANANKE v3 beyond the unary shift-register wall (C_classical <= L + 1 on
{a^k : k <= L}) using two noncommuting operations {x, z} with ZERO rank upper-bound
assumption.

Core mathematical theorems (PROVED in docs/ananke_v4_multisymbol_ontology_gap.md):

1. Theorem 1 (Kochen--Specker Linear-Witness Ceiling for Single Qubits, PROVED):
   Every single-qubit prepare-transform-measure Hankel matrix H_f admits the
   Kochen--Specker integral decomposition over S^2 of total mass 4 (consistent
   with Toner--Bacon 2003 / Renner--Tavakoli--Quintino 2023 two-bit simulation).
   Consequently, while linear witnesses <W, H_f> / gamma_+(W) CAN exceed 2
   (e.g., 9/4 = 2.25 on a 3x3 qubit block, certifying N >= 3), NO linear witness
   can certify N > 4 on any single-qubit Hankel block. Any single-qubit bound
   exceeding N = 4 MUST exploit a non-convex structural invariant.

2. Theorem 2 (Eliminated-Effect Support-Envelope Obstruction, PROVED & CERTIFIED):
   For ANY N-state classical realization g(w) = p M_w e (arbitrary rank <= N)
   satisfying L_{i,j} <= g(u_i v_j) <= U_{i,j} on ANY prefix-suffix pattern E
   (rectangular or depth-L staircase |u| + |v| <= L):
   Each hidden state column a = P_{.,s} in [0, 1]^m admits a valid effect vector
   q in [0, 1]^n with a_i q_j <= U_{i,j} and a_i (1 - q_j) <= 1 - L_{i,j}
   IF AND ONLY IF a lies in the eliminated-effect support envelope

       A(U, V) = { a in [0, 1]^m : forall (i1, j), (i2, j) in E,
                                   U_{i1, j} / a_{i1} + V_{i2, j} / a_{i2} >= 1 },

   where V_{i, j} = 1 - L_{i, j}. Hence for EVERY probability vector mu in Delta_m:

       C_classical(f; eps, W) >= ceil(1 / sup_{a in A(U, V)} <mu, a>).

   Certified globally via best-first spatial branch-and-bound with exact hyperbola
   propagation and the proved box-scaled secant identity:
       (B_q - V_{q,j}) a_p + (B_p - U_{p,j}) a_q <= B_p B_q.
   Under finite binomial shots, simultaneous Chernoff--KL confidence bounds
   (Hoeffding 1963) exploit O(log(|W|/alpha)/M) variance collapse near 0 and 1.

3. Theorem 3 (Noncommutative Semigroup Spectral Synergy, PROVED & CERTIFIED):
   For ANY composite word w in {x, z}^l, M_w is an N x N row-stochastic matrix
   with spec(M_w) subset Theta_N and tr(M_w^k) >= 0. In particular, the exact
   rational-gate qubit R_x(pi/2) (order 4) and R_z(pi/3) (order 6) satisfies
   C_cl(x^*) <= 4 and C_cl(z^*) <= 6 even at infinite horizon, yet the noncommuting
   product w = xz has cos(theta_{xz}) = -1/4 (strictly irrational by Niven's
   Theorem), certifying arbitrarily large rank-unrestricted N_cl along {(xz)^k}.

4. Theorem 4 (Unconditional Short-Depth Multi-Symbol Spectral Rank Obstruction,
   PROVED & CERTIFIED):
   Combining rank(H_g) <= N, Weyl's singular-value inequality, and ANANKE v2's
   proved Hankel Matrix Hoeffding inequality certifies
       C_classical(f; eps, {x, z}^{<= L}) >= r
   with ZERO rank upper-bound assumption whenever sigma_hat_r > eps_H(alpha) + sqrt(m*n)*eps.
   On verified two-symbol d-level quantum systems (d = 3, 4, 5), full Liouville
   rank d^2 is certified at short depth L = 6, 8, 10, strictly exceeding both
   C_quantum = d and the unary shift-register ceiling L + 1.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
from math import acos, ceil, cos, log, nextafter, pi, sin, sqrt
from typing import Mapping, Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import Bounds, LinearConstraint, linprog, minimize

from .certified_inference import (
    _svd_numerical_guard,
    build_unbiased_empirical_hankel,
    hankel_matrix_hoeffding_bound,
    kl_binomial_confidence_interval,
)
from .examples import qubit_rotation_process
from .observations import ShotDataset
from .process import LinearProcess
from .rank_unrestricted import (
    NoiselessRankUnrestrictedBound,
    RankUnrestrictedReport,
    certify_noiseless_counterfeit_error_lower_bound,
    certify_rank_unrestricted_fourier_cap,
    certify_rank_unrestricted_split_sample,
)
from .words import words_upto

FloatArray = NDArray[np.float64]
_ROUNDING_GUARD = 1.0 + 1e-12
_FLOAT64_PAD = 1e-12


# ---------------------------------------------------------------------------
# Theorem 1: Linear Simplex-Box Witness & Frenkel--Weiner Ceiling Diagnostics
# ---------------------------------------------------------------------------


def rank1_binary_max(weight_matrix: FloatArray) -> float:
    """Exact max_{a in {0,1}^m, b in {0,1}^n} a^T W b for small dimensions (min(m, n) <= 18)."""
    w = np.asarray(weight_matrix, dtype=float)
    m, n = w.shape
    if min(m, n) > 18:
        raise ValueError("exact rank1_binary_max requires min(m, n) <= 18")
    if m <= n:
        best = 0.0
        for mask in range(1, 1 << m):
            bits = np.array([(mask >> i) & 1 for i in range(m)], dtype=float)
            col_sums = bits @ w
            val = float(np.sum(np.maximum(0.0, col_sums)))
            if val > best:
                best = val
        return best
    return rank1_binary_max(w.T)


def simplex_box_linear_ratio(hankel_matrix: FloatArray, weight_matrix: FloatArray) -> dict[str, float]:
    """Compute <W, H_f>, exact gamma_+(W) = max_{a,b in {0,1}} a^T W b, and their ratio.

    By Theorem 1 (Kochen--Specker Linear-Witness Ceiling, PROVED): for EVERY single-qubit
    Hankel matrix H_f and EVERY real weight matrix W with gamma_+(W) > 0,
    <W, H_f> / gamma_+(W) <= 4 (values above 2 are achievable, e.g. 9/4 = 2.25 on a 3x3
    qubit block, certifying N >= 3, but no linear witness can certify N > 4).
    """
    h = np.asarray(hankel_matrix, dtype=float)
    w = np.asarray(weight_matrix, dtype=float)
    if h.shape != w.shape:
        raise ValueError("hankel_matrix and weight_matrix must have identical shapes")
    inner = float(np.sum(w * h))
    g_plus = rank1_binary_max(w)
    ratio = inner / g_plus if g_plus > 0.0 else 0.0
    return {
        "inner_product": inner,
        "gamma_plus": g_plus,
        "linear_lower_bound_ratio": ratio,
    }


# ---------------------------------------------------------------------------
# Theorem 2: Eliminated-Effect Support-Envelope Obstruction (Static & Staircase)
# ---------------------------------------------------------------------------


def compute_voronoi_weights(bloch_points: FloatArray, *, quadrature_points: int = 2400) -> FloatArray:
    """Approximate spherical Voronoi area weights on S^2 for a set of 3D Bloch vectors.

    Any probability vector mu in Delta_m is valid in Theorem 2; Voronoi weights
    prevent clustered prefixes from inflating the single-state cap integral.
    """
    pts = np.asarray(bloch_points, dtype=float)
    if pts.ndim != 2 or pts.shape[1] != 3:
        raise ValueError("bloch_points must have shape (m, 3)")
    norms = np.linalg.norm(pts, axis=1, keepdims=True)
    unit_pts = pts / np.maximum(norms, 1e-12)

    idx = np.arange(int(quadrature_points), dtype=float) + 0.5
    phi = np.arccos(1.0 - 2.0 * idx / float(quadrature_points))
    ang = pi * (1.0 + sqrt(5.0)) * idx
    ref = np.column_stack([np.sin(phi) * np.cos(ang), np.sin(phi) * np.sin(ang), np.cos(phi)])
    nearest = np.argmax(ref @ unit_pts.T, axis=1)
    counts = np.bincount(nearest, minlength=pts.shape[0]).astype(float)
    total = float(np.sum(counts))
    if total <= 0.0:
        return np.full(pts.shape[0], 1.0 / pts.shape[0], dtype=float)
    return counts / total


def build_staircase_envelope_noiseless(
    process: LinearProcess,
    max_length: int,
    max_prefix_length: int,
    *,
    max_suffix_length: int | None = None,
    target_epsilon: float = 0.0,
) -> tuple[tuple[str, ...], tuple[str, ...], FloatArray, FloatArray, NDArray[np.bool_]]:
    """Build exact staircase upper/complement envelopes (U, V) for |u| + |v| <= max_length.

    For every observed pair (u_i, v_j) with |u_i| + |v_j| <= max_length:
        U[i, j] = min(1, f(u_i v_j) + target_epsilon),
        V[i, j] = min(1, 1 - f(u_i v_j) + target_epsilon).
    Unobserved pairs (|u_i| + |v_j| > max_length) receive +inf so they impose no constraint.
    """
    if max_length < 1 or max_prefix_length < 0:
        raise ValueError("invalid length parameters")
    if target_epsilon < 0.0:
        raise ValueError("target_epsilon must be non-negative")
    s_max = max_length if max_suffix_length is None else min(max_length, int(max_suffix_length))
    prefixes = tuple(words_upto(process.alphabet, int(max_prefix_length)))
    suffixes = tuple(words_upto(process.alphabet, int(s_max)))

    # Cache exact evaluations of unique words of length <= max_length
    cache: dict[str, float] = {}
    m, n = len(prefixes), len(suffixes)
    u_mat = np.full((m, n), np.inf, dtype=float)
    v_mat = np.full((m, n), np.inf, dtype=float)
    valid = np.zeros((m, n), dtype=bool)
    for i, u in enumerate(prefixes):
        lu = len(u)
        for j, v in enumerate(suffixes):
            if lu + len(v) <= max_length:
                w = u + v
                if w not in cache:
                    cache[w] = float(np.clip(process.behavior(w), 0.0, 1.0))
                val = cache[w]
                u_mat[i, j] = min(1.0, val + target_epsilon)
                v_mat[i, j] = min(1.0, 1.0 - val + target_epsilon)
                valid[i, j] = True
    return prefixes, suffixes, u_mat, v_mat, valid


def build_staircase_envelope_finite_shot(
    dataset: ShotDataset,
    max_length: int,
    max_prefix_length: int,
    *,
    max_suffix_length: int | None = None,
    target_epsilon: float = 0.0,
    alpha: float = 0.01,
) -> tuple[tuple[str, ...], tuple[str, ...], FloatArray, FloatArray, NDArray[np.bool_], int, int]:
    """Build simultaneous (1 - alpha) Chernoff--KL confidence envelopes (U, V) on |u| + |v| <= L.

    By Hoeffding (1963) Theorem 1 + union bound over unique observed words W:
    with probability >= 1 - alpha simultaneously over ALL w in W,
        L_w <= f(w) <= U_w.
    Therefore every N-state classical model g with max_{w in W} |g(w) - f(w)| <= target_epsilon
    obeys g(u_i v_j) <= U_w + target_epsilon and 1 - g(u_i v_j) <= (1 - L_w) + target_epsilon.
    Crucially, Chernoff--KL half-widths collapse to O(log(|W|/alpha) / M_w) near 0 and 1.

    Returns ``(prefixes, suffixes, U, V, valid_mask, unique_word_count, total_shots)``.
    """
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    if target_epsilon < 0.0:
        raise ValueError("target_epsilon must be non-negative")
    s_max = max_length if max_suffix_length is None else min(max_length, int(max_suffix_length))
    prefixes = tuple(words_upto(dataset.alphabet, int(max_prefix_length)))
    suffixes = tuple(words_upto(dataset.alphabet, int(s_max)))

    unique_words = sorted(
        {u + v for u in prefixes for v in suffixes if len(u) + len(v) <= max_length},
        key=lambda w: (len(w), w),
    )
    dataset.require_words(unique_words)

    delta_each = alpha / float(len(unique_words))
    lo_map: dict[str, float] = {}
    hi_map: dict[str, float] = {}
    total_shots = 0
    for w in unique_words:
        succ = dataset.successes[w]
        tr = dataset.trials[w]
        total_shots += tr
        lo, hi = kl_binomial_confidence_interval(succ, tr, delta_each)
        lo_map[w] = max(0.0, lo - _FLOAT64_PAD)
        hi_map[w] = min(1.0, hi + _FLOAT64_PAD)

    m, n = len(prefixes), len(suffixes)
    u_mat = np.full((m, n), np.inf, dtype=float)
    v_mat = np.full((m, n), np.inf, dtype=float)
    valid = np.zeros((m, n), dtype=bool)
    for i, u in enumerate(prefixes):
        lu = len(u)
        for j, v in enumerate(suffixes):
            if lu + len(v) <= max_length:
                w = u + v
                u_mat[i, j] = min(1.0, hi_map[w] + target_epsilon)
                v_mat[i, j] = min(1.0, 1.0 - lo_map[w] + target_epsilon)
                valid[i, j] = True
    return prefixes, suffixes, u_mat, v_mat, valid, len(unique_words), total_shots


def optimize_support_envelope_weights(
    u_mat: FloatArray,
    v_mat: FloatArray,
    valid: NDArray[np.bool_],
    suffix_bloch: FloatArray | None = None,
    *,
    num_directions: int = 140,
    betas: Sequence[float] = (0.9, 1.25, 1.7, 3.0, 100.0),
) -> FloatArray:
    """Propose minimax-optimized prefix weights mu in Delta_m via LP over cap probes.

    Rigor of Theorem 2 does NOT depend on how mu is selected: ANY probability
    vector mu in Delta_m chosen deterministically (or on an independent pilot split)
    yields a 100% valid certified lower bound when passed to
    ``certify_support_envelope_lower_bound``.
    """
    m, n = u_mat.shape
    probes: list[FloatArray] = []

    if suffix_bloch is not None:
        idx = np.arange(int(num_directions), dtype=float) + 0.5
        phi = np.arccos(1.0 - 2.0 * idx / float(num_directions))
        ang = pi * (1.0 + sqrt(5.0)) * idx
        dirs = np.column_stack([np.sin(phi) * np.cos(ang), np.sin(phi) * np.sin(ang), np.cos(phi)])
        for u_dir in dirs:
            dots = suffix_bloch @ u_dir
            for beta in betas:
                q = np.clip(0.5 + float(beta) * dots, 0.0, 1.0)
                with np.errstate(divide="ignore", invalid="ignore"):
                    ub1 = np.where(valid & (q[None, :] > 1e-12), u_mat / q[None, :], np.inf)
                    ub2 = np.where(
                        valid & (q[None, :] < 1.0 - 1e-12), v_mat / (1.0 - q[None, :]), np.inf
                    )
                probes.append(np.minimum(1.0, np.min(np.minimum(ub1, ub2), axis=1)))
    else:
        # Data-only fallback: threshold rows of U
        h_est = np.where(valid, u_mat, 0.5)
        for i0 in range(m):
            for thr in (0.25, 0.5, 0.75):
                q = (h_est[i0] >= thr).astype(float)
                with np.errstate(divide="ignore", invalid="ignore"):
                    ub1 = np.where(valid & (q[None, :] > 1e-12), u_mat / q[None, :], np.inf)
                    ub2 = np.where(
                        valid & (q[None, :] < 1.0 - 1e-12), v_mat / (1.0 - q[None, :]), np.inf
                    )
                probes.append(np.minimum(1.0, np.min(np.minimum(ub1, ub2), axis=1)))

    a_caps = np.asarray(probes, dtype=float)
    c = np.zeros(m + 1, dtype=float)
    c[m] = 1.0
    res = linprog(
        c,
        A_ub=np.hstack([a_caps, -np.ones((a_caps.shape[0], 1), dtype=float)]),
        b_ub=np.zeros(a_caps.shape[0], dtype=float),
        A_eq=np.hstack([np.ones((1, m), dtype=float), np.zeros((1, 1), dtype=float)]),
        b_eq=np.array([1.0], dtype=float),
        bounds=[(0.0, 1.0)] * (m + 1),
        method="highs",
    )
    if not res.success or res.x is None:
        return np.full(m, 1.0 / m, dtype=float)
    mu = np.maximum(0.0, np.asarray(res.x[:m], dtype=float))
    mu[mu < 1e-6] = 0.0
    total = float(np.sum(mu))
    if total <= 0.0:
        return np.full(m, 1.0 / m, dtype=float)
    return mu / total


@dataclass(frozen=True)
class SupportEnvelopeCertificate:
    """Machine-certified rank-unrestricted lower bound via Theorem 2 (Support Envelope)."""

    certified_sup_upper_bound: float
    continuous_state_lower_bound: float
    certified_classical_state_lower_bound: int
    active_prefix_count: int
    suffix_count: int
    evaluated_nodes: int
    converged: bool
    max_length: int | None
    target_epsilon: float
    alpha: float | None
    total_shots: int | None
    unique_word_count: int | None

    def to_dict(self) -> dict[str, object]:
        return {
            "certified_sup_upper_bound": self.certified_sup_upper_bound,
            "continuous_state_lower_bound": self.continuous_state_lower_bound,
            "certified_classical_state_lower_bound": self.certified_classical_state_lower_bound,
            "active_prefix_count": self.active_prefix_count,
            "suffix_count": self.suffix_count,
            "evaluated_nodes": self.evaluated_nodes,
            "converged": self.converged,
            "max_length": self.max_length,
            "target_epsilon": self.target_epsilon,
            "alpha": self.alpha,
            "confidence_level": None if self.alpha is None else 1.0 - self.alpha,
            "total_shots": self.total_shots,
            "unique_word_count": self.unique_word_count,
            "epistemic_status": (
                "PROVED & CERTIFIED rank-unrestricted lower bound on C_classical(f; eps, W) "
                "via Theorem 2 (Eliminated-Effect Support Envelope + Box-Scaled Secant Branch-and-Bound). "
                "Requires ZERO rank upper-bound assumption and ZERO Jordan-structure assumption."
            ),
        }


def certify_support_envelope_lower_bound(
    u_mat: FloatArray,
    v_mat: FloatArray,
    weights: Sequence[float] | None = None,
    *,
    tol: float = 1.5e-3,
    max_nodes_per_star: int = 3000,
    max_length: int | None = None,
    target_epsilon: float = 0.0,
    alpha: float | None = None,
    total_shots: int | None = None,
    unique_word_count: int | None = None,
) -> SupportEnvelopeCertificate:
    """Globally certify an upper bound on sup_{a in A(U, V)} <mu, a> via spatial branch-and-bound.

    Every node [L, B] enforces:
      1. Exact closed-form hyperbola propagation:
             a_p >= L_p > U_{p,j}  =>  a_q <= V_{q,j} / (1 - U_{p,j} / L_p)
             a_p >= L_p > V_{p,j}  =>  a_q <= U_{q,j} / (1 - V_{p,j} / L_p)
      2. Exact box-scaled secant matching savings:
             (B_q - V_{q,j}) a_p + (B_p - U_{p,j}) a_q <= B_p B_q
         over vertex-disjoint active pairs (p, q).
    Because every pruned or remaining leaf carries a provably valid upper bound,
    the returned ``certified_sup_upper_bound`` is ALWAYS a valid global upper bound
    even if ``max_nodes_per_star`` is reached before ``tol``.
    """
    u_full = np.asarray(u_mat, dtype=float)
    v_full = np.asarray(v_mat, dtype=float)
    if u_full.shape != v_full.shape or u_full.ndim != 2:
        raise ValueError("u_mat and v_mat must be 2D arrays of identical shape")
    if np.any(np.isnan(u_full)) or np.any(np.isnan(v_full)):
        raise ValueError("u_mat and v_mat must not contain NaN")
    if np.any(u_full < 0.0) or np.any(v_full < 0.0):
        raise ValueError("u_mat and v_mat entries must be non-negative (or +inf if unobserved)")
    m_full, n = u_full.shape
    if m_full == 0:
        raise ValueError("u_mat must have at least one row")
    if weights is None:
        mu_full = np.full(m_full, 1.0 / m_full, dtype=float)
    else:
        mu_raw = np.asarray(weights, dtype=float).reshape(-1)
        if mu_raw.size != m_full:
            raise ValueError("weights length must match rows of u_mat")
        if not np.all(np.isfinite(mu_raw)):
            raise ValueError("weights must be finite")
        if np.any(mu_raw < 0.0):
            raise ValueError("weights must be non-negative")
        max_w = float(np.max(mu_raw))
        if max_w <= 0.0:
            raise ValueError("weights must have positive sum")
        # Scale by max_w before summing to prevent IEEE-754 overflow on large finite weights
        scaled_w = mu_raw / max_w
        mu_full = scaled_w / float(np.sum(scaled_w))

    # Drop ONLY strictly zero-weight rows (never drop tiny positive weights)
    keep = np.where(mu_full > 0.0)[0]
    u = u_full[keep].copy()
    v = v_full[keep].copy()
    mu = mu_full[keep] / float(np.sum(mu_full[keep]))
    m = int(keep.size)
    fin_u = np.isfinite(u)
    fin_v = np.isfinite(v)

    def _propagate(low: FloatArray, high: FloatArray) -> tuple[FloatArray, FloatArray] | None:
        """Outward-rounded exact hyperbola bound propagation using Sterbenz-safe differences."""
        low = low.copy()
        high = high.copy()
        changed = True
        while changed:
            changed = False
            pos = np.where(low > 0.0)[0]
            for p in pos:
                lp = float(low[p])
                # Rewrite V / (1 - U / L_p) = (V * L_p) / (L_p - U) so L_p - U is
                # Sterbenz-exact near cancellation, then apply directed IEEE-754 outward rounding.
                mu_mask = fin_u[p] & (u[p] < lp)
                if np.any(mu_mask):
                    diff_lo = np.nextafter(lp - u[p, mu_mask], -np.inf)
                    good = diff_lo > 0.0
                    if np.any(good):
                        cols = np.where(mu_mask)[0][good]
                        d_lo = diff_lo[good]
                        num_hi = np.nextafter(v[:, cols] * lp, np.inf)
                        nb = np.min(np.nextafter(num_hi / d_lo[None, :], np.inf), axis=1)
                        nb = np.minimum(1.0, nb)
                        nb[p] = high[p]
                        upd = nb < high - 1e-12
                        if np.any(upd):
                            high[upd] = nb[upd]
                            changed = True
                mv_mask = fin_v[p] & (v[p] < lp)
                if np.any(mv_mask):
                    diff_lo = np.nextafter(lp - v[p, mv_mask], -np.inf)
                    good = diff_lo > 0.0
                    if np.any(good):
                        cols = np.where(mv_mask)[0][good]
                        d_lo = diff_lo[good]
                        num_hi = np.nextafter(u[:, cols] * lp, np.inf)
                        nb = np.min(np.nextafter(num_hi / d_lo[None, :], np.inf), axis=1)
                        nb = np.minimum(1.0, nb)
                        nb[p] = high[p]
                        upd = nb < high - 1e-12
                        if np.any(upd):
                            high[upd] = nb[upd]
                            changed = True
                # Only prune when strictly infeasible beyond outward ULP guard
                if np.any(low > np.nextafter(high, np.inf)):
                    return None
        return low, high

    def _node_ub_and_branch(low: FloatArray, high: FloatArray) -> tuple[float, tuple[int, int] | None]:
        # Outward-rounded upper bound on <mu, high>
        raw_hi = float(np.sum(np.nextafter(mu * high, np.inf))) * (1.0 + (m + 2) * 1e-15)
        pos = np.where(high > 1e-5)[0]
        k = int(pos.size)
        if k < 2:
            return min(1.0, raw_hi), None
        bp = high[pos]
        mup = mu[pos]
        up = u[pos] / bp[:, None]
        vp = v[pos] / bp[:, None]

        best_viol = 1.0
        best_pair: tuple[int, int] | None = None
        edges: list[tuple[float, int, int]] = []
        for idx_p in range(k):
            s_mat = up[idx_p, None, :] + vp
            j_best = np.argmin(s_mat, axis=1)
            s_min = s_mat[np.arange(k), j_best]
            s_min[idx_p] = 2.0
            for idx_q in range(k):
                sv = float(s_min[idx_q])
                if sv < 1.0 - 1e-9:
                    if sv < best_viol:
                        best_viol = sv
                        best_pair = (int(pos[idx_p]), int(pos[idx_q]))
                    j = int(j_best[idx_q])
                    u_val = float(u[pos[idx_p], j])
                    v_val = float(v[pos[idx_q], j])
                    bp_val = float(bp[idx_p])
                    bq_val = float(bp[idx_q])
                    # Directed rounding: upper bounds on divisors c1, c2 and lower bound on gap
                    c1_hi = nextafter(bq_val - v_val, float("inf"))
                    c2_hi = nextafter(bp_val - u_val, float("inf"))
                    if c1_hi > 1e-12 and c2_hi > 1e-12 and (bq_val > v_val) and (bp_val > u_val):
                        a1_lo = nextafter(float(mup[idx_p]) / c1_hi, 0.0)
                        a2_lo = nextafter(float(mup[idx_q]) / c2_hi, 0.0)
                        alpha_lo = min(a1_lo, a2_lo)
                        prod_lo = nextafter(bp_val * bq_val, -float("inf"))
                        sub_hi = nextafter(
                            nextafter(v_val * bp_val, float("inf"))
                            + nextafter(u_val * bq_val, float("inf")),
                            float("inf"),
                        )
                        gap_lo = nextafter(prod_lo - sub_hi, -float("inf"))
                        if alpha_lo > 0.0 and gap_lo > 1e-12:
                            sav_lo = nextafter(alpha_lo * gap_lo, 0.0)
                            if sav_lo > 1e-11:
                                edges.append((sav_lo, idx_p, idx_q))
        if best_pair is None:
            return min(1.0, raw_hi), None
        edges.sort(reverse=True)
        used = [False] * k
        total_sav_lo = 0.0
        for sav_lo, p_i, q_i in edges:
            if not used[p_i] and not used[q_i]:
                used[p_i] = True
                used[q_i] = True
                total_sav_lo = nextafter(total_sav_lo + sav_lo, 0.0)
        ub_val = nextafter(raw_hi - total_sav_lo, float("inf"))
        low_dot = float(np.dot(mu, low))
        return min(1.0, max(low_dot, ub_val)), best_pair

    global_ub = 0.0
    total_nodes = 0
    all_converged = True
    alphas = np.array([0.0, 0.12, 0.24, 0.38, 0.54, 0.72, 1.0], dtype=float)

    # Symmetry-breaking partition by argmax index i_star in {0, ..., m-1}
    for i_star in range(m):
        heap: list[tuple[float, int, FloatArray, FloatArray, tuple[int, int] | None]] = []
        ctr = 0
        for k_a in range(len(alphas) - 1):
            a_lo, a_hi = float(alphas[k_a]), float(alphas[k_a + 1])
            l0 = np.zeros(m, dtype=float)
            b0 = np.full(m, a_hi, dtype=float)
            l0[i_star] = a_lo
            pr = _propagate(l0, b0)
            if pr is None:
                continue
            l0, b0 = pr
            ub0, bp0 = _node_ub_and_branch(l0, b0)
            if ub0 > global_ub:
                ctr += 1
                heapq.heappush(heap, (-ub0, ctr, l0, b0, bp0))

        nodes = 0
        local_lb = 0.0
        while heap and nodes < int(max_nodes_per_star):
            neg_ub, _, low, high, bp = heap[0]
            top_ub = -neg_ub
            if top_ub <= max(global_ub, local_lb + tol):
                break
            heapq.heappop(heap)
            nodes += 1
            total_nodes += 1
            if bp is None:
                local_lb = max(local_lb, top_ub)
                global_ub = max(global_ub, top_ub)
                continue
            p, q = bp
            br = p if mu[p] * (high[p] - low[p]) >= mu[q] * (high[q] - low[q]) else q
            if high[br] - low[br] < 1e-5:
                br = q if br == p else p
            if high[br] - low[br] < 1e-5:
                # Terminal narrow box: MUST retain top_ub in global_ub!
                local_lb = max(local_lb, top_ub)
                global_ub = max(global_ub, top_ub)
                continue
            mid = 0.5 * (float(low[br]) + float(high[br]))

            # Left branch: a[br] <= mid
            b_left = high.copy()
            b_left[br] = mid
            if br == i_star:
                b_left = np.minimum(b_left, mid)
            ub_l, bp_l = _node_ub_and_branch(low, b_left)
            if ub_l > global_ub:
                ctr += 1
                heapq.heappush(heap, (-ub_l, ctr, low.copy(), b_left, bp_l))

            # Right branch: a[br] >= mid (triggers hyperbola propagation!)
            l_right = low.copy()
            l_right[br] = mid
            pr = _propagate(l_right, high)
            if pr is not None:
                l_right, b_right = pr
                ub_r, bp_r = _node_ub_and_branch(l_right, b_right)
                if ub_r > global_ub:
                    ctr += 1
                    heapq.heappush(heap, (-ub_r, ctr, l_right, b_right, bp_r))

        if heap:
            rem_ub = -heap[0][0]
            if rem_ub > max(global_ub, local_lb + tol):
                all_converged = False
            global_ub = max(global_ub, rem_ub)

    # Apply conservative outward guard against IEEE-754 rounding
    safe_ub = min(1.0, global_ub * _ROUNDING_GUARD + 1e-11)
    cont_lb = 1.0 / safe_ub if safe_ub > 0.0 else float("inf")
    int_lb = max(1, int(ceil(cont_lb - 1e-11))) if np.isfinite(cont_lb) else 1

    return SupportEnvelopeCertificate(
        certified_sup_upper_bound=safe_ub,
        continuous_state_lower_bound=cont_lb,
        certified_classical_state_lower_bound=int_lb,
        active_prefix_count=m,
        suffix_count=n,
        evaluated_nodes=total_nodes,
        converged=all_converged,
        max_length=max_length,
        target_epsilon=float(target_epsilon),
        alpha=alpha,
        total_shots=total_shots,
        unique_word_count=unique_word_count,
    )


def certify_staircase_support_envelope_noiseless(
    process: LinearProcess,
    max_length: int,
    max_prefix_length: int,
    *,
    weights: Sequence[float] | None = None,
    max_suffix_length: int | None = None,
    target_epsilon: float = 0.0,
    tol: float = 1.5e-3,
    max_nodes_per_star: int = 3000,
) -> SupportEnvelopeCertificate:
    """Certify a noiseless rank-unrestricted lower bound on C_classical(f; eps, W_L) via Theorem 2."""
    prefixes, suffixes, u_mat, v_mat, valid = build_staircase_envelope_noiseless(
        process,
        max_length,
        max_prefix_length,
        max_suffix_length=max_suffix_length,
        target_epsilon=target_epsilon,
    )
    if weights is None:
        if process.dimension == 4:
            pts_p = np.array([process.row_after(u)[1:] for u in prefixes], dtype=float)
            pts_q = []
            for v in suffixes:
                vec = process.final.copy()
                for ch in reversed(v):
                    vec = process.transitions[ch] @ vec
                pts_q.append(2.0 * vec[1:])
            weights_arr = optimize_support_envelope_weights(
                u_mat, v_mat, valid, np.asarray(pts_q, dtype=float)
            )
            # Blend slightly with Voronoi if LP is overly sparse? No: keep pure LP or let caller pass weights
            _ = pts_p
        else:
            weights_arr = optimize_support_envelope_weights(u_mat, v_mat, valid, None)
    else:
        weights_arr = np.asarray(weights, dtype=float)

    unique_words = {
        u + v for u in prefixes for v in suffixes if len(u) + len(v) <= max_length
    }
    return certify_support_envelope_lower_bound(
        u_mat,
        v_mat,
        weights_arr,
        tol=tol,
        max_nodes_per_star=max_nodes_per_star,
        max_length=max_length,
        target_epsilon=target_epsilon,
        unique_word_count=len(unique_words),
    )


def certify_staircase_support_envelope_finite_shot(
    dataset: ShotDataset,
    max_length: int,
    max_prefix_length: int,
    weights: Sequence[float],
    *,
    max_suffix_length: int | None = None,
    target_epsilon: float = 0.0,
    alpha: float = 0.01,
    tol: float = 1.5e-3,
    max_nodes_per_star: int = 3000,
) -> SupportEnvelopeCertificate:
    """Certify a non-asymptotic (1 - alpha) rank-unrestricted lower bound on C_classical(f; eps, W_L).

    Requires deterministic (a priori or pilot-chosen) prefix weights ``weights`` in Delta_m
    so no data-snooping enters the simultaneous Chernoff--KL confidence envelope.
    """
    _, _, u_mat, v_mat, _, unique_count, total_shots = build_staircase_envelope_finite_shot(
        dataset,
        max_length,
        max_prefix_length,
        max_suffix_length=max_suffix_length,
        target_epsilon=target_epsilon,
        alpha=alpha,
    )
    return certify_support_envelope_lower_bound(
        u_mat,
        v_mat,
        weights,
        tol=tol,
        max_nodes_per_star=max_nodes_per_star,
        max_length=max_length,
        target_epsilon=target_epsilon,
        alpha=alpha,
        total_shots=total_shots,
        unique_word_count=unique_count,
    )


def continuous_sphere_support_envelope_ceiling(
    *,
    num_grid: int = 32,
) -> dict[str, dict[str, float]]:
    """NUMERICAL axisymmetric cap approximation for the continuous S^2 and S^1 envelopes.

    Discretizes the pairwise log-concave cap constraint
        (1 - a(phi_1))(1 - a(phi_2)) >= sin^2((phi_1 + phi_2) / 2)
    with z(phi) = -ln(1 - a(phi)) >= 0 over a finite midpoint grid and axisymmetric
    cutoffs phi_max in [25 deg, 90 deg]. This is a NUMERICAL diagnostic estimate,
    NOT a certified upper or lower enclosure of the continuum supremum.
    """
    out: dict[str, dict[str, float]] = {}
    for manifold in ("S2", "S1"):
        best_val = 0.0
        best_deg = 0.0
        for pm_deg in range(25, 91, 5):
            pm = np.deg2rad(float(pm_deg))
            ph = np.linspace(0.0, pm, int(num_grid), endpoint=False) + pm / (2.0 * num_grid)
            if manifold == "S2":
                w = 0.5 * np.sin(ph) * (pm / float(num_grid))
            else:
                w = np.full(int(num_grid), (pm / float(num_grid)) / pi, dtype=float)
            c_mat = -2.0 * np.log(np.sin(0.5 * (ph[:, None] + ph[None, :])))
            idx_i, idx_j = np.triu_indices(int(num_grid))
            a_mat = np.zeros((idx_i.size, int(num_grid)), dtype=float)
            for k, (i, j) in enumerate(zip(idx_i, idx_j)):
                a_mat[k, i] += 1.0
                a_mat[k, j] += 1.0
            b_vec = c_mat[idx_i, idx_j]
            res = minimize(
                lambda z: -float(np.sum(w * (1.0 - np.exp(-z)))),
                x0=np.zeros(int(num_grid), dtype=float),
                jac=lambda z: -w * np.exp(-z),
                bounds=Bounds(0.0, 20.0),
                constraints=LinearConstraint(a_mat, -np.inf, b_vec),
                method="SLSQP",
                options={"ftol": 1e-11, "maxiter": 400},
            )
            val = float(-res.fun)
            if val > best_val:
                best_val = val
                best_deg = float(pm_deg)
        out[manifold] = {
            "sup_integral": best_val,
            "continuous_lower_bound": 1.0 / best_val,
            "integer_lower_bound": float(ceil(1.0 / best_val - 1e-12)),
            "maximizing_cap_degrees": best_deg,
        }
    return out


# ---------------------------------------------------------------------------
# Theorem 3: Multi-Symbol Noncommutative Semigroup Spectral Obstruction
# ---------------------------------------------------------------------------


def niven_rational_gate_qubit(
    *,
    initial_bloch: FloatArray | None = None,
    measurement_axis: FloatArray | None = None,
) -> LinearProcess:
    """Return the exact rational-gate qubit U_x = R_x(pi/2), U_z = R_z(pi/3).

    Mathematical properties (PROVED):
      - R_x(pi/2) has order 4 (eigenvalues in Theta_4): unary x-rays satisfy C_cl <= 4!
      - R_z(pi/3) has order 6 (eigenvalues in Theta_6): unary z-rays satisfy C_cl <= 6!
      - Noncommuting product w = xz has exact rotation angle
            cos(theta_{xz}) = 2 cos^2(pi/4) cos^2(pi/6) - 1 = 2*(1/2)*(3/4) - 1 = -1/4,
        so theta_{xz} = arccos(-1/4) ~ 1.82347658 rad.
      - By Niven's Theorem, theta_{xz} / (2*pi) is strictly irrational, so
        e^{i*theta_{xz}} not in Theta_N for EVERY finite N!
    """
    # Choose initial & measurement axes orthogonal to the rotation axis of R_x(pi/2) R_z(pi/3)
    # so the oscillation amplitude along (xz)^k is maximal (A = 0.500)!
    # Rotation axis of R_z(pi/3) followed by R_x(pi/2) (row convention: r -> r M_x M_z = (R_z R_x r)):
    # Wait: in qubit_rotation_process, row_after("xz") = initial @ M_x @ M_z = (R_z @ R_x @ r0)!
    # Let's compute its exact rotation axis and pick an orthogonal unit vector if none supplied.
    proc_tmp = qubit_rotation_process(
        theta_x=pi / 2.0,
        theta_z=pi / 3.0,
        initial_bloch=np.array([0.0, 0.0, 1.0]),
        measurement_axis=np.array([0.0, 0.0, 1.0]),
    )
    rot_xz = (proc_tmp.transitions["x"] @ proc_tmp.transitions["z"]).T[1:, 1:]
    # Find unit eigenvector of rot_xz with eigenvalue +1
    evals, evecs = np.linalg.eig(rot_xz)
    axis_idx = int(np.argmin(np.abs(evals - 1.0)))
    axis = np.real(evecs[:, axis_idx])
    axis /= float(np.linalg.norm(axis))
    # Pick a canonical unit vector orthogonal to `axis`
    ref = np.array([1.0, 0.0, 0.0]) if abs(axis[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    orth = ref - float(np.dot(ref, axis)) * axis
    orth /= float(np.linalg.norm(orth))

    r0 = orth if initial_bloch is None else np.asarray(initial_bloch, dtype=float)
    m0 = orth if measurement_axis is None else np.asarray(measurement_axis, dtype=float)
    return qubit_rotation_process(
        theta_x=pi / 2.0,
        theta_z=pi / 3.0,
        initial_bloch=r0,
        measurement_axis=m0,
    )


def composite_word_rotation_angle(process: LinearProcess, word: str) -> float:
    """Return the principal peripheral eigenphase theta_w in (0, pi] of B_w = prod_{a in w} B_a."""
    if not word:
        raise ValueError("word must be non-empty")
    mat = np.eye(process.dimension, dtype=float)
    for ch in word:
        mat = mat @ process.transitions[ch]
    evals = np.linalg.eigvals(mat)
    # Find largest-modulus eigenvalue with positive imaginary part
    cands = [ev for ev in evals if ev.imag > 1e-10]
    if not cands:
        # Check -1 eigenvalue
        if any(abs(ev + 1.0) < 1e-9 for ev in evals):
            return pi
        return 0.0
    best = max(cands, key=lambda ev: abs(ev))
    return float(np.angle(best))


def composite_ray_words(
    word: str,
    max_repetitions: int,
    *,
    prefix: str = "",
    suffix: str = "",
) -> tuple[str, ...]:
    """Return the composite-word ray ``(prefix + word*k + suffix)`` for ``k = 0..max_repetitions``."""
    if not word:
        raise ValueError("word must be non-empty")
    if max_repetitions < 0:
        raise ValueError("max_repetitions must be non-negative")
    return tuple(f"{prefix}{word * k}{suffix}" for k in range(int(max_repetitions) + 1))


def certify_composite_word_noiseless(
    process: LinearProcess,
    word: str,
    max_repetitions: int,
    order: int,
    *,
    theta_radians: float | None = None,
    prefix: str = "",
    suffix: str = "",
    num_moments: int = 10,
    tol: float = 2e-3,
) -> NoiselessRankUnrestrictedBound:
    """Certify a rank-unrestricted lower bound along any composite word ray {u w^k v} (Theorem 3).

    Because M_w = prod_{a in w} M_a is an N x N row-stochastic matrix for ANY N-state
    classical realization of ANY rank <= N, ANANKE v3's B-spline Cayley--Hamilton +
    Subharmonic Dual theorem applies verbatim to w^k!
    """
    theta = composite_word_rotation_angle(process, word) if theta_radians is None else float(theta_radians)
    words = composite_ray_words(word, max_repetitions, prefix=prefix, suffix=suffix)
    vals = [process.behavior(w) for w in words]
    return certify_noiseless_counterfeit_error_lower_bound(
        vals,
        order,
        theta,
        num_moments=num_moments,
        tol=tol,
    )


def _collapse_composite_word_dataset(
    dataset: ShotDataset,
    word: str,
    max_repetitions: int,
    *,
    prefix: str = "",
    suffix: str = "",
) -> ShotDataset:
    """Re-index observed composite-word ray counts {prefix + word*k + suffix} as unary symbol 'w'."""
    words = composite_ray_words(word, max_repetitions, prefix=prefix, suffix=suffix)
    dataset.require_words(words)
    succ = {"w" * k: dataset.successes[w_str] for k, w_str in enumerate(words)}
    tr = {"w" * k: dataset.trials[w_str] for k, w_str in enumerate(words)}
    return ShotDataset(("w",), succ, tr)


def certify_composite_word_finite_shot(
    dataset: ShotDataset,
    word: str,
    max_repetitions: int,
    theta_radians: float,
    *,
    mode: str = "fourier_cap",
    prefix: str = "",
    suffix: str = "",
    orders: Sequence[int] | None = None,
    maximum_order: int = 12,
    target_epsilon: float = 0.0,
    alpha: float = 0.01,
    pilot_fraction: float = 0.15,
    rng: np.random.Generator | None = None,
    num_moments: int = 10,
    cert_tol: float = 2e-3,
    early_stop: bool = True,
) -> RankUnrestrictedReport:
    """Non-asymptotic (1 - alpha) rank-unrestricted certificate along a composite word ray {u w^k v}."""
    collapsed = _collapse_composite_word_dataset(
        dataset, word, max_repetitions, prefix=prefix, suffix=suffix
    )
    if mode == "fourier_cap":
        return certify_rank_unrestricted_fourier_cap(
            collapsed,
            symbol="w",
            max_ray_power=max_repetitions,
            theta_radians=theta_radians,
            orders=orders,
            maximum_order=maximum_order,
            target_epsilon=target_epsilon,
            alpha=alpha,
            num_moments=num_moments,
            cert_tol=cert_tol,
            early_stop=early_stop,
        )
    if mode == "split_sample":
        return certify_rank_unrestricted_split_sample(
            collapsed,
            symbol="w",
            max_ray_power=max_repetitions,
            theta_radians=theta_radians,
            orders=orders,
            maximum_order=maximum_order,
            target_epsilon=target_epsilon,
            alpha=alpha,
            pilot_fraction=pilot_fraction,
            rng=rng,
            num_moments=num_moments,
            cert_tol=cert_tol,
            early_stop=early_stop,
        )
    raise ValueError(f"unknown mode {mode!r}; expected 'fourier_cap' or 'split_sample'")


# ---------------------------------------------------------------------------
# Theorem 4: Unconditional Short-Depth Multi-Symbol Spectral Rank Obstruction
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class UnconditionalSpectralRankReport:
    """Unconditional (zero rank-upper-bound) classical state lower bound via Weyl + Matrix Hoeffding."""

    max_prefix_length: int
    max_suffix_length: int
    max_word_length: int
    unary_shift_register_ceiling: int
    hankel_shape: tuple[int, int]
    unique_word_count: int
    total_shots: int | None
    alpha: float | None
    target_epsilon: float
    hoeffding_operator_radius: float
    epsilon_operator_padding: float
    svd_numerical_guard: float
    total_threshold: float
    certified_classical_state_lower_bound: int
    breaks_unary_ceiling: bool
    top_singular_values: tuple[float, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "max_prefix_length": self.max_prefix_length,
            "max_suffix_length": self.max_suffix_length,
            "max_word_length": self.max_word_length,
            "unary_shift_register_ceiling": self.unary_shift_register_ceiling,
            "hankel_shape": list(self.hankel_shape),
            "unique_word_count": self.unique_word_count,
            "total_shots": self.total_shots,
            "alpha": self.alpha,
            "confidence_level": None if self.alpha is None else 1.0 - self.alpha,
            "target_epsilon": self.target_epsilon,
            "hoeffding_operator_radius": self.hoeffding_operator_radius,
            "epsilon_operator_padding": self.epsilon_operator_padding,
            "svd_numerical_guard": self.svd_numerical_guard,
            "total_threshold": self.total_threshold,
            "certified_classical_state_lower_bound": self.certified_classical_state_lower_bound,
            "breaks_unary_ceiling": self.breaks_unary_ceiling,
            "top_singular_values": list(self.top_singular_values),
            "epistemic_status": (
                "PROVED & CERTIFIED unconditional rank-unrestricted lower bound on "
                "C_classical(f; eps, W_L) via Weyl's singular-value inequality and "
                "Hankel Matrix Hoeffding (ANANKE v2 Theorem 2). ZERO rank upper-bound assumption."
            ),
        }


def certify_unconditional_hankel_rank_noiseless(
    hankel_matrix: FloatArray,
    max_prefix_length: int,
    max_suffix_length: int,
    *,
    alphabet_size: int = 2,
    target_epsilon: float = 0.0,
) -> UnconditionalSpectralRankReport:
    """Certify C_classical(f; eps, W_L) >= r unconditionally from exact Hankel singular values.

    For ANY N-state classical model g with ||H_f - H_g||_inf <= eps:
        ||H_f - H_g||_2 <= ||H_f - H_g||_F <= sqrt(m * n) * eps,
    so by Weyl's inequality sigma_r(H_f) > sqrt(m * n) * eps implies rank(H_g) >= r,
    hence N >= rank(H_g) >= r with ZERO rank upper-bound assumption.
    """
    if target_epsilon < 0.0:
        raise ValueError("target_epsilon must be non-negative")
    if max_prefix_length < 0 or max_suffix_length < 0 or alphabet_size < 1:
        raise ValueError("max_prefix_length, max_suffix_length must be >= 0 and alphabet_size >= 1")
    h = np.asarray(hankel_matrix, dtype=float)
    if h.ndim != 2 or not np.all(np.isfinite(h)):
        raise ValueError("hankel_matrix must be a finite 2D array")
    m, n = h.shape
    exp_m = (
        int(max_prefix_length) + 1
        if alphabet_size == 1
        else int((alphabet_size ** (int(max_prefix_length) + 1) - 1) // (alphabet_size - 1))
    )
    exp_n = (
        int(max_suffix_length) + 1
        if alphabet_size == 1
        else int((alphabet_size ** (int(max_suffix_length) + 1) - 1) // (alphabet_size - 1))
    )
    if (m, n) != (exp_m, exp_n):
        raise ValueError(
            f"hankel_matrix shape {(m, n)} does not match expected {(exp_m, exp_n)} "
            f"for prefix_depth={max_prefix_length}, suffix_depth={max_suffix_length}, alphabet_size={alphabet_size}"
        )
    sv = np.linalg.svd(h, compute_uv=False)
    svd_guard = _svd_numerical_guard(h)
    eps_pad = float(sqrt(float(m * n)) * target_epsilon * _ROUNDING_GUARD)
    thresh = eps_pad + svd_guard
    lb = int(np.count_nonzero(sv > thresh))
    max_len = int(max_prefix_length + max_suffix_length)
    unary_ceil = max_len + 1
    unique_count = (
        max_len + 1
        if alphabet_size == 1
        else int((alphabet_size ** (max_len + 1) - 1) // (alphabet_size - 1))
    )
    return UnconditionalSpectralRankReport(
        max_prefix_length=int(max_prefix_length),
        max_suffix_length=int(max_suffix_length),
        max_word_length=max_len,
        unary_shift_register_ceiling=unary_ceil,
        hankel_shape=(m, n),
        unique_word_count=unique_count,
        total_shots=None,
        alpha=None,
        target_epsilon=float(target_epsilon),
        hoeffding_operator_radius=0.0,
        epsilon_operator_padding=eps_pad,
        svd_numerical_guard=svd_guard,
        total_threshold=thresh,
        certified_classical_state_lower_bound=lb,
        breaks_unary_ceiling=lb > unary_ceil,
        top_singular_values=tuple(float(v) for v in sv[: min(len(sv), 32)]),
    )


def certify_unconditional_hankel_rank_finite_shot(
    dataset: ShotDataset,
    max_prefix_length: int,
    max_suffix_length: int,
    *,
    target_epsilon: float = 0.0,
    alpha: float = 0.01,
) -> UnconditionalSpectralRankReport:
    """Certify C_classical(f; eps, W_L) >= r with (1 - alpha) finite-shot confidence (Theorem 4).

    Uses ONLY the unshifted Hankel block H[u, v] = f(uv) (words of length <= L1 + L2)
    and ANANKE v2's proved Hankel Matrix Hoeffding inequality:
        Pr(||H_hat - H_f||_2 > eps_H(alpha)) <= alpha.
    Combined with ||H_f - H_g||_2 <= sqrt(m*n)*eps and Weyl's inequality:
        sigma_hat_r > eps_H(alpha) + sqrt(m*n)*eps + svd_guard  =>  N >= rank(H_g) >= r.
    """
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    if target_epsilon < 0.0:
        raise ValueError("target_epsilon must be non-negative")

    prefixes = tuple(words_upto(dataset.alphabet, int(max_prefix_length)))
    suffixes = tuple(words_upto(dataset.alphabet, int(max_suffix_length)))
    unique_words = sorted(
        {u + v for u in prefixes for v in suffixes},
        key=lambda w: (len(w), w),
    )
    dataset.require_words(unique_words)

    h_hat = np.array(
        [[dataset.empirical_rate(u + v) for v in suffixes] for u in prefixes],
        dtype=float,
    )
    m, n = h_hat.shape
    sv = np.linalg.svd(h_hat, compute_uv=False)

    # Exact Hankel Matrix Hoeffding radius (ANANKE v2 Theorem 2)
    eps_h = hankel_matrix_hoeffding_bound(
        dataset, int(max_prefix_length), int(max_suffix_length), delta=alpha
    )
    eps_pad = float(sqrt(float(m * n)) * target_epsilon * _ROUNDING_GUARD)
    svd_guard = _svd_numerical_guard(h_hat)
    thresh = eps_h + eps_pad + svd_guard
    lb = int(np.count_nonzero(sv > thresh))

    max_len = int(max_prefix_length + max_suffix_length)
    unary_ceil = max_len + 1
    total_shots = int(sum(dataset.trials[w] for w in unique_words))

    return UnconditionalSpectralRankReport(
        max_prefix_length=int(max_prefix_length),
        max_suffix_length=int(max_suffix_length),
        max_word_length=max_len,
        unary_shift_register_ceiling=unary_ceil,
        hankel_shape=(m, n),
        unique_word_count=len(unique_words),
        total_shots=total_shots,
        alpha=float(alpha),
        target_epsilon=float(target_epsilon),
        hoeffding_operator_radius=float(eps_h),
        epsilon_operator_padding=eps_pad,
        svd_numerical_guard=svd_guard,
        total_threshold=float(thresh),
        certified_classical_state_lower_bound=lb,
        breaks_unary_ceiling=lb > unary_ceil,
        top_singular_values=tuple(float(v) for v in sv[: min(len(sv), 32)]),
    )
