#!/usr/bin/env python3
"""Final package validation for TP-01 v1.1."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

REQUIRED = [
    "README.md",
    "CITATION.cff",
    "TP-01_Dirac_BRST_Global_Audit_v1.1.pdf",
    "paper/tp01_dirac_brst_global_audit_v1_1.tex",
    "acceptance_matrix.csv",
    "claim_novelty_acceptance_matrix.csv",
    "dirac_brst_analysis.md",
    "kk_brst_closure.md",
    "global_bundle_large_gauge_audit.md",
    "strengthened_no_go_theorem.md",
    "source_and_notation_ledger.md",
    "bibliography/references.bib",
    "code/verify_dirac_brst_global_v1_1.py",
    "code/generate_summary_figures.py",
    "code/tests/test_verification.py",
    "results/verification_results.json",
    "results/terminal_verdict.json",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    missing = [item for item in REQUIRED if not (root / item).is_file()]

    data = json.loads((root / "results/verification_results.json").read_text(encoding="utf-8"))
    checks = {
        "required_files_present": not missing,
        "verification_all_pass": bool(data.get("all_pass")),
        "paper_pdf_nonempty": (root / "TP-01_Dirac_BRST_Global_Audit_v1.1.pdf").stat().st_size > 100_000,
        "paper_has_20_pages": False,
        "unit_tests_pass": False,
    }

    try:
        result = subprocess.run(
            ["pdfinfo", str(root / "TP-01_Dirac_BRST_Global_Audit_v1.1.pdf")],
            check=True, capture_output=True, text=True,
        )
        checks["paper_has_20_pages"] = "Pages:           20" in result.stdout
    except Exception:
        checks["paper_has_20_pages"] = False

    try:
        subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", "code/tests", "-v"],
            cwd=root, check=True, capture_output=True, text=True,
        )
        checks["unit_tests_pass"] = True
    except Exception:
        checks["unit_tests_pass"] = False

    output = {
        "project": "TP-01 v1.1",
        "all_pass": all(checks.values()),
        "checks": checks,
        "missing": missing,
        "scope_warning": "Validation confirms package integrity and reported calculations; it does not turn the rejected strong parent into an accepted theory."
    }
    (root / "results/final_validation.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    lines = ["# Final validation", "", f"Overall: **{'PASS' if output['all_pass'] else 'FAIL'}**", ""]
    for key, value in checks.items():
        lines.append(f"- `{key}`: **{'PASS' if value else 'FAIL'}**")
    if missing:
        lines.extend(["", "Missing:", *[f"- `{item}`" for item in missing]])
    lines.extend(["", output["scope_warning"]])
    (root / "results/final_validation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    if not output["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
