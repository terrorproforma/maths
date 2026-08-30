"""Portability and reproducibility audit."""
from __future__ import annotations

import json
from pathlib import Path


TEXT_SUFFIXES = {
    ".py", ".md", ".tex", ".txt", ".yaml", ".yml", ".json", ".csv", ".toml", ".sh"
}


def scan_tree(root: Path) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if ("/mnt" + "/data") in line:
                matches.append(
                    {
                        "path": str(path.relative_to(root)),
                        "line": line_number,
                        "text": line.strip()[:240],
                    }
                )
    return matches


def run(repo_root: Path, active_root: Path) -> dict:
    repo_root = repo_root.resolve()
    active_root = active_root.resolve()
    active_matches = scan_tree(active_root)
    legacy_root = repo_root / "chronometric-emergence" / "original-info"
    legacy_matches = scan_tree(legacy_root) if legacy_root.exists() else []
    dependency_files = [active_root / "pyproject.toml", active_root / "Makefile"]
    return {
        "evidence_class": "INDEPENDENT_RECOMPUTATION",
        "active_package_absolute_path_matches": active_matches,
        "active_package_match_count": len(active_matches),
        "legacy_archive_absolute_path_match_count": len(legacy_matches),
        "legacy_examples": legacy_matches[:20],
        "dependency_declarations_exist": all(path.exists() for path in dependency_files),
        "scientific_policy": (
            "Legacy artifacts remain immutable historical records and may contain sandbox paths. "
            "The active evidence package must be path-relative and runnable from a clean checkout."
        ),
        "all_active_portability_gates_pass": len(active_matches) == 0
        and all(path.exists() for path in dependency_files),
    }


def write_results(repo_root: Path, active_root: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run(repo_root, active_root)
    (output_dir / "portability_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
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
