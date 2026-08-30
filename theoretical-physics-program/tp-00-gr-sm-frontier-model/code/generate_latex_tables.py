#!/usr/bin/env python3
"""Generate all paper tables and the seam equation appendix from machine-readable ledgers.

The generated TeX files are deterministic. They contain no hand-entered physics values;
all content is read from CSV/YAML inputs in the package root.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import yaml


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def latex_escape(value: object) -> str:
    mapping = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(mapping.get(character, character) for character in str(value))


def verified_domains_table(rows: list[dict[str, str]]) -> str:
    lines = [
        r"\begingroup\small",
        r"\setlength\LTleft{0pt}\setlength\LTright{0pt}",
        r"\begin{longtable}{@{}p{0.75cm}p{2.35cm}p{2.55cm}p{7.35cm}@{}}",
        r"\caption{Representative verified and parametrized domains.}\label{tab:verified}\\",
        r"\toprule ID & Domain & Status & Result and caveat\\\midrule\endfirsthead",
        r"\toprule ID & Domain & Status & Result and caveat\\\midrule\endhead",
    ]
    for row in rows:
        text = row["result"].rstrip(".") + ". " + row["caveat"]
        lines.append(
            f"{latex_escape(row['domain_id'])} & {latex_escape(row['domain'])} & "
            f"{latex_escape(row['status'])} & {latex_escape(text)} " + r"\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\endgroup"])
    return "\n".join(lines) + "\n"


def seam_summary_table(rows: list[dict[str, str]]) -> str:
    lines = [
        r"\begingroup\small",
        r"\setlength\LTleft{0pt}\setlength\LTright{0pt}",
        r"\begin{longtable}{@{}p{0.7cm}p{2.35cm}p{2.55cm}p{7.4cm}@{}}",
        r"\caption{Seam ledger summary. The exact equation, all seven taxonomy flags, sources and resolution criteria are preserved in \texttt{seam\_ledger.csv}; Appendix~\ref{app:seam-equations} reproduces the equation index.}\label{tab:seams}\\",
        r"\toprule ID & Seam & Primary class & Established status and evidentiary boundary\\\midrule\endfirsthead",
        r"\toprule ID & Seam & Primary class & Established status and evidentiary boundary\\\midrule\endhead",
    ]
    for row in rows:
        text = row["established_status"].rstrip(".") + ". " + row["not_a_claim"]
        lines.append(
            f"{latex_escape(row['seam_id'])} & {latex_escape(row['seam'])} & "
            f"{latex_escape(row['primary_class'])} & {latex_escape(text)} " + r"\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\endgroup"])
    return "\n".join(lines) + "\n"


def successor_gates_table(rows: list[dict[str, str]]) -> str:
    lines = [
        r"\begingroup\scriptsize",
        r"\setlength\LTleft{0pt}\setlength\LTright{0pt}",
        r"\begin{longtable}{@{}p{0.9cm}p{1.25cm}p{3.15cm}p{7.7cm}@{}}",
        r"\caption{Operational successor gates. Applicability and model-class dependence are retained in the YAML/CSV records.}\label{tab:gates}\\",
        r"\toprule ID & Tier & Requirement & Pass condition\\\midrule\endfirsthead",
        r"\toprule ID & Tier & Requirement & Pass condition\\\midrule\endhead",
    ]
    for row in rows:
        lines.append(
            f"{latex_escape(row['test_id'])} & {latex_escape(row['tier'])} & "
            f"{latex_escape(row['requirement'])} & {latex_escape(row['pass_condition'])} " + r"\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\endgroup"])
    return "\n".join(lines) + "\n"


def seam_equation_index(rows: list[dict[str, str]]) -> str:
    lines = [
        r"\section{Equation index for every seam}\label{app:seam-equations}",
        r"This appendix is generated from the same rows as \texttt{seam\_ledger.csv}. The CSV remains authoritative for taxonomy flags, source keys, resolution evidence and successor obligations.",
    ]
    for row in rows:
        equation = row["structural_equation"].replace(r";\quad", r";\allowbreak\quad")
        lines.extend(
            [
                rf"\subsection*{{{latex_escape(row['seam_id'])}: {latex_escape(row['seam'])}}}",
                r"\begingroup\small",
                r"\begin{equation*}",
                equation,
                r"\end{equation*}",
                r"\endgroup",
                latex_escape(row["established_status"]),
            ]
        )
    return "\n".join(lines) + "\n"


def main(root: Path) -> None:
    output = root / "tables"
    output.mkdir(parents=True, exist_ok=True)

    verified = read_csv(root / "verified_domains.csv")
    seams = read_csv(root / "seam_ledger.csv")
    recovery = read_csv(root / "recovery_requirements.csv")

    # Parse YAML as an additional syntax/provenance check. CSV and YAML gate IDs must agree.
    with (root / "successor_acceptance_tests.yaml").open(encoding="utf-8") as handle:
        yaml_ids = [gate["id"] for gate in yaml.safe_load(handle)["gates"]]
    csv_ids = [row["test_id"] for row in recovery]
    if yaml_ids != csv_ids:
        raise ValueError("Gate order/IDs differ between YAML and recovery_requirements.csv")

    files = {
        "verified_domains_table.tex": verified_domains_table(verified),
        "seam_summary_table.tex": seam_summary_table(seams),
        "successor_gates_table.tex": successor_gates_table(recovery),
        "seam_equation_index.tex": seam_equation_index(seams),
    }
    for name, content in files.items():
        (output / name).write_text(content, encoding="utf-8")
    print(f"generated {len(files)} deterministic LaTeX table/appendix files")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    arguments = parser.parse_args()
    main(Path(arguments.root).resolve())
