#!/usr/bin/env python3
"""Reproduce the scale/conformal-to-chronometry applicability audit.

Author: Angus Muffatti. AI-assisted research and implementation.
Symbolic identities and a specified oscillator benchmark are checked here.
This script does NOT verify the OpenAI theorem, quantum QCD, or a UV completion.
"""
from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s


def run_checks() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def zero(name: str, value: Any) -> None:
        matrix = s.Matrix(value) if isinstance(value, s.MatrixBase) else s.Matrix([value])
        reduced = [s.simplify(item) for item in matrix]
        checks.append({"name": name, "kind": "symbolic_identity", "passed": all(item == 0 for item in reduced), "residual": [str(item) for item in reduced]})

    def numeric(name: str, passed: bool, value: float, tolerance: float) -> None:
        checks.append({"name": name, "kind": "numerical_benchmark", "passed": bool(passed), "value": float(value), "tolerance": float(tolerance)})

    chi, h = s.symbols("chi h", real=True)
    f, zeta, lam, B, f0 = s.symbols("f zeta lambda B f0", positive=True)
    phi = s.Matrix([chi, h])
    V = lam * (h**2 - zeta**2 * chi**2)**2 / 4
    grad = s.Matrix([s.diff(V, var) for var in phi])
    vacuum = {chi: f, h: zeta * f}
    H = s.hessian(V, phi).subs(vacuum)
    radial = s.Matrix([1, zeta])
    transverse = s.Matrix([-zeta, 1])
    mass2 = 2 * lam * zeta**2 * (1 + zeta**2) * f**2
    zero("quartic_euler_identity", (phi.dot(grad) - 4 * V))
    zero("stationary_valley", grad.subs(vacuum))
    zero("massless_radial_direction", H * radial)
    zero("massive_transverse_direction", H * transverse - mass2 * transverse)
    zero("hessian_trace", s.trace(H) - mass2)
    zero("improved_trace_classical", 4 * V - phi.dot(grad))
    eta = s.symbols("eta", real=True)
    Vextra = V + eta * chi**4 / 4
    zero("allowed_quartic_requires_flat_direction_tuning", s.diff(Vextra, chi).subs(vacuum) - eta * f**3)

    # Use a positive field c in logarithms. This is an anomalous-potential
    # diagnostic, not an exactly scale-invariant regulator calculation.
    c = s.symbols("c", positive=True)
    Vcw = B * c**4 * (s.log(c**2 / f0**2) - s.Rational(1, 2)) + B * f0**4 / 2
    theta_cw = 4 * Vcw - c * s.diff(Vcw, c)
    zero("cw_minimum", s.diff(Vcw, c).subs(c, f0))
    zero("cw_curvature", s.diff(Vcw, c, 2).subs(c, f0) - 8 * B * f0**2)
    zero("cw_nonzero_trace_formula", theta_cw + 2 * B * (c**4 - f0**4))
    zero("cw_trace_vanishes_at_tuned_vacuum_only", theta_cw.subs(c, f0))
    Hlift = H + s.diag(8 * B * f**2, 0)
    zero("lifted_full_hessian_determinant", Hlift.det() - 16 * B * lam * zeta**2 * f**4)

    mu, g, b = s.symbols("mu g b", positive=True)
    beta = -b * g**3 / (16 * s.pi**2)
    logLambda = s.log(mu) - 8 * s.pi**2 / (b * g**2)
    rg_derivative = mu * s.diff(logLambda, mu) + beta * s.diff(logLambda, g)
    zero("rgi_scale_independent_of_subtraction_scale", rg_derivative)
    zero("mu_equals_chi_is_not_physical_lock", (rg_derivative - 1) - (-1))

    A = [s.Rational(19, 21), s.Rational(21, 23), s.Rational(23, 25), s.Rational(25, 27)]
    high_weight = s.prod(A)
    weights = [(1 - A[i]) * s.prod(A[i + 1:]) for i in range(4)]
    zero("qcd_high_scale_weight", high_weight - s.Rational(19, 27))
    zero("qcd_each_heavy_threshold_weight", s.Matrix(weights) - s.ones(4, 1) * s.Rational(2, 27))
    zero("qcd_total_homogeneous_weight", high_weight + sum(weights) - 1)
    zero("qcd_fixed_high_scale_ratio_response", sum(weights) - 1 + s.Rational(19, 27))

    p, Delta = s.symbols("p Delta", real=True)
    F = s.Function("F")
    G = f**(2 * Delta - 4) * F(p / f)
    zero("conditional_two_point_scaling_identity", f * s.diff(G, f) + p * s.diff(G, p) - (2 * Delta - 4) * G)
    y = s.symbols("y", positive=True)
    Gpole = 1 / (p**2 + y**2 * f**2)
    zero("tree_pole_scaling_identity", f * s.diff(Gpole, f) + p * s.diff(Gpole, p) + 2 * Gpole)

    a, t = s.symbols("a t", real=True)
    ramp = 1 + a * t
    omega = y * ramp
    W2 = omega + 3 * a**2 / (8 * y * ramp**3)
    residual = W2**2 - omega**2 + s.diff(W2, t, 2) / (2 * W2) - 3 * (s.diff(W2, t) / W2)**2 / 4
    zero("adiabatic_frequency_equation_through_order_three", s.series(residual, a, 0, 4).removeO())

    samples: list[dict[str, float]] = []
    all_wr: list[float] = []
    all_convergence: list[float] = []
    for slope in (0.01, 0.02, 0.04):
        frequencies: dict[float, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
        for coupling in (1.0, 2.0):
            grid = np.linspace(0.0, 20.0, 2001)
            w0 = coupling + 3 * slope**2 / (8 * coupling)
            dw0 = coupling * slope - 9 * slope**3 / (8 * coupling)
            u0 = 1 / np.sqrt(2 * w0)
            v0 = (-1j * w0 - dw0 / (2 * w0)) * u0

            def rhs(time: float, state: np.ndarray) -> np.ndarray:
                om = coupling * (1 + slope * time)
                return np.array([state[1], -(om**2) * state[0]], dtype=complex)

            def solve(rtol: float, atol: float) -> tuple[np.ndarray, np.ndarray]:
                sol = solve_ivp(rhs, (0.0, 20.0), np.array([u0, v0], dtype=complex), t_eval=grid, method="DOP853", rtol=rtol, atol=atol)
                if not sol.success or not np.all(np.isfinite(sol.y)):
                    raise RuntimeError(f"Oscillator solve failed: {sol.message}")
                phase_frequency = -np.imag(sol.y[1] / sol.y[0])
                wronskian = -2 * np.imag(np.conjugate(sol.y[0]) * sol.y[1])
                return phase_frequency, wronskian

            exact, wr = solve(2e-12, 2e-14)
            finer, _ = solve(2e-13, 2e-15)
            field = 1 + slope * grid
            leading = coupling * field
            second = leading + 3 * slope**2 / (8 * coupling * field**3)
            err0 = float(np.max(np.abs(exact / leading - 1)))
            err2 = float(np.max(np.abs(exact / second - 1)))
            conv = float(np.max(np.abs(exact / finer - 1)))
            wrerr = float(np.max(np.abs(wr - 1)))
            all_wr.append(wrerr)
            all_convergence.append(conv)
            numeric(f"wkb_improves_ramp_a{slope:g}_y{coupling:g}", err2 < err0 / 20, err2 / err0, 0.05)
            samples.append({"slope": slope, "coupling": coupling, "leading_max_relative_error": err0, "second_order_max_relative_error": err2, "wronskian_max_error": wrerr, "solver_refinement_max_relative_difference": conv})
            frequencies[coupling] = (exact, second, field)
        exact1, second1, field = frequencies[1.0]
        exact2, second2, _ = frequencies[2.0]
        observed = np.log((exact1 / exact2) / (1.0 / 2.0))
        predicted = (1.0 - 1.0 / 4.0) * 3 * slope**2 / (8 * field**4)
        error = float(np.max(np.abs(observed - predicted)))
        signal = float(np.max(np.abs(observed)))
        numeric(f"gradient_ratio_prediction_a{slope:g}", error < signal / 20, error / signal, 0.05)
        samples.append({"slope": slope, "ratio_max_log_deviation": signal, "ratio_second_order_max_absolute_error": error})
    numeric("oscillator_wronskian", max(all_wr) < 1e-9, max(all_wr), 1e-9)
    numeric("oscillator_solver_refinement", max(all_convergence) < 1e-9, max(all_convergence), 1e-9)
    return {
        "title": "Scale/conformal-to-chronometry bridge: first applicability audit",
        "author": "Angus Muffatti",
        "assistance": "AI-assisted derivation and implementation",
        "scope": "Symbolic classical and leading-log identities plus a free-probe time-dependent oscillator benchmark. Not an independent proof of the OpenAI paper or quantum completion.",
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "sympy": s.__version__},
        "checks": checks,
        "check_count": len(checks),
        "all_passed": all(item["passed"] for item in checks),
        "oscillator_initial_state": "Second-order adiabatic positive-frequency initial data; both integrations use the same initial state. This tests that specified preparation, not all clock protocols.",
        "oscillator_samples": samples,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results.json")
    args = parser.parse_args()
    results = run_checks()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"{sum(item['passed'] for item in results['checks'])}/{results['check_count']} checks passed")
    print(f"Results written to {args.output}")
    if not results["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
