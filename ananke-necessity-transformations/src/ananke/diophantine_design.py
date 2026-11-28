"""Diophantine gate design and Karpelevič Markov spectrum analysis (ANANKE v2).

Establishes both the exact asymptotic optimality of noble phases and its
finite-horizon / Hankel-conditioning refinements:

- Theorem 4 (Karpelevič Markov Theorem, PROVED):
  For any irrational phase alpha in (0, 1), define
      kappa_Theta(alpha) := liminf_{N -> inf} N^3 * dist(e^{2*pi*i*alpha}, Theta_N).
  Every noble irrational alpha_* = [0; a_1, ..., a_m, overline{1}] attains
      kappa_Theta(alpha_*) = 2 * pi^2 * phi^3 / (5 * sqrt(5)) ~= 7.478899,
  whereas every non-noble irrational satisfies
      kappa_Theta(alpha) <= 3 * pi^2 / 4 ~= 7.402203 < kappa_Theta(alpha_*)
  (algebraically 245 < 256).

- Refinement A (Finite-Horizon Arc-Asymmetry Counterexample, PROVED):
  On any individual Farey arc (p/q, r/s) with d = floor(N/q) and s > q*d,
  the radial gap cubic t*(1-t)*(t/s + (1-t)/(q*d)) peaks at t_opt < 1/2,
  whereas noble phases sit at t_* > 0.64 (asymptotically phi/sqrt(5) ~= 0.7236).
  Consequently, non-noble phases such as silver [0; 8, overline{2}] beat
  noble [0; 8, overline{1}] at fixed N = 15, and [0; 8, overline{1,2}] beats
  it at fixed N = 25.

- Refinement B (Cross-Sector Hankel Conditioning, QUANTIFIED/CERTIFIED):
  Moving from the small-angle sector k = 8 (theta_x ~= 0.73 rad) to larger-angle
  noble phases such as the golden angle [0; 2, overline{1}] = 1/phi^2
  (theta_x ~= 2.400 rad) or [0; 3, overline{1}] (theta_x ~= 1.737 rad) roughly
  doubles the minimal Hankel singular value sigma_4(H) and reduces finite-shot
  certified eigenvalue radii by 2x--3x at the same shot budget.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log, pi, sqrt
from typing import Sequence

import numpy as np

from .examples import qubit_rotation_process
from .hankel import build_hankel
from .karpelevich import farey_sequence, karpelevich_boundary_radius
from .karpelevich_certified import certified_distance_to_karpelevich

PHI = (1.0 + sqrt(5.0)) / 2.0
KARPELEVICH_NOBLE_MARKOV_CONSTANT = 2.0 * (pi**2) * (PHI**3) / (5.0 * sqrt(5.0))
NON_NOBLE_ANALYTIC_UPPER_BOUND = 3.0 * (pi**2) / 4.0


def noble_phase_turns(sector_k: int) -> float:
    """Return the noble phase [0; k, overline{1}] = 1 / (k + 1/phi) in turns."""
    k = int(sector_k)
    if k < 1:
        raise ValueError("sector_k must be a positive integer")
    return 1.0 / (k + 1.0 / PHI)


def periodic_cf_turns(
    prefix: Sequence[int],
    period: Sequence[int],
    *,
    repeats: int = 60,
) -> float:
    """Evaluate [0; *prefix, overline{*period}] accurately as a float in (0, 1)."""
    if not period or any(int(a) < 1 for a in period):
        raise ValueError("period must contain positive integers")
    if any(int(a) < 1 for a in prefix):
        raise ValueError("prefix must contain positive integers")
    tail = 1.0
    for _ in range(repeats):
        for a in reversed(period):
            tail = int(a) + 1.0 / tail
    val = tail
    for a in reversed(prefix):
        val = int(a) + 1.0 / val
    return 1.0 / val


def asymptotic_karpelevich_radial_gap(order: int, phase_turns: float) -> float:
    """Leading asymptotic formula for 1 - rho_N(2*pi*alpha) (accurate to O(N^{-2})).

    Theorem 1 corollary (PROVED):
        1 - rho_N(theta(t)) = 2*pi^2 * t*(1-t)/(q*s) * (t/s + (1-t)/(q*d)) * (1 + O(N^{-2})).
    """
    n = int(order)
    if n < 3:
        raise ValueError("order must be at least 3")
    turns = float(phase_turns % 1.0)
    seq = farey_sequence(n)
    for idx in range(len(seq) - 1):
        f_left, f_right = seq[idx], seq[idx + 1]
        if float(f_left) <= turns <= float(f_right):
            if turns == float(f_left) or turns == float(f_right):
                return 0.0
            p, q = f_left.numerator, f_left.denominator
            r, s = f_right.numerator, f_right.denominator
            t_turns = turns
            if q > s:
                p, q, r, s = s - r, s, q - p, q
                t_turns = 1.0 - turns
            t = (t_turns - p / q) * q * s
            d = n // q
            return float(
                2.0 * (pi**2) * t * (1.0 - t) / (q * s) * (t / s + (1.0 - t) / (q * d))
            )
    return 0.0


def periodic_karpelevich_markov_constant(period: Sequence[int]) -> float:
    """Compute the exact asymptotic liminf_{N -> inf} N^3 * dist(e^{2*pi*i*alpha}, Theta_N)
    for any irrational with eventually periodic continued-fraction tail ``period``.
    """
    p_seq = tuple(int(a) for a in period)
    if not p_seq or any(a < 1 for a in p_seq):
        raise ValueError("period must contain positive integers")
    length = len(p_seq)
    # Forward periodic tails alpha_{k+1} = [a_{k+1}; a_{k+2}, ...]
    tails: list[float] = []
    for shift in range(length):
        val = 1.0
        rotated = p_seq[shift:] + p_seq[:shift]
        for _ in range(180):
            for a in reversed(rotated):
                val = a + 1.0 / val
        tails.append(val)

    min_c = float("inf")
    for step in range(length):
        ak1 = p_seq[step]
        alpha_k1 = tails[step]
        # Backward periodic ratio beta_k = q_k / q_{k-1} = [a_k; a_{k-1}, ...]
        beta_k = 1.0
        for _ in range(180):
            for idx in range(length):
                beta_k = p_seq[(step - 1 - idx) % length] + 1.0 / beta_k
        d0 = p_seq[(step - 1) % length]
        for m in range(ak1):
            if m == 0:
                t = (alpha_k1 * beta_k) / (alpha_k1 * beta_k + 1.0)
                c_val = (
                    2.0
                    * (pi**2)
                    * beta_k
                    * t
                    * (1.0 - t)
                    * (t + (beta_k / d0) * (1.0 - t))
                )
            else:
                sq = m + 1.0 / beta_k
                t = sq / (alpha_k1 + 1.0 / beta_k)
                c_val = (
                    2.0
                    * (pi**2)
                    * sq
                    * t
                    * (1.0 - t)
                    * (t + (sq / m) * (1.0 - t))
                )
            if c_val < min_c:
                min_c = c_val
    return float(min_c)


@dataclass(frozen=True)
class PhaseDesignMetrics:
    """Combined geometric (Karpelevič) and statistical (Hankel sensitivity) design metrics."""

    label: str
    theta_x: float
    theta_z: float
    phase_turns: float
    target_order: int
    sigma_1: float
    sigma_4: float
    condition_number_4: float
    exact_scalar_sensitivity_l2: float
    predicted_scalar_hoeffding_radius: float
    karpelevich_radial_gap: float
    karpelevich_distance_lo: float
    karpelevich_distance_hi: float
    witness_margin_ratio: float

    def to_dict(self) -> dict[str, object]:
        return {
            "label": self.label,
            "theta_x": self.theta_x,
            "theta_z": self.theta_z,
            "phase_turns": self.phase_turns,
            "target_order": self.target_order,
            "sigma_1": self.sigma_1,
            "sigma_4": self.sigma_4,
            "condition_number_4": self.condition_number_4,
            "exact_scalar_sensitivity_l2": self.exact_scalar_sensitivity_l2,
            "predicted_scalar_hoeffding_radius": self.predicted_scalar_hoeffding_radius,
            "karpelevich_radial_gap": self.karpelevich_radial_gap,
            "karpelevich_distance_lo": self.karpelevich_distance_lo,
            "karpelevich_distance_hi": self.karpelevich_distance_hi,
            "witness_margin_ratio": self.witness_margin_ratio,
        }


def qubit_phase_design_metrics(
    theta_x: float,
    *,
    label: str = "",
    theta_z: float = 1.11,
    target_order: int = 15,
    max_prefix_length: int = 3,
    max_suffix_length: int = 3,
    shots_per_word: int = 300_000,
    alpha: float = 0.01,
    initial_bloch: np.ndarray | None = None,
    measurement_axis: np.ndarray | None = None,
) -> PhaseDesignMetrics:
    """Evaluate exact Hankel conditioning, scalar Hoeffding sensitivity, and certified Karpelevič distance."""
    process = qubit_rotation_process(
        theta_x=theta_x,
        theta_z=theta_z,
        initial_bloch=initial_bloch,
        measurement_axis=measurement_axis,
    )
    hankel = build_hankel(process.behavior, process.alphabet, max_prefix_length, max_suffix_length)
    u_mat, sv, vt_mat = np.linalg.svd(hankel.matrix, full_matrices=False)
    r = 4
    ur, vr = u_mat[:, :r], vt_mat[:r, :].T
    x_mat = ur.T @ hankel.matrix @ vr
    y_mat = ur.T @ hankel.shifts["x"] @ vr
    x_inv = np.linalg.inv(x_mat)
    t_mat = y_mat @ x_inv

    exact_mode = complex(np.exp(1j * theta_x))
    eigvals, eigvecs = np.linalg.eig(t_mat)
    k = int(np.argmin(np.abs(eigvals - exact_mode)))
    lam = complex(eigvals[k])
    q1 = eigvecs[:, k] / np.linalg.norm(eigvecs[:, k])
    _, _, vh = np.linalg.svd((t_mat - lam * np.eye(r, dtype=complex)).conj().T)
    p1 = vh[-1, :].conj()
    p1 = p1 / complex(np.vdot(p1, q1)).conjugate()

    # Exact deterministic linear functional sensitivity ||c||_2 for S = p1^H (Delta_Y - lam Delta_X) X^{-1} q1
    right_vec = x_inv @ q1
    inc_h: dict[str, list[tuple[int, int]]] = {}
    inc_hx: dict[str, list[tuple[int, int]]] = {}
    for i, p in enumerate(hankel.prefixes):
        for j, s in enumerate(hankel.suffixes):
            inc_h.setdefault(p + s, []).append((i, j))
            inc_hx.setdefault(p + "x" + s, []).append((i, j))
    c_sq = 0.0
    for w in set(inc_h) | set(inc_hx):
        cw = 0.0 + 0.0j
        if w in inc_hx:
            for i, j in inc_hx[w]:
                cw += complex(np.dot(p1.conj(), ur[i, :]) * np.dot(vr[j, :], right_vec))
        if w in inc_h:
            for i, j in inc_h[w]:
                cw -= lam * complex(np.dot(p1.conj(), ur[i, :]) * np.dot(vr[j, :], right_vec))
        c_sq += abs(cw) ** 2
    sens_l2 = sqrt(c_sq)
    # Predicted leading scalar Hoeffding radius (with delta_s = 0.5*alpha on 85% main split)
    m_main = 0.85 * shots_per_word
    pred_rad = sqrt(0.5 * (c_sq / m_main) * log(4.0 / (0.5 * alpha)))

    rad_gap = 1.0 - karpelevich_boundary_radius(target_order, theta_x)
    dist = certified_distance_to_karpelevich(
        exact_mode, target_order, tol=1e-4, max_subdivisions=400
    )
    margin_ratio = dist.distance_lo / pred_rad if pred_rad > 0.0 else float("inf")
    return PhaseDesignMetrics(
        label=label or f"theta={theta_x:.6f}",
        theta_x=float(theta_x),
        theta_z=float(theta_z),
        phase_turns=float((theta_x / (2.0 * pi)) % 1.0),
        target_order=int(target_order),
        sigma_1=float(sv[0]),
        sigma_4=float(sv[3]),
        condition_number_4=float(sv[0] / sv[3]),
        exact_scalar_sensitivity_l2=float(sens_l2),
        predicted_scalar_hoeffding_radius=float(pred_rad),
        karpelevich_radial_gap=float(rad_gap),
        karpelevich_distance_lo=dist.distance_lo,
        karpelevich_distance_hi=dist.distance_hi,
        witness_margin_ratio=float(margin_ratio),
    )


def optimize_phase_in_sector(
    sector_k: int,
    target_order: int,
    *,
    grid_points: int = 300,
) -> tuple[float, float]:
    """Find the phase angle (radians) in sector [0; k, ...] maximizing 1 - rho_{target_order}(theta)."""
    k = int(sector_k)
    if k < 2:
        raise ValueError("sector_k must be at least 2")
    lo = 2.0 * pi / (k + 1) + 1e-6
    hi = 2.0 * pi / k - 1e-6
    angles = np.linspace(lo, hi, grid_points)
    gaps = [1.0 - karpelevich_boundary_radius(target_order, float(a)) for a in angles]
    best_i = int(np.argmax(gaps))
    return (float(angles[best_i]), float(gaps[best_i]))
