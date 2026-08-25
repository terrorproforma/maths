#!/usr/bin/env python3
"""Symbolic and numerical checks for the crossed-null chronometry audit v0.2.

The script verifies:
  1. reduction of the crossed-null metric to the standard mimetic conformal map;
  2. factorisation of the repaired EFT principal polynomial;
  3. positivity conditions for the quadratic Hamiltonian;
  4. exact dispersion relation of the heavy-mediator completion;
  5. low-energy expansion and dimensionless speed/dispersion sum rules;
  6. random numerical stability scans inside and outside the proposed domain.

Run:
    python verify_crossed_null_audit_v0_2.py

Outputs are written beside this script:
    verification_results_v0_2.json
    phase_speed_anisotropy_v0_2.pdf
    mediator_dispersion_v0_2.pdf
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


OUT_DIR = Path(__file__).resolve().parent


def sympy_zero(expr: sp.Expr) -> bool:
    """Return True if SymPy can reduce an expression exactly to zero."""
    return sp.simplify(sp.factor(expr)) == 0


def verify_mimetic_reduction() -> dict[str, str]:
    """Verify C=-T^2=R^2 and T.R=0 from two null constraints."""
    T2, R2, TR = sp.symbols("T2 R2 TR", real=True)
    p2 = T2 + R2 + 2 * TR
    q2 = T2 + R2 - 2 * TR

    # Solve the two null constraints p^2=q^2=0 for R^2 and T.R.
    solutions = sp.solve([sp.Eq(p2, 0), sp.Eq(q2, 0)], [R2, TR], dict=True)
    assert solutions == [{R2: -T2, TR: 0}]

    pdotq = T2 - R2
    C = -sp.Rational(1, 2) * pdotq
    C_reduced = sp.simplify(C.subs(solutions[0]))
    assert sympy_zero(C_reduced + T2)
    assert sympy_zero(C_reduced - (-T2))

    return {
        "null_constraints": "p^2=q^2=0 imply T.R=0 and R^2=-T^2",
        "cross_invariant": "C=-1/2 p.q=-T^2=R^2",
        "metric_map": "h_ab=C g_ab=-(g^{cd} T_c T_d) g_ab (standard mimetic map)",
    }


def verify_repaired_eft() -> dict[str, Any]:
    """Verify the repaired EFT determinant and Hamiltonian positivity criterion."""
    F, a = sp.symbols("F a", positive=True, finite=True)
    omega, kx, kp = sp.symbols("omega kx kp", real=True)
    k2 = kx**2 + kp**2

    # Fourier-space matrix for (s,r).
    matrix = sp.Matrix(
        [
            [F * k2 - (F + a) * omega**2, -a * omega * kx],
            [-a * omega * kx, -F * omega**2 + (F - a) * kx**2 + F * kp**2],
        ]
    )
    determinant = sp.factor(matrix.det())
    expected = F * (omega**2 - k2) * ((F + a) * omega**2 - F * k2 + a * kx**2)
    assert sympy_zero(determinant - expected)

    # Hamiltonian block for P_s and d_x r, after removing an overall 1/2.
    hessian = sp.Matrix(
        [
            [1 / (F + a), a / (F + a)],
            [a / (F + a), F**2 / (F + a)],
        ]
    )
    det_hessian = sp.factor(hessian.det())
    assert sympy_zero(det_hessian - (F - a) / (F + a))

    epsilon, theta = sp.symbols("epsilon theta", positive=True, real=True)
    c2 = sp.simplify((1 - epsilon * sp.cos(theta) ** 2) / (1 + epsilon))
    c_parallel = sp.simplify(c2.subs(theta, 0))
    c_perp = sp.simplify(c2.subs(theta, sp.pi / 2))
    sum_rule = sp.simplify(c_parallel - (2 * c_perp - 1))
    assert sympy_zero(sum_rule)

    return {
        "determinant": str(determinant),
        "branches": [
            "omega_1^2=k^2",
            "omega_2^2=(F k^2-a k_x^2)/(F+a)",
        ],
        "hamiltonian_block_determinant": str(det_hessian),
        "healthy_domain": "F>0 and 0<a<F, equivalently 0<epsilon=a/F<1",
        "speed_sum_rule": "c_parallel^2=2 c_perp^2-1",
    }


def verify_mediator_completion() -> dict[str, Any]:
    """Verify exact mediator dispersion and its low-momentum expansion."""
    F, lam, M2 = sp.symbols("F lam M2", positive=True, finite=True)
    omega, kx, kp = sp.symbols("omega kx kp", real=True)
    k2 = kx**2 + kp**2
    B = M2 + k2 - omega**2
    A = F * (k2 - omega**2)

    matrix = sp.Matrix(
        [
            [A, 0, -sp.I * lam * omega],
            [0, A, -sp.I * lam * kx],
            [sp.I * lam * omega, sp.I * lam * kx, B],
        ]
    )
    determinant = sp.factor(matrix.det())
    expected = -A * (-A * B + lam**2 * (omega**2 + kx**2))
    assert sympy_zero(determinant - expected)

    # Solve the non-luminal quadratic in x=omega^2.
    x, mu2 = sp.symbols("x mu2", real=True)
    polynomial = sp.expand((k2 - x) * (M2 + k2 - x) - mu2 * (x + kx**2))
    roots = sp.solve(sp.Eq(polynomial, 0), x)
    assert len(roots) == 2

    # Verify the closed form used in the paper.
    radical = sp.sqrt((M2 + mu2) ** 2 + 4 * mu2 * (k2 + kx**2))
    root_minus = (M2 + mu2 + 2 * k2 - radical) / 2
    root_plus = (M2 + mu2 + 2 * k2 + radical) / 2
    assert any(sympy_zero(root - root_minus) for root in roots)
    assert any(sympy_zero(root - root_plus) for root in roots)

    # Low-k expansion: introduce a bookkeeping parameter z with k_i -> z k_i.
    z, epsilon, M = sp.symbols("z epsilon M", positive=True, finite=True)
    substituted = root_minus.subs(
        {
            M2: M**2,
            mu2: epsilon * M**2,
            kx: z * kx,
            kp: z * kp,
        }
    )
    series = sp.series(substituted, z, 0, 6).removeO().expand()
    expected_series = (
        z**2 * (k2 - epsilon * kx**2) / (1 + epsilon)
        + z**4
        * epsilon**2
        * (k2 + kx**2) ** 2
        / (M**2 * (1 + epsilon) ** 3)
    )
    assert sympy_zero(series - expected_series)

    # Dimensionless k^4 consistency relation using Omega_H^2=M^2(1+epsilon).
    theta = sp.symbols("theta", real=True)
    alpha_theta = (
        epsilon**2
        * (1 + sp.cos(theta) ** 2) ** 2
        / (M**2 * (1 + epsilon) ** 3)
    )
    omega_h2 = M**2 * (1 + epsilon)
    c_perp2 = 1 / (1 + epsilon)
    prediction = sp.simplify(
        omega_h2 * alpha_theta
        - (1 - c_perp2) ** 2 * (1 + sp.cos(theta) ** 2) ** 2
    )
    assert sympy_zero(prediction)

    return {
        "determinant": str(determinant),
        "nonluminal_roots": [str(root_minus), str(root_plus)],
        "heavy_gap_at_zero_momentum": "Omega_H^2=M^2+lambda^2/F=M^2(1+epsilon)",
        "positive_hamiltonian_domain": "F>0, M^2>0, lambda^2<F M^2",
        "low_energy_series": str(expected_series.subs(z, 1)),
        "dimensionless_dispersion_rule": (
            "Omega_H^2 alpha(theta)=(1-c_perp^2)^2(1+cos^2(theta))^2"
        ),
    }


def numerical_scan(seed: int = 732451, samples: int = 20_000) -> dict[str, Any]:
    """Randomly test the exact roots in the healthy and unhealthy parameter domains."""
    rng = np.random.default_rng(seed)

    healthy_min_omega2 = math.inf
    healthy_violations = 0
    for _ in range(samples):
        F = 10 ** rng.uniform(-2, 2)
        M2 = 10 ** rng.uniform(-2, 2)
        epsilon = rng.uniform(1e-5, 0.999)
        mu2 = epsilon * M2
        k = 10 ** rng.uniform(-4, 3)
        cos_theta = rng.uniform(-1.0, 1.0)
        kx2 = k * k * cos_theta * cos_theta
        k2 = k * k
        radical = math.sqrt((M2 + mu2) ** 2 + 4 * mu2 * (k2 + kx2))
        roots = (
            0.5 * (M2 + mu2 + 2 * k2 - radical),
            0.5 * (M2 + mu2 + 2 * k2 + radical),
            k2,
        )
        healthy_min_omega2 = min(healthy_min_omega2, *roots)
        if min(roots) < -1e-10 * max(1.0, k2, M2):
            healthy_violations += 1

    # Outside the Hamiltonian domain, the light branch is tachyonic near k parallel
    # to the crossed-stream axis. Count explicit examples.
    unhealthy_tachyons = 0
    unhealthy_samples = 2_000
    for _ in range(unhealthy_samples):
        M2 = 10 ** rng.uniform(-2, 2)
        epsilon = rng.uniform(1.001, 4.0)
        mu2 = epsilon * M2
        k = 10 ** rng.uniform(-6, -2) * math.sqrt(M2)
        k2 = k * k
        kx2 = k2
        radical = math.sqrt((M2 + mu2) ** 2 + 4 * mu2 * (k2 + kx2))
        root_minus = 0.5 * (M2 + mu2 + 2 * k2 - radical)
        if root_minus < 0:
            unhealthy_tachyons += 1

    assert healthy_violations == 0
    assert unhealthy_tachyons > int(0.99 * unhealthy_samples)

    return {
        "seed": seed,
        "healthy_samples": samples,
        "healthy_negative_root_violations": healthy_violations,
        "smallest_healthy_omega_squared_seen": healthy_min_omega2,
        "unhealthy_samples": unhealthy_samples,
        "unhealthy_parallel_tachyons": unhealthy_tachyons,
    }


def make_speed_plot() -> str:
    """Plot the low-energy phase speed as a function of propagation angle."""
    theta = np.linspace(0.0, 0.5 * np.pi, 500)
    for epsilon in (0.1, 0.4, 0.8):
        c2 = (1.0 - epsilon * np.cos(theta) ** 2) / (1.0 + epsilon)
        plt.plot(np.degrees(theta), np.sqrt(c2), label=rf"$\epsilon={epsilon}$")
    plt.xlabel(r"Angle to crossed-null axis $\theta$ (degrees)")
    plt.ylabel(r"Light-branch phase speed $c_2(\theta)$")
    plt.title("Stable anisotropic mode in the repaired EFT")
    plt.ylim(0.0, 1.02)
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    output = OUT_DIR / "phase_speed_anisotropy_v0_2.pdf"
    plt.savefig(output)
    plt.close()
    return output.name


def make_dispersion_plot() -> str:
    """Plot exact mediator branches for propagation parallel to the null-pair axis."""
    M = 1.0
    epsilon = 0.4
    mu2 = epsilon * M**2
    k = np.linspace(0.0, 4.0, 600)
    k2 = k**2
    kx2 = k2
    radical = np.sqrt((M**2 + mu2) ** 2 + 4.0 * mu2 * (k2 + kx2))
    omega_minus2 = 0.5 * (M**2 + mu2 + 2.0 * k2 - radical)
    omega_plus2 = 0.5 * (M**2 + mu2 + 2.0 * k2 + radical)
    plt.plot(k, np.sqrt(np.maximum(omega_minus2, 0.0)), label=r"light mixed branch $\omega_-$")
    plt.plot(k, k, label=r"exact luminal branch $\omega=k$")
    plt.plot(k, np.sqrt(omega_plus2), label=r"heavy mixed branch $\omega_+$")
    plt.xlabel(r"Wave number $k/M$")
    plt.ylabel(r"Frequency $\omega/M$")
    plt.title(r"Exact mediator dispersion ($\epsilon=0.4$, parallel propagation)")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    output = OUT_DIR / "mediator_dispersion_v0_2.pdf"
    plt.savefig(output)
    plt.close()
    return output.name


def main() -> None:
    results: dict[str, Any] = {
        "mimetic_reduction": verify_mimetic_reduction(),
        "repaired_eft": verify_repaired_eft(),
        "mediator_completion": verify_mediator_completion(),
        "numerical_scan": numerical_scan(),
    }
    results["plots"] = [make_speed_plot(), make_dispersion_plot()]

    output = OUT_DIR / "verification_results_v0_2.json"
    output.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    print(f"\nWrote {output}")


if __name__ == "__main__":
    main()
