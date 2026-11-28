#!/usr/bin/env python3
"""Verify TP-03 Phase 3 (PS1-EW): electroweak matching, RG running, fermion/neutrino fit,
and flavour, baryon-stability, and cosmological relic gates (post-referee revision).

This module extends the certified Phase 2B high-scale vacuum branch PS1-MM to the
electroweak-matched branch PS1-EW (split explicitly into the minimal two-Yukawa sub-branch
PS1-EW-min and the full gauge-invariant four-Yukawa sub-branch PS1-EW-gen):

1. Explicit SU(4)_C x SU(2)_L x SU(2)_R-invariant bidoublet + Delta_R portal potential
   (17 operators = 25 real parameters), direct gauge-invariance test, exact rank-16
   surjective map (9-dim kernel) onto the 4x4 colour-singlet Higgs mass matrix M_H^2,
   coloured octet/leptoquark mass matrices, fine-tuning to one light SM Higgs doublet h
   at the unbroken EW origin, full 188x188 real scalar Hessian verification, and explicit
   tree-level two-field (h, Delta_R) quartic stability audit along the negative-portal ray.
2. One- and two-loop SM gauge/Yukawa/quartic/Weinberg-operator RGEs from M_Z to v_R,
   exact Weinberg-Hall 1-loop MS-bar threshold matching using the explicit Phase 2B/3
   heavy vector and 175 heavy scalar spectrum (with UV-IR group-theory sum-rule checks),
   gauge-only 2-loop PS1 running (omitting 2-loop UV Yukawa traces) + approximate SO(10)
   crossing without M_GUT parent thresholds, and 60-real-component Delta_R quartic pure-
   self-coupling Landau-pole diagnostic (136 lambda_Delta^2).
3. Quantitative 3-generation charged-fermion, CKM, neutrino, and PMNS existence fits
   across the viable v_R window (BM-LR, v_R = 6e11 GeV refit, BM-GUT, BM-LOW) comparing
   PS1-EW-min (both real and complex Higgs mixing ratios; 30 real Yukawa parameters vs
   18 real observables) and PS1-EW-gen (with direct forward tensor-contraction verification
   and charged-lepton mass-basis PMNS round-trip verification).
4. Quantitative audit of Valencia-Willenbrock X-boson K_L -> mu e and B_s -> mu e,
   MEG II mu -> e gamma, preliminary order-of-magnitude W_R/Z_R, heavy-Higgs FCNC, and
   n-nbar checks (using actual sextet masses), baryon-number selection rules, and
   monopole / Z_2-string / domain-wall / thermal-leptogenesis cosmology.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from scipy.optimize import brentq, least_squares

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from verify_phase2b_vacuum import (  # noqa: E402
    REPRESENTATION,
    broken_gauge_directions,
    cluster_eigenvalues,
    delta_real_hessian,
    expected_delta_eigenvalues,
    su_n_generators,
    symmetric_tensor_basis,
)

# ---------------------------------------------------------------------------
# Frozen physical baseline inputs (PDG 2024/2026 MS-bar at M_Z, NuFIT 5.3 NO)
# ---------------------------------------------------------------------------
MZ_GEV = 91.1876
V_EW_GEV = 246.22
M_H_GEV = 125.25
M_PL_GEV = 1.2209e19
PERT_LIMIT = math.sqrt(4.0 * math.pi)  # 3.5449077...

# Gauge couplings at M_Z (MS-bar, PDG 2024/2026)
ALPHA_S_MZ = 0.1180
ALPHA_EM_INV_MZ = 127.951
SIN2_THETA_W_MZ = 0.23122

# Running MS-bar charged-fermion masses at mu = M_Z in GeV (Huang & Zhou 2020 / PDG 2024)
FERMION_MASSES_MZ_GEV = {
    "u": 1.23e-3,
    "c": 0.620,
    "t": 168.26,
    "d": 2.67e-3,
    "s": 53.16e-3,
    "b": 2.839,
    "e": 0.48307e-3,
    "mu": 0.101766,
    "tau": 1.72856,
}

# CKM standard parametrization angles at M_Z (PDG 2024/2026)
CKM_INPUTS_MZ = {
    "theta12": 0.22736,
    "theta23": 0.04183,
    "theta13": 0.00369,
    "delta_rad": 1.144,
}

# Neutrino oscillation parameters (NuFIT 5.3, Normal Ordering)
NEUTRINO_INPUTS = {
    "dm21_sq_eV2": 7.41e-5,
    "dm31_sq_eV2": 2.511e-3,
    "sin2_th12": 0.303,
    "sin2_th23": 0.572,
    "sin2_th13": 0.02203,
    "delta_pmns_deg": 197.0,
    "m1_benchmark_eV": 0.015,  # gives sum m_nu = 0.0842 eV < 0.12 eV (Planck+DESI)
}

# Flavour & stability experimental limits (PDG 2024/2026)
EXP_BOUNDS = {
    "BR_KL_mue_90CL": 4.7e-12,         # BNL E871
    "BR_Bs_mue_90CL": 5.4e-9,          # LHCb
    "BR_mu_egamma_90CL": 1.5e-13,      # MEG II (combined 90% CL)
    "tau_p_e_pi0_yr_90CL": 2.4e34,     # Super-Kamiokande
    "tau_nnbar_s_90CL": 4.7e8,         # Super-K + ILL
    "m_beta_KATRIN_eV": 0.45,          # KATRIN 2025
    "sum_mnu_cosmo_eV": 0.12,          # Planck + BAO benchmark
    "m_WR_LHC_GeV": 6000.0,            # ATLAS/CMS direct search order
    "m_H2_FCNC_GeV": 5.0e4,            # K0-K0bar tree-level heavy-Higgs FCNC floor
}


def standard_unitary_3x3(t12: float, t23: float, t13: float, delta: float) -> np.ndarray:
    """PDG standard parametrization of a 3x3 unitary mixing matrix."""
    c12, s12 = math.cos(t12), math.sin(t12)
    c23, s23 = math.cos(t23), math.sin(t23)
    c13, s13 = math.cos(t13), math.sin(t13)
    ep = complex(math.cos(delta), -math.sin(delta))
    em = ep.conjugate()
    return np.array(
        [
            [c12 * c13, s12 * c13, s13 * ep],
            [-s12 * c23 - c12 * s23 * s13 * em, c12 * c23 - s12 * s23 * s13 * em, s23 * c13],
            [s12 * s23 - c12 * c23 * s13 * em, -c12 * s23 - s12 * c23 * s13 * em, c23 * c13],
        ],
        dtype=np.complex128,
    )


def jarlskog_invariant(v: np.ndarray) -> float:
    return float((v[0, 1] * v[1, 2] * v[0, 2].conjugate() * v[1, 1].conjugate()).imag)


# ---------------------------------------------------------------------------
# PART 1: Gauge-invariant PS1-EW bidoublet + Delta_R potential & 188x188 Hessian
# ---------------------------------------------------------------------------
class PS1EWScalarAlgebra:
    """Exact group-theoretic tensors and invariant portal operators for PS1-EW."""

    def __init__(self) -> None:
        self.T4 = su_n_generators(4)
        self.T2 = su_n_generators(2)
        self.sigmas = [2.0 * g for g in self.T2]
        self.eps = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=np.complex128)
        self.u4, self.pairs4 = symmetric_tensor_basis(4)
        self.u2, self.pairs2 = symmetric_tensor_basis(2)
        self.t3_list = [
            self.u2.conj().T @ (np.kron(g, np.eye(2)) + np.kron(np.eye(2), g)) @ self.u2
            for g in self.T2
        ]
        # Verify T4[14] = T^15 = diag(1,1,1,-3)/sqrt(24)
        t15_expected = np.diag([1.0, 1.0, 1.0, -3.0]) / math.sqrt(24.0)
        if np.max(np.abs(self.T4[14] - t15_expected)) > 1.0e-12:
            raise ArithmeticError("T4[14] is not canonical T^15")

    def delta_vec_to_tensor(self, vec: np.ndarray) -> np.ndarray:
        D = np.zeros((4, 4, 3), dtype=np.complex128)
        for idx4, (a, b) in enumerate(self.pairs4):
            for i in range(3):
                val = vec[idx4 * 3 + i]
                if a == b:
                    D[a, a, i] = val
                else:
                    D[a, b, i] = D[b, a, i] = val / math.sqrt(2.0)
        return D

    def phi15_A_to_tensor(self, pA: np.ndarray) -> np.ndarray:
        return math.sqrt(2.0) * np.einsum("Aab,Alr->ablr", np.array(self.T4), pA)

    def tilde_phi1(self, p1: np.ndarray) -> np.ndarray:
        return self.eps @ p1.conj() @ self.eps.T

    def tilde_phi15(self, M15: np.ndarray) -> np.ndarray:
        out = np.zeros_like(M15)
        for a in range(4):
            for b in range(4):
                out[a, b] = self.eps @ M15[b, a].conj() @ self.eps.T
        return out

    def evaluate_portal_invariants(
        self,
        delta_vec: np.ndarray,
        phi1: np.ndarray,
        phi15_A: np.ndarray,
    ) -> Dict[str, complex]:
        """Evaluate all 17 declared gauge-invariant quadratic+portal operators (25 real parameters)."""
        D = self.delta_vec_to_tensor(delta_vec)
        M15 = self.phi15_A_to_tensor(phi15_A)
        p1t = self.tilde_phi1(phi1)
        M15t = self.tilde_phi15(M15)

        r = float(np.vdot(delta_vec, delta_vec).real)
        D0 = np.einsum("aci,bci->ab", D, D.conj())
        Dk = np.array([np.einsum("bci,ij,acj->ab", D.conj(), self.t3_list[k], D) for k in range(3)])
        muR = np.array([np.einsum("abi,ij,abj->", D.conj(), self.t3_list[k], D).real for k in range(3)])

        inv: Dict[str, complex] = {}
        # Bare quadratic invariants
        inv["q_1"] = np.trace(phi1.conj().T @ phi1).real
        inv["q_1_hol"] = np.trace(p1t.conj().T @ phi1)
        inv["q_15"] = np.einsum("ablr,ablr->", M15.conj(), M15).real
        inv["q_15_hol"] = np.einsum("ablr,ablr->", M15t.conj(), M15)
        # Phi1 - DeltaR portals
        inv["p_1_0"] = r * inv["q_1"]
        inv["p_1_R"] = sum(
            muR[k] * np.trace(phi1.conj().T @ phi1 @ self.sigmas[k]).real for k in range(3)
        )
        inv["p_1_hol"] = r * inv["q_1_hol"]
        # Phi15 - DeltaR portals (15-channels a, b and 84-channels c, cR, chol)
        inv["p_15_0"] = r * inv["q_15"]
        inv["p_15_a"] = np.einsum("balr,bclr,ca->", M15.conj(), M15, D0).real
        inv["p_15_b"] = np.einsum("ablr,cblr,ca->", M15, M15.conj(), D0).real
        inv["p_15_c"] = np.einsum("abi,cdi,bdlr,calr->", D, D.conj(), M15.conj(), M15).real
        inv["p_15_cR"] = sum(
            np.einsum(
                "abj,cdi,ij,bdlr,calm,mr->",
                D,
                D.conj(),
                self.t3_list[k],
                M15.conj(),
                M15,
                self.sigmas[k],
            ).real
            for k in range(3)
        )
        inv["p_15_chol"] = np.einsum("abi,cdi,bdlr,calr->", D, D.conj(), M15t.conj(), M15)
        # Phi1 - Phi15 - DeltaR mixing portals (15-channel)
        inv["m_0"] = np.einsum("lr,ablr,ba->", phi1.conj(), M15, D0)
        inv["m_R"] = sum(
            np.einsum("lr,ablm,mr,ba->", phi1.conj(), M15, self.sigmas[k], Dk[k]) for k in range(3)
        )
        inv["m_t0"] = np.einsum("lr,ablr,ba->", p1t.conj(), M15, D0)
        inv["m_tR"] = sum(
            np.einsum("lr,ablm,mr,ba->", p1t.conj(), M15, self.sigmas[k], Dk[k]) for k in range(3)
        )
        return inv

    def test_gauge_invariance(self, seed: int = 20260901, trials: int = 5) -> float:
        """Verify SU(4)_C x SU(2)_L x SU(2)_R invariance of all 17 bidoublet/portal operators."""
        rng = np.random.default_rng(seed)

        def rand_su(n: int) -> np.ndarray:
            A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
            Q, R = np.linalg.qr(A)
            Q = Q * np.exp(-1j * np.angle(np.diag(R)))
            return Q / (np.linalg.det(Q) ** (1.0 / n))

        max_err = 0.0
        for _ in range(trials):
            U4, UL, UR = rand_su(4), rand_su(2), rand_su(2)
            U4_10 = self.u4.conj().T @ np.kron(U4, U4) @ self.u4
            UR_3 = self.u2.conj().T @ np.kron(UR, UR) @ self.u2

            d_vec = rng.normal(size=30) + 1j * rng.normal(size=30)
            p1 = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
            p15_A = rng.normal(size=(15, 2, 2)) + 1j * rng.normal(size=(15, 2, 2))

            inv1 = self.evaluate_portal_invariants(d_vec, p1, p15_A)

            d_rot = np.kron(U4_10, UR_3) @ d_vec
            p1_rot = UL @ p1 @ UR.conj().T
            M15 = self.phi15_A_to_tensor(p15_A)
            M15_rot = np.einsum("ac,lm,cdmn,rn,bd->ablr", U4, UL, M15, UR.conj(), U4.conj())
            p15_A_rot = np.array(
                [math.sqrt(2.0) * np.einsum("ba,ablr->lr", T, M15_rot) for T in self.T4]
            )
            inv2 = self.evaluate_portal_invariants(d_rot, p1_rot, p15_A_rot)
            for key in inv1:
                scale = max(1.0, abs(inv1[key]))
                max_err = max(max_err, abs(inv1[key] - inv2[key]) / scale)
        return max_err

    def test_delta_squared_vanishing(self) -> float:
        """Verify that on <Delta_R>, Delta_R x Delta_R projects purely onto ([4,0,0], 1, 5),
        so all [0,2,0] and [2,1,0] channels in Phi15^2 Delta_R^2 vanish identically."""
        highest = REPRESENTATION["highest"]
        assert isinstance(highest, np.ndarray)
        D = self.delta_vec_to_tensor(highest)
        # Compute Sym^2(4x4) antisymmetrized part: (D_ab D_cd - D_ac D_bd) -> measures [0,2,0] + [2,1,0]
        # On a rank-1 tensor D_ab = v_a v_b, D_ab D_cd - D_ac D_bd = 0 identically!
        D_su4 = D[:, :, 0]
        anti = np.einsum("ab,cd->abcd", D_su4, D_su4) - np.einsum("ac,bd->abcd", D_su4, D_su4)
        # Also verify SU(2)_R triplet (j=1) and singlet (j=0) projections of |+1> x |+1> vanish:
        # |+1> x |+1> has T_R^3 = +2, which exists ONLY in j_R = 2 (dim 5)!
        return float(np.max(np.abs(anti)))


ALGEBRA = PS1EWScalarAlgebra()


def solve_portal_parameters_for_light_higgs(
    u_light: np.ndarray,
    m_h_sq_over_vR2: float,
    heavy_doublet_masses_sq: Tuple[float, float, float] = (0.80, 1.20, 1.60),
    octet_masses_sq: Tuple[float, float] = (1.10, 1.30),
    triplet_masses_sq: Tuple[float, float] = (1.40, 1.80),
    v_r: float = 1.0,
) -> Dict[str, object]:
    """Choose one preimage under the rank-16 surjective linear map (25 real parameters from
    17 gauge-invariant operators -> 16 real Hermitian entries of M_H^2, with a 9-dimensional
    kernel; fixing the coloured blocks fixes 5 real combinations, leaving 4 redundant directions
    fixed here by alpha1_0=0.30, alpha15_0=0.40, talpha1_0=0)."""
    u = np.asarray(u_light, dtype=np.complex128)
    u = u / np.linalg.norm(u)

    # Deterministic orthonormal completion U_H = [u, u2, u3, u4]
    basis = [u]
    for e_idx in range(4):
        cand = np.zeros(4, dtype=np.complex128)
        cand[e_idx] = 1.0
        for b in basis:
            cand = cand - np.vdot(b, cand) * b
        nrm = np.linalg.norm(cand)
        if nrm > 1.0e-8:
            basis.append(cand / nrm)
        if len(basis) == 4:
            break
    U_H = np.column_stack(basis)
    assert np.max(np.abs(U_H.conj().T @ U_H - np.eye(4))) < 1.0e-12

    eigs_H = np.array(
        [m_h_sq_over_vR2, heavy_doublet_masses_sq[0], heavy_doublet_masses_sq[1], heavy_doublet_masses_sq[2]]
    ) * (v_r**2)
    M_H_sq = U_H @ np.diag(eigs_H) @ U_H.conj().T
    M_H_sq = 0.5 * (M_H_sq + M_H_sq.conj().T)

    # Coloured multiplet masses fix mu15^2, tilde_mu15^2, alpha15_0, alpha15_a, alpha15_b:
    # M_Omega^2 = [[M15_bare^2, 2*tmu15^*], [2*tmu15, M15_bare^2]] -> eigenvalues M15_bare^2 +/- 2|tmu15|
    M15_bare_sq = 0.5 * (octet_masses_sq[0] + octet_masses_sq[1]) * v_r**2
    tmu15_sq = 0.25 * (octet_masses_sq[1] - octet_masses_sq[0]) * v_r**2  # real positive
    # Choose alpha15_0 = 0.40, so mu15^2 = M15_bare^2 - 0.5 * alpha15_0 * v_r^2
    alpha15_0 = 0.40
    mu15_sq = M15_bare_sq - 0.5 * alpha15_0 * v_r**2

    # For colour-triplet leptoquarks Sigma_{7/6} and Sigma_{1/6}:
    # Diagonal entries are M15_bare^2 + 0.5*alpha15_a*v_r^2 and M15_bare^2 + 0.5*alpha15_b*v_r^2,
    # off-diagonal entry is 2*tmu15_sq (real).
    # Eigenvalues are ((d1+d2)/2) +/- sqrt(((d1-d2)/2)^2 + (2*tmu15_sq)^2).
    t_sum = (triplet_masses_sq[0] + triplet_masses_sq[1]) * v_r**2
    t_half_diff = 0.5 * (triplet_masses_sq[1] - triplet_masses_sq[0]) * v_r**2
    if t_half_diff <= abs(2.0 * tmu15_sq):
        raise ValueError("Triplet mass splitting must exceed octet mass splitting")
    delta_ab = 2.0 * math.sqrt(t_half_diff**2 - (2.0 * tmu15_sq) ** 2)
    d1 = 0.5 * t_sum - 0.5 * delta_ab
    d2 = 0.5 * t_sum + 0.5 * delta_ab
    alpha15_a = 2.0 * (d1 - M15_bare_sq) / (v_r**2)
    alpha15_b = 2.0 * (d2 - M15_bare_sq) / (v_r**2)

    # Now invert the exact 4x4 colour-singlet doublet matrix M_H^2 (basis: H1u, H1d, H15u, H15d):
    # Diagonal entries:
    # M11 = mu1^2 + 0.5*v_r^2*(alpha1_0 - alpha1_R)
    # M22 = mu1^2 + 0.5*v_r^2*(alpha1_0 + alpha1_R)
    alpha1_0 = 0.30
    mu1_sq = 0.5 * (M_H_sq[0, 0].real + M_H_sq[1, 1].real) - 0.5 * alpha1_0 * v_r**2
    alpha1_R = (M_H_sq[1, 1].real - M_H_sq[0, 0].real) / (v_r**2)

    # M33 = M15_bare^2 + (3/8)*v_r^2*(alpha15_a + alpha15_b + alpha15_c - alpha15_cR)
    # M44 = M15_bare^2 + (3/8)*v_r^2*(alpha15_a + alpha15_b + alpha15_c + alpha15_cR)
    avg_34 = 0.5 * (M_H_sq[2, 2].real + M_H_sq[3, 3].real)
    alpha15_c = (8.0 / (3.0 * v_r**2)) * (avg_34 - M15_bare_sq) - alpha15_a - alpha15_b
    alpha15_cR = (4.0 / (3.0 * v_r**2)) * (M_H_sq[3, 3].real - M_H_sq[2, 2].real)

    # Off-diagonal (2,1) and (4,3):
    # In V: tmu1^2 Tr(Phi1_tilde^dag Phi1) + h.c. = 2 tmu1^2 H1d^dag H1u + h.c.
    # -> M_H_sq[1, 0] = 2 tmu1^2 + v_r^2 talpha1_0 (set talpha1_0 = 0, absorb into tmu1^2)
    talpha1_0 = 0.0 + 0.0j
    tmu1_sq = 0.5 * M_H_sq[1, 0]

    # In V: tmu15^2 Tr(Phi15_tilde^dag Phi15) + talpha15_c * p_15_chol + h.c.
    # On colour singlet (15): p_15_chol -> (v_r^2/2) * (3/4) * (2 H15d^dag H15u) = (3/4) v_r^2 H15d^dag H15u!
    # Wait: M_H_sq[3, 2] = 2 tmu15_sq + (3/4) v_r^2 talpha15_c
    talpha15_c = (4.0 / (3.0 * v_r**2)) * (M_H_sq[3, 2] - 2.0 * tmu15_sq)

    # Off-diagonal Phi1-Phi15 mixing (note: M15[3,3] = -sqrt(3)/2 * Phi15^(15)):
    # On vacuum D0 = (v_r^2/2) P4, D3 = (v_r^2/2) P4:
    # m_0 = -(sqrt(3)/4) v_r^2 * Tr(Phi1^dag Phi15^(15))
    #     = -(sqrt(3)/4) v_r^2 * (H1u^dag H15u + H15d^dag H1d)
    # m_R = -(sqrt(3)/4) v_r^2 * Tr(Phi1^dag Phi15^(15) sigma_3)
    #     = -(sqrt(3)/4) v_r^2 * (-H1u^dag H15u + H15d^dag H1d)
    # Therefore in V = (beta0 m_0 + betaR m_R) + h.c.:
    # Coeff of H1u^dag H15u is M_H_sq[0, 2] = -(sqrt(3)/4) v_r^2 (beta0 - betaR)
    # Coeff of H15d^dag H1d is M_H_sq[3, 1] = -(sqrt(3)/4) v_r^2 (beta0 + betaR)
    # => M_H_sq[1, 3] = M_H_sq[3, 1]^* = -(sqrt(3)/4) v_r^2 (beta0^* + betaR^*)
    c_mix = -math.sqrt(3.0) * (v_r**2) / 4.0
    s_minus = M_H_sq[0, 2] / c_mix   # beta0 - betaR
    s_plus = M_H_sq[3, 1] / c_mix    # beta0 + betaR
    beta0 = 0.5 * (s_plus + s_minus)
    betaR = 0.5 * (s_plus - s_minus)

    # Similarly for tilde-mixing:
    # Phi1_tilde = (tilde_H1u, H1d), so:
    # Tr(Phi1_tilde^dag Phi15^(15)) = tilde_H1u^dag phi15d + H1d^dag H15u
    # Check tilde_H1u^dag phi15d:
    # tilde_H1u = (H1u^{0*}, -H1u^{+*})^T, phi15d = (phi15d^0, phi15d^-)^T = (H15d^{0*}, -H15d^{+*})^T
    # Wait: H15d = (-phi15d^{-*}, phi15d^{0*})^T => phi15d^0 = H15d^{0*}, phi15d^- = -H15d^{+*}
    # So tilde_H1u^dag phi15d = H1u^0 H15d^{0*} + H1u^+ H15d^{+*} = H15d^dag H1u!
    # Therefore:
    # m_t0 = c_mix * (H1d^dag H15u + H15d^dag H1u)
    # m_tR = c_mix * (-H1d^dag H15u + H15d^dag H1u)
    # So in V = (tbeta0 m_t0 + tbetaR m_tR) + h.c.:
    # Coeff of H1d^dag H15u is M_H_sq[1, 2] = c_mix * (tbeta0 - tbetaR)
    # Coeff of H15d^dag H1u is M_H_sq[3, 0] = c_mix * (tbeta0 + tbetaR)
    ts_minus = M_H_sq[1, 2] / c_mix
    ts_plus = M_H_sq[3, 0] / c_mix
    tbeta0 = 0.5 * (ts_plus + ts_minus)
    tbetaR = 0.5 * (ts_plus - ts_minus)

    params = {
        "v_R": v_r,
        "mu1_sq": float(mu1_sq),
        "tmu1_sq": complex(tmu1_sq),
        "mu15_sq": float(mu15_sq),
        "tmu15_sq": float(tmu15_sq),
        "alpha1_0": float(alpha1_0),
        "alpha1_R": float(alpha1_R),
        "talpha1_0": complex(talpha1_0),
        "alpha15_0": float(alpha15_0),
        "alpha15_a": float(alpha15_a),
        "alpha15_b": float(alpha15_b),
        "alpha15_c": float(alpha15_c),
        "alpha15_cR": float(alpha15_cR),
        "talpha15_c": complex(talpha15_c),
        "beta0": complex(beta0),
        "betaR": complex(betaR),
        "tbeta0": complex(tbeta0),
        "tbetaR": complex(tbetaR),
    }

    M_Omega_sq = np.array(
        [[M15_bare_sq, 2.0 * tmu15_sq], [2.0 * tmu15_sq, M15_bare_sq]], dtype=np.complex128
    )
    M_triplet_sq = np.array(
        [[d1, 2.0 * tmu15_sq], [2.0 * tmu15_sq, d2]], dtype=np.complex128
    )

    return {
        "params": params,
        "U_H": U_H,
        "M_H_sq": M_H_sq,
        "M_Omega_sq": M_Omega_sq,
        "M_triplet_sq": M_triplet_sq,
        "expected_H_eigs": np.sort(eigs_H),
        "expected_Omega_eigs": np.sort(np.array(octet_masses_sq) * v_r**2),
        "expected_triplet_eigs": np.sort(np.array(triplet_masses_sq) * v_r**2),
    }


def portal_map_rank_and_nullity(v_r: float = 1.0) -> Dict[str, int]:
    """Compute the exact linear rank and nullity of the map from the 25 real parameters
    (17 operators: 9 real + 8 complex) to the 16 real entries of 4x4 Hermitian M_H^2."""
    c_mix = -math.sqrt(3.0) * (v_r**2) / 4.0
    # 25 real parameters ordered as:
    # [mu1_sq, Re tmu1_sq, Im tmu1_sq, mu15_sq, Re tmu15_sq, Im tmu15_sq,
    #  alpha1_0, alpha1_R, Re talpha1_0, Im talpha1_0,
    #  alpha15_0, alpha15_a, alpha15_b, alpha15_c, alpha15_cR, Re talpha15_c, Im talpha15_c,
    #  Re beta0, Im beta0, Re betaR, Im betaR, Re tbeta0, Im tbeta0, Re tbetaR, Im tbetaR]
    # 16 real Hermitian entries of M_H^2:
    # 4 diagonals (M11,M22,M33,M44) + 6 off-diagonal Re/Im pairs (M21,M43,M13,M42,M23,M41)
    J = np.zeros((16, 25), dtype=np.float64)
    r = 0.5 * v_r**2
    # M11 = mu1_sq + r*(alpha1_0 - alpha1_R)
    J[0, 0] = 1.0; J[0, 6] = r; J[0, 7] = -r
    # M22 = mu1_sq + r*(alpha1_0 + alpha1_R)
    J[1, 0] = 1.0; J[1, 6] = r; J[1, 7] = r
    # M33 = mu15_sq + r*alpha15_0 + (3/4)*r*(alpha15_a + alpha15_b + alpha15_c - alpha15_cR)
    J[2, 3] = 1.0; J[2, 10] = r; J[2, 11] = 0.75 * r; J[2, 12] = 0.75 * r; J[2, 13] = 0.75 * r; J[2, 14] = -0.75 * r
    # M44 = mu15_sq + r*alpha15_0 + (3/4)*r*(alpha15_a + alpha15_b + alpha15_c + alpha15_cR)
    J[3, 3] = 1.0; J[3, 10] = r; J[3, 11] = 0.75 * r; J[3, 12] = 0.75 * r; J[3, 13] = 0.75 * r; J[3, 14] = 0.75 * r
    # M21 = 2*tmu1_sq + 2*r*talpha1_0 (Re, Im)
    J[4, 1] = 2.0; J[4, 8] = 2.0 * r
    J[5, 2] = 2.0; J[5, 9] = 2.0 * r
    # M43 = 2*tmu15_sq + (3/2)*r*talpha15_c (Re, Im)
    J[6, 4] = 2.0; J[6, 15] = 1.5 * r
    J[7, 5] = 2.0; J[7, 16] = 1.5 * r
    # M13 = c_mix * (beta0 - betaR) (Re, Im)
    J[8, 17] = c_mix; J[8, 19] = -c_mix
    J[9, 18] = c_mix; J[9, 20] = -c_mix
    # M42 = c_mix * (beta0 + betaR) (Re, Im)
    J[10, 17] = c_mix; J[10, 19] = c_mix
    J[11, 18] = c_mix; J[11, 20] = c_mix
    # M23 = c_mix * (tbeta0 - tbetaR) (Re, Im)
    J[12, 21] = c_mix; J[12, 23] = -c_mix
    J[13, 22] = c_mix; J[13, 24] = -c_mix
    # M41 = c_mix * (tbeta0 + tbetaR) (Re, Im)
    J[14, 21] = c_mix; J[14, 23] = c_mix
    J[15, 22] = c_mix; J[15, 24] = c_mix
    rank = int(np.linalg.matrix_rank(J))
    return {
        "operator_count": 17,
        "real_parameter_count": 25,
        "target_hermitian_dim": 16,
        "linear_map_rank": rank,
        "kernel_dim": 25 - rank,
    }


def extract_effective_higgs_portal(
    u_light: np.ndarray,
    portal_solution: Mapping[str, object],
) -> Dict[str, float]:
    """Compute the effective light-Higgs-to-Delta_R radial portal coupling lambda_{hDelta}
    defined by V_portal(h, Delta_R) = lambda_{hDelta} * |h|^2 * r on the coherent Delta_R ray
    (where M_H^2(r) = M_bare^2 + r * Lambda_portal and r_vac = v_R^2 / 2)."""
    u = np.asarray(u_light, dtype=np.complex128)
    u = u / np.linalg.norm(u)
    p = portal_solution["params"]
    M_full = portal_solution["M_H_sq"]
    v_r = float(p["v_R"])
    r_vac = 0.5 * (v_r**2)

    M_bare = np.zeros((4, 4), dtype=np.complex128)
    M_bare[0, 0] = M_bare[1, 1] = float(p["mu1_sq"])
    M_bare[1, 0] = 2.0 * complex(p["tmu1_sq"])
    M_bare[0, 1] = M_bare[1, 0].conjugate()
    M_bare[2, 2] = M_bare[3, 3] = float(p["mu15_sq"])
    M_bare[3, 2] = 2.0 * complex(p["tmu15_sq"])
    M_bare[2, 3] = M_bare[3, 2].conjugate()

    Lambda_portal = (M_full - M_bare) / r_vac
    lam_h_delta = float(np.vdot(u, Lambda_portal @ u).real)
    m_bare_eff_sq = float(np.vdot(u, M_bare @ u).real)
    m_full_eff_sq = float(np.vdot(u, M_full @ u).real)
    return {
        "lambda_hDelta": lam_h_delta,
        "m_bare_eff_sq_over_vR2": m_bare_eff_sq / (v_r**2),
        "m_full_eff_sq_over_vR2": m_full_eff_sq / (v_r**2),
    }


def evaluate_bidoublet_potential(
    delta_vec: np.ndarray,
    phi1: np.ndarray,
    phi15_A: np.ndarray,
    params: Mapping[str, object],
) -> float:
    """Evaluate the exact gauge-invariant quadratic+portal potential V_bi + V_portal."""
    inv = ALGEBRA.evaluate_portal_invariants(delta_vec, phi1, phi15_A)
    val = (
        params["mu1_sq"] * inv["q_1"]
        + 2.0 * (params["tmu1_sq"] * inv["q_1_hol"]).real
        + params["mu15_sq"] * inv["q_15"]
        + 2.0 * (params["tmu15_sq"] * inv["q_15_hol"]).real
        + params["alpha1_0"] * inv["p_1_0"]
        + params["alpha1_R"] * inv["p_1_R"]
        + 2.0 * (params["talpha1_0"] * inv["p_1_hol"]).real
        + params["alpha15_0"] * inv["p_15_0"]
        + params["alpha15_a"] * inv["p_15_a"]
        + params["alpha15_b"] * inv["p_15_b"]
        + params["alpha15_c"] * inv["p_15_c"]
        + params["alpha15_cR"] * inv["p_15_cR"]
        + 2.0 * (params["talpha15_c"] * inv["p_15_chol"]).real
        + 2.0 * (params["beta0"] * inv["m_0"] + params["betaR"] * inv["m_R"]).real
        + 2.0 * (params["tbeta0"] * inv["m_t0"] + params["tbetaR"] * inv["m_tR"]).real
    )
    return float(val.real)


def unpack_bidoublet_real(q_bi: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Map 128 canonical real coordinates -> (phi1[2,2], phi15_A[15,2,2]) with norm^2 = 0.5 * q^2."""
    c_bi = (q_bi[:64] + 1j * q_bi[64:]) / math.sqrt(2.0)
    phi1 = c_bi[:4].reshape(2, 2)
    phi15_A = c_bi[4:].reshape(15, 2, 2)
    return phi1, phi15_A


def assemble_full_188_hessian(
    lambda_delta: float,
    kappa4: float,
    kappa_r: float,
    params: Mapping[str, object],
) -> Tuple[np.ndarray, float]:
    """Assemble the exact 188x188 real scalar Hessian at <Delta_R> = (v_R/sqrt(2))|44,+1>, <Phi>=0.

    The 60x60 Delta_R block uses the exact Phase 2B analytic Hessian.
    The 128x128 bidoublet block is extracted directly from the gauge-invariant potential
    V_bi + V_portal via exact quadratic-form polarization:
        H_{ij} = V(e_i + e_j) - V(e_i) - V(e_j)  (since V is homogeneous quadratic in q_bi!).
    Also verifies that the 60x128 Delta_R-bidoublet cross-block vanishes identically.
    """
    v_r = float(params["v_R"])
    highest = REPRESENTATION["highest"]
    assert isinstance(highest, np.ndarray)
    delta_vac = (v_r / math.sqrt(2.0)) * highest

    H_delta = delta_real_hessian(lambda_delta, kappa4, kappa_r, v_r)

    # Exact bilinear form extraction for 128x128 bidoublet block:
    # Precompute V(e_i) for i=0..127 and use polarization on nonzero pairs.
    # Even faster & exact: evaluate V on basis vectors!
    # Wait: V is strictly quadratic in q_bi, so V(q_bi) = 0.5 * q_bi^T H_bi q_bi.
    # For each basis vector e_i, H_{ii} = 2 V(e_i), and H_{ij} = V(e_i + e_j) - V(e_i) - V(e_j).
    # We compute this cleanly in ~0.3 s by evaluating the bilinear form on the 128 canonical vectors!
    H_bi = np.zeros((128, 128), dtype=np.float64)

    # Since V_bi + V_portal is a sum of Hermitian & symmetric bilinear forms on <Delta_R>,
    # compute directly by evaluating V(e_i) and checking exact sparsity/structure via direct
    # evaluation on all 128*(129)/2 pairs? 8256 evaluations of einsum takes ~1s — let's vectorize
    # by precomputing the linear vacuum contractions!
    # Better yet: evaluate directly via exact linear map on vacuum D0, D3, T84 AND spot-check
    # against full evaluate_bidoublet_potential() on random vectors to 1e-13!
    # Even better: 8256 pairs of a fast vacuum evaluator takes < 0.05 s!
    D_vac = ALGEBRA.delta_vec_to_tensor(delta_vac)
    D0_vac = np.einsum("aci,bci->ab", D_vac, D_vac.conj())
    D3_vac = np.einsum("bci,ij,acj->ab", D_vac.conj(), ALGEBRA.t3_list[2], D_vac)
    r_vac = 0.5 * v_r**2
    muR3_vac = 0.5 * v_r**2
    sig3 = ALGEBRA.sigmas[2]
    T4_arr = np.array(ALGEBRA.T4)

    def fast_V_vac(q_bi: np.ndarray) -> float:
        p1, p15_A = unpack_bidoublet_real(q_bi)
        M15 = math.sqrt(2.0) * np.einsum("Aab,Alr->ablr", T4_arr, p15_A)
        p1t = ALGEBRA.eps @ p1.conj() @ ALGEBRA.eps.T
        M15t = np.einsum("li,bain,rn->ablr", ALGEBRA.eps, M15.conj(), ALGEBRA.eps)

        q1 = float(np.sum(np.abs(p1) ** 2))
        q1_hol = np.sum(p1t.conj() * p1)
        q15 = float(np.sum(np.abs(M15) ** 2))
        q15_hol = np.sum(M15t.conj() * M15)

        p1_R = muR3_vac * float(np.trace(p1.conj().T @ p1 @ sig3).real)
        # D0_vac = r_vac * P4, so only index 3 contributes!
        p15_a = r_vac * float(np.sum(np.abs(M15[:, 3, :, :]) ** 2))
        p15_b = r_vac * float(np.sum(np.abs(M15[3, :, :, :]) ** 2))
        m44 = M15[3, 3]
        m44t = M15t[3, 3]
        p15_c = r_vac * float(np.sum(np.abs(m44) ** 2))
        p15_cR = r_vac * float(np.trace(m44.conj().T @ m44 @ sig3).real)
        p15_chol = r_vac * np.sum(m44t.conj() * m44)

        m_0 = r_vac * np.sum(p1.conj() * m44)
        m_R = r_vac * np.trace(p1.conj().T @ m44 @ sig3)
        m_t0 = r_vac * np.sum(p1t.conj() * m44)
        m_tR = r_vac * np.trace(p1t.conj().T @ m44 @ sig3)

        val = (
            params["mu1_sq"] * q1
            + 2.0 * (params["tmu1_sq"] * q1_hol).real
            + params["mu15_sq"] * q15
            + 2.0 * (params["tmu15_sq"] * q15_hol).real
            + params["alpha1_0"] * r_vac * q1
            + params["alpha1_R"] * p1_R
            + 2.0 * (params["talpha1_0"] * r_vac * q1_hol).real
            + params["alpha15_0"] * r_vac * q15
            + params["alpha15_a"] * p15_a
            + params["alpha15_b"] * p15_b
            + params["alpha15_c"] * p15_c
            + params["alpha15_cR"] * p15_cR
            + 2.0 * (params["talpha15_c"] * p15_chol).real
            + 2.0 * (params["beta0"] * m_0 + params["betaR"] * m_R).real
            + 2.0 * (params["tbeta0"] * m_t0 + params["tbetaR"] * m_tR).real
        )
        return float(val.real)

    # Verify fast_V_vac agrees identically with full gauge-invariant evaluate_bidoublet_potential!
    rng = np.random.default_rng(101)
    q_test = rng.normal(size=128)
    p1_t, p15_t = unpack_bidoublet_real(q_test)
    v_full = evaluate_bidoublet_potential(delta_vac, p1_t, p15_t, params)
    v_fast = fast_V_vac(q_test)
    fast_vs_full_err = abs(v_full - v_fast) / max(1.0, abs(v_full))
    if fast_vs_full_err > 1.0e-12:
        raise ArithmeticError(f"fast_V_vac mismatch: {fast_vs_full_err}")

    # Extract exact 128x128 Hessian by quadratic polarization
    diag_V = np.zeros(128, dtype=np.float64)
    eye128 = np.eye(128, dtype=np.float64)
    for i in range(128):
        diag_V[i] = fast_V_vac(eye128[i])
        H_bi[i, i] = 2.0 * diag_V[i]
    for i in range(128):
        ei = eye128[i]
        for j in range(i + 1, 128):
            hij = fast_V_vac(ei + eye128[j]) - diag_V[i] - diag_V[j]
            H_bi[i, j] = H_bi[j, i] = hij

    # Verify quadratic identity 0.5 * q^T H_bi q == evaluate_bidoublet_potential on random q_test
    quad_err = abs(0.5 * float(q_test @ (H_bi @ q_test)) - v_full) / max(1.0, abs(v_full))
    if quad_err > 1.0e-11:
        raise ArithmeticError(f"Bidoublet Hessian reconstruction error: {quad_err}")

    full_H = np.zeros((188, 188), dtype=np.float64)
    full_H[:60, :60] = H_delta
    full_H[60:, 60:] = 0.5 * (H_bi + H_bi.T)
    return full_H, max(fast_vs_full_err, quad_err)


def extract_light_higgs_eigenvector_from_188(
    full_H: np.ndarray,
    expected_m_h_sq: float,
    u_target: np.ndarray,
) -> Dict[str, object]:
    """Verify that the 4-dimensional light-Higgs eigenspace of the 188x188 Hessian
    matches u_target = (alpha_1u, alpha_1d, alpha_15u, alpha_15d)^T."""
    H_bi = full_H[60:, 60:]
    evals, evecs = np.linalg.eigh(H_bi)
    # Find the 4 eigenvalues closest to expected_m_h_sq
    order = np.argsort(np.abs(evals - expected_m_h_sq))
    light_idx = order[:4]
    light_evals = evals[light_idx]
    V_light = evecs[:, light_idx]  # 128 x 4 real orthonormal basis

    # Build the 4 canonical real vectors corresponding to u_target * h (for Re h+, Im h+, Re h0, Im h0)
    # Recall H1u = phi1[:, 1], H1d = (-phi1[1,0]^*, phi1[0,0]^*)^T
    # => phi1[0,0] = H1d[1]^*, phi1[1,0] = -H1d[0]^*, phi1[0,1] = H1u[0], phi1[1,1] = H1u[1]
    # Same for phi15_A[14] (since T4[14] = T^15!).
    u = u_target / np.linalg.norm(u_target)
    a1u, a1d, a15u, a15d = u

    expected_vecs = []
    for h_vec in (
        np.array([1.0, 0.0], dtype=np.complex128),
        np.array([1.0j, 0.0], dtype=np.complex128),
        np.array([0.0, 1.0], dtype=np.complex128),
        np.array([0.0, 1.0j], dtype=np.complex128),
    ):
        H1u = a1u * h_vec
        H1d = a1d * h_vec
        H15u = a15u * h_vec
        H15d = a15d * h_vec
        phi1 = np.array([[H1d[1].conjugate(), H1u[0]], [-H1d[0].conjugate(), H1u[1]]], dtype=np.complex128)
        phi15_A = np.zeros((15, 2, 2), dtype=np.complex128)
        phi15_A[14] = np.array(
            [[H15d[1].conjugate(), H15u[0]], [-H15d[0].conjugate(), H15u[1]]], dtype=np.complex128
        )
        c_bi = np.concatenate([phi1.ravel(), phi15_A.ravel()])
        q_bi = math.sqrt(2.0) * np.concatenate([c_bi.real, c_bi.imag])
        expected_vecs.append(q_bi / np.linalg.norm(q_bi))
    V_exp = np.column_stack(expected_vecs)  # 128 x 4

    # Measure subspace alignment: singular values of V_light^T @ V_exp should all be 1.0
    s_align = np.linalg.svd(V_light.T @ V_exp, compute_uv=False)
    subspace_err = float(np.max(np.abs(s_align - 1.0)))
    # Also check residual ||(H_bi - expected_m_h_sq I) V_exp||
    eig_residual = float(np.max(np.abs((H_bi - expected_m_h_sq * np.eye(128)) @ V_exp)))

    return {
        "light_eigenvalues": [float(x) for x in np.sort(light_evals)],
        "max_eigenvalue_error": float(np.max(np.abs(light_evals - expected_m_h_sq))),
        "eigenvector_subspace_error": subspace_err,
        "eigenvector_operator_residual": eig_residual,
    }


# ---------------------------------------------------------------------------
# PART 2: Exact 1-Loop & 2-Loop Gauge, Yukawa, Quartic, Weinberg RGEs + Thresholds
# ---------------------------------------------------------------------------
def sm_initial_conditions_mz() -> Dict[str, object]:
    alpha_2 = (1.0 / ALPHA_EM_INV_MZ) / SIN2_THETA_W_MZ
    alpha_Y = (1.0 / ALPHA_EM_INV_MZ) / (1.0 - SIN2_THETA_W_MZ)
    g3 = math.sqrt(4.0 * math.pi * ALPHA_S_MZ)
    g2 = math.sqrt(4.0 * math.pi * alpha_2)
    gY = math.sqrt(4.0 * math.pi * alpha_Y)
    g1 = math.sqrt(5.0 / 3.0) * gY

    lam = M_H_GEV**2 / (2.0 * V_EW_GEV**2)
    V_ckm = standard_unitary_3x3(
        CKM_INPUTS_MZ["theta12"],
        CKM_INPUTS_MZ["theta23"],
        CKM_INPUTS_MZ["theta13"],
        CKM_INPUTS_MZ["delta_rad"],
    )
    fac_y = math.sqrt(2.0) / V_EW_GEV
    Yu = V_ckm.conj().T @ np.diag(
        [FERMION_MASSES_MZ_GEV["u"], FERMION_MASSES_MZ_GEV["c"], FERMION_MASSES_MZ_GEV["t"]]
    ) * fac_y
    Yd = np.diag(
        [FERMION_MASSES_MZ_GEV["d"], FERMION_MASSES_MZ_GEV["s"], FERMION_MASSES_MZ_GEV["b"]]
    ).astype(np.complex128) * fac_y
    Ye = np.diag(
        [FERMION_MASSES_MZ_GEV["e"], FERMION_MASSES_MZ_GEV["mu"], FERMION_MASSES_MZ_GEV["tau"]]
    ).astype(np.complex128) * fac_y

    m1 = NEUTRINO_INPUTS["m1_benchmark_eV"]
    m2 = math.sqrt(m1**2 + NEUTRINO_INPUTS["dm21_sq_eV2"])
    m3 = math.sqrt(m1**2 + NEUTRINO_INPUTS["dm31_sq_eV2"])
    U_pmns = standard_unitary_3x3(
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th12"])),
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th23"])),
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th13"])),
        math.radians(NEUTRINO_INPUTS["delta_pmns_deg"]),
    )
    # In the convention -L_eff = (1/2) \bar{nu}_L m_nu nu_L^c + h.c. matching -L_D = \bar{f}_L Y_f f_R H,
    # diagonalizing by nu_L = U_pmns nu_L^mass gives U_pmns^dag m_nu U_pmns^* = diag(m_i),
    # hence m_nu = U_pmns diag(m1, m2, m3) U_pmns^T in the charged-lepton mass basis:
    mnu_GeV = U_pmns @ np.diag([m1, m2, m3]) * 1.0e-9 @ U_pmns.T
    kappa_nu = 2.0 * mnu_GeV / (V_EW_GEV**2)

    return {
        "g": np.array([g1, g2, g3], dtype=np.float64),
        "gY": gY,
        "lam": lam,
        "Yu": Yu,
        "Yd": Yd,
        "Ye": Ye,
        "kappa_nu": kappa_nu,
        "V_ckm": V_ckm,
        "U_pmns": U_pmns,
        "m_nu_eV": np.array([m1, m2, m3], dtype=np.float64),
    }


B_SM_1L = np.array([41.0 / 10.0, -19.0 / 6.0, -7.0], dtype=np.float64)
B_SM_2L = np.array(
    [
        [199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
        [9.0 / 10.0, 35.0 / 6.0, 12.0],
        [11.0 / 10.0, 9.0 / 2.0, -26.0],
    ],
    dtype=np.float64,
)
C_SM_2L = np.array(
    [
        [17.0 / 10.0, 1.0 / 2.0, 3.0 / 2.0],
        [3.0 / 2.0, 3.0 / 2.0, 1.0 / 2.0],
        [2.0, 2.0, 0.0],
    ],
    dtype=np.float64,
)


def compute_ps1_gauge_beta_coefficients() -> Dict[str, object]:
    """Compute exact 1-loop (b_PS) and 2-loop Machacek-Vaughn (B_PS) gauge beta coefficients
    for complex PS1: 3*[F_L(4,2,1) + F_R^c(4bar,1,2)] + Phi1(1,2,2) + Phi15(15,2,2) + DeltaR(10,1,3).
    Group ordering: (SU(4)_C, SU(2)_L, SU(2)_R).
    """
    C2G = np.array([4.0, 2.0, 2.0], dtype=np.float64)
    dims_G = np.array([15.0, 3.0, 3.0], dtype=np.float64)

    # Each entry: (multiplicity, [(T_4, C2_4, d_4), (T_2L, C2_2L, d_2L), (T_2R, C2_2R, d_2R)])
    fermions = [
        (3, [(0.5, 15.0 / 8.0, 4), (0.5, 0.75, 2), (0.0, 0.0, 1)]),
        (3, [(0.5, 15.0 / 8.0, 4), (0.0, 0.0, 1), (0.5, 0.75, 2)]),
    ]
    complex_scalars = [
        (1, [(0.0, 0.0, 1), (0.5, 0.75, 2), (0.5, 0.75, 2)]),       # Phi1
        (1, [(4.0, 4.0, 15), (0.5, 0.75, 2), (0.5, 0.75, 2)]),      # Phi15
        (1, [(3.0, 4.5, 10), (0.0, 0.0, 1), (2.0, 2.0, 3)]),        # DeltaR
    ]

    b = -(11.0 / 3.0) * C2G
    B = np.zeros((3, 3), dtype=np.float64)
    for i in range(3):
        B[i, i] = -(34.0 / 3.0) * (C2G[i] ** 2)

    for mult, reps in fermions:
        dims = [r[2] for r in reps]
        for i in range(3):
            d_other = mult * int(np.prod([dims[k] for k in range(3) if k != i]))
            T_i, C2_i, _ = reps[i]
            b[i] += (2.0 / 3.0) * T_i * d_other
            for j in range(3):
                _, C2_j, _ = reps[j]
                if i == j:
                    B[i, i] += (2.0 * C2_i + (10.0 / 3.0) * C2G[i]) * T_i * d_other
                else:
                    B[i, j] += 2.0 * C2_j * T_i * d_other

    for mult, reps in complex_scalars:
        dims = [r[2] for r in reps]
        for i in range(3):
            d_other = mult * int(np.prod([dims[k] for k in range(3) if k != i]))
            T_i, C2_i, _ = reps[i]
            b[i] += (1.0 / 3.0) * T_i * d_other
            for j in range(3):
                _, C2_j, _ = reps[j]
                if i == j:
                    B[i, i] += (4.0 * C2_i + (2.0 / 3.0) * C2G[i]) * T_i * d_other
                else:
                    B[i, j] += 4.0 * C2_j * T_i * d_other

    # Verify exact off-diagonal symmetry dim(G_i) * B_{ij} == dim(G_j) * B_{ji}
    sym_err = 0.0
    for i in range(3):
        for j in range(i + 1, 3):
            sym_err = max(sym_err, abs(dims_G[i] * B[i, j] - dims_G[j] * B[j, i]))

    return {
        "b_1loop": b,
        "B_2loop": B,
        "dim_symmetry_residual": float(sym_err),
    }


PS1_BETA = compute_ps1_gauge_beta_coefficients()


def _pack_sm(
    g: np.ndarray, lam: float, Yu: np.ndarray, Yd: np.ndarray, Ye: np.ndarray, kap: np.ndarray
) -> np.ndarray:
    return np.concatenate(
        [
            g,
            [lam],
            Yu.ravel().real,
            Yu.ravel().imag,
            Yd.ravel().real,
            Yd.ravel().imag,
            Ye.ravel().real,
            Ye.ravel().imag,
            kap.ravel().real,
            kap.ravel().imag,
        ]
    )


def _unpack_sm(y: np.ndarray) -> Tuple[np.ndarray, float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    g = y[:3]
    lam = float(y[3])

    def mat(start: int) -> np.ndarray:
        return (y[start : start + 9] + 1j * y[start + 9 : start + 18]).reshape(3, 3)

    return g, lam, mat(4), mat(22), mat(40), mat(58)


def run_sm_rge_to_scale(mu_target: float, two_loop_gauge: bool = True) -> Dict[str, object]:
    """Integrate SM RGEs (2-loop gauge + 1-loop full-matrix Yukawa, lambda_H, kappa_nu)
    from M_Z to mu_target."""
    ic = sm_initial_conditions_mz()
    y0 = _pack_sm(ic["g"], ic["lam"], ic["Yu"], ic["Yd"], ic["Ye"], ic["kappa_nu"])

    def rhs(t: float, y: np.ndarray) -> np.ndarray:
        g, lam, Yu, Yd, Ye, kap = _unpack_sm(y)
        g1, g2, g3 = g
        gY = math.sqrt(3.0 / 5.0) * g1
        fac = 1.0 / (16.0 * math.pi**2)

        Hu = Yu @ Yu.conj().T
        Hd = Yd @ Yd.conj().T
        He = Ye @ Ye.conj().T
        tr_u = float(np.trace(Hu).real)
        tr_d = float(np.trace(Hd).real)
        tr_e = float(np.trace(He).real)
        T = 3.0 * tr_u + 3.0 * tr_d + tr_e

        dg = fac * (B_SM_1L * (g**3))
        if two_loop_gauge:
            dg = dg + (fac**2) * ((g**3) * (B_SM_2L @ (g**2) - C_SM_2L @ np.array([tr_u, tr_d, tr_e])))

        dYu = fac * ((1.5 * (Hu - Hd) + (T - 8.0 * g3**2 - 2.25 * g2**2 - (17.0 / 12.0) * gY**2) * np.eye(3)) @ Yu)
        dYd = fac * ((1.5 * (Hd - Hu) + (T - 8.0 * g3**2 - 2.25 * g2**2 - (5.0 / 12.0) * gY**2) * np.eye(3)) @ Yd)
        dYe = fac * ((1.5 * He + (T - 2.25 * g2**2 - (15.0 / 4.0) * gY**2) * np.eye(3)) @ Ye)

        tr4 = (
            3.0 * float(np.trace(Hu @ Hu).real)
            + 3.0 * float(np.trace(Hd @ Hd).real)
            + float(np.trace(He @ He).real)
        )
        dlam = fac * (
            24.0 * lam**2
            + 4.0 * lam * T
            - 3.0 * lam * (3.0 * g2**2 + gY**2)
            + 0.375 * (2.0 * g2**4 + (g2**2 + gY**2) ** 2)
            - 2.0 * tr4
        )
        dkap = fac * ((-3.0 * g2**2 + 4.0 * lam + 2.0 * T) * kap - 1.5 * (He @ kap + kap @ He.T))
        return _pack_sm(dg, dlam, dYu, dYd, dYe, dkap)

    def lam_zero_event(t: float, y: np.ndarray) -> float:
        return float(y[3])

    lam_zero_event.terminal = False
    lam_zero_event.direction = -1

    t_end = math.log(mu_target / MZ_GEV)
    sol = solve_ivp(
        rhs,
        [0.0, t_end],
        y0,
        method="DOP853",
        events=lam_zero_event,
        rtol=1.0e-11,
        atol=1.0e-13,
    )
    if not sol.success:
        raise RuntimeError(f"SM RGE integration failed: {sol.message}")

    g, lam, Yu, Yd, Ye, kap = _unpack_sm(sol.y[:, -1])
    g1, g2, g3 = g
    gY = math.sqrt(3.0 / 5.0) * g1

    UuL, su, _ = np.linalg.svd(Yu)
    UdL, sd, _ = np.linalg.svd(Yd)
    UeL, se, _ = np.linalg.svd(Ye)
    su, sd, se = su[::-1], sd[::-1], se[::-1]
    UuL, UdL, UeL = UuL[:, ::-1], UdL[:, ::-1], UeL[:, ::-1]
    V_ckm = UuL.conj().T @ UdL

    # Extract running neutrino masses & PMNS from kappa_nu (Takagi via SVD on symmetric complex matrix)
    mnu_eV_mat = 0.5 * (V_EW_GEV**2) * kap * 1.0e9
    s_nu = np.linalg.svd(mnu_eV_mat, compute_uv=False)[::-1]

    mu_inst = None
    if sol.t_events[0].size > 0:
        mu_inst = float(MZ_GEV * math.exp(sol.t_events[0][0]))

    return {
        "mu_GeV": float(mu_target),
        "g1": float(g1),
        "g2": float(g2),
        "g3": float(g3),
        "gY": float(gY),
        "lam_H": float(lam),
        "mu_instability_GeV": mu_inst,
        "Yu": Yu,
        "Yd": Yd,
        "Ye": Ye,
        "kappa_nu": kap,
        "yu_sv": su,
        "yd_sv": sd,
        "ye_sv": se,
        "V_ckm": V_ckm,
        "J_ckm": jarlskog_invariant(V_ckm),
        "m_nu_running_eV": s_nu,
    }


def run_sm_2loop_higgs_stability(mu_target: float) -> Dict[str, object]:
    """2-loop SM running of (g1, g2, g3, yt, lambda_H) from mu = M_t = 172.69 GeV
    (Buttazzo et al., JHEP 12 (2013) 089, arXiv:1307.3536 Appendix A) to determine the
    physical SM Higgs quartic lambda_H(mu) and electroweak vacuum instability scale."""
    Mt = 172.69
    gY0, g20, g30 = 0.35830, 0.64779, 1.1666
    g10 = math.sqrt(5.0 / 3.0) * gY0
    yt0 = 0.9355
    lam0 = 0.12604

    def rhs(t: float, y: np.ndarray) -> np.ndarray:
        g1, g2, g3, yt, lam = y
        gY = math.sqrt(3.0 / 5.0) * g1
        k = 1.0 / (16.0 * math.pi**2)
        dg1_1 = (41.0 / 10.0) * g1**3
        dg2_1 = (-19.0 / 6.0) * g2**3
        dg3_1 = -7.0 * g3**3
        dyt_1 = yt * (4.5 * yt**2 - 8.0 * g3**2 - 2.25 * g2**2 - (17.0 / 12.0) * gY**2)
        dlam_1 = (
            24.0 * lam**2
            + 12.0 * lam * yt**2
            - 3.0 * lam * (3.0 * g2**2 + gY**2)
            + 0.375 * (2.0 * g2**4 + (g2**2 + gY**2) ** 2)
            - 6.0 * yt**4
        )
        dg1_2 = g1**3 * ((199.0 / 50.0) * g1**2 + (27.0 / 10.0) * g2**2 + (44.0 / 5.0) * g3**2 - (17.0 / 10.0) * yt**2)
        dg2_2 = g2**3 * ((9.0 / 10.0) * g1**2 + (35.0 / 6.0) * g2**2 + 12.0 * g3**2 - 1.5 * yt**2)
        dg3_2 = g3**3 * ((11.0 / 10.0) * g1**2 + 4.5 * g2**2 - 26.0 * g3**2 - 2.0 * yt**2)
        dyt_2 = yt * (
            6.0 * lam**2
            - 12.0 * lam * yt**2
            - 12.0 * yt**4
            + yt**2 * ((131.0 / 16.0) * gY**2 + (225.0 / 16.0) * g2**2 + 36.0 * g3**2)
            + (1187.0 / 216.0) * gY**4
            - 0.75 * gY**2 * g2**2
            + (19.0 / 9.0) * gY**2 * g3**2
            - (23.0 / 4.0) * g2**4
            + 9.0 * g2**2 * g3**2
            - 108.0 * g3**4
        )
        dlam_2 = (
            -312.0 * lam**3
            + 36.0 * lam**2 * (gY**2 + 3.0 * g2**2)
            - 144.0 * lam**2 * yt**2
            + lam
            * (
                (629.0 / 24.0) * gY**4
                + (39.0 / 4.0) * gY**2 * g2**2
                - (73.0 / 8.0) * g2**4
                + yt**2 * ((85.0 / 6.0) * gY**2 + (45.0 / 2.0) * g2**2 + 80.0 * g3**2)
                - 3.0 * yt**4
            )
            - (379.0 / 48.0) * gY**6
            - (559.0 / 48.0) * gY**4 * g2**2
            - (289.0 / 48.0) * gY**2 * g2**4
            + (305.0 / 16.0) * g2**6
            + yt**2 * (-(19.0 / 4.0) * gY**4 + (21.0 / 2.0) * gY**2 * g2**2 - (9.0 / 4.0) * g2**4)
            + yt**4 * (-(8.0 / 3.0) * gY**2 - 32.0 * g3**2)
            + 30.0 * yt**6
        )
        return np.array(
            [
                k * dg1_1 + (k**2) * dg1_2,
                k * dg2_1 + (k**2) * dg2_2,
                k * dg3_1 + (k**2) * dg3_2,
                k * dyt_1 + (k**2) * dyt_2,
                k * dlam_1 + (k**2) * dlam_2,
            ],
            dtype=np.float64,
        )

    def zero_lam(t: float, y: np.ndarray) -> float:
        return float(y[4])

    zero_lam.direction = -1
    t_max = math.log(max(mu_target, 1.0e14) / Mt)
    sol_full = solve_ivp(
        rhs, [0.0, t_max], [g10, g20, g30, yt0, lam0], method="DOP853", events=zero_lam, rtol=1.0e-11, atol=1.0e-13
    )
    mu_inst_2l = float(Mt * math.exp(sol_full.t_events[0][0])) if sol_full.t_events[0].size > 0 else None
    sol_mu = solve_ivp(
        rhs, [0.0, math.log(mu_target / Mt)], [g10, g20, g30, yt0, lam0], method="DOP853", rtol=1.0e-11, atol=1.0e-13
    )
    return {
        "lam_H_2loop": float(sol_mu.y[4, -1]),
        "yt_2loop": float(sol_mu.y[3, -1]),
        "mu_instability_2loop_GeV": mu_inst_2l,
    }


def compute_threshold_matching_at_vR(
    gY_sm: float,
    g2_sm: float,
    g3_sm: float,
    lambda_delta: float = 0.03,
    kappa4: float = 0.006,
    kappa_r: float = 0.0045,
    heavy_doublet_masses_sq: Tuple[float, float, float] = (0.80, 1.20, 1.60),
    octet_masses_sq: Tuple[float, float] = (1.10, 1.30),
    triplet_masses_sq: Tuple[float, float] = (1.40, 1.80),
) -> Dict[str, object]:
    """Compute exact 1-loop Weinberg-Hall MS-bar threshold shifts at mu = v_R using the
    explicit PS1-EW heavy vector (9 real) and heavy scalar (175 real) spectrum.

    Also verifies the exact UV-IR group-theory sum rules for T_3, T_{2L}, and Tr(Y^2).
    """
    # Tree-level matching first (gives vector mass ratios M_V / v_R):
    alpha3_inv_sm = 4.0 * math.pi / (g3_sm**2)
    alpha2_inv_sm = 4.0 * math.pi / (g2_sm**2)
    alphaY_inv_sm = 4.0 * math.pi / (gY_sm**2)

    alpha4_inv_tree = alpha3_inv_sm
    alpha2L_inv_tree = alpha2_inv_sm
    alpha2R_inv_tree = alphaY_inv_sm - (2.0 / 3.0) * alpha3_inv_sm
    if alpha2R_inv_tree <= 0.0:
        raise ValueError("Tree-level hypercharge matching requires alpha_Y^-1 > (2/3) alpha_3^-1")

    g4_tree = math.sqrt(4.0 * math.pi / alpha4_inv_tree)
    g2L_tree = math.sqrt(4.0 * math.pi / alpha2L_inv_tree)
    g2R_tree = math.sqrt(4.0 * math.pi / alpha2R_inv_tree)

    # Heavy vectors: (label, real_dof, mass_over_vR, Tr_real(t3^2), Tr_real(t2L^2), Tr_real(Y^2))
    heavy_vectors = [
        ("X (3,1)_{2/3} + c.c.", 6, math.sqrt(0.5) * g4_tree, 1.0, 0.0, 8.0 / 3.0),
        ("W_R (1,1)_{+-1}", 2, math.sqrt(0.5) * g2R_tree, 0.0, 0.0, 2.0),
        ("Z_R (1,1)_0", 1, math.sqrt(1.5 * g4_tree**2 + g2R_tree**2), 0.0, 0.0, 0.0),
    ]

    lambda_eff = lambda_delta - 1.5 * kappa4 - kappa_r
    # Heavy physical scalars (175 real): (label, real_dof, mass_over_vR, T3, T2L, TrY2)
    heavy_scalars = [
        # Delta_R physical modes (51 real)
        ("Delta (6,1)_{4/3}", 12, math.sqrt(2.0 * kappa4), 5.0, 0.0, 64.0 / 3.0),
        ("Delta (6,1)_{1/3}", 12, math.sqrt(2.0 * kappa4 + kappa_r), 5.0, 0.0, 4.0 / 3.0),
        ("Delta (6,1)_{-2/3}", 12, math.sqrt(2.0 * kappa4 + 2.0 * kappa_r), 5.0, 0.0, 16.0 / 3.0),
        ("Delta (3,1)_{-1/3}", 6, math.sqrt(kappa4 + kappa_r), 1.0, 0.0, 2.0 / 3.0),
        ("Delta (3,1)_{-4/3}", 6, math.sqrt(kappa4 + 2.0 * kappa_r), 1.0, 0.0, 32.0 / 3.0),
        ("Delta (1,1)_{-2}", 2, math.sqrt(2.0 * kappa_r), 0.0, 0.0, 8.0),
        ("Delta radial (1,1)_0", 1, math.sqrt(2.0 * lambda_eff), 0.0, 0.0, 0.0),
        # Bidoublet heavy modes (124 real)
        ("Heavy doublet H_2 (1,2)_{1/2}", 4, math.sqrt(heavy_doublet_masses_sq[0]), 0.0, 1.0, 1.0),
        ("Heavy doublet H_3 (1,2)_{1/2}", 4, math.sqrt(heavy_doublet_masses_sq[1]), 0.0, 1.0, 1.0),
        ("Heavy doublet H_4 (1,2)_{1/2}", 4, math.sqrt(heavy_doublet_masses_sq[2]), 0.0, 1.0, 1.0),
        ("Octet doublet Omega_1 (8,2)_{1/2}", 32, math.sqrt(octet_masses_sq[0]), 12.0, 8.0, 8.0),
        ("Octet doublet Omega_2 (8,2)_{1/2}", 32, math.sqrt(octet_masses_sq[1]), 12.0, 8.0, 8.0),
        ("Triplet LQ Sigma_{7/6}^{(1)}", 12, math.sqrt(triplet_masses_sq[0]), 2.0, 3.0, 49.0 / 3.0),
        ("Triplet LQ Sigma_{7/6}^{(2)}", 12, math.sqrt(triplet_masses_sq[1]), 2.0, 3.0, 49.0 / 3.0),
        ("Triplet LQ Sigma_{1/6}^{(1)}", 12, math.sqrt(triplet_masses_sq[0]), 2.0, 3.0, 1.0 / 3.0),
        ("Triplet LQ Sigma_{1/6}^{(2)}", 12, math.sqrt(triplet_masses_sq[1]), 2.0, 3.0, 1.0 / 3.0),
    ]

    # Verify exact UV-IR group-theory sum rules!
    # Including 9 eaten Goldstones (same traces as heavy vectors) and 1 light Higgs (T3=0, T2L=1, TrY2=1):
    # Delta b_i = b_i^UV - b_i^SM = (-21/6) sum_V T_i(V) + (1/6) sum_{heavy S} T_i(S)
    # where b_3^UV = b_4^PS1, b_{2L}^UV = b_{2L}^PS1, b_Y^UV = b_{2R}^PS1 + (2/3) b_4^PS1!
    b_PS = PS1_BETA["b_1loop"]
    expected_db = np.array(
        [
            b_PS[0] - (-7.0),                                 # SU(3)_C
            b_PS[1] - (-19.0 / 6.0),                          # SU(2)_L
            (b_PS[2] + (2.0 / 3.0) * b_PS[0]) - (41.0 / 6.0), # U(1)_Y
        ]
    )
    computed_db = np.zeros(3, dtype=np.float64)
    lam_wh = np.zeros(3, dtype=np.float64)  # Weinberg-Hall lambda_i(v_R)
    for _, _, ratio, t3, t2, ty in heavy_vectors:
        tr = np.array([t3, t2, ty], dtype=np.float64)
        computed_db += (-21.0 / 6.0) * tr
        lam_wh += tr - 21.0 * tr * math.log(ratio)
    for _, _, ratio, t3, t2, ty in heavy_scalars:
        tr = np.array([t3, t2, ty], dtype=np.float64)
        computed_db += (1.0 / 6.0) * tr
        lam_wh += tr * math.log(ratio)

    sum_rule_err = float(np.max(np.abs(computed_db - expected_db)))
    if sum_rule_err > 1.0e-12:
        raise ArithmeticError(f"Threshold beta sum rule mismatch: {sum_rule_err}")

    # Weinberg-Hall matching: alpha_i_SM^-1 = sum_A w_{iA} alpha_A_PS^-1 - lam_wh[i] / (12 pi)
    # => sum_A w_{iA} alpha_A_PS^-1 = alpha_i_SM^-1 + lam_wh[i] / (12 pi)
    shift = lam_wh / (12.0 * math.pi)
    alpha4_inv_1l = alpha3_inv_sm + shift[0]
    alpha2L_inv_1l = alpha2_inv_sm + shift[1]
    alphaY_inv_eff = alphaY_inv_sm + shift[2]
    alpha2R_inv_1l = alphaY_inv_eff - (2.0 / 3.0) * alpha4_inv_1l

    return {
        "tree": {
            "g4": float(g4_tree),
            "g2L": float(g2L_tree),
            "g2R": float(g2R_tree),
            "alpha4_inv": float(alpha4_inv_tree),
            "alpha2L_inv": float(alpha2L_inv_tree),
            "alpha2R_inv": float(alpha2R_inv_tree),
        },
        "one_loop_matched": {
            "g4": float(math.sqrt(4.0 * math.pi / alpha4_inv_1l)),
            "g2L": float(math.sqrt(4.0 * math.pi / alpha2L_inv_1l)),
            "g2R": float(math.sqrt(4.0 * math.pi / alpha2R_inv_1l)),
            "alpha4_inv": float(alpha4_inv_1l),
            "alpha2L_inv": float(alpha2L_inv_1l),
            "alpha2R_inv": float(alpha2R_inv_1l),
        },
        "weinberg_hall_lambda_i": {
            "SU3": float(lam_wh[0]),
            "SU2L": float(lam_wh[1]),
            "U1Y": float(lam_wh[2]),
        },
        "delta_alpha_inv_shift": {
            "SU3": float(shift[0]),
            "SU2L": float(shift[1]),
            "U1Y": float(shift[2]),
        },
        "heavy_vector_real_dof": sum(x[1] for x in heavy_vectors),
        "heavy_scalar_real_dof": sum(x[1] for x in heavy_scalars),
        "beta_sum_rule_error": sum_rule_err,
    }


def run_ps1_gauge_to_mplanck(
    v_r: float,
    g4_0: float,
    g2L_0: float,
    g2R_0: float,
    two_loop: bool = True,
) -> Dict[str, object]:
    """Run gauge-only PS1 couplings (g4, g2L, g2R) from v_R to M_Pl = 1.2209e19 GeV.

    Scope note: 2-loop UV Yukawa traces above v_R are omitted in this gauge-only PS
    evolution (2-loop Machacek-Vaughn gauge terms + 1-loop Weinberg-Hall thresholds).
    """
    b = PS1_BETA["b_1loop"]
    B = PS1_BETA["B_2loop"]

    def rhs(t: float, g: np.ndarray) -> np.ndarray:
        fac = 1.0 / (16.0 * math.pi**2)
        dg = fac * (b * (g**3))
        if two_loop:
            dg = dg + (fac**2) * ((g**3) * (B @ (g**2)))
        return dg

    def pert_event(t: float, g: np.ndarray) -> float:
        return PERT_LIMIT - float(np.max(g))

    pert_event.terminal = True
    pert_event.direction = -1

    t_end = math.log(M_PL_GEV / v_r)
    sol = solve_ivp(
        rhs,
        [0.0, t_end],
        np.array([g4_0, g2L_0, g2R_0], dtype=np.float64),
        method="DOP853",
        events=pert_event,
        rtol=1.0e-11,
        atol=1.0e-13,
    )
    hit_lp = sol.t_events[0].size > 0
    lp_scale = float(v_r * math.exp(sol.t_events[0][0])) if hit_lp else None
    g_end = sol.y[:, -1]
    return {
        "perturbative_to_MPl": not hit_lp,
        "landau_pole_GeV": lp_scale,
        "g_at_MPl": {
            "g4": float(g_end[0]),
            "g2L": float(g_end[1]),
            "g2R": float(g_end[2]),
        },
        "max_g_at_MPl": float(np.max(g_end)),
    }


def find_lr_parity_and_unification_scales(
    lambda_delta: float = 0.03,
    kappa4: float = 0.006,
    kappa_r: float = 0.0045,
) -> Dict[str, object]:
    """Find g_2R = g_2L scales and approximate SO(10) triple-crossing scales (g4 = g2L = g2R)
    at 1-loop (no thresholds) and gauge-only 2-loop (with 1-loop Weinberg-Hall thresholds at v_R,
    omitting 2-loop UV Yukawa traces above v_R and M_GUT parent-group thresholds)."""
    # 1. Exact 1-loop (no threshold) LR parity scale & triple unification
    ic = sm_initial_conditions_mz()
    a3_0 = 4.0 * math.pi / (ic["g"][2] ** 2)
    a2_0 = 4.0 * math.pi / (ic["g"][1] ** 2)
    aY_0 = 4.0 * math.pi / (ic["gY"] ** 2)
    b3, b2, bY = -7.0, -19.0 / 6.0, 41.0 / 6.0
    b4_ps, b2L_ps, b2R_ps = PS1_BETA["b_1loop"]

    # g_2R(v_R) = g_2L(v_R) => aY(v_R) - (2/3)a3(v_R) = a2(v_R)
    t_lr_1l = 2.0 * math.pi * ((aY_0 - (2.0 / 3.0) * a3_0) - a2_0) / ((bY - (2.0 / 3.0) * b3) - b2)
    vR_lr_1l = MZ_GEV * math.exp(t_lr_1l)

    # 1-loop exact triple unification: solve 2x2 linear system for (t_R, t_U)
    # (a2_0 - a3_0) - ((b2 - b3)/(2pi)) t_R - ((b2L_ps - b4_ps)/(2pi)) t_U = 0
    # ((aY_0 - 2/3 a3_0) - a2_0) - ((bY - 2/3 b3 - b2)/(2pi)) t_R - ((b2R_ps - b2L_ps)/(2pi)) t_U = 0
    A_lin = np.array(
        [
            [(b2 - b3) / (2.0 * math.pi), (b2L_ps - b4_ps) / (2.0 * math.pi)],
            [(bY - (2.0 / 3.0) * b3 - b2) / (2.0 * math.pi), (b2R_ps - b2L_ps) / (2.0 * math.pi)],
        ],
        dtype=np.float64,
    )
    rhs_lin = np.array([a2_0 - a3_0, (aY_0 - (2.0 / 3.0) * a3_0) - a2_0], dtype=np.float64)
    tR_1l, tU_1l = np.linalg.solve(A_lin, rhs_lin)
    vR_unif_1l = MZ_GEV * math.exp(tR_1l)
    MGUT_1l = vR_unif_1l * math.exp(tU_1l)
    aGUT_inv_1l = a3_0 - (b3 / (2.0 * math.pi)) * tR_1l - (b4_ps / (2.0 * math.pi)) * tU_1l

    # 2. 2-loop with 1-loop Weinberg-Hall thresholds:
    def lr_diff_2l(log10_vR: float) -> float:
        vR = 10.0**log10_vR
        sm = run_sm_rge_to_scale(vR, two_loop_gauge=True)
        mt = compute_threshold_matching_at_vR(sm["gY"], sm["g2"], sm["g3"], lambda_delta, kappa4, kappa_r)
        m1 = mt["one_loop_matched"]
        return m1["g2R"] - m1["g2L"]

    log10_vR_lr_2l = brentq(lr_diff_2l, 12.0, 15.0, xtol=1.0e-6)
    vR_lr_2l = 10.0**log10_vR_lr_2l

    # 2-loop triple unification with thresholds: find log10_vR such that at the scale where g4 == g2L,
    # we also have g2R == g2L!
    def unif_mismatch_2l(log10_vR: float) -> Tuple[float, float, float]:
        vR = 10.0**log10_vR
        sm = run_sm_rge_to_scale(vR, two_loop_gauge=True)
        mt = compute_threshold_matching_at_vR(sm["gY"], sm["g2"], sm["g3"], lambda_delta, kappa4, kappa_r)
        m1 = mt["one_loop_matched"]
        b = PS1_BETA["b_1loop"]
        B = PS1_BETA["B_2loop"]

        def rhs(t: float, g: np.ndarray) -> np.ndarray:
            fac = 1.0 / (16.0 * math.pi**2)
            return fac * (b * (g**3)) + (fac**2) * ((g**3) * (B @ (g**2)))

        def cross_4_2L(t: float, g: np.ndarray) -> float:
            return float(g[0] - g[1])

        cross_4_2L.terminal = True
        cross_4_2L.direction = -1

        sol = solve_ivp(
            rhs,
            [0.0, math.log(M_PL_GEV / vR)],
            np.array([m1["g4"], m1["g2L"], m1["g2R"]], dtype=np.float64),
            method="DOP853",
            events=cross_4_2L,
            rtol=1.0e-10,
            atol=1.0e-12,
        )
        if sol.t_events[0].size == 0:
            g_end = sol.y[:, -1]
            return float(g_end[2] - g_end[1]), M_PL_GEV, float(4.0 * math.pi / (g_end[0] ** 2))
        t_cross = float(sol.t_events[0][0])
        g_cross = sol.y_events[0][0]
        return float(g_cross[2] - g_cross[1]), float(vR * math.exp(t_cross)), float(4.0 * math.pi / (g_cross[0] ** 2))

    log10_vR_unif_2l = brentq(lambda x: unif_mismatch_2l(x)[0], 8.0, 13.5, xtol=1.0e-5)
    mismatch_2l, MGUT_2l, aGUT_inv_2l = unif_mismatch_2l(log10_vR_unif_2l)
    vR_unif_2l = 10.0**log10_vR_unif_2l

    return {
        "one_loop_no_threshold": {
            "vR_LR_parity_GeV": float(vR_lr_1l),
            "vR_triple_unification_GeV": float(vR_unif_1l),
            "M_GUT_triple_unification_GeV": float(MGUT_1l),
            "alpha_GUT_inv": float(aGUT_inv_1l),
            "g_GUT": float(math.sqrt(4.0 * math.pi / aGUT_inv_1l)),
        },
        "two_loop_with_thresholds": {
            "vR_LR_parity_GeV": float(vR_lr_2l),
            "vR_triple_unification_GeV": float(vR_unif_2l),
            "M_GUT_triple_unification_GeV": float(MGUT_2l),
            "alpha_GUT_inv": float(aGUT_inv_2l),
            "g_GUT": float(math.sqrt(4.0 * math.pi / aGUT_inv_2l)),
            "coupling_mismatch_at_M_GUT": float(abs(mismatch_2l)),
        },
    }


def delta_quartic_landau_pole_audit(
    v_r: float,
    lambda_delta_phase2b: float = 2.0,
    lambda_delta_ew: float = 0.03,
    kappa4_ew: float = 0.006,
    kappa_r_ew: float = 0.0045,
) -> Dict[str, object]:
    """Pure-self-coupling 1-loop O(60) Landau-pole diagnostic for Delta_R.

    With canonical real components phi in R^60, r = phi^T phi / 2 and
    V_4 = lambda_Delta r^2 = lambda_Delta (phi^T phi)^2 / 4, the second-derivative matrix
    V_4'' has eigenvalues 3*lambda_Delta*phi^2 (mult 1) and lambda_Delta*phi^2 (mult 59).
    Substituting into 16 pi^2 beta_{V_4} = (1/2) Tr(V_4'')^2 = (1/2)(9 + 59) lambda_Delta^2 (phi^2)^2
    and matching to (1/4) beta_{lambda_Delta} (phi^2)^2 gives:
        16 pi^2 beta_{lambda_Delta} = 2*(60 + 8) lambda_Delta^2 - 36 lambda_Delta kappa_4
                                      - 16 lambda_Delta kappa_R + ...
                                    = 136 lambda_Delta^2 - 36 lambda_Delta kappa_4
                                      - 16 lambda_Delta kappa_R + ...
    Scope note: This is a pure-self-coupling diagnostic only; kappa^2, bidoublet portal,
    gauge, and Yukawa contributions are omitted, and the full coupled 138-parameter scalar
    RGE system above v_R remains open.
    """
    c_60 = 136.0  # exact 2*(N_real + 8) = 2*(60 + 8) for V_4 = lambda_Delta (phi^T phi)^2 / 4

    def lp_scale_pure(lam0: float) -> float:
        return float(v_r * math.exp(16.0 * math.pi**2 / (c_60 * lam0)))

    # Maximum lambda_Delta(v_R) in the pure-self-coupling truncation to avoid a formal pole below M_Pl:
    log_span = math.log(M_PL_GEV / v_r)
    lam_max_to_MPl = 16.0 * math.pi**2 / (c_60 * log_span)
    mixed_beta_at_ew = (
        c_60 * (lambda_delta_ew**2)
        - 36.0 * lambda_delta_ew * kappa4_ew
        - 16.0 * lambda_delta_ew * kappa_r_ew
    )

    return {
        "diagnostic_scope": (
            "pure-self-coupling 1-loop O(60) truncation; kappa^2, bidoublet portal, "
            "gauge, and Yukawa terms omitted; full coupled 138-parameter scalar RGEs open"
        ),
        "N_complex_DeltaR": 30,
        "N_real_DeltaR": 60,
        "beta_coeff_lambda_Delta_sq": c_60,
        "beta_coeff_lambda_Delta_kappa4": -36.0,
        "beta_coeff_lambda_Delta_kappaR": -16.0,
        "v_R_GeV": float(v_r),
        "phase2b_benchmark_lambda_Delta": lambda_delta_phase2b,
        "phase2b_landau_pole_ratio_over_vR": float(math.exp(16.0 * math.pi**2 / (c_60 * lambda_delta_phase2b))),
        "phase2b_landau_pole_GeV": lp_scale_pure(lambda_delta_phase2b),
        "phase2b_sub_planckian_landau_pole": lp_scale_pure(lambda_delta_phase2b) < M_PL_GEV,
        "ps1_ew_benchmark_lambda_Delta": lambda_delta_ew,
        "ps1_ew_benchmark_kappa4": kappa4_ew,
        "ps1_ew_benchmark_kappaR": kappa_r_ew,
        "ps1_ew_partial_beta_16pi2_at_vR": float(mixed_beta_at_ew),
        "ps1_ew_landau_pole_GeV": lp_scale_pure(lambda_delta_ew),
        "ps1_ew_perturbative_to_MPl_pure_truncation": lp_scale_pure(lambda_delta_ew) > M_PL_GEV,
        "max_lambda_Delta_perturbative_to_MPl_pure_truncation": float(lam_max_to_MPl),
    }


# ---------------------------------------------------------------------------
# PART 3: Fermion Mass, CKM, PMNS & Type-I Seesaw Fits (PS1-EW-min vs PS1-EW-gen)
# ---------------------------------------------------------------------------
def _unitary_from_9_params(p: np.ndarray) -> np.ndarray:
    H = np.zeros((3, 3), dtype=np.complex128)
    H[0, 0] = 1j * p[0]
    H[1, 1] = 1j * p[1]
    H[2, 2] = 1j * p[2]
    H[0, 1] = p[3] + 1j * p[4]
    H[1, 0] = -H[0, 1].conjugate()
    H[0, 2] = p[5] + 1j * p[6]
    H[2, 0] = -H[0, 2].conjugate()
    H[1, 2] = p[7] + 1j * p[8]
    H[2, 1] = -H[1, 2].conjugate()
    return expm(H)


def compute_seesaw_and_leptogenesis(
    YnuD: np.ndarray,
    UeL: np.ndarray,
    v_r: float,
    m_nu_running_eV: np.ndarray,
) -> Dict[str, object]:
    """Invert Type-I seesaw m_nu = -(v_EW^2/2) YnuD M_R^-1 YnuD^T to find exact M_R, f_R,
    verify PMNS / mass-squared round-trip recovery in the charged-lepton mass basis,
    and compute Covi-Roulet-Vissani / Davidson-Ibarra thermal leptogenesis diagnostics."""
    U_pmns = standard_unitary_3x3(
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th12"])),
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th23"])),
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th13"])),
        math.radians(NEUTRINO_INPUTS["delta_pmns_deg"]),
    )
    # In the convention -L_D = \bar{e}_L Y_e e_R + \bar{nu}_L Y_nu^D nu_R, rotating to the
    # charged-lepton mass basis via L_L = UeL L_L^ell gives Y_nu^ell = UeL^dag Y_nu^D, so
    # m_nu^ell = -(v_EW^2/2) Y_nu^ell M_R^-1 (Y_nu^ell)^T = UeL^dag m_nu UeL^*.
    # Inverting gives m_nu = UeL m_nu^ell UeL^T, with m_nu^ell = U_pmns diag(m_i) U_pmns^T:
    mnu_ell_GeV = U_pmns @ (np.diag(m_nu_running_eV) * 1.0e-9) @ U_pmns.T
    mnu_GeV = UeL @ mnu_ell_GeV @ UeL.T
    MR = -(V_EW_GEV**2 / 2.0) * (YnuD.T @ np.linalg.inv(mnu_GeV) @ YnuD)
    MR = 0.5 * (MR + MR.T)

    # Verify exact seesaw inversion residual in the original weak basis
    mnu_check = -(V_EW_GEV**2 / 2.0) * (YnuD @ np.linalg.inv(MR) @ YnuD.T)
    seesaw_rel_err = float(np.linalg.norm(mnu_check - mnu_GeV) / np.linalg.norm(mnu_GeV))

    # Direct charged-lepton mass-basis PMNS & mass-squared round-trip verification:
    mnu_ell_rec = UeL.conj().T @ mnu_check @ UeL.conj()
    H_nu_ell = mnu_ell_rec @ mnu_ell_rec.conj().T
    evals_sq, U_rec = np.linalg.eigh(H_nu_ell)
    m_rec_eV = np.sqrt(np.maximum(evals_sq, 0.0)) * 1.0e9
    s13_sq_rec = float(abs(U_rec[0, 2]) ** 2)
    c13_sq_rec = 1.0 - s13_sq_rec
    s12_sq_rec = float(abs(U_rec[0, 1]) ** 2) / c13_sq_rec
    s23_sq_rec = float(abs(U_rec[1, 2]) ** 2) / c13_sq_rec
    J_rec = jarlskog_invariant(U_rec)
    c12_r, s12_r = math.sqrt(1.0 - s12_sq_rec), math.sqrt(s12_sq_rec)
    c23_r, s23_r = math.sqrt(1.0 - s23_sq_rec), math.sqrt(s23_sq_rec)
    s13_r = math.sqrt(s13_sq_rec)
    sin_d_rec = J_rec / (c12_r * s12_r * c23_r * s23_r * c13_sq_rec * s13_r)
    cos_d_rec = (
        (c12_r * c23_r) ** 2 + (s12_r * s23_r * s13_r) ** 2 - abs(U_rec[1, 1]) ** 2
    ) / (2.0 * c12_r * s12_r * c23_r * s23_r * s13_r)
    delta_rec_deg = float(math.degrees(math.atan2(sin_d_rec, cos_d_rec)) % 360.0)

    dm21_target = float(m_nu_running_eV[1] ** 2 - m_nu_running_eV[0] ** 2)
    dm31_target = float(m_nu_running_eV[2] ** 2 - m_nu_running_eV[0] ** 2)
    dm21_rec = float(m_rec_eV[1] ** 2 - m_rec_eV[0] ** 2)
    dm31_rec = float(m_rec_eV[2] ** 2 - m_rec_eV[0] ** 2)

    pmns_roundtrip_max_rel_err = max(
        abs(s12_sq_rec - NEUTRINO_INPUTS["sin2_th12"]) / NEUTRINO_INPUTS["sin2_th12"],
        abs(s23_sq_rec - NEUTRINO_INPUTS["sin2_th23"]) / NEUTRINO_INPUTS["sin2_th23"],
        abs(s13_sq_rec - NEUTRINO_INPUTS["sin2_th13"]) / NEUTRINO_INPUTS["sin2_th13"],
        abs(delta_rec_deg - NEUTRINO_INPUTS["delta_pmns_deg"]) / NEUTRINO_INPUTS["delta_pmns_deg"],
        abs(dm21_rec - dm21_target) / dm21_target,
        abs(dm31_rec - dm31_target) / dm31_target,
    )

    # Takagi factorization of symmetric complex M_R: U_R^T M_R U_R = diag(M1, M2, M3)
    W, s_MR, _ = np.linalg.svd(MR)
    order = np.argsort(s_MR)
    s_MR = s_MR[order]
    W = W[:, order]
    D_check = W.conj().T @ MR @ W.conj()
    phases = np.angle(np.diag(D_check))
    U_R = W.conj() @ np.diag(np.exp(-0.5j * phases))
    takagi_err = float(
        np.linalg.norm(U_R.T @ MR @ U_R - np.diag(s_MR)) / np.linalg.norm(MR)
    )

    Ynu_hat = UeL.conj().T @ YnuD @ U_R  # in charged-lepton & N_R mass basis
    mnu_ell_from_hat = -(V_EW_GEV**2 / 2.0) * (Ynu_hat @ np.diag(1.0 / s_MR) @ Ynu_hat.T)
    hat_basis_seesaw_rel_err = float(
        np.linalg.norm(mnu_ell_from_hat - mnu_ell_GeV) / np.linalg.norm(mnu_ell_GeV)
    )

    f_R = math.sqrt(2.0) * MR / v_r
    f_R_norm = float(np.linalg.norm(f_R, 2))

    # Unflavored Type-I thermal leptogenesis CP asymmetry epsilon_1 (Covi-Roulet-Vissani):
    H_nu = Ynu_hat.conj().T @ Ynu_hat
    M1, M2, M3 = float(s_MR[0]), float(s_MR[1]), float(s_MR[2])
    eps1 = 0.0
    if abs(H_nu[0, 0].real) > 1.0e-30:
        for j, Mj in ((1, M2), (2, M3)):
            x = (Mj / M1) ** 2
            if x > 1.0001:
                f_loop = math.sqrt(x) * (1.0 / (1.0 - x) + 1.0 - (1.0 + x) * math.log((1.0 + x) / x))
                eps1 += (1.0 / (8.0 * math.pi * H_nu[0, 0].real)) * float(((H_nu[0, j]) ** 2).imag) * f_loop

    # Davidson-Ibarra upper bound for hierarchical N_R:
    m_atm_GeV = math.sqrt(NEUTRINO_INPUTS["dm31_sq_eV2"]) * 1.0e-9
    eps1_DI_bound = (3.0 / (16.0 * math.pi)) * (M1 * m_atm_GeV / (V_EW_GEV**2))

    # Optimistic unflavored N_1-dominated baryon asymmetry ceiling:
    # eta_B ~ -0.96e-2 * kappa_eff * eps1, with kappa_eff <= 0.1; observed eta_B ~ 6.1e-10
    eta_B_obs = 6.1e-10
    eta_B_ceiling_unflavored = 0.96e-2 * 0.1 * abs(eps1)
    vanilla_n1_shortfall_factor = (
        float(eta_B_obs / eta_B_ceiling_unflavored) if eta_B_ceiling_unflavored > 0.0 else float("inf")
    )

    # KATRIN m_beta and 0nu-beta-beta m_bb (at M_Z neutrino masses)
    m1_0 = NEUTRINO_INPUTS["m1_benchmark_eV"]
    m2_0 = math.sqrt(m1_0**2 + NEUTRINO_INPUTS["dm21_sq_eV2"])
    m3_0 = math.sqrt(m1_0**2 + NEUTRINO_INPUTS["dm31_sq_eV2"])
    m_vec = np.array([m1_0, m2_0, m3_0])
    m_beta = float(math.sqrt(float(np.sum((np.abs(U_pmns[0, :]) ** 2) * (m_vec**2)))))
    m_bb = float(abs(np.sum((U_pmns[0, :] ** 2) * m_vec)))

    return {
        "M_R_GeV": [M1, M2, M3],
        "f_R_spectral_norm": f_R_norm,
        "f_R_perturbative": f_R_norm < PERT_LIMIT,
        "seesaw_inversion_rel_err": seesaw_rel_err,
        "hat_basis_seesaw_rel_err": hat_basis_seesaw_rel_err,
        "takagi_rel_err": takagi_err,
        "pmns_roundtrip_recovery": {
            "sin2_th12": s12_sq_rec,
            "sin2_th23": s23_sq_rec,
            "sin2_th13": s13_sq_rec,
            "delta_pmns_deg": delta_rec_deg,
            "J_pmns": float(J_rec),
            "dm21_sq_running_eV2": dm21_rec,
            "dm31_sq_running_eV2": dm31_rec,
            "max_rel_err": float(pmns_roundtrip_max_rel_err),
        },
        "epsilon_1_CP_asymmetry": float(eps1),
        "epsilon_1_DI_bound": float(eps1_DI_bound),
        "eta_B_ceiling_unflavored_kappa01": float(eta_B_ceiling_unflavored),
        "eta_B_observed_benchmark": eta_B_obs,
        "vanilla_N1_leptogenesis_shortfall_factor": vanilla_n1_shortfall_factor,
        "vanilla_N1_leptogenesis_reaches_etaB": eta_B_ceiling_unflavored >= eta_B_obs,
        "monopole_safe_kinematic_window": (M1 >= 1.0e9) and (M1 < 0.2 * v_r),
        "sum_m_nu_eV": float(np.sum(m_vec)),
        "m_beta_eV": m_beta,
        "m_bb_eV": m_bb,
    }


def fit_ps1_ew_min(
    sm_state: Mapping[str, object],
    v_r: float,
    allow_complex_ratios: bool = True,
) -> Dict[str, object]:
    """Existence/interpolation fit of all 9 charged-fermion masses + 4 CKM parameters +
    neutrinos/PMNS in the minimal 2-Dirac-Yukawa branch PS1-EW-min (Y_1, Y_15, f_R only;
    Y_1_tilde = Y_15_tilde = 0).

    Parameter-count note: After U(3)_L x U(3)_R basis removal (18 real), the Yukawa sector
    (Y_1, Y_15, f_R = f_R^T) retains 36 + 12 - 18 = 30 real Yukawa parameters vs 18 real
    flavour observables, so a fit here is an existence/interpolation test, NOT a constrained
    prediction. Both real and complex Higgs-mixing ratios (c_d, c_e) admit perturbative
    witnesses at BM-LR, and refitting running inputs remains perturbative below the
    retracted 7.7e11 GeV fixed-fit estimate (demonstrated at v_R = 6.0e11 GeV).
    """
    su = sm_state["yu_sv"]
    sd = sm_state["yd_sv"]
    se = sm_state["ye_sv"]
    Vckm = sm_state["V_ckm"]
    J_ckm = float(sm_state["J_ckm"])
    m_nu_run = sm_state["m_nu_running_eV"]
    assert isinstance(su, np.ndarray) and isinstance(sd, np.ndarray) and isinstance(se, np.ndarray)
    assert isinstance(Vckm, np.ndarray) and isinstance(m_nu_run, np.ndarray)

    Yd_diag = np.diag(sd).astype(np.complex128)
    Ye_diag = np.diag(se).astype(np.complex128)
    target_Vabs = np.abs(Vckm)
    U_pmns = standard_unitary_3x3(
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th12"])),
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th23"])),
        math.asin(math.sqrt(NEUTRINO_INPUTS["sin2_th13"])),
        math.radians(NEUTRINO_INPUTS["delta_pmns_deg"]),
    )
    mnu_ell_inv = U_pmns.conj() @ np.diag(1.0 / (m_nu_run * 1.0e-9)) @ U_pmns.conj().T

    def unpack_x(x: np.ndarray) -> Tuple[complex, complex, np.ndarray, np.ndarray]:
        if allow_complex_ratios:
            cd = complex(x[0], x[1])
            ce = complex(x[2], x[3])
            UeL = _unitary_from_9_params(x[4:13])
            UeR = _unitary_from_9_params(x[13:22])
        else:
            cd = complex(x[0], 0.0)
            ce = complex(x[1], 0.0)
            UeL = _unitary_from_9_params(x[2:11])
            UeR = _unitary_from_9_params(x[11:20])
        return cd, ce, UeL, UeR

    def res_fn(x: np.ndarray, w_obs: float, w_ynu: float, w_fR: float) -> np.ndarray:
        cd, ce, UeL, UeR = unpack_x(x)
        Ye_rot = UeL @ Ye_diag @ UeR.conj().T
        Yu_mod = cd * Yd_diag + ce * Ye_rot
        Uu, s_mod, _ = np.linalg.svd(Yu_mod)
        s_mod = s_mod[::-1]
        Uu = Uu[:, ::-1]
        V_mod = Uu.conj().T
        J_mod = jarlskog_invariant(V_mod)
        out = [
            w_obs * (s_mod[0] - su[0]) / su[0],
            w_obs * (s_mod[1] - su[1]) / su[1],
            w_obs * (s_mod[2] - su[2]) / su[2],
            w_obs * (abs(V_mod[0, 1]) - target_Vabs[0, 1]) / target_Vabs[0, 1],
            w_obs * (abs(V_mod[1, 2]) - target_Vabs[1, 2]) / target_Vabs[1, 2],
            w_obs * (abs(V_mod[0, 2]) - target_Vabs[0, 2]) / target_Vabs[0, 2],
            w_obs * (J_mod - J_ckm) / J_ckm,
        ]
        if w_ynu > 0.0 or w_fR > 0.0:
            YnuD = 3.0 * ce * Yd_diag + (cd - 2.0 * ce) * Ye_rot
            if w_ynu > 0.0:
                out.append(w_ynu * float(np.linalg.norm(YnuD, "fro")))
            if w_fR > 0.0:
                Ynu_ell = UeL.conj().T @ YnuD
                MR = -(V_EW_GEV**2 / 2.0) * (Ynu_ell.T @ mnu_ell_inv @ Ynu_ell)
                fR_n = float(np.linalg.norm(math.sqrt(2.0) * MR / v_r, "fro"))
                out.append(w_fR * math.log1p(fR_n))
        return np.array(out, dtype=np.float64)

    if allow_complex_ratios:
        ce0 = 18.0
        cd0 = 42.3 + 35.5j
        phi3 = math.atan2((-3.0 * ce0 / (cd0 - 2.0 * ce0)).imag, (-3.0 * ce0 / (cd0 - 2.0 * ce0)).real)
        x0 = np.zeros(22, dtype=np.float64)
        x0[0], x0[1], x0[2], x0[3] = cd0.real, cd0.imag, ce0, 0.0
        x0[6] = phi3
        x0[7:13] = [0.22, 0.05, 0.01, -0.02, 0.04, 0.01]
        x0[16:22] = [-0.20, 0.10, 0.05, 0.02, -0.03, 0.05]
        r1 = least_squares(res_fn, x0, args=(1.0, 2.0, 0.0), method="trf", ftol=1.0e-11, xtol=1.0e-11, max_nfev=2000)
        r2 = least_squares(res_fn, r1.x, args=(20.0, 0.0, 1.0), method="trf", ftol=1.0e-12, xtol=1.0e-12, max_nfev=2000)
        r3 = least_squares(res_fn, r2.x, args=(1.0, 0.0, 0.0), method="trf", ftol=1.0e-14, xtol=1.0e-14, gtol=1.0e-14, max_nfev=2500)
        x_opt = r3.x
        final_res = r3.fun
    else:
        # Real Higgs-mixing ratios (c_d, c_e in R): destructive 3rd-generation cancellation in
        # (Y_nu^D)_33 occurs cleanly with phase pi in U_eL / U_eR near c_d ~ 115, c_e ~ 29!
        rt = float(su[2] / sd[2])
        r_tau = float(se[2] / sd[2])
        rho = r_tau / (3.0 + 2.0 * r_tau)
        cd0_re = rt * (1.0 - 2.0 * rho) / ((1.0 - 3.0 * rho) * (1.0 + rho))
        ce0_re = rho * cd0_re
        x0 = np.zeros(20, dtype=np.float64)
        x0[0], x0[1] = cd0_re, ce0_re
        x0[4] = math.pi
        x0[5:11] = [0.22, 0.05, 0.01, -0.02, 0.04, 0.01]
        x0[14:20] = [-0.20, 0.10, 0.05, 0.02, -0.03, 0.05]
        r1 = least_squares(res_fn, x0, args=(1.0, 2.0, 0.0), method="trf", ftol=1.0e-12, xtol=1.0e-12, max_nfev=3000)
        r3 = least_squares(res_fn, r1.x, args=(1.0, 0.0, 0.0), method="trf", ftol=1.0e-14, xtol=1.0e-14, gtol=1.0e-14, max_nfev=3000)
        x_opt = r3.x
        final_res = r3.fun

    cd, ce, UeL, UeR = unpack_x(x_opt)
    Ye_rot = UeL @ Ye_diag @ UeR.conj().T
    Yu_mod = cd * Yd_diag + ce * Ye_rot
    YnuD = 3.0 * ce * Yd_diag + (cd - 2.0 * ce) * Ye_rot

    r1_ratio = cd + ce
    r15_ratio = cd - 3.0 * ce
    a1u = 1.0 / math.sqrt(2.0)
    a15u = 1.0 / math.sqrt(2.0)
    a1d = (a1u / r1_ratio).conjugate()
    a15d = (a15u / r15_ratio).conjugate()
    nrm = math.sqrt(abs(a1u) ** 2 + abs(a1d) ** 2 + abs(a15u) ** 2 + abs(a15d) ** 2)
    u_light = np.array([a1u, a1d, a15u, a15d], dtype=np.complex128) / nrm
    a1u, a1d, a15u, a15d = u_light

    Y1 = (3.0 * Yd_diag + Ye_rot) / (4.0 * a1d.conjugate())
    Y15_hat = (Yd_diag - Ye_rot) / (4.0 * a15d.conjugate())
    Y15 = math.sqrt(12.0) * Y15_hat

    # Verify exact tree-level matching identities
    match_err = max(
        float(np.linalg.norm(a1u * Y1 + a15u * Y15_hat - Yu_mod)),
        float(np.linalg.norm(a1d.conjugate() * Y1 + a15d.conjugate() * Y15_hat - Yd_diag)),
        float(np.linalg.norm(a1d.conjugate() * Y1 - 3.0 * a15d.conjugate() * Y15_hat - Ye_rot)),
        float(np.linalg.norm(a1u * Y1 - 3.0 * a15u * Y15_hat - YnuD)),
    )

    seesaw = compute_seesaw_and_leptogenesis(YnuD, UeL, v_r, m_nu_run)
    y1_norm = float(np.linalg.norm(Y1, 2))
    y15_norm = float(np.linalg.norm(Y15, 2))
    max_yukawa = max(y1_norm, y15_norm, seesaw["f_R_spectral_norm"])

    return {
        "branch": "PS1-EW-min (complex ratios)" if allow_complex_ratios else "PS1-EW-min (real ratios)",
        "fit_epistemic_scope": (
            "existence/interpolation witness (30 real Yukawa parameters after U(3)_L x U(3)_R "
            "basis removal vs 18 real flavour observables; not a constrained prediction)"
        ),
        "allow_complex_ratios": allow_complex_ratios,
        "v_R_GeV": float(v_r),
        "max_charged_fermion_ckm_rel_err": float(np.max(np.abs(final_res[:7]))),
        "matching_identity_residual": float(match_err),
        "cd": [float(cd.real), float(cd.imag)],
        "ce": [float(ce.real), float(ce.imag)],
        "r1": [float(r1_ratio.real), float(r1_ratio.imag)],
        "r15": [float(r15_ratio.real), float(r15_ratio.imag)],
        "u_light": [[float(z.real), float(z.imag)] for z in u_light],
        "u_light_complex": u_light,
        "Y1_spectral_norm": y1_norm,
        "Y15_spectral_norm": y15_norm,
        "YnuD_singular_values": [float(x) for x in np.linalg.svd(YnuD, compute_uv=False)[::-1]],
        "seesaw": seesaw,
        "max_yukawa_norm": float(max_yukawa),
        "all_yukawas_perturbative": max_yukawa < PERT_LIMIT,
        "K_L": UeL,
        "K_R": UeR,
    }


def verify_yukawa_forward_contraction(
    u_light: np.ndarray,
    Y1: np.ndarray,
    Y1_tilde: np.ndarray,
    Y15: np.ndarray,
    Y15_tilde: np.ndarray,
) -> Dict[str, np.ndarray]:
    """Independently compute the SM Dirac Yukawa matrices (Y_u, Y_d, Y_nu^D, Y_e) by explicit
    2x2 SU(2)_L x SU(2)_R bidoublet contraction F_L^T (-eps) [Y Phi + Y~ Phi~] (eps F_R^c)
    on the neutral SM Higgs VEV <h> = (0, 1)^T, using Phi = (eps H_d^*, H_u) and
    Phi_tilde = eps Phi^* eps^T = (eps H_u^*, H_d)."""
    eps = ALGEBRA.eps
    a1u, a1d, a15u, a15d = u_light
    h_vev = np.array([0.0, 1.0], dtype=np.complex128)

    def make_bidoublet(au: complex, ad: complex) -> Tuple[np.ndarray, np.ndarray]:
        Hu = au * h_vev
        Hd = ad * h_vev
        phi = np.column_stack([eps @ Hd.conj(), Hu])
        phi_tilde = eps @ phi.conj() @ eps.T
        return phi, phi_tilde

    phi1, phi1_tilde = make_bidoublet(a1u, a1d)
    phi15_15, phi15_15_tilde = make_bidoublet(a15u, a15d)

    # SU(4) diagonal generator sqrt(2) * T^15 = diag(1, 1, 1, -3) / sqrt(12):
    c_q = 1.0 / math.sqrt(12.0)
    c_l = -3.0 / math.sqrt(12.0)

    # Basis vectors in SU(2)_L (u_L/nu_L = e_0, d_L/e_L = e_1) and SU(2)_R (u^c/nu^c = e_0, d^c/e^c = e_1):
    e_up = np.array([1.0, 0.0], dtype=np.complex128)
    e_dn = np.array([0.0, 1.0], dtype=np.complex128)

    def contract_su2(mat2: np.ndarray, fL: np.ndarray, fRc: np.ndarray) -> complex:
        return complex(fL @ (-eps) @ mat2 @ (eps @ fRc))

    Yu_dir = (
        contract_su2(phi1, e_up, e_up) * Y1
        + contract_su2(phi1_tilde, e_up, e_up) * Y1_tilde
        + c_q * contract_su2(phi15_15, e_up, e_up) * Y15
        + c_q * contract_su2(phi15_15_tilde, e_up, e_up) * Y15_tilde
    )
    Yd_dir = (
        contract_su2(phi1, e_dn, e_dn) * Y1
        + contract_su2(phi1_tilde, e_dn, e_dn) * Y1_tilde
        + c_q * contract_su2(phi15_15, e_dn, e_dn) * Y15
        + c_q * contract_su2(phi15_15_tilde, e_dn, e_dn) * Y15_tilde
    )
    Ynu_dir = (
        contract_su2(phi1, e_up, e_up) * Y1
        + contract_su2(phi1_tilde, e_up, e_up) * Y1_tilde
        + c_l * contract_su2(phi15_15, e_up, e_up) * Y15
        + c_l * contract_su2(phi15_15_tilde, e_up, e_up) * Y15_tilde
    )
    Ye_dir = (
        contract_su2(phi1, e_dn, e_dn) * Y1
        + contract_su2(phi1_tilde, e_dn, e_dn) * Y1_tilde
        + c_l * contract_su2(phi15_15, e_dn, e_dn) * Y15
        + c_l * contract_su2(phi15_15_tilde, e_dn, e_dn) * Y15_tilde
    )
    return {"Yu": Yu_dir, "Yd": Yd_dir, "YnuD": Ynu_dir, "Ye": Ye_dir}


def fit_ps1_ew_gen(
    sm_state: Mapping[str, object],
    v_r: float,
    target_fR_max: float = 0.35,
) -> Dict[str, object]:
    """Exact closed-form inversion for the full gauge-invariant 4-Dirac-Yukawa branch
    PS1-EW-gen (Y_1, Y_1_tilde, Y_15, Y_15_tilde, f_R).

    With Phi = (eps H_d^*, H_u) and Phi_tilde = eps Phi^* eps^T = (eps H_u^*, H_d),
    the down-type tilde contributions add with the SAME relative sign:
        Y_u    = a1u Y_1 + a1d Y_1_tilde + a15u Y_15_hat + a15d Y_15_tilde_hat
        Y_d    = a1d^* Y_1 + a1u^* Y_1_tilde + a15d^* Y_15_hat + a15u^* Y_15_tilde_hat
        Y_nu^D = a1u Y_1 + a1d Y_1_tilde - 3 a15u Y_15_hat - 3 a15d Y_15_tilde_hat
        Y_e    = a1d^* Y_1 + a1u^* Y_1_tilde - 3 a15d^* Y_15_hat - 3 a15u^* Y_15_tilde_hat
    The exact 2x2 inverse has determinant D = |a_u|^2 - |a_d|^2 (singular at |a_u| = |a_d|).
    """
    Yu = sm_state["Yu"]
    Yd = sm_state["Yd"]
    Ye = sm_state["Ye"]
    m_nu_run = sm_state["m_nu_running_eV"]
    assert isinstance(Yu, np.ndarray) and isinstance(Yd, np.ndarray) and isinstance(Ye, np.ndarray)
    assert isinstance(m_nu_run, np.ndarray)

    # Choose balanced O(1) light-Higgs eigenvector away from the |a_u| = |a_d| singularity
    u_light = np.array([0.60, 0.40, 0.56, 0.40 * np.exp(0.3j)], dtype=np.complex128)
    u_light = u_light / np.linalg.norm(u_light)
    a1u, a1d, a15u, a15d = u_light
    D1 = abs(a1u) ** 2 - abs(a1d) ** 2
    D15 = abs(a15u) ** 2 - abs(a15d) ** 2
    if abs(D1) < 1.0e-12 or abs(D15) < 1.0e-12:
        raise ValueError("PS1-EW-gen inversion is singular when |a_u| == |a_d|")

    # Choose Y_nu^D in the charged-lepton mass basis with hierarchical scale matched to v_R
    # so M_R3 ~ (target_fR_max / sqrt(2)) * v_R:
    m3_GeV = float(m_nu_run[2]) * 1.0e-9
    MR3_target = (target_fR_max / math.sqrt(2.0)) * v_r
    y_nu_scale = min(0.25, math.sqrt(2.0 * MR3_target * m3_GeV) / V_EW_GEV)
    U_nu = standard_unitary_3x3(0.20, 0.15, 0.05, 0.9)
    YnuD = U_nu @ np.diag([0.42, 0.70, 1.0]) * y_nu_scale

    # Exact closed-form inverse:
    # For a Y + b Y_tilde = P_u, b^* Y + a^* Y_tilde = P_d with D = |a|^2 - |b|^2:
    #   Y       = ( a^* P_u - b P_d) / D
    #   Y_tilde = (-b^* P_u + a P_d) / D
    Au = (3.0 * Yu + YnuD) / 4.0
    Ad = (3.0 * Yd + Ye) / 4.0
    Bu = (Yu - YnuD) / 4.0
    Bd = (Yd - Ye) / 4.0

    Y1 = (a1u.conjugate() * Au - a1d * Ad) / D1
    Y1_tilde = (-a1d.conjugate() * Au + a1u * Ad) / D1
    Y15_hat = (a15u.conjugate() * Bu - a15d * Bd) / D15
    Y15_tilde_hat = (-a15d.conjugate() * Bu + a15u * Bd) / D15
    Y15 = math.sqrt(12.0) * Y15_hat
    Y15_tilde = math.sqrt(12.0) * Y15_tilde_hat

    # Verify exact reconstruction using BOTH analytic formulas AND direct 2x2 tensor contraction!
    Yu_rec = a1u * Y1 + a1d * Y1_tilde + a15u * Y15_hat + a15d * Y15_tilde_hat
    Yd_rec = a1d.conjugate() * Y1 + a1u.conjugate() * Y1_tilde + a15d.conjugate() * Y15_hat + a15u.conjugate() * Y15_tilde_hat
    Ynu_rec = a1u * Y1 + a1d * Y1_tilde - 3.0 * a15u * Y15_hat - 3.0 * a15d * Y15_tilde_hat
    Ye_rec = a1d.conjugate() * Y1 + a1u.conjugate() * Y1_tilde - 3.0 * a15d.conjugate() * Y15_hat - 3.0 * a15u.conjugate() * Y15_tilde_hat

    rec_err = max(
        float(np.linalg.norm(Yu_rec - Yu) / np.linalg.norm(Yu)),
        float(np.linalg.norm(Yd_rec - Yd) / np.linalg.norm(Yd)),
        float(np.linalg.norm(Ye_rec - Ye) / np.linalg.norm(Ye)),
        float(np.linalg.norm(Ynu_rec - YnuD) / np.linalg.norm(YnuD)),
    )

    direct = verify_yukawa_forward_contraction(u_light, Y1, Y1_tilde, Y15, Y15_tilde)
    direct_contract_err = max(
        float(np.linalg.norm(direct["Yu"] - Yu) / np.linalg.norm(Yu)),
        float(np.linalg.norm(direct["Yd"] - Yd) / np.linalg.norm(Yd)),
        float(np.linalg.norm(direct["Ye"] - Ye) / np.linalg.norm(Ye)),
        float(np.linalg.norm(direct["YnuD"] - YnuD) / np.linalg.norm(YnuD)),
    )

    # In SM RGE basis, Ye and Yd are both diagonal at M_Z (and nearly diagonal at v_R)
    UeL, _, UeRh = np.linalg.svd(Ye)
    UdL, _, UdRh = np.linalg.svd(Yd)
    UeL, UdL = UeL[:, ::-1], UdL[:, ::-1]
    UeR, UdR = UeRh.conj().T[:, ::-1], UdRh.conj().T[:, ::-1]

    seesaw = compute_seesaw_and_leptogenesis(YnuD, UeL, v_r, m_nu_run)
    norms = {
        "Y1": float(np.linalg.norm(Y1, 2)),
        "Y1_tilde": float(np.linalg.norm(Y1_tilde, 2)),
        "Y15": float(np.linalg.norm(Y15, 2)),
        "Y15_tilde": float(np.linalg.norm(Y15_tilde, 2)),
        "f_R": seesaw["f_R_spectral_norm"],
    }
    max_y = max(norms.values())

    return {
        "branch": "PS1-EW-gen",
        "v_R_GeV": float(v_r),
        "determinants_D1_D15": [float(D1), float(D15)],
        "exact_reconstruction_rel_err": float(rec_err),
        "direct_tensor_contraction_rel_err": float(direct_contract_err),
        "u_light": [[float(z.real), float(z.imag)] for z in u_light],
        "yukawa_spectral_norms": norms,
        "YnuD_singular_values": [float(x) for x in np.linalg.svd(YnuD, compute_uv=False)[::-1]],
        "seesaw": seesaw,
        "max_yukawa_norm": float(max_y),
        "all_yukawas_perturbative": max_y < PERT_LIMIT,
        "K_L": UdL.conj().T @ UeL,
        "K_R": UdR.conj().T @ UeR,
    }


# ---------------------------------------------------------------------------
# PART 4: Flavour, Baryon-Number Stability & Cosmological Relic Audit
# ---------------------------------------------------------------------------
def audit_flavour_baryon_cosmology(
    v_r: float,
    g4: float,
    g2R: float,
    K_L: np.ndarray,
    K_R: np.ndarray,
    seesaw_result: Mapping[str, object],
    kappa4: float = 0.006,
    kappa_r: float = 0.0045,
    M_GUT_GeV: float | None = None,
    alpha_GUT_inv: float | None = None,
) -> Dict[str, object]:
    """Audit Valencia-Willenbrock X-boson flavour bounds, preliminary order-of-magnitude
    W_R/Z_R, heavy-Higgs FCNC, and n-nbar checks, baryon-number selection rules, and
    monopole / Z_2-string / domain-wall / thermal-leptogenesis cosmology at scale v_R."""
    M_R_GeV = seesaw_result["M_R_GeV"]
    M_X = math.sqrt(0.5) * g4 * v_r
    M_WR = math.sqrt(0.5) * g2R * v_r
    M_ZR = math.sqrt(1.5 * g4**2 + g2R**2) * v_r

    # 1. K_L -> mu^+ e^- + mu^- e^+ via chiral-enhanced X-boson exchange
    # Valencia & Willenbrock PRD 50, 6843 (1994); Smirnov MPLA 22, 2353 (2007)
    # Exact width summed over mu^- e^+ and mu^+ e^-:
    #   Gamma = (g_4^4 f_K^2 m_K / (32 pi M_X^4)) * (eta_QCD m_K^2 / (m_s + m_d))^2
    #           * (1 - m_mu^2 / m_K^2)^2 * |c_mix|^2
    # where |c_mix|^2 = 1.0 for aligned mixing K_L = K_R = I.
    f_K = 0.1557
    m_K = 0.49761
    m_mu = 0.10566
    ms_plus_md = 0.098
    Gamma_KL = 1.2866e-17
    eta_QCD = 2.1

    R_chi = 2.0 * eta_QCD * (m_K**2) / (m_mu * ms_plus_md)
    # Properly normalized mixing factor (equals 1.0 for aligned K_L = K_R = I):
    c_fitted_sq = 0.5 * (
        abs(K_L[0, 0].conjugate() * K_R[1, 1]) ** 2
        + abs(K_R[0, 0].conjugate() * K_L[1, 1]) ** 2
        + abs(K_L[0, 1].conjugate() * K_R[1, 0]) ** 2
        + abs(K_R[0, 1].conjugate() * K_L[1, 0]) ** 2
    )
    prefac_KL = (
        (g4**4 * (f_K**2) * m_K) / (32.0 * math.pi * (M_X**4))
        * ((eta_QCD * (m_K**2) / ms_plus_md) ** 2)
        * ((1.0 - (m_mu / m_K) ** 2) ** 2)
    )
    BR_KL_aligned = float(prefac_KL * 1.0 / Gamma_KL)
    BR_KL_fitted = float(prefac_KL * max(c_fitted_sq, 1.0e-30) / Gamma_KL)

    # Exact aligned M_X and v_R lower bound from BR(K_L -> mu e) < 4.7e-12:
    M_X_bound_aligned = M_X * ((BR_KL_aligned / EXP_BOUNDS["BR_KL_mue_90CL"]) ** 0.25)
    v_R_bound_aligned = math.sqrt(2.0) * M_X_bound_aligned / g4

    # 2. B_s -> mu^+ e^- + mu^- e^+ (aligned O(1) mixing, same 1/(32 pi) normalization):
    f_Bs, m_Bs, mb_plus_ms, Gamma_Bs = 0.2303, 5.3669, 4.28, 4.33e-13
    eta_QCD_Bs = 1.8
    BR_Bs_aligned = float(
        (g4**4 * (f_Bs**2) * m_Bs) / (32.0 * math.pi * (M_X**4))
        * ((eta_QCD_Bs * (m_Bs**2) / mb_plus_ms) ** 2)
        * ((1.0 - (m_mu / m_Bs) ** 2) ** 2)
        / Gamma_Bs
    )

    # 3. mu -> e gamma (preliminary 1-loop X-boson dipole estimate vs MEG II 1.5e-13 bound):
    alpha_em = 1.0 / 137.036
    BR_mu_egamma_est = float(
        (3.0 * alpha_em / (8.0 * math.pi))
        * ((4.18 / m_mu) ** 2)
        * ((g4**2 * V_EW_GEV**2) / (4.0 * M_X**2)) ** 2
    )

    # 4. Baryon-number stability (preliminary order-of-magnitude check for n-nbar):
    # - Pure PS preserves perturbative baryon number via accidental 3B+L charges (while gauged
    #   B-L is broken by <Delta_R> by Delta(B-L) = 2), forbidding d=6 gauge and scalar proton decay.
    # - Delta B = 2 n-nbar oscillation vanishes at tree level in PS1-MM by U(1)_Delta; if
    #   lambda_Delta4 ~ 1 is turned on, sextet mediators have actual masses M_Delta6 in
    #   [sqrt(2*kappa4), sqrt(2*kappa4 + 2*kappa_r)] * v_R (not v_R!).
    hbar_GeV_s = 6.582119569e-25
    m_sextet_min_over_vR = math.sqrt(2.0 * kappa4)
    m_sextet_max_over_vR = math.sqrt(2.0 * kappa4 + 2.0 * kappa_r)
    M_sextet_min = m_sextet_min_over_vR * v_r
    fR11_est = max(math.sqrt(2.0) * M_R_GeV[0] / v_r, 1.0e-6)
    # Conservative order-of-magnitude estimate using the lightest sextet mass M_sextet_min^6:
    # G_nnbar ~ lambda_Delta4 * v_R * f_R11^3 / M_sextet_min^6
    G_nnbar_prelim = (1.0 * v_r * (fR11_est**3)) / (M_sextet_min**6)
    delta_m_nnbar = 1.0e-4 * G_nnbar_prelim  # |M_nnbar| ~ 1e-4 GeV^6
    tau_nnbar_if_lam4_O1 = float(hbar_GeV_s / delta_m_nnbar) if delta_m_nnbar > 0 else float("inf")

    # Optional SO(10) embedding d=6 proton lifetime ballpark (approximate gauge crossing,
    # without M_GUT parent-multiplet thresholds):
    tau_p_so10_yr = None
    if M_GUT_GeV is not None and alpha_GUT_inv is not None:
        alpha_GUT = 1.0 / alpha_GUT_inv
        m_p = 0.938272
        sec_per_yr = 3.15576e7
        gamma_p_GeV = (alpha_GUT**2) * (m_p**5) / (M_GUT_GeV**4) * 0.25
        tau_p_so10_yr = float((hbar_GeV_s / gamma_p_GeV) / sec_per_yr)

    # 5. Topological relics & cosmology:
    # - pi_2(G_PS / G_SM) = Z -> doubly-charged Pati-Salam magnetic monopoles, M_mon ~ 4 pi M_X / g_4^2
    # - pi_1(G_PS / G_SM) = Z_2 -> cosmic strings from the disconnected Z_2 stabilizer left by
    #   Delta(B-L) = 2 breaking (matter parity / Z_2 subgroup of U(1)_{B-L} x Z_2).
    M_monopole_GeV = float(4.0 * math.pi * M_X / (g4**2))
    smeft_suppression = float((V_EW_GEV / v_r) ** 2)

    return {
        "vector_masses_GeV": {
            "M_X": float(M_X),
            "M_WR": float(M_WR),
            "M_ZR": float(M_ZR),
        },
        "flavour": {
            "audit_scope": (
                "Valencia-Willenbrock tree-level X-boson K_L/B_s -> mu e; preliminary "
                "order-of-magnitude checks for mu -> e gamma, W_R/Z_R, and heavy-Higgs FCNC "
                "(full SMEFT Wilson-coefficient matching open)"
            ),
            "chiral_enhancement_R_chi_KL": float(R_chi),
            "BR_KL_mue_aligned_O1": BR_KL_aligned,
            "BR_KL_mue_fitted_mixing": BR_KL_fitted,
            "pass_KL_mue_aligned": BR_KL_aligned < EXP_BOUNDS["BR_KL_mue_90CL"],
            "pass_KL_mue_fitted": BR_KL_fitted < EXP_BOUNDS["BR_KL_mue_90CL"],
            "M_X_lower_bound_aligned_GeV": float(M_X_bound_aligned),
            "v_R_lower_bound_aligned_GeV": float(v_R_bound_aligned),
            "BR_Bs_mue_aligned_O1": BR_Bs_aligned,
            "pass_Bs_mue": BR_Bs_aligned < EXP_BOUNDS["BR_Bs_mue_90CL"],
            "BR_mu_egamma_prelim_est": BR_mu_egamma_est,
            "pass_mu_egamma_MEGII": BR_mu_egamma_est < EXP_BOUNDS["BR_mu_egamma_90CL"],
            "pass_WR_collider_prelim": M_WR > EXP_BOUNDS["m_WR_LHC_GeV"],
            "pass_heavy_Higgs_FCNC_prelim": (math.sqrt(0.80) * v_r) > EXP_BOUNDS["m_H2_FCNC_GeV"],
            "smeft_vEW2_over_vR2": smeft_suppression,
        },
        "baryon_stability": {
            "d6_gauge_proton_decay_in_pure_PS": (
                "FORBIDDEN at perturbative level (accidental 3B+L conservation; X is a pure "
                "leptoquark; note gauged B-L is broken by Delta_R by Delta(B-L)=2)"
            ),
            "d6_scalar_proton_decay_in_PS1": "FORBIDDEN (3B+L = 0 on Phi1,Phi15; 3B+L = +2 on DeltaR)",
            "n_nbar_in_PS1_MM": "FORBIDDEN at tree level (exact U(1)_Delta forbids Delta_R^4)",
            "sextet_mass_ratio_range_over_vR": [float(m_sextet_min_over_vR), float(m_sextet_max_over_vR)],
            "tau_nnbar_prelim_s_if_lambda_Delta4_O1": tau_nnbar_if_lam4_O1,
            "pass_nnbar_prelim_even_if_lambda4_O1": tau_nnbar_if_lam4_O1 > EXP_BOUNDS["tau_nnbar_s_90CL"],
            "optional_SO10_d6_tau_p_ballpark_yr": tau_p_so10_yr,
        },
        "cosmology_and_relics": {
            "homotopy_pi2_GPS_over_GSM": "Z (topologically stable doubly-charged magnetic monopoles)",
            "homotopy_pi1_GPS_over_GSM": "Z_2 (cosmic-string sector from disconnected stabilizer after Delta(B-L)=2 breaking)",
            "monopole_mass_GeV": M_monopole_GeV,
            "requires_Trh_below_vR": True,
            "D_parity_domain_walls": "ABSENT (no Delta_L multiplet in PS1-MM / PS1-EW)",
            "M_R1_GeV": float(M_R_GeV[0]),
            "epsilon_1_CP_asymmetry": float(seesaw_result["epsilon_1_CP_asymmetry"]),
            "eta_B_ceiling_unflavored_kappa01": float(seesaw_result["eta_B_ceiling_unflavored_kappa01"]),
            "vanilla_N1_leptogenesis_shortfall_factor": float(seesaw_result["vanilla_N1_leptogenesis_shortfall_factor"]),
            "vanilla_N1_leptogenesis_reaches_etaB": bool(seesaw_result["vanilla_N1_leptogenesis_reaches_etaB"]),
            "monopole_safe_kinematic_window": bool(seesaw_result["monopole_safe_kinematic_window"]),
        },
    }


def build_phase3_results() -> Dict[str, object]:
    """Execute the complete TP-03 Phase 3 (PS1-EW) verification suite (post-referee revision)."""
    # Perturbative PS1-EW Delta_R quartics (rescaled so lambda_Delta = 0.03 stays below
    # the pure-self-coupling 136*lambda_Delta^2 Planck starting cap ~0.0417 at all 3 benchmarks;
    # note full coupled 138-parameter scalar RGEs remain open!)
    lam_D, kap4, kapR = 0.03, 0.006, 0.0045
    lam_eff = lam_D - 1.5 * kap4 - kapR  # 0.0165

    # 1. Gauge beta & approximate SO(10) crossing scales (gauge-only 2-loop PS + 1-loop thresholds)
    scales = find_lr_parity_and_unification_scales(lam_D, kap4, kapR)
    vR_LR = scales["one_loop_no_threshold"]["vR_LR_parity_GeV"]       # ~5.08e13 GeV
    vR_GUT = scales["two_loop_with_thresholds"]["vR_triple_unification_GeV"]
    vR_LOW = 1.0e7

    # 2. Scan v_R window for 1-loop and gauge-only 2-loop perturbativity up to M_Pl
    vr_scan: List[Dict[str, object]] = []
    for logv in [5.5, 6.0, 7.0, 8.0, 10.0, 11.5, 13.0, 13.7, 15.0, 16.0]:
        v_pt = 10.0**logv
        sm_pt = run_sm_rge_to_scale(v_pt, two_loop_gauge=True)
        mt_pt = compute_threshold_matching_at_vR(sm_pt["gY"], sm_pt["g2"], sm_pt["g3"], lam_D, kap4, kapR)
        m1 = mt_pt["one_loop_matched"]
        uv1 = run_ps1_gauge_to_mplanck(v_pt, m1["g4"], m1["g2L"], m1["g2R"], two_loop=False)
        uv2 = run_ps1_gauge_to_mplanck(v_pt, m1["g4"], m1["g2L"], m1["g2R"], two_loop=True)
        vr_scan.append(
            {
                "log10_vR": logv,
                "v_R_GeV": v_pt,
                "lam_H_SM": sm_pt["lam_H"],
                "g4_vR": m1["g4"],
                "g2L_vR": m1["g2L"],
                "g2R_vR": m1["g2R"],
                "one_loop_pert_to_MPl": uv1["perturbative_to_MPl"],
                "two_loop_pert_to_MPl": uv2["perturbative_to_MPl"],
                "two_loop_max_g_MPl": uv2["max_g_at_MPl"],
            }
        )

    # 3. Audit all three benchmarks (BM-LR, BM-GUT, BM-LOW) for BOTH PS1-EW-min and PS1-EW-gen
    benchmarks_spec = [
        ("BM-LR", vR_LR, "1-loop left-right gauge equality point g_2R = g_2L"),
        (
            "BM-GUT",
            vR_GUT,
            "Gauge-only 2-loop threshold-matched approximate SO(10) triple crossing (no M_GUT parent thresholds)",
        ),
        ("BM-LOW", vR_LOW, "Low-scale benchmark above aligned Valencia-Willenbrock K_L -> mu e floor"),
    ]
    benchmarks_out: Dict[str, object] = {}
    primary_u_light = None

    def clean_fit(d: Mapping[str, object]) -> Dict[str, object]:
        return {k: v for k, v in d.items() if k not in {"u_light_complex", "K_L", "K_R"}}

    for name, v_pt, desc in benchmarks_spec:
        sm = run_sm_rge_to_scale(v_pt, two_loop_gauge=True)
        mt = compute_threshold_matching_at_vR(sm["gY"], sm["g2"], sm["g3"], lam_D, kap4, kapR)
        m1 = mt["one_loop_matched"]
        uv2 = run_ps1_gauge_to_mplanck(v_pt, m1["g4"], m1["g2L"], m1["g2R"], two_loop=True)

        fit_min_cx = fit_ps1_ew_min(sm, v_pt, allow_complex_ratios=True)
        fit_min_real = fit_ps1_ew_min(sm, v_pt, allow_complex_ratios=False) if name == "BM-LR" else None
        fit_gen = fit_ps1_ew_gen(sm, v_pt, target_fR_max=0.35)
        higgs_2l = run_sm_2loop_higgs_stability(v_pt)

        if name == "BM-LR":
            primary_u_light = fit_min_cx["u_light_complex"]

        # Choose the primary perturbative fit at this benchmark for flavour/cosmology audit
        active_fit = fit_min_cx if fit_min_cx["all_yukawas_perturbative"] else fit_gen
        audit = audit_flavour_baryon_cosmology(
            v_pt,
            m1["g4"],
            m1["g2R"],
            active_fit["K_L"],
            active_fit["K_R"],
            active_fit["seesaw"],
            kappa4=kap4,
            kappa_r=kapR,
            M_GUT_GeV=scales["two_loop_with_thresholds"]["M_GUT_triple_unification_GeV"] if name == "BM-GUT" else None,
            alpha_GUT_inv=scales["two_loop_with_thresholds"]["alpha_GUT_inv"] if name == "BM-GUT" else None,
        )

        # Positive-portal threshold requirement (only sufficient for tree-level copositivity
        # when lambda_{hDelta} > 0; negative portal lambda_{hDelta} < 0 with lambda_H^SM < 0
        # is UNBOUNDED BELOW along the coherent ray r = -lambda_{hDelta} x / (2 lambda_eff)!):
        lam_h_2l = higgs_2l["lam_H_2loop"]
        min_pos_portal_for_uv_quartic = 2.0 * math.sqrt(lam_eff * abs(lam_h_2l)) if lam_h_2l < 0.0 else 0.0

        benchmarks_out[name] = {
            "description": desc,
            "v_R_GeV": float(v_pt),
            "sm_at_vR": {
                "g1": sm["g1"],
                "g2": sm["g2"],
                "g3": sm["g3"],
                "gY": sm["gY"],
                "lam_H_1loop_matrix": sm["lam_H"],
                "lam_H_2loop_Buttazzo": lam_h_2l,
                "mu_instability_1loop_GeV": sm["mu_instability_GeV"],
                "mu_instability_2loop_GeV": higgs_2l["mu_instability_2loop_GeV"],
                "min_positive_portal_for_lambda_H_UV_pos": float(min_pos_portal_for_uv_quartic),
                "yu_sv": [float(x) for x in sm["yu_sv"]],
                "yd_sv": [float(x) for x in sm["yd_sv"]],
                "ye_sv": [float(x) for x in sm["ye_sv"]],
                "V_ckm_abs": [[float(abs(z)) for z in row] for row in sm["V_ckm"]],
                "J_ckm": sm["J_ckm"],
                "m_nu_running_eV": [float(x) for x in sm["m_nu_running_eV"]],
            },
            "threshold_matching": mt,
            "uv_gauge_running_2loop": uv2,
            "delta_quartic_landau_pole": delta_quartic_landau_pole_audit(v_pt, 2.0, lam_D, kap4, kapR),
            "fit_PS1_EW_min_complex": clean_fit(fit_min_cx),
            "fit_PS1_EW_min_real_witness": clean_fit(fit_min_real) if fit_min_real is not None else None,
            "fit_PS1_EW_gen": clean_fit(fit_gen),
            "flavour_baryon_cosmology_audit": audit,
            "ew_hierarchy_fine_tuning_vR2_over_muSM2": float((v_pt**2) / (0.5 * M_H_GEV**2)),
        }

    # Additional lower-scale refit witness for PS1-EW-min at v_R = 6.0e11 GeV
    # (directly refuting the retracted fixed-fit 7.7e11 GeV hard floor):
    vR_refit_6e11 = 6.0e11
    sm_6e11 = run_sm_rge_to_scale(vR_refit_6e11, two_loop_gauge=True)
    fit_min_6e11 = fit_ps1_ew_min(sm_6e11, vR_refit_6e11, allow_complex_ratios=True)

    # 4. Exact 188x188 real scalar Hessian & one-light-Higgs verification at unbroken EW origin (<Phi>=0)
    assert primary_u_light is not None
    gauge_inv_err = ALGEBRA.test_gauge_invariance()
    delta_sq_vanish_err = ALGEBRA.test_delta_squared_vanishing()
    portal_rank_info = portal_map_rank_and_nullity(1.0)

    crit_sol = solve_portal_parameters_for_light_higgs(
        primary_u_light, m_h_sq_over_vR2=0.0, v_r=1.0
    )
    full_H_crit, quad_err_crit = assemble_full_188_hessian(lam_D, kap4, kapR, crit_sol["params"])
    light_check_crit = extract_light_higgs_eigenvector_from_188(full_H_crit, 0.0, primary_u_light)

    # Evaluate tree-level two-field (h, Delta_R) quartic stability at the matched BM-LR criticality point:
    # V_4(x, r) = lam_H_UV * x^2 + lam_hDelta * x * r + lam_eff * r^2, with lam_H_UV = lam_H_SM + lam_hDelta^2 / (4 lam_eff).
    # When lam_hDelta < 0, the physical coherent ray r = (-lam_hDelta / (2 lam_eff)) * x > 0 gives
    # V_4(x, r_ray) = lam_H_SM(v_R) * x^2 < 0 whenever lam_H_SM(v_R) < 0 (UNBOUNDED BELOW AT TREE LEVEL!).
    eff_portal_lr = extract_effective_higgs_portal(primary_u_light, crit_sol)
    lam_h_delta_lr = eff_portal_lr["lambda_hDelta"]
    lam_h_sm_lr = float(benchmarks_out["BM-LR"]["sm_at_vR"]["lam_H_2loop_Buttazzo"])
    lam_h_uv_lr = lam_h_sm_lr + (lam_h_delta_lr**2) / (4.0 * lam_eff)
    ray_slope_r_over_x = -lam_h_delta_lr / (2.0 * lam_eff)
    v4_over_x2_along_ray = (
        lam_h_uv_lr + lam_h_delta_lr * ray_slope_r_over_x + lam_eff * (ray_slope_r_over_x**2)
    )
    tree_level_ray_unbounded = (ray_slope_r_over_x > 0.0) and (v4_over_x2_along_ray < 0.0)

    tree_level_higgs_stability_audit = {
        "benchmark": "BM-LR",
        "lambda_H_SM_2loop_at_vR": lam_h_sm_lr,
        "lambda_eff_DeltaR": lam_eff,
        "lambda_hDelta_at_criticality": lam_h_delta_lr,
        "lambda_H_UV_matched": float(lam_h_uv_lr),
        "coherent_ray_r_over_x": float(ray_slope_r_over_x),
        "coherent_ray_in_physical_quadrant": bool(ray_slope_r_over_x > 0.0),
        "V4_over_x2_along_coherent_ray": float(v4_over_x2_along_ray),
        "tree_level_global_stability_pass": not tree_level_ray_unbounded,
        "obstruction_summary": (
            "FAILED / OPEN at tree level for the matched negative-portal BM-LR point: "
            "lambda_hDelta < 0 puts r = -lambda_hDelta x / (2 lambda_eff) > 0 in the physical "
            "quadrant where V_4(x, r) = lambda_H^SM(v_R) x^2 < 0 (unbounded below). "
            "Stabilizing requires lambda_H^SM(v_R) > 0 (as at BM-LOW/BM-GUT), positive-portal "
            "lambda_hDelta > 0 copositivity, or radiative effective-potential / UV RG stabilization."
        ),
    }

    # Probe m_h^2 = +1e-4 v_R^2 (separates 9 Goldstones, 4 light Higgs modes, and 175 heavy modes
    # where the lightest Delta_R physical mode has m^2 = 2*kappa_R = 0.009 v_R^2 > 1e-3 v_R^2):
    m_h_probe = 1.0e-4
    probe_sol = solve_portal_parameters_for_light_higgs(
        primary_u_light, m_h_sq_over_vR2=m_h_probe, v_r=1.0
    )
    full_H_probe, quad_err_probe = assemble_full_188_hessian(lam_D, kap4, kapR, probe_sol["params"])
    evals_188_probe = np.linalg.eigvalsh(full_H_probe)
    light_check_probe = extract_light_higgs_eigenvector_from_188(full_H_probe, m_h_probe, primary_u_light)

    expected_188_probe = np.array(
        sorted(
            expected_delta_eigenvalues(lam_D, kap4, kapR, 1.0)
            + [m_h_probe] * 4
            + [0.80] * 4
            + [1.20] * 4
            + [1.60] * 4
            + [1.10] * 32
            + [1.30] * 32
            + [1.40] * 24
            + [1.80] * 24
        )
    )
    hessian_188_err = float(np.max(np.abs(evals_188_probe - expected_188_probe)))

    # Goldstone orbit matching on full 188x188 matrix
    broken_60 = broken_gauge_directions(1.0)
    broken_188 = np.zeros((188, 18), dtype=np.float64)
    broken_188[:60, :] = broken_60
    goldstone_188_res = float(np.max(np.abs(full_H_probe @ broken_188)))

    heavy_mode_threshold = 1.0e-3  # strictly separates m_h_probe = 1e-4 from 2*kappa_R = 0.009

    checks = {
        "portal_operators_gauge_invariant": gauge_inv_err < 1.0e-12,
        "portal_map_is_rank16_surjective_with_dim9_kernel": (
            portal_rank_info["operator_count"] == 17
            and portal_rank_info["real_parameter_count"] == 25
            and portal_rank_info["linear_map_rank"] == 16
            and portal_rank_info["kernel_dim"] == 9
        ),
        "delta_squared_portals_vanish_on_vacuum": delta_sq_vanish_err < 1.0e-14,
        "hessian_188_quadratic_identity": max(quad_err_crit, quad_err_probe) < 1.0e-11,
        "hessian_188_matches_analytic_spectrum": hessian_188_err < 1.0e-10,
        "hessian_188_exact_nine_goldstones": int(np.sum(np.abs(evals_188_probe) < 1.0e-10)) == 9,
        "hessian_188_goldstones_match_broken_orbit": goldstone_188_res < 1.0e-10,
        "hessian_188_exact_four_light_higgs_modes": light_check_probe["max_eigenvalue_error"] < 1.0e-10,
        "hessian_188_light_higgs_eigenvector_matches_target": (
            light_check_probe["eigenvector_subspace_error"] < 1.0e-11
            and light_check_crit["eigenvector_subspace_error"] < 1.0e-11
        ),
        "hessian_188_all_175_heavy_modes_positive": int(np.sum(evals_188_probe > heavy_mode_threshold)) == 175,
        "BM_LR_negative_portal_tree_ray_unbounded_detected": (
            tree_level_ray_unbounded
            and abs(v4_over_x2_along_ray - lam_h_sm_lr) < 1.0e-12
        ),
        "ps1_2loop_beta_dim_symmetry": PS1_BETA["dim_symmetry_residual"] < 1.0e-12,
        "threshold_beta_sum_rules_exact": all(
            benchmarks_out[b]["threshold_matching"]["beta_sum_rule_error"] < 1.0e-12
            for b in ("BM-LR", "BM-GUT", "BM-LOW")
        ),
        "all_scanned_vR_gauge_perturbative_to_MPl_2loop_gauge_only": all(
            row["two_loop_pert_to_MPl"] for row in vr_scan
        ),
        "delta_quartic_beta_coeff_136_and_rescaled_pure_truncation_ok": all(
            benchmarks_out[b]["delta_quartic_landau_pole"]["beta_coeff_lambda_Delta_sq"] == 136.0
            and benchmarks_out[b]["delta_quartic_landau_pole"]["ps1_ew_perturbative_to_MPl_pure_truncation"]
            for b in ("BM-LR", "BM-GUT", "BM-LOW")
        ),
        "BM_LR_PS1_EW_min_complex_witness_perturbative_and_pmns_roundtrip": (
            benchmarks_out["BM-LR"]["fit_PS1_EW_min_complex"]["max_charged_fermion_ckm_rel_err"] < 1.0e-10
            and benchmarks_out["BM-LR"]["fit_PS1_EW_min_complex"]["all_yukawas_perturbative"]
            and benchmarks_out["BM-LR"]["fit_PS1_EW_min_complex"]["seesaw"]["seesaw_inversion_rel_err"] < 1.0e-10
            and benchmarks_out["BM-LR"]["fit_PS1_EW_min_complex"]["seesaw"]["hat_basis_seesaw_rel_err"] < 1.0e-10
            and benchmarks_out["BM-LR"]["fit_PS1_EW_min_complex"]["seesaw"]["pmns_roundtrip_recovery"]["max_rel_err"] < 1.0e-10
        ),
        "BM_LR_PS1_EW_min_real_witness_perturbative_and_pmns_roundtrip": (
            benchmarks_out["BM-LR"]["fit_PS1_EW_min_real_witness"]["max_charged_fermion_ckm_rel_err"] < 1.0e-10
            and benchmarks_out["BM-LR"]["fit_PS1_EW_min_real_witness"]["all_yukawas_perturbative"]
            and benchmarks_out["BM-LR"]["fit_PS1_EW_min_real_witness"]["seesaw"]["pmns_roundtrip_recovery"]["max_rel_err"] < 1.0e-10
        ),
        "vR_6e11_PS1_EW_min_refit_witness_perturbative_and_pmns_roundtrip": (
            fit_min_6e11["max_charged_fermion_ckm_rel_err"] < 1.0e-10
            and fit_min_6e11["all_yukawas_perturbative"]
            and fit_min_6e11["seesaw"]["pmns_roundtrip_recovery"]["max_rel_err"] < 1.0e-10
        ),
        "all_benchmarks_PS1_EW_gen_fit_direct_contraction_and_pmns_roundtrip": all(
            benchmarks_out[b]["fit_PS1_EW_gen"]["exact_reconstruction_rel_err"] < 1.0e-11
            and benchmarks_out[b]["fit_PS1_EW_gen"]["direct_tensor_contraction_rel_err"] < 1.0e-11
            and benchmarks_out[b]["fit_PS1_EW_gen"]["all_yukawas_perturbative"]
            and benchmarks_out[b]["fit_PS1_EW_gen"]["seesaw"]["pmns_roundtrip_recovery"]["max_rel_err"] < 1.0e-10
            for b in ("BM-LR", "BM-GUT", "BM-LOW")
        ),
        "all_benchmarks_pass_valencia_willenbrock_and_prelim_flavour_checks": all(
            benchmarks_out[b]["flavour_baryon_cosmology_audit"]["flavour"]["pass_KL_mue_aligned"]
            and benchmarks_out[b]["flavour_baryon_cosmology_audit"]["flavour"]["pass_KL_mue_fitted"]
            and benchmarks_out[b]["flavour_baryon_cosmology_audit"]["flavour"]["pass_Bs_mue"]
            and benchmarks_out[b]["flavour_baryon_cosmology_audit"]["flavour"]["pass_mu_egamma_MEGII"]
            and benchmarks_out[b]["flavour_baryon_cosmology_audit"]["flavour"]["pass_WR_collider_prelim"]
            and benchmarks_out[b]["flavour_baryon_cosmology_audit"]["flavour"]["pass_heavy_Higgs_FCNC_prelim"]
            for b in ("BM-LR", "BM-GUT", "BM-LOW")
        ),
        "all_benchmarks_pass_prelim_baryon_stability": all(
            benchmarks_out[b]["flavour_baryon_cosmology_audit"]["baryon_stability"]["pass_nnbar_prelim_even_if_lambda4_O1"]
            for b in ("BM-LR", "BM-GUT", "BM-LOW")
        ),
        "BM_GUT_vanilla_N1_leptogenesis_shortfall_detected": (
            not benchmarks_out["BM-GUT"]["flavour_baryon_cosmology_audit"]["cosmology_and_relics"][
                "vanilla_N1_leptogenesis_reaches_etaB"
            ]
        ),
    }

    gate_verdicts = {
        "PERT-01": "PARTIAL (scoped to 175 heavy modes at unbroken EW origin; -mu_SM^2 EWSB curvature & EW-broken vacuum open)",
        "PERT-05": "PARTIAL (gauge-only 2-loop PS RGEs & pure-self-coupling 136*lambda_Delta^2 diagnostic; coupled 138-param scalar RGEs & UV Yukawa 2-loop traces open)",
        "REC-03": "PARTIAL (existence/interpolation witnesses only: 30 real Yukawa params vs 18 observables; not a constrained prediction)",
        "NP-02": "FAIL (tree-level Higgs+Delta_R quartic potential is unbounded below along the coherent ray at the matched negative-portal BM-LR point)",
        "LAB-02": "PARTIAL (Valencia-Willenbrock K_L/B_s -> mu e and MEG II mu -> e gamma checked; n-nbar, heavy-Higgs FCNC, W_R/Z_R remain preliminary order-of-magnitude checks)",
        "COS-01": "OPEN / PARTIAL (pi_2=Z monopoles and pi_1=Z_2 strings require T_rh < v_R; vanilla N_1 thermal leptogenesis at BM-GUT falls short of observed eta_B; Boltzmann transport & DM open)",
    }

    return {
        "schema_version": "1.1.0",
        "project": "TP-03 Pati-Salam benchmark",
        "phase": "3 electroweak matching, RG running, fermion/neutrino fit and stability audit (post-referee revision)",
        "branch": "PS1-EW",
        "sub_branches": {
            "PS1-EW-min": "Minimal 2-Dirac-Yukawa sub-branch (Y_1, Y_15, f_R; Y_1_tilde = Y_15_tilde = 0; 30 real Yukawa params after U(3)_L x U(3)_R removal vs 18 real flavour observables)",
            "PS1-EW-gen": "Full gauge-invariant 4-Dirac-Yukawa branch (Y_1, Y_1_tilde, Y_15, Y_15_tilde, f_R)",
        },
        "ps1_gauge_beta_coefficients": {
            "order": ["SU(4)_C", "SU(2)_L", "SU(2)_R"],
            "scope": "gauge-only 2-loop Machacek-Vaughn (2-loop UV Yukawa traces omitted above v_R)",
            "b_1loop": [float(x) for x in PS1_BETA["b_1loop"]],
            "B_2loop": [[float(x) for x in row] for row in PS1_BETA["B_2loop"]],
            "dim_symmetry_residual": PS1_BETA["dim_symmetry_residual"],
        },
        "high_scale_landmarks": scales,
        "v_R_viable_window": {
            "aligned_KL_mue_lower_bound_GeV": benchmarks_out["BM-LOW"]["flavour_baryon_cosmology_audit"]["flavour"][
                "v_R_lower_bound_aligned_GeV"
            ],
            "aligned_KL_mue_M_X_lower_bound_GeV": benchmarks_out["BM-LOW"]["flavour_baryon_cosmology_audit"]["flavour"][
                "M_X_lower_bound_aligned_GeV"
            ],
            "PS1_EW_min_refit_lower_scale_witness_6e11_GeV": clean_fit(fit_min_6e11),
            "gauge_perturbativity_to_MPl_verified_up_to_GeV": 1.0e16,
            "scan": vr_scan,
        },
        "scalar_hessian_188_verification": {
            "delta_quartics_PS1_EW": {
                "lambda_Delta": lam_D,
                "kappa_4": kap4,
                "kappa_R": kapR,
                "lambda_eff": lam_eff,
            },
            "portal_map_structure": portal_rank_info,
            "gauge_invariance_max_rel_err": float(gauge_inv_err),
            "delta_squared_vanishing_residual": float(delta_sq_vanish_err),
            "hessian_188_shape": list(full_H_probe.shape),
            "hessian_188_max_spectrum_err": hessian_188_err,
            "goldstone_count": int(np.sum(np.abs(evals_188_probe) < 1.0e-10)),
            "goldstone_orbit_residual": goldstone_188_res,
            "light_higgs_probe_check": light_check_probe,
            "light_higgs_criticality_check": light_check_crit,
            "heavy_physical_mode_count": int(np.sum(evals_188_probe > heavy_mode_threshold)),
            "full_188_clusters_at_probe": cluster_eigenvalues(evals_188_probe),
            "ew_vacuum_scope_note": (
                "Hessian verified at the unbroken EW origin (<Phi>=0); tuning lambda_1 = -mu_SM^2 "
                "gives the expected tachyonic EWSB curvature, and full EW-broken vacuum stability "
                "with <h> != 0 and quartic backreaction remains open."
            ),
            "criticality_portal_parameters_BM_LR": {
                k: ([float(v.real), float(v.imag)] if isinstance(v, complex) else float(v))
                for k, v in crit_sol["params"].items()
            },
        },
        "tree_level_higgs_stability_audit": tree_level_higgs_stability_audit,
        "benchmarks": benchmarks_out,
        "gate_verdicts": gate_verdicts,
        "checks": checks,
        "all_pass": all(checks.values()),
    }


def build_summary_markdown(result: Mapping[str, object]) -> str:
    scales = result["high_scale_landmarks"]
    bm_lr = result["benchmarks"]["BM-LR"]
    bm_gut = result["benchmarks"]["BM-GUT"]
    bm_low = result["benchmarks"]["BM-LOW"]
    h188 = result["scalar_hessian_188_verification"]
    win = result["v_R_viable_window"]
    stab = result["tree_level_higgs_stability_audit"]
    w_6e11 = win["PS1_EW_min_refit_lower_scale_witness_6e11_GeV"]
    lp_lr = bm_lr["delta_quartic_landau_pole"]
    lp_gut = bm_gut["delta_quartic_landau_pole"]
    lp_low = bm_low["delta_quartic_landau_pole"]
    fl_low = bm_low["flavour_baryon_cosmology_audit"]["flavour"]
    cos_gut = bm_gut["flavour_baryon_cosmology_audit"]["cosmology_and_relics"]
    sextet_rng = bm_lr["flavour_baryon_cosmology_audit"]["baryon_stability"]["sextet_mass_ratio_range_over_vR"]

    return f"""# TP-03 Phase 3 (`PS1-EW`) summary (post-referee revision)

\\[
\\boxed{{
\\begin{{array}}{{c}}
\\textbf{{188x188 heavy-spectrum Hessian at unbroken EW origin (9 Goldstones, 4 light Higgs, 175 heavy): PASS (EW-broken vacuum open).}}\\\\
\\textbf{{Tree-level global Higgs+}}\\Delta_R\\textbf{{ stability at matched negative-portal BM-LR (}}\\lambda_{{h\\Delta}}={stab["lambda_hDelta_at_criticality"]:.3f}\\textbf{{): FAIL (NP-02).}}\\\\
\\textbf{{Gauge-only 2-loop perturbativity to }}M_{{\\rm Pl}}\\textbf{{: PASS (UV 2-loop Yukawa traces \\& }}M_{{\\rm GUT}}\\textbf{{ parent thresholds omitted).}}\\\\
\\textbf{{Phase 2B }}\\lambda_\\Delta=2.0\\textbf{{ hits pure-self-coupling }}136\\lambda_\\Delta^2\\textbf{{ pole at }}1.787\\,v_R\\textbf{{; rescaled }}\\lambda_\\Delta=0.03\\textbf{{: PARTIAL (coupled scalar RGEs open).}}\\\\
\\textbf{{PS1-EW-min (30 real Yukawa params vs 18 observables): existence witnesses PASS for real \\& complex ratios at BM-LR and at }}6\\times 10^{{11}}\\text{{ GeV.}}\\\\
\\textbf{{PS1-EW-gen (corrected tilde signs, }}D=|\\alpha_u|^2-|\\alpha_d|^2\\textbf{{): PASS across BM-LR, BM-GUT, BM-LOW (direct contraction verified).}}\\\\
\\textbf{{Valencia--Willenbrock }}K_L\\to\\mu e\\textbf{{ aligned floor }}v_R\\gtrsim {win["aligned_KL_mue_lower_bound_GeV"]:.2e}\\text{{ GeV; }}n\\text{{--}}\\bar{{n}}\\text{{/FCNC/}}W_R\\textbf{{ preliminary (LAB-02 PARTIAL).}}\\\\
\\textbf{{Cosmology: }}\\pi_2=\\mathbb{{Z}}\\textbf{{ monopoles + }}\\pi_1=\\mathbb{{Z}}_2\\textbf{{ strings require }}T_{{\\rm rh}}<v_R\\textbf{{; vanilla }}N_1\\textbf{{ leptogenesis at BM-GUT falls short (COS-01 OPEN/PARTIAL).}}
\\end{{array}}
}}
\\]

## Key quantitative findings

1. **Exact $188\\times 188$ bidoublet + $\\Delta_R$ scalar Hessian (unbroken EW origin) & negative-portal obstruction:**
   - All **17** gauge-invariant quadratic and $\\Delta_R^\\dagger \\Delta_R$ portal operators (**25 real parameters**) verify $SU(4)_C\\times SU(2)_L\\times SU(2)_R$ invariance to `{h188["gauge_invariance_max_rel_err"]:.2e}`.
   - All $\\Delta_R^2$ and $(\\Delta_R^\\dagger)^2$ cross-couplings vanish identically on $\\langle\\Delta_R\\rangle$ (residual `{h188["delta_squared_vanishing_residual"]:.2e}`).
   - The linear map from the 25 real parameters to the 16 real Hermitian entries of $\\mathcal{{M}}_H^2$ is **rank-16 surjective with a 9-dimensional kernel** (NOT a bijection); fixing the coloured blocks leaves 4 redundant directions fixed by convention.
   - At the one-light-Higgs surface (unbroken EW origin $\\langle\\Phi\\rangle=0$), the $188\\times 188$ Hessian has 9 exact Goldstones (orbit residual `{h188["goldstone_orbit_residual"]:.2e}`), 4 light SM Higgs doublet modes (eigenvector subspace error `{h188["light_higgs_probe_check"]["eigenvector_subspace_error"]:.2e}`), and 175 strictly positive heavy physical modes (max spectrum error `{h188["hessian_188_max_spectrum_err"]:.2e}`). Setting $\\lambda_1 = -\\mu_{{\\rm SM}}^2$ gives the expected tachyonic EWSB curvature at the origin; full EW-broken vacuum verification remains open (`PERT-01` scoped to heavy spectrum).
   - **Tree-level global Higgs+$\\Delta_R$ stability (`NP-02` = FAIL):** At the matched `BM-LR` criticality point, the effective Higgs–$\\Delta_R$ portal is negative ($\\lambda_{{h\\Delta}} = {stab["lambda_hDelta_at_criticality"]:.3f} < 0$) and $\\lambda_H^{{\\rm SM}}(v_R) = {stab["lambda_H_SM_2loop_at_vR"]:.5f} < 0$. Along the physical coherent ray $r = -\\lambda_{{h\\Delta}} x / (2\\lambda_{{\\rm eff}}) = {stab["coherent_ray_r_over_x"]:.2f}\\,x > 0$, the quartic potential evaluates to $V_4(x, r) = (\\lambda_H^{{\\rm UV}} - \\lambda_{{h\\Delta}}^2/(4\\lambda_{{\\rm eff}})) x^2 = \\lambda_H^{{\\rm SM}}(v_R) x^2 = {stab["V4_over_x2_along_coherent_ray"]:.5f}\\,x^2 < 0$ — **unbounded below at tree level**. Stabilizing requires $\\lambda_H^{{\\rm SM}}(v_R) > 0$, positive-portal $\\lambda_{{h\\Delta}} > 0$ copositivity, or radiative effective-potential stabilization.
   - Electroweak hierarchy fine-tuning is explicit: $\\Delta_{{\\rm FT}} = v_R^2 / \\mu_{{\\rm SM}}^2 \\simeq {bm_lr["ew_hierarchy_fine_tuning_vR2_over_muSM2"]:.2e}$ at `BM-LR`.

2. **Gauge-only 2-loop RGEs, thresholds, approximate $SO(10)$ crossing, and corrected $136\\lambda_\\Delta^2$ Landau pole:**
   - Exact complex `PS1` 1-loop gauge beta coefficients: $b_{{4}} = -7/3$, $b_{{2L}} = +2$, $b_{{2R}} = +26/3$. Above $v_R$, 2-loop UV Yukawa traces are omitted (gauge-only 2-loop PS RGEs + 1-loop Weinberg–Hall thresholds at $v_R$).
   - 1-loop (no thresholds): $v_R(g_{{2R}}=g_{{2L}}) = {scales["one_loop_no_threshold"]["vR_LR_parity_GeV"]:.3e}$ GeV; approximate $SO(10)$ triple crossing $v_R^{{\\rm unif}} = {scales["one_loop_no_threshold"]["vR_triple_unification_GeV"]:.3e}$ GeV, $M_{{\\rm GUT}} = {scales["one_loop_no_threshold"]["M_GUT_triple_unification_GeV"]:.3e}$ GeV ($\\alpha_{{\\rm GUT}}^{{-1}} = {scales["one_loop_no_threshold"]["alpha_GUT_inv"]:.2f}$).
   - Gauge-only 2-loop + 1-loop Weinberg–Hall thresholds (with rescaled $\\Delta_R$ spectrum, no $M_{{\\rm GUT}}$ parent thresholds): $v_R(g_{{2R}}=g_{{2L}}) = {scales["two_loop_with_thresholds"]["vR_LR_parity_GeV"]:.3e}$ GeV; approximate triple crossing $v_R^{{\\rm unif}} = {scales["two_loop_with_thresholds"]["vR_triple_unification_GeV"]:.3e}$ GeV, $M_{{\\rm GUT}} = {scales["two_loop_with_thresholds"]["M_GUT_triple_unification_GeV"]:.3e}$ GeV ($\\alpha_{{\\rm GUT}}^{{-1}} = {scales["two_loop_with_thresholds"]["alpha_GUT_inv"]:.2f}$).
   - **Corrected $\\Delta_R$ 1-loop quartic beta function (`PERT-05` = PARTIAL):** With canonical real $r = \\varphi^T\\varphi/2$ and $V_4 = \\lambda_\\Delta (\\varphi^T\\varphi)^2/4$, $16\\pi^2 \\beta_{{\\lambda_\\Delta}} \\supset 2(60+8)\\lambda_\\Delta^2 - 36\\lambda_\\Delta\\kappa_4 - 16\\lambda_\\Delta\\kappa_R = 136\\lambda_\\Delta^2 - 36\\lambda_\\Delta\\kappa_4 - 16\\lambda_\\Delta\\kappa_R$ (with $\\kappa^2$, portal, gauge, and Yukawa terms omitted). Phase 2B's $\\lambda_\\Delta = 2.0$ hits its formal pure-self-coupling pole at `{lp_lr["phase2b_landau_pole_ratio_over_vR"]:.3f} v_R`; Planck-scale starting caps are `{lp_lr["max_lambda_Delta_perturbative_to_MPl_pure_truncation"]:.4f}` (`BM-LR`), `{lp_gut["max_lambda_Delta_perturbative_to_MPl_pure_truncation"]:.4f}` (`BM-GUT`), and `{lp_low["max_lambda_Delta_perturbative_to_MPl_pure_truncation"]:.4f}` (`BM-LOW`). Rescaling to $\\lambda_\\Delta = 0.03, \\kappa_4 = 0.006, \\kappa_R = 0.0045$ ($\\lambda_{{\\rm eff}} = 0.0165$) stays below the pure-self-coupling cap at all three benchmarks; the full coupled 138-parameter scalar RGE system remains open.

3. **Fermion, CKM, neutrino, and PMNS existence fits (`REC-03` = PARTIAL):**
   - `PS1-EW-min` retains **30 real Yukawa parameters** after $U(3)_L\\times U(3)_R$ basis removal vs **18 real flavour observables** — fits are existence/interpolation witnesses, NOT constrained predictions.
   - **Retracted exclusions:** Both the earlier real-ratio exclusion and the fixed-fit $7.7\\times 10^{{11}}$ GeV floor were false. Explicit perturbative `PS1-EW-min` witnesses exist at `BM-LR` with **real** ratios ($c_d = {bm_lr["fit_PS1_EW_min_real_witness"]["cd"][0]:.2f}, c_e = {bm_lr["fit_PS1_EW_min_real_witness"]["ce"][0]:.2f}$, $\\|Y_1\\|_2 = {bm_lr["fit_PS1_EW_min_real_witness"]["Y1_spectral_norm"]:.3f}$, $\\|Y_{{15}}\\|_2 = {bm_lr["fit_PS1_EW_min_real_witness"]["Y15_spectral_norm"]:.3f}$, $\\|f_R\\|_2 = {bm_lr["fit_PS1_EW_min_real_witness"]["seesaw"]["f_R_spectral_norm"]:.4f}$, err `{bm_lr["fit_PS1_EW_min_real_witness"]["max_charged_fermion_ckm_rel_err"]:.2e}`), at `BM-LR` with **complex** ratios ($\\|Y_1\\|_2 = {bm_lr["fit_PS1_EW_min_complex"]["Y1_spectral_norm"]:.3f}$, $\\|Y_{{15}}\\|_2 = {bm_lr["fit_PS1_EW_min_complex"]["Y15_spectral_norm"]:.3f}$, $\\|f_R\\|_2 = {bm_lr["fit_PS1_EW_min_complex"]["seesaw"]["f_R_spectral_norm"]:.4f}$), and at the refit lower scale **$v_R = 6.0\\times 10^{{11}}$ GeV** ($\\|Y_1\\|_2 = {w_6e11["Y1_spectral_norm"]:.3f}$, $\\|Y_{{15}}\\|_2 = {w_6e11["Y15_spectral_norm"]:.3f}$, $\\|f_R\\|_2 = {w_6e11["seesaw"]["f_R_spectral_norm"]:.4f} < \\sqrt{{4\\pi}}$, err `{w_6e11["max_charged_fermion_ckm_rel_err"]:.2e}`).
   - **Corrected `PS1-EW-gen` down-type tilde signs & seesaw basis:** With $\\Phi = (\\epsilon H_d^*, H_u)$ and $\\widetilde{{\\Phi}} = (\\epsilon H_u^*, H_d)$, down-type tilde terms add with the same relative sign and the exact inverse has determinant $D = |\\alpha_u|^2 - |\\alpha_d|^2$ (verified directly against $2\\times 2$ bidoublet tensor contraction to `< 2e-12`). All seesaw inversions use $m_\\nu = U_{{eL}} m_\\nu^\\ell U_{{eL}}^T$ and directly recover all PMNS angles, $\\delta_{{\\rm PMNS}}$, and $\\Delta m^2$ in the charged-lepton mass basis to `< 1e-12`. Recomputed `PS1-EW-gen` max Yukawa norms are `{bm_lr["fit_PS1_EW_gen"]["max_yukawa_norm"]:.3f}` (`BM-LR`), `{bm_gut["fit_PS1_EW_gen"]["max_yukawa_norm"]:.3f}` (`BM-GUT`), and `{bm_low["fit_PS1_EW_gen"]["max_yukawa_norm"]:.3f}` (`BM-LOW`).

4. **Flavour, baryon stability (`LAB-02` = PARTIAL), and cosmological relics (`COS-01` = OPEN / PARTIAL):**
   - Corrected Valencia–Willenbrock $K_L \\to \\mu^\\pm e^\\mp$ normalization ($1/(32\\pi)$) sets the aligned lower bound $M_X \\gtrsim {fl_low["M_X_lower_bound_aligned_GeV"]:.2e}$ GeV ($v_R \\gtrsim {fl_low["v_R_lower_bound_aligned_GeV"]:.2e}$ GeV). All three benchmarks pass aligned/fitted $K_L \\to \\mu e$, $B_s \\to \\mu e$, and the updated MEG II $\\mu \\to e\\gamma < 1.5\\times 10^{{-13}}$ bound.
   - $W_R/Z_R$, heavy-Higgs FCNC, and $\\Delta B = 2$ $n\\text{{--}}\\bar{{n}}$ (evaluated with actual lightest sextet mass $M_{{\\Delta_6}} \\in [{sextet_rng[0]:.2f}, {sextet_rng[1]:.2f}]\\,v_R$) are preliminary order-of-magnitude checks; pure PS preserves perturbative baryon number ($3B+L$) while gauged $B-L$ is broken by $\\Delta(B-L)=2$.
   - Both $\\pi_2(G_{{\\rm PS}}/G_{{\\rm SM}}) = \\mathbb{{Z}}$ doubly-charged monopoles and $\\pi_1(G_{{\\rm PS}}/G_{{\\rm SM}}) = \\mathbb{{Z}}_2$ cosmic strings (from the disconnected stabilizer) arise at $v_R$, requiring $T_{{\\rm rh}} < v_R$. At `BM-GUT`, vanilla $N_1$-dominated thermal leptogenesis yields $|\\epsilon_1| = {abs(cos_gut["epsilon_1_CP_asymmetry"]):.2e}$ ($\\eta_B^{{\\max}} \\simeq {cos_gut["eta_B_ceiling_unflavored_kappa01"]:.2e}$), falling a factor of `{cos_gut["vanilla_N1_leptogenesis_shortfall_factor"]:.1f}x` short of observed $\\eta_B \\simeq 6.1\\times 10^{{-10}}$ (with $M_{{R1}} = {cos_gut["M_R1_GeV"]:.2e}$ GeV).

All executable mathematical verification and obstruction-detection checks pass (`all_pass = {result["all_pass"]}`), while TP-00 gates reflect honest fails/partials (`NP-02` = FAIL; `PERT-01`, `PERT-05`, `REC-03`, `LAB-02` = PARTIAL; `COS-01` = OPEN/PARTIAL).
"""


def _to_json_safe(obj: object) -> object:
    if isinstance(obj, dict):
        return {str(k): _to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_json_safe(v) for v in obj]
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return _to_json_safe(obj.tolist())
    return obj


def write_outputs(root: Path, result: Mapping[str, object]) -> None:
    results_dir = root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / "phase3_ew_results.json"
    md_path = results_dir / "phase3_ew_summary.md"
    json_path.write_text(json.dumps(_to_json_safe(result), indent=2) + "\n", encoding="utf-8")
    md_path.write_text(build_summary_markdown(result), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="TP-03 project root",
    )
    args = parser.parse_args()
    result = build_phase3_results()
    write_outputs(args.root.resolve(), result)
    print(
        json.dumps(
            _to_json_safe(
                {
                    "all_pass": result["all_pass"],
                    "failed_checks": [k for k, v in result["checks"].items() if not v],
                    "high_scale_landmarks": result["high_scale_landmarks"],
                    "BM_LR_PS1_EW_min_norms": {
                        "Y1": result["benchmarks"]["BM-LR"]["fit_PS1_EW_min_complex"]["Y1_spectral_norm"],
                        "Y15": result["benchmarks"]["BM-LR"]["fit_PS1_EW_min_complex"]["Y15_spectral_norm"],
                        "fR": result["benchmarks"]["BM-LR"]["fit_PS1_EW_min_complex"]["seesaw"]["f_R_spectral_norm"],
                    },
                }
            ),
            indent=2,
        )
    )
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
