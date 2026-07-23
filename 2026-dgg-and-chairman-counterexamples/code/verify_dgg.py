#!/usr/bin/env python3
"""Exact exhaustive verifier for the seven-vertex SSUF counterexample.

No third-party packages are required.  The script enumerates every directed
source-terminal path and all unsplittable routings, recomputes the fractional
arc loads from the stated path decomposition, and checks both cost variants.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

Arc = Tuple[str, str]
Path = Tuple[Arc, ...]


@dataclass(frozen=True)
class Instance:
    source: str
    terminals: Mapping[str, int]
    arcs: Tuple[Arc, ...]
    fractional_load: Mapping[Arc, int]
    unit_cost: Mapping[Arc, int]
    named_paths: Mapping[str, Mapping[str, Path]]
    decomposition: Mapping[str, Mapping[str, int]]


def build_instance(unit_cost: Mapping[Arc, int] | None = None) -> Instance:
    arcs: Tuple[Arc, ...] = (
        ("s", "t1"),
        ("s", "t2"),
        ("s", "u"),
        ("u", "t3"),
        ("u", "v"),
        ("v", "t1"),
        ("v", "w"),
        ("w", "t2"),
        ("w", "t3"),
    )
    x = {
        ("s", "t1"): 10,
        ("s", "t2"): 6,
        ("s", "u"): 24,
        ("u", "t3"): 10,
        ("u", "v"): 14,
        ("v", "t1"): 5,
        ("v", "w"): 9,
        ("w", "t2"): 4,
        ("w", "t3"): 5,
    }
    default_cost = {
        ("s", "t1"): 2,
        ("s", "t2"): 3,
        ("s", "u"): 0,
        ("u", "t3"): 2,
        ("u", "v"): 0,
        ("v", "t1"): 0,
        ("v", "w"): 0,
        ("w", "t2"): 0,
        ("w", "t3"): 0,
    }
    paths = {
        "t1": {
            "E1": (("s", "t1"),),
            "Z1": (("s", "u"), ("u", "v"), ("v", "t1")),
        },
        "t2": {
            "E2": (("s", "t2"),),
            "Z2": (("s", "u"), ("u", "v"), ("v", "w"), ("w", "t2")),
        },
        "t3": {
            "E3": (("s", "u"), ("u", "t3")),
            "Z3": (("s", "u"), ("u", "v"), ("v", "w"), ("w", "t3")),
        },
    }
    decomposition = {
        "t1": {"E1": 10, "Z1": 5},
        "t2": {"E2": 6, "Z2": 4},
        "t3": {"E3": 10, "Z3": 5},
    }
    return Instance(
        source="s",
        terminals={"t1": 15, "t2": 10, "t3": 15},
        arcs=arcs,
        fractional_load=x,
        unit_cost=dict(default_cost if unit_cost is None else unit_cost),
        named_paths=paths,
        decomposition=decomposition,
    )


def enumerate_paths(source: str, target: str, arcs: Iterable[Arc]) -> List[Path]:
    adjacency: Dict[str, List[str]] = defaultdict(list)
    for u, v in arcs:
        adjacency[u].append(v)
    answer: List[Path] = []

    def dfs(node: str, visited: Tuple[str, ...], current: Tuple[Arc, ...]) -> None:
        if node == target:
            answer.append(current)
            return
        for nxt in adjacency[node]:
            if nxt in visited:
                continue
            dfs(nxt, visited + (nxt,), current + ((node, nxt),))

    dfs(source, (source,), tuple())
    return answer


def path_cost(path: Sequence[Arc], unit_cost: Mapping[Arc, int]) -> int:
    return sum(unit_cost[a] for a in path)


def reconstruct_fractional_load(instance: Instance) -> Dict[Arc, int]:
    load = {a: 0 for a in instance.arcs}
    for terminal, pieces in instance.decomposition.items():
        assert sum(pieces.values()) == instance.terminals[terminal]
        for name, amount in pieces.items():
            for arc in instance.named_paths[terminal][name]:
                load[arc] += amount
    return load


def routing_load_and_cost(
    instance: Instance, choices: Mapping[str, str]
) -> Tuple[Dict[Arc, int], int]:
    load = {a: 0 for a in instance.arcs}
    cost = 0
    for terminal, name in choices.items():
        demand = instance.terminals[terminal]
        path = instance.named_paths[terminal][name]
        for arc in path:
            load[arc] += demand
        cost += demand * path_cost(path, instance.unit_cost)
    return load, cost


def verify(instance: Instance, expected_fractional_cost: int, expected_good_optimum: int) -> None:
    D = max(instance.terminals.values())

    # There are exactly two actual graph paths per terminal; this closes the
    # usual omitted-hybrid-path loophole.
    for terminal, named in instance.named_paths.items():
        actual = set(enumerate_paths(instance.source, terminal, instance.arcs))
        stated = set(named.values())
        assert actual == stated, (terminal, actual, stated)

    reconstructed = reconstruct_fractional_load(instance)
    assert reconstructed == dict(instance.fractional_load)

    fractional_cost = sum(
        instance.fractional_load[a] * instance.unit_cost[a] for a in instance.arcs
    )
    assert fractional_cost == expected_fractional_cost

    terminals = ("t1", "t2", "t3")
    option_names = [tuple(instance.named_paths[t].keys()) for t in terminals]
    good_costs: List[int] = []

    print("choices\tcost\tstatus\twitness")
    for options in product(*option_names):
        choices = dict(zip(terminals, options))
        load, cost = routing_load_and_cost(instance, choices)
        violations = [
            (a, load[a] - (instance.fractional_load[a] + D))
            for a in instance.arcs
            if load[a] > instance.fractional_load[a] + D
        ]
        good = not violations
        if good:
            good_costs.append(cost)
        witness = "-" if good else ", ".join(f"{a[0]}->{a[1]}:+{e}" for a, e in violations)
        print("/".join(options), cost, "GOOD" if good else "BAD", witness, sep="\t")

    assert len(good_costs) == 4
    assert min(good_costs) == expected_good_optimum
    assert expected_good_optimum > expected_fractional_cost

    print(f"fractional cost = {fractional_cost}")
    print(f"minimum additive-D-good unsplittable cost = {min(good_costs)}")
    print("certificate verified")


def main() -> None:
    verify(build_instance(), expected_fractional_cost=58, expected_good_optimum=60)

    positive_costs = {
        ("s", "t1"): 12,
        ("s", "t2"): 18,
        ("s", "u"): 1,
        ("u", "t3"): 12,
        ("u", "v"): 1,
        ("v", "t1"): 1,
        ("v", "w"): 1,
        ("w", "t2"): 1,
        ("w", "t3"): 1,
    }
    verify(
        build_instance(positive_costs),
        expected_fractional_cost=409,
        expected_good_optimum=415,
    )


if __name__ == "__main__":
    main()
