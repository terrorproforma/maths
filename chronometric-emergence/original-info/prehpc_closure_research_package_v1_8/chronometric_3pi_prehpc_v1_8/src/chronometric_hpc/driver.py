from __future__ import annotations
import argparse
import json
from .preflight import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--results", required=True)
    args = parser.parse_args()
    report = run(args.config, args.results)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["all_pass"] else 2)

if __name__ == "__main__":
    main()
