"""Portability and reproducibility audit.

The portability gate applies to executable source, tests, build metadata,
configuration and the active GitHub workflow. Historical quotations, errata and
generated forensic reports may legitimately mention the old ChatGPT sandbox
path; those references are reported separately and cannot make a clean checkout
non-portable.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {
    ".py", ".md", ".tex", ".txt", ".yaml", ".yml", ".json", ".csv", ".toml", ".sh"
}
SANDBOX_PATH = "/mnt" + "/data"


def _iter_text_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path
        return
    if not path.exists():
        return
    for candidate in path.rglob("*"):
        if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES:
            yield candidate


def scan_paths(paths: Iterable[Path], relative_to: Path) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    seen: set[Path] = set()
    for root in paths:
        for path in _iter_text_files(root):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for line_number, line in enumerate(text.splitlines(), 1):
                if SANDBOX_PATH in line:
                    try:
                        display_path = path.resolve().relative_to(relative_to.resolve())
                    except ValueError:
                        display_path = path.resolve()
                    matches.append(
                        {
                            "path": str(display_path),
                            "line": line_number,
                            "text": line.strip()[:240],
                        }
                    )
    return matches


def run(repo_root: Path, active_root: Path) -> dict:
    repo_root = repo_root.resolve()
    active_root = active_root.resolve()

    # Only files capable of controlling execution or reproduction are fatal.
    runtime_targets = [
        active_root / "src",
        active_root / "tests",
        active_root / "tools",
        active_root / "config",
        active_root / "scripts",
        active_root / "Makefile",
        active_root / "pyproject.toml",
        repo_root / ".github" / "workflows" / "chronometric-frontier-repair-v2.yml",
    ]
    runtime_matches = scan_paths(runtime_targets, repo_root)

    # These files preserve the audit trail and may quote legacy sandbox links.
    # They are informational, not executable dependencies.
    reference_targets = [
        active_root / "README.md",
        active_root / "ERRATA.md",
        active_root / "AUDIT_RESPONSE.md",
        active_root / "EVIDENCE_POLICY.md",
        active_root / "FRONTIER_GATES.md",
        active_root / "docs",
    ]
    reference_matches = scan_paths(reference_targets, repo_root)

    legacy_root = repo_root / "chronometric-emergence" / "original-info"
    legacy_matches = scan_paths([legacy_root], repo_root) if legacy_root.exists() else []
    dependency_files = [active_root / "pyproject.toml", active_root / "Makefile"]
    dependency_declarations_exist = bool(all(path.exists() for path in dependency_files))

    return {
        "evidence_class": "INDEPENDENT_RECOMPUTATION",
        "runtime_absolute_path_matches": runtime_matches,
        "runtime_absolute_path_match_count": len(runtime_matches),
        # Backward-compatible aliases retained for downstream report readers.
        "active_package_absolute_path_matches": runtime_matches,
        "active_package_match_count": len(runtime_matches),
        "documentation_or_errata_reference_match_count": len(reference_matches),
        "documentation_or_errata_examples": reference_matches[:20],
        "legacy_archive_absolute_path_match_count": len(legacy_matches),
        "legacy_examples": legacy_matches[:20],
        "dependency_declarations_exist": dependency_declarations_exist,
        "scientific_policy": (
            "Legacy artifacts, independent audits and errata remain immutable historical records and may quote "
            "sandbox paths. Executable source, tests, build metadata, configuration and CI must be path-relative "
            "and runnable from a clean checkout."
        ),
        "all_active_portability_gates_pass": bool(
            len(runtime_matches) == 0 and dependency_declarations_exist
        ),
    }


def write_results(repo_root: Path, active_root: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run(repo_root, active_root)
    (output_dir / "portability_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--active-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    result = write_results(args.repo_root, args.active_root, args.output_dir)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["all_active_portability_gates_pass"] else 2)
