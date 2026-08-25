#!/usr/bin/env python3
"""Symbolic and numerical checks for the Z_N-protected QCD chronometry model v0.6.

The script verifies:
1. the closed form of F(N);
2. the root-of-unity cancellation of harmonics below N;
3. the one-loop Coleman-Weinberg Nth-harmonic coefficient;
4. the 2/27 visible-QCD threshold coefficient;
5. the N=6 benchmark identities;
6. positivity of all vectorlike masses for 0 < epsilon < 1;
7. representative ultralight-mass benchmarks.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

OUT = Path('/mnt/data/zn_protected_qcd_chronometry_verification_v0_6.json')
MPL_GEV = 2.435e18
N_C = 3


def f_sum(n: int) -> float:
    return 2.0 ** (1 - n) * n * sum(
        math.comb(4, ell) * ((-1) ** ell) / (n - ell) for ell in range(5)
    )


def f_closed(n: int) -> float:
    return 24.0 * 2.0 ** (1 - n) / (
        (n - 1) * (n - 2) * (n - 3) * (n - 4)
    )


def cw_potential(x: np.ndarray, n: int, eps: float, m: float = 1.0, nc: int = N_C) -> np.ndarray:
    """One-loop fermion CW potential with mu=M; x=a/f."""
    result = np.zeros_like(x, dtype=float)
    for k in range(n):
        mk = m * (1.0 - eps * np.cos(x + 2.0 * np.pi * k / n))
        result += -(nc / (16.0 * np.pi**2)) * mk**4 * (
            np.log(mk**2 / m**2) - 1.5
        )
    return result


def nth_cosine_coefficient(values: np.ndarray, x: np.ndarray, n: int) -> float:
    """Numerical Fourier cosine coefficient on [0, 2pi]."""
    return float(np.trapezoid(values * np.cos(n * x), x) / np.pi)


def predicted_cw_amplitude(n: int, eps: float, m: float = 1.0, nc: int = N_C) -> float:
    return nc * m**4 * eps**n * f_closed(n) / (8.0 * np.pi**2)


def scalar_mass_ev(n: int, eps: float, m_gev: float, f_gev: float, nc: int = N_C) -> float:
    mass_sq_gev2 = (
        nc * m_gev**4 * n**2 * eps**n * f_closed(n) / (8.0 * np.pi**2 * f_gev**2)
    )
    return math.sqrt(abs(mass_sq_gev2)) * 1.0e9


def main() -> None:
    results: dict[str, Any] = {}

    # 1. Symbolic F(N) identity.
    n_sym = sp.symbols('N', integer=True, positive=True)
    finite_sum = sum(
        sp.binomial(4, ell) * (-1) ** ell / (n_sym - ell) for ell in range(5)
    )
    f_symbolic = sp.factor(2 ** (1 - n_sym) * n_sym * finite_sum)
    f_expected = sp.factor(
        24 * 2 ** (1 - n_sym) /
        ((n_sym - 1) * (n_sym - 2) * (n_sym - 3) * (n_sym - 4))
    )
    results['F_identity'] = {
        'symbolic': str(f_symbolic),
        'expected': str(f_expected),
        'pass': bool(sp.simplify(f_symbolic - f_expected) == 0),
    }

    # 2. Root-of-unity cancellations for m<N.
    root_tests = []
    for n in range(5, 15):
        xs = np.linspace(0.0, 2.0 * np.pi, 401)
        for power in range(1, n):
            vals = np.array([
                sum(np.cos(x + 2.0 * np.pi * k / n) ** power for k in range(n))
                for x in xs
            ])
            variation = float(np.max(vals) - np.min(vals))
            root_tests.append({'N': n, 'power': power, 'variation': variation})
    max_variation = max(item['variation'] for item in root_tests)
    results['root_of_unity'] = {
        'max_variation_for_m_less_than_N': max_variation,
        'pass': bool(max_variation < 2.0e-11),
    }

    # 3. Direct CW Fourier check.  Use small epsilon so the O(eps^(N+1)) remainder is controlled.
    cw_tests = []
    x_grid = np.linspace(0.0, 2.0 * np.pi, 200_001)
    for n, eps in [(5, 0.02), (6, 0.03), (8, 0.08), (10, 0.12)]:
        values = cw_potential(x_grid, n=n, eps=eps)
        numerical = nth_cosine_coefficient(values, x_grid, n)
        predicted = predicted_cw_amplitude(n=n, eps=eps)
        relative_error = abs(numerical - predicted) / abs(predicted)
        cw_tests.append({
            'N': n,
            'epsilon': eps,
            'numerical_cosine_amplitude': numerical,
            'leading_prediction': predicted,
            'relative_error': relative_error,
        })
    # Errors are O(epsilon); the chosen eps values keep them modest.
    results['coleman_weinberg_fourier'] = {
        'tests': cw_tests,
        'max_relative_error': max(t['relative_error'] for t in cw_tests),
        'pass': bool(max(t['relative_error'] for t in cw_tests) < 0.20),
    }

    # 4. QCD threshold telescoping coefficient.
    qcd_coeff = (1.0 - 19.0 / 21.0) * (21.0 / 23.0) * (23.0 / 25.0) * (25.0 / 27.0)
    results['qcd_threshold'] = {
        'computed': qcd_coeff,
        'expected': 2.0 / 27.0,
        'pass': bool(abs(qcd_coeff - 2.0 / 27.0) < 1.0e-15),
    }

    # 5. Minimal N=6 identities at x0=pi/2.
    x0 = np.pi / 2.0
    eps_symbol = sp.symbols('epsilon', positive=True)
    x_symbol = sp.symbols('x', real=True)
    kappa = sp.diff(sp.log(1 - eps_symbol * sp.cos(x_symbol)), x_symbol)
    kappa_x0 = sp.simplify(kappa.subs(x_symbol, sp.pi / 2))
    n6_mass_coefficient = sp.simplify(
        N_C * 6**2 * sp.Rational(1, 160) / (8 * sp.pi**2)
    )
    results['N6_benchmark'] = {
        'F6': f_closed(6),
        'kappa0_at_pi_over_2': str(kappa_x0),
        'mass_squared_coefficient': str(n6_mass_coefficient),
        'expected_mass_squared_coefficient': '27/(320*pi**2)',
        'pass': bool(
            abs(f_closed(6) - 1.0 / 160.0) < 1.0e-15
            and sp.simplify(kappa_x0 - eps_symbol) == 0
            and sp.simplify(n6_mass_coefficient - sp.Rational(27, 320) / sp.pi**2) == 0
        ),
    }

    # 6. Random positivity of masses for epsilon<1.
    rng = np.random.default_rng(20260816)
    minimum_ratio = float('inf')
    for _ in range(100_000):
        n = int(rng.integers(5, 41))
        eps = float(rng.uniform(1.0e-8, 0.999999))
        x = float(rng.uniform(-np.pi, np.pi))
        ratios = [1.0 - eps * math.cos(x + 2.0 * math.pi * k / n) for k in range(n)]
        minimum_ratio = min(minimum_ratio, min(ratios))
    results['mass_positivity_scan'] = {
        'points': 100_000,
        'minimum_Mk_over_M': minimum_ratio,
        'pass': bool(minimum_ratio > 0.0),
    }

    # 7. Benchmarks and protection law.
    benchmark_rows = []
    for eps in (1.0e-1, 1.0e-3, 1.0e-6):
        for n in (5, 6, 8, 10, 12, 20, 24):
            mass_ev = scalar_mass_ev(n=n, eps=eps, m_gev=1.0e4, f_gev=MPL_GEV)
            dg_max = (2.0 / 27.0) * eps  # f_a=M_P and x0=pi/2.
            benchmark_rows.append({
                'N': n,
                'epsilon': eps,
                'M_GeV': 1.0e4,
                'f_GeV': MPL_GEV,
                'mass_eV': mass_ev,
                'd_g_at_maximal_slope': dg_max,
            })
    results['benchmarks'] = benchmark_rows

    # 8. Compare N=6 protected mass with the naive one-loop order-epsilon^2 estimate.
    # m_naive^2 = N_c M^4 epsilon^2/(4 pi^2 f^2) under the v0.5 normalization.
    ratio = sp.simplify(
        (sp.Rational(27, 320) / sp.pi**2 * eps_symbol**6)
        / (sp.Rational(3, 4) / sp.pi**2 * eps_symbol**2)
    )
    results['N6_suppression_relative_to_naive'] = {
        'ratio': str(ratio),
        'expected': '9*epsilon**4/80',
        'pass': bool(sp.simplify(ratio - sp.Rational(9, 80) * eps_symbol**4) == 0),
    }

    results['overall_pass'] = all(
        value.get('pass', True) if isinstance(value, dict) else True
        for value in results.values()
    )

    OUT.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
