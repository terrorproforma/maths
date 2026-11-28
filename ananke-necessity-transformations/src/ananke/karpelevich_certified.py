"""Interval-certified Karpelevič distance and finite-state exclusion.

Replaces v1's floating-point golden-section minimization with a mathematically
rigorous outward-rounded interval-arithmetic branch-and-bound certifier over
every Farey arc of the Kirkland--Laffey--Šmigoc (2020) boundary of Theta_N.

Core mathematical reductions (PROVED in docs/ananke_v2_certified_core.md):
1. Reduced Positive-Trinomial Form (Theorem 1):
   On every Farey arc (p/q, r/s) of F_N (N >= 3, oriented by conjugation so
   1 <= q < s <= N, q*r - p*s = 1) parameterized by theta(t) = 2*pi*(p/q + t/(q*s))
   with t in (0, 1), all modular indices cancel identically modulo 2*pi, reducing
   the KLS radial boundary equation to the strictly monotonic zero-cancellation
   gap equation for y = 1 - rho_hat in (0, 1):

       sin(beta_1) * P_{s_1}(y) + sin(beta_2) * P_{q*d_1}(y)
           = 4 * sin(beta_1/2) * sin(beta_2/2) * sin((beta_1 + beta_2)/2),

   where beta_1 = 2*pi*t/s, beta_2 = 2*pi*(1-t)/(q*d), d = floor(N/q),
   delta = gcd(d, s), s_1 = s/delta, d_1 = d/delta, P_m(y) = 1 - (1-y)^m,
   and rho_N(theta(t)) = (1 - y)^{d_1}.

2. Exact Star-Shaped Sector Distance Identity:
   Because Theta_N = {r * e^{i*theta} : 0 <= r <= rho_N(theta)} is star-shaped
   about 0 for N >= 2, for any sector T = [theta_lo, theta_hi] with certified
   upper bound rho_max >= sup_{theta in T} rho_N(theta) and z = x + i*y:

       |z - r * e^{i*theta}|^2 = (r - p(theta))^2 + q(theta)^2
           >= dist([0, rho_max], P(T))^2 + dist(0, Q(T))^2,

   where p(theta) = x*cos(theta) + y*sin(theta), q(theta) = x*sin(theta) - y*cos(theta).
   This rigorously prunes distant Farey arcs with rho_max = 1 and drives
   global branch-and-bound over all of [0, 2*pi) with a certified global
   lower bound d_lo <= dist(z, Theta_N) <= d_hi.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
import heapq
from math import gcd
from typing import Iterable

from .interval import (
    DEFAULT_PREC,
    Interval,
    atan2_point_interval,
    cos_interval,
    interval_distance_sq,
    pi_interval,
    sin_interval,
    two_pi_interval,
    _ceil_ctx,
    _dec_sqrt_floor,
    _floor_ctx,
)
from .karpelevich import farey_sequence

_ZERO = Decimal(0)
_ONE = Decimal(1)
_TWO = Decimal(2)
_FOUR = Decimal(4)


def _zero_cancel_poly_gap(y: Interval, m: int, prec: int) -> Interval:
    """Outwardly enclose P_m(y) = 1 - (1 - y)^m for y in [0, 1] without cancellation.

    Uses the exact positive recurrence:
        P_0(y) = 0, P_1(y) = y,
        P_{2k}(y) = P_k(y) * (2 - P_k(y)),
        P_{2k+1}(y) = y + (1 - y) * P_{2k}(y).
    Every intermediate operand is nonnegative for y in [0, 1].
    """
    if m <= 0:
        return Interval.exact(0)
    if m == 1:
        return y
    one_iv = Interval.exact(1)
    two_iv = Interval.exact(2)
    one_minus_y = one_iv.sub(y, prec).clamp(_ZERO, _ONE)
    # Recursive binary decomposition (bit-by-bit from MSB)
    bits = bin(m)[2:]
    p = Interval.exact(0)
    for bit in bits:
        # Double: P_{2k} = P_k * (2 - P_k)
        p = p.mul(two_iv.sub(p, prec), prec).clamp(_ZERO, _ONE)
        if bit == "1":
            # Increment: P_{2k+1} = y + (1 - y) * P_{2k}
            p = y.add(one_minus_y.mul(p, prec), prec).clamp(_ZERO, _ONE)
    return p


@dataclass(frozen=True)
class _FareyArcSpec:
    """Normalized Farey arc (p/q, r/s) with conjugated orientation q < s."""

    orig_left: Fraction
    orig_right: Fraction
    reflected: bool
    p: int
    q: int
    r: int
    s: int
    d: int
    delta: int
    s1: int
    d1: int
    qd: int
    qd1: int

    @classmethod
    def from_farey_pair(cls, order: int, left: Fraction, right: Fraction) -> "_FareyArcSpec":
        p, q = left.numerator, left.denominator
        r, s = right.numerator, right.denominator
        reflected = False
        if q > s:
            reflected = True
            p, q, r, s = s - r, s, q - p, q
        if q >= s:
            raise ArithmeticError(f"Invalid Farey orientation for order {order}: {left}, {right}")
        d = order // q
        g = gcd(d, s)
        return cls(
            orig_left=left,
            orig_right=right,
            reflected=reflected,
            p=p,
            q=q,
            r=r,
            s=s,
            d=d,
            delta=g,
            s1=s // g,
            d1=d // g,
            qd=q * d,
            qd1=q * (d // g),
        )

    def angle_interval_for_t(self, t_iv: Interval, prec: int) -> Interval:
        """Certified enclosure of the original polar angle theta in [0, 2*pi] for t in t_iv.

        In oriented coordinates, turns = p/q + t/(q*s).
        If reflected, original turns = 1 - oriented_turns = orig_right - t/(q*s).
        """
        two_pi = two_pi_interval(prec)
        qs_iv = Interval.exact(self.q * self.s)
        if not self.reflected:
            base = Interval.from_fraction(self.orig_left, prec)
            turns = base.add(t_iv.div(qs_iv, prec), prec)
        else:
            base = Interval.from_fraction(self.orig_right, prec)
            turns = base.sub(t_iv.div(qs_iv, prec), prec)
        return turns.mul(two_pi, prec)


def _float_poly_gap(y: float, m: int) -> float:
    """Fast cancellation-free float evaluation of P_m(y) = 1 - (1 - y)^m for y in [0, 1]."""
    if m <= 0:
        return 0.0
    if m == 1:
        return y
    one_minus_y = 1.0 - y
    p = 0.0
    for bit in bin(m)[2:]:
        p = p * (2.0 - p)
        if bit == "1":
            p = y + one_minus_y * p
    return p


def _float_solve_gap_root(a: float, s1: int, b: float, qd1: int, rhs: float) -> float:
    """Fast float64 approximation of the unique root y in (0, 1) of a*P_{s1}(y) + b*P_{qd1}(y) = rhs."""
    if rhs <= 0.0:
        return 0.0
    if a + b <= rhs:
        return 1.0
    lo = 0.0
    hi = 1.0
    # Linear initial lower bound
    slope = a * s1 + b * qd1
    if slope > 0.0:
        y0 = rhs / slope
        if 0.0 < y0 < 1.0:
            lo = y0
            hi = min(1.0, max(2.0 * y0, y0 + 1e-6))
            while hi < 1.0 and a * _float_poly_gap(hi, s1) + b * _float_poly_gap(hi, qd1) < rhs:
                lo = hi
                hi = min(1.0, 2.0 * hi)
    for _ in range(56):
        mid = 0.5 * (lo + hi)
        if mid == lo or mid == hi:
            break
        if a * _float_poly_gap(mid, s1) + b * _float_poly_gap(mid, qd1) <= rhs:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _certified_gap_bounds_on_t(
    arc: _FareyArcSpec,
    t_iv: Interval,
    prec: int,
    *,
    bisect_steps: int = 24,
    need_lower_rho: bool = False,
    high_precision_root: bool = False,
) -> tuple[Decimal, Decimal]:
    """Return certified (rho_lo, rho_hi) enclosing rho_N(theta(t)) for all t in t_iv.

    Uses a fast float64 root guess followed by a single outward-rounded interval
    verification (with safeguarded bisection fallback), keeping 100% mathematical
    rigor while avoiding slow Decimal bisection at every branch-and-bound node.
    """
    if t_iv.lo <= _ZERO and t_iv.hi >= _ONE:
        return (_ZERO, _ONE)

    one_iv = Interval.exact(1)
    two_pi = two_pi_interval(prec)
    pi_iv = pi_interval(prec)
    one_minus_t = one_iv.sub(t_iv, prec).clamp(_ZERO, _ONE)

    h1 = pi_iv.mul(t_iv, prec).div(Interval.exact(arc.s), prec)
    h2 = pi_iv.mul(one_minus_t, prec).div(Interval.exact(arc.qd), prec)
    h3 = h1.add(h2, prec)

    b1 = two_pi.mul(t_iv, prec).div(Interval.exact(arc.s), prec)
    b2 = two_pi.mul(one_minus_t, prec).div(Interval.exact(arc.qd), prec)

    a_iv = sin_interval(b1, prec).clamp(_ZERO, _ONE)
    b_iv = sin_interval(b2, prec).clamp(_ZERO, _ONE)

    sh1 = sin_interval(h1, prec).clamp(_ZERO, _ONE)
    sh2 = sin_interval(h2, prec).clamp(_ZERO, _ONE)
    sh3 = sin_interval(h3, prec).clamp(_ZERO, _ONE)
    rhs_iv = Interval.exact(4).mul(sh1, prec).mul(sh2, prec).mul(sh3, prec)

    def _eval_phi(a_c: Interval, b_c: Interval, y_val: Decimal) -> Interval:
        y_i = Interval(y_val, y_val)
        return a_c.mul(_zero_cancel_poly_gap(y_i, arc.s1, prec), prec).add(
            b_c.mul(_zero_cancel_poly_gap(y_i, arc.qd1, prec), prec), prec
        )

    # 1. Certified upper bound rho_hi <= 1 (lower bound y_lo on gap y = 1 - rho_hat).
    a_hi_iv = Interval(a_iv.hi, a_iv.hi)
    b_hi_iv = Interval(b_iv.hi, b_iv.hi)
    rhs_lo = rhs_iv.lo

    if rhs_lo <= _ZERO:
        rho_hi = _ONE
    else:
        y_lo = _ZERO
        y_f = _float_solve_gap_root(float(a_iv.hi), arc.s1, float(b_iv.hi), arc.qd1, float(rhs_lo))
        # Try 1-shot certified verification slightly below float root
        verified = False
        if not high_precision_root and 0.0 < y_f < 1.0:
            for shrink in (1.0 - 1e-12, 1.0 - 1e-9, 1.0 - 1e-6):
                y_cand = Decimal.from_float(max(0.0, y_f * shrink))
                if y_cand > _ZERO and _eval_phi(a_hi_iv, b_hi_iv, y_cand).hi <= rhs_lo:
                    y_lo = y_cand
                    verified = True
                    break
        if not verified:
            # Safeguarded bisection (tightly bracketed around y_f when possible)
            y_hi = _ONE
            if 0.0 < y_f < 1.0:
                c_lo = Decimal.from_float(max(0.0, y_f * (1.0 - 1e-9)))
                c_hi = Decimal.from_float(min(1.0, y_f * (1.0 + 1e-9)))
                if _eval_phi(a_hi_iv, b_hi_iv, c_lo).hi <= rhs_lo:
                    y_lo = c_lo
                if _eval_phi(a_hi_iv, b_hi_iv, c_hi).hi > rhs_lo:
                    y_hi = c_hi
            steps = max(bisect_steps, 64) if high_precision_root else bisect_steps
            for _ in range(steps):
                mid = _floor_ctx(prec).divide(_floor_ctx(prec).add(y_lo, y_hi), _TWO)
                if mid <= y_lo or mid >= y_hi:
                    break
                if _eval_phi(a_hi_iv, b_hi_iv, mid).hi <= rhs_lo:
                    y_lo = mid
                else:
                    y_hi = mid
        rho_hat_hi = one_iv.sub(Interval(y_lo, y_lo), prec).clamp(_ZERO, _ONE)
        rho_hi = rho_hat_hi.pow_int(arc.d1, prec).clamp(_ZERO, _ONE).hi

    if not need_lower_rho:
        return (_ZERO, rho_hi)

    # 2. Certified lower bound rho_lo >= 0 (upper bound y_hi on gap y = 1 - rho_hat).
    a_lo_iv = Interval(a_iv.lo, a_iv.lo)
    b_lo_iv = Interval(b_iv.lo, b_iv.lo)
    rhs_hi = rhs_iv.hi
    if a_iv.lo + b_iv.lo <= rhs_hi:
        rho_lo = _ZERO
    else:
        y_hi_cert: Decimal | None = None
        y_f2 = _float_solve_gap_root(float(a_iv.lo), arc.s1, float(b_iv.lo), arc.qd1, float(rhs_hi))
        if not high_precision_root and 0.0 < y_f2 < 1.0:
            for grow in (1.0 + 1e-12, 1.0 + 1e-9, 1.0 + 1e-6):
                y_cand = Decimal.from_float(min(1.0, y_f2 * grow))
                if y_cand <= _ONE and _eval_phi(a_lo_iv, b_lo_iv, y_cand).lo >= rhs_hi:
                    y_hi_cert = y_cand
                    break
        if y_hi_cert is None:
            lo_b = _ZERO
            hi_b = _ONE
            if 0.0 < y_f2 < 1.0:
                c_lo = Decimal.from_float(max(0.0, y_f2 * (1.0 - 1e-9)))
                c_hi = Decimal.from_float(min(1.0, y_f2 * (1.0 + 1e-9)))
                if _eval_phi(a_lo_iv, b_lo_iv, c_lo).lo < rhs_hi:
                    lo_b = c_lo
                if _eval_phi(a_lo_iv, b_lo_iv, c_hi).lo >= rhs_hi:
                    hi_b = c_hi
            steps = max(bisect_steps, 64) if high_precision_root else bisect_steps + 16
            for _ in range(steps):
                mid = _ceil_ctx(prec).divide(_ceil_ctx(prec).add(lo_b, hi_b), _TWO)
                if mid <= lo_b or mid >= hi_b:
                    break
                if _eval_phi(a_lo_iv, b_lo_iv, mid).lo >= rhs_hi:
                    hi_b = mid
                else:
                    lo_b = mid
            if _eval_phi(a_lo_iv, b_lo_iv, hi_b).lo >= rhs_hi:
                y_hi_cert = hi_b
        if y_hi_cert is not None:
            rho_hat_lo = one_iv.sub(Interval(y_hi_cert, y_hi_cert), prec).clamp(_ZERO, _ONE)
            rho_lo = rho_hat_lo.pow_int(arc.d1, prec).clamp(_ZERO, _ONE).lo
        else:
            rho_lo = _ZERO

    return (rho_lo, rho_hi)


def _sector_distance_lb_polar(
    r_z_iv: Interval,
    ang_z_iv: Interval,
    theta_iv: Interval,
    rho_max: Decimal,
    prec: int,
) -> Decimal:
    """Certified lower bound on inf_{theta in theta_iv, 0 <= r <= rho_max} |z - r*e^{i*theta}|.

    Uses the zero-dependency polar identity (quadratic tightness near theta = arg(z)):
        |z - r*e^{i*theta}|^2 = (r - |z|*cos(theta - phi))^2 + (|z|*sin(theta - phi))^2.
    """
    delta_iv = theta_iv.sub(ang_z_iv, prec)
    c_iv = cos_interval(delta_iv, prec)
    s_iv = sin_interval(delta_iv, prec)
    p_iv = r_z_iv.mul(c_iv, prec)
    q_iv = r_z_iv.mul(s_iv, prec)
    r_iv = Interval(_ZERO, rho_max)
    d2_lo = _floor_ctx(prec).add(
        interval_distance_sq(r_iv, p_iv, prec),
        interval_distance_sq(Interval.exact(0), q_iv, prec),
    )
    if d2_lo <= _ZERO:
        return _ZERO
    return _dec_sqrt_floor(d2_lo, prec)


def _point_ray_distance_ub_polar(
    r_z_iv: Interval,
    ang_z_iv: Interval,
    theta_iv: Interval,
    rho_lo: Decimal,
    prec: int,
) -> Decimal:
    """Certified upper bound on dist(z, Theta_N) witnessed by r * e^{i*theta} for r in [0, rho_lo]."""
    delta_iv = theta_iv.sub(ang_z_iv, prec)
    c_iv = cos_interval(delta_iv, prec)
    s_iv = sin_interval(delta_iv, prec)
    p_iv = r_z_iv.mul(c_iv, prec)
    q_iv = r_z_iv.mul(s_iv, prec)
    p_mid = p_iv.midpoint(prec)
    r_star = max(_ZERO, min(rho_lo, p_mid))
    r_iv = Interval(r_star, r_star)
    d2 = r_iv.sub(p_iv, prec).sqr(prec).add(q_iv.sqr(prec), prec)
    return d2.sqrt(prec).hi


@dataclass(frozen=True)
class CertifiedRadiusEnclosure:
    """Two-sided mathematically certified enclosure of rho_N(angle)."""

    order: int
    angle_radians: float
    radius_lo: float
    radius_hi: float
    farey_left: Fraction
    farey_right: Fraction

    def to_dict(self) -> dict[str, object]:
        return {
            "order": self.order,
            "angle_radians": self.angle_radians,
            "radius_lo": self.radius_lo,
            "radius_hi": self.radius_hi,
            "width": self.radius_hi - self.radius_lo,
            "farey_left": f"{self.farey_left.numerator}/{self.farey_left.denominator}",
            "farey_right": f"{self.farey_right.numerator}/{self.farey_right.denominator}",
            "certification": "PROVED (outward-rounded Decimal interval arithmetic)",
        }


def certified_karpelevich_radius(
    order: int,
    angle_radians: float,
    *,
    prec: int = DEFAULT_PREC,
) -> CertifiedRadiusEnclosure:
    """Compute a mathematically certified two-sided enclosure [rho_lo, rho_hi] of rho_N(theta)."""
    n = int(order)
    if n < 2:
        raise ValueError("Karpelevič order must be at least 2")

    two_pi = two_pi_interval(prec)
    ang_iv = Interval.from_float(angle_radians)
    # Soundly enclose angle / (2*pi) and split across any integer wrap boundary
    # without ever clipping away valid negative or wrap-straddling residuals.
    q_iv = ang_iv.div(two_pi, prec)
    from decimal import ROUND_FLOOR

    k_lo = int(q_iv.lo.to_integral_value(rounding=ROUND_FLOOR))
    k_hi = int(q_iv.hi.to_integral_value(rounding=ROUND_FLOOR))
    if k_hi - k_lo >= 2 or (k_hi - k_lo == 1 and q_iv.hi - q_iv.lo >= _ONE):
        turns_intervals = [Interval(_ZERO, _ONE)]
    elif k_lo == k_hi:
        sub = q_iv.sub(Interval.exact(k_lo), prec).clamp(_ZERO, _ONE)
        turns_intervals = [sub]
    else:
        # Straddles integer boundary k_hi: retain both [q_lo - k_lo, 1] and [0, q_hi - k_hi]
        left_part = Interval(max(_ZERO, q_iv.sub(Interval.exact(k_lo), prec).lo), _ONE)
        right_part = Interval(_ZERO, min(_ONE, q_iv.sub(Interval.exact(k_hi), prec).hi))
        turns_intervals = [left_part, right_part]

    if n == 2:
        # Theta_2 = [-1, 1]: radius is 1 at turns in {0, 1/2, 1}, else 0.
        half = Decimal("0.5")
        hits_root = any(
            tiv.contains(_ZERO) or tiv.contains(half) or tiv.contains(_ONE)
            for tiv in turns_intervals
        )
        all_root = all(
            tiv.lo == tiv.hi and (tiv.lo == _ZERO or tiv.lo == half or tiv.lo == _ONE)
            for tiv in turns_intervals
        )
        if all_root:
            return CertifiedRadiusEnclosure(2, float(angle_radians), 1.0, 1.0, Fraction(0, 1), Fraction(1, 2))
        if hits_root:
            return CertifiedRadiusEnclosure(2, float(angle_radians), 0.0, 1.0, Fraction(0, 1), Fraction(1, 2))
        return CertifiedRadiusEnclosure(2, float(angle_radians), 0.0, 0.0, Fraction(0, 1), Fraction(1, 2))

    seq = farey_sequence(n)
    # Find all Farey arcs intersecting any wrapped turns interval
    rho_lo_all = _ONE
    rho_hi_all = _ZERO
    matched_left = seq[0]
    matched_right = seq[1]
    found = False
    for turns_iv in turns_intervals:
        for idx in range(len(seq) - 1):
            f_left, f_right = seq[idx], seq[idx + 1]
            l_iv = Interval.from_fraction(f_left, prec)
            r_iv = Interval.from_fraction(f_right, prec)
            if turns_iv.hi < l_iv.lo or turns_iv.lo > r_iv.hi:
                continue
            found = True
            matched_left, matched_right = f_left, f_right
            sub_turns = Interval(max(turns_iv.lo, l_iv.lo), min(turns_iv.hi, r_iv.hi))
            arc = _FareyArcSpec.from_farey_pair(n, f_left, f_right)
            qs_iv = Interval.exact(arc.q * arc.s)
            if not arc.reflected:
                t_iv = sub_turns.sub(l_iv, prec).mul(qs_iv, prec).clamp(_ZERO, _ONE)
            else:
                t_iv = r_iv.sub(sub_turns, prec).mul(qs_iv, prec).clamp(_ZERO, _ONE)
            r_lo, r_hi = _certified_gap_bounds_on_t(
                arc, t_iv, prec, bisect_steps=64, need_lower_rho=True, high_precision_root=True
            )
            rho_lo_all = min(rho_lo_all, r_lo)
            rho_hi_all = max(rho_hi_all, r_hi)

    if not found:
        return CertifiedRadiusEnclosure(n, float(angle_radians), 0.0, 1.0, seq[0], seq[-1])

    # Outward-round Decimal -> IEEE-754 float64 using math.nextafter only if needed
    lo_f = _decimal_to_float_floor(rho_lo_all)
    hi_f = _decimal_to_float_ceil(rho_hi_all)
    return CertifiedRadiusEnclosure(
        order=n,
        angle_radians=float(angle_radians),
        radius_lo=max(0.0, lo_f),
        radius_hi=min(1.0, hi_f),
        farey_left=matched_left,
        farey_right=matched_right,
    )


def _decimal_to_float_floor(value: Decimal) -> float:
    """Convert Decimal to float guaranteed <= value (sound on binary64 overflow)."""
    import math
    import sys

    f = float(value)
    if math.isnan(f):
        raise ValueError("Cannot convert NaN Decimal")
    if math.isinf(f):
        if f > 0.0 and not value.is_infinite():
            return sys.float_info.max
        return f
    while Decimal.from_float(f) > value:
        f = math.nextafter(f, -math.inf)
    return f


def _decimal_to_float_ceil(value: Decimal) -> float:
    """Convert Decimal to float guaranteed >= value (sound on binary64 overflow)."""
    import math
    import sys

    f = float(value)
    if math.isnan(f):
        raise ValueError("Cannot convert NaN Decimal")
    if math.isinf(f):
        if f < 0.0 and not value.is_infinite():
            return -sys.float_info.max
        return f
    while Decimal.from_float(f) < value:
        f = math.nextafter(f, math.inf)
    return f


@dataclass(frozen=True)
class CertifiedDistanceResult:
    """Mathematically certified global Euclidean distance enclosure to Theta_order."""

    order: int
    distance_lo: float
    distance_hi: float
    closest_angle_radians: float
    certified_inside: bool
    pruned_arcs: int
    evaluated_subintervals: int
    status: str

    def to_dict(self) -> dict[str, object]:
        return {
            "order": self.order,
            "distance_lo": self.distance_lo,
            "distance_hi": self.distance_hi,
            "enclosure_width": self.distance_hi - self.distance_lo,
            "closest_angle_radians": self.closest_angle_radians,
            "certified_inside": self.certified_inside,
            "pruned_arcs": self.pruned_arcs,
            "evaluated_subintervals": self.evaluated_subintervals,
            "status": self.status,
            "certification": "PROVED (outward-rounded interval branch-and-bound over all Farey arcs)",
        }


def certified_distance_to_karpelevich(
    value: complex,
    order: int,
    *,
    target_radius: float | None = None,
    tol: float = 1e-7,
    max_subdivisions: int = 8_000,
    prec: int = 24,
) -> CertifiedDistanceResult:
    """Compute a mathematically certified enclosure [d_lo, d_hi] of dist(value, Theta_order).

    Covers all of [0, 2*pi) rigorously across every Farey arc of F_order.
    If ``target_radius`` is provided, may terminate early as soon as
    ``d_lo > target_radius`` (certified disjoint) or ``d_hi <= target_radius``
    (certified non-disjoint).
    """
    n = int(order)
    if n < 1:
        raise ValueError("order must be positive")
    if tol <= 0.0:
        raise ValueError("tol must be positive")
    if target_radius is not None and target_radius < 0.0:
        raise ValueError("target_radius must be non-negative")

    z = complex(value)
    # Conjugation symmetry: Theta_N is symmetric about the real axis.
    reflected_z = z.imag < 0.0
    x_iv = Interval.from_float(z.real)
    y_iv = Interval.from_float(abs(z.imag))

    # Exact case N = 1: Theta_1 = {1}
    if n == 1:
        dx = x_iv.sub(Interval.exact(1), prec)
        d_iv = dx.sqr(prec).add(y_iv.sqr(prec), prec).sqrt(prec)
        d_lo = max(0.0, _decimal_to_float_floor(d_iv.lo))
        d_hi = _decimal_to_float_ceil(d_iv.hi)
        return CertifiedDistanceResult(
            order=1,
            distance_lo=d_lo,
            distance_hi=d_hi,
            closest_angle_radians=0.0,
            certified_inside=(d_hi == 0.0),
            pruned_arcs=0,
            evaluated_subintervals=1,
            status="exact_order_1",
        )

    # Exact case N = 2: Theta_2 = [-1, 1]
    if n == 2:
        dx_sq = interval_distance_sq(x_iv, Interval(Decimal(-1), Decimal(1)), prec)
        dy_sq = y_iv.sqr(prec)
        # Upper bound: clamp x to [-1, 1]
        x_clamped = max(Decimal(-1), min(Decimal(1), x_iv.lo))
        d_hi_iv = x_iv.sub(Interval(x_clamped, x_clamped), prec).sqr(prec).add(dy_sq, prec).sqrt(prec)
        d_lo_dec = _dec_sqrt_floor(_floor_ctx(prec).add(dx_sq, dy_sq.lo), prec)
        d_lo = max(0.0, _decimal_to_float_floor(d_lo_dec))
        d_hi = _decimal_to_float_ceil(d_hi_iv.hi)
        closest_ang = 0.0 if x_clamped >= _ZERO else float(pi_interval(prec).midpoint(prec))
        return CertifiedDistanceResult(
            order=2,
            distance_lo=d_lo,
            distance_hi=d_hi,
            closest_angle_radians=closest_ang,
            certified_inside=(d_hi == 0.0),
            pruned_arcs=0,
            evaluated_subintervals=1,
            status="exact_order_2",
        )

    # N >= 3:
    # Step 1: Quick check if z = 0 (always inside Theta_N for N >= 2)
    if x_iv.lo == _ZERO and y_iv.lo == _ZERO:
        return CertifiedDistanceResult(
            order=n,
            distance_lo=0.0,
            distance_hi=0.0,
            closest_angle_radians=0.0,
            certified_inside=True,
            pruned_arcs=0,
            evaluated_subintervals=0,
            status="certified_inside_origin",
        )

    # Step 2: Check whether z is certified INSIDE Theta_N along its own ray
    r_z_iv = x_iv.sqr(prec).add(y_iv.sqr(prec), prec).sqrt(prec)
    ang_z_iv = atan2_point_interval(y_iv.lo, x_iv.lo, prec)
    if r_z_iv.hi <= _ONE:
        # Evaluate rho_N on ang_z_iv
        two_pi = two_pi_interval(prec)
        turns_z = ang_z_iv.div(two_pi, prec).clamp(_ZERO, _ONE)
        seq = farey_sequence(n)
        rho_z_lo = _ONE
        for idx in range(len(seq) - 1):
            f_left, f_right = seq[idx], seq[idx + 1]
            l_iv = Interval.from_fraction(f_left, prec)
            r_iv = Interval.from_fraction(f_right, prec)
            if turns_z.hi < l_iv.lo or turns_z.lo > r_iv.hi:
                continue
            sub_turns = Interval(max(turns_z.lo, l_iv.lo), min(turns_z.hi, r_iv.hi))
            arc = _FareyArcSpec.from_farey_pair(n, f_left, f_right)
            qs_iv = Interval.exact(arc.q * arc.s)
            if not arc.reflected:
                t_iv = sub_turns.sub(l_iv, prec).mul(qs_iv, prec).clamp(_ZERO, _ONE)
            else:
                t_iv = r_iv.sub(sub_turns, prec).mul(qs_iv, prec).clamp(_ZERO, _ONE)
            r_lo_seg, _ = _certified_gap_bounds_on_t(
                arc, t_iv, prec, bisect_steps=48, need_lower_rho=True
            )
            rho_z_lo = min(rho_z_lo, r_lo_seg)
        if r_z_iv.hi <= rho_z_lo:
            ang_out = float(ang_z_iv.midpoint(prec))
            if reflected_z:
                ang_out = float(two_pi.midpoint(prec)) - ang_out
            return CertifiedDistanceResult(
                order=n,
                distance_lo=0.0,
                distance_hi=0.0,
                closest_angle_radians=ang_out,
                certified_inside=True,
                pruned_arcs=0,
                evaluated_subintervals=1,
                status="certified_inside_ray",
            )

    # Step 3: Build global initial upper bound d_hi from Farey roots of unity + ray projection
    seq = farey_sequence(n)
    two_pi = two_pi_interval(prec)
    best_ub = r_z_iv.hi  # 0 in Theta_N always gives valid upper bound |z|
    best_angle_dec = _ZERO

    # Check all Farey roots e^{2*pi*i*p/q} in Theta_N (cheap: O(N^2) points, <= 1000 for N<=50)
    for frac in seq[:-1]:
        theta_f = Interval.from_fraction(frac, prec).mul(two_pi, prec)
        ub = _point_ray_distance_ub_polar(r_z_iv, ang_z_iv, theta_f, _ONE, prec)
        if ub < best_ub:
            best_ub = ub
            best_angle_dec = theta_f.midpoint(prec)

    # Also test along z's own ray (often very close to the global minimizer!)
    turns_z = ang_z_iv.div(two_pi, prec).clamp(_ZERO, _ONE)
    for idx in range(len(seq) - 1):
        f_left, f_right = seq[idx], seq[idx + 1]
        l_iv = Interval.from_fraction(f_left, prec)
        r_iv = Interval.from_fraction(f_right, prec)
        if turns_z.hi < l_iv.lo or turns_z.lo > r_iv.hi:
            continue
        sub_turns = Interval(max(turns_z.lo, l_iv.lo), min(turns_z.hi, r_iv.hi))
        arc = _FareyArcSpec.from_farey_pair(n, f_left, f_right)
        qs_iv = Interval.exact(arc.q * arc.s)
        t_mid = (
            sub_turns.sub(l_iv, prec).mul(qs_iv, prec).midpoint(prec)
            if not arc.reflected
            else r_iv.sub(sub_turns, prec).mul(qs_iv, prec).midpoint(prec)
        )
        t_mid = max(_ZERO, min(_ONE, t_mid))
        t_pt = Interval(t_mid, t_mid)
        r_lo_ray, _ = _certified_gap_bounds_on_t(arc, t_pt, prec, bisect_steps=24, need_lower_rho=True)
        theta_pt = arc.angle_interval_for_t(t_pt, prec)
        ub_ray = _point_ray_distance_ub_polar(r_z_iv, ang_z_iv, theta_pt, r_lo_ray, prec)
        if ub_ray < best_ub:
            best_ub = ub_ray
            best_angle_dec = theta_pt.midpoint(prec)

    target_dec = Decimal.from_float(target_radius) if target_radius is not None else None
    tol_dec = Decimal.from_float(tol)

    # Quick early exit if already certified NOT excluded (d_hi <= target_radius)
    if target_dec is not None and best_ub <= target_dec:
        ang_out = float(best_angle_dec)
        if reflected_z and ang_out > 0.0:
            ang_out = float(two_pi.midpoint(prec)) - ang_out
        return CertifiedDistanceResult(
            order=n,
            distance_lo=0.0,
            distance_hi=_decimal_to_float_ceil(best_ub),
            closest_angle_radians=ang_out,
            certified_inside=(best_ub == _ZERO),
            pruned_arcs=0,
            evaluated_subintervals=1,
            status="certified_not_excluded_early",
        )

    # Step 4: Sweep EVERY Farey arc of F_N covering [0, 2*pi).
    # Rigorously prune arcs whose trivial unit-disk sector lower bound exceeds best_ub.
    # Push remaining arcs into a min-heap keyed by certified lower bound.
    pruned_min_lb = Decimal("Infinity")
    pruned_arcs = 0
    evaluated = 0
    # Heap entries: (lb_float, tie_breaker, lb_dec, arc_index, t_lo, t_hi)
    arcs: list[_FareyArcSpec] = []
    heap: list[tuple[float, int, Decimal, int, Decimal, Decimal]] = []
    counter = 0

    for idx in range(len(seq) - 1):
        f_left, f_right = seq[idx], seq[idx + 1]
        theta_arc = Interval.from_fraction(f_left, prec).mul(two_pi, prec)
        theta_arc_hi = Interval.from_fraction(f_right, prec).mul(two_pi, prec)
        full_theta = Interval(theta_arc.lo, theta_arc_hi.hi)
        # Rigorous unit-disk pruning (rho_max = 1)
        trivial_lb = _sector_distance_lb_polar(r_z_iv, ang_z_iv, full_theta, _ONE, prec)
        if trivial_lb > best_ub:
            pruned_arcs += 1
            if trivial_lb < pruned_min_lb:
                pruned_min_lb = trivial_lb
            continue
        arc = _FareyArcSpec.from_farey_pair(n, f_left, f_right)
        arc_idx = len(arcs)
        arcs.append(arc)
        # Split initial arc at t=0.5 so interior gap is immediately active away from endpoints
        for t_lo, t_hi in ((_ZERO, Decimal("0.5")), (Decimal("0.5"), _ONE)):
            t_iv = Interval(t_lo, t_hi)
            theta_sub = arc.angle_interval_for_t(t_iv, prec)
            _, rho_hi = _certified_gap_bounds_on_t(arc, t_iv, prec, bisect_steps=20, need_lower_rho=False)
            lb = _sector_distance_lb_polar(r_z_iv, ang_z_iv, theta_sub, rho_hi, prec)
            evaluated += 1
            if lb > best_ub:
                if lb < pruned_min_lb:
                    pruned_min_lb = lb
            else:
                counter += 1
                heapq.heappush(heap, (lb, counter, arc_idx, t_lo, t_hi))

    # Step 5: Best-first branch-and-bound keyed by exact Decimal lower bound
    status = "converged"
    while heap and evaluated < max_subdivisions:
        current_lb, _, arc_idx, t_lo, t_hi = heap[0]
        global_lb = min(current_lb, pruned_min_lb)

        # Check termination criteria
        if target_dec is not None:
            if global_lb > target_dec:
                status = "certified_excluded"
                break
            if best_ub <= target_dec:
                status = "certified_not_excluded"
                break
        if best_ub - global_lb <= tol_dec:
            status = "converged"
            break

        heapq.heappop(heap)
        if current_lb > best_ub:
            if current_lb < pruned_min_lb:
                pruned_min_lb = current_lb
            continue

        arc = arcs[arc_idx]
        t_mid = _floor_ctx(prec).divide(_floor_ctx(prec).add(t_lo, t_hi), _TWO)
        if t_mid <= t_lo or t_mid >= t_hi:
            # Precision floor reached; reinsert and stop
            counter += 1
            heapq.heappush(heap, (current_lb, counter, arc_idx, t_lo, t_hi))
            status = "precision_limit"
            break

        # Sample midpoint to tighten upper bound best_ub
        t_pt = Interval(t_mid, t_mid)
        r_lo_mid, _ = _certified_gap_bounds_on_t(arc, t_pt, prec, bisect_steps=24, need_lower_rho=True)
        theta_mid = arc.angle_interval_for_t(t_pt, prec)
        ub_mid = _point_ray_distance_ub_polar(r_z_iv, ang_z_iv, theta_mid, r_lo_mid, prec)
        if ub_mid < best_ub:
            best_ub = ub_mid
            best_angle_dec = theta_mid.midpoint(prec)

        # Subdivide into [t_lo, t_mid] and [t_mid, t_hi]
        for sub_lo, sub_hi in ((t_lo, t_mid), (t_mid, t_hi)):
            sub_iv = Interval(sub_lo, sub_hi)
            theta_sub = arc.angle_interval_for_t(sub_iv, prec)
            _, rho_hi = _certified_gap_bounds_on_t(
                arc, sub_iv, prec, bisect_steps=20, need_lower_rho=False
            )
            lb_sub = _sector_distance_lb_polar(r_z_iv, ang_z_iv, theta_sub, rho_hi, prec)
            # Monotonicity tightening: a child interval cannot have a smaller true minimum than its parent
            lb_sub = max(lb_sub, current_lb)
            evaluated += 1
            if lb_sub > best_ub:
                if lb_sub < pruned_min_lb:
                    pruned_min_lb = lb_sub
            else:
                counter += 1
                heapq.heappush(heap, (lb_sub, counter, arc_idx, sub_lo, sub_hi))
    else:
        if heap and (best_ub - min(heap[0][0], pruned_min_lb) > tol_dec):
            status = "max_subdivisions_reached"

    final_lb_dec = min(heap[0][0], pruned_min_lb) if heap else min(pruned_min_lb, best_ub)
    # Guard final_lb_dec <= best_ub
    final_lb_dec = min(final_lb_dec, best_ub)
    d_lo = max(0.0, _decimal_to_float_floor(final_lb_dec))
    d_hi = _decimal_to_float_ceil(best_ub)
    ang_out = float(best_angle_dec)
    if reflected_z and ang_out > 0.0:
        ang_out = float(two_pi.midpoint(prec)) - ang_out

    return CertifiedDistanceResult(
        order=n,
        distance_lo=d_lo,
        distance_hi=d_hi,
        closest_angle_radians=ang_out,
        certified_inside=(d_hi == 0.0),
        pruned_arcs=pruned_arcs,
        evaluated_subintervals=evaluated,
        status=status,
    )


@dataclass(frozen=True)
class CertifiedOrderTest:
    """Result of testing one stochastic order N with interval-certified distance."""

    order: int
    disk_radius: float
    distance_lo: float
    distance_hi: float
    closest_angle_radians: float
    certified_excluded: bool
    certified_inside: bool
    pruned_arcs: int
    evaluated_subintervals: int
    status: str

    def to_dict(self) -> dict[str, object]:
        return {
            "order": self.order,
            "disk_radius": self.disk_radius,
            "distance_lo": self.distance_lo,
            "distance_hi": self.distance_hi,
            "closest_angle_radians": self.closest_angle_radians,
            "certified_excluded": self.certified_excluded,
            "certified_inside": self.certified_inside,
            "pruned_arcs": self.pruned_arcs,
            "evaluated_subintervals": self.evaluated_subintervals,
            "status": self.status,
        }


@dataclass(frozen=True)
class CertifiedExclusionReport:
    """Interval-certified exclusion report across nested Karpelevič regions Theta_N."""

    point_estimate: complex
    disk_radius: float
    confidence_level: float
    hankel_rank_lower_bound: int
    maximum_order_tested: int
    certified_excluded_through: int
    certified_classical_state_lower_bound: int
    tests: tuple[CertifiedOrderTest, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "point_estimate": [self.point_estimate.real, self.point_estimate.imag],
            "disk_radius": self.disk_radius,
            "confidence_level": self.confidence_level,
            "hankel_rank_lower_bound": self.hankel_rank_lower_bound,
            "maximum_order_tested": self.maximum_order_tested,
            "certified_excluded_through": self.certified_excluded_through,
            "certified_classical_state_lower_bound": self.certified_classical_state_lower_bound,
            "tests": [test.to_dict() for test in self.tests],
            "certification": (
                "PROVED geometric separation: every excluded order N satisfies "
                "distance_lo > disk_radius via outward-rounded interval arithmetic "
                "over all Farey arcs of Theta_N."
            ),
        }


def certify_finite_stochastic_exclusions(
    point_estimate: complex,
    disk_radius: float,
    *,
    confidence_level: float,
    hankel_rank_lower_bound: int,
    maximum_order: int = 30,
    tol: float = 1e-4,
    early_stop: bool = False,
    prec: int = 24,
) -> CertifiedExclusionReport:
    """Certify exclusion of nested stochastic orders Theta_2, ..., Theta_{maximum_order}.

    When ``early_stop=True``, uses ``target_radius=disk_radius`` for fast
    exclusion certification and stops once an order is not excluded.
    When ``early_stop=False``, computes tight distance enclosures through
    ``maximum_order`` (stopping only if the point is certified inside Theta_N).
    """
    if disk_radius < 0.0:
        raise ValueError("disk_radius must be non-negative")
    if hankel_rank_lower_bound < 1:
        raise ValueError("hankel_rank_lower_bound must be positive")
    if maximum_order < 2:
        raise ValueError("maximum_order must be at least 2")

    z = complex(point_estimate)
    tests: list[CertifiedOrderTest] = []
    # Explicitly test order 1 (Theta_1 = {1}) before testing higher orders.
    res1 = certified_distance_to_karpelevich(z, 1, tol=tol, prec=prec)
    if res1.distance_lo > disk_radius:
        excluded_through = 1
        contiguous = True
    else:
        excluded_through = 0
        contiguous = False

    if not (early_stop and not contiguous):
        for order in range(2, maximum_order + 1):
            res = certified_distance_to_karpelevich(
                z,
                order,
                target_radius=(disk_radius if early_stop else None),
                tol=tol,
                prec=prec,
            )
            excluded = bool(res.distance_lo > disk_radius)
            if contiguous and excluded:
                excluded_through = order
            else:
                contiguous = False
            tests.append(
                CertifiedOrderTest(
                    order=order,
                    disk_radius=float(disk_radius),
                    distance_lo=res.distance_lo,
                    distance_hi=res.distance_hi,
                    closest_angle_radians=res.closest_angle_radians,
                    certified_excluded=excluded,
                    certified_inside=res.certified_inside,
                    pruned_arcs=res.pruned_arcs,
                    evaluated_subintervals=res.evaluated_subintervals,
                    status=res.status,
                )
            )
            if res.certified_inside:
                break
            if early_stop and not excluded:
                break

    return CertifiedExclusionReport(
        point_estimate=z,
        disk_radius=float(disk_radius),
        confidence_level=float(confidence_level),
        hankel_rank_lower_bound=int(hankel_rank_lower_bound),
        maximum_order_tested=int(maximum_order),
        certified_excluded_through=int(excluded_through),
        certified_classical_state_lower_bound=max(
            int(hankel_rank_lower_bound), int(excluded_through) + 1
        ),
        tests=tuple(tests),
    )
