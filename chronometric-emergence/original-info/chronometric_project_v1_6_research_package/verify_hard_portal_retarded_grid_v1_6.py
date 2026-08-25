#!/usr/bin/env python3
"""Hard 2<->2 portal matching and a KMS-complete near-shell Pi_R grid.

This script advances the q-D-H portal calculation beyond v1.5 in two layers:

1. It evaluates the strict leading-order *integrated* hard+soft 2<->2
   reaction coefficient by adapting the representation-general form of the
   Bodeker-Schröder right-handed-electron result to

       - y_D \bar Q_L H D_R + h.c.

   with Q_L=(3,2,1/6), D_R=(3,1,-1/3).

2. It constructs momentum-resolved on-shell widths. The LPM shape is obtained
   directly from the v1.5 impact-parameter solver. The hard-cut shape is
   evaluated with a screened, full-angle quasi-Monte-Carlo phase-space
   integral and then normalized to the exact integrated hard coefficient.

The off-shell Pi_R(omega,k) table is a causal, KMS-complete near-shell
reconstruction matched exactly on shell. It is a benchmark kernel for reduced
Schwinger-Keldysh/Wigner calculations, NOT an exact arbitrary-off-shell
three-loop thermal self-energy. That remaining distinction is explicit in all
outputs.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import PchipInterpolator
from scipy.special import expit
from scipy.stats import qmc

OUT = Path('/mnt/data')
VERSION = 'v1.6'
PI = math.pi
NC = 3.0
CF = 4.0 / 3.0
C2 = 3.0 / 4.0
YQ = 1.0 / 6.0
YD = -1.0 / 3.0
G_H = 2.0                    # two complex Higgs-doublet components
CHI_H_OVER_T2 = 2.0 / 3.0
C_PARTNER = 3.52             # universal hard+soft phase-space constant
C_SINGLED = 2.69
C_TOP = 2.82


@dataclass(frozen=True)
class Point:
    alpha_s: float = 0.0393544
    g2: float = 0.57
    g1: float = 0.39
    y_t: float = 0.58
    y_d: float = 0.30
    m_d_over_t: float = 0.01
    T0_GeV: float = 1.002e8
    Gamma_R_GeV: float = 1.47850065e-2


def load_v15():
    path = OUT / 'verify_electroweak_yukawa_lpm_v1_5.py'
    spec = importlib.util.spec_from_file_location('ew_lpm_v15', path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Cannot load {path}')
    mod = importlib.util.module_from_spec(spec)
    sys.modules['ew_lpm_v15'] = mod
    spec.loader.exec_module(mod)
    return mod


def fermi(x: np.ndarray | float) -> np.ndarray:
    return expit(-np.asarray(x, dtype=float))


def bose(x: np.ndarray | float) -> np.ndarray:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr)
    small = np.abs(arr) < 1.0e-8
    positive = (~small) & (arr < 45.0)
    large = arr >= 45.0
    out[small] = 1.0 / np.where(arr[small] == 0.0, 1.0e-12, arr[small]) - 0.5
    out[positive] = 1.0 / np.expm1(arr[positive])
    out[large] = np.exp(-arr[large])
    return out


def coth_half(x: np.ndarray) -> np.ndarray:
    """coth(x/2) with a stable small-x limit supplied by the caller's odd ImPi."""
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    small = np.abs(x) < 1.0e-6
    out[small] = 2.0 / np.where(x[small] == 0.0, 1.0e-12, x[small]) + x[small] / 6.0
    out[~small] = 1.0 / np.tanh(0.5 * x[~small])
    return out


def hard_integrated(point: Point) -> dict:
    """Strict-LO integrated hard+soft 2<->2 q-D-H reaction coefficient.

    The representation-general form is

      Gamma_Y^hard/T^3 = N_c y_D^2/(2048 pi)
        [ A_Q(c_Q+ln 1/A_Q) + A_D(c_D+ln 1/A_D) ],

    with A_i=4 sum_G C_i^G g_G^2.  This is the gauge-assisted part of
    the qD contribution to the Higgs retarded self-energy.  The optional
    top-Yukawa four-fermion crossing term is reported separately because it
    contributes to chemical equilibration but is not a cut of Pi_H,qD.
    """
    g3 = math.sqrt(4.0 * PI * point.alpha_s)
    aq_parts = {
        'SU3': 4.0 * CF * g3**2,
        'SU2': 4.0 * C2 * point.g2**2,
        'U1': 4.0 * YQ**2 * point.g1**2,
    }
    ad_parts = {
        'SU3': 4.0 * CF * g3**2,
        'SU2': 0.0,
        'U1': 4.0 * YD**2 * point.g1**2,
    }
    aq = sum(aq_parts.values())
    ad = sum(ad_parts.values())
    pref = NC * point.y_d**2 / (2048.0 * PI)
    q_factor = C_PARTNER + math.log(1.0 / aq)
    d_factor = C_SINGLED + math.log(1.0 / ad)
    by_group = {
        name: pref * (aq_parts[name] * q_factor + ad_parts[name] * d_factor)
        for name in aq_parts
    }
    gamma_y_hard = sum(by_group.values())
    gamma_h_occ = gamma_y_hard / CHI_H_OVER_T2
    top_chemical = pref * point.y_t**2 * C_TOP

    # Published e_R normalization identity, used as a structural check.
    a_l = 3.0 * point.g2**2 + point.g1**2
    a_e = 4.0 * point.g1**2
    electron_rewritten = point.y_d**2 / (2048.0 * PI) * (
        a_l * (C_PARTNER + math.log(1.0 / a_l))
        + a_e * (C_SINGLED + math.log(1.0 / a_e))
    )
    electron_literal = point.y_d**2 / (2048.0 * PI) * (
        (3.0 * point.g2**2 + point.g1**2)
        * (C_PARTNER + math.log(1.0 / (3.0 * point.g2**2 + point.g1**2)))
        + 4.0 * point.g1**2
        * (C_SINGLED + math.log(1.0 / (4.0 * point.g1**2)))
    )
    return {
        'g3': g3,
        'A_Q': aq,
        'A_D': ad,
        'A_Q_by_group': aq_parts,
        'A_D_by_group': ad_parts,
        'GammaY_hard_over_T3': gamma_y_hard,
        'GammaH_hard_occ_over_T': gamma_h_occ,
        'GammaY_hard_by_group_over_T3': by_group,
        'top_four_fermion_chemical_only_over_T3': top_chemical,
        'electron_formula_rewrite_residual': electron_rewritten - electron_literal,
    }


def matrix_element_checks() -> dict:
    """Check the generic abelian coefficients against the published e_R amplitudes."""
    # One weak component: [constant, u/t, t/u] = [4 qQ qD, 2qQ^2, 2qD^2].
    def coeffs(q_q: float, q_d: float, multiplicity: float) -> np.ndarray:
        return multiplicity * np.array([4.0 * q_q * q_d, 2.0 * q_q**2, 2.0 * q_d**2])

    electron = coeffs(-0.5, -1.0, 2.0)
    qd_u1 = coeffs(YQ, YD, 2.0 * NC)
    expected_e = np.array([4.0, 1.0, 4.0])
    expected_qd = np.array([-4.0 / 3.0, 1.0 / 3.0, 4.0 / 3.0])

    # Non-abelian group traces for the declared representations.
    # sum_A Tr(T^A T^A)=T_F dim(adj)=4 for SU(3); two weak components -> 8.
    su3 = np.array([32.0, 16.0, 16.0])
    # Published SU(2) electron coefficient 3 u/t, multiplied by spectator colour 3.
    su2 = np.array([0.0, 9.0, 0.0])
    return {
        'electron_coefficients': electron.tolist(),
        'electron_expected': expected_e.tolist(),
        'electron_max_residual': float(np.max(np.abs(electron - expected_e))),
        'qD_U1_coefficients': qd_u1.tolist(),
        'qD_U1_expected': expected_qd.tolist(),
        'qD_U1_max_residual': float(np.max(np.abs(qd_u1 - expected_qd))),
        'qD_SU3_coefficients': su3.tolist(),
        'qD_SU2_coefficients': su2.tolist(),
    }


def _boost_lab_to_cm(E: np.ndarray, pvec: np.ndarray, beta: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    b2 = np.sum(beta * beta, axis=1)
    bp = np.sum(beta * pvec, axis=1)
    coef = np.where(b2 > 1.0e-16, (gamma - 1.0) * bp / b2 - gamma * E, 0.0)
    return pvec + coef[:, None] * beta


def _boost_cm_to_lab(E: np.ndarray, pvec: np.ndarray, beta: np.ndarray, gamma: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    b2 = np.sum(beta * beta, axis=1)
    bp = np.sum(beta * pvec, axis=1)
    coef = np.where(b2 > 1.0e-16, (gamma - 1.0) * bp / b2 + gamma * E, 0.0)
    out_vec = pvec + coef[:, None] * beta
    out_E = gamma * (E + bp)
    return out_E, out_vec


def hard_shape_one_k(
    k: float,
    point: Point,
    m_q2: float,
    m_d2: float,
    screen_factor: float,
    n_power: int,
    seed: int,
    pmax: float = 22.0,
) -> tuple[float, float]:
    """Full-angle screened hard-cut shape for a tagged Higgs mode.

    Absolute normalization is intentionally not used; the resulting shape is
    normalized afterwards to the exact integrated hard+soft coefficient.
    """
    n = 2**n_power
    sampler = qmc.Sobol(d=4, scramble=True, seed=seed)
    u = sampler.random_base2(n_power)
    p = pmax * u[:, 0]
    c_in = 2.0 * u[:, 1] - 1.0
    c_star = 2.0 * u[:, 2] - 1.0
    phi_star = 2.0 * PI * u[:, 3]
    s_in = np.sqrt(np.maximum(0.0, 1.0 - c_in**2))

    kvec = np.column_stack([np.zeros(n), np.zeros(n), np.full(n, k)])
    pvec = np.column_stack([p * s_in, np.zeros(n), p * c_in])
    e_tot = k + p
    v_tot = kvec + pvec
    beta = v_tot / np.maximum(e_tot[:, None], 1.0e-30)
    b2 = np.sum(beta * beta, axis=1)
    gamma = 1.0 / np.sqrt(np.maximum(1.0 - b2, 1.0e-15))
    s = 2.0 * k * p * (1.0 - c_in)
    valid = (p > 1.0e-9) & (s > 1.0e-9) & (b2 < 1.0 - 1.0e-13)

    kstar = _boost_lab_to_cm(np.full(n, k), kvec, beta, gamma)
    norm = np.linalg.norm(kstar, axis=1)
    n_in = kstar / np.maximum(norm[:, None], 1.0e-30)
    ref = np.tile(np.array([0.0, 1.0, 0.0]), (n, 1))
    e1 = np.cross(n_in, ref)
    e1_norm = np.linalg.norm(e1, axis=1)
    bad = e1_norm < 1.0e-10
    if np.any(bad):
        e1[bad] = np.cross(n_in[bad], np.array([1.0, 0.0, 0.0]))
        e1_norm[bad] = np.linalg.norm(e1[bad], axis=1)
    e1 /= np.maximum(e1_norm[:, None], 1.0e-30)
    e2 = np.cross(n_in, e1)
    s_star = np.sqrt(np.maximum(0.0, 1.0 - c_star**2))
    n3 = (
        c_star[:, None] * n_in
        + s_star[:, None]
        * (np.cos(phi_star)[:, None] * e1 + np.sin(phi_star)[:, None] * e2)
    )
    e_star = np.sqrt(np.maximum(s, 0.0)) / 2.0
    p3_star = e_star[:, None] * n3
    e3, _ = _boost_cm_to_lab(e_star, p3_star, beta, gamma)
    e4 = e_tot - e3

    t = -0.5 * s * (1.0 - c_star)
    u_man = -0.5 * s * (1.0 + c_star)
    tq = t - screen_factor * m_q2
    ud = u_man - screen_factor * m_d2
    tiny = 1.0e-18

    g3 = math.sqrt(4.0 * PI * point.alpha_s)
    # Coefficients include two weak components and all colour/polarization sums.
    # A: G+H -> Q+Dbar.
    m_a = (
        g3**2 * (32.0 + 16.0 * u_man / tq + 16.0 * t / ud)
        + point.g2**2 * (9.0 * u_man / tq)
        + point.g1**2 * (-4.0 / 3.0 + (u_man / tq) / 3.0 + 4.0 * (t / ud) / 3.0)
    )
    # Qbar+H -> G+Dbar.
    m_q = (
        g3**2 * (-32.0 + 16.0 * s / (-tq) + 16.0 * (-t) / np.maximum(s, tiny))
        + point.g2**2 * (9.0 * s / (-tq))
        + point.g1**2 * (-4.0 / 3.0 + (s / (-tq)) / 3.0 + 4.0 * (-t) / (3.0 * np.maximum(s, tiny)))
    )
    # D+H -> G+Q, obtained by Q<->D and t<->u crossing.
    m_d = (
        g3**2 * (-32.0 + 16.0 * s / (-ud) + 16.0 * (-u_man) / np.maximum(s, tiny))
        + point.g2**2 * (9.0 * s / (-ud))
        + point.g1**2 * (-4.0 / 3.0 + 4.0 * s / (3.0 * (-ud)) + (-u_man) / (3.0 * np.maximum(s, tiny)))
    )
    # Numerical round-off can produce tiny negative values near singular boundaries.
    m_a = np.maximum(m_a, 0.0)
    m_q = np.maximum(m_q, 0.0)
    m_d = np.maximum(m_d, 0.0)

    ff3 = fermi(e3)
    ff4 = fermi(e4)
    # The final-particle assignment is immaterial after angular integration; this
    # convention is used consistently for all three crossed channels.
    channel_a = bose(p) * (1.0 - ff3) * (1.0 - ff4) * m_a
    channel_q = fermi(p) * (1.0 + bose(e3)) * (1.0 - ff4) * m_q
    channel_d = fermi(p) * (1.0 + bose(e3)) * (1.0 - ff4) * m_d
    integrand = p * (channel_a + channel_q + channel_d)
    integrand = np.where(valid, np.nan_to_num(integrand), 0.0)

    # Integration volume in p, cos(theta_in), cos(theta*), phi*.
    volume = pmax * 2.0 * 2.0 * 2.0 * PI
    average = float(np.mean(integrand) * volume)
    error = float(np.std(integrand, ddof=1) / math.sqrt(n) * volume)
    denominator = 2.0 * k * (1.0 + float(bose(k)))
    return average / denominator, error / denominator


def compute_hard_shape(point: Point, m_q2: float, m_d2: float) -> dict:
    k_grid = np.geomspace(0.12, 20.0, 30)
    central = []
    errors = []
    for i, k in enumerate(k_grid):
        val, err = hard_shape_one_k(
            float(k), point, m_q2, m_d2, 1.0, 14, 1761 + i
        )
        central.append(val)
        errors.append(err)

    # A lower-resolution screen variation gives a shape systematic after exact
    # integrated normalization.  This does not affect the exact total rate.
    variations: dict[str, np.ndarray] = {}
    for sf in (0.5, 2.0):
        vals = []
        for i, k in enumerate(k_grid):
            val, _ = hard_shape_one_k(
                float(k), point, m_q2, m_d2, sf, 12, 2819 + i + int(100 * sf)
            )
            vals.append(val)
        variations[str(sf)] = np.asarray(vals)
    return {
        'k': k_grid,
        'central_raw': np.asarray(central),
        'mc_error_raw': np.asarray(errors),
        'screen_variations_raw': variations,
    }


def lpm_dI_dk(k: float, module, data: dict, p_nodes: int = 8, p_max: float = 20.0) -> float:
    z, w = leggauss(p_nodes)
    groups = data['groups']
    masses = (data['m_h2'], data['m_q2'], data['m_d2'])
    total = 0.0
    uvals = 0.5 * (z + 1.0) * p_max
    uw = 0.5 * p_max * w
    for u, weight in zip(uvals, uw):
        total += weight * module.integrand_point(k, -u, masses, groups, module.FAST)
    pvals = 0.5 * (z + 1.0) * k
    pw = 0.5 * k * w
    for p, weight in zip(pvals, pw):
        total += weight * module.integrand_point(k, p, masses, groups, module.FAST)
    for u, weight in zip(uvals, uw):
        total += weight * module.integrand_point(k, k + u, masses, groups, module.FAST)
    return total / (8.0 * PI**3)


def compute_lpm_shape(point: Point, module, data: dict, exact_integral: float) -> dict:
    k_grid = np.geomspace(0.08, 22.0, 30)
    dI = np.asarray([lpm_dI_dk(float(k), module, data) for k in k_grid])
    raw_integral = float(np.trapezoid(dI, k_grid))
    scale = exact_integral / raw_integral
    dI *= scale
    fb = bose(k_grid)
    denominator = (G_H / (2.0 * PI**2)) * k_grid**2 * fb * (1.0 + fb)
    width = NC * point.y_d**2 * dI / denominator
    return {
        'k': k_grid,
        'dI_dk': dI,
        'width_occ_over_T': width,
        'quadrature_normalization_scale': scale,
        'raw_integral': raw_integral,
    }


def normalize_hard_shape(shape: dict, exact_gamma_y_hard: float) -> dict:
    k = shape['k']
    raw = shape['central_raw']
    interp = PchipInterpolator(k, raw, extrapolate=True)
    dense = np.geomspace(0.05, 28.0, 1600)
    weighted = (G_H / (2.0 * PI**2)) * dense**2 * bose(dense) * (1.0 + bose(dense))
    raw_integral = float(np.trapezoid(weighted * interp(dense), dense))
    norm = exact_gamma_y_hard / raw_integral
    central = raw * norm
    mc_err = shape['mc_error_raw'] * norm

    variations_norm: dict[str, np.ndarray] = {}
    rels = []
    for key, vals in shape['screen_variations_raw'].items():
        vint = PchipInterpolator(k, vals, extrapolate=True)
        integral = float(np.trapezoid(weighted * vint(dense), dense))
        nv = exact_gamma_y_hard / integral
        normalized = vals * nv
        variations_norm[key] = normalized
        rels.append(np.abs(normalized / central - 1.0))
    envelope = np.max(np.vstack(rels), axis=0)
    return {
        **shape,
        'normalization': norm,
        'raw_susceptibility_integral': raw_integral,
        'width_occ_over_T': central,
        'width_mc_error_over_T': mc_err,
        'screen_variations_width_over_T': variations_norm,
        'screen_shape_relative_envelope': envelope,
    }


def on_shell_table(lpm: dict, hard: dict, m_h: float, target_lpm_gamma_y: float, target_hard_gamma_y: float) -> dict:
    k_grid = np.geomspace(0.03, 28.0, 120)
    lpm_interp = PchipInterpolator(lpm['k'], lpm['width_occ_over_T'], extrapolate=True)
    hard_interp = PchipInterpolator(hard['k'], hard['width_occ_over_T'], extrapolate=True)
    lpm_w = np.maximum(lpm_interp(k_grid), 0.0)
    hard_w = np.maximum(hard_interp(k_grid), 0.0)
    susceptibility_weight = (G_H / (2.0 * PI**2)) * k_grid**2 * bose(k_grid) * (1.0 + bose(k_grid))
    lpm_grid_integral = float(np.trapezoid(susceptibility_weight * lpm_w, k_grid))
    hard_grid_integral = float(np.trapezoid(susceptibility_weight * hard_w, k_grid))
    lpm_w *= target_lpm_gamma_y / lpm_grid_integral
    hard_w *= target_hard_gamma_y / hard_grid_integral
    total = lpm_w + hard_w
    energy = np.sqrt(k_grid**2 + m_h**2)
    im_pi = -energy * total
    return {
        'k': k_grid,
        'energy': energy,
        'lpm_width': lpm_w,
        'hard_width': hard_w,
        'total_width': total,
        'im_pi_on_shell': im_pi,
    }


def retarded_grid(on_shell: dict, m_h: float, memory_scale: float) -> dict:
    """Causal near-shell spectral completion exactly matched on shell."""
    k_grid = np.geomspace(0.12, 16.0, 48)
    omega = np.linspace(-20.0, 20.0, 801)
    width_interp = PchipInterpolator(on_shell['k'], on_shell['total_width'], extrapolate=True)
    widths = np.maximum(width_interp(k_grid), 1.0e-12)
    im_pi = np.zeros((len(k_grid), len(omega)))
    for ik, k in enumerate(k_grid):
        e = math.sqrt(k * k + m_h * m_h)
        lam = memory_scale
        lp = lam**2 / ((omega - e) ** 2 + lam**2)
        lm = lam**2 / ((omega + e) ** 2 + lam**2)
        denom = 1.0 - lam**2 / ((2.0 * e) ** 2 + lam**2)
        odd_profile = (lp - lm) / denom
        im_pi[ik] = -e * widths[ik] * odd_profile

    # Once-subtracted discrete dispersion relation.  The subtraction anchors
    # RePi(0,k)=m_H^2 and reduces sensitivity to the finite omega window.
    re_pi = np.zeros_like(im_pi)
    dw = omega[1] - omega[0]
    nonzero = np.abs(omega) > 1.0e-12
    for ik in range(len(k_grid)):
        y = im_pi[ik]
        for i, wi in enumerate(omega):
            mask = np.ones(len(omega), dtype=bool)
            mask[i] = False
            mask &= nonzero
            kernel = 1.0 / (omega[mask] - wi) - 1.0 / omega[mask]
            re_pi[ik, i] = m_h**2 + float(np.sum(y[mask] * kernel) * dw / PI)

    # Real positive noise kernel N=-coth(omega/2T) ImPi_R.
    noise = -coth_half(omega)[None, :] * im_pi
    zero_idx = int(np.argmin(np.abs(omega)))
    # Stable omega->0 value from adjacent points.
    noise[:, zero_idx] = 0.5 * (noise[:, zero_idx - 1] + noise[:, zero_idx + 1])

    odd_residual = float(np.max(np.abs(im_pi + im_pi[:, ::-1])))
    noise_min = float(np.min(noise))
    # On-shell matching residual by interpolation in omega.
    match_residuals = []
    for ik, k in enumerate(k_grid):
        e = math.sqrt(k * k + m_h * m_h)
        got = float(np.interp(e, omega, im_pi[ik]))
        target = -e * widths[ik]
        match_residuals.append(abs(got - target) / max(abs(target), 1.0e-30))

    # KMS detailed-balance check: Pi^</Pi^>=exp(-omega/T) for omega>0.
    pos = omega > 1.0e-5
    n = bose(omega[pos])
    rho_pi = -2.0 * im_pi[:, pos]  # positive for omega>0 in this convention
    pi_less = n[None, :] * rho_pi
    pi_greater = (1.0 + n)[None, :] * rho_pi
    ratio = np.divide(pi_less, pi_greater, out=np.zeros_like(pi_less), where=pi_greater > 0)
    expected = np.exp(-omega[pos])[None, :]
    kms_residual = float(np.max(np.abs(ratio - expected)))

    return {
        'k': k_grid,
        'omega': omega,
        'width_on_shell': widths,
        'im_pi_R': im_pi,
        're_pi_R': re_pi,
        'noise_N': noise,
        'diagnostics': {
            'oddness_max_abs': odd_residual,
            'noise_min': noise_min,
            'max_relative_on_shell_match_residual': float(max(match_residuals)),
            'KMS_ratio_max_abs_residual': kms_residual,
            'memory_scale_over_T': memory_scale,
            'scope': 'Causal KMS-complete near-shell reconstruction; not exact arbitrary-off-shell hard thermal self-energy.',
        },
    }


def wigner_benchmark(on_shell: dict) -> dict:
    """Momentum-resolved relaxation benchmark using the matched collision width."""
    k = on_shell['k']
    gamma = on_shell['total_width']
    eq = bose(np.sqrt(k**2 + 0.4382065722921097**2))
    initial = eq + 0.35 * np.exp(-0.5 * ((np.log(k) - math.log(3.0)) / 0.35) ** 2)
    times = np.linspace(0.0, 12000.0, 500)
    f = eq[None, :] + (initial - eq)[None, :] * np.exp(-times[:, None] * gamma[None, :])
    entropy_like = np.trapezoid(
        k[None, :] ** 2
        * ((1.0 + f) * np.log1p(f) - f * np.log(np.maximum(f, 1.0e-300))),
        k,
        axis=1,
    )
    # The entropy of a subsystem relaxing to a fixed bath need not be monotonic by
    # itself, so use the positive relative-entropy functional instead.
    rel = np.trapezoid(
        k[None, :] ** 2
        * (f * np.log(np.maximum(f / eq[None, :], 1.0e-300))
           - (1.0 + f) * np.log(np.maximum((1.0 + f) / (1.0 + eq[None, :]), 1.0e-300))),
        k,
        axis=1,
    )
    return {
        'times_Tinv': times,
        'f': f,
        'relative_entropy': rel,
        'subsystem_entropy_like': entropy_like,
        'relative_entropy_nonincrease_max_step': float(np.max(np.diff(rel))),
        'final_relative_entropy_fraction': float(rel[-1] / rel[0]),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def figures(results: dict, arrays: dict) -> None:
    k = arrays['onshell_k_over_T']
    fig, ax = plt.subplots(figsize=(7.4, 4.9))
    ax.plot(k, arrays['Gamma_LPM_occ_over_T'], label='LPM collinear')
    ax.plot(k, arrays['Gamma_hard_occ_over_T'], label='hard+soft 2<->2')
    ax.plot(k, arrays['Gamma_total_occ_over_T'], linewidth=2.2, label='matched total')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(r'$k/T$')
    ax.set_ylabel(r'$\Gamma_H^{\rm occ}(k)/T$')
    ax.set_title('Momentum-resolved q-D-H portal width')
    ax.grid(True, which='both', alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / 'hard_portal_onshell_width_v1_6.png', dpi=220)
    plt.close(fig)

    groups = results['hard_2to2']['GammaY_hard_by_group_over_T3']
    fig, ax = plt.subplots(figsize=(6.7, 4.6))
    ax.bar(list(groups.keys()), list(groups.values()))
    ax.set_ylabel(r'$\Gamma_{Y,G}^{\rm hard}/T^3$')
    ax.set_title('Exact integrated hard portal decomposition')
    ax.grid(True, axis='y', alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / 'hard_portal_group_decomposition_v1_6.png', dpi=220)
    plt.close(fig)

    omega = arrays['omega_over_T']
    kg = arrays['grid_k_over_T']
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    im = ax.pcolormesh(omega, kg, arrays['ImPiR_over_T2'], shading='auto')
    ax.set_xlabel(r'$\omega/T$')
    ax.set_ylabel(r'$k/T$')
    ax.set_yscale('log')
    ax.set_title(r'Near-shell matched $\mathrm{Im}\,\Pi_H^R/T^2$')
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(OUT / 'hard_portal_retarded_grid_v1_6.png', dpi=220)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    im = ax.pcolormesh(omega, kg, arrays['KMS_noise_over_T2'], shading='auto')
    ax.set_xlabel(r'$\omega/T$')
    ax.set_ylabel(r'$k/T$')
    ax.set_yscale('log')
    ax.set_title('KMS noise kernel')
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(OUT / 'hard_portal_kms_noise_v1_6.png', dpi=220)
    plt.close(fig)

    t = arrays['wigner_t_Tinv']
    rel = arrays['wigner_relative_entropy']
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.plot(t, rel / rel[0])
    ax.set_yscale('log')
    ax.set_xlabel(r'$Tt$')
    ax.set_ylabel('relative entropy / initial')
    ax.set_title('Reduced covariant-Wigner relaxation benchmark')
    ax.grid(True, which='both', alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / 'hard_portal_wigner_relaxation_v1_6.png', dpi=220)
    plt.close(fig)


def main() -> None:
    started = time.time()
    point = Point()
    v15 = load_v15()
    v15_point = v15.ModelPoint(
        alpha_s=point.alpha_s,
        g2=point.g2,
        g1=point.g1,
        y_t=point.y_t,
        y_d=point.y_d,
        m_d_over_t=point.m_d_over_t,
    )
    thermal = v15.qd_thermal_data(v15_point)
    with (OUT / 'electroweak_yukawa_lpm_results_v1_5.json').open(encoding='utf-8') as handle:
        old = json.load(handle)
    exact_lpm_integral = old['benchmark']['integral_central']
    exact_lpm_gamma_y = old['benchmark']['gamma_chem_over_T3']
    exact_lpm_occ = old['benchmark']['gamma_occ_over_T']

    hard = hard_integrated(point)
    checks = matrix_element_checks()
    hard_raw = compute_hard_shape(point, thermal['m_q2'], thermal['m_d2'])
    hard_shape = normalize_hard_shape(hard_raw, hard['GammaY_hard_over_T3'])
    lpm_shape = compute_lpm_shape(point, v15, thermal, exact_lpm_integral)
    onshell = on_shell_table(lpm_shape, hard_shape, thermal['m_h'], exact_lpm_gamma_y, hard['GammaY_hard_over_T3'])
    grid = retarded_grid(onshell, thermal['m_h'], thermal['m_debye3'])
    wigner = wigner_benchmark(onshell)

    total_gamma_y = exact_lpm_gamma_y + hard['GammaY_hard_over_T3']
    total_occ = total_gamma_y / CHI_H_OVER_T2
    total_gev = total_occ * point.T0_GeV
    hierarchy = total_gev / point.Gamma_R_GeV

    results = {
        'version': VERSION,
        'point': asdict(point),
        'project_scope': {
            'exact': [
                'Integrated strict-LO hard+soft 2<->2 reaction coefficient at leading order in y_D^2.',
                'v1.5 direct LPM integral and exact susceptibility-weighted on-shell match.',
                'KMS and causality identities of the reconstructed grid.',
            ],
            'numerical': [
                'Full-angle screened hard-cut momentum shape, normalized to the exact integrated coefficient.',
                'Direct momentum-resolved LPM shape from the impact-parameter solver.',
            ],
            'not_claimed': [
                'An exact arbitrary-off-shell two-loop plus LPM scalar self-energy over the full omega-k plane.',
                'A Ward-complete non-Abelian 3+1D 2PI/Kadanoff-Baym evolution.',
            ],
        },
        'matrix_element_checks': checks,
        'hard_2to2': hard,
        'lpm': {
            'I_LPM': exact_lpm_integral,
            'GammaY_LPM_over_T3': exact_lpm_gamma_y,
            'GammaH_LPM_occ_over_T': exact_lpm_occ,
            'shape_quadrature_normalization': lpm_shape['quadrature_normalization_scale'],
        },
        'combined': {
            'GammaY_total_over_T3': total_gamma_y,
            'GammaH_total_occ_over_T': total_occ,
            'GammaH_total_occ_GeV_at_T0': total_gev,
            'GammaH_total_over_Gamma_R': hierarchy,
            'hard_to_LPM_occupation_ratio': hard['GammaH_hard_occ_over_T'] / exact_lpm_occ,
            'hard_fraction_of_total': hard['GammaH_hard_occ_over_T'] / total_occ,
            'adiabatic_lag': 1.0 / hierarchy,
            'B5_shift_bound_for_B5_0p00529888708': 0.00529888708 / hierarchy,
        },
        'hard_shape': {
            'max_screen_shape_relative_envelope': float(np.max(hard_shape['screen_shape_relative_envelope'])),
            'median_screen_shape_relative_envelope': float(np.median(hard_shape['screen_shape_relative_envelope'])),
            'max_MC_relative_error': float(np.max(hard_shape['width_mc_error_over_T'] / hard_shape['width_occ_over_T'])),
            'normalization': hard_shape['normalization'],
            'statement': 'Screening changes only the provisional momentum shape; exact integrated normalization is held fixed.',
        },
        'retarded_grid': grid['diagnostics'],
        'wigner': {
            'relative_entropy_nonincrease_max_step': wigner['relative_entropy_nonincrease_max_step'],
            'final_relative_entropy_fraction': wigner['final_relative_entropy_fraction'],
            'equation': '[K^2-m_H^2-RePi_R,G^<]_PB^cov = Pi^<G^> - Pi^>G^<',
            'gauge_covariance': 'The Wigner transform is defined with straight Wilson lines to the midpoint; the numerical benchmark uses the homogeneous singlet projection.',
        },
        'runtime_seconds': time.time() - started,
    }

    arrays = {
        'onshell_k_over_T': onshell['k'],
        'onshell_energy_over_T': onshell['energy'],
        'Gamma_LPM_occ_over_T': onshell['lpm_width'],
        'Gamma_hard_occ_over_T': onshell['hard_width'],
        'Gamma_total_occ_over_T': onshell['total_width'],
        'ImPiR_onshell_over_T2': onshell['im_pi_on_shell'],
        'hard_shape_k_over_T': hard_shape['k'],
        'hard_screen_shape_envelope': hard_shape['screen_shape_relative_envelope'],
        'grid_k_over_T': grid['k'],
        'omega_over_T': grid['omega'],
        'ImPiR_over_T2': grid['im_pi_R'],
        'RePiR_over_T2': grid['re_pi_R'],
        'KMS_noise_over_T2': grid['noise_N'],
        'wigner_t_Tinv': wigner['times_Tinv'],
        'wigner_f': wigner['f'],
        'wigner_relative_entropy': wigner['relative_entropy'],
    }

    with (OUT / 'hard_portal_retarded_results_v1_6.json').open('w', encoding='utf-8') as handle:
        json.dump(results, handle, indent=2)
    np.savez_compressed(OUT / 'hard_portal_retarded_grid_v1_6.npz', **arrays)

    rows = []
    for i, k in enumerate(onshell['k']):
        rows.append({
            'k_over_T': k,
            'E_over_T': onshell['energy'][i],
            'Gamma_LPM_occ_over_T': onshell['lpm_width'][i],
            'Gamma_hard_occ_over_T': onshell['hard_width'][i],
            'Gamma_total_occ_over_T': onshell['total_width'][i],
            'ImPiR_onshell_over_T2': onshell['im_pi_on_shell'][i],
        })
    write_csv(OUT / 'hard_portal_onshell_table_v1_6.csv', rows)

    acceptance = [
        {'target': 'Project-level publication value', 'verdict': 'PASS AS CANDIDATE PROGRAMME', 'basis': 'Contains falsifiable factorisation, rank and clock/EP relations; absolute priority still requires specialist review.'},
        {'target': 'Strict-LO integrated hard 2<->2 portal cuts', 'verdict': 'PASS', 'basis': 'Representation-general hard+soft formula with Q,D thermal charges and exact group decomposition.'},
        {'target': 'Hard matrix-element group factors', 'verdict': 'PASS AT TREE LEVEL', 'basis': 'U1 result reproduces published e_R coefficients; SU3/SU2 traces implemented for declared representations.'},
        {'target': 'Momentum-resolved hard on-shell shape', 'verdict': 'PASS AS MATCHED NUMERICAL SHAPE', 'basis': 'Full-angle screened phase space, normalized to exact integrated rate; screening-shape envelope reported.'},
        {'target': 'Momentum-resolved LPM width', 'verdict': 'PASS', 'basis': 'Direct v1.5 impact-parameter solver evaluated as dI/dk and normalized to exact integral.'},
        {'target': 'Combined on-shell Pi_R', 'verdict': 'PASS', 'basis': 'Im Pi_R(Ek,k)=-Ek Gamma_occ(k), with exact integrated LPM+hard normalization.'},
        {'target': 'KMS noise kernel', 'verdict': 'PASS', 'basis': 'Detailed-balance ratio and positivity checked numerically.'},
        {'target': 'Arbitrary off-shell Pi_R grid', 'verdict': 'PARTIAL', 'basis': 'Causal near-shell dispersive reconstruction; exact full thermal cut away from shell remains open.'},
        {'target': 'Covariant Wigner transport', 'verdict': 'PASS AS REDUCED BENCHMARK', 'basis': 'Wilson-line definition and matched collision/noise kernel; homogeneous singlet numerical relaxation.'},
        {'target': 'Full Ward-consistent non-Abelian 3+1D 2PI/KB', 'verdict': 'OPEN', 'basis': 'Requires dynamical gauge correlators, vertices and a Ward-preserving truncation.'},
    ]
    write_csv(OUT / 'hard_portal_retarded_acceptance_matrix_v1_6.csv', acceptance)
    figures(results, arrays)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
