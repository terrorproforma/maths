from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_ledger(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("diagram ledger must be a list")
    return data


def validate_ledger(path: str | Path) -> dict[str, Any]:
    rows = load_ledger(path)
    ids = [row["id"] for row in rows]
    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1})
    loop_failures = []
    required = {
        "G20_B4_BARE", "G20_B33_MIX", "G20_F3_MIX", "G30_B44_MIX", "G30_B334",
        "G2I_B33", "G2I_F3", "G3I_B44", "G3I_B3333", "G3I_FFFB", "G3I_FFFF",
    }
    for row in rows:
        calculated = int(row["internal_lines"]) - int(row["vertices"]) + 1
        if calculated != int(row["loop_order"]):
            loop_failures.append({"id": row["id"], "declared": row["loop_order"], "calculated": calculated})
    missing = sorted(required.difference(ids))
    return {
        "row_count": len(rows),
        "duplicate_ids": duplicate_ids,
        "loop_failures": loop_failures,
        "missing_required_topologies": missing,
        "all_pass": not duplicate_ids and not loop_failures and not missing,
    }
