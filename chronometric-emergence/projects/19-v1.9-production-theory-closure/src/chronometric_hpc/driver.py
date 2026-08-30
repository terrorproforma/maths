from __future__ import annotations
import argparse
import json
from .preflight import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--results", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    report = run(args.config, args.results)
    text = json.dumps(report, indent=2)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    raise SystemExit(0 if report["all_pass"] else 2)

if __name__ == "__main__":
    main()
