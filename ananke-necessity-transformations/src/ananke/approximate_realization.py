"""Constructive classical stochastic counterfeits (upper bounds on C_classical(f; eps, W)).

Provides explicit, strictly verified N-state classical stochastic realizations
(p in Delta_N, M_a >= 0, M_a 1 = 1, e in [0, 1]^N) to establish honest UPPER
bounds on approximate counterfeit complexity and contrast them directly against
the proved rank-unrestricted lower bounds of ``rank_unrestricted.py``.

Constructions implemented:
1. Acyclic Shift-Register Counterfeit (EXACT, PROVED):
   Matches ANY unary probability sequence of length L+1 with N = L + 1 states
   and EXACT error 0.0 (proving C_classical(f; 0, {a^k : k <= L}) <= L + 1 and
   explicitly demonstrating why v2's L = 7 unary block cannot exclude N >= 8
   without a rank upper bound).

2. Exact Ito / Karpelevič-Boundary Stochastic Matrix & Unary Counterfeit
   (EXACT CONSTRUCTION, PROVED):
   Constructs an explicit N x N row-stochastic matrix attaining the exact
   Karpelevič boundary eigenvalue rho_N(theta) * e^{i*theta} on any Farey arc,
   plus exact LP optimization of the response vector e in [0, 1]^N and initial
   state p in Delta_N.

3. Unconstrained High-Rank Unary Classical HMM Optimizer (NUMERICAL):
   Multi-start L-BFGS-B search over arbitrary-rank N-state classical models
   (warm-started from Ito boundary matrices and random initializations) + LP
   polish of e in [0, 1]^N.

4. Two-Symbol Bloch-Polytope Classical Counterfeit (EXACT LP CONSTRUCTION):
   Constructs valid N-state classical realizations of a two-symbol qubit
   {x, z} via spherical polytopes (Platonic solids / Fibonacci spherical codes)
   and exact barycentric LP transitions.

5. Static Simplex-Box NMF Probe (NUMERICAL):
   Measures the static (zero-dynamics) factorization error min ||H_f - P Q||_inf
   with P in Delta_N^m, Q in [0, 1]^{N x n}.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, cos, pi, sin, sqrt
from typing import Mapping, Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import linprog, minimize

from .karpelevich import farey_sequence, karpelevich_boundary_radius
from .process import LinearProcess

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class ClassicalRealization:
    """A verified finite-state classical stochastic realization (p, {M_a}, e)."""

    alphabet: tuple[str, ...]
    initial: FloatArray
    transitions: Mapping[str, FloatArray]
    final: FloatArray
    construction: str = "generic"

    def __post_init__(self) -> None:
        validate_classical_realization(
            self.alphabet, self.initial, self.transitions, self.final
        )

    @property
    def state_count(self) -> int:
        return int(self.initial.size)

    def to_linear_process(self) -> LinearProcess:
        return LinearProcess(
            alphabet=self.alphabet,
            initial=self.initial,
            transitions=self.transitions,
            final=self.final,
        )

    def behavior(self, word: str) -> float:
        return self.to_linear_process().behavior(word)

    def evaluate_unary_ray(
        self,
        symbol: str,
        max_power: int,
        *,
        prefix: str = "",
        suffix: str = "",
    ) -> FloatArray:
        if symbol not in self.transitions:
            raise ValueError(f"unknown symbol {symbol!r}")
        proc = self.to_linear_process()
        row = proc.row_after(prefix)
        mat = self.transitions[symbol]
        # Precompute suffix effect vector M_suffix @ e
        eff = self.final.copy()
        for ch in reversed(suffix):
            eff = self.transitions[ch] @ eff
        out = np.empty(max_power + 1, dtype=float)
        for k in range(max_power + 1):
            out[k] = float(row @ eff)
            row = row @ mat
        return out

    def error_on_words(
        self,
        target: LinearProcess,
        words: Sequence[str],
    ) -> tuple[float, float]:
        """Return ``(max_abs_error, rms_error)`` against ``target`` on ``words``."""
        proc = self.to_linear_process()
        diffs = np.array([proc.behavior(w) - target.behavior(w) for w in words], dtype=float)
        return float(np.max(np.abs(diffs))), float(np.sqrt(np.mean(diffs * diffs)))


def validate_classical_realization(
    alphabet: Sequence[str],
    initial: FloatArray,
    transitions: Mapping[str, FloatArray],
    final: FloatArray,
    *,
    tol: float = 1e-8,
) -> None:
    """Strictly verify p in Delta_N, M_a >= 0, M_a 1 = 1, e in [0, 1]^N."""
    p = np.asarray(initial, dtype=float).reshape(-1)
    e = np.asarray(final, dtype=float).reshape(-1)
    n = p.size
    if n == 0 or e.size != n:
        raise ValueError("initial and final must be non-empty vectors of equal length")
    if np.any(p < -tol) or abs(float(np.sum(p)) - 1.0) > tol:
        raise ValueError(
            f"initial distribution violates simplex constraint: min={p.min()}, sum={p.sum()}"
        )
    if np.any(e < -tol) or np.any(e > 1.0 + tol):
        raise ValueError(
            f"response vector violates [0, 1] bounds: min={e.min()}, max={e.max()}"
        )
    for sym in alphabet:
        if sym not in transitions:
            raise ValueError(f"missing transition matrix for {sym!r}")
        mat = np.asarray(transitions[sym], dtype=float)
        if mat.shape != (n, n):
            raise ValueError(f"transition {sym!r} has shape {mat.shape}, expected {(n, n)}")
        if np.any(mat < -tol):
            raise ValueError(f"transition {sym!r} has negative entry {mat.min()}")
        row_err = float(np.max(np.abs(mat.sum(axis=1) - 1.0)))
        if row_err > tol:
            raise ValueError(f"transition {sym!r} row sums deviate from 1 by {row_err}")


def construct_shift_register_counterfeit(
    target_values: Sequence[float],
    *,
    symbol: str = "x",
) -> ClassicalRealization:
    """Construct the exact (L+1)-state acyclic shift register matching target_values[0..L].

    PROVED upper bound: C_classical(f; 0, {a^k : 0 <= k <= L}) <= L + 1.
    """
    vals = np.asarray(target_values, dtype=float).reshape(-1)
    if vals.size == 0:
        raise ValueError("target_values must not be empty")
    if np.any(vals < -1e-12) or np.any(vals > 1.0 + 1e-12):
        raise ValueError("target_values must lie in [0, 1]")
    vals = np.clip(vals, 0.0, 1.0)
    n = int(vals.size)
    p = np.zeros(n, dtype=float)
    p[0] = 1.0
    m = np.zeros((n, n), dtype=float)
    for i in range(n - 1):
        m[i, i + 1] = 1.0
    m[n - 1, n - 1] = 1.0
    return ClassicalRealization(
        alphabet=(symbol,),
        initial=p,
        transitions={symbol: m},
        final=vals,
        construction="acyclic_shift_register_exact",
    )


def _solve_ito_mixing_parameter(
    q: int,
    d: int,
    s: int,
    lam: complex,
) -> float:
    """Solve |(lam^q - t)| = (1 - t) * |lam|^{(q*d - s)/d} for exact t in [0, 1]."""
    lam_q = lam**q
    rho = abs(lam)
    alpha = (rho ** ((q * d - s) / float(d))) ** 2
    # |lam_q - t|^2 = alpha * (1 - t)^2
    # (1 - alpha) t^2 + 2 (alpha - Re(lam_q)) t + (|lam_q|^2 - alpha) = 0
    a_coef = 1.0 - alpha
    b_coef = 2.0 * (alpha - lam_q.real)
    c_coef = (lam_q.real**2 + lam_q.imag**2) - alpha
    candidates: list[float] = []
    if abs(a_coef) < 1e-14:
        if abs(b_coef) > 1e-14:
            candidates.append(-c_coef / b_coef)
    else:
        disc = max(0.0, b_coef * b_coef - 4.0 * a_coef * c_coef)
        sq = sqrt(disc)
        candidates.append((-b_coef - sq) / (2.0 * a_coef))
        candidates.append((-b_coef + sq) / (2.0 * a_coef))
    # Also test boundary endpoints 0 and 1
    candidates.extend([0.0, 1.0])

    # Evaluate exact characteristic polynomial residual for each feasible t in [0, 1]
    best_t = 0.0
    best_res = float("inf")
    for t_raw in candidates:
        t = float(np.clip(t_raw, 0.0, 1.0))
        if q * d >= s:
            res = abs((lam_q - t) ** d - ((1.0 - t) ** d) * (lam ** (q * d - s)))
        else:
            res = abs((lam ** (s - q * d)) * ((lam_q - t) ** d) - (1.0 - t) ** d)
        if res < best_res:
            best_res = res
            best_t = t
    return best_t


def construct_karpelevich_boundary_matrix(
    order: int,
    theta_radians: float,
) -> FloatArray:
    """Construct an exact N x N row-stochastic matrix attaining rho_N(theta) * e^{i*theta}.

    Implements Ito's (1997) / Karpelevič's (1951) exact boundary stochastic matrix
    for every Farey arc (p/q, r/s) of F_N (N >= 2).
    """
    n = int(order)
    if n < 2:
        raise ValueError("order must be at least 2")

    turns = (float(theta_radians) / (2.0 * pi)) % 1.0
    if n == 2:
        # Theta_2 = [-1, 1]
        if abs(turns) < 1e-12 or abs(turns - 1.0) < 1e-12:
            return np.eye(2, dtype=float)
        if abs(turns - 0.5) < 1e-12:
            return np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
        return np.full((2, 2), 0.5, dtype=float)

    seq = farey_sequence(n)
    fl, fr = seq[0], seq[1]
    for idx in range(len(seq) - 1):
        if float(seq[idx]) <= turns <= float(seq[idx + 1]) + 1e-15:
            fl, fr = seq[idx], seq[idx + 1]
            break

    # Check exact Farey vertex
    if abs(turns - float(fl)) < 1e-12 or abs(turns - float(fr)) < 1e-12:
        q_v = fl.denominator if abs(turns - float(fl)) < 1e-12 else fr.denominator
        mat = np.eye(n, dtype=float)
        if q_v >= 2:
            mat[:q_v, :q_v] = 0.0
            for i in range(q_v):
                mat[i, (i + 1) % q_v] = 1.0
        return mat

    p, q = fl.numerator, fl.denominator
    r, s = fr.numerator, fr.denominator
    theta_eval = float(theta_radians) % (2.0 * pi)
    if q > s:
        p, q, r, s = s - r, s, q - p, q
        theta_eval = 2.0 * pi - theta_eval

    d = n // q
    rho = karpelevich_boundary_radius(n, theta_eval)
    lam = rho * complex(cos(theta_eval), sin(theta_eval))
    t = _solve_ito_mixing_parameter(q, d, s, lam)

    mat = np.zeros((n, n), dtype=float)
    qd = q * d
    if qd >= s:
        # Type I: d blocks of length q (total q*d states <= N), outer return shifted by r_shift = q*d - s < q
        r_shift = qd - s
        for b in range(d):
            base = b * q
            for j in range(q - 1):
                mat[base + j, base + j + 1] = 1.0
            end_state = base + q - 1
            mat[end_state, base] += t
            if b < d - 1:
                mat[end_state, (b + 1) * q] += 1.0 - t
            else:
                mat[end_state, r_shift] += 1.0 - t
        for extra in range(qd, n):
            mat[extra, extra] = 1.0
    else:
        # Type II: d blocks of length q plus r_extra = s - q*d chain states (total s <= N)
        r_extra = s - qd
        for b in range(d):
            base = b * q
            for j in range(q - 1):
                mat[base + j, base + j + 1] = 1.0
            end_state = base + q - 1
            mat[end_state, base] += t
            if b < d - 1:
                mat[end_state, (b + 1) * q] += 1.0 - t
            else:
                mat[end_state, qd] += 1.0 - t
        for idx_e in range(r_extra - 1):
            mat[qd + idx_e, qd + idx_e + 1] = 1.0
        mat[qd + r_extra - 1, 0] = 1.0
        for extra in range(s, n):
            mat[extra, extra] = 1.0

    return mat


def _solve_optimal_response_lp(
    trajectory: FloatArray,
    target_values: FloatArray,
) -> tuple[FloatArray, float]:
    """Given trajectory rows P[k] = p M^k (shape (L+1, N)), find e in [0,1]^N minimizing ||P e - y||_inf."""
    l1, n = trajectory.shape
    # Variables: [e_0, ..., e_{N-1}, tau]
    c = np.zeros(n + 1, dtype=float)
    c[n] = 1.0
    a_ub = np.vstack(
        [
            np.hstack([trajectory, -np.ones((l1, 1), dtype=float)]),
            np.hstack([-trajectory, -np.ones((l1, 1), dtype=float)]),
        ]
    )
    b_ub = np.concatenate([target_values, -target_values])
    bounds = [(0.0, 1.0)] * n + [(0.0, None)]
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success or res.x is None:
        return np.full(n, 0.5, dtype=float), float(np.max(np.abs(target_values - 0.5)))
    e = np.clip(res.x[:n], 0.0, 1.0)
    err = float(np.max(np.abs(trajectory @ e - target_values)))
    return e, err


def _solve_optimal_initial_lp(
    effect_traj: FloatArray,
    target_values: FloatArray,
) -> tuple[FloatArray, float]:
    """Given columns E[k] = M^k e (shape (L+1, N)), find p in Delta_N minimizing ||E p - y||_inf."""
    l1, n = effect_traj.shape
    c = np.zeros(n + 1, dtype=float)
    c[n] = 1.0
    a_ub = np.vstack(
        [
            np.hstack([effect_traj, -np.ones((l1, 1), dtype=float)]),
            np.hstack([-effect_traj, -np.ones((l1, 1), dtype=float)]),
        ]
    )
    b_ub = np.concatenate([target_values, -target_values])
    a_eq = np.zeros((1, n + 1), dtype=float)
    a_eq[0, :n] = 1.0
    b_eq = np.array([1.0], dtype=float)
    bounds = [(0.0, 1.0)] * n + [(0.0, None)]
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success or res.x is None:
        p = np.full(n, 1.0 / n, dtype=float)
        return p, float(np.max(np.abs(effect_traj @ p - target_values)))
    p = np.clip(res.x[:n], 0.0, 1.0)
    p /= float(np.sum(p))
    err = float(np.max(np.abs(effect_traj @ p - target_values)))
    return p, err


def _fit_pe_for_fixed_matrix(
    mat: FloatArray,
    target_values: FloatArray,
    *,
    alt_steps: int = 4,
) -> tuple[FloatArray, FloatArray, float]:
    """Find best (p in Delta_N, e in [0,1]^N) for fixed stochastic M by vertex starts + alternating LP."""
    n = mat.shape[0]
    l1 = target_values.size
    # Precompute powers M^k for k=0..L
    powers = [np.eye(n, dtype=float)]
    for _ in range(l1 - 1):
        powers.append(powers[-1] @ mat)

    best_err = float("inf")
    best_p = np.full(n, 1.0 / n, dtype=float)
    best_e = np.full(n, 0.5, dtype=float)

    for start_idx in range(n):
        p = np.zeros(n, dtype=float)
        p[start_idx] = 1.0
        for _ in range(alt_steps):
            traj = np.array([p @ pk for pk in powers], dtype=float)
            e, err = _solve_optimal_response_lp(traj, target_values)
            eff = np.array([pk @ e for pk in powers], dtype=float)
            p, err = _solve_optimal_initial_lp(eff, target_values)
        if err < best_err:
            best_err = err
            best_p = p
            best_e = e
    return best_p, best_e, best_err


@dataclass(frozen=True)
class UnaryCounterfeitResult:
    """Verified N-state classical counterfeit and its achieved error on a unary ray."""

    realization: ClassicalRealization
    max_error: float
    rms_error: float
    method: str

    def to_dict(self) -> dict[str, object]:
        return {
            "state_count": self.realization.state_count,
            "max_error": self.max_error,
            "rms_error": self.rms_error,
            "method": self.method,
            "construction": self.realization.construction,
        }


def construct_karpelevich_unary_counterfeit(
    target_values: Sequence[float],
    order: int,
    theta_radians: float,
    *,
    symbol: str = "x",
) -> UnaryCounterfeitResult:
    """Construct best structured N-state counterfeit from Ito boundary + nearest Farey cycles.

    Checks:
      (1) exact Ito/Karpelevič boundary matrix M_N(theta),
      (2) deterministic q-cycles for q <= N (padded to N),
      (3) acyclic shift register if N >= len(target_values).
    Returns the strictly verified classical realization with smallest L_inf error.
    """
    vals = np.asarray(target_values, dtype=float).reshape(-1)
    n = int(order)
    if n >= vals.size:
        sr = construct_shift_register_counterfeit(vals, symbol=symbol)
        # Pad to n states if n > vals.size
        if n > vals.size:
            pad = n - vals.size
            p = np.concatenate([sr.initial, np.zeros(pad)])
            e = np.concatenate([sr.final, np.zeros(pad)])
            m = np.eye(n, dtype=float)
            m[: vals.size, : vals.size] = sr.transitions[symbol]
            sr = ClassicalRealization(
                (symbol,), p, {symbol: m}, e, construction="acyclic_shift_register_exact"
            )
        return UnaryCounterfeitResult(sr, 0.0, 0.0, "acyclic_shift_register_exact")

    candidates: list[tuple[str, FloatArray]] = [
        ("ito_karpelevich_boundary", construct_karpelevich_boundary_matrix(n, theta_radians))
    ]
    # Also test pure deterministic cycles of period q in [max(2, n-3), n]
    for q in range(max(2, n - 3), n + 1):
        c_mat = np.eye(n, dtype=float)
        c_mat[:q, :q] = 0.0
        for i in range(q):
            c_mat[i, (i + 1) % q] = 1.0
        candidates.append((f"deterministic_{q}_cycle", c_mat))

    best_res: UnaryCounterfeitResult | None = None
    for name, mat in candidates:
        p, e, _ = _fit_pe_for_fixed_matrix(mat, vals)
        real = ClassicalRealization((symbol,), p, {symbol: mat}, e, construction=name)
        preds = real.evaluate_unary_ray(symbol, vals.size - 1)
        diff = np.abs(preds - vals)
        mx = float(np.max(diff))
        rms = float(np.sqrt(np.mean(diff * diff)))
        if best_res is None or mx < best_res.max_error:
            best_res = UnaryCounterfeitResult(real, mx, rms, name)

    assert best_res is not None
    return best_res


def optimize_unary_classical_counterfeit(
    target_values: Sequence[float],
    order: int,
    *,
    theta_radians: float | None = None,
    symbol: str = "x",
    restarts: int = 8,
    maxiter: int = 250,
    seed: int = 0,
) -> UnaryCounterfeitResult:
    """Numerically search arbitrary-rank N-state classical counterfeits on a unary ray.

    Starts from both structured Karpelevič/cycle initializations (if theta_radians
    is given) and random stochastic matrices, then polishes (p, e) by exact LP.
    """
    vals = np.asarray(target_values, dtype=float).reshape(-1)
    n = int(order)
    l_max = vals.size - 1

    best: UnaryCounterfeitResult | None = None
    if theta_radians is not None:
        best = construct_karpelevich_unary_counterfeit(
            vals, n, theta_radians, symbol=symbol
        )
        if best.max_error <= 1e-12:
            return best

    rng = np.random.default_rng(seed)

    def _unpack(x: FloatArray) -> tuple[FloatArray, FloatArray, FloatArray]:
        logits_m = x[: n * n].reshape(n, n)
        logits_m = logits_m - np.max(logits_m, axis=1, keepdims=True)
        exp_m = np.exp(np.clip(logits_m, -40.0, 0.0))
        m_mat = exp_m / np.sum(exp_m, axis=1, keepdims=True)

        logits_p = x[n * n : n * n + n]
        logits_p = logits_p - np.max(logits_p)
        exp_p = np.exp(np.clip(logits_p, -40.0, 0.0))
        p_vec = exp_p / np.sum(exp_p)

        e_vec = 1.0 / (1.0 + np.exp(-np.clip(x[n * n + n :], -30.0, 30.0)))
        return p_vec, m_mat, e_vec

    def _loss(x: FloatArray) -> float:
        p_vec, m_mat, e_vec = _unpack(x)
        preds = np.empty(l_max + 1, dtype=float)
        v = p_vec
        for k in range(l_max + 1):
            preds[k] = float(v @ e_vec)
            v = v @ m_mat
        diff = preds - vals
        return float(np.mean(diff * diff) + 0.05 * np.max(diff * diff))

    for r in range(int(restarts)):
        if r == 0 and best is not None:
            # Warm start near Ito/structured solution
            m0 = np.clip(best.realization.transitions[symbol], 1e-3, 1.0)
            p0 = np.clip(best.realization.initial, 1e-3, 1.0)
            e0 = np.clip(best.realization.final, 1e-3, 1.0 - 1e-3)
            x0 = np.concatenate(
                [
                    np.log(m0).reshape(-1) + rng.normal(0, 0.15, size=n * n),
                    np.log(p0),
                    np.log(e0 / (1.0 - e0)),
                ]
            )
        else:
            x0 = rng.normal(0.0, 1.5, size=n * n + 2 * n)
        res = minimize(_loss, x0, method="L-BFGS-B", options={"maxiter": maxiter})
        _, m_opt, _ = _unpack(res.x)
        # Exact LP polish of (p, e) for the optimized stochastic matrix M
        p_lp, e_lp, _ = _fit_pe_for_fixed_matrix(m_opt, vals, alt_steps=3)
        real = ClassicalRealization(
            (symbol,), p_lp, {symbol: m_opt}, e_lp, construction="numerical_lbfgs_lp_polish"
        )
        preds = real.evaluate_unary_ray(symbol, l_max)
        diff = np.abs(preds - vals)
        mx = float(np.max(diff))
        rms = float(np.sqrt(np.mean(diff * diff)))
        if best is None or mx < best.max_error:
            best = UnaryCounterfeitResult(real, mx, rms, "numerical_lbfgs_lp_polish")

    assert best is not None
    return best


def _spherical_polytope_vertices(order: int) -> FloatArray:
    """Return N well-distributed unit vectors on S^2 (exact Platonic for N=4,6,8,12, else Fibonacci)."""
    n = int(order)
    if n < 4:
        raise ValueError("3D Bloch polytope requires at least 4 vertices")
    if n == 4:
        v = np.array(
            [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float
        )
        return v / np.linalg.norm(v, axis=1, keepdims=True)
    if n == 6:
        return np.array(
            [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]],
            dtype=float,
        )
    if n == 8:
        v = np.array(
            [[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)],
            dtype=float,
        )
        return v / np.linalg.norm(v, axis=1, keepdims=True)
    if n == 12:
        phi = 0.5 * (1.0 + sqrt(5.0))
        raw = [
            (0, s1, s2 * phi) for s1 in (-1, 1) for s2 in (-1, 1)
        ] + [
            (s1, s2 * phi, 0) for s1 in (-1, 1) for s2 in (-1, 1)
        ] + [
            (s2 * phi, 0, s1) for s1 in (-1, 1) for s2 in (-1, 1)
        ]
        v = np.array(raw, dtype=float)
        return v / np.linalg.norm(v, axis=1, keepdims=True)

    idx = np.arange(n, dtype=float) + 0.5
    phi = np.arccos(1.0 - 2.0 * idx / n)
    theta = pi * (1.0 + sqrt(5.0)) * idx
    return np.column_stack(
        [np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta), np.cos(phi)]
    )


@dataclass(frozen=True)
class BlochPolytopeCounterfeitResult:
    """Explicit N-state two-symbol classical counterfeit via Bloch polytope discretization."""

    realization: ClassicalRealization
    inradius_rho: float
    initial_rho: float
    max_error: float
    rms_error: float
    word_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "state_count": self.realization.state_count,
            "inradius_rho": self.inradius_rho,
            "initial_rho": self.initial_rho,
            "max_error": self.max_error,
            "rms_error": self.rms_error,
            "word_count": self.word_count,
            "construction": self.realization.construction,
        }


def construct_bloch_polytope_counterfeit(
    qubit_process: LinearProcess,
    order: int,
    words: Sequence[str],
) -> BlochPolytopeCounterfeitResult:
    """Construct an explicit N-state classical realization of a 2-symbol qubit via Bloch polytope LPs."""
    if qubit_process.dimension != 4:
        raise ValueError("qubit_process must be a 4D homogeneous Bloch LinearProcess")
    n = int(order)
    verts = _spherical_polytope_vertices(n)  # (N, 3)

    r0 = qubit_process.initial[1:]
    m_vec = 2.0 * qubit_process.final[1:]
    rot_mats = {
        sym: qubit_process.transitions[sym].T[1:, 1:]
        for sym in qubit_process.alphabet
    }

    def _max_barycentric(u: FloatArray) -> tuple[float, FloatArray]:
        c = np.zeros(n + 1, dtype=float)
        c[n] = -1.0
        a_eq = np.zeros((4, n + 1), dtype=float)
        a_eq[:3, :n] = verts.T
        a_eq[:3, n] = -u
        a_eq[3, :n] = 1.0
        b_eq = np.array([0.0, 0.0, 0.0, 1.0], dtype=float)
        bounds = [(0.0, 1.0)] * n + [(0.0, 1.0)]
        res = linprog(c, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if not res.success or res.x is None:
            return 0.0, np.full(n, 1.0 / n, dtype=float)
        p = np.clip(res.x[:n], 0.0, 1.0)
        p /= float(np.sum(p))
        return float(res.x[n]), p

    rho_0, p_init = _max_barycentric(r0)
    transitions: dict[str, FloatArray] = {}
    min_rho = 1.0
    for sym, rot in rot_mats.items():
        mat = np.zeros((n, n), dtype=float)
        for i in range(n):
            rho_i, row_i = _max_barycentric(rot @ verts[i])
            min_rho = min(min_rho, rho_i)
            mat[i] = row_i
        transitions[sym] = mat

    e_vec = np.clip(0.5 * (1.0 + verts @ m_vec), 0.0, 1.0)
    real = ClassicalRealization(
        alphabet=qubit_process.alphabet,
        initial=p_init,
        transitions=transitions,
        final=e_vec,
        construction="bloch_polytope_barycentric_lp",
    )
    mx, rms = real.error_on_words(qubit_process, words)
    return BlochPolytopeCounterfeitResult(
        realization=real,
        inradius_rho=min_rho,
        initial_rho=rho_0,
        max_error=mx,
        rms_error=rms,
        word_count=len(words),
    )


def fit_static_simplex_box_nmf(
    hankel_matrix: FloatArray,
    order: int,
    *,
    restarts: int = 8,
    iterations: int = 180,
    seed: int = 0,
) -> tuple[float, float]:
    """Numerical upper bound on static simplex-box factorization min ||H - P Q||_inf.

    Enforces P in Delta_N^m (nonnegative, row sums 1) and Q in [0, 1]^{N x n}.
    Returns ``(max_abs_error, frobenius_error)``.
    """
    h = np.asarray(hankel_matrix, dtype=float)
    m, n_cols = h.shape
    k = int(order)
    rng = np.random.default_rng(seed)
    best_max = float("inf")
    best_fro = float("inf")

    for _ in range(int(restarts)):
        p_mat = rng.dirichlet(np.ones(k, dtype=float), size=m)
        q_mat = rng.uniform(0.0, 1.0, size=(k, n_cols))
        for _ in range(int(iterations)):
            ptp = p_mat.T @ p_mat + 1e-10 * np.eye(k)
            pth = p_mat.T @ h
            for _ in range(4):
                for s in range(k):
                    rhs = pth[s] - (ptp[s] @ q_mat - ptp[s, s] * q_mat[s])
                    q_mat[s] = np.clip(rhs / ptp[s, s], 0.0, 1.0)
            qqt = q_mat @ q_mat.T
            hqt = h @ q_mat.T
            step = 1.0 / (float(np.linalg.norm(qqt, 2)) + 1e-9)
            for _ in range(8):
                grad = p_mat @ qqt - hqt
                p_new = p_mat - step * grad
                u_sorted = np.sort(p_new, axis=1)[:, ::-1]
                cssv = np.cumsum(u_sorted, axis=1) - 1.0
                ind = np.arange(1, k + 1, dtype=float)
                cond = u_sorted - cssv / ind > 0.0
                rho = np.sum(cond, axis=1) - 1
                theta = cssv[np.arange(m), rho] / (rho + 1.0)
                p_mat = np.maximum(p_new - theta[:, None], 0.0)
        err = np.abs(h - p_mat @ q_mat)
        mx = float(np.max(err))
        fro = float(np.linalg.norm(err, "fro"))
        if mx < best_max:
            best_max = mx
            best_fro = fro
    return best_max, best_fro
