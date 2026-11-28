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
    PERT_LIMIT,
    PS1_BETA,
    build_phase3_results,
    compute_threshold_matching_at_vR,
    delta_quartic_landau_pole_audit,
    run_sm_2loop_higgs_stability,
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

    def test_portal_gauge_invariance_and_delta_sq_vanishing(self):
        self.assertLess(self.h188["gauge_invariance_max_rel_err"], 1.0e-12)
        self.assertLess(self.h188["delta_squared_vanishing_residual"], 1.0e-14)
        # Independent fresh-seed check
        self.assertLess(ALGEBRA.test_gauge_invariance(seed=99991, trials=3), 1.0e-12)

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

    def test_gauge_perturbativity_unification_and_scalar_landau_pole(self):
        # All scanned v_R remain gauge-perturbative to M_Pl at 2-loop
        for row in self.result["v_R_viable_window"]["scan"]:
            self.assertTrue(row["one_loop_pert_to_MPl"])
            self.assertTrue(row["two_loop_pert_to_MPl"])
            self.assertLess(row["two_loop_max_g_MPl"], 1.0)

        # Exact 1-loop LR parity matches Phase 1 ~5.07e13 GeV
        vR_lr_1l = self.result["high_scale_landmarks"]["one_loop_no_threshold"]["vR_LR_parity_GeV"]
        self.assertGreater(vR_lr_1l, 4.9e13)
        self.assertLess(vR_lr_1l, 5.2e13)

        # 2-loop threshold-matched triple unification closes tightly below M_Pl
        u2 = self.result["high_scale_landmarks"]["two_loop_with_thresholds"]
        self.assertLess(u2["coupling_mismatch_at_M_GUT"], 1.0e-5)
        self.assertLess(u2["M_GUT_triple_unification_GeV"], M_PL_GEV)

        # Phase 2B lambda_Delta=2.0 hits sub-Planckian scalar Landau pole; PS1-EW lambda_Delta=0.08 passes
        for bm in (self.bm_lr, self.bm_gut, self.bm_low):
            lp = bm["delta_quartic_landau_pole"]
            self.assertTrue(lp["phase2b_sub_planckian_landau_pole"])
            self.assertLess(lp["phase2b_landau_pole_ratio_over_vR"], 3.5)
            self.assertTrue(lp["ps1_ew_perturbative_to_MPl"])

    def test_sm_2loop_higgs_instability_scale_and_threshold_stabilization(self):
        mu_inst = self.bm_lr["sm_at_vR"]["mu_instability_2loop_GeV"]
        self.assertGreater(mu_inst, 5.0e9)
        self.assertLess(mu_inst, 2.0e10)
        self.assertGreater(self.bm_low["sm_at_vR"]["lam_H_2loop_Buttazzo"], 0.0)
        self.assertLess(self.bm_lr["sm_at_vR"]["lam_H_2loop_Buttazzo"], 0.0)
        self.assertGreater(self.bm_lr["sm_at_vR"]["min_portal_coupling_for_UV_stability"], 0.0)
        self.assertLess(self.bm_lr["sm_at_vR"]["min_portal_coupling_for_UV_stability"], 0.2)

    def test_fermion_neutrino_fits_min_vs_gen_and_complex_phase_requirement(self):
        # BM-LR PS1-EW-min with complex phase passes perturbatively to < 1e-10
        f_min_cx = self.bm_lr["fit_PS1_EW_min_complex"]
        self.assertLess(f_min_cx["max_charged_fermion_ckm_rel_err"], 1.0e-10)
        self.assertLess(f_min_cx["matching_identity_residual"], 1.0e-12)
        self.assertTrue(f_min_cx["all_yukawas_perturbative"])
        self.assertLess(f_min_cx["seesaw"]["f_R_spectral_norm"], 1.0)
        self.assertLess(f_min_cx["seesaw"]["seesaw_inversion_rel_err"], 1.0e-12)
        self.assertLess(f_min_cx["seesaw"]["takagi_rel_err"], 1.0e-12)
        self.assertLess(f_min_cx["seesaw"]["sum_m_nu_eV"], EXP_BOUNDS["sum_mnu_cosmo_eV"])
        self.assertLess(f_min_cx["seesaw"]["m_beta_eV"], EXP_BOUNDS["m_beta_KATRIN_eV"])

        # BM-LR PS1-EW-min with REAL ratios fails f_R perturbativity
        f_min_re = self.bm_lr["fit_PS1_EW_min_real_control"]
        self.assertFalse(f_min_re["all_yukawas_perturbative"])
        self.assertGreater(f_min_re["seesaw"]["f_R_spectral_norm"], PERT_LIMIT)

        # BM-GUT and BM-LOW fail PS1-EW-min perturbativity
        self.assertFalse(self.bm_gut["fit_PS1_EW_min_complex"]["all_yukawas_perturbative"])
        self.assertFalse(self.bm_low["fit_PS1_EW_min_complex"]["all_yukawas_perturbative"])

        # PS1-EW-gen passes all three benchmarks with machine-precision reconstruction and perturbative Yukawas
        for bm in (self.bm_lr, self.bm_gut, self.bm_low):
            fg = bm["fit_PS1_EW_gen"]
            self.assertLess(fg["exact_reconstruction_rel_err"], 1.0e-12)
            self.assertTrue(fg["all_yukawas_perturbative"])
            self.assertLess(fg["max_yukawa_norm"], 1.5)

    def test_flavour_baryon_stability_and_cosmology_gates(self):
        # Generic K_L -> mu e bound sits at ~4.5e6 GeV
        vR_lb = self.result["v_R_viable_window"]["generic_KL_mue_lower_bound_GeV"]
        self.assertGreater(vR_lb, 2.0e6)
        self.assertLess(vR_lb, 1.0e7)

        for bm in (self.bm_lr, self.bm_gut, self.bm_low):
            aud = bm["flavour_baryon_cosmology_audit"]
            self.assertTrue(aud["flavour"]["pass_KL_mue_generic"])
            self.assertTrue(aud["flavour"]["pass_KL_mue_fitted"])
            self.assertTrue(aud["flavour"]["pass_Bs_mue"])
            self.assertTrue(aud["flavour"]["pass_mu_egamma"])
            self.assertTrue(aud["flavour"]["pass_WR_collider"])
            self.assertTrue(aud["flavour"]["pass_heavy_Higgs_FCNC"])
            self.assertTrue(aud["baryon_stability"]["pass_nnbar_even_if_lambda4_O1"])
            self.assertTrue(aud["cosmology_and_relics"]["requires_Trh_below_vR"])

        # Optional SO(10) proton decay at BM-GUT is safely above Super-K bound
        tau_p = self.bm_gut["flavour_baryon_cosmology_audit"]["baryon_stability"]["optional_SO10_d6_tau_p_yr"]
        self.assertGreater(tau_p, EXP_BOUNDS["tau_p_e_pi0_yr_90CL"])

        # Monopole-safe hierarchical thermal leptogenesis open at BM-LR and BM-GUT, closed at BM-LOW
        self.assertTrue(
            self.bm_lr["flavour_baryon_cosmology_audit"]["cosmology_and_relics"][
                "hierarchical_thermal_leptogenesis_compatible_with_monopole_inflation"
            ]
        )
        self.assertTrue(
            self.bm_gut["flavour_baryon_cosmology_audit"]["cosmology_and_relics"][
                "hierarchical_thermal_leptogenesis_compatible_with_monopole_inflation"
            ]
        )
        self.assertFalse(
            self.bm_low["flavour_baryon_cosmology_audit"]["cosmology_and_relics"][
                "hierarchical_thermal_leptogenesis_compatible_with_monopole_inflation"
            ]
        )


if __name__ == "__main__":
    unittest.main()
