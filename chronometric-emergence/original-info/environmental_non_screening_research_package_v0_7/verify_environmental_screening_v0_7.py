#!/usr/bin/env python3
"""Verification and benchmark calculations for Z6 QCD chronometry environmental profiles.

The script derives the finite-density effective potential, solves the exact nonlinear
spherical boundary-value problem in scaled variables, evaluates Earth/Sun/laboratory
benchmarks, and generates figures/tables used by the v0.7 technical note.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import G, c, electron_volt
from scipy.integrate import solve_bvp
from scipy.optimize import brentq

OUT = Path('/mnt/data')

# -----------------------------
# Model benchmark and constants
# -----------------------------
PI = math.pi
HBARC_EV_M = 1.973269804e-7
MPL_EV = 2.435e27               # reduced Planck mass
M_HEAVY_EV = 1.0e13             # 10 TeV
EPS = 1.0e-6
P_QCD = 2.0 / 27.0              # conservative Q_Lambda = 1 source coupling
F_A_EV = MPL_EV
X_INF = PI / 2.0
DX_ADJ = PI / 3.0
N_C = 3.0

M_A2_EV2 = (27.0 / (320.0 * PI**2)) * (M_HEAVY_EV**4 / F_A_EV**2) * EPS**6
M_A_EV = math.sqrt(M_A2_EV2)
LAMBDA_A_M = HBARC_EV_M / M_A_EV
V0_EV4 = M_A2_EV2 * F_A_EV**2 / 36.0
SIGMA_WALL_EV3 = (2.0 / 9.0) * M_A_EV * F_A_EV**2

J_PER_M3_PER_EV4 = electron_volt / HBARC_EV_M**3
EV4_PER_KG_M3 = c**2 / J_PER_M3_PER_EV4
EV4_PER_G_CM3 = 1000.0 * EV4_PER_KG_M3


def rho_ev4(rho_kg_m3: float | np.ndarray) -> float | np.ndarray:
    return np.asarray(rho_kg_m3) * EV4_PER_KG_M3


def source_mass_factor(x: np.ndarray | float, p: float = P_QCD) -> np.ndarray | float:
    """A(x)=m_A(x)/m_A(pi/2) at leading 2/27 threshold order."""
    return np.power(1.0 - EPS * np.cos(x), p)


def source_mass_factor_prime(x: np.ndarray | float, p: float = P_QCD) -> np.ndarray | float:
    return p * EPS * np.sin(x) * np.power(1.0 - EPS * np.cos(x), p - 1.0)


def veff_dimensionless(x: np.ndarray, t: float, p: float = P_QCD) -> np.ndarray:
    """[V_eff(x)-V_eff(pi/2)] / V0 for t=rho*p*eps/(m_a^2 f_a^2)."""
    # Stable evaluation of A(x)-1 for tiny EPS.
    log_a = p * np.log1p(-EPS * np.cos(x))
    a_minus_one = np.expm1(log_a)
    rho_over_v0 = 36.0 * t / (p * EPS)
    return 1.0 + np.cos(6.0 * x) + rho_over_v0 * a_minus_one


# Local homogeneous-medium thresholds (epsilon -> 0 is more than adequate here).
y_star = (6.0 - math.sqrt(21.0)) / 20.0
c_star = math.sqrt(y_star)
x_star = math.acos(c_star)
D_STAR = 32.0 * c_star**5 - 32.0 * c_star**3 + 6.0 * c_star
T_SPINODAL = D_STAR / 6.0
RHO_C_EV4 = M_A2_EV2 * F_A_EV**2 / (P_QCD * EPS)
RHO_C_G_CM3 = RHO_C_EV4 / EV4_PER_G_CM3
RHO_SP_G_CM3 = T_SPINODAL * RHO_C_G_CM3

# Adjacent-vacuum matter-energy gain coefficient.
DELTA_A_ADJ = 1.0 - float(source_mass_factor(PI / 6.0))
C_EPS = DELTA_A_ADJ / (P_QCD * EPS)  # -> sqrt(3)/2
Q_CONV_0 = DX_ADJ**2 / (2.0 * C_EPS)


@dataclass
class Source:
    name: str
    mass_kg: float
    radius_m: float
    rho_mean_kg_m3: float
    rho_max_kg_m3: float
    profile: Callable[[np.ndarray], np.ndarray]


@dataclass
class Result:
    source: str
    radius_m: float
    mass_kg: float
    phi_surface: float
    mu_mR: float
    q0_scalar_compactness: float
    t_mean: float
    t_max: float
    tmax_over_spinodal: float
    center_shift_dx: float
    surface_shift_dx: float
    linear_surface_form_factor: float
    nonlinear_screening_factor: float
    nonlinear_relative_bound: float
    conversion_threshold_q: float
    q0_over_conversion_threshold: float
    max_subsphere_q: float
    max_subsphere_radius_fraction: float
    max_subsphere_q_over_conversion_threshold: float
    clock_ratio_shift_surface_K1: float
    adjacent_phase_energy_radius_m: float
    adjacent_phase_nucleation_radius_m: float


def make_earth_profile() -> Callable[[np.ndarray], np.ndarray]:
    # PREM-inspired four-layer density model; tanh smoothing avoids numerical
    # artifacts at boundaries. Raw mean is already 5.510 g/cm^3.
    bounds = np.array([1221.5 / 6371.0, 3480.0 / 6371.0, 5701.0 / 6371.0])
    densities = np.array([13.0, 11.0, 5.0, 3.3]) * 1000.0
    width = 0.0015

    def raw(s: np.ndarray) -> np.ndarray:
        s = np.asarray(s)
        val = np.full_like(s, densities[-1], dtype=float)
        for i, b in enumerate(bounds[::-1]):
            j = len(bounds) - 1 - i
            jump = densities[j] - densities[j + 1]
            val += 0.5 * jump * (1.0 - np.tanh((s - b) / width))
        return val

    grid = np.linspace(0.0, 1.0, 200001)
    mean_raw = 3.0 * np.trapezoid(raw(grid) * grid**2, grid)
    scale = 5514.0 / mean_raw

    def profile(s: np.ndarray) -> np.ndarray:
        return scale * raw(np.asarray(s))

    return profile


def make_sun_profile() -> Callable[[np.ndarray], np.ndarray]:
    # Analytic centrally concentrated profile matching mean and central density.
    rho_c = 150000.0
    rho_mean = 1408.0
    ratio = rho_mean / rho_c

    def f_n(n: float) -> float:
        return 6.0 / ((n + 1.0) * (n + 2.0) * (n + 3.0)) - ratio

    n = brentq(f_n, 0.0, 30.0)

    def profile(s: np.ndarray) -> np.ndarray:
        s = np.asarray(s)
        return rho_c * np.maximum(1.0 - s, 0.0) ** n

    profile.exponent = n  # type: ignore[attr-defined]
    return profile


def uniform_profile(rho: float) -> Callable[[np.ndarray], np.ndarray]:
    def profile(s: np.ndarray) -> np.ndarray:
        return np.full_like(np.asarray(s), rho, dtype=float)
    return profile


EARTH = Source(
    'Earth', 5.9722e24, 6.371e6, 5514.0, 13000.0, make_earth_profile()
)
SUN = Source(
    'Sun', 1.98847e30, 6.957e8, 1408.0, 150000.0, make_sun_profile()
)
R_LAB = 0.05
RHO_W = 19250.0
M_LAB = 4.0 * PI * R_LAB**3 * RHO_W / 3.0
LAB = Source(
    'Tungsten sphere (R=5 cm)', M_LAB, R_LAB, RHO_W, RHO_W, uniform_profile(RHO_W)
)
SOURCES = [EARTH, SUN, LAB]


def profile_D(source: Source) -> Callable[[np.ndarray], np.ndarray]:
    # D(s)=4 pi R^3 rho(s)/M, normalized so integral_0^1 D s^2 ds=1.
    grid = np.linspace(0.0, 1.0, 200001)
    rho = source.profile(grid)
    norm = np.trapezoid(rho * grid**2, grid)

    def D(s: np.ndarray) -> np.ndarray:
        return source.profile(np.asarray(s)) / norm

    return D


def stable_sinc(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z)
    out = np.empty_like(z, dtype=float)
    small = np.abs(z) < 1.0e-6
    zs = z[small]
    out[small] = 1.0 - zs**2 / 6.0 + zs**4 / 120.0
    out[~small] = np.sin(z[~small]) / z[~small]
    return out


def solve_profile(source: Source):
    phi = G * source.mass_kg / (source.radius_m * c**2)
    mu = M_A_EV * source.radius_m / HBARC_EV_M
    q0 = (P_QCD * EPS * source.mass_kg * c**2 / electron_volt) / (
        4.0 * PI * F_A_EV**2 * (source.radius_m / HBARC_EV_M)
    )
    # Cross-check against 2 p eps (M_P/f)^2 Phi.
    q0_grav = 2.0 * P_QCD * EPS * (MPL_EV / F_A_EV) ** 2 * phi
    assert abs(q0 / q0_grav - 1.0) < 5.0e-4

    D = profile_D(source)
    mesh = np.linspace(0.0, 1.0, 900)
    singular = np.array([[0.0, 0.0], [0.0, -2.0]])

    def bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
        return np.array([ya[1], yb[1] + (1.0 + mu) * yb[0]])

    def f_linear(s: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.vstack((y[1], mu**2 * y[0] + D(s)))

    guess = np.zeros((2, mesh.size))
    guess[0] = -1.0
    linear = solve_bvp(
        f_linear, bc, mesh, guess, S=singular, tol=3.0e-9,
        max_nodes=60000, verbose=0
    )
    if linear.status != 0:
        raise RuntimeError(f'Linear BVP failed for {source.name}: {linear.message}')

    def f_nonlinear(s: np.ndarray, y: np.ndarray) -> np.ndarray:
        u = y[0]
        delta = q0 * u
        vacuum = mu**2 * u * stable_sinc(6.0 * delta)
        matter = D(s) * np.cos(delta) * np.power(1.0 + EPS * np.sin(delta), P_QCD - 1.0)
        return np.vstack((y[1], vacuum + matter))

    nonlinear = solve_bvp(
        f_nonlinear, bc, mesh, linear.sol(mesh), S=singular,
        tol=3.0e-9, max_nodes=60000, verbose=0
    )
    if nonlinear.status != 0:
        raise RuntimeError(f'Nonlinear BVP failed for {source.name}: {nonlinear.message}')

    # Evaluate on a regular grid.
    s_eval = np.linspace(0.0, 1.0, 2001)
    u_lin = linear.sol(s_eval)[0]
    u_nl = nonlinear.sol(s_eval)[0]

    dx_center = q0 * u_nl[0]
    dx_surface = q0 * u_nl[-1]
    form_factor = -u_lin[-1]
    screening_factor = u_nl[-1] / u_lin[-1]
    max_delta = float(np.max(np.abs(q0 * u_nl)))
    # Leading relative nonlinear source corrections: matter O(eps*delta),
    # vacuum and trigonometric source O(delta^2).
    nonlinear_bound = (1.0 - P_QCD) * EPS * max_delta + 7.0 * max_delta**2

    t_mean = float(rho_ev4(source.rho_mean_kg_m3) * P_QCD * EPS /
                   (M_A2_EV2 * F_A_EV**2))
    t_max = float(rho_ev4(source.rho_max_kg_m3) * P_QCD * EPS /
                  (M_A2_EV2 * F_A_EV**2))

    q_conv = Q_CONV_0 * (1.0 + mu)

    # Maximum scalar compactness of any concentric sub-sphere. This is the
    # relevant diagnostic for a converted core rather than the whole body.
    s_q = np.linspace(1.0e-8, 1.0, 100001)
    rho_q = source.profile(s_q)
    integrand_q = rho_q * s_q**2
    ds_q = s_q[1] - s_q[0]
    cumulative_q = np.zeros_like(s_q)
    cumulative_q[1:] = np.cumsum(0.5 * (integrand_q[1:] + integrand_q[:-1]) * ds_q)
    mass_fraction_q = cumulative_q / cumulative_q[-1]
    q_sub = q0 * mass_fraction_q / s_q
    iq = int(np.argmax(q_sub))
    max_subsphere_q = float(q_sub[iq])
    max_subsphere_radius_fraction = float(s_q[iq])

    d_g = P_QCD * EPS * MPL_EV / F_A_EV
    clock_ratio_shift_surface_K1 = abs(d_g * dx_surface)

    # Thin-wall adjacent-vacuum radii, quoted only as large-R diagnostics.
    delta_v_mean = float(rho_ev4(source.rho_mean_kg_m3) * DELTA_A_ADJ)
    r_nuc = 2.0 * SIGMA_WALL_EV3 / delta_v_mean * HBARC_EV_M
    r_energy = 3.0 * SIGMA_WALL_EV3 / delta_v_mean * HBARC_EV_M

    result = Result(
        source=source.name,
        radius_m=source.radius_m,
        mass_kg=source.mass_kg,
        phi_surface=phi,
        mu_mR=mu,
        q0_scalar_compactness=q0,
        t_mean=t_mean,
        t_max=t_max,
        tmax_over_spinodal=t_max / T_SPINODAL,
        center_shift_dx=dx_center,
        surface_shift_dx=dx_surface,
        linear_surface_form_factor=form_factor,
        nonlinear_screening_factor=screening_factor,
        nonlinear_relative_bound=nonlinear_bound,
        conversion_threshold_q=q_conv,
        q0_over_conversion_threshold=q0 / q_conv,
        max_subsphere_q=max_subsphere_q,
        max_subsphere_radius_fraction=max_subsphere_radius_fraction,
        max_subsphere_q_over_conversion_threshold=max_subsphere_q / Q_CONV_0,
        clock_ratio_shift_surface_K1=clock_ratio_shift_surface_K1,
        adjacent_phase_energy_radius_m=r_energy,
        adjacent_phase_nucleation_radius_m=r_nuc,
    )
    return result, s_eval, u_lin, u_nl


# -----------------------------
# Run calculations
# -----------------------------
results: list[Result] = []
profiles = {}
for src in SOURCES:
    res, s, ulin, unl = solve_profile(src)
    results.append(res)
    profiles[src.name] = {'s': s, 'u_linear': ulin, 'u_nonlinear': unl}

# Solar core patch above the local spinodal in the analytic profile.
sun_profile = SUN.profile
rho_spin_kg_m3 = RHO_SP_G_CM3 * 1000.0
n_sun = float(getattr(sun_profile, 'exponent'))
s_spin = 1.0 - (rho_spin_kg_m3 / SUN.rho_max_kg_m3) ** (1.0 / n_sun)
grid_core = np.linspace(0.0, s_spin, 100001)
full_grid = np.linspace(0.0, 1.0, 100001)
core_mass_frac = (
    np.trapezoid(sun_profile(grid_core) * grid_core**2, grid_core) /
    np.trapezoid(sun_profile(full_grid) * full_grid**2, full_grid)
)
q0_sun = results[1].q0_scalar_compactness
mu_sun = results[1].mu_mR
q0_sun_core = q0_sun * core_mass_frac / s_spin
mu_sun_core = mu_sun * s_spin
t_sun_core_mean = 3.0 * q0_sun_core / mu_sun_core**2

# -----------------------------
# Verification assertions
# -----------------------------
assert abs(M_A_EV - 3.79715263282238e-21) / M_A_EV < 1e-12
assert abs(T_SPINODAL - 0.1727234029434) < 2e-12
assert abs(RHO_SP_G_CM3 - 46.2496629551) < 1e-7
assert abs(C_EPS - math.sqrt(3.0) / 2.0) < 1e-6
assert abs(Q_CONV_0 - 0.6331354175) < 2e-6
assert results[0].tmax_over_spinodal < 1.0
assert results[1].tmax_over_spinodal > 1.0
assert results[2].tmax_over_spinodal < 1.0
assert all(r.q0_over_conversion_threshold < 1e-11 for r in results)
assert all(r.max_subsphere_q_over_conversion_threshold < 2e-12 for r in results)
assert all(abs(r.nonlinear_screening_factor - 1.0) < 1e-12 for r in results)
assert results[1].nonlinear_relative_bound < 2e-18
assert t_sun_core_mean > T_SPINODAL

# -----------------------------
# Tables and machine output
# -----------------------------
csv_path = OUT / 'environmental_screening_benchmarks_v0_7.csv'
with csv_path.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(asdict(results[0]).keys()))
    writer.writeheader()
    for r in results:
        writer.writerow(asdict(r))

AU_M = 1.495978707e11
D_G = P_QCD * EPS * MPL_EV / F_A_EV
sun_result = results[1]
sun_x_at_earth = (
    sun_result.q0_scalar_compactness
    * sun_result.linear_surface_form_factor
    * sun_result.radius_m / AU_M
    * math.exp(-M_A_EV * (AU_M - sun_result.radius_m) / HBARC_EV_M)
)

summary = {
    'model': {
        'M_heavy_eV': M_HEAVY_EV,
        'f_a_eV': F_A_EV,
        'epsilon': EPS,
        'p_QCD': P_QCD,
        'm_a_eV': M_A_EV,
        'compton_length_m': LAMBDA_A_M,
        'compton_length_AU': LAMBDA_A_M / 1.495978707e11,
        'V0_eV4': V0_EV4,
        'wall_tension_eV3': SIGMA_WALL_EV3,
        'rho_c_g_cm3': RHO_C_G_CM3,
        'rho_spinodal_g_cm3': RHO_SP_G_CM3,
        'spinodal_t': T_SPINODAL,
        'spinodal_x_rad': x_star,
        'adjacent_phase_delta_A': DELTA_A_ADJ,
        'finite_size_conversion_q_threshold_mu0': Q_CONV_0,
        'dimensionless_visible_QCD_coupling_dg': D_G,
        'unscreened_fifth_force_fraction_2dg2': 2.0 * D_G**2,
    },
    'solar_signal_at_earth_orbit': {
        'x_shift_at_1_AU': sun_x_at_earth,
        'clock_ratio_shift_K1': D_G * sun_x_at_earth,
        'annual_modulation_estimate_e_0p0167': 2.0 * 0.0167 * D_G * sun_x_at_earth,
    },
    'solar_core_patch': {
        'spinodal_radius_fraction': s_spin,
        'mass_fraction': core_mass_frac,
        'mu': mu_sun_core,
        'q0': q0_sun_core,
        'mean_t': t_sun_core_mean,
        'q0_over_conversion_threshold': q0_sun_core / (Q_CONV_0 * (1.0 + mu_sun_core)),
    },
    'benchmarks': [asdict(r) for r in results],
    'checks': {
        'all_bvp_solutions_converged': True,
        'all_nonlinear_screening_factors_unity_to_1e-12': True,
        'sun_core_locally_above_spinodal_but_finite_size_stable': True,
    },
}
json_path = OUT / 'environmental_screening_verification_v0_7.json'
json_path.write_text(json.dumps(summary, indent=2))

# -----------------------------
# Figures
# -----------------------------
# 1. Effective potential in homogeneous media.
x = np.linspace(0.0, PI / 2.0, 2000)
plt.figure(figsize=(8.0, 5.2))
for label, t in [
    ('Vacuum', 0.0),
    ('Earth mean', results[0].t_mean),
    ('Tungsten', results[2].t_mean),
    ('Solar core', results[1].t_max),
]:
    u = veff_dimensionless(x, t)
    plt.plot(x, u, label=label)
plt.axvline(PI / 2.0, linestyle='--', linewidth=0.9)
plt.axvline(PI / 6.0, linestyle=':', linewidth=0.9)
plt.xlabel(r'$x=a/f_a$')
plt.ylabel(r'$[V_{\rm eff}(x)-V_{\rm eff}(\pi/2)]/V_0$')
plt.title('Local finite-density effective potential')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'environmental_effective_potential_v0_7.png', dpi=220)
plt.close()

# 2. Normalized spherical profiles (inside and near exterior).
plt.figure(figsize=(8.0, 5.2))
for src, res in zip(SOURCES, results):
    data = profiles[src.name]
    s_in = data['s']
    u_in = data['u_nonlinear']
    s_out = np.linspace(1.0, 5.0, 1000)
    u_out = u_in[-1] * np.exp(-res.mu_mR * (s_out - 1.0)) / s_out
    s_all = np.concatenate([s_in, s_out[1:]])
    u_all = np.concatenate([u_in, u_out[1:]])
    plt.plot(s_all, u_all, label=src.name)
plt.axvline(1.0, linestyle='--', linewidth=0.9)
plt.xlabel(r'$r/R$')
plt.ylabel(r'$(x-x_\infty)/q_0$')
plt.title('Exact nonlinear environmental profiles (normalized)')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'environmental_profiles_v0_7.png', dpi=220)
plt.close()

# 3. Screening/phase-conversion map.
mu_grid = np.logspace(-17, 2, 1200)
q_spin = T_SPINODAL * mu_grid**2 / 3.0
q_conv = Q_CONV_0 * (1.0 + mu_grid)
plt.figure(figsize=(8.0, 5.6))
plt.loglog(mu_grid, q_spin, label='Homogeneous spinodal (mean density)')
plt.loglog(mu_grid, q_conv, label='Finite-size phase-conversion threshold')
for r in results:
    plt.scatter(r.mu_mR, r.q0_scalar_compactness, s=45)
    plt.annotate(r.source, (r.mu_mR, r.q0_scalar_compactness), xytext=(5, 5), textcoords='offset points', fontsize=8)
plt.scatter(mu_sun_core, q0_sun_core, marker='x', s=55)
plt.annotate('Solar core patch', (mu_sun_core, q0_sun_core), xytext=(5, -13), textcoords='offset points', fontsize=8)
plt.xlabel(r'$\mu=m_aR$')
plt.ylabel(r'$q_0=M p\epsilon/(4\pi f_a^2R)$')
plt.title('Density preference versus finite-size ability to move the field')
plt.ylim(1e-35, 20)
plt.xlim(1e-17, 1e2)
plt.legend(loc='lower right', fontsize=8)
plt.tight_layout()
plt.savefig(OUT / 'environmental_screening_map_v0_7.png', dpi=220)
plt.close()

print(json.dumps(summary, indent=2))
print(f'Wrote {csv_path}')
print(f'Wrote {json_path}')
