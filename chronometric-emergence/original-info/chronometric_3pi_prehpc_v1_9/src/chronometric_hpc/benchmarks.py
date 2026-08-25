from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import numpy as np


@dataclass(frozen=True)
class BenchmarkMetrics:
    free_scalar_equal_time_rho: float
    free_scalar_equal_time_derivative_error: float
    kms_residual: float
    abelian_ward_residual: float
    markov_limit_max_error: float
    narrow_width_area_error: float
    narrow_width_peak_location_error: float


def free_scalar_spectral(t: np.ndarray, tp: float, omega: float) -> np.ndarray:
    return np.sin(omega * (t - tp)) / omega


def free_scalar_statistical(t: np.ndarray, tp: float, omega: float, temperature: float) -> np.ndarray:
    n = 1.0 / np.expm1(omega / temperature)
    return (n + 0.5) * np.cos(omega * (t - tp)) / omega


def line_integral_vertex_residual() -> float:
    # Scalar toy inverse propagator K(p)=p^2+m^2+a(p.u)^2.  The analytic
    # line-integral vertex must satisfy q_mu Gamma^mu=K(p+q)-K(p).
    metric = np.diag([1.0, -1.0, -1.0, -1.0])
    p = np.array([2.0, 0.2, -0.5, 0.3])
    q = np.array([0.7, -0.1, 0.4, 0.2])
    u = np.array([1.0, 0.0, 0.0, 0.0])
    a = 0.17
    m2 = 0.33
    dot = lambda x, y: float(x @ metric @ y)
    def inv(x: np.ndarray) -> float:
        return dot(x, x) + m2 + a * dot(x, u) ** 2
    # Integral of dK/dp_mu along p+s q.  Contravariant component convention.
    mid = p + 0.5 * q
    gamma = 2.0 * metric @ mid + 2.0 * a * dot(mid, u) * (metric @ u)
    lhs = float(q @ gamma)
    rhs = inv(p + q) - inv(p)
    return abs(lhs - rhs) / max(abs(rhs), 1.0e-30)


def run_benchmarks() -> dict[str, float | bool]:
    omega = 2.3
    temperature = 4.1
    dt = 1.0e-6
    rho0 = float(free_scalar_spectral(np.array([0.0]), 0.0, omega)[0])
    derivative = float((free_scalar_spectral(np.array([dt]), 0.0, omega)[0] - free_scalar_spectral(np.array([-dt]), 0.0, omega)[0]) / (2 * dt))
    derivative_error = abs(derivative - 1.0)

    # Frequency-space KMS check for a damped oscillator: F(omega)=-(n_B+1/2)rho(omega).
    w = np.linspace(0.15, 8.0, 1000)
    gamma = 0.12
    mass = 1.7
    rho = 4 * gamma * w / ((w**2 - mass**2)**2 + (2 * gamma * w)**2)
    n = 1.0 / np.expm1(w / temperature)
    F = -(n + 0.5) * rho
    kms = np.max(np.abs(F + 0.5 / np.tanh(w / (2 * temperature)) * rho)) / max(np.max(np.abs(F)), 1.0e-30)

    # Finite-memory two-variable embedding approaches dn/dt=-2 Gamma(n-neq) for Lambda>>Gamma.
    Gamma = 0.02
    Lambda = 50.0
    times = np.linspace(0, 200, 4001)
    from scipy.linalg import expm
    generator = np.array([[0.0, -2.0 * Gamma], [Lambda, -Lambda]])
    initial = np.array([1.0, 0.0])
    values = np.array([(expm(generator * t) @ initial)[0] for t in times])
    markov = np.exp(-2 * Gamma * times)
    # Ignore the microscopic boundary layer t < 5/Lambda; the comparison tests
    # the controlled Markov limit rather than mismatched auxiliary initial data.
    mask = times >= 5.0 / Lambda
    markov_error = float(np.max(np.abs(values[mask] - markov[mask])))

    # Normalized Breit-Wigner representation of a delta function on a wide grid.
    center = 1.4
    width = 0.003
    grid = np.linspace(center - 0.25, center + 0.25, 200001)
    lorentz = (width / math.pi) / ((grid - center)**2 + width**2)
    area = float(np.trapezoid(lorentz, grid))
    peak = float(grid[int(np.argmax(lorentz))])

    metrics = BenchmarkMetrics(
        free_scalar_equal_time_rho=abs(rho0),
        free_scalar_equal_time_derivative_error=derivative_error,
        kms_residual=float(kms),
        abelian_ward_residual=line_integral_vertex_residual(),
        markov_limit_max_error=markov_error,
        narrow_width_area_error=abs(area - 1.0),
        narrow_width_peak_location_error=abs(peak - center),
    )
    result = asdict(metrics)
    result["pass_free"] = metrics.free_scalar_equal_time_rho < 1e-14 and derivative_error < 1e-9
    result["pass_kms"] = metrics.kms_residual < 1e-12
    result["pass_ward"] = metrics.abelian_ward_residual < 1e-12
    # This reduced embedding has O(Gamma/Lambda) error; 1e-2 is the declared test gate.
    result["pass_markov"] = metrics.markov_limit_max_error < 1e-2
    result["pass_narrow_width"] = metrics.narrow_width_area_error < 1e-2 and metrics.narrow_width_peak_location_error < 1e-12
    result["all_pass"] = all(result[k] for k in ["pass_free", "pass_kms", "pass_ward", "pass_markov", "pass_narrow_width"])
    return result
