"""Self-contained outward-rounded arbitrary-precision interval arithmetic.

Every arithmetic operation and transcendental enclosure uses Python's C-backed
``decimal`` module with explicit ``ROUND_FLOOR`` (lower endpoint) and
``ROUND_CEILING`` (upper endpoint) contexts, requiring zero external
dependencies beyond the Python standard library.

Careful decimal hygiene:
- Bare Python ``-d``, ``abs(d)``, ``+``, ``-``, ``*``, ``/`` on ``Decimal``
  objects round to the thread's default 28-digit context; this module NEVER
  uses them on high-precision values, using ``copy_negate()``, ``copy_abs()``,
  and explicit ``Context`` methods everywhere.
- ``decimal.Context.sqrt()`` ignores ``ROUND_FLOOR``/``ROUND_CEILING`` (it
  always rounds half-even per IEEE 754-2008 / IBM GDA); ``Interval.sqrt()``
  therefore verifies ``s_lo^2 <= lo`` and ``s_hi^2 >= hi`` explicitly and steps
  via ``next_minus`` / ``next_plus`` if needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction
from functools import lru_cache

DEFAULT_PREC = 28

_ZERO = Decimal(0)
_ONE = Decimal(1)
_NEG_ONE = Decimal(-1)
_TWO = Decimal(2)
_FOUR = Decimal(4)


@lru_cache(maxsize=64)
def _floor_ctx(prec: int) -> Context:
    return Context(prec=prec, rounding=ROUND_FLOOR)


@lru_cache(maxsize=64)
def _ceil_ctx(prec: int) -> Context:
    return Context(prec=prec, rounding=ROUND_CEILING)


def _dec_floor(value: Decimal, prec: int) -> Decimal:
    return _floor_ctx(prec).plus(value)


def _dec_ceil(value: Decimal, prec: int) -> Decimal:
    return _ceil_ctx(prec).plus(value)


def _dec_sqrt_floor(value: Decimal, prec: int) -> Decimal:
    """Return Decimal s with exact s*s <= value (guaranteed outward lower bound).

    Scales by an even power of 10 so the verification product never underflows
    or overflows even near Decimal exponent limits.
    """
    if value <= _ZERO:
        return _ZERO
    # Scale value into [1, 100) by an even power 10^(2*k)
    k = value.adjusted() // 2
    scaled = value.scaleb(-2 * k)
    f = _floor_ctx(prec)
    check_c = _ceil_ctx(max(2 * prec + 4, 60))
    s = f.sqrt(scaled)
    while check_c.multiply(s, s) > scaled:
        s = f.next_minus(s)
    s = max(_ZERO, s)
    return _floor_ctx(prec).plus(s.scaleb(k))


def _dec_sqrt_ceil(value: Decimal, prec: int) -> Decimal:
    """Return Decimal s with exact s*s >= value (guaranteed outward upper bound).

    Scales by an even power of 10 so the verification product never underflows
    or overflows even near Decimal exponent limits.
    """
    if value <= _ZERO:
        return _ZERO
    k = value.adjusted() // 2
    scaled = value.scaleb(-2 * k)
    c = _ceil_ctx(prec)
    check_f = _floor_ctx(max(2 * prec + 4, 60))
    s = c.sqrt(scaled)
    while check_f.multiply(s, s) < scaled:
        s = c.next_plus(s)
    return _ceil_ctx(prec).plus(s.scaleb(k))


@dataclass(frozen=True, slots=True)
class Interval:
    """Closed real interval ``[lo, hi]`` with outward-rounded Decimal endpoints."""

    lo: Decimal
    hi: Decimal

    def __post_init__(self) -> None:
        if self.lo.is_nan() or self.hi.is_nan():
            raise ValueError("Interval endpoints must not be NaN")
        if self.lo > self.hi:
            raise ValueError(f"Invalid interval: lo={self.lo} > hi={self.hi}")

    @classmethod
    def exact(cls, value: int | Decimal) -> "Interval":
        d = Decimal(value) if isinstance(value, int) else value
        return cls(d, d)

    @classmethod
    def from_float(cls, value: float) -> "Interval":
        """Losslessly represent an IEEE-754 float as a point interval."""
        d = Decimal.from_float(float(value))
        return cls(d, d)

    @classmethod
    def from_fraction(cls, value: Fraction, prec: int = DEFAULT_PREC) -> "Interval":
        """Outwardly enclose an exact rational Fraction."""
        num = Decimal(value.numerator)
        den = Decimal(value.denominator)
        lo = _floor_ctx(prec).divide(num, den)
        hi = _ceil_ctx(prec).divide(num, den)
        return cls(lo, hi)

    @classmethod
    def hull(cls, a: "Interval", b: "Interval") -> "Interval":
        return cls(min(a.lo, b.lo), max(a.hi, b.hi))

    def width(self, prec: int = DEFAULT_PREC) -> Decimal:
        return _ceil_ctx(prec).subtract(self.hi, self.lo)

    def midpoint(self, prec: int = DEFAULT_PREC) -> Decimal:
        f = _floor_ctx(prec)
        return f.divide(f.add(self.lo, self.hi), _TWO)

    def contains(self, value: Decimal | float | int) -> bool:
        d = Decimal.from_float(value) if isinstance(value, float) else Decimal(value)
        return self.lo <= d <= self.hi

    def abs(self) -> "Interval":
        if self.lo >= _ZERO:
            return self
        if self.hi <= _ZERO:
            return Interval(self.hi.copy_negate(), self.lo.copy_negate())
        return Interval(_ZERO, max(self.lo.copy_negate(), self.hi))

    def neg(self) -> "Interval":
        return Interval(self.hi.copy_negate(), self.lo.copy_negate())

    def add(self, other: "Interval", prec: int = DEFAULT_PREC) -> "Interval":
        return Interval(
            _floor_ctx(prec).add(self.lo, other.lo),
            _ceil_ctx(prec).add(self.hi, other.hi),
        )

    def sub(self, other: "Interval", prec: int = DEFAULT_PREC) -> "Interval":
        return Interval(
            _floor_ctx(prec).subtract(self.lo, other.hi),
            _ceil_ctx(prec).subtract(self.hi, other.lo),
        )

    def mul(self, other: "Interval", prec: int = DEFAULT_PREC) -> "Interval":
        f = _floor_ctx(prec)
        c = _ceil_ctx(prec)
        if self.lo >= _ZERO and other.lo >= _ZERO:
            return Interval(f.multiply(self.lo, other.lo), c.multiply(self.hi, other.hi))
        p_lo = (
            f.multiply(self.lo, other.lo),
            f.multiply(self.lo, other.hi),
            f.multiply(self.hi, other.lo),
            f.multiply(self.hi, other.hi),
        )
        p_hi = (
            c.multiply(self.lo, other.lo),
            c.multiply(self.lo, other.hi),
            c.multiply(self.hi, other.lo),
            c.multiply(self.hi, other.hi),
        )
        return Interval(min(p_lo), max(p_hi))

    def div(self, other: "Interval", prec: int = DEFAULT_PREC) -> "Interval":
        if other.lo <= _ZERO <= other.hi:
            raise ZeroDivisionError(f"Interval division by interval containing zero: {other}")
        f = _floor_ctx(prec)
        c = _ceil_ctx(prec)
        if self.lo >= _ZERO and other.lo > _ZERO:
            return Interval(f.divide(self.lo, other.hi), c.divide(self.hi, other.lo))
        q_lo = (
            f.divide(self.lo, other.lo),
            f.divide(self.lo, other.hi),
            f.divide(self.hi, other.lo),
            f.divide(self.hi, other.hi),
        )
        q_hi = (
            c.divide(self.lo, other.lo),
            c.divide(self.lo, other.hi),
            c.divide(self.hi, other.lo),
            c.divide(self.hi, other.hi),
        )
        return Interval(min(q_lo), max(q_hi))

    def sqr(self, prec: int = DEFAULT_PREC) -> "Interval":
        f = _floor_ctx(prec)
        c = _ceil_ctx(prec)
        if self.lo >= _ZERO:
            return Interval(f.multiply(self.lo, self.lo), c.multiply(self.hi, self.hi))
        if self.hi <= _ZERO:
            return Interval(f.multiply(self.hi, self.hi), c.multiply(self.lo, self.lo))
        m = max(self.lo.copy_negate(), self.hi)
        return Interval(_ZERO, c.multiply(m, m))

    def sqrt(self, prec: int = DEFAULT_PREC) -> "Interval":
        if self.hi < _ZERO:
            raise ValueError(f"sqrt of strictly negative interval: {self}")
        lo_in = max(_ZERO, self.lo)
        return Interval(_dec_sqrt_floor(lo_in, prec), _dec_sqrt_ceil(self.hi, prec))

    def pow_int(self, exponent: int, prec: int = DEFAULT_PREC) -> "Interval":
        """Exact outward-rounded integer power for integer exponent."""
        n = int(exponent)
        if n < 0:
            return Interval.exact(1).div(self.pow_int(-n, prec), prec)
        if n == 0:
            return Interval.exact(1)
        if n == 1:
            return Interval(_dec_floor(self.lo, prec), _dec_ceil(self.hi, prec))
        if n == 2:
            return self.sqr(prec)

        def _pos_pow(val: Decimal, ctx: Context) -> Decimal:
            res = _ONE
            base = val
            k = n
            while k > 0:
                if k & 1:
                    res = ctx.multiply(res, base)
                k >>= 1
                if k > 0:
                    base = ctx.multiply(base, base)
            return res

        f = _floor_ctx(prec)
        c = _ceil_ctx(prec)
        if self.lo >= _ZERO:
            return Interval(_pos_pow(self.lo, f), _pos_pow(self.hi, c))
        if n % 2 == 1:
            lo_out = (
                _pos_pow(self.lo.copy_negate(), c).copy_negate()
                if self.lo < _ZERO
                else _pos_pow(self.lo, f)
            )
            hi_out = (
                _pos_pow(self.hi.copy_negate(), f).copy_negate()
                if self.hi < _ZERO
                else _pos_pow(self.hi, c)
            )
            return Interval(lo_out, hi_out)
        if self.hi <= _ZERO:
            return Interval(
                _pos_pow(self.hi.copy_negate(), f),
                _pos_pow(self.lo.copy_negate(), c),
            )
        m = max(self.lo.copy_negate(), self.hi)
        return Interval(_ZERO, _pos_pow(m, c))

    def clamp(self, lower: Decimal, upper: Decimal) -> "Interval":
        lo = max(lower, min(upper, self.lo))
        hi = max(lower, min(upper, self.hi))
        return Interval(lo, hi)

    def __neg__(self) -> "Interval":
        return self.neg()

    def __add__(self, other: "Interval") -> "Interval":
        return self.add(other)

    def __sub__(self, other: "Interval") -> "Interval":
        return self.sub(other)

    def __mul__(self, other: "Interval") -> "Interval":
        return self.mul(other)

    def __truediv__(self, other: "Interval") -> "Interval":
        return self.div(other)


def _atan_inv_int(m: int, prec: int) -> Interval:
    """Certified enclosure of arctan(1/m) for integer m >= 2 via alternating series."""
    work_prec = prec + 10
    cutoff = Decimal(1).scaleb(-(prec + 6))
    total = Interval.exact(0)
    power = m
    k = 0
    f_ctx = _floor_ctx(work_prec)
    c_ctx = _ceil_ctx(work_prec)
    while True:
        denom = Decimal((2 * k + 1) * power)
        term_lo = f_ctx.divide(_ONE, denom)
        term_hi = c_ctx.divide(_ONE, denom)
        term = Interval(term_lo, term_hi)
        if term_hi < cutoff:
            rem = Interval(_ZERO, term_hi) if k % 2 == 0 else Interval(term_hi.copy_negate(), _ZERO)
            total = total.add(rem, work_prec)
            break
        if k % 2 == 0:
            total = total.add(term, work_prec)
        else:
            total = total.sub(term, work_prec)
        power *= m * m
        k += 1
    return Interval(_dec_floor(total.lo, prec), _dec_ceil(total.hi, prec))


@lru_cache(maxsize=64)
def pi_interval(prec: int = DEFAULT_PREC) -> Interval:
    """Certified enclosure of pi via Machin's formula: pi = 16*atan(1/5) - 4*atan(1/239)."""
    work_prec = prec + 8
    a5 = _atan_inv_int(5, work_prec)
    a239 = _atan_inv_int(239, work_prec)
    pi_val = Interval.exact(16).mul(a5, work_prec).sub(
        Interval.exact(4).mul(a239, work_prec), work_prec
    )
    return Interval(_dec_floor(pi_val.lo, prec), _dec_ceil(pi_val.hi, prec))


@lru_cache(maxsize=64)
def two_pi_interval(prec: int = DEFAULT_PREC) -> Interval:
    return Interval.exact(2).mul(pi_interval(prec), prec)


@lru_cache(maxsize=64)
def half_pi_interval(prec: int = DEFAULT_PREC) -> Interval:
    return pi_interval(prec).div(Interval.exact(2), prec)


@lru_cache(maxsize=256)
def _factorial_dec(n: int) -> Decimal:
    res = 1
    for i in range(2, n + 1):
        res *= i
    return Decimal(res)


@lru_cache(maxsize=64)
def _sin_cos_taylor_coeffs(n_terms: int, work_prec: int) -> tuple[tuple[Interval, ...], tuple[Interval, ...]]:
    s_list = []
    c_list = []
    for j in range(n_terms - 1, -1, -1):
        sign = _ONE if (j % 2 == 0) else _NEG_ONE
        s_list.append(Interval.exact(sign).div(Interval.exact(_factorial_dec(2 * j + 1)), work_prec))
        c_list.append(Interval.exact(sign).div(Interval.exact(_factorial_dec(2 * j)), work_prec))
    return (tuple(s_list), tuple(c_list))


def _sin_cos_reduced(u: Interval, prec: int) -> tuple[Interval, Interval]:
    """Certified (sin(u), cos(u)) for |u| <= 1 via cached Horner Taylor series + Lagrange remainder."""
    work_prec = prec + 6
    u_abs_max = max(u.lo.copy_abs(), u.hi.copy_abs())
    if u_abs_max > _ONE:
        raise ValueError(f"Reduced argument exceeds 1: {u}")
    # For |u| <= 0.85, (2N)! >= 10^(work_prec + 2): N = work_prec // 3 + 7 is ample.
    n_terms = max(12, (work_prec // 3) + 7)
    u2 = u.sqr(work_prec)
    s_coeffs, c_coeffs = _sin_cos_taylor_coeffs(n_terms, work_prec)

    sin_acc = s_coeffs[0]
    cos_acc = c_coeffs[0]
    for s_c, c_c in zip(s_coeffs[1:], c_coeffs[1:]):
        sin_acc = sin_acc.mul(u2, work_prec).add(s_c, work_prec)
        cos_acc = cos_acc.mul(u2, work_prec).add(c_c, work_prec)
    sin_poly = u.mul(sin_acc, work_prec)
    cos_poly = cos_acc

    c_ctx = _ceil_ctx(work_prec)
    u_max_iv = Interval(_ZERO, u_abs_max)
    rem_sin = c_ctx.divide(
        u_max_iv.pow_int(2 * n_terms + 1, work_prec).hi,
        _factorial_dec(2 * n_terms + 1),
    )
    rem_cos = c_ctx.divide(
        u_max_iv.pow_int(2 * n_terms, work_prec).hi,
        _factorial_dec(2 * n_terms),
    )
    sin_iv = sin_poly.add(Interval(rem_sin.copy_negate(), rem_sin), work_prec).clamp(_NEG_ONE, _ONE)
    cos_iv = cos_poly.add(Interval(rem_cos.copy_negate(), rem_cos), work_prec).clamp(_NEG_ONE, _ONE)
    return (
        Interval(_dec_floor(sin_iv.lo, prec), _dec_ceil(sin_iv.hi, prec)).clamp(_NEG_ONE, _ONE),
        Interval(_dec_floor(cos_iv.lo, prec), _dec_ceil(cos_iv.hi, prec)).clamp(_NEG_ONE, _ONE),
    )


def _sin_cos_point(x: Decimal, prec: int) -> tuple[Interval, Interval]:
    """Certified (sin(x), cos(x)) for a single exact Decimal x."""
    work_prec = prec + 6
    hp = half_pi_interval(work_prec)
    hp_mid = hp.midpoint(work_prec)
    q_approx = _floor_ctx(work_prec).divide(x, hp_mid)
    k = int(q_approx.to_integral_value())
    u = Interval(x, x).sub(Interval.exact(k).mul(hp, work_prec), work_prec)
    thresh_hi = Decimal("0.85")
    thresh_lo = Decimal("-0.85")
    while u.lo > thresh_hi:
        k += 1
        u = Interval(x, x).sub(Interval.exact(k).mul(hp, work_prec), work_prec)
    while u.hi < thresh_lo:
        k -= 1
        u = Interval(x, x).sub(Interval.exact(k).mul(hp, work_prec), work_prec)
    if max(u.lo.copy_abs(), u.hi.copy_abs()) > _ONE:
        return Interval(_NEG_ONE, _ONE), Interval(_NEG_ONE, _ONE)

    s_u, c_u = _sin_cos_reduced(u, work_prec)
    quad = k % 4
    if quad == 0:
        s_res, c_res = s_u, c_u
    elif quad == 1:
        s_res, c_res = c_u, s_u.neg()
    elif quad == 2:
        s_res, c_res = s_u.neg(), c_u.neg()
    else:
        s_res, c_res = c_u.neg(), s_u
    return (
        Interval(_dec_floor(s_res.lo, prec), _dec_ceil(s_res.hi, prec)).clamp(_NEG_ONE, _ONE),
        Interval(_dec_floor(c_res.lo, prec), _dec_ceil(c_res.hi, prec)).clamp(_NEG_ONE, _ONE),
    )


def _contains_congruent_int(q_lo: Decimal, q_hi: Decimal, residue: int, prec: int) -> bool:
    """Return True if there exists integer m such that 4*m + residue lies in [q_lo, q_hi]."""
    res_d = Decimal(residue)
    f = _floor_ctx(prec)
    c = _ceil_ctx(prec)
    # m_min = ceil((q_lo - residue) / 4), m_max = floor((q_hi - residue) / 4)
    # Use conservative outward bounds: floor(q_lo - res)/4 rounded down for m_min?
    # To NEVER miss a critical point, widen [q_lo, q_hi] outward:
    # lower bound on (q_lo - res)/4 rounded DOWN -> ceil could be slightly too small (safe: more likely True)
    # upper bound on (q_hi - res)/4 rounded UP -> floor could be slightly too large (safe: more likely True)
    lo_scaled = f.divide(f.subtract(q_lo, res_d), _FOUR)
    hi_scaled = c.divide(c.subtract(q_hi, res_d), _FOUR)
    m_min = int(c.to_integral_value(lo_scaled))
    m_max = int(f.to_integral_value(hi_scaled))
    return m_min <= m_max


def sin_interval(x: Interval, prec: int = DEFAULT_PREC) -> Interval:
    """Sharp certified enclosure of sin(X) over any closed interval X."""
    if x.lo == x.hi:
        return _sin_cos_point(x.lo, prec)[0]
    s_lo, _ = _sin_cos_point(x.lo, prec)
    s_hi, _ = _sin_cos_point(x.hi, prec)
    lo = min(s_lo.lo, s_hi.lo)
    hi = max(s_lo.hi, s_hi.hi)
    q_prec = prec + 6
    q = x.div(half_pi_interval(q_prec), q_prec)
    if _contains_congruent_int(q.lo, q.hi, 1, q_prec):
        hi = _ONE
    if _contains_congruent_int(q.lo, q.hi, 3, q_prec):
        lo = _NEG_ONE
    return Interval(lo, hi).clamp(_NEG_ONE, _ONE)


def cos_interval(x: Interval, prec: int = DEFAULT_PREC) -> Interval:
    """Sharp certified enclosure of cos(X) over any closed interval X."""
    if x.lo == x.hi:
        return _sin_cos_point(x.lo, prec)[1]
    _, c_lo = _sin_cos_point(x.lo, prec)
    _, c_hi = _sin_cos_point(x.hi, prec)
    lo = min(c_lo.lo, c_hi.lo)
    hi = max(c_lo.hi, c_hi.hi)
    q_prec = prec + 6
    q = x.div(half_pi_interval(q_prec), q_prec)
    if _contains_congruent_int(q.lo, q.hi, 0, q_prec):
        hi = _ONE
    if _contains_congruent_int(q.lo, q.hi, 2, q_prec):
        lo = _NEG_ONE
    return Interval(lo, hi).clamp(_NEG_ONE, _ONE)


def _atan_small_point(t: Decimal, prec: int) -> Interval:
    """Certified enclosure of arctan(t) for |t| <= 0.5 via alternating Maclaurin series."""
    work_prec = prec + 10
    abs_t = t.copy_abs()
    if abs_t > Decimal("0.5"):
        raise ValueError(f"Expected |t| <= 0.5, got {t}")
    t_iv = Interval(t, t)
    t2 = t_iv.sqr(work_prec)
    cutoff = Decimal(1).scaleb(-(prec + 6))
    k = 0
    total = Interval.exact(0)
    t_pow = t_iv
    abs_t_pow = abs_t
    c_ctx = _ceil_ctx(work_prec)
    abs_t2 = c_ctx.multiply(abs_t, abs_t)
    while True:
        rem_bound = c_ctx.divide(abs_t_pow, Decimal(2 * k + 1))
        if rem_bound < cutoff:
            total = total.add(Interval(rem_bound.copy_negate(), rem_bound), work_prec)
            break
        term = t_pow.div(Interval.exact(2 * k + 1), work_prec)
        if k % 2 == 0:
            total = total.add(term, work_prec)
        else:
            total = total.sub(term, work_prec)
        t_pow = t_pow.mul(t2, work_prec)
        abs_t_pow = c_ctx.multiply(abs_t_pow, abs_t2)
        k += 1
    return Interval(_dec_floor(total.lo, prec), _dec_ceil(total.hi, prec))


def _atan_point(x: Decimal, prec: int) -> Interval:
    """Certified enclosure of arctan(x) for any exact Decimal x."""
    work_prec = prec + 10
    if x == _ZERO:
        return Interval.exact(0)
    if x < _ZERO:
        return _atan_point(x.copy_negate(), work_prec).neg()
    if x > _ONE:
        inv_x = Interval.exact(1).div(Interval(x, x), work_prec)
        sub_lo = _atan_point(inv_x.lo, work_prec)
        sub_hi = _atan_point(inv_x.hi, work_prec)
        sub = Interval.hull(sub_lo, sub_hi)
        res = half_pi_interval(work_prec).sub(sub, work_prec)
        return Interval(_dec_floor(res.lo, prec), _dec_ceil(res.hi, prec))
    if x > Decimal("0.5"):
        q_pi = pi_interval(work_prec).div(Interval.exact(4), work_prec)
        x_iv = Interval(x, x)
        u = x_iv.sub(Interval.exact(1), work_prec).div(
            x_iv.add(Interval.exact(1), work_prec), work_prec
        )
        a_lo = _atan_small_point(u.lo, work_prec)
        a_hi = _atan_small_point(u.hi, work_prec)
        res = q_pi.add(Interval.hull(a_lo, a_hi), work_prec)
        return Interval(_dec_floor(res.lo, prec), _dec_ceil(res.hi, prec))
    res = _atan_small_point(x, work_prec)
    return Interval(_dec_floor(res.lo, prec), _dec_ceil(res.hi, prec))


def atan_interval(x: Interval, prec: int = DEFAULT_PREC) -> Interval:
    """Certified enclosure of arctan(X) (monotonically increasing on R)."""
    a = _atan_point(x.lo, prec)
    b = _atan_point(x.hi, prec)
    return Interval(a.lo, b.hi)


def atan2_point_interval(y: Decimal, x: Decimal, prec: int = DEFAULT_PREC) -> Interval:
    """Certified enclosure of atan2(y, x) in [0, 2*pi) for exact Decimals (x, y) != (0, 0)."""
    work_prec = prec + 8
    if x == _ZERO and y == _ZERO:
        raise ValueError("atan2(0, 0) is undefined")
    pi_iv = pi_interval(work_prec)
    hp_iv = half_pi_interval(work_prec)
    tp_iv = two_pi_interval(work_prec)
    if x == _ZERO:
        res = hp_iv if y > _ZERO else Interval.exact(3).mul(hp_iv, work_prec)
    elif y == _ZERO:
        res = Interval.exact(0) if x > _ZERO else pi_iv
    elif x > _ZERO and y > _ZERO:
        ratio = Interval(y, y).div(Interval(x, x), work_prec)
        res = atan_interval(ratio, work_prec)
    elif x < _ZERO and y > _ZERO:
        nx = x.copy_negate()
        ratio = Interval(y, y).div(Interval(nx, nx), work_prec)
        res = pi_iv.sub(atan_interval(ratio, work_prec), work_prec)
    elif x < _ZERO and y < _ZERO:
        nx = x.copy_negate()
        ny = y.copy_negate()
        ratio = Interval(ny, ny).div(Interval(nx, nx), work_prec)
        res = pi_iv.add(atan_interval(ratio, work_prec), work_prec)
    else:  # x > 0, y < 0
        ny = y.copy_negate()
        ratio = Interval(ny, ny).div(Interval(x, x), work_prec)
        res = tp_iv.sub(atan_interval(ratio, work_prec), work_prec)
    return Interval(_dec_floor(res.lo, prec), _dec_ceil(res.hi, prec))


def interval_distance_sq(a: Interval, b: Interval, prec: int = DEFAULT_PREC) -> Decimal:
    """Certified lower bound on min_{u in a, v in b} (u - v)^2."""
    f = _floor_ctx(prec)
    if a.hi < b.lo:
        diff = f.subtract(b.lo, a.hi)
        return f.multiply(diff, diff)
    if b.hi < a.lo:
        diff = f.subtract(a.lo, b.hi)
        return f.multiply(diff, diff)
    return _ZERO


@lru_cache(maxsize=64)
def ln2_interval(prec: int = DEFAULT_PREC) -> Interval:
    """Certified enclosure of ln(2) = 2 * atanh(1/3) via positive series + geometric tail."""
    work_prec = prec + 10
    cutoff = Decimal(1).scaleb(-(prec + 6))
    total = Interval.exact(0)
    power = 3
    k = 0
    f_ctx = _floor_ctx(work_prec)
    c_ctx = _ceil_ctx(work_prec)
    nine = Decimal(9)
    while True:
        denom = Decimal((2 * k + 1) * power)
        term_lo = f_ctx.divide(_TWO, denom)
        term_hi = c_ctx.divide(_TWO, denom)
        # Exact tail bound: sum_{m>=0} 2 / ((2k+1) * 3^{2k+1} * 9^m) = (9/8) * 2 / denom = 9 / (4*denom)
        tail_hi = c_ctx.divide(nine, Decimal(4 * (2 * k + 1) * power))
        if tail_hi < cutoff:
            total = total.add(Interval(_ZERO, tail_hi), work_prec)
            break
        total = total.add(Interval(term_lo, term_hi), work_prec)
        power *= 9
        k += 1
    return Interval(_dec_floor(total.lo, prec), _dec_ceil(total.hi, prec))


def _log_point(x: Decimal, prec: int) -> Interval:
    """Certified enclosure of ln(x) for exact Decimal x > 0."""
    if x <= _ZERO:
        raise ValueError(f"log requires strictly positive input, got {x}")
    if x == _ONE:
        return Interval.exact(0)
    work_prec = prec + 10
    # Range-reduce x = 2^e * m with m in [0.7, 1.45] so |(m-1)/(m+1)| < 0.2.
    # Find integer e using exact bit/float estimate, then refine with Decimal comparisons.
    x_iv = Interval(x, x)
    # Estimate e = round(log2(x)) using float on scaled decimal if extreme
    adj = x.adjusted()
    # x = s * 10^adj with 1 <= s < 10; log2(10) ~ 3.321928
    e = int(round(adj * 3.321928094887362))
    two_pow = Interval.exact(2).pow_int(e, work_prec)
    m_iv = x_iv.div(two_pow, work_prec)
    lo_bound = Decimal("0.7")
    hi_bound = Decimal("1.45")
    while m_iv.hi > hi_bound:
        e += 1
        two_pow = Interval.exact(2).pow_int(e, work_prec)
        m_iv = x_iv.div(two_pow, work_prec)
    while m_iv.lo < lo_bound:
        e -= 1
        two_pow = Interval.exact(2).pow_int(e, work_prec)
        m_iv = x_iv.div(two_pow, work_prec)

    one_iv = Interval.exact(1)
    u = m_iv.sub(one_iv, work_prec).div(m_iv.add(one_iv, work_prec), work_prec)
    u2 = u.sqr(work_prec)
    u_abs_max = max(u.lo.copy_abs(), u.hi.copy_abs())
    c_ctx = _ceil_ctx(work_prec)
    f_ctx = _floor_ctx(work_prec)
    # 1 - u_abs_max^2 lower bound for geometric tail
    one_minus_u2_lo = f_ctx.subtract(_ONE, c_ctx.multiply(u_abs_max, u_abs_max))
    if one_minus_u2_lo <= _ZERO:
        raise ArithmeticError(f"Range reduction failed for log({x}): u={u}")

    cutoff = Decimal(1).scaleb(-(prec + 6))
    total = Interval.exact(0)
    u_pow = u
    abs_pow = u_abs_max
    abs_u2 = c_ctx.multiply(u_abs_max, u_abs_max)
    k = 0
    while True:
        denom = Decimal(2 * k + 1)
        rem_num = c_ctx.multiply(_TWO, abs_pow)
        rem_den = f_ctx.multiply(denom, one_minus_u2_lo)
        rem_hi = c_ctx.divide(rem_num, rem_den)
        if rem_hi < cutoff:
            total = total.add(Interval(rem_hi.copy_negate(), rem_hi), work_prec)
            break
        term = Interval.exact(2).mul(u_pow, work_prec).div(Interval.exact(denom), work_prec)
        total = total.add(term, work_prec)
        u_pow = u_pow.mul(u2, work_prec)
        abs_pow = c_ctx.multiply(abs_pow, abs_u2)
        k += 1

    if e != 0:
        total = total.add(Interval.exact(e).mul(ln2_interval(work_prec), work_prec), work_prec)
    return Interval(_dec_floor(total.lo, prec), _dec_ceil(total.hi, prec))


def log_interval(x: Interval, prec: int = DEFAULT_PREC) -> Interval:
    """Certified enclosure of ln(X) for strictly positive interval X > 0."""
    if x.lo <= _ZERO:
        raise ValueError(f"log_interval requires strictly positive interval, got {x}")
    if x.lo == x.hi:
        return _log_point(x.lo, prec)
    a = _log_point(x.lo, prec)
    b = _log_point(x.hi, prec)
    return Interval(a.lo, b.hi)


def _exp_point(x: Decimal, prec: int) -> Interval:
    """Certified enclosure of exp(x) for exact Decimal x."""
    if x == _ZERO:
        return Interval.exact(1)
    work_prec = prec + 10
    ln2 = ln2_interval(work_prec)
    ln2_mid = ln2.midpoint(work_prec)
    k = int(_floor_ctx(work_prec).divide(x, ln2_mid).to_integral_value())
    r = Interval(x, x).sub(Interval.exact(k).mul(ln2, work_prec), work_prec)
    half = Decimal("0.5")
    neg_half = Decimal("-0.5")
    while r.hi > half:
        k += 1
        r = Interval(x, x).sub(Interval.exact(k).mul(ln2, work_prec), work_prec)
    while r.lo < neg_half:
        k -= 1
        r = Interval(x, x).sub(Interval.exact(k).mul(ln2, work_prec), work_prec)

    r_abs_max = max(r.lo.copy_abs(), r.hi.copy_abs())
    cutoff = Decimal(1).scaleb(-(prec + 6))
    c_ctx = _ceil_ctx(work_prec)
    total = Interval.exact(1)
    r_pow = r
    abs_pow = r_abs_max
    j = 1
    while True:
        fact = _factorial_dec(j)
        # Since |r| <= 0.5 and j >= 1, sum_{m>=j} |r|^m/m! <= (|r|^j / j!) / (1 - 0.5/(j+1)) <= 2*|r|^j / j!
        rem_hi = c_ctx.divide(c_ctx.multiply(_TWO, abs_pow), fact)
        if rem_hi < cutoff:
            total = total.add(Interval(rem_hi.copy_negate(), rem_hi), work_prec)
            break
        total = total.add(r_pow.div(Interval.exact(fact), work_prec), work_prec)
        r_pow = r_pow.mul(r, work_prec)
        abs_pow = c_ctx.multiply(abs_pow, r_abs_max)
        j += 1

    if total.lo < _ZERO:
        total = Interval(_ZERO, total.hi)
    if k != 0:
        total = total.mul(Interval.exact(2).pow_int(k, work_prec), work_prec)
    return Interval(_dec_floor(total.lo, prec), _dec_ceil(total.hi, prec))


def exp_interval(x: Interval, prec: int = DEFAULT_PREC) -> Interval:
    """Certified enclosure of exp(X) for any closed interval X."""
    if x.lo == x.hi:
        return _exp_point(x.lo, prec)
    a = _exp_point(x.lo, prec)
    b = _exp_point(x.hi, prec)
    return Interval(a.lo, b.hi)
