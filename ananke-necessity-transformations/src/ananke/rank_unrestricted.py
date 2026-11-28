"""Rank-unrestricted approximate counterfeit complexity bounds for ANANKE v3.

Closes the exact-rank loophole of ANANKE v2 (Theorem 3, Epistemic Scope Box)
with genuinely model-independent, rank-unrestricted lower bounds on the
approximate classical counterfeit complexity C_classical(f; eps, W).

Core mathematical theorems (PROVED in docs/ananke_v3_rank_unrestricted.md):

1. Theorem 1 (B-Spline Cayley--Hamilton Spectral Obstruction, PROVED):
   For ANY N-state classical stochastic realization g(w) = p M_w e of ARBITRARY
   rank <= N and arbitrary Jordan structure, along any unary ray w_k = u a^k v:
   Let w^{(N)} = (w^{(1)})^{*N} be the N-fold discrete B-spline window formed
   from the uniform length-M boxcar w^{(1)}, supported on {0, ..., N(M-1)}.
   Let chi(z) = det(z I - M_a) = sum_{j=0}^N c_j z^j.  Because chi(M_a) = 0
   and chi(1) = 0, applying the backward shift identity chi(e^{i*theta} S) =
   sum_{m=0}^N ((-e^{i*theta})^m chi^{(m)}(e^{i*theta}) / m!) nabla^m with
   ||nabla^m w^{(N)}||_1 <= (2/M)^m yields:

     (a) Unconditional Fourier-Amplitude Cap (Mode A, no reference model):
         |sum_{k=0}^{N(M-1)} w^{(N)}_k e^{-ik*theta} (g(w_k) - 1/2)|
             <= 0.5 * (Psi_N(M, theta) - 1),

     (b) Reference-Sinusoid Residual Bound (Mode B, short depth L = N*M):
         For any reference sinusoid s(k) = c_0 + A cos(k*theta + phi):
         (A/2) * (1 - |W^{(N)}(2*theta)|)
             <= Psi_N(M, theta) * max_{0 <= k <= N*M} |g(w_k) - s(k)|,

   where |W^{(N)}(2*theta)| = |sin(M*theta) / (M sin(theta))|^N and
         Psi_N(M, theta) := sup_{A in S_N} prod_{j=1}^N (1 + 2 / (M |e^{i*theta} - lam_j(A)|)).

2. Theorem 2 (Subharmonic Dual Spectral-Measure Certificate, PROVED & CERTIFIED):
   For any nonnegative trace multipliers y_1, ..., y_K >= 0, the function
       psi_{M,y}(lam) = 0.5*ln(1 + 2/(M|z-lam|)) + 0.5*ln(1 + 2/(M|z-conj(lam)|))
                        + sum_{k=1}^K y_k Re(lam^k)
   is strictly subharmonic on C \\ {z, conj(z)} (Laplacian > 0).  By the
   Subharmonic Maximum Principle and tr(A^k) >= 0 for every stochastic matrix A:
       Psi_N(M, theta) <= (1 + 2/(M|z-1|)) * exp(sum_k y_k + (N-1) * sup_{lam in dTheta_N+ U [-1,1]} psi_{M,y}(lam)).
   The 1D boundary supremum is machine-certified using outward-rounded Decimal
   interval branch-and-bound over every Farey arc of Theta_N plus [-1, 1].

3. Theorem 3 (Non-Asymptotic Finite-Shot Rank-Unrestricted Certificates, PROVED):
   Combines Theorems 1--2 with scalar Hoeffding (Mode A) and exact Hypergeometric
   split-sample + simultaneous Chernoff--KL + scalar Hoeffding (Mode B), yielding
   non-asymptotic (1 - alpha)-certified lower bounds on C_classical(f; eps, W)
   with ZERO rank upper-bound assumption.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache
import heapq
from math import cos, exp, log, pi, sin, sqrt
from typing import Sequence

import numpy as np
from scipy.optimize import linprog

from .certified_inference import (
    kl_binomial_confidence_interval,
    split_shot_dataset,
)
from .interval import (
    Interval,
    _ceil_ctx,
    _dec_sqrt_floor,
    _floor_ctx,
    cos_interval,
    exp_interval,
    interval_distance_sq,
    log_interval,
    pi_interval,
    sin_interval,
    two_pi_interval,
)
from .karpelevich import farey_sequence, karpelevich_boundary_radius
from .karpelevich_certified import (
    _FareyArcSpec,
    _certified_gap_bounds_on_t,
    _decimal_to_float_ceil,
)
from .observations import ShotDataset
from .process import LinearProcess

_ZERO = Decimal(0)
_ONE = Decimal(1)
_NEG_ONE = Decimal(-1)
_TWO = Decimal(2)
_HALF = Decimal("0.5")
_ROUNDING_GUARD = 1.0 + 1e-12


def bspline_window(order: int, boxcar_length: int) -> np.ndarray:
    """Return the exact ``order``-fold discrete B-spline window of boxcar length M.

    Supported on ``0, ..., order * (boxcar_length - 1)``, nonnegative, summing to 1.
    """
    d = int(order)
    m = int(boxcar_length)
    if d < 1:
        raise ValueError("order must be at least 1")
    if m < 1:
        raise ValueError("boxcar_length must be at least 1")
    box = np.full(m, 1.0 / m, dtype=float)
    w = box.copy()
    for _ in range(d - 1):
        w = np.convolve(w, box)
    # Normalize against floating-point drift (exact mathematical sum is 1)
    w /= float(np.sum(w))
    return w


def bspline_conjugate_leakage(order: int, boxcar_length: int, theta: float) -> float:
    """Exact magnitude |W^{(d)}(2*theta)| = |sin(M*theta) / (M*sin(theta))|^d."""
    d = int(order)
    m = int(boxcar_length)
    if d < 1 or m < 1:
        raise ValueError("order and boxcar_length must be positive")
    s_den = abs(sin(theta))
    if s_den < 1e-15:
        return 1.0
    ratio = min(1.0, abs(sin(m * theta)) / (m * s_den))
    return float(ratio**d)


def _normalize_angle_upper_half(theta: float) -> float:
    """Map angle to [0, pi] using 2*pi periodicity and conjugation symmetry."""
    t = float(theta) % (2.0 * pi)
    if t > pi:
        t = 2.0 * pi - t
    return t


def _sample_boundary_for_lp(order: int, theta_upper: float) -> np.ndarray:
    """Sample 1D boundary of Theta_order^+ union [-1, 1] for heuristic dual LP."""
    if order == 2:
        xs = np.linspace(-1.0, 1.0, 401)
        return xs.astype(complex)

    seq = farey_sequence(order)
    farey_angs = [2.0 * pi * float(f) for f in seq if float(f) <= 0.5]
    if not farey_angs or farey_angs[-1] < pi:
        farey_angs.append(pi)
    grid = np.unique(
        np.concatenate(
            [
                np.linspace(0.0, pi, 360),
                np.clip(theta_upper + np.linspace(-0.25, 0.25, 160), 0.0, pi),
                np.clip(theta_upper + np.linspace(-0.04, 0.04, 120), 0.0, pi),
                np.array(farey_angs, dtype=float),
            ]
        )
    )
    boundary = [
        karpelevich_boundary_radius(order, float(a)) * np.exp(1j * float(a))
        for a in grid
    ]
    real_seg = np.linspace(-1.0, 1.0, 81).astype(complex)
    return np.concatenate([np.array(boundary, dtype=complex), real_seg])


def _solve_dual_trace_lp(
    order: int,
    boxcar_length: int,
    theta_upper: float,
    *,
    num_moments: int = 10,
) -> tuple[np.ndarray, float]:
    """Heuristic LP for nonnegative trace multipliers y_1, ..., y_K >= 0.

    The LP only proposes dual multipliers y >= 0; rigor comes entirely from
    the subsequent outward-rounded interval branch-and-bound certification.
    """
    z = complex(cos(theta_upper), sin(theta_upper))
    pts = _sample_boundary_for_lp(order, theta_upper)
    d_pos = np.abs(z - pts)
    d_neg = np.abs(z - np.conj(pts))
    if np.min(d_pos) < 1e-14 or np.min(d_neg) < 1e-14:
        return np.zeros(num_moments, dtype=float), float("inf")

    c_scale = 2.0 / float(boxcar_length)
    f_val = 0.5 * (np.log1p(c_scale / d_pos) + np.log1p(c_scale / d_neg))
    k_eff = max(0, int(num_moments))
    if k_eff == 0:
        t_opt = float(np.max(f_val))
        y_opt = np.zeros(0, dtype=float)
    else:
        re_pk = np.array([np.real(pts**k) for k in range(1, k_eff + 1)], dtype=float)
        c_obj = np.zeros(k_eff + 1, dtype=float)
        c_obj[0] = float(order - 1)
        c_obj[1:] = 1.0
        a_ub = np.hstack([-np.ones((len(pts), 1), dtype=float), re_pk.T])
        b_ub = -f_val
        bounds = [(None, None)] + [(0.0, None)] * k_eff
        res = linprog(c_obj, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if not res.success or res.x is None:
            t_opt = float(np.max(f_val))
            y_opt = np.zeros(k_eff, dtype=float)
        else:
            t_opt = float(res.x[0])
            y_opt = np.maximum(0.0, np.asarray(res.x[1:], dtype=float))
            # Prune negligible multipliers so interval certification is fast
            y_opt[y_opt < 1e-7] = 0.0

    log_est = log(1.0 + c_scale / abs(z - 1.0)) + float(np.sum(y_opt)) + (order - 1) * t_opt
    psi_est = exp(min(log_est, 700.0))
    return y_opt, psi_est


def _polar_box_psi_bounds(
    r_iv: Interval,
    alpha_iv: Interval,
    theta_iv: Interval,
    c_iv: Interval,
    active_y: Sequence[tuple[int, Decimal]],
    prec: int,
) -> tuple[Decimal, Decimal]:
    """Return certified (lb, ub) enclosing psi_{M,y}(r e^{i*alpha}) on r_iv x alpha_iv."""
    f_ctx = _floor_ctx(prec)
    c_ctx = _ceil_ctx(prec)

    # Distance to z = e^{i*theta}: |e^{i*theta} - r e^{i*alpha}|^2 = (r - cos(alpha - theta))^2 + sin^2(alpha - theta)
    d_plus = alpha_iv.sub(theta_iv, prec)
    cos_p = cos_interval(d_plus, prec)
    sin_p = sin_interval(d_plus, prec)
    d2_p_lo = f_ctx.add(
        interval_distance_sq(r_iv, cos_p, prec),
        interval_distance_sq(Interval.exact(0), sin_p, prec),
    )
    if d2_p_lo <= _ZERO:
        return (Decimal("-Infinity"), Decimal("Infinity"))
    dist_p_lo = _dec_sqrt_floor(d2_p_lo, prec)
    dist_p_hi = r_iv.sub(cos_p, prec).sqr(prec).add(sin_p.sqr(prec), prec).sqrt(prec).hi

    # Distance to conj(z) = e^{-i*theta}: |e^{i*theta} - r e^{-i*alpha}|^2 = (r - cos(alpha + theta))^2 + sin^2(alpha + theta)
    d_minus = alpha_iv.add(theta_iv, prec)
    cos_m = cos_interval(d_minus, prec)
    sin_m = sin_interval(d_minus, prec)
    d2_m_lo = f_ctx.add(
        interval_distance_sq(r_iv, cos_m, prec),
        interval_distance_sq(Interval.exact(0), sin_m, prec),
    )
    if d2_m_lo <= _ZERO:
        return (Decimal("-Infinity"), Decimal("Infinity"))
    dist_m_lo = _dec_sqrt_floor(d2_m_lo, prec)
    dist_m_hi = r_iv.sub(cos_m, prec).sqr(prec).add(sin_m.sqr(prec), prec).sqrt(prec).hi

    # 0.5 * (ln(1 + c/d_+) + ln(1 + c/d_-)): decreasing in d_+ and d_-
    arg_p = Interval.exact(1).add(c_iv.div(Interval(dist_p_lo, dist_p_hi), prec), prec)
    arg_m = Interval.exact(1).add(c_iv.div(Interval(dist_m_lo, dist_m_hi), prec), prec)
    log_p = log_interval(arg_p, prec)
    log_m = log_interval(arg_m, prec)
    half_iv = Interval(_HALF, _HALF)
    total = half_iv.mul(log_p.add(log_m, prec), prec)

    # Add sum_k y_k * r^k * cos(k * alpha)
    for k, y_k in active_y:
        rk = r_iv.pow_int(k, prec)
        ka = Interval.exact(k).mul(alpha_iv, prec)
        ck = cos_interval(ka, prec)
        term = Interval(y_k, y_k).mul(rk.mul(ck, prec), prec)
        total = total.add(term, prec)

    return (total.lo, total.hi)


def _real_interval_psi_bounds(
    x_iv: Interval,
    cos_theta_iv: Interval,
    sin_theta_sq_iv: Interval,
    c_iv: Interval,
    active_y: Sequence[tuple[int, Decimal]],
    prec: int,
) -> tuple[Decimal, Decimal]:
    """Return certified (lb, ub) enclosing psi_{M,y}(x) for real x in x_iv subset [-1, 1]."""
    f_ctx = _floor_ctx(prec)
    # |e^{i*theta} - x|^2 = (x - cos(theta))^2 + sin^2(theta)
    d2_lo = f_ctx.add(
        interval_distance_sq(x_iv, cos_theta_iv, prec),
        sin_theta_sq_iv.lo,
    )
    if d2_lo <= _ZERO:
        return (Decimal("-Infinity"), Decimal("Infinity"))
    d_lo = _dec_sqrt_floor(d2_lo, prec)
    d_hi = x_iv.sub(cos_theta_iv, prec).sqr(prec).add(sin_theta_sq_iv, prec).sqrt(prec).hi

    arg = Interval.exact(1).add(c_iv.div(Interval(d_lo, d_hi), prec), prec)
    total = log_interval(arg, prec)  # 0.5*(ln + ln) = ln for real x

    for k, y_k in active_y:
        xk = x_iv.pow_int(k, prec)
        total = total.add(Interval(y_k, y_k).mul(xk, prec), prec)

    return (total.lo, total.hi)


@dataclass(frozen=True)
class CertifiedBSplineMultiplier:
    """Machine-certified upper bound on Psi_N(M, theta) over all N x N stochastic matrices."""

    order: int
    boxcar_length: int
    theta_radians: float
    certified: bool
    psi_upper_bound: float
    lp_psi_estimate: float
    dual_multipliers: tuple[float, ...]
    sup_psi_lo: float
    sup_psi_ub: float
    evaluated_subintervals: int
    status: str

    def to_dict(self) -> dict[str, object]:
        return {
            "order": self.order,
            "boxcar_length": self.boxcar_length,
            "theta_radians": self.theta_radians,
            "certified": self.certified,
            "psi_upper_bound": (
                self.psi_upper_bound if np.isfinite(self.psi_upper_bound) else None
            ),
            "lp_psi_estimate": (
                self.lp_psi_estimate if np.isfinite(self.lp_psi_estimate) else None
            ),
            "dual_multipliers": list(self.dual_multipliers),
            "sup_psi_lo": self.sup_psi_lo,
            "sup_psi_ub": self.sup_psi_ub if np.isfinite(self.sup_psi_ub) else None,
            "evaluated_subintervals": self.evaluated_subintervals,
            "status": self.status,
            "certification": (
                "CERTIFIED (outward-rounded Decimal interval branch-and-bound over "
                "dTheta_N+ U [-1, 1] via the proved Subharmonic Maximum Principle)"
                if self.certified
                else "NOT_CERTIFIED"
            ),
        }


@lru_cache(maxsize=512)
def certify_bspline_multiplier(
    order: int,
    boxcar_length: int,
    theta_radians: float,
    *,
    num_moments: int = 10,
    tol: float = 2e-3,
    max_subdivisions: int = 1500,
    prec: int = 20,
) -> CertifiedBSplineMultiplier:
    """Compute a machine-certified upper bound on Psi_N(M, theta).

    Guarantees (PROVED & CERTIFIED):
        For EVERY N x N row-stochastic matrix A (arbitrary rank, arbitrary Jordan form),
            prod_{j=1}^N (1 + 2 / (M * |e^{i*theta} - lam_j(A)|)) <= psi_upper_bound.
    """
    n = int(order)
    m = int(boxcar_length)
    if n < 2:
        raise ValueError("order must be at least 2")
    if m < 1:
        raise ValueError("boxcar_length must be at least 1")
    if tol <= 0.0:
        raise ValueError("tol must be positive")

    theta_u = _normalize_angle_upper_half(theta_radians)
    if theta_u <= 1e-12 or abs(theta_u - pi) <= 1e-12:
        return CertifiedBSplineMultiplier(
            order=n,
            boxcar_length=m,
            theta_radians=float(theta_radians),
            certified=False,
            psi_upper_bound=float("inf"),
            lp_psi_estimate=float("inf"),
            dual_multipliers=(),
            sup_psi_lo=float("inf"),
            sup_psi_ub=float("inf"),
            evaluated_subintervals=0,
            status="angle_on_real_axis",
        )

    y_opt, lp_est = _solve_dual_trace_lp(n, m, theta_u, num_moments=num_moments)
    if not np.isfinite(lp_est):
        return CertifiedBSplineMultiplier(
            order=n,
            boxcar_length=m,
            theta_radians=float(theta_radians),
            certified=False,
            psi_upper_bound=float("inf"),
            lp_psi_estimate=float("inf"),
            dual_multipliers=tuple(float(v) for v in y_opt),
            sup_psi_lo=float("inf"),
            sup_psi_ub=float("inf"),
            evaluated_subintervals=0,
            status="point_on_boundary",
        )

    active_y = [
        (k, Decimal.from_float(float(y_k)))
        for k, y_k in enumerate(y_opt, start=1)
        if y_k > 0.0
    ]
    # Enclose the EXACT supplied angle FIRST, then reduce mod 2*pi and reflect into [0, pi]
    # purely in outward-rounded Decimal interval arithmetic (never via float64 2*pi - theta).
    raw_theta_iv = Interval.from_float(float(theta_radians))
    two_pi_iv = two_pi_interval(prec)
    pi_iv = pi_interval(prec)
    q_iv = raw_theta_iv.div(two_pi_iv, prec)
    from decimal import ROUND_FLOOR

    k_period = int(q_iv.lo.to_integral_value(rounding=ROUND_FLOOR))
    theta_mod = raw_theta_iv.sub(Interval.exact(k_period).mul(two_pi_iv, prec), prec)
    if theta_mod.lo > pi_iv.hi:
        theta_iv = two_pi_iv.sub(theta_mod, prec)
    elif theta_mod.hi < pi_iv.lo:
        theta_iv = theta_mod
    else:
        # Straddles pi: take the symmetric hull of [theta_mod.lo, pi_hi] and [2*pi - theta_mod.hi, pi_hi]
        refl = two_pi_iv.sub(theta_mod, prec)
        theta_iv = Interval(min(theta_mod.lo, refl.lo), max(theta_mod.hi, refl.hi))

    c_iv = Interval.exact(2).div(Interval.exact(m), prec)
    cos_th = cos_interval(theta_iv, prec)
    sin_th = sin_interval(theta_iv, prec)
    sin_th_sq = sin_th.sqr(prec)

    # Max-heap keyed by EXACT negative Decimal ub: (-ub_dec, tie, kind, arc_idx, lo, hi)
    # kind == 0: real interval [lo, hi] in [-1, 1]
    # kind == 1: Farey arc arc_idx, t in [lo, hi] subset [0, 1]
    arcs: list[_FareyArcSpec] = []
    heap: list[tuple[Decimal, int, int, int, Decimal, Decimal]] = []
    counter = 0
    evaluated = 0
    best_lb = Decimal("-Infinity")

    # 1. Cover real segment [-1, 1] (handles N=2 and the real boundary slit of N=3)
    real_cuts = [_NEG_ONE, Decimal("-0.5"), _ZERO, _HALF, _ONE]
    for a, b in zip(real_cuts[:-1], real_cuts[1:]):
        x_iv = Interval(a, b)
        lb, ub = _real_interval_psi_bounds(x_iv, cos_th, sin_th_sq, c_iv, active_y, prec)
        evaluated += 1
        if lb > best_lb:
            best_lb = lb
        counter += 1
        heapq.heappush(heap, (-ub, counter, 0, -1, a, b))

    # 2. Cover every Farey arc in [0, 1/2] (covering alpha in [0, pi]) for N >= 3
    if n >= 3:
        seq = farey_sequence(n)
        for idx in range(len(seq) - 1):
            f_left, f_right = seq[idx], seq[idx + 1]
            if float(f_left) >= 0.5:
                break
            arc = _FareyArcSpec.from_farey_pair(n, f_left, f_right)
            arc_idx = len(arcs)
            arcs.append(arc)
            for t_lo, t_hi in ((_ZERO, _HALF), (_HALF, _ONE)):
                t_iv = Interval(t_lo, t_hi)
                r_lo, r_hi = _certified_gap_bounds_on_t(
                    arc, t_iv, prec, bisect_steps=16, need_lower_rho=True
                )
                ang_iv = arc.angle_interval_for_t(t_iv, prec)
                lb, ub = _polar_box_psi_bounds(
                    Interval(r_lo, r_hi), ang_iv, theta_iv, c_iv, active_y, prec
                )
                evaluated += 1
                if lb > best_lb:
                    best_lb = lb
                counter += 1
                heapq.heappush(heap, (-ub, counter, 1, arc_idx, t_lo, t_hi))

    tol_dec = Decimal.from_float(tol)
    status = "converged"
    while heap and evaluated < max_subdivisions:
        neg_top_ub, _, kind, arc_idx, lo, hi = heap[0]
        top_ub = -neg_top_ub
        if top_ub.is_finite() and best_lb.is_finite() and _ceil_ctx(prec).subtract(top_ub, best_lb) <= tol_dec:
            status = "converged"
            break
        heapq.heappop(heap)
        mid = _floor_ctx(prec).divide(_floor_ctx(prec).add(lo, hi), _TWO)
        if mid <= lo or mid >= hi:
            counter += 1
            heapq.heappush(heap, (-top_ub, counter, kind, arc_idx, lo, hi))
            status = "precision_limit"
            break

        if kind == 0:
            # Sample midpoint for tighter lower bound
            m_lb, _ = _real_interval_psi_bounds(
                Interval(mid, mid), cos_th, sin_th_sq, c_iv, active_y, prec
            )
            if m_lb > best_lb:
                best_lb = m_lb
            for s_lo, s_hi in ((lo, mid), (mid, hi)):
                lb, ub = _real_interval_psi_bounds(
                    Interval(s_lo, s_hi), cos_th, sin_th_sq, c_iv, active_y, prec
                )
                evaluated += 1
                if lb > best_lb:
                    best_lb = lb
                if ub >= best_lb:
                    counter += 1
                    heapq.heappush(heap, (-ub, counter, 0, -1, s_lo, s_hi))
        else:
            arc = arcs[arc_idx]
            # Sample midpoint for tighter lower bound
            t_pt = Interval(mid, mid)
            rm_lo, rm_hi = _certified_gap_bounds_on_t(
                arc, t_pt, prec, bisect_steps=16, need_lower_rho=True
            )
            ang_pt = arc.angle_interval_for_t(t_pt, prec)
            m_lb, _ = _polar_box_psi_bounds(
                Interval(rm_lo, rm_hi), ang_pt, theta_iv, c_iv, active_y, prec
            )
            if m_lb > best_lb:
                best_lb = m_lb

            for s_lo, s_hi in ((lo, mid), (mid, hi)):
                t_iv = Interval(s_lo, s_hi)
                r_lo, r_hi = _certified_gap_bounds_on_t(
                    arc, t_iv, prec, bisect_steps=16, need_lower_rho=True
                )
                ang_iv = arc.angle_interval_for_t(t_iv, prec)
                lb, ub = _polar_box_psi_bounds(
                    Interval(r_lo, r_hi), ang_iv, theta_iv, c_iv, active_y, prec
                )
                evaluated += 1
                if lb > best_lb:
                    best_lb = lb
                if ub >= best_lb:
                    counter += 1
                    heapq.heappush(heap, (-ub, counter, 1, arc_idx, s_lo, s_hi))
    else:
        if heap:
            status = "max_subdivisions"

    # Include best_lb in global_ub to cover cells pruned when ub < best_lb.
    global_ub = max(-heap[0][0], best_lb) if heap else best_lb
    if not global_ub.is_finite():
        return CertifiedBSplineMultiplier(
            order=n,
            boxcar_length=m,
            theta_radians=float(theta_radians),
            certified=False,
            psi_upper_bound=float("inf"),
            lp_psi_estimate=lp_est,
            dual_multipliers=tuple(float(v) for v in y_opt),
            sup_psi_lo=float(best_lb) if best_lb.is_finite() else float("-inf"),
            sup_psi_ub=float("inf"),
            evaluated_subintervals=evaluated,
            status="not_separated_from_theta_N",
        )

    # Combine: Psi_N <= (1 + 2/(M|z-1|)) * exp(sum y_k + (N-1)*global_ub)
    c_ctx = _ceil_ctx(prec)
    f_ctx = _floor_ctx(prec)
    d1_sq_lo = f_ctx.add(
        interval_distance_sq(Interval.exact(1), cos_th, prec),
        sin_th_sq.lo,
    )
    if d1_sq_lo <= _ZERO:
        return CertifiedBSplineMultiplier(
            order=n,
            boxcar_length=m,
            theta_radians=float(theta_radians),
            certified=False,
            psi_upper_bound=float("inf"),
            lp_psi_estimate=lp_est,
            dual_multipliers=tuple(float(v) for v in y_opt),
            sup_psi_lo=float(best_lb),
            sup_psi_ub=float(global_ub),
            evaluated_subintervals=evaluated,
            status="z_too_close_to_1",
        )
    d1_lo = _dec_sqrt_floor(d1_sq_lo, prec)
    fac_1_hi = c_ctx.add(_ONE, c_ctx.divide(c_iv.hi, d1_lo))
    sum_y_hi = _ZERO
    for _, y_k in active_y:
        sum_y_hi = c_ctx.add(sum_y_hi, y_k)
    exp_arg_hi = c_ctx.add(sum_y_hi, c_ctx.multiply(Decimal(n - 1), global_ub))

    # Avoid Decimal overflow if exp_arg_hi is huge
    if exp_arg_hi > Decimal(500):
        psi_ub_float = float("inf")
        certified_flag = False
        status = "exponent_overflow"
    else:
        exp_hi = exp_interval(Interval(exp_arg_hi, exp_arg_hi), prec).hi
        psi_hi = c_ctx.multiply(fac_1_hi, exp_hi)
        psi_ub_float = _decimal_to_float_ceil(psi_hi)
        certified_flag = True

    return CertifiedBSplineMultiplier(
        order=n,
        boxcar_length=m,
        theta_radians=float(theta_radians),
        certified=certified_flag,
        psi_upper_bound=psi_ub_float,
        lp_psi_estimate=lp_est,
        dual_multipliers=tuple(float(v) for v in y_opt),
        sup_psi_lo=float(best_lb) if best_lb.is_finite() else float("-inf"),
        sup_psi_ub=float(global_ub),
        evaluated_subintervals=evaluated,
        status=status,
    )


def fit_sinusoid_on_ray(
    values: Sequence[float],
    theta: float,
) -> tuple[float, float, float, float]:
    """Fit s(k) = c0 + A * cos(k * theta + phi) by linear least squares.

    Returns ``(c0, amplitude, phase, max_residual)``.
    """
    y = np.asarray(values, dtype=float)
    ks = np.arange(y.size, dtype=float)
    design = np.column_stack([np.ones_like(ks), np.cos(ks * theta), np.sin(ks * theta)])
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    c0 = float(coef[0])
    a_cos = float(coef[1])
    b_sin = float(coef[2])
    amplitude = float(sqrt(a_cos * a_cos + b_sin * b_sin))
    # a cos(k th) + b sin(k th) = A cos(k th + phi) with phi = atan2(-b, a)
    phase = float(np.arctan2(-b_sin, a_cos))
    fitted = c0 + amplitude * np.cos(ks * theta + phase)
    max_resid = float(np.max(np.abs(y - fitted)))
    return c0, amplitude, phase, max_resid


@dataclass(frozen=True)
class NoiselessRankUnrestrictedBound:
    """Certified rank-unrestricted lower bound on inf_{g in O_N^cl} max_{k <= L} |f(w_k) - g(w_k)|."""

    order: int
    boxcar_length: int
    horizon_L: int
    theta_radians: float
    amplitude: float
    conjugate_leakage: float
    multiplier: CertifiedBSplineMultiplier
    mode_a_error_lower_bound: float
    mode_b_error_lower_bound: float
    best_error_lower_bound: float

    def to_dict(self) -> dict[str, object]:
        return {
            "order": self.order,
            "boxcar_length": self.boxcar_length,
            "horizon_L": self.horizon_L,
            "theta_radians": self.theta_radians,
            "amplitude": self.amplitude,
            "conjugate_leakage": self.conjugate_leakage,
            "psi_upper_bound": (
                self.multiplier.psi_upper_bound
                if np.isfinite(self.multiplier.psi_upper_bound)
                else None
            ),
            "mode_a_error_lower_bound": self.mode_a_error_lower_bound,
            "mode_b_error_lower_bound": self.mode_b_error_lower_bound,
            "best_error_lower_bound": self.best_error_lower_bound,
            "epistemic_status": (
                "PROVED & CERTIFIED rank-unrestricted lower bound on sup_{k<=L} |f(w_k) - g(w_k)| "
                "over ALL N-state classical stochastic realizations g of arbitrary rank <= N."
            ),
        }


def certify_noiseless_counterfeit_error_lower_bound(
    ray_values: Sequence[float],
    order: int,
    theta_radians: float,
    *,
    boxcar_length: int | None = None,
    num_moments: int = 10,
    tol: float = 2e-3,
    max_subdivisions: int = 1500,
) -> NoiselessRankUnrestrictedBound:
    """Certify a rank-unrestricted lower bound on min_{g in O_N^cl} max_{k<=L} |f(w_k) - g(w_k)|.

    Requires ``len(ray_values) >= order * boxcar_length + 1`` for Mode B
    (and ``order * (boxcar_length - 1) + 1`` for Mode A).
    """
    n = int(order)
    vals = np.asarray(ray_values, dtype=float)
    horizon_l = int(vals.size - 1)
    if boxcar_length is None:
        m = horizon_l // n
    else:
        m = int(boxcar_length)
    if m < 1 or n * m > horizon_l:
        raise ValueError(
            f"ray_values length {vals.size} is too short for order={n}, boxcar_length={m} "
            f"(requires at least {n * m + 1})"
        )

    mult = certify_bspline_multiplier(
        n, m, theta_radians, num_moments=num_moments, tol=tol, max_subdivisions=max_subdivisions
    )
    w_bs = bspline_window(n, m)
    k_len = w_bs.size  # N*(M-1) + 1
    ks_a = np.arange(k_len, dtype=float)
    fourier_a = complex(np.sum(w_bs * np.exp(-1j * ks_a * theta_radians) * (vals[:k_len] - 0.5)))

    c0, amp, phase, _ = fit_sinusoid_on_ray(vals[: n * m + 1], theta_radians)
    ks_full = np.arange(n * m + 1, dtype=float)
    ref = c0 + amp * np.cos(ks_full * theta_radians + phase)
    resid = vals[: n * m + 1] - ref
    r_lin = abs(complex(np.sum(w_bs * np.exp(-1j * ks_a * theta_radians) * resid[:k_len])))
    r_max = float(np.max(np.abs(resid)))
    leak = bspline_conjugate_leakage(n, m, theta_radians)

    if not mult.certified or not np.isfinite(mult.psi_upper_bound):
        return NoiselessRankUnrestrictedBound(
            order=n,
            boxcar_length=m,
            horizon_L=n * m,
            theta_radians=float(theta_radians),
            amplitude=amp,
            conjugate_leakage=leak,
            multiplier=mult,
            mode_a_error_lower_bound=0.0,
            mode_b_error_lower_bound=0.0,
            best_error_lower_bound=0.0,
        )

    psi = mult.psi_upper_bound
    lb_a = max(0.0, abs(fourier_a) - 0.5 * (psi - 1.0))
    sig_b = 0.5 * amp * max(0.0, 1.0 - leak) - r_lin - (psi - 1.0) * r_max
    lb_b = max(0.0, sig_b / psi)
    return NoiselessRankUnrestrictedBound(
        order=n,
        boxcar_length=m,
        horizon_L=n * m,
        theta_radians=float(theta_radians),
        amplitude=amp,
        conjugate_leakage=leak,
        multiplier=mult,
        mode_a_error_lower_bound=lb_a,
        mode_b_error_lower_bound=lb_b,
        best_error_lower_bound=max(lb_a, lb_b),
    )


def ray_words(
    symbol: str,
    max_power: int,
    *,
    prefix: str = "",
    suffix: str = "",
) -> tuple[str, ...]:
    """Return the unary ray words ``(prefix + symbol*k + suffix)`` for ``k = 0..max_power``."""
    if len(symbol) != 1:
        raise ValueError("symbol must be a single character")
    if max_power < 0:
        raise ValueError("max_power must be non-negative")
    return tuple(f"{prefix}{symbol * k}{suffix}" for k in range(max_power + 1))


@dataclass(frozen=True)
class RankUnrestrictedOrderCheck:
    """Result of testing one candidate classical state count N without rank assumptions."""

    order: int
    boxcar_length: int
    used_horizon_L: int
    psi_upper_bound: float
    empirical_signal: float
    statistical_margin: float
    certified_error_lower_bound: float
    excluded_exact: bool
    excluded_at_epsilon: bool
    multiplier: CertifiedBSplineMultiplier

    def to_dict(self) -> dict[str, object]:
        return {
            "order": self.order,
            "boxcar_length": self.boxcar_length,
            "used_horizon_L": self.used_horizon_L,
            "psi_upper_bound": (
                self.psi_upper_bound if np.isfinite(self.psi_upper_bound) else None
            ),
            "empirical_signal": self.empirical_signal,
            "statistical_margin": self.statistical_margin,
            "certified_error_lower_bound": self.certified_error_lower_bound,
            "excluded_exact": self.excluded_exact,
            "excluded_at_epsilon": self.excluded_at_epsilon,
        }


@dataclass(frozen=True)
class RankUnrestrictedReport:
    """Non-asymptotic finite-shot rank-unrestricted lower bound on C_classical(f; eps, W)."""

    method: str
    symbol: str
    prefix: str
    suffix: str
    theta_radians: float
    max_ray_power: int
    target_epsilon: float
    alpha: float
    confidence_level: float
    total_shots: int
    tested_orders: tuple[RankUnrestrictedOrderCheck, ...]
    certified_classical_state_lower_bound: int

    def to_dict(self) -> dict[str, object]:
        return {
            "method": self.method,
            "symbol": self.symbol,
            "prefix": self.prefix,
            "suffix": self.suffix,
            "theta_radians": self.theta_radians,
            "max_ray_power": self.max_ray_power,
            "target_epsilon": self.target_epsilon,
            "alpha": self.alpha,
            "confidence_level": self.confidence_level,
            "total_shots": self.total_shots,
            "certified_classical_state_lower_bound": self.certified_classical_state_lower_bound,
            "tested_orders": [item.to_dict() for item in self.tested_orders],
            "epistemic_scope": (
                "PROVED & CERTIFIED non-asymptotic, rank-unrestricted lower bound: "
                "with probability >= 1 - alpha over binomial shot noise, NO classical "
                "stochastic realization of size N < certified_classical_state_lower_bound "
                "(of ANY Hankel rank <= N and ANY Jordan structure) approximates f within "
                "target_epsilon uniformly on the observed unary ray. ZERO rank upper-bound "
                "assumption is required."
            ),
        }


def _choose_boxcar_for_order(
    order: int,
    max_power: int,
    *,
    mode: str,
) -> int:
    """Return the largest valid boxcar length M for ``order`` within ``max_power``."""
    if mode == "fourier_cap":
        # Need N * (M - 1) <= max_power  =>  M <= max_power // N + 1
        return (max_power // order) + 1
    # Mode B needs N * M <= max_power  =>  M <= max_power // N
    return max_power // order


def certify_rank_unrestricted_fourier_cap(
    dataset: ShotDataset,
    *,
    symbol: str,
    max_ray_power: int,
    theta_radians: float,
    prefix: str = "",
    suffix: str = "",
    orders: Sequence[int] | None = None,
    maximum_order: int = 12,
    target_epsilon: float = 0.0,
    alpha: float = 0.01,
    num_moments: int = 10,
    cert_tol: float = 2e-3,
    early_stop: bool = True,
) -> RankUnrestrictedReport:
    """Mode A: Unconditional single-sample B-spline Fourier-cap rank-unrestricted certifier.

    Requires NO sample splitting, NO reference sinusoid, NO word-wise union bound,
    and NO rank upper bound.  Simultaneously valid over all tested orders via an
    explicit union bound ``delta_N = alpha / len(order_list)``.
    """
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    if target_epsilon < 0.0:
        raise ValueError("target_epsilon must be non-negative")
    words = ray_words(symbol, max_ray_power, prefix=prefix, suffix=suffix)
    dataset.require_words(words)

    rates = np.array([dataset.empirical_rate(w) for w in words], dtype=float)
    trials = np.array([dataset.trials[w] for w in words], dtype=float)
    total_shots = int(np.sum(trials))

    order_list = (
        tuple(int(n) for n in orders)
        if orders is not None
        else tuple(range(2, int(maximum_order) + 1))
    )
    if not order_list or any(n < 2 for n in order_list):
        raise ValueError("orders must contain integers >= 2")

    delta_each = alpha / float(len(order_list))
    checks: list[RankUnrestrictedOrderCheck] = []
    lb_states = 1

    # Order N=1 (constant process): excluded whenever signal differs from constant,
    # automatically superseded once N=2 is excluded.
    all_prefix_excluded = True
    for n in order_list:
        m = _choose_boxcar_for_order(n, max_ray_power, mode="fourier_cap")
        if m < 2:
            break
        w_bs = bspline_window(n, m)
        k_len = w_bs.size
        ks = np.arange(k_len, dtype=float)
        f_hat = abs(complex(np.sum(w_bs * np.exp(-1j * ks * theta_radians) * (rates[:k_len] - 0.5))))

        # Exact complex scalar Hoeffding: Pr(|F_hat - F| > eps_lin) <= delta_each
        var_sum = float(np.sum((w_bs * w_bs) / trials[:k_len]))
        eps_lin = float(_ROUNDING_GUARD * sqrt(0.5 * var_sum * log(4.0 / delta_each)))

        mult = certify_bspline_multiplier(
            n, m, theta_radians, num_moments=num_moments, tol=cert_tol
        )
        if mult.certified and np.isfinite(mult.psi_upper_bound):
            cap = 0.5 * (mult.psi_upper_bound - 1.0)
            err_lb = max(0.0, f_hat - eps_lin - cap)
        else:
            err_lb = 0.0

        excl_exact = err_lb > 0.0
        excl_eps = err_lb > target_epsilon
        checks.append(
            RankUnrestrictedOrderCheck(
                order=n,
                boxcar_length=m,
                used_horizon_L=k_len - 1,
                psi_upper_bound=mult.psi_upper_bound,
                empirical_signal=f_hat,
                statistical_margin=eps_lin,
                certified_error_lower_bound=err_lb,
                excluded_exact=excl_exact,
                excluded_at_epsilon=excl_eps,
                multiplier=mult,
            )
        )
        if all_prefix_excluded and excl_eps:
            lb_states = max(lb_states, n + 1)
        else:
            all_prefix_excluded = False
            if early_stop:
                break

    return RankUnrestrictedReport(
        method="bspline_cayley_hamilton_fourier_cap_mode_a",
        symbol=symbol,
        prefix=prefix,
        suffix=suffix,
        theta_radians=float(theta_radians),
        max_ray_power=max_ray_power,
        target_epsilon=float(target_epsilon),
        alpha=float(alpha),
        confidence_level=1.0 - float(alpha),
        total_shots=total_shots,
        tested_orders=tuple(checks),
        certified_classical_state_lower_bound=lb_states,
    )


def certify_rank_unrestricted_split_sample(
    dataset: ShotDataset | tuple[ShotDataset, ShotDataset],
    *,
    symbol: str,
    max_ray_power: int,
    theta_radians: float,
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
    """Mode B: Two-stage Hypergeometric split-sample rank-unrestricted certifier.

    Uses pilot split to fit a deterministic reference sinusoid s(k), then certifies
    on the independent main split via simultaneous Chernoff--KL word intervals
    (level alpha/2, shared across all orders) plus scalar Hoeffding on the
    B-spline residual average (level alpha/(2*|orders|) per tested order).
    """
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    if target_epsilon < 0.0:
        raise ValueError("target_epsilon must be non-negative")

    words = ray_words(symbol, max_ray_power, prefix=prefix, suffix=suffix)
    if isinstance(dataset, tuple):
        pilot_ds, main_ds = dataset
        pilot_ds.require_words(words)
        main_ds.require_words(words)
    else:
        dataset.require_words(words)
        if rng is None:
            rng = np.random.default_rng()
        # Subset to the ray words before splitting so splitting is fast and exact
        sub_ds = ShotDataset(
            dataset.alphabet,
            {w: dataset.successes[w] for w in words},
            {w: dataset.trials[w] for w in words},
        )
        pilot_ds, main_ds = split_shot_dataset(sub_ds, pilot_fraction, rng)

    total_shots = int(sum(pilot_ds.trials[w] + main_ds.trials[w] for w in words))

    order_list = (
        tuple(int(n) for n in orders)
        if orders is not None
        else tuple(range(2, int(maximum_order) + 1))
    )
    if not order_list or any(n < 2 for n in order_list):
        raise ValueError("orders must contain integers >= 2")

    # Stage 1 (Pilot): fit deterministic reference sinusoid s(k)
    pilot_rates = np.array([pilot_ds.empirical_rate(w) for w in words], dtype=float)
    c0, amp, phase, _ = fit_sinusoid_on_ray(pilot_rates, theta_radians)
    ks_all = np.arange(len(words), dtype=float)
    ref_all = c0 + amp * np.cos(ks_all * theta_radians + phase)

    # Stage 2 (Main, strictly independent conditional on Stage 1):
    main_rates = np.array([main_ds.empirical_rate(w) for w in words], dtype=float)
    main_trials = np.array([main_ds.trials[w] for w in words], dtype=float)
    resid_all = main_rates - ref_all

    # Simultaneous Chernoff-KL confidence half-widths on all L+1 ray words (shared across all N, level alpha/2)
    delta_kl_each = (0.5 * alpha) / float(len(words))
    kl_halfwidths = np.empty(len(words), dtype=float)
    for idx, w in enumerate(words):
        lo, hi = kl_binomial_confidence_interval(
            main_ds.successes[w], main_ds.trials[w], delta_kl_each
        )
        q = main_rates[idx]
        kl_halfwidths[idx] = _ROUNDING_GUARD * max(q - lo, hi - q)

    delta_lin_each = (0.5 * alpha) / float(len(order_list))
    checks: list[RankUnrestrictedOrderCheck] = []
    lb_states = 1
    all_prefix_excluded = True

    for n in order_list:
        m = _choose_boxcar_for_order(n, max_ray_power, mode="split_sample")
        if m < 2:
            break
        used_l = n * m
        w_bs = bspline_window(n, m)
        k_len = w_bs.size
        ks_a = np.arange(k_len, dtype=float)

        # Observed linear residual and scalar Hoeffding bound on main split
        r_lin = abs(complex(np.sum(w_bs * np.exp(-1j * ks_a * theta_radians) * resid_all[:k_len])))
        var_sum = float(np.sum((w_bs * w_bs) / main_trials[:k_len]))
        eps_lin = float(_ROUNDING_GUARD * sqrt(0.5 * var_sum * log(4.0 / delta_lin_each)))

        # Pointwise observed + KL bound on {0, ..., N*M}
        max_dev = float(np.max(np.abs(resid_all[: used_l + 1]) + kl_halfwidths[: used_l + 1]))
        leak = bspline_conjugate_leakage(n, m, theta_radians)
        sig = 0.5 * amp * max(0.0, 1.0 - leak)

        mult = certify_bspline_multiplier(
            n, m, theta_radians, num_moments=num_moments, tol=cert_tol
        )
        if mult.certified and np.isfinite(mult.psi_upper_bound):
            psi = mult.psi_upper_bound
            stat_margin = r_lin + eps_lin + (psi - 1.0) * max_dev
            err_lb = max(0.0, (sig - stat_margin) / psi)
            # Also check Mode A on the same main split (no extra alpha cost because we already paid eps_lin!)
            f_hat_main = abs(
                complex(
                    np.sum(
                        w_bs * np.exp(-1j * ks_a * theta_radians) * (main_rates[:k_len] - 0.5)
                    )
                )
            )
            err_lb_a = max(0.0, f_hat_main - eps_lin - 0.5 * (psi - 1.0))
            err_lb = max(err_lb, err_lb_a)
        else:
            stat_margin = float("inf")
            err_lb = 0.0

        excl_exact = err_lb > 0.0
        excl_eps = err_lb > target_epsilon
        checks.append(
            RankUnrestrictedOrderCheck(
                order=n,
                boxcar_length=m,
                used_horizon_L=used_l,
                psi_upper_bound=mult.psi_upper_bound,
                empirical_signal=sig,
                statistical_margin=stat_margin,
                certified_error_lower_bound=err_lb,
                excluded_exact=excl_exact,
                excluded_at_epsilon=excl_eps,
                multiplier=mult,
            )
        )
        if all_prefix_excluded and excl_eps:
            lb_states = max(lb_states, n + 1)
        else:
            all_prefix_excluded = False
            if early_stop:
                break

    return RankUnrestrictedReport(
        method="bspline_cayley_hamilton_split_sample_mode_b",
        symbol=symbol,
        prefix=prefix,
        suffix=suffix,
        theta_radians=float(theta_radians),
        max_ray_power=max_ray_power,
        target_epsilon=float(target_epsilon),
        alpha=float(alpha),
        confidence_level=1.0 - float(alpha),
        total_shots=total_shots,
        tested_orders=tuple(checks),
        certified_classical_state_lower_bound=lb_states,
    )
