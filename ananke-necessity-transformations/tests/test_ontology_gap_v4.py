"""Unit tests for ANANKE v4 quantum realizations, dynamical gap, and ontology comparison."""

from __future__ import annotations

from math import sqrt
import unittest

import numpy as np

from ananke import (
    QuantumRealization,
    dynamical_bloch_polytope_contraction_summary,
    fejes_toth_inradius_upper_bound,
    optimize_two_symbol_classical_hmm,
    qubit_quantum_realization,
    qubit_rotation_process,
    qudit_two_symbol_quantum_realization,
    validate_quantum_realization,
    words_upto,
)


class OntologyGapV4Tests(unittest.TestCase):
    def test_qubit_quantum_realization_matches_bloch_linear_process(self) -> None:
        """Exact d=2 QuantumRealization matches qubit_rotation_process on all words <= 5."""
        r0 = np.array([0.23, -0.41, 0.71])
        m0 = np.array([0.4, 0.7, -0.2])
        q_real = qubit_quantum_realization(0.73, 1.11, initial_bloch=r0, measurement_axis=m0)
        lin_from_q = q_real.to_linear_process()
        bloch_proc = qubit_rotation_process(0.73, 1.11, initial_bloch=r0, measurement_axis=m0)

        self.assertEqual(q_real.hilbert_dimension, 2)
        self.assertEqual(q_real.liouville_dimension, 4)
        for w in words_upto(("x", "z"), 5):
            p_q = q_real.behavior(w)
            p_l = lin_from_q.behavior(w)
            p_b = bloch_proc.behavior(w)
            self.assertAlmostEqual(p_q, p_b, places=12)
            self.assertAlmostEqual(p_l, p_b, places=12)

    def test_qudit_quantum_realization_validation_and_liouville_equivalence(self) -> None:
        """d=3, 4 QuantumRealizations pass strict CPTP/POVM checks and match their d^2 Liouville process."""
        for d in (3, 4):
            q_real = qudit_two_symbol_quantum_realization(d, seed=d)
            self.assertEqual(q_real.hilbert_dimension, d)
            self.assertEqual(q_real.liouville_dimension, d * d)
            lin = q_real.to_linear_process()
            self.assertEqual(lin.dimension, d * d)
            for w in words_upto(("x", "z"), 4):
                p_q = q_real.behavior(w)
                p_l = lin.behavior(w)
                self.assertGreaterEqual(p_q, -1e-12)
                self.assertLessEqual(p_q, 1.0 + 1e-12)
                self.assertAlmostEqual(p_q, p_l, places=11)

    def test_validate_quantum_realization_rejects_invalid_operators(self) -> None:
        """Strict quantum validator rejects non-PSD states, non-unitary maps, and invalid POVMs."""
        eye2 = np.eye(2, dtype=complex)
        rho_bad = np.diag([1.2, -0.2]).astype(complex)
        with self.assertRaises(ValueError):
            validate_quantum_realization(("x",), rho_bad, {"x": eye2}, 0.5 * eye2)

        u_bad = 2.0 * eye2
        with self.assertRaises(ValueError):
            validate_quantum_realization(("x",), 0.5 * eye2, {"x": u_bad}, 0.5 * eye2)

        e_bad = np.diag([1.5, 0.2]).astype(complex)
        with self.assertRaises(ValueError):
            validate_quantum_realization(("x",), 0.5 * eye2, {"x": eye2}, e_bad)

    def test_fejes_toth_inradius_exact_platonic_values(self) -> None:
        """Fejes Toth formula is exact for tetrahedron (N=4), octahedron (N=6), icosahedron (N=12)."""
        self.assertAlmostEqual(fejes_toth_inradius_upper_bound(4), 1.0 / 3.0, places=12)
        self.assertAlmostEqual(fejes_toth_inradius_upper_bound(6), 1.0 / sqrt(3.0), places=12)
        self.assertAlmostEqual(
            fejes_toth_inradius_upper_bound(12), sqrt((5.0 + 2.0 * sqrt(5.0)) / 15.0), places=12
        )
        # Strictly increasing with N and bounded below 1
        vals = [fejes_toth_inradius_upper_bound(n) for n in (4, 6, 8, 12, 32, 64, 128)]
        for a, b in zip(vals, vals[1:]):
            self.assertLess(a, b)
            self.assertLess(b, 1.0)
        summary = dynamical_bloch_polytope_contraction_summary(128, depth=7)
        self.assertGreater(summary["implied_amplitude_loss_lb"], 0.05)

    def test_unconstrained_two_symbol_hmm_returns_valid_classical_realization(self) -> None:
        """Unconstrained 2-symbol HMM optimizer returns a strictly verified classical realization."""
        proc = qubit_rotation_process(theta_x=0.73, theta_z=1.11)
        words = words_upto(("x", "z"), 4)
        res = optimize_two_symbol_classical_hmm(proc, words, order=4, restarts=2, maxiter=60, seed=0)
        self.assertEqual(res.realization.state_count, 4)
        self.assertEqual(res.word_count, len(words))
        mx, rms = res.realization.error_on_words(proc, words)
        self.assertAlmostEqual(mx, res.max_error, places=12)
        self.assertAlmostEqual(rms, res.rms_error, places=12)


if __name__ == "__main__":
    unittest.main()
