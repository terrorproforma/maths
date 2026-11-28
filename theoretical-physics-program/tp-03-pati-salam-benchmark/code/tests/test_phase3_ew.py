import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from verify_phase3_ew_matching import (  # noqa: E402
    ALGEBRA,
    EXP_BOUNDS,
    M_PL_GEV,
    NEUTRINO_INPUTS,
    PERT_LIMIT,
    PS1_BETA,
    build_phase3_results,
    compute_seesaw_and_leptogenesis,
    delta_quartic_landau_pole_audit,
    portal_map_rank_and_nullity,
    verify_yukawa_forward_contraction,
)


class Phase3ScalarHessianAndRGTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_phase3_results()
        cls.checks = cls.result["checks"]
        cls.h188 = cls.result["scalar_hessian_188_verification"]
        cls.bm_lr = cls.result["benchmarks"]["BM-LR"]
        cls.bm_gut = cls.result["benchmarks"]["BM-GUT"]
        cls.bm_low = cls.result["benchmarks"]["BM-LOW"]

    def test_all_master_checks_pass(self):
        failed = [k for k, v in self.checks.items() if not v]
        self.assertEqual(failed, [], f"Failed Phase 3 checks: {failed}")
        self.assertTrue(self.result["all_pass"])

    def test_portal_gauge_invariance_rank_and_delta_sq_vanishing(self):
        self.assertLess(self.h188["gauge_invariance_max_rel_err"], 1.0e-12)
        self.assertLess(self.h188["delta_squared_vanishing_residual"], 1.0e-14)
        # Independent fresh-seed check
        self.assertLess(ALGEBRA.test_gauge_invariance(seed=99991, trials=3), 1.0e-12)
        # Exact linear map: 17 operators (25 real params) -> rank-16 surjective onto M_H^2, kernel dim 9
        info = portal_map_rank_and_nullity(1.0)
        self.assertEqual(info["operator_count"], 17)
        self.assertEqual(info["real_parameter_count"], 25)
        self.assertEqual(info["linear_map_rank"], 16)
        self.assertEqual(info["kernel_dim"], 9)

    def test_full_188_hessian_one_light_higgs_and_nine_goldstones(self):
        self.assertEqual(self.h188["hessian_188_shape"], [188, 188])
        self.assertEqual(self.h188["goldstone_count"], 9)
        self.assertEqual(self.h188["heavy_physical_mode_count"], 175)
        self.assertLess(self.h188["goldstone_orbit_residual"], 1.0e-10)
        self.assertLess(self.h188["hessian_188_max_spectrum_err"], 1.0e-10)
        self.assertLess(self.h188["light_higgs_probe_check"]["eigenvector_subspace_error"], 1.0e-11)
        self.assertLess(self.h188["light_higgs_criticality_check"]["eigenvector_subspace_error"], 1.0e-11)

    def test_ps1_beta_functions_and_threshold_sum_rules(self):
        b1 = PS1_BETA["b_1loop"]
        self.assertAlmostEqual(b1[0], -7.0 / 3.0, places=12)
        self.assertAlmostEqual(b1[1], 2.0, places=12)
        self.assertAlmostEqual(b1[2], 26.0 / 3.0, places=12)
        self.assertLess(PS1_BETA["dim_symmetry_residual"], 1.0e-12)

        for bm in (self.bm_lr, self.bm_gut, self.bm_low):
            mt = bm["threshold_matching"]
            self.assertEqual(mt["heavy_vector_real_dof"], 9)
            self.assertEqual(mt["heavy_scalar_real_dof"], 175)
            self.assertLess(mt["beta_sum_rule_error"], 1.0e-12)

    def test_gauge_perturbativity_unification_and_corrected_136_scalar_landau_pole(self):
        # All scanned v_R remain gauge-perturbative to M_Pl at gauge-only 2-loop
        for row in self.result["v_R_viable_window"]["scan"]:
            self.assertTrue(row["one_loop_pert_to_MPl"])
            self.assertTrue(row["two_loop_pert_to_MPl"])
            self.assertLess(row["two_loop_max_g_MPl"], 1.0)

        # Exact 1-loop LR parity matches Phase 1 ~5.08e13 GeV
        vR_lr_1l = self.result["high_scale_landmarks"]["one_loop_no_threshold"]["vR_LR_parity_GeV"]
        self.assertGreater(vR_lr_1l, 4.9e13)
        self.assertLess(vR_lr_1l, 5.2e13)

        # Gauge-only 2-loop threshold-matched approximate triple crossing closes below M_Pl
        u2 = self.result["high_scale_landmarks"]["two_loop_with_thresholds"]
        self.assertLess(u2["coupling_mismatch_at_M_GUT"], 1.0e-5)
        self.assertLess(u2["M_GUT_triple_unification_GeV"], M_PL_GEV)

        # Exact O(60) 1-loop beta coefficient = 2*(60+8) = 136 (NOT 68!), mixed terms -36, -16
        # Phase 2B lambda_Delta = 2.0 hits formal pole at exp(16 pi^2 / (136*2)) = 1.787 v_R
        for bm in (self.bm_lr, self.bm_gut, self.bm_low):
            lp = bm["delta_quartic_landau_pole"]
            self.assertEqual(lp["beta_coeff_lambda_Delta_sq"], 136.0)
            self.assertEqual(lp["beta_coeff_lambda_Delta_kappa4"], -36.0)
            self.assertEqual(lp["beta_coeff_lambda_Delta_kappaR"], -16.0)
            self.assertTrue(lp["phase2b_sub_planckian_landau_pole"])
            self.assertAlmostEqual(lp["phase2b_landau_pole_ratio_over_vR"], 1.787048, places=4)
            self.assertTrue(lp["ps1_ew_perturbative_to_MPl_pure_truncation"])

        # Verify pure-self-coupling Planck starting caps at BM-LR (~0.0937) and BM-LOW (~0.0417)
        self.assertAlmostEqual(
            self.bm_lr["delta_quartic_landau_pole"]["max_lambda_Delta_perturbative_to_MPl_pure_truncation"],
            0.0937,
            places=3,
        )
        self.assertAlmostEqual(
            self.bm_low["delta_quartic_landau_pole"]["max_lambda_Delta_perturbative_to_MPl_pure_truncation"],
            0.0417,
            places=3,
        )

    def test_negative_portal_tree_level_higgs_stability_obstruction(self):
        mu_inst = self.bm_lr["sm_at_vR"]["mu_instability_2loop_GeV"]
        self.assertGreater(mu_inst, 5.0e9)
        self.assertLess(mu_inst, 2.0e10)
        self.assertGreater(self.bm_low["sm_at_vR"]["lam_H_2loop_Buttazzo"], 0.0)
        self.assertLess(self.bm_lr["sm_at_vR"]["lam_H_2loop_Buttazzo"], 0.0)

        # At the matched BM-LR criticality point, lambda_hDelta < 0 renders V_4 unbounded below
        # along the physical coherent ray r = -lambda_hDelta x / (2 lambda_eff) > 0!
        stab = self.result["tree_level_higgs_stability_audit"]
        self.assertLess(stab["lambda_hDelta_at_criticality"], -1.0)
        self.assertTrue(stab["coherent_ray_in_physical_quadrant"])
        self.assertLess(stab["V4_over_x2_along_coherent_ray"], 0.0)
        self.assertAlmostEqual(
            stab["V4_over_x2_along_coherent_ray"],
            stab["lambda_H_SM_2loop_at_vR"],
            places=12,
        )
        self.assertFalse(stab["tree_level_global_stability_pass"])
        self.assertTrue(self.result["gate_verdicts"]["NP-02"].startswith("FAIL"))

    def test_direct_yukawa_forward_contraction_and_tilde_signs(self):
        # Independent random check of Phi = (eps H_d^*, H_u) and Phi_tilde = eps Phi^* eps^T = (eps H_u^*, H_d)
        rng = np.random.default_rng(20261129)
        u_rand = rng.normal(size=4) + 1j * rng.normal(size=4)
        u_rand /= np.linalg.norm(u_rand)
        # Ensure away from |a_u| == |a_d| singularity
        if abs(abs(u_rand[0]) ** 2 - abs(u_rand[1]) ** 2) < 0.05:
            u_rand[0] *= 1.5
            u_rand /= np.linalg.norm(u_rand)
        if abs(abs(u_rand[2]) ** 2 - abs(u_rand[3]) ** 2) < 0.05:
            u_rand[2] *= 1.5
            u_rand /= np.linalg.norm(u_rand)

        Yu_t = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        Yd_t = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        Ye_t = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        Ynu_t = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))

        a1u, a1d, a15u, a15d = u_rand
        D1 = abs(a1u) ** 2 - abs(a1d) ** 2
        D15 = abs(a15u) ** 2 - abs(a15d) ** 2
        Au, Ad = (3.0 * Yu_t + Ynu_t) / 4.0, (3.0 * Yd_t + Ye_t) / 4.0
        Bu, Bd = (Yu_t - Ynu_t) / 4.0, (Yd_t - Ye_t) / 4.0
        Y1 = (a1u.conjugate() * Au - a1d * Ad) / D1
        Y1_t = (-a1d.conjugate() * Au + a1u * Ad) / D1
        Y15 = math.sqrt(12.0) * (a15u.conjugate() * Bu - a15d * Bd) / D15
        Y15_t = math.sqrt(12.0) * (-a15d.conjugate() * Bu + a15u * Bd) / D15

        # Forward contraction via literal 2x2 SU(2)_L x SU(2)_R matrices Phi and Phi_tilde
        out = verify_yukawa_forward_contraction(u_rand, Y1, Y1_t, Y15, Y15_t)
        self.assertLess(np.linalg.norm(out["Yu"] - Yu_t) / np.linalg.norm(Yu_t), 1.0e-12)
        self.assertLess(np.linalg.norm(out["Yd"] - Yd_t) / np.linalg.norm(Yd_t), 1.0e-12)
        self.assertLess(np.linalg.norm(out["Ye"] - Ye_t) / np.linalg.norm(Ye_t), 1.0e-12)
        self.assertLess(np.linalg.norm(out["YnuD"] - Ynu_t) / np.linalg.norm(Ynu_t), 1.0e-12)

        # Verify singularity when |a_u| == |a_d|
        M_sing = np.array([[0.5, 0.5j], [-0.5j, 0.5]], dtype=np.complex128)
        self.assertAlmostEqual(abs(np.linalg.det(M_sing)), 0.0, places=14)

    def test_seesaw_charged_lepton_basis_pmns_roundtrip_independent(self):
        # Independent check with non-trivial complex unitary UeL and non-diagonal YnuD
        rng = np.random.default_rng(777)
        A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        UeL, _ = np.linalg.qr(A)
        YnuD = 0.05 * (rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)))
        m_nu_eV = np.array([0.015, math.sqrt(0.015**2 + NEUTRINO_INPUTS["dm21_sq_eV2"]), math.sqrt(0.015**2 + NEUTRINO_INPUTS["dm31_sq_eV2"])])
        ss = compute_seesaw_and_leptogenesis(YnuD, UeL, 1.0e13, m_nu_eV)
        self.assertLess(ss["seesaw_inversion_rel_err"], 1.0e-12)
        self.assertLess(ss["hat_basis_seesaw_rel_err"], 1.0e-12)
        self.assertLess(ss["takagi_rel_err"], 1.0e-12)
        rt = ss["pmns_roundtrip_recovery"]
        self.assertLess(rt["max_rel_err"], 1.0e-11)
        self.assertAlmostEqual(rt["sin2_th12"], NEUTRINO_INPUTS["sin2_th12"], places=10)
        self.assertAlmostEqual(rt["sin2_th23"], NEUTRINO_INPUTS["sin2_th23"], places=10)
        self.assertAlmostEqual(rt["sin2_th13"], NEUTRINO_INPUTS["sin2_th13"], places=10)
        self.assertAlmostEqual(rt["delta_pmns_deg"], NEUTRINO_INPUTS["delta_pmns_deg"], places=8)

    def test_fermion_neutrino_fits_real_witness_lower_vR_refit_and_gen(self):
        # 1. BM-LR PS1-EW-min with complex ratios passes perturbatively + PMNS round-trip
        f_min_cx = self.bm_lr["fit_PS1_EW_min_complex"]
        self.assertLess(f_min_cx["max_charged_fermion_ckm_rel_err"], 1.0e-10)
        self.assertLess(f_min_cx["matching_identity_residual"], 1.0e-12)
        self.assertTrue(f_min_cx["all_yukawas_perturbative"])
        self.assertLess(f_min_cx["seesaw"]["f_R_spectral_norm"], 1.0)
        self.assertLess(f_min_cx["seesaw"]["pmns_roundtrip_recovery"]["max_rel_err"], 1.0e-10)
        self.assertLess(f_min_cx["seesaw"]["sum_m_nu_eV"], EXP_BOUNDS["sum_mnu_cosmo_eV"])
        self.assertLess(f_min_cx["seesaw"]["m_beta_eV"], EXP_BOUNDS["m_beta_KATRIN_eV"])

        # 2. BM-LR PS1-EW-min with REAL ratios ALSO passes perturbatively (retracting false exclusion!)
        f_min_re = self.bm_lr["fit_PS1_EW_min_real_witness"]
        self.assertLess(f_min_re["max_charged_fermion_ckm_rel_err"], 1.0e-10)
        self.assertTrue(f_min_re["all_yukawas_perturbative"])
        self.assertLess(f_min_re["seesaw"]["f_R_spectral_norm"], 1.0)
        self.assertAlmostEqual(f_min_re["cd"][1], 0.0, places=15)
        self.assertAlmostEqual(f_min_re["ce"][1], 0.0, places=15)
        self.assertLess(f_min_re["seesaw"]["pmns_roundtrip_recovery"]["max_rel_err"], 1.0e-10)

        # 3. Lower-scale refit at v_R = 6.0e11 GeV passes perturbatively (retracting false 7.7e11 GeV floor!)
        f_6e11 = self.result["v_R_viable_window"]["PS1_EW_min_refit_lower_scale_witness_6e11_GeV"]
        self.assertLess(f_6e11["max_charged_fermion_ckm_rel_err"], 1.0e-10)
        self.assertTrue(f_6e11["all_yukawas_perturbative"])
        self.assertLess(f_6e11["seesaw"]["f_R_spectral_norm"], PERT_LIMIT)
        self.assertLess(f_6e11["seesaw"]["pmns_roundtrip_recovery"]["max_rel_err"], 1.0e-10)

        # 4. PS1-EW-gen passes all three benchmarks with corrected tilde signs & direct contraction
        for bm in (self.bm_lr, self.bm_gut, self.bm_low):
            fg = bm["fit_PS1_EW_gen"]
            self.assertLess(fg["exact_reconstruction_rel_err"], 1.0e-11)
            self.assertLess(fg["direct_tensor_contraction_rel_err"], 1.0e-11)
            self.assertTrue(fg["all_yukawas_perturbative"])
            self.assertLess(fg["max_yukawa_norm"], PERT_LIMIT)
            self.assertLess(fg["seesaw"]["pmns_roundtrip_recovery"]["max_rel_err"], 1.0e-10)

    def test_flavour_baryon_stability_and_cosmology_gates(self):
        # Corrected Valencia-Willenbrock 1/(32 pi) aligned K_L -> mu e floor:
        # M_X >= 2.04e6 GeV, v_R >= 3.78e6 GeV
        mx_lb = self.result["v_R_viable_window"]["aligned_KL_mue_M_X_lower_bound_GeV"]
        vR_lb = self.result["v_R_viable_window"]["aligned_KL_mue_lower_bound_GeV"]
        self.assertGreater(mx_lb, 1.95e6)
        self.assertLess(mx_lb, 2.15e6)
        self.assertGreater(vR_lb, 3.60e6)
        self.assertLess(vR_lb, 3.95e6)

        # Updated MEG II bound
        self.assertAlmostEqual(EXP_BOUNDS["BR_mu_egamma_90CL"], 1.5e-13, places=16)

        for bm in (self.bm_lr, self.bm_gut, self.bm_low):
            aud = bm["flavour_baryon_cosmology_audit"]
            self.assertTrue(aud["flavour"]["pass_KL_mue_aligned"])
            self.assertTrue(aud["flavour"]["pass_KL_mue_fitted"])
            self.assertTrue(aud["flavour"]["pass_Bs_mue"])
            self.assertTrue(aud["flavour"]["pass_mu_egamma_MEGII"])
            self.assertTrue(aud["flavour"]["pass_WR_collider_prelim"])
            self.assertTrue(aud["flavour"]["pass_heavy_Higgs_FCNC_prelim"])
            self.assertTrue(aud["baryon_stability"]["pass_nnbar_prelim_even_if_lambda4_O1"])
            # Actual sextet masses are sqrt(2*kappa4) to sqrt(2*kappa4 + 2*kappaR) * v_R (~0.11-0.14 v_R)
            sr = aud["baryon_stability"]["sextet_mass_ratio_range_over_vR"]
            self.assertLess(sr[0], 0.25)
            self.assertGreater(sr[0], 0.05)
            self.assertTrue(aud["cosmology_and_relics"]["requires_Trh_below_vR"])
            self.assertIn("Z_2", aud["cosmology_and_relics"]["homotopy_pi1_GPS_over_GSM"])

        # Vanilla N_1-dominated thermal leptogenesis at BM-GUT falls short of observed eta_B
        cos_gut = self.bm_gut["flavour_baryon_cosmology_audit"]["cosmology_and_relics"]
        self.assertFalse(cos_gut["vanilla_N1_leptogenesis_reaches_etaB"])
        self.assertGreater(cos_gut["vanilla_N1_leptogenesis_shortfall_factor"], 1.0)


if __name__ == "__main__":
    unittest.main()
