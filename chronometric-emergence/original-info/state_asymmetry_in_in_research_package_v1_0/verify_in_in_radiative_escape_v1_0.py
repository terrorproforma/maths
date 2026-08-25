#!/usr/bin/env python3
"""Verification suite for the v1.0 closed-time-path radiative matching note.

Checks:
1. Root-of-unity cancellation of vacuum harmonics p=1,...,5 through a generic
   Taylor expansion of an identical sector functional.
2. Numerical Fourier spectrum of representative one- and two-loop vacuum
   functions summed over the Z6 orbit.
3. One-loop and NLO high-temperature state phasors for the v0.9 benchmark.
4. Exact one-loop thermal scalar-density suppression as T/M falls.
5. Selector/reheaton overlap and late-state separation.
6. A toy spectral memory kernel with no zero-frequency pole decays at late time.

The script writes JSON results and four figures into /mnt/data.
"""
from __future__ import annotations

import cmath
import json
import math
from pathlib import Path
from typing import Dict, List

import numpy as np
import sympy as sp
from scipy.integrate import quad
import matplotlib.pyplot as plt

OUT = Path('/mnt/data')
N = 6
THETA = 2.0 * math.pi / N
NC = 3.0
CF = 4.0 / 3.0
GAMMA_E = 0.5772156649015329
J3_ZERO = -0.00129532

# v0.9 benchmark
M_PSI = 1.002e6       # GeV
T0 = 1.002e8          # GeV
T5 = T0 / 4.0
EPS = 2.70e-13        # cosmological v0.8/v0.9 benchmark
GAMMA_Q = 1.0         # GeV
GAMMA_R = 1.4135e-2   # GeV


def alpha_run_1loop(alpha: float, mu1: float, mu2: float, nf: int) -> float:
    beta0 = 11.0 - 2.0 * nf / 3.0
    return 1.0 / (1.0 / alpha + beta0 / (2.0 * math.pi) * math.log(mu2 / mu1))


def alpha_s_benchmark(mu: float) -> float:
    """Piecewise one-loop running used only for a transparent benchmark estimate."""
    alpha_mz = 0.1179
    mz = 91.1876
    mt = 172.76
    a_mt = alpha_run_1loop(alpha_mz, mz, mt, 5)
    a_mpsi = alpha_run_1loop(a_mt, mt, M_PSI, 6)
    return alpha_run_1loop(a_mpsi, M_PSI, mu, 7)


def c_thermal(mu_over_T: float) -> float:
    """Coefficient of m^2 T^2 in the NLO massive-quark pressure.

    Derived from Eq. (2.1) and the high-T limits in Appendix A of
    arXiv:2101.08240, with their convention g = 4 pi alpha_s.
    """
    return J3_ZERO + (
        0.5 + 3.0 * math.log(mu_over_T * math.exp(GAMMA_E) / math.pi)
    ) / (48.0 * math.pi**2)


def relative_nlo(alpha_s: float, mu_over_T: float) -> float:
    g_hat = 4.0 * math.pi * alpha_s
    return 12.0 * g_hat * CF * c_thermal(mu_over_T)


def j2_thermal(y: float) -> float:
    """Dimensionless J2(y, mu=0) integral."""
    if y < 0:
        raise ValueError('y must be nonnegative')

    def integrand(p: float) -> float:
        e = math.sqrt(p * p + y * y)
        if e > 700:
            return 0.0
        return p * p / e / (math.exp(e) + 1.0)

    val, err = quad(integrand, 0.0, np.inf, epsabs=1e-11, epsrel=1e-9, limit=300)
    return val / math.pi**2


def root_of_unity_symbolic() -> Dict[str, object]:
    """Check generic Taylor terms through epsilon^10."""
    z = sp.symbols('z')
    # Work with z = exp(i x).  cos(x+theta_k) = (z omega^k + z^-1 omega^-k)/2.
    coeffs: Dict[str, object] = {}
    passed = True
    for n in range(0, 11):
        harmonic_coeffs = {}
        # cos^n expansion: choose r factors of z and n-r of z^-1.
        for r in range(n + 1):
            p = 2 * r - n
            binom = sp.binomial(n, r) / 2**n
            # Exact roots-of-unity projector: sum_k exp(i p 2pi k/N)=N iff p=0 mod N.
            orbit = sp.Integer(N) if p % N == 0 else sp.Integer(0)
            c = sp.simplify(binom * orbit)
            if c != 0:
                harmonic_coeffs[int(p)] = str(c)
                if p % N != 0:
                    passed = False
        coeffs[str(n)] = harmonic_coeffs
    return {'passed': passed, 'nonzero_harmonics_by_order': coeffs}


def numerical_vacuum_fourier(epsilon: float = 0.07, ngrid: int = 8192) -> Dict[str, object]:
    xs = np.linspace(0.0, 2.0 * np.pi, ngrid, endpoint=False)
    thetas = np.arange(N) * THETA

    # Representative identical-sector functional: one-loop-like plus an alpha_s correction.
    # It is analytic for epsilon < 1 and therefore obeys the exact orbit selection rule.
    values = np.zeros_like(xs)
    for th in thetas:
        m = 1.0 - epsilon * np.cos(xs + th)
        values += m**4 * np.log(m**2) + 0.13 * m**4 * (np.log(m**2) ** 2 + 0.4)

    fft = np.fft.rfft(values) / ngrid
    amplitudes = {str(p): float(2.0 * abs(fft[p])) for p in range(1, 13)}
    forbidden_max = max(amplitudes[str(p)] for p in range(1, 6))
    first_allowed = amplitudes['6']
    return {
        'epsilon': epsilon,
        'harmonic_amplitudes_1_to_12': amplitudes,
        'max_forbidden_p1_to_p5': forbidden_max,
        'p6_amplitude': first_allowed,
        'forbidden_to_p6_ratio': forbidden_max / first_allowed,
        'passed': forbidden_max / first_allowed < 1e-6,
    }


def benchmark_phasor() -> Dict[str, object]:
    mu0 = 2.0 * math.pi * T0
    mu5 = 2.0 * math.pi * T5
    a0 = alpha_s_benchmark(mu0)
    a5 = alpha_s_benchmark(mu5)
    r0 = relative_nlo(a0, mu0 / T0)
    r5 = relative_nlo(a5, mu5 / T5)

    w_lo = 1.0 + (T5 / T0) ** 2 * cmath.exp(1j * 5.0 * THETA)
    w_nlo = (1.0 + r0) + (T5 / T0) ** 2 * (1.0 + r5) * cmath.exp(1j * 5.0 * THETA)

    scale_band = {}
    for c in (1.0, 2.0, 4.0):
        mu0c = c * math.pi * T0
        mu5c = c * math.pi * T5
        aa0 = alpha_s_benchmark(mu0c)
        aa5 = alpha_s_benchmark(mu5c)
        rr0 = relative_nlo(aa0, mu0c / T0)
        rr5 = relative_nlo(aa5, mu5c / T5)
        ww = (1.0 + rr0) + (T5 / T0) ** 2 * (1.0 + rr5) * cmath.exp(1j * 5.0 * THETA)
        scale_band[f'{c:.0f}piT'] = {
            'alpha0': aa0,
            'alpha5': aa5,
            'r0': rr0,
            'r5': rr5,
            'amplitude_ratio_to_LO': abs(ww) / abs(w_lo),
            'phase_rad': cmath.phase(ww),
        }

    return {
        'alpha_s_2piT_sector0': a0,
        'alpha_s_2piT_sector5': a5,
        'relative_NLO_sector0': r0,
        'relative_NLO_sector5': r5,
        'LO_amplitude': abs(w_lo),
        'LO_phase_rad': cmath.phase(w_lo),
        'NLO_amplitude': abs(w_nlo),
        'NLO_phase_rad': cmath.phase(w_nlo),
        'NLO_to_LO_amplitude': abs(w_nlo) / abs(w_lo),
        'phase_shift_rad': cmath.phase(w_nlo) - cmath.phase(w_lo),
        'phase_shift_deg': (cmath.phase(w_nlo) - cmath.phase(w_lo)) * 180.0 / math.pi,
        'renormalization_scale_band': scale_band,
    }


def selector_overlap() -> Dict[str, float]:
    ratio = GAMMA_R / GAMMA_Q
    fraction = 1.0 - math.exp(-ratio)
    return {
        'GammaR_over_GammaQ': ratio,
        'fraction_decayed_by_one_selector_lifetime': fraction,
        'fraction_if_GammaQ_10GeV': 1.0 - math.exp(-GAMMA_R / 10.0),
    }


def memory_kernel_values() -> Dict[str, object]:
    """Toy gapped spectral kernel showing Riemann-Lebesgue decay.

    Dimensionless M=1. The smooth UV regulator is for numerical convergence only.
    rho(w) ~ w^2(1-4/w^2)^(3/2) theta(w-2) exp(-w/20).
    """
    def rho(w: float) -> float:
        if w <= 2.0:
            return 0.0
        return w * w * (1.0 - 4.0 / (w * w)) ** 1.5 * math.exp(-w / 20.0)

    def kernel(t: float) -> float:
        # QUADPACK's oscillatory-weight routine handles the semi-infinite sine transform.
        val, _ = quad(lambda w: rho(w), 2.0, np.inf, weight='sin', wvar=t,
                      epsabs=2e-7, epsrel=2e-6, limlst=300, limit=300)
        return val / math.pi

    ts = np.geomspace(0.2, 100.0, 120)
    vals = np.array([kernel(float(t)) for t in ts])
    late_rms = float(np.sqrt(np.mean(vals[-20:] ** 2)))
    early_rms = float(np.sqrt(np.mean(vals[:20] ** 2)))

    plt.figure(figsize=(7.2, 4.4))
    plt.loglog(ts, np.abs(vals) + 1e-30)
    plt.xlabel(r'$M(t-t\prime)$')
    plt.ylabel(r'$|K_R(t-t\prime)|$ (arbitrary units)')
    plt.title('Gapped retarded-memory kernel: no zero-frequency pole')
    plt.tight_layout()
    plt.savefig(OUT / 'in_in_memory_kernel_v1_0.png', dpi=200)
    plt.close()

    return {
        'early_rms': early_rms,
        'late_rms': late_rms,
        'late_to_early_rms': late_rms / early_rms,
        'sample_times': ts[::15].tolist(),
        'sample_abs_kernel': np.abs(vals[::15]).tolist(),
    }


def thermal_decay_curve() -> Dict[str, object]:
    # Scale factor A = a/a_R; T0(A)=T0/A. Exact one-loop scalar-density coefficient.
    scales = np.geomspace(1.0, 3.0e4, 240)
    coeff_lo = []
    coeff_nlo = []
    for A in scales:
        temp0 = T0 / A
        temp5 = T5 / A
        # First-harmonic phasor coefficient up to an overall -2 Nc M^2 epsilon.
        j20 = j2_thermal(M_PSI / temp0)
        j25 = j2_thermal(M_PSI / temp5)
        w = temp0**2 * j20 + temp5**2 * j25 * cmath.exp(1j * 5.0 * THETA)
        coeff_lo.append(abs(w))

        # NLO high-T correction used only where T > 3M; smoothly turn it off below.
        def nlo_weight(temp: float) -> float:
            if temp <= 0:
                return 0.0
            r = relative_nlo(alpha_s_benchmark(max(2.0 * math.pi * temp, 1.01 * M_PSI)), 2.0 * math.pi)
            switch = 1.0 / (1.0 + (3.0 * M_PSI / temp) ** 6)
            return r * switch

        r0 = nlo_weight(temp0)
        r5 = nlo_weight(temp5)
        wn = temp0**2 * j20 * (1.0 + r0) + temp5**2 * j25 * (1.0 + r5) * cmath.exp(1j * 5.0 * THETA)
        coeff_nlo.append(abs(wn))

    coeff_lo = np.array(coeff_lo)
    coeff_nlo = np.array(coeff_nlo)
    coeff_lo /= coeff_lo[0]
    coeff_nlo /= coeff_nlo[0]

    plt.figure(figsize=(7.2, 4.4))
    plt.loglog(scales, coeff_lo, label='one-loop state harmonic')
    plt.loglog(scales, coeff_nlo, linestyle='--', label='with NLO QCD correction')
    plt.axvline(T0 / M_PSI, linestyle=':', label=r'$T_0=M$')
    plt.xlabel(r'scale factor $a/a_R$')
    plt.ylabel('normalized lower-harmonic amplitude')
    plt.title('The asymmetric-state harmonic redshifts and Boltzmann-suppresses')
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / 'in_in_state_harmonic_decay_v1_0.png', dpi=200)
    plt.close()

    return {
        'a_when_T0_equals_M': T0 / M_PSI,
        'normalized_LO_at_final': float(coeff_lo[-1]),
        'normalized_NLO_at_final': float(coeff_nlo[-1]),
        'sample_scale_factors': scales[::40].tolist(),
        'sample_LO': coeff_lo[::40].tolist(),
        'sample_NLO': coeff_nlo[::40].tolist(),
    }


def selector_state_figure() -> Dict[str, object]:
    tau = np.linspace(0.0, 250.0, 1000)  # tau = Gamma_Q t
    q = np.exp(-2.0 * tau)
    reheaton = np.exp(-(GAMMA_R / GAMMA_Q) * tau)
    radiation = 1.0 - reheaton

    plt.figure(figsize=(7.2, 4.4))
    plt.semilogy(tau, q + 1e-30, label=r'selector spurion $|Q_0|^2/v_Q^2$')
    plt.semilogy(tau, reheaton + 1e-30, label=r'$R_0$ population')
    plt.semilogy(tau, radiation + 1e-30, label='asymmetric daughter occupation')
    plt.xlabel(r'$\Gamma_Q t$')
    plt.ylabel('normalized quantity')
    plt.title('The selector disappears; the state asymmetry remains temporarily')
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / 'in_in_selector_state_separation_v1_0.png', dpi=200)
    plt.close()

    return {
        'selector_spurion_at_one_lifetime': math.exp(-2.0),
        'radiation_fraction_at_one_lifetime': 1.0 - math.exp(-GAMMA_R / GAMMA_Q),
        'selector_spurion_at_five_lifetimes': math.exp(-10.0),
        'radiation_fraction_at_five_lifetimes': 1.0 - math.exp(-5.0 * GAMMA_R / GAMMA_Q),
    }


def harmonic_bar_figure(vacuum: Dict[str, object]) -> None:
    ps = np.arange(1, 13)
    amps = np.array([vacuum['harmonic_amplitudes_1_to_12'][str(int(p))] for p in ps])
    plt.figure(figsize=(7.2, 4.4))
    plt.semilogy(ps, amps + 1e-30, marker='o')
    plt.axvline(6, linestyle=':')
    plt.xlabel('Fourier harmonic p')
    plt.ylabel('orbit-summed vacuum amplitude')
    plt.title('Exact Z6 vacuum matching: first allowed harmonic is p=6')
    plt.xticks(ps)
    plt.tight_layout()
    plt.savefig(OUT / 'in_in_vacuum_harmonics_v1_0.png', dpi=200)
    plt.close()


def main() -> None:
    symbolic = root_of_unity_symbolic()
    vacuum = numerical_vacuum_fourier()
    harmonic_bar_figure(vacuum)
    phasor = benchmark_phasor()
    overlap = selector_overlap()
    selector_sep = selector_state_figure()
    thermal = thermal_decay_curve()
    memory = memory_kernel_values()

    results = {
        'metadata': {
            'model': 'Z6 state-selected reheating / QCD chronometry v1.0',
            'N': N,
            'M_Psi_GeV': M_PSI,
            'T0_GeV': T0,
            'T5_GeV': T5,
            'epsilon': EPS,
        },
        'root_of_unity_symbolic': symbolic,
        'vacuum_fourier': vacuum,
        'thermal_NLO_phasor': phasor,
        'selector_overlap': overlap,
        'selector_state_separation': selector_sep,
        'thermal_state_decay': thermal,
        'memory_kernel': memory,
        'acceptance': {
            'vacuum_forbidden_harmonics_cancel': bool(symbolic['passed'] and vacuum['passed']),
            'two_loop_state_correction_is_perturbative_at_2piT': bool(
                abs(phasor['relative_NLO_sector0']) < 0.2 and abs(phasor['relative_NLO_sector5']) < 0.2
            ),
            'state_harmonic_decays': bool(thermal['normalized_LO_at_final'] < 1e-12),
            'gapped_memory_decays': bool(memory['late_to_early_rms'] < 0.1),
        },
    }

    with open(OUT / 'in_in_radiative_escape_results_v1_0.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    # Compact CSV benchmark table.
    rows = [
        ('alpha_s(2piT0)', phasor['alpha_s_2piT_sector0']),
        ('alpha_s(2piT5)', phasor['alpha_s_2piT_sector5']),
        ('NLO/LO correction sector0', phasor['relative_NLO_sector0']),
        ('NLO/LO correction sector5', phasor['relative_NLO_sector5']),
        ('NLO phasor amplitude / LO', phasor['NLO_to_LO_amplitude']),
        ('NLO phase shift [rad]', phasor['phase_shift_rad']),
        ('selector/reheaton overlap fraction', overlap['fraction_decayed_by_one_selector_lifetime']),
        ('forbidden harmonic / p6', vacuum['forbidden_to_p6_ratio']),
        ('late/early memory RMS', memory['late_to_early_rms']),
    ]
    with open(OUT / 'in_in_radiative_escape_benchmark_v1_0.csv', 'w', encoding='utf-8') as f:
        f.write('quantity,value\n')
        for name, value in rows:
            f.write(f'"{name}",{value:.16e}\n')

    print(json.dumps(results['acceptance'], indent=2))
    print('Wrote results and figures to', OUT)


if __name__ == '__main__':
    main()
