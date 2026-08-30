from pathlib import Path
import os

from frontier_evidence.formal_core import run as run_formal
from frontier_evidence.qcd_threshold import run as run_qcd
from frontier_evidence.rg_audit import run as run_rg
from frontier_evidence.scalar_two_time import run as run_scalar
from frontier_evidence.threepi_combinatorics import run as run_threepi
from frontier_evidence.nu0_fate import run as run_nu
from frontier_evidence.compact_objects import run as run_compact
from frontier_evidence.uv_quality import run as run_uv
from frontier_evidence.kernel_uncertainty import run as run_kernel
from frontier_evidence.lpm_repair import run as run_lpm
from frontier_evidence.portability import run as run_portability


REPO_ROOT = Path(os.environ.get("CHRONOMETRIC_REPO_ROOT", Path(__file__).resolve().parents[3]))
PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_formal_and_rg_scope():
    formal = run_formal()
    assert formal["universal_clock_factorisation"]["status"] == "EXACT_ELEMENTARY_THEOREM"
    assert formal["v0_2_relations"]["status"] == "RETIRED_AS_UNIVERSAL_CLAIMS"
    qcd = run_qcd()
    assert abs(qcd["one_loop_exact"] - 2 / 27) < 1e-15
    assert 0.02 < qcd["relative_NLO_shift"] < 0.06
    rg = run_rg()
    assert rg["cancellation_is_exact"]
    assert rg["scientific_verdict"] == "RETRACTED"
    assert rg["fixed_order_scale_derivative"] != "0"


def test_scalar_two_time_is_fallible_and_converged():
    summary, arrays = run_scalar()
    assert summary["all_gates_pass"], summary
    assert arrays["rho_exact_bath"].shape == arrays["F_exact_bath"].shape
    assert min(summary["observed_orders"]) > 2.8
    assert summary["memory_window_relative_l2_changes"]["12"] < 0.002


def test_threepi_magnitudes_are_independently_reproduced():
    result = run_threepi()
    assert result["all_magnitudes_match"], result
    assert len(result["rows"]) == 11
    assert {row["automorphism_order"] for row in result["rows"]} >= {1, 2, 3, 4, 6, 8, 12, 24, 48}


def test_cosmology_repairs_and_blockers_are_explicit():
    nu = run_nu()
    assert nu["sterile_cascade"]["DeltaNeff_total"] > 0.1
    assert nu["all_repair_gates_pass"], nu
    compact = run_compact()
    assert compact["neutron_star_blocker"]
    assert compact["scientific_status"] == "BLOCKED"
    uv = run_uv()
    row = next(item for item in uv["deconstructed_scan"] if item["links"] == 24)
    assert row["quality_pass"]
    assert uv["log10_elementary_c6_bound"] < -70


def test_repo_dependent_evidence_layers():
    kernel = run_kernel(REPO_ROOT)
    assert kernel["coverage_audit"]["requested_exceeds_table"]
    assert all(kernel["gates"].values())
    lpm = run_lpm(REPO_ROOT, full=False)
    assert lpm["all_gates_pass"], lpm
    portable = run_portability(REPO_ROOT, PACKAGE_ROOT)
    assert portable["all_active_portability_gates_pass"], portable
