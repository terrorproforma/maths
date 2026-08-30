from pathlib import Path
import json
import numpy as np

from chronometric_hpc.config import load_config
from chronometric_hpc.diagram_ledger import validate_ledger
from chronometric_hpc.tensor_basis import evaluate_basis_metrics, chiral_yukawa_basis, matrix_span_rank
from chronometric_hpc.renormalization import validate_closure, superficial_degree
from chronometric_hpc.benchmarks import run_benchmarks
from chronometric_hpc.contracts import validate_contract
from chronometric_hpc.preflight import run

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config' / 'hpc_solver_spec_portable_v1_9.yaml'
RESULTS = ROOT / 'inputs' / 'prehpc_closure_results_v1_8.json'


def test_ledger_exact_topology_checks():
    cfg = load_config(CONFIG)
    result = validate_ledger(cfg.diagram_ledger_path)
    assert result['all_pass'], result
    assert result['row_count'] == 11


def test_complete_component_tensor_spaces():
    m = evaluate_basis_metrics()
    assert m.clifford_rank == 16
    assert m.fermion_vertex_rank == 48
    assert m.fermion_vertex_transverse_residual < 1e-12
    assert m.scalar_vertex_rank == 3
    assert m.yukawa_chiral_rank == 4
    assert matrix_span_rank(chiral_yukawa_basis('L_to_R')) == 4
    assert m.three_gauge_rank == 27
    assert m.three_gauge_transverse_residual < 1e-12


def test_power_counting_and_counterterm_closure():
    cfg = load_config(CONFIG)
    closure = validate_closure(cfg.counterterm_matrix_path)
    assert closure['all_pass'], closure
    assert superficial_degree(n_boson=2) == 2
    assert superficial_degree(n_fermion=2) == 1
    assert superficial_degree(n_boson=4) == 0
    assert superficial_degree(n_boson=5) < 0


def test_analytic_benchmark_hierarchy():
    result = run_benchmarks()
    assert result['all_pass'], result


def test_observable_error_contract_complete():
    cfg = load_config(CONFIG)
    result = validate_contract(cfg.observable_contract_path)
    assert result['all_pass'], result


def test_integrated_preflight():
    report = run(CONFIG, RESULTS)
    assert report['all_pass'], json.dumps(report, indent=2)
