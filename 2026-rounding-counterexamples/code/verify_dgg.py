#!/usr/bin/env python3
"""Exact exhaustive verifier for the seven-vertex SSUF counterexample.

The program intentionally uses only the Python standard library and integer
arithmetic.  It reconstructs all source-terminal paths from the arc list,
enumerates every unsplittable routing, and checks the claimed optimum.
"""

from __future__ import annotations

import itertools
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Arc = Tuple[str, str]
PathType = Tuple[Arc, ...]

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "dgg_instance.json"


def all_simple_paths(
    adjacency: Dict[str, List[str]], source: str, target: str
) -> List[Tuple[str, ...]]:
    result: List[Tuple[str, ...]] = []

    def visit(vertex: str, prefix: Tuple[str, ...]) -> None:
        if vertex == target:
            result.append(prefix)
            return
        for successor in adjacency.get(vertex, []):
            if successor not in prefix:
                visit(successor, prefix + (successor,))

    visit(source, (source,))
    return result


def path_arcs(path: Sequence[str]) -> PathType:
    return tuple(zip(path, path[1:]))


def main() -> None:
    instance = json.loads(DATA.read_text(encoding="utf-8"))
    source = instance["source"]
    demands = {t: int(d) for t, d in instance["terminals"].items()}
    maximum_demand = max(demands.values())
    assert maximum_demand == int(instance["maximum_demand"])

    arcs: List[Arc] = []
    fractional_load: Dict[Arc, int] = {}
    cost: Dict[Arc, int] = {}
    adjacency: Dict[str, List[str]] = defaultdict(list)

    for record in instance["arcs"]:
        arc = (record["tail"], record["head"])
        assert arc not in fractional_load, f"duplicate arc {arc}"
        arcs.append(arc)
        fractional_load[arc] = int(record["fractional_load"])
        cost[arc] = int(record["cost"])
        adjacency[arc[0]].append(arc[1])

    # Verify aggregate fractional-flow conservation.
    balance = {v: 0 for v in instance["vertices"]}
    for arc in arcs:
        u, v = arc
        balance[u] -= fractional_load[arc]
        balance[v] += fractional_load[arc]
    assert balance[source] == -sum(demands.values())
    for terminal, demand in demands.items():
        assert balance[terminal] == demand
    for vertex in set(instance["vertices"]) - {source, *demands.keys()}:
        assert balance[vertex] == 0

    # Reconstruct every path from the graph, rather than trusting the supplied
    # path decomposition.
    paths: Dict[str, List[PathType]] = {}
    for terminal in demands:
        vertex_paths = all_simple_paths(adjacency, source, terminal)
        paths[terminal] = [path_arcs(path) for path in vertex_paths]
        assert len(paths[terminal]) == 2, (
            terminal,
            [tuple([source] + [v for _, v in p]) for p in paths[terminal]],
        )

    fractional_cost = sum(fractional_load[a] * cost[a] for a in arcs)
    assert fractional_cost == int(instance["claimed_fractional_cost"]) == 58

    terminals = tuple(demands)
    routing_records = []
    for choices in itertools.product(*(paths[t] for t in terminals)):
        load = {a: 0 for a in arcs}
        total_cost = 0
        selected = []
        for terminal, path in zip(terminals, choices):
            demand = demands[terminal]
            per_unit = sum(cost[a] for a in path)
            total_cost += demand * per_unit
            selected.append("Z" if per_unit == 0 else "E")
            for arc in path:
                load[arc] += demand

        violations = {
            a: load[a] - (fractional_load[a] + maximum_demand)
            for a in arcs
            if load[a] > fractional_load[a] + maximum_demand
        }
        routing_records.append(
            {
                "selected": "".join(selected),
                "cost": total_cost,
                "good": not violations,
                "violations": violations,
            }
        )

    assert len(routing_records) == 8
    good = [record for record in routing_records if record["good"]]
    bad = [record for record in routing_records if not record["good"]]
    assert len(good) == 4
    assert len(bad) == 4
    minimum_good_cost = min(record["cost"] for record in good)
    assert minimum_good_cost == int(
        instance["claimed_minimum_cost_subject_to_additive_bound"]
    ) == 60
    assert minimum_good_cost > fractional_cost

    # Every routing with two cheap paths has the advertised unit excess on a
    # bottleneck arc.  The all-cheap routing may violate several arcs.
    required_witnesses = {
        "ZZE": ("s", "u"),
        "ZEZ": ("u", "v"),
        "EZZ": ("v", "w"),
    }
    by_selection = {record["selected"]: record for record in routing_records}
    for selection, witness in required_witnesses.items():
        assert by_selection[selection]["violations"][witness] == 1

    print("All source-terminal paths reconstructed from the graph:")
    for terminal in terminals:
        rendered = ["->".join([source] + [v for _, v in path]) for path in paths[terminal]]
        print(f"  {terminal}: {rendered}")
    print("\nAll eight routings:")
    for record in sorted(routing_records, key=lambda r: r["selected"]):
        witness = ", ".join(
            f"{u}->{v}:+{excess}" for (u, v), excess in record["violations"].items()
        ) or "none"
        print(
            f"  {record['selected']}  cost={record['cost']:>2}  "
            f"good={str(record['good']):<5}  violations={witness}"
        )
    print(
        "\nDGG certificate verified: min good cost = "
        f"{minimum_good_cost} > fractional cost = {fractional_cost}"
    )


if __name__ == "__main__":
    main()
