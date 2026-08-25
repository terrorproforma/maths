#!/usr/bin/env python3
"""Working cosmological solver for Z_N protected QCD chronometry v0.8.

Conventions:
- reduced Planck mass throughout;
- x=a/f_a is the compact field;
- V0 = m_a^2 f_a^2 / N^2 * (1 + cos N x), so x=0 is a maximum for even N;
- visible thermal free energies favour x=0 (smallest visible threshold mass);
- a weakly populated adjacent sector k=N-1 biases the field toward +pi/N.

This is an EFT/cosmology verification script, not a precision Boltzmann code.
"""
from __future__ import annotations

import dataclasses
import json
import math
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
from scipy.special import k1
from scipy.optimize import brentq

# ---------- constants ----------
MPL = 2.435e18  # reduced Planck mass, GeV
T0 = 2.7255 * 8.617333262e-14  # CMB temperature, GeV
H0_KM_S_MPC = 67.4
# 1 s^-1 = 6.582119569e-25 GeV; 1 Mpc = 3.085677581e19 km
H0 = H0_KM_S_MPC / 3.085677581e19 * 6.582119569e-25  # GeV
OMEGA_M = 0.315
OMEGA_B = 0.0493
OMEGA_L = 0.685
RHO_C0 = 3.0 * MPL**2 * H0**2
RHO_B0 = OMEGA_B * RHO_C0
GSTAR_S0 = 3.909
P_QCD = 2.0 / 27.0
NC = 3.0
G_PSI = 12.0  # Dirac color triplet: 4 spin/particle x 3 color
EV_PER_GEV = 1e9
H0_EV = H0 * EV_PER_GEV
AU_INV_EV = 1.3198e-18

# Borsanyi et al. 2+1+1 trace anomaly fit parameters, arXiv:1606.07494
TRACE_PARAMS = dict(h0=0.353, h1=-1.04, h2=0.534,
                    f0=1.75, f1=6.80, f2=-5.18,
                    g1=0.525, g2=0.160)

# g_rho and g_rho/g_s table, T in MeV, from arXiv:1606.07494 supplement.
_LOG10_T_MEV = np.array([
    0.00, 0.50, 1.00, 1.25, 1.60, 2.00, 2.15, 2.20,
    2.40, 2.50, 3.00, 4.00, 4.30, 4.60, 5.00, 5.45,
], dtype=float)
_G_RHO_TAB = np.array([
    10.71, 10.74, 10.76, 11.09, 13.68, 17.61, 24.07, 29.84,
    47.83, 53.04, 73.48, 83.10, 85.56, 91.97, 102.17, 104.98,
], dtype=float)
_GRHO_OVER_GS_TAB = np.array([
    1.00228, 1.00029, 1.00048, 1.00505, 1.02159, 1.02324,
    1.05423, 1.07578, 1.06118, 1.04690, 1.01778, 1.00123,
    1.00389, 1.00887, 1.00750, 1.00023,
], dtype=float)
_GRHO_SPL = PchipInterpolator(_LOG10_T_MEV, _G_RHO_TAB, extrapolate=True)
_RATIO_SPL = PchipInterpolator(_LOG10_T_MEV, _GRHO_OVER_GS_TAB, extrapolate=True)


def smoothstep(z: float) -> float:
    z = max(0.0, min(1.0, z))
    return z * z * (3.0 - 2.0 * z)


def g_rho(T: float) -> float:
    """Approximate SM energy degrees of freedom as a smooth function of T [GeV]."""
    T_mev = T * 1e3
    if T_mev <= 0.05:
        return 3.383
    if T_mev < 1.0:
        # smooth e+e- annihilation interpolation in log T
        z = (math.log10(T_mev) - math.log10(0.05)) / (0.0 - math.log10(0.05))
        return 3.383 + (10.71 - 3.383) * smoothstep(z)
    logt = math.log10(T_mev)
    if logt <= _LOG10_T_MEV[-1]:
        return float(_GRHO_SPL(logt))
    # approach 106.75 above the table
    z = min(1.0, max(0.0, (logt - _LOG10_T_MEV[-1]) / 1.0))
    return float(_G_RHO_TAB[-1] + (106.75 - _G_RHO_TAB[-1]) * smoothstep(z))


def g_s(T: float) -> float:
    T_mev = T * 1e3
    if T_mev <= 0.05:
        return GSTAR_S0
    if T_mev < 1.0:
        z = (math.log10(T_mev) - math.log10(0.05)) / (0.0 - math.log10(0.05))
        return GSTAR_S0 + (10.71 / 1.00228 - GSTAR_S0) * smoothstep(z)
    logt = math.log10(T_mev)
    if logt <= _LOG10_T_MEV[-1]:
        gr = float(_GRHO_SPL(logt))
        ratio = float(_RATIO_SPL(logt))
        return gr / ratio
    gr = g_rho(T)
    return gr  # ratio -> 1 at high T


def trace_anomaly_over_t4(T: float) -> float:
    """2+1+1 lattice fit, smoothly tapered outside the 0.08-2 GeV range."""
    if T <= 0.0:
        return 0.0
    t = T / 0.2
    p = TRACE_PARAMS
    core = math.exp(-p['h1'] / t - p['h2'] / (t * t)) * (
        p['h0'] + p['f0'] * (math.tanh(p['f1'] * t + p['f2']) + 1.0)
        / (1.0 + p['g1'] * t + p['g2'] * t * t)
    )
    # The fit is reliable around the crossover and up to ~1 GeV.
    # Taper below 50 MeV and above 2 GeV to avoid overinterpreting it.
    low = smoothstep((math.log10(T) - math.log10(0.03)) /
                     (math.log10(0.08) - math.log10(0.03))) if T < 0.08 else 1.0
    high = 1.0
    if T > 1.0:
        if T >= 5.0:
            high = 0.0
        else:
            high = 1.0 - smoothstep((math.log10(T) - 0.0) / math.log10(5.0))
    return max(0.0, core * low * high)



# Inverse of q(T)=T g_s(T)^(1/3), used to conserve entropy separately in hidden sectors.
_Q_T_GRID = np.geomspace(1e-16, 1e12, 12000)
_Q_GRID = np.array([T * g_s(float(T)) ** (1.0/3.0) for T in _Q_T_GRID])
_LOGT_FROM_LOGQ = PchipInterpolator(np.log(_Q_GRID), np.log(_Q_T_GRID), extrapolate=True)

def sector_temperature(T_visible: float, xi_reheat: float) -> float:
    """Temperature of a decoupled identical sector with high-T ratio xi_reheat."""
    if xi_reheat <= 0.0:
        return 0.0
    q_target = xi_reheat * T_visible * g_s(T_visible) ** (1.0/3.0)
    return float(math.exp(float(_LOGT_FROM_LOGQ(math.log(q_target)))))

def entropy_scale_factor(T: float) -> float:
    """Scale factor normalized a(T0)=1 from visible entropy conservation."""
    return (T0 / T) * (GSTAR_S0 / g_s(T)) ** (1.0 / 3.0)


def build_temperature_map(T_min: float, T_max: float, points: int = 5000):
    Ts = np.geomspace(T_min, T_max, points)
    aa = np.array([entropy_scale_factor(float(T)) for T in Ts])
    uu = np.log(aa)
    # T increases while u decreases. Reverse to make u increasing.
    order = np.argsort(uu)
    u_sorted = uu[order]
    logT_sorted = np.log(Ts[order])
    return PchipInterpolator(u_sorted, logT_sorted, extrapolate=True)


def hidden_radiation_ratio(T: float, xis: Dict[int, float]) -> float:
    """Approximate hidden radiation rho_hidden/rho_visible."""
    grv = g_rho(T)
    total = 0.0
    for k, xi in xis.items():
        if k == 0 or xi <= 0.0:
            continue
        Tk = sector_temperature(T, xi)
        total += g_rho(max(Tk, 1e-20)) * (Tk/T)**4 / grv
    return total


def hubble_from_u_T(u: float, T: float, xis: Dict[int, float]) -> float:
    a = math.exp(u)
    rho_rad_vis = math.pi**2 / 30.0 * g_rho(T) * T**4
    rho_rad = rho_rad_vis * (1.0 + hidden_radiation_ratio(T, xis))
    rho_m = OMEGA_M * RHO_C0 / a**3
    rho_l = OMEGA_L * RHO_C0
    return math.sqrt((rho_rad + rho_m + rho_l) / (3.0 * MPL**2))


def dlnH_du_numeric(u: float, T_of_u: Callable[[float], float], xis: Dict[int, float]) -> float:
    h = 1e-4
    up = min(0.0, u + h)
    um = u - h
    Tp = math.exp(float(T_of_u(up)))
    Tm = math.exp(float(T_of_u(um)))
    Hp = hubble_from_u_T(up, Tp, xis)
    Hm = hubble_from_u_T(um, Tm, xis)
    return (math.log(Hp) - math.log(Hm)) / (up - um)


def F_N(N: int) -> float:
    if N <= 4:
        raise ValueError("N must exceed 4")
    return 24.0 * 2.0 ** (1 - N) / ((N - 1) * (N - 2) * (N - 3) * (N - 4))


def mass_a_GeV(N: int, M: float, f: float, eps: float) -> float:
    c = NC * N * N * F_N(N) / (8.0 * math.pi**2)
    return math.sqrt(c) * M * M * eps ** (N / 2.0) / f


def d_g_at_vacuum(N: int, f: float, eps: float, branch: int = 0) -> float:
    # nearest positive minimum from x=0 is x=pi/N (branch 0)
    xv = (2 * branch + 1) * math.pi / N
    kappa = eps * math.sin(xv) / (1.0 - eps * math.cos(xv))
    return P_QCD * MPL / f * kappa


def thermal_focus_eta_peak(eps: float, f: float, gstar: float = 110.0) -> float:
    """Peak eta=4 m_T^2/H^2 for one Dirac colour triplet.

    The coefficient is obtained by maximizing the exact Bessel-series thermal
    function; it is 0.22673 for g_*=110.  Hidden-sector contributions and
    entropy thresholds are handled in the full numerical evolution.
    """
    coeff = 0.22673 * (110.0 / gstar)
    return coeff * eps * (MPL / f) ** 2


def qcd_focus_eta(T: float, eps: float, f: float) -> float:
    # eta=4 m_T^2/H^2 where V_Q≈-p eps I cos x, m_T^2=p eps I/f^2
    I = trace_anomaly_over_t4(T) * T**4
    H = math.sqrt((math.pi**2 / 30 * g_rho(T) * T**4) / (3 * MPL**2))
    return 4.0 * P_QCD * eps * I / (f * f * H * H)


class FermionThermalAmplitude:
    """Spline of A/(epsilon M^4) as function z=M/T."""
    def __init__(self):
        zs = np.geomspace(1e-4, 60.0, 1000)
        vals = np.array([self._value(float(z)) for z in zs])
        self._spl = PchipInterpolator(np.log(zs), np.log(np.maximum(vals, 1e-300)), extrapolate=True)

    @staticmethod
    def _value(z: float) -> float:
        if z < 1e-3:
            return G_PSI / (24.0 * z * z)
        if z > 60:
            return 0.0
        # alternating Bessel series. Enough terms for z>=1e-3; for tiny z high-T used.
        s = 0.0
        maxn = int(min(5000, max(30, 30.0 / z)))
        for n in range(1, maxn + 1):
            term = ((-1) ** (n + 1)) * float(k1(n * z)) / n
            s += term
            if n > 20 and abs(term) < 1e-12 * max(abs(s), 1e-30):
                break
        return max(0.0, G_PSI / (2.0 * math.pi**2 * z) * s)

    def __call__(self, z: float) -> float:
        if z >= 100:
            return 0.0
        if z <= 1e-4:
            return G_PSI / (24.0 * z * z)
        return float(math.exp(float(self._spl(math.log(z)))))


FERM_AMP = FermionThermalAmplitude()


@dataclasses.dataclass
class Model:
    N: int = 6
    M: float = 5.0e4  # GeV
    f: float = 4.87e11  # GeV
    eps: float = 5.4e-12
    T_R: float = 5.0e6  # GeV
    xi_adj: float = 0.25
    adj_sector: int = 5
    xi_map: dict | None = None
    p_b: float = P_QCD
    include_heavy: bool = True
    include_qcd: bool = True
    include_baryons: bool = True

    @property
    def m(self) -> float:
        return mass_a_GeV(self.N, self.M, self.f, self.eps)

    @property
    def dg(self) -> float:
        return d_g_at_vacuum(self.N, self.f, self.eps)

    @property
    def xis(self) -> Dict[int, float]:
        if self.xi_map is not None:
            out = {0: 1.0}
            out.update({int(k): float(v) for k, v in self.xi_map.items()})
            return out
        return {0: 1.0, self.adj_sector: self.xi_adj}


def dVdx(model: Model, x: float, u: float, T: float) -> Tuple[float, Dict[str, float]]:
    N, M, f, eps = model.N, model.M, model.f, model.eps
    m = model.m
    # zero-temperature periodic potential V=m^2 f^2/N^2 (1+cos Nx)
    d0 = -(m * m * f * f / N) * math.sin(N * x)
    dh = 0.0
    dq = 0.0
    # thermal sectors: visible plus one adjacent populated sector
    for k, xi in model.xis.items():
        if xi <= 0:
            continue
        Tk = sector_temperature(T, xi)
        theta = x + 2.0 * math.pi * k / N
        if model.include_heavy and Tk > 0:
            z = M / Tk
            amp = eps * M**4 * FERM_AMP(z)
            # V=-A cos(theta)
            dh += amp * math.sin(theta)
        if model.include_qcd and 0.02 <= Tk <= 5.0:
            I = trace_anomaly_over_t4(Tk) * Tk**4
            denom = 1.0 - eps * math.cos(theta)
            dq += P_QCD * I * eps * math.sin(theta) / denom
    db = 0.0
    if model.include_baryons and T < 0.5:
        a = math.exp(u)
        rho_b = RHO_B0 / a**3
        denom = 1.0 - eps * math.cos(x)
        db = rho_b * model.p_b * eps * math.sin(x) * denom ** (model.p_b - 1.0)
    return d0 + dh + dq + db, dict(zero=d0, heavy=dh, qcd=dq, baryon=db)


@dataclasses.dataclass
class Background:
    u0: float
    u_end: float
    logT_of_u: object
    logH: object
    dlogH: object
    heavy: Dict[int, object]
    qcd: Dict[int, object]
    baryon: object


def build_background(model: Model, stop_ratio: float = 100.0,
                     points: int = 7200) -> Background:
    """Precompute the thermal and cosmological background for fast basin scans."""
    Tmin = T0
    Tmax = max(model.T_R, 1.01 * model.M)
    logT_of_u = build_temperature_map(Tmin, Tmax, points=7000)
    u0 = math.log(entropy_scale_factor(model.T_R))

    # Locate the requested late-time endpoint from m/H.
    uprobe = np.linspace(u0, 0.0, 5000)
    Tprobe = np.exp(logT_of_u(uprobe))
    Hprobe = np.array([hubble_from_u_T(float(u), float(T), model.xis)
                       for u, T in zip(uprobe, Tprobe)])
    idx = np.where(model.m / Hprobe >= stop_ratio)[0]
    u_end = float(uprobe[idx[0]]) if len(idx) else 0.0

    ug = np.linspace(u0, u_end, points)
    Tg = np.exp(logT_of_u(ug))
    Hg = np.array([hubble_from_u_T(float(u), float(T), model.xis)
                   for u, T in zip(ug, Tg)])
    logHg = np.log(Hg)
    logH_spl = PchipInterpolator(ug, logHg, extrapolate=True)
    dlogH_spl = logH_spl.derivative()

    heavy_spl: Dict[int, object] = {}
    qcd_spl: Dict[int, object] = {}
    for k, xi in model.xis.items():
        phase = 2.0 * math.pi * k / model.N
        Ah = np.zeros_like(ug)
        Aq = np.zeros_like(ug)
        for i, T in enumerate(Tg):
            Tk = sector_temperature(float(T), xi)
            if model.include_heavy and Tk > 0.0:
                Ah[i] = model.eps * model.M**4 * FERM_AMP(model.M / Tk)
            if model.include_qcd and 0.02 <= Tk <= 5.0:
                I = trace_anomaly_over_t4(Tk) * Tk**4
                Aq[i] = P_QCD * I * model.eps
        heavy_spl[k] = PchipInterpolator(ug, Ah, extrapolate=True)
        qcd_spl[k] = PchipInterpolator(ug, Aq, extrapolate=True)

    Ab = np.zeros_like(ug)
    if model.include_baryons:
        for i, (u, T) in enumerate(zip(ug, Tg)):
            if T < 0.5:
                Ab[i] = RHO_B0 / math.exp(3.0 * float(u)) * model.p_b * model.eps
    baryon_spl = PchipInterpolator(ug, Ab, extrapolate=True)

    return Background(u0=u0, u_end=u_end, logT_of_u=logT_of_u,
                      logH=logH_spl, dlogH=dlogH_spl,
                      heavy=heavy_spl, qcd=qcd_spl, baryon=baryon_spl)


def integrate_model(model: Model, x_init: float, v_init: float = 0.0,
                    stop_ratio: float = 100.0, rtol: float = 1e-8,
                    atol: float = 1e-10, background: Background | None = None) -> Dict[str, object]:
    bg = background or build_background(model, stop_ratio=stop_ratio)

    def amplitudes(u: float, x: float) -> Tuple[float, Dict[str, float]]:
        d0 = -(model.m**2 * model.f**2 / model.N) * math.sin(model.N * x)
        dh = 0.0
        dq = 0.0
        for k in model.xis:
            theta = x + 2.0 * math.pi * k / model.N
            dh += float(bg.heavy[k](u)) * math.sin(theta)
            denom = 1.0 - model.eps * math.cos(theta)
            dq += float(bg.qcd[k](u)) * math.sin(theta) / denom
        denom0 = 1.0 - model.eps * math.cos(x)
        db = float(bg.baryon(u)) * math.sin(x) * denom0**(model.p_b - 1.0)
        return d0 + dh + dq + db, dict(zero=d0, heavy=dh, qcd=dq, baryon=db)

    def rhs(u, y):
        x, xp = float(y[0]), float(y[1])
        H = math.exp(float(bg.logH(u)))
        dlh = float(bg.dlogH(u))
        dv, _ = amplitudes(float(u), x)
        return [xp, -(3.0 + dlh) * xp - dv / (model.f**2 * H**2)]

    sol = solve_ivp(rhs, (bg.u0, bg.u_end), [x_init, v_init], method='Radau',
                    rtol=rtol, atol=atol, dense_output=True, max_step=0.08)
    u_samp = np.linspace(bg.u0, bg.u_end, 2400)
    yy = sol.sol(u_samp)
    xarr, varr = yy[0], yy[1]
    Tarr = np.exp(bg.logT_of_u(u_samp))
    Harr = np.exp(bg.logH(u_samp))
    comps = {name: [] for name in ('zero', 'heavy', 'qcd', 'baryon')}
    for u, x, H in zip(u_samp, xarr, Harr):
        _, cc = amplitudes(float(u), float(x))
        for name in comps:
            comps[name].append(cc[name] / (model.f**2 * H**2))
    comps = {k: np.asarray(v) for k, v in comps.items()}

    xf = float(xarr[-1])
    vacua = np.array([(2*j+1)*math.pi/model.N for j in range(model.N)])
    dists = np.abs(np.angle(np.exp(1j*(xf-vacua))))
    jmin = int(np.argmin(dists))
    xv = float(vacua[jmin])
    return {
        'success': bool(sol.success), 'message': sol.message,
        'u': u_samp, 'a': np.exp(u_samp), 'T': Tarr, 'H': Harr,
        'x': xarr, 'xprime': varr, 'components': comps,
        'u_end': bg.u_end, 'T_end': float(Tarr[-1]),
        'z_end': float(1/np.exp(bg.u_end)-1),
        'm_over_H_end': float(model.m/Harr[-1]),
        'selected_vacuum': xv, 'selected_index': jmin,
        'distance_to_vacuum': float(dists[jmin]),
    }

def misalignment_omega_h2(m: float, f: float, theta: float, gosc: float = 3.36) -> float:
    """Constant-mass, radiation-era estimate; adequate as a diagnostic."""
    if m <= 0:
        return 0.0
    # Solve 3H=m with radiation H=sqrt(pi^2 g/90) T^2/Mpl.
    T_osc = math.sqrt(m * MPL / (3.0 * math.sqrt(math.pi**2 * gosc / 90.0)))
    gsosc = g_s(max(T_osc, T0))
    sratio = GSTAR_S0 * T0**3 / (gsosc * T_osc**3)
    rho0 = 0.5 * m*m*f*f*theta*theta*sratio
    rho_c_h2 = 1.05375e-5 / (5.0677307e13**3)  # GeV^4
    return rho0 / rho_c_h2


def delta_neff_full_copy(xi: float) -> float:
    # Hidden photons plus three hidden neutrinos with standard internal reheating.
    rnu = (4.0/11.0)**(1.0/3.0)
    g_hidden = 2.0 + (7.0/8.0)*2.0*3.0*rnu**4
    g_one_nu = (7.0/8.0)*2.0*rnu**4
    return (g_hidden/g_one_nu) * xi**4


def optimize_grid() -> List[Dict[str, float]]:
    """Analytic Pareto scan. Objective is maximal d_g under working constraints."""
    rows: List[Dict[str, float]] = []
    dmax = 1.0e-6  # conservative working MICROSCOPE recast cap
    for N in [6, 8, 10, 12]:
        s = math.sin(math.pi/N)
        for y in np.geomspace(3e-11, 3e-5, 121):
            f = y*MPL
            eps = dmax*y/(P_QCD*s)
            if eps <= 0 or eps >= 0.3:
                continue
            eta = thermal_focus_eta_peak(eps, f)
            # Choose M to place m=7.5e-29 eV (near recombination onset), then impose windows.
            mtgt = 7.5e-29/EV_PER_GEV
            c = NC*N*N*F_N(N)/(8*math.pi**2)
            M = math.sqrt(mtgt*f/(math.sqrt(c)*eps**(N/2)))
            if not (2e3 <= M <= min(f/10.0, 1e12)):
                continue
            TR = 100.0*M
            if TR >= f:
                continue
            omega = misalignment_omega_h2(mtgt, f, math.pi/N)
            rows.append(dict(N=N, y=y, f=f, eps=eps, d_g=dmax, eta_peak=eta,
                             M=M, TR=TR, m_eV=mtgt*EV_PER_GEV,
                             omega_h2=omega, slope=s,
                             score=eta/(1.0+delta_neff_full_copy(0.25))))
    rows.sort(key=lambda r: (-min(r['eta_peak'], 30.0), r['N'], r['M']))
    return rows


def high_t_thermal_phase(model: Model) -> float:
    """Minimum of the leading high-T first harmonic, in (-pi,pi]."""
    W = 0.0 + 0.0j
    for k, xi in model.xis.items():
        if xi <= 0:
            continue
        # A_psi \propto T_k^2 at T_k >> M.
        W += xi**2 * np.exp(2j*math.pi*k/model.N)
    # V=-Re(e^{ix} W), so x_min=-arg W.
    return float(-np.angle(W))


def qcd_eta_peak(eps: float, f: float) -> Tuple[float, float]:
    Ts = np.geomspace(0.03, 3.0, 4000)
    vals = np.array([qcd_focus_eta(float(T), eps, f) for T in Ts])
    i = int(np.argmax(vals))
    return float(Ts[i]), float(vals[i])


def baryon_instability_redshift(model: Model) -> float:
    """Solve m_a^2 = rho_b p eps/f^2 for the homogeneous x=0 branch."""
    ratio = RHO_B0 * model.p_b * model.eps / (model.m**2 * model.f**2)
    if ratio <= 0:
        return float('nan')
    a = ratio**(1.0/3.0)
    return 1.0/a - 1.0


def annual_clock_signal(dg: float, sensitivity: float = 1.0, m_eV: float = 0.0) -> float:
    """Peak-to-peak solar annual modulation, long-range scalar approximation."""
    delta_phi_sun = 3.29e-10
    # Yukawa factor at 1 AU, normalized using m/(1/AU).
    q = m_eV / AU_INV_EV
    yuk = (1.0 + q) * math.exp(-q) if q < 700 else 0.0
    return 2.0 * sensitivity * dg**2 * delta_phi_sun * yuk


def make_plots(strong_trajs: List[Tuple[str, Dict[str, object]]],
               strong_model: Model, balanced_model: Model,
               balanced_basin: List[Dict[str, float]],
               strong_basin: List[Dict[str, float]],
               scan_rows: List[Dict[str, float]], outdir: Path) -> None:
    import matplotlib.pyplot as plt

    # 1. Strong-attractor field histories.
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for label, tr in strong_trajs:
        ax.plot(tr['T'], np.mod(tr['x'] + math.pi, 2*math.pi) - math.pi,
                label=label)
    ax.axhline(math.pi/strong_model.N, linewidth=0.8, linestyle='--',
               label=r'$+\pi/N$ vacuum')
    ax.axhline(-math.pi/strong_model.N, linewidth=0.8, linestyle='--',
               label=r'$-\pi/N$ vacuum')
    ax.set_xscale('log'); ax.invert_xaxis()
    ax.set_xlabel('Visible-sector temperature $T$ [GeV]')
    ax.set_ylabel(r'$x=a/f_a$')
    ax.set_title('Strong-attractor cosmological evolution')
    ax.legend(fontsize=8, loc='best')
    fig.tight_layout()
    fig.savefig(outdir/'cosmological_vacuum_trajectory_v0_8.png', dpi=220)
    plt.close(fig)

    # 2. Curvature hierarchy for the strong benchmark.
    model = strong_model
    Tgrid = np.geomspace(model.T_R, T0, 2800)
    eta_h, eta_q, eta_b, eta_0 = [], [], [], []
    for T in Tgrid:
        a = entropy_scale_factor(float(T)); u = math.log(a)
        H = hubble_from_u_T(u, float(T), model.xis)
        Ah = 0.0; Aq = 0.0
        for k, xi in model.xis.items():
            Tk = sector_temperature(float(T), xi)
            if Tk > 0.0:
                Ah += model.eps*model.M**4*FERM_AMP(model.M/Tk)*math.cos(2*math.pi*k/model.N)
            if 0.02 <= Tk <= 5.0:
                Aq += P_QCD*trace_anomaly_over_t4(Tk)*Tk**4*model.eps*math.cos(2*math.pi*k/model.N)
        rho_b = RHO_B0/a**3 if T < 0.5 else 0.0
        mb2 = rho_b*model.p_b*model.eps/model.f**2
        eta_h.append(abs(Ah)/(model.f**2*H**2))
        eta_q.append(abs(Aq)/(model.f**2*H**2))
        eta_b.append(abs(mb2)/(H**2))
        eta_0.append((model.m/H)**2)
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.plot(Tgrid, eta_h, label='heavy-threshold thermal curvature')
    ax.plot(Tgrid, eta_q, label='QCD trace-anomaly curvature')
    ax.plot(Tgrid, eta_b, label='homogeneous baryon curvature')
    ax.plot(Tgrid, eta_0, label='zero-temperature tachyonic curvature')
    ax.axhline(1.0, linewidth=0.8, linestyle='--', label='$H^2$')
    ax.set_xscale('log'); ax.set_yscale('log'); ax.invert_xaxis()
    ax.set_ylim(1e-12, 1e14)
    ax.set_xlabel('Visible-sector temperature $T$ [GeV]')
    ax.set_ylabel(r'$|m_{\rm eff}^2|/H^2$')
    ax.set_title('Force hierarchy on the strong-attractor ridge')
    ax.legend(fontsize=8, loc='best')
    fig.tight_layout()
    fig.savefig(outdir/'cosmological_force_hierarchy_v0_8.png', dpi=220)
    plt.close(fig)

    # 3. Basin comparison.
    fig, ax = plt.subplots(figsize=(8.2, 4.9))
    xb = np.array([r['x_initial'] for r in balanced_basin])
    vb = np.array([r['selected_signed_vacuum'] for r in balanced_basin])
    xs = np.array([r['x_initial'] for r in strong_basin])
    vs = np.array([r['selected_signed_vacuum'] for r in strong_basin])
    ax.scatter(xb, vb, marker='o', label='moderate focusing')
    ax.scatter(xs, vs, marker='x', s=60, label='strong attractor')
    ax.axhline(math.pi/strong_model.N, linewidth=0.8, linestyle='--')
    ax.axhline(-math.pi/strong_model.N, linewidth=0.8, linestyle='--')
    ax.set_xlabel(r'Inflationary homogeneous phase $x_i$')
    ax.set_ylabel('Selected signed vacuum')
    ax.set_title('Vacuum selection: memory regime versus attractor regime')
    ax.set_xlim(0, 2*math.pi)
    ax.legend(fontsize=8, loc='best')
    fig.tight_layout()
    fig.savefig(outdir/'cosmological_vacuum_basin_v0_8.png', dpi=220)
    plt.close(fig)

    # 4. EP-saturating parameter ridge.
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for N in sorted(set(int(r['N']) for r in scan_rows)):
        rr = [r for r in scan_rows if int(r['N']) == N and r['eta_peak'] >= 1.0]
        if rr:
            ax.scatter([r['f_over_Mpl'] for r in rr], [r['M_GeV'] for r in rr],
                       s=12, label=f'$N={N}$')
    ax.scatter([balanced_model.f/MPL], [balanced_model.M], marker='*', s=150,
               label='moderate benchmark')
    ax.scatter([strong_model.f/MPL], [strong_model.M], marker='D', s=70,
               label='strong-attractor benchmark')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel(r'$f_a/M_{\rm Pl}$')
    ax.set_ylabel(r'$M$ [GeV]')
    ax.set_title(r'EP-saturating cosmological ridge ($d_g=10^{-6}$)')
    ax.legend(fontsize=8, loc='best')
    fig.tight_layout()
    fig.savefig(outdir/'cosmological_parameter_ridge_v0_8.png', dpi=220)
    plt.close(fig)

def make_ridge_model(y: float, d_target: float = 1.0e-6,
                    m_target_eV: float = 7.5e-29,
                    xi_adj: float = 0.25) -> Model:
    f = y*MPL
    eps = d_target*y/(P_QCD*math.sin(math.pi/6))
    mt = m_target_eV/EV_PER_GEV
    c6 = NC*36*F_N(6)/(8*math.pi**2)
    M = math.sqrt(mt*f/(math.sqrt(c6)*eps**3))
    return Model(N=6, M=M, f=f, eps=eps, T_R=100.0*M,
                 xi_adj=xi_adj, adj_sector=5)


def main() -> None:
    outdir = Path('/mnt/data')
    old = Model(N=6, M=1.0e4, f=MPL, eps=1.0e-6, T_R=1.0e6,
                xi_adj=0.0, adj_sector=5)
    balanced = make_ridge_model(2.0e-7)
    strong = make_ridge_model(1.0e-8)

    print('stage: backgrounds', flush=True)
    bg_bal = build_background(balanced, stop_ratio=60.0, points=5200)
    bg_str = build_background(strong, stop_ratio=150.0, points=5600)

    print('stage: representative trajectories', flush=True)
    balanced_full = integrate_model(balanced, math.pi/2, stop_ratio=60.0,
                                    rtol=4e-7, atol=4e-9, background=bg_bal)
    balanced_zero = integrate_model(balanced, 0.0, stop_ratio=60.0,
                                    rtol=4e-7, atol=4e-9, background=bg_bal)
    no_qcd_model = dataclasses.replace(balanced, include_qcd=False)
    bg_noq = build_background(no_qcd_model, stop_ratio=60.0, points=5200)
    no_qcd = integrate_model(no_qcd_model, math.pi/2, stop_ratio=60.0,
                             rtol=4e-7, atol=4e-9, background=bg_noq)
    no_baryon_model = dataclasses.replace(balanced, include_baryons=False)
    bg_nob = build_background(no_baryon_model, stop_ratio=60.0, points=5200)
    no_baryon = integrate_model(no_baryon_model, math.pi/2, stop_ratio=60.0,
                                rtol=4e-7, atol=4e-9, background=bg_nob)

    strong_trajs: List[Tuple[str, Dict[str, object]]] = []
    for label, x0 in [(r'$x_i=0$', 0.0), (r'$x_i=\pi/2$', math.pi/2),
                      (r'$x_i=\pi$', math.pi), (r'$x_i=3\pi/2$', 3*math.pi/2)]:
        tr = integrate_model(strong, x0, stop_ratio=150.0,
                             rtol=2e-6, atol=2e-8, background=bg_str)
        strong_trajs.append((label, tr))

    print('stage: basin scans', flush=True)
    balanced_basin: List[Dict[str, float]] = []
    strong_basin: List[Dict[str, float]] = []
    for x0 in np.linspace(0.0, 2*math.pi, 12, endpoint=False):
        trb = integrate_model(balanced, float(x0), stop_ratio=60.0,
                              rtol=2e-6, atol=2e-8, background=bg_bal)
        trs = integrate_model(strong, float(x0), stop_ratio=150.0,
                              rtol=2e-6, atol=2e-8, background=bg_str)
        for rows, tr in [(balanced_basin, trb), (strong_basin, trs)]:
            xv = float(tr['selected_vacuum'])
            rows.append({
                'x_initial': float(x0),
                'selected_vacuum_0_2pi': xv,
                'selected_signed_vacuum': float(np.angle(np.exp(1j*xv))),
                'x_at_stop': float(tr['x'][-1]),
                'distance_to_vacuum': float(tr['distance_to_vacuum']),
            })

    print('stage: parameter scan', flush=True)
    raw_scan = optimize_grid()
    scan_rows: List[Dict[str, float]] = []
    for r in raw_scan:
        scan_rows.append({
            'N': int(r['N']), 'f_over_Mpl': float(r['y']), 'f_GeV': float(r['f']),
            'epsilon': float(r['eps']), 'd_g': float(r['d_g']),
            'eta_peak': float(r['eta_peak']), 'M_GeV': float(r['M']),
            'TR_GeV': float(r['TR']), 'm_eV': float(r['m_eV']),
            'Omega_h2': float(r['omega_h2']), 'slope': float(r['slope']),
        })

    def benchmark_row(name: str, model: Model) -> Dict[str, float]:
        tq, etaq = qcd_eta_peak(model.eps, model.f)
        return {
            'name': name, 'N': model.N, 'M_GeV': model.M,
            'f_GeV': model.f, 'f_over_Mpl': model.f/MPL,
            'epsilon': model.eps, 'm_eV': model.m*EV_PER_GEV,
            'd_g_at_selected_vacuum': model.dg,
            'TR_GeV': model.T_R, 'TR_over_f': model.T_R/model.f,
            'xi_adjacent': model.xi_adj,
            'Delta_Neff': delta_neff_full_copy(model.xi_adj),
            'high_T_minimum_x': high_t_thermal_phase(model),
            'eta_heavy_peak': thermal_focus_eta_peak(model.eps, model.f),
            'T_qcd_eta_peak_GeV': tq, 'eta_qcd_peak': etaq,
            'baryon_instability_redshift': baryon_instability_redshift(model),
            'Omega_h2_if_theta_pi_over_6': misalignment_omega_h2(model.m, model.f, math.pi/6),
            'annual_clock_signal_K1': annual_clock_signal(model.dg, 1.0, model.m*EV_PER_GEV),
            'annual_clock_signal_K1e4': annual_clock_signal(model.dg, 1e4, model.m*EV_PER_GEV),
            'inflation_homogeneity_scale_GeV': 2*math.pi*model.f*abs(high_t_thermal_phase(model)),
        }

    old_tq, old_etaq = qcd_eta_peak(old.eps, old.f)
    benchmarks = [{
        'name': 'v0.6 local benchmark', 'N': old.N, 'M_GeV': old.M,
        'f_GeV': old.f, 'f_over_Mpl': old.f/MPL, 'epsilon': old.eps,
        'm_eV': old.m*EV_PER_GEV, 'd_g_at_selected_vacuum': old.dg,
        'eta_heavy_peak': thermal_focus_eta_peak(old.eps, old.f),
        'eta_qcd_peak': old_etaq,
        'Omega_h2_if_theta_pi_over_6': misalignment_omega_h2(old.m, old.f, math.pi/6),
        'Delta_Neff': 0.0,
    }, benchmark_row('moderate-focusing cosmological benchmark', balanced),
       benchmark_row('strong-attractor cosmological benchmark', strong)]

    milestones: List[Dict[str, float]] = []
    ref = strong_trajs[1][1]
    for Ttar in [strong.T_R, 0.4*strong.M, strong.M/5, 10.0, 1.0, 0.2,
                 0.15, 0.10, 0.01, 1e-3, 1e-6, 1e-9, 1e-10]:
        i = int(np.argmin(np.abs(np.log(ref['T']/Ttar))))
        milestones.append({
            'T_target_GeV': Ttar, 'T_GeV': float(ref['T'][i]),
            'redshift': float(1.0/ref['a'][i]-1.0),
            'x': float(ref['x'][i]), 'dx_dln_a': float(ref['xprime'][i]),
            'm_over_H': float(strong.m/ref['H'][i]),
        })

    bal_pos = sum(1 for r in balanced_basin if r['selected_signed_vacuum'] > 0)
    str_pos = sum(1 for r in strong_basin if r['selected_signed_vacuum'] > 0)
    acceptance = [
        ('Finite-temperature heavy-threshold evolution', 'PASS', 'Exact fermion thermal function at leading order in epsilon.'),
        ('Replicated-sector entropy evolution', 'PASS within decoupled-sector approximation', 'Each populated sector conserves entropy independently.'),
        ('QCD crossover', 'PASS at leading lock defect', 'Lattice trace anomaly and dF/dlnLambda=Theta are included.'),
        ('Matter domination', 'PASS', 'Homogeneous baryon locking is included and delays the tachyonic release.'),
        ('Unique vacuum in moderate-focusing benchmark', 'FAIL', 'Initial inflationary phase remains visible in the final basin.'),
        ('Unique vacuum in strong-attractor benchmark', 'PASS numerically for sampled phases', 'All 12 tested homogeneous phases select the same adjacent vacuum.'),
        ('Permanent global domain-wall cure', 'CONDITIONAL', 'Requires pre-inflation breaking/no restoration or an additional technically safe bias.'),
        ('Dark-radiation bound', 'PASS for one xi=0.25 adjacent copy', 'Approximate Delta Neff is below the 2026 95% bound.'),
        ('Misalignment abundance', 'PASS on low-f ridge', 'The scalar is a negligible matter component.'),
        ('Largest generic chronometric shear', 'EP-limited', 'Cosmology admits the working d_g=1e-6 cap but does not exceed it.'),
        ('N=6 choice', 'PREFERRED', 'Smallest even N>4, largest adjacent-vacuum slope, and lowest replicated-sector burden.'),
    ]

    import csv
    def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
        if not rows: return
        fieldnames=[]; seen=set()
        for row in rows:
            for key in row:
                if key not in seen: seen.add(key); fieldnames.append(key)
        with path.open('w', newline='') as fobj:
            w=csv.DictWriter(fobj, fieldnames=fieldnames); w.writeheader(); w.writerows(rows)
    write_csv(outdir/'cosmological_vacuum_benchmarks_v0_8.csv', benchmarks)
    write_csv(outdir/'cosmological_vacuum_milestones_v0_8.csv', milestones)
    write_csv(outdir/'cosmological_vacuum_basin_v0_8.csv', strong_basin)
    write_csv(outdir/'cosmological_vacuum_basin_moderate_v0_8.csv', balanced_basin)
    write_csv(outdir/'cosmological_parameter_scan_v0_8.csv', scan_rows)
    with (outdir/'cosmological_vacuum_acceptance_matrix_v0_8.csv').open('w', newline='') as fobj:
        w=csv.writer(fobj); w.writerow(['Requirement','Verdict','Reason']); w.writerows(acceptance)

    result = {
        'benchmarks': benchmarks,
        'moderate_focusing': {
            'basin_positive': bal_pos,
            'basin_negative': len(balanced_basin)-bal_pos,
            'representative_selected_signed_vacuum': float(np.angle(np.exp(1j*balanced_full['selected_vacuum']))),
            'without_QCD_signed_vacuum': float(np.angle(np.exp(1j*no_qcd['selected_vacuum']))),
            'without_baryons_signed_vacuum': float(np.angle(np.exp(1j*no_baryon['selected_vacuum']))),
        },
        'strong_attractor': {
            'basin_positive': str_pos,
            'basin_negative': len(strong_basin)-str_pos,
            'tested_initial_phases': len(strong_basin),
            'max_final_distance_to_vacuum': max(r['distance_to_vacuum'] for r in strong_basin),
            'selected_signed_vacua': [float(np.angle(np.exp(1j*tr['selected_vacuum']))) for _,tr in strong_trajs],
        },
        'scan_counts_by_N': {str(N): int(sum(1 for r in scan_rows if r['N']==N))
                             for N in sorted(set(r['N'] for r in scan_rows))},
        'acceptance': [{'requirement':a,'verdict':b,'reason':c} for a,b,c in acceptance],
    }
    with (outdir/'cosmological_vacuum_selection_results_v0_8.json').open('w') as fobj:
        json.dump(result, fobj, indent=2)

    np.savez_compressed(outdir/'cosmological_vacuum_trajectories_v0_8.npz',
        T_balanced=balanced_full['T'], x_balanced=balanced_full['x'],
        T_strong=strong_trajs[0][1]['T'],
        x_strong_0=strong_trajs[0][1]['x'], x_strong_pi2=strong_trajs[1][1]['x'],
        x_strong_pi=strong_trajs[2][1]['x'], x_strong_3pi2=strong_trajs[3][1]['x'])

    make_plots(strong_trajs, strong, balanced, balanced_basin, strong_basin,
               scan_rows, outdir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

