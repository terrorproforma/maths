from pathlib import Path
import json
import numpy as np
from chronometric_hpc.config import load_config
from chronometric_hpc.kernels import MatchedKernel
from chronometric_hpc.bse import separable_ladder

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "hpc_solver_spec_v1_8.yaml"
RESULTS = Path("/mnt/data/prehpc_closure_results_v1_8.json")


def test_config_and_table_exist():
    cfg = load_config(CONFIG)
    assert cfg.table_path.exists()


def test_factorization_scale_cancels():
    cfg = load_config(CONFIG)
    ker = MatchedKernel.load(cfg.table_path)
    assert ker.factorization_spread() < cfg.acceptance["factorization_scale_relative_spread_max"]


def test_precomputed_acceptance_metrics():
    cfg = load_config(CONFIG)
    r = json.loads(RESULTS.read_text())
    assert r["pointwise_matching"]["on_shell_max_interpolation_residual"] < cfg.acceptance["on_shell_width_relative_error_max"]
    assert r["vertex_and_STI_closure"]["STI_max_relative_residual"] < cfg.acceptance["quantum_STI_relative_residual_max"]
    assert r["singlet_BSE"]["positive_frequency_minimum"] >= 0.0


def test_separable_bse_identity():
    chi0 = np.array([[0.2-0.1j, 0.1-0.02j]])
    chi, vertex, residual = separable_ladder(chi0, np.array([0.08]))
    assert residual < 1.0e-14
    assert np.all(np.isfinite(chi))
    assert np.all(np.isfinite(vertex))
