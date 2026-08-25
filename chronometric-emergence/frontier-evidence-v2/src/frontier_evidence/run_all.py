"""Run the complete adversarial evidence repair suite."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from . import compact_objects, formal_core, kernel_uncertainty, lpm_repair
from . import nu0_fate, portability, qcd_threshold, rg_audit
from . import scalar_two_time, threepi_combinatorics, uv_quality


def _write_claim_matrix(path: Path) -> None:
    rows = [
        {"claim":"universal clock factorisation theorem","current_status":"RETAINED","evidence_class":"IDENTITY_PIN","frontier_effect":"formal core survives; novelty review open"},
        {"claim":"rank-r clock network identifies r fields","current_status":"CORRECTED","evidence_class":"IDENTITY_PIN","frontier_effect":"requires full-rank sensitivities and independent excitations"},
        {"claim":"2/27 exact transmission","current_status":"LEADING_ORDER_ONLY","evidence_class":"IDENTITY_PIN+EXTERNAL_BENCHMARK","frontier_effect":"NLO few-percent band required"},
        {"claim":"v1.3 RG completion","current_status":"RETRACTED","evidence_class":"IDENTITY_PIN","frontier_effect":"hard matching at natural scale retained; RG closure open"},
        {"claim":"v1.4 transport table","current_status":"DEPRECATED","evidence_class":"INDEPENDENT_RECOMPUTATION","frontier_effect":"corrected diagnostic generated; v1.5 is anchor"},
        {"claim":"v1.5 LPM portal anchor","current_status":"RETAINED_WITH_SCOPE","evidence_class":"CONVERGENCE+EXTERNAL_BENCHMARK","frontier_effect":"collinear sector only; hard cuts remain"},
        {"claim":"v1.7-v1.8 arbitrary off-shell kernel","current_status":"MODEL_FAMILY_ONLY","evidence_class":"MODEL_DISCREPANCY","frontier_effect":"no pointwise physical error bar claimed"},
        {"claim":"v1.9 pilot ready","current_status":"RETRACTED","evidence_class":"SOURCE_AUDIT","frontier_effect":"specification only; no 3PI solver"},
        {"claim":"prompt daughter harmless","current_status":"REPAIRED_CONDITIONALLY","evidence_class":"RATE_CALCULATION+PREDICTION","frontier_effect":"gauge-charged daughter thermalises; model representation changed"},
        {"claim":"low-f_a ridge environmentally safe","current_status":"BLOCKED","evidence_class":"PREDICTION","frontier_effect":"neutron-star conversion condition is met"},
        {"claim":"elementary global Z6 field has adequate UV quality","current_status":"RETRACTED","evidence_class":"PREDICTION","frontier_effect":"24-link local gauge completion is a conditional repair"},
        {"claim":"real-time infrastructure exists","current_status":"UNIT_TIER_EARNED","evidence_class":"INDEPENDENT_RECOMPUTATION+CONVERGENCE","frontier_effect":"scalar two-time gate passes; non-Abelian 3PI remains unimplemented"},
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _render_report(results: dict[str, Any]) -> str:
    scalar = results["scalar_two_time"]
    lpm = results["lpm_repair"]
    compact = results["compact_objects"]
    kernel = results["kernel_uncertainty"]
    nu = results["nu0_fate"]
    uv = results["uv_quality"]
    threepi = results["threepi_combinatorics"]
    qcd = results["qcd_threshold"]
    lines = [
        "# Frontier evidence report v2",
        "",
        "**Author: Angus Muffatti**",
        "",
        "## Executive result",
        "",
        "The repair suite earns a defensible **evidence frontier** for the narrow formal core, the leading QCD-threshold interpretation, the corrected LPM evidence layer, exact 3PI combinatorial magnitudes, and a real scalar unequal-time unit tier.",
        "",
        "It does **not** authorize the full non-Abelian pilot or establish a viable cosmological completion. Neutron-star conversion and the absence of a working 3PI evolution engine remain load-bearing blockers.",
        "",
        "## Results",
        "",
        f"- Scalar unequal-time gates: **{sum(scalar['gates'].values())}/{len(scalar['gates'])}**; all pass = `{scalar['all_gates_pass']}`.",
        f"- 3PI coefficient magnitudes: **{len(threepi['rows'])}/11** checked; all match = `{threepi['all_magnitudes_match']}`.",
        f"- v1.3 RG closure: **{results['rg_audit']['scientific_verdict']}**.",
        f"- Corrected LPM evidence gates: **{sum(lpm['gates'].values())}/{len(lpm['gates'])}**; all pass = `{lpm['all_gates_pass']}`.",
        f"- v1.5 recomputed portal occupation width: `{lpm['v15_recomputation']['Gamma_H_occupation_over_T']:.6g} T`.",
        f"- Leading QCD coefficient: `{qcd['one_loop_exact']:.9g}`; conventional NLO estimate: `{qcd['conventional_NLO_estimate']:.9g}`.",
        f"- Sterile prompt-daughter Delta N_eff: `{nu['sterile_cascade']['DeltaNeff_total']:.4g}`; repaired Delta N_eff: `{nu['repaired_cascade']['DeltaNeff_total']:.4g}`.",
        f"- Neutron-star blocker: `{compact['neutron_star_blocker']}`.",
        f"- UV-quality status: `{uv['status']}`.",
        f"- v1.7/v1.8 far-off-shell p95 model discrepancy: `{kernel['relative_model_discrepancy']['far_off_shell']['p95']}`.",
        "",
        "## Evidence boundary",
        "",
        "The scalar unit tier is a genuine calculation, but it is an exactly specified open scalar system rather than the desired gauge plasma. The 3PI graph audit independently validates coefficient magnitudes, not Minkowski phases or the correctness of a future discretised functional derivative. The LPM run validates the collinear layer, not the missing hard cuts.",
        "",
        "## Frontier decision",
        "",
        "| Frontier | Decision |",
        "|---|---|",
        "| Formal chronometric-shear programme | **CONDITIONALLY EARNED** |",
        "| Leading threshold phenomenology | **EARNED AT ONE LOOP; NLO BAND ADDED** |",
        "| Scalar real-time software unit tier | **EARNED** |",
        "| Full q-D-H hard+LPM thermal correlator | **NOT YET** |",
        "| PT/BFM three-loop 3PI pilot | **NOT AUTHORIZED** |",
        "| Cosmological realization | **BLOCKED BY COMPACT OBJECTS** |",
        "| UV completion | **CONDITIONAL 24-LINK SKELETON** |",
        "",
        "The correct next frontier calculation is therefore a real, source-generated scalar/Yukawa 2PI evolution followed by the hard-cut completion—not an eight-GPU run of a nonexistent solver.",
        "",
    ]
    return "\n".join(lines)


def run_all(repo_root: Path, package_root: Path, full_lpm: bool = True) -> dict[str, Any]:
    output_dir = package_root / "results"
    docs_dir = package_root / "docs"
    output_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, Any] = {}
    results["formal_core"] = formal_core.write_results(output_dir)
    results["qcd_threshold"] = qcd_threshold.write_results(output_dir)
    results["rg_audit"] = rg_audit.write_results(output_dir)
    results["scalar_two_time"] = scalar_two_time.write_results(output_dir)
    results["threepi_combinatorics"] = threepi_combinatorics.write_results(output_dir)
    results["nu0_fate"] = nu0_fate.write_results(output_dir)
    results["compact_objects"] = compact_objects.write_results(output_dir)
    results["uv_quality"] = uv_quality.write_results(output_dir)
    results["lpm_repair"] = lpm_repair.write_results(repo_root, output_dir, full=full_lpm)
    results["kernel_uncertainty"] = kernel_uncertainty.write_results(repo_root, output_dir)
    results["portability"] = portability.write_results(repo_root, package_root, output_dir)

    software_gates = {
        "scalar_two_time": results["scalar_two_time"]["all_gates_pass"],
        "threepi_magnitudes": results["threepi_combinatorics"]["all_magnitudes_match"],
        "nu0_repair": results["nu0_fate"]["all_repair_gates_pass"],
        "lpm_repair": results["lpm_repair"]["all_gates_pass"],
        "portability": results["portability"]["all_active_portability_gates_pass"],
        "kernel_audit": all(results["kernel_uncertainty"]["gates"].values()),
    }
    results["frontier_status"] = {
        "software_evidence_gates": software_gates,
        "all_software_evidence_gates_pass": bool(all(software_gates.values())),
        "formal_frontier": "CONDITIONAL_EARNED",
        "scalar_unit_frontier": "EARNED",
        "nonabelian_3pi_frontier": "NOT_AUTHORIZED",
        "cosmology_frontier": "BLOCKED",
        "publication_frontier": "NARROW_NOTE_ONLY_AFTER_SPECIALIST_REVIEW",
    }

    (output_dir / "frontier_status.json").write_text(json.dumps(results["frontier_status"], indent=2) + "\n", encoding="utf-8")
    _write_claim_matrix(output_dir / "claim_matrix_v2.csv")
    (docs_dir / "FRONTIER_EVIDENCE_REPORT.md").write_text(_render_report(results), encoding="utf-8")
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--package-root", type=Path)
    parser.add_argument("--fast-lpm", action="store_true")
    args = parser.parse_args()
    package_root = args.package_root or Path(__file__).resolve().parents[2]
    results = run_all(args.repo_root.resolve(), package_root.resolve(), full_lpm=not args.fast_lpm)
    print(json.dumps(results["frontier_status"], indent=2))
    raise SystemExit(0 if results["frontier_status"]["all_software_evidence_gates_pass"] else 2)


if __name__ == "__main__":
    main()
