#!/usr/bin/env python3
"""One-loop scalar-channel audit. Author: Angus Muffatti; AI assistance disclosed.

Run: python verify.py
Writes results.json beside this file. These are algebra/quadrature checks of the
specified one-loop model, not a proof of a complete quantum theory or a clock.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
import sympy as sp

LOOP = 16.0 * math.pi**2
CHECKS: list[dict] = []
PARAMS = dict(a=0.04, b=0.09, lambda_A=0.3, lambda_B=0.4, kappa=0.1, z=0.5)


def check(name: str, condition: bool, **details: object) -> None:
    CHECKS.append(dict(name=name, passed=bool(condition), **details))


def zero(name: str, expression: sp.Expr) -> None:
    residual = sp.simplify(expression)
    check(name, residual == 0, residual=str(residual), category="symbolic identity")


def log_kernel(r: float, log_mass: float) -> complex:
    """Integral of log[x*(1-(1-x)*r)-i0] plus log(m^2/mu^2)."""
    if abs(r) < 1e-5:
        return complex(log_mass - 1.0 - sum(r**n / (n * (n + 1)) for n in range(1, 8)))
    if r == 1.0:
        return complex(log_mass - 2.0)
    logarithm = complex(math.log(abs(1.0 - r)), -math.pi if r > 1.0 else 0.0)
    return log_mass - 2.0 - (1.0 - r) * logarithm / r


def kernel_quad(r: float, log_mass: float) -> complex:
    split = 1.0 - 1.0 / r if r > 1.0 else None
    points = [0.0, split, 1.0] if split is not None else [0.0, 1.0]
    real = log_mass
    for lo, hi in zip(points[:-1], points[1:]):
        real += quad(lambda x: math.log(x) + math.log(abs(1.0 - (1.0 - x) * r)),
                     lo, hi, epsabs=2e-12, epsrel=2e-12)[0]
    return complex(real, -math.pi * split if split is not None else 0.0)


def kernel_prime(r: float) -> float:
    if r >= 1.0:
        raise ValueError("Derivative used only below the massless threshold.")
    if abs(r) < 1e-5:
        return -sum(r**(n - 1) / (n + 1) for n in range(1, 8))
    return (r + math.log1p(-r)) / r**2


def sigma(s: float, f: float, a: float, b: float, lam: float,
          kappa: float, z: float, *, evanescent: bool = True) -> complex:
    if min(f, a, b, z) <= 0.0:
        raise ValueError("f, both mass couplings and z must be positive.")
    la, lb = math.log(a / z**2), math.log(b / z**2)
    tad = lam * a * (la - 1.0) / 2.0 + kappa * b * (lb - 1.0) / 2.0
    bubble = 4.0 * a**2 * log_kernel(s / (a * f**2), la)
    local = -8.0 * a**2 if evanescent else 0.0
    return f**2 * (tad + bubble + local) / LOOP


def source_insertions(s: float, f: float, a: float, b: float, lam: float,
                      kappa: float, z: float, *, omit_scale_vertices: bool = False) -> float:
    """f*d(m^2+Sigma)/df from differentiated loop integrands, below threshold.

    This is a zero-momentum background-source insertion. It is NOT an
    independently calculated finite-momentum three-point function.
    """
    m2, n2 = a * f**2, b * f**2
    if s >= m2:
        raise ValueError("Use strictly subthreshold external momentum.")
    la, lb = math.log(a / z**2), math.log(b / z**2)
    regulator = 0.0 if omit_scale_vertices else 2.0
    tad = lam * m2 * (2.0 * la - regulator) / 2.0
    tad += kappa * n2 * (2.0 * lb - regulator) / 2.0
    internal = quad(lambda x: 2.0 * m2 / (m2 - (1.0 - x) * s) - regulator,
                    0.0, 1.0, epsabs=1e-11, epsrel=1e-11)[0]
    bubble = 4.0 * a**2 * f**2 * (2.0 * kernel_quad(s / m2, la).real + internal)
    ev = -16.0 * a**2 * f**2
    return 2.0 * m2 + (tad + bubble + ev) / LOOP


def dlog(function, f: float, h: float = 1e-4) -> float:
    """Five-point derivative with respect to ln(f)."""
    return float((function(f * math.exp(-2 * h)) - 8 * function(f * math.exp(-h))
                  + 8 * function(f * math.exp(h)) - function(f * math.exp(2 * h))) / (12 * h))


def symbolic_checks() -> None:
    chi, A, B = sp.symbols("chi A B", positive=True)
    a, b, la, lb, k = sp.symbols("a b lambda_A lambda_B kappa", real=True)
    V = (a * chi**2 * A**2 + b * chi**2 * B**2) / 2
    V += la * A**4 / 24 + lb * B**4 / 24 + k * A**2 * B**2 / 4
    fields = [chi, A, B]
    H = sp.hessian(V, fields)
    ell = sp.log(chi)
    K = sp.Matrix(3, 3, lambda i, j:
                  sp.diff(ell, fields[i]) * sp.diff(V, fields[j])
                  + sp.diff(ell, fields[j]) * sp.diff(V, fields[i])
                  + sp.diff(ell, fields[i], fields[j]) * V)
    delta = sp.expand(-4 * sp.trace(H * K))
    alternative = -4 / chi**2 * (sp.diff(V, chi, 2) * (2 * chi * sp.diff(V, chi) - V)
                    + 2 * chi * sum(sp.diff(V, x) * sp.diff(V, x, chi) for x in [A, B]))
    zero("evanescent matrix trace versus field formula", delta - alternative)
    zero("classical Euler identity", sum(x * sp.diff(V, x) for x in fields) - 4 * V)
    zero("evanescent Euler identity", sum(x * sp.diff(delta, x) for x in fields) - 4 * delta)
    zero("evanescent A mass coefficient", sp.diff(delta, A, 2).subs({A: 0, B: 0}) / 4 + 8 * a**2 * chi**2)
    zero("evanescent B mass coefficient", sp.diff(delta, B, 2).subs({A: 0, B: 0}) / 4 + 8 * b**2 * chi**2)
    trace_h2 = sp.expand(sp.trace(H * H))
    zero("A UV pole from Hessian", trace_h2.coeff(A, 2).subs(B, 0) / chi**2 - (la * a + k * b + 8 * a**2))
    zero("B UV pole from Hessian", trace_h2.coeff(B, 2).subs(A, 0) / chi**2 - (lb * b + k * a + 8 * b**2))
    zero("vacuum UV pole", trace_h2.subs({A: 0, B: 0}) - (a**2 + b**2) * chi**4)
    zero("tree radial zero mode", H.subs({A: 0, B: 0})[0, 0])
    r = sp.symbols("r", positive=True)
    shape = -2 - (1 - r) * sp.log(1 - r) / r
    zero("bubble derivative", sp.diff(shape, r) - (r + sp.log(1 - r)) / r**2)
    zero("bubble zero-momentum limit", sp.limit(shape, r, 0) + 1)
    zero("bubble threshold value", sp.limit(shape, r, 1, dir="-") + 2)
    z = sp.symbols("z", positive=True)
    LA, LB = sp.log(a / z**2), sp.log(b / z**2)
    c = la * a * (LA - 1) / 2 + k * b * (LB - 1) / 2 + 4 * a**2 * (LA + shape) - 8 * a**2
    zero("one-loop subtraction-parameter RG check", z * sp.diff(c, z) + la * a + k * b + 8 * a**2)
    lchi = -6 * (a**2 * (LA - sp.Rational(3, 2)) + b**2 * (LB - sp.Rational(3, 2)))
    zero("flat-direction subtraction running", z * sp.diff(lchi, z) - 12 * (a**2 + b**2))
    zero("tuned vacuum potential", lchi / 24 + (a**2 * (LA - sp.Rational(3, 2)) + b**2 * (LB - sp.Rational(3, 2))) / 4)
    v, u, m2, q2 = sp.symbols("v u m2 q2", positive=True)
    x0, x1, x2 = 1 - v, v * u, v * (1 - u)
    D = (x1 + x2) * m2 - x0 * (x1 + x2) * m2 + x1 * x2 * q2
    zero("on-shell triangle soft factorization", D - v**2 * (m2 + u * (1 - u) * q2))
    zero("triangle gradient logarithm coefficient", sp.integrate(-u * (1 - u), (u, 0, 1)) + sp.Rational(1, 6))


def numerical_checks() -> dict:
    channels = [dict(name="A", a=PARAMS["a"], b=PARAMS["b"], lam=PARAMS["lambda_A"]),
                dict(name="B", a=PARAMS["b"], b=PARAMS["a"], lam=PARAMS["lambda_B"])]
    for r in [-3.0, -0.2, 0.0, 0.3, 0.9, 1.0, 1.4, 3.0]:
        error = abs(log_kernel(r, -0.7) - kernel_quad(r, -0.7))
        check(f"bubble quadrature r={r}", error < 3e-10, absolute_error=error, category="independent quadrature")
    for r in [-2.0, 0.0, 0.5, 0.99, 0.999999]:
        numeric = quad(lambda x: -(1 - x) / (1 - (1 - x) * r), 0, 1, epsabs=1e-10)[0]
        error = abs(numeric - kernel_prime(r))
        check(f"bubble derivative quadrature r={r}", error < 2e-8, absolute_error=error, category="independent quadrature")
    summaries = []
    for ch in channels:
        a, b, lam = ch["a"], ch["b"], ch["lam"]
        args = (a, b, lam, PARAMS["kappa"], PARAMS["z"])
        one = lambda f: sigma(a * f**2, f, *args).real
        mass = lambda f: math.sqrt(a) * f * (1.0 + one(f) / (2.0 * a * f**2))
        naive = lambda f: math.sqrt(a) * f * (1.0 + sigma(a * f**2, f, *args, evanescent=False).real / (2 * a * f**2))
        defects = [dlog(lambda t: math.log(mass(t)), f) - 1 for f in [0.2, 1.0, 5.0]]
        check(f"{ch['name']} homogeneous mass response", max(map(abs, defects)) < 3e-10,
              maximum_absolute_defect=max(map(abs, defects)), category="finite difference")
        check(f"{ch['name']} incomplete model also passes scale-only gate", abs(dlog(lambda t: math.log(naive(t)), 1) - 1) < 3e-10,
              category="negative control")
        source_errors, ward_errors, missing_errors = [], [], []
        beta = (lam * a + PARAMS["kappa"] * b + 8 * a**2) / LOOP
        for f in [0.5, 1.0, 3.0]:
            for r in [-2.0, -0.25, 0.5, 0.95]:
                s = r * a * f**2
                actual = source_insertions(s, f, *args)
                numeric = dlog(lambda t: a * t**2 + sigma(s, t, *args).real, f)
                source_errors.append(abs(actual - numeric) / (a * f**2))
                dsigma = 4 * a * kernel_prime(r) / LOOP
                expected = 2 * (a * f**2 + sigma(s, f, *args).real) - 2 * s * dsigma
                ward_errors.append(abs(actual - expected) / (a * f**2))
                bad = source_insertions(s, f, *args, omit_scale_vertices=True)
                missing_errors.append(abs((bad - actual) / f**2 - beta))
        check(f"{ch['name']} zero-soft insertions versus mass differentiation", max(source_errors) < 2e-9,
              max_normalized_error=max(source_errors), category="diagram differentiation and quadrature")
        check(f"{ch['name']} off-shell scaling Ward identity", max(ward_errors) < 2e-11,
              max_normalized_error=max(ward_errors), category="diagram differentiation and quadrature")
        check(f"{ch['name']} omitted regulator vertex leaves beta residual", max(missing_errors) < 2e-12 and beta > 0,
              beta=beta, residual_error=max(missing_errors), category="negative control")
        imag = sigma(2 * a, 1, *args).imag
        check(f"{ch['name']} absorptive cut sign and normalization", abs(imag + a**2 / (8 * math.pi)) < 1e-12,
              imaginary_self_energy=imag, category="cut check")
        def cw_potential(probe: float) -> float:
            hessian = np.array([[a * probe**2, 2 * a * probe, 0.0],
                                [2 * a * probe, a + lam * probe**2 / 2, 0.0],
                                [0.0, 0.0, b + PARAMS["kappa"] * probe**2 / 2]])
            eigenvalues = np.linalg.eigvalsh(hessian)
            # An off-valley negative eigenvalue contributes only O(probe^4)
            # here; its real logarithm suffices for the second derivative.
            return sum(x*x * (math.log(abs(x) / PARAMS["z"]**2) - 1.5)
                       for x in eigenvalues if x != 0.0) / (4 * LOOP)
        h = 1e-4
        curvature = 2 * (cw_potential(h) - cw_potential(0.0)) / h**2
        diagram = sigma(0.0, 1.0, *args, evanescent=False).real
        check(f"{ch['name']} effective-potential Hessian versus zero-momentum diagrams",
              abs(curvature-diagram) / a < 2e-7,
              normalized_error=abs(curvature-diagram)/a, category="independent eigenvalue calculation")
        fixed_mu_coefficient = lambda f: sigma(a*f*f, f, a, b, lam, PARAMS["kappa"],
                                               PARAMS["z"]/f, evanescent=False).real / (f*f)
        anomaly = dlog(fixed_mu_coefficient, 1.0) / (2*a)
        check(f"{ch['name']} fixed-mu negative control from finite differences",
              abs(anomaly-beta/(2*a)) < 2e-10,
              response_at_one_loop=anomaly, category="negative control")
        frac = one(1) / a
        check(f"{ch['name']} small one-loop mass correction", abs(frac) < 0.03, fractional_mass_squared_shift=frac,
              category="benchmark perturbative-size gate")
        ir = [dict(delta=d, sigma_s_derivative=4 * a * kernel_prime(1 - d) / LOOP)
              for d in [1e-3, 1e-6, 1e-9]]
        check(f"{ch['name']} infrared slope grows logarithmically", all(ir[i+1]["sigma_s_derivative"] < ir[i]["sigma_s_derivative"] for i in range(2)),
              category="infrared diagnostic")
        summaries.append(dict(channel=ch["name"], mass_at_f1_one_loop=mass(1), fractional_mass_squared_shift=frac,
                              evanescent_mass_squared_shift=-8 * a**2 / LOOP,
                              fixed_mu_response_at_one_loop=beta / (2 * a), infrared_slope=ir))
    triangle = []
    for Q2 in [0.01, 0.1, 1.0]:
        J = quad(lambda u: 1 / (1 + u * (1-u) * Q2), 0, 1, epsabs=1e-13)[0]
        Jclosed = 4 * math.atanh(math.sqrt(Q2 / (4 + Q2))) / math.sqrt(Q2 * (4 + Q2))
        check(f"triangle angular integral Q2={Q2}", abs(J-Jclosed) < 1e-12,
              category="independent quadrature")
        vals = []
        for vmin in [1e-2, 1e-4, 1e-6]:
            exact = quad(lambda v: quad(lambda u: v / (v*v*(1+u*(1-u)*Q2)) - 1/v,
                                        0, 1, epsabs=1e-11)[0], vmin, 1, epsabs=1e-10)[0]
            predicted = math.log(1/vmin) * (J-1)
            vals.append(dict(vmin=vmin, subtracted_triangle=exact))
            check(f"subtracted soft triangle Q2={Q2} vmin={vmin}", abs(exact-predicted) < 2e-10,
                  absolute_error=abs(exact-predicted), category="two-parameter quadrature")
        triangle.append(dict(Q2_over_m2=Q2, logarithm_coefficient_m2=J-1, values=vals))
    masses = [x["mass_at_f1_one_loop"] for x in summaries]
    return dict(parameters=PARAMS, channels=summaries, mass_ratio_A_over_B=masses[0]/masses[1],
                triangle_IR_cut_is_parameter_cut_not_physical_regulator=True, triangle=triangle)


def main() -> None:
    symbolic_checks()
    numerical = numerical_checks()
    source = Path(__file__).resolve()
    raw = source.read_bytes()
    output = dict(title="Two-channel one-loop scalar/dilaton audit", author="Angus Muffatti",
                  assistance="AI-assisted derivation and implementation", date="2026-10-11",
                  scope="One-loop scalar theory, zero-soft source, and an on-shell triangle subdiagram; not Yukawa, inclusive dressing, or a physical clock calculation.",
                  source_sha256=hashlib.sha256(raw).hexdigest(),
                  source_git_blob_sha1=hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
                  versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, sympy=sp.__version__),
                  checks=CHECKS, numerical=numerical,
                  total=len(CHECKS), passed=sum(x["passed"] for x in CHECKS),
                  all_passed=all(x["passed"] for x in CHECKS))
    target = source.with_name("results.json")
    target.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({k: output[k] for k in ["total", "passed", "all_passed", "source_git_blob_sha1"]}, indent=2))
    print(json.dumps(numerical, indent=2))
    if not output["all_passed"]:
        raise SystemExit("One or more checks failed; inspect results.json")


if __name__ == "__main__":
    main()
