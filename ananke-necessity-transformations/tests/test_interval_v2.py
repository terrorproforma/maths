from __future__ import annotations

import math
import unittest
from decimal import Decimal
from fractions import Fraction

from ananke.interval import (
    Interval,
    atan2_point_interval,
    atan_interval,
    cos_interval,
    pi_interval,
    sin_interval,
    two_pi_interval,
)


class IntervalArithmeticV2Tests(unittest.TestCase):
    def test_pi_enclosure_contains_reference_pi_and_is_tight(self) -> None:
        pi_ref = Decimal("3.1415926535897932384626433832795028841971693993751")
        two_pi_ref = Decimal("6.2831853071795864769252867665590057683943387987502")
        pi_iv = pi_interval(36)
        self.assertLessEqual(pi_iv.lo, pi_ref)
        self.assertGreaterEqual(pi_iv.hi, pi_ref)
        self.assertLess(pi_iv.width(40), Decimal("1e-33"))

        tp = two_pi_interval(36)
        self.assertLessEqual(tp.lo, two_pi_ref)
        self.assertGreaterEqual(tp.hi, two_pi_ref)

    def test_fraction_and_arithmetic_outward_rounding(self) -> None:
        third = Interval.from_fraction(Fraction(1, 3), prec=20)
        self.assertLess(third.lo, Decimal(1) / Decimal(3) + Decimal("1e-30"))
        self.assertLessEqual(third.lo * 3, Decimal(1))
        self.assertGreaterEqual(third.hi * 3, Decimal(1))

        # Product of signed intervals encloses all corner products
        a = Interval(Decimal("-2.5"), Decimal("1.5"))
        b = Interval(Decimal("-3.0"), Decimal("4.0"))
        prod = a.mul(b)
        self.assertLessEqual(prod.lo, Decimal("-10.0"))
        self.assertGreaterEqual(prod.hi, Decimal("7.5"))

        # Sqrt and integer power outward rounding (verify with high-prec multiplication)
        two = Interval.exact(2)
        s2 = two.sqrt(28)
        from decimal import localcontext
        with localcontext() as ctx:
            ctx.prec = 70
            self.assertLessEqual(s2.lo * s2.lo, Decimal(2))
            self.assertGreaterEqual(s2.hi * s2.hi, Decimal(2))

        p3 = Interval(Decimal("-2"), Decimal("3")).pow_int(3)
        self.assertEqual(p3.lo, Decimal("-8"))
        self.assertEqual(p3.hi, Decimal("27"))
        p2 = Interval(Decimal("-2"), Decimal("3")).pow_int(2)
        self.assertEqual(p2.lo, Decimal("0"))
        self.assertEqual(p2.hi, Decimal("9"))

    def test_sin_cos_point_and_critical_points(self) -> None:
        for angle in (-4.2, -1.5, -0.3, 0.0, 0.73, 1.57, 2.5, 5.1, 6.28):
            iv = Interval.from_float(angle)
            s = sin_interval(iv)
            c = cos_interval(iv)
            self.assertLessEqual(float(s.lo), math.sin(angle) + 1e-15)
            self.assertGreaterEqual(float(s.hi), math.sin(angle) - 1e-15)
            self.assertLessEqual(float(c.lo), math.cos(angle) + 1e-15)
            self.assertGreaterEqual(float(c.hi), math.cos(angle) - 1e-15)
            # Pythagorean identity sin^2 + cos^2 contains 1
            unit = s.sqr().add(c.sqr())
            self.assertLessEqual(unit.lo, Decimal(1))
            self.assertGreaterEqual(unit.hi, Decimal(1))

        # Wide interval straddling pi/2 must hit sin max = 1
        wide_sin = sin_interval(Interval(Decimal("1.0"), Decimal("2.2")))
        self.assertEqual(wide_sin.hi, Decimal(1))
        # Wide interval straddling pi must hit cos min = -1
        wide_cos = cos_interval(Interval(Decimal("2.5"), Decimal("3.8")))
        self.assertEqual(wide_cos.lo, Decimal(-1))
        # Full circle interval hits [-1, 1]
        full = Interval(Decimal(0), Decimal("6.3"))
        self.assertEqual(sin_interval(full).lo, Decimal(-1))
        self.assertEqual(sin_interval(full).hi, Decimal(1))
        self.assertEqual(cos_interval(full).lo, Decimal(-1))
        self.assertEqual(cos_interval(full).hi, Decimal(1))

    def test_atan_and_atan2_enclosures(self) -> None:
        # atan(1) == pi/4
        a1 = atan_interval(Interval.exact(1))
        q_pi = pi_interval().div(Interval.exact(4))
        self.assertLessEqual(a1.lo, q_pi.hi)
        self.assertGreaterEqual(a1.hi, q_pi.lo)

        for x, y in ((1.0, 0.0), (1.0, 1.0), (-1.0, 1.0), (-1.0, -1.0), (0.73, 0.68), (0.5, -0.8)):
            ang = atan2_point_interval(Decimal.from_float(y), Decimal.from_float(x))
            ref = math.atan2(y, x) % (2.0 * math.pi)
            self.assertLessEqual(float(ang.lo), ref + 1e-15)
            self.assertGreaterEqual(float(ang.hi), ref - 1e-15)


if __name__ == "__main__":
    unittest.main()
