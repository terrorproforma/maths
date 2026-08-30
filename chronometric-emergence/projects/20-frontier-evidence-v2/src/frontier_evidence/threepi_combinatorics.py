"""Independent coloured half-edge automorphism audit of the v1.9 3PI ledger."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable

import networkx as nx
from networkx.algorithms.isomorphism import categorical_node_match


@dataclass(frozen=True)
class Vertex:
    name: str
    color: str


@dataclass(frozen=True)
class Propagator:
    name: str
    color: str
    left_vertex: str
    left_halfedge: str
    right_vertex: str
    right_halfedge: str


def incidence_graph(vertices: Iterable[Vertex], propagators: Iterable[Propagator]) -> nx.Graph:
    graph = nx.Graph()
    for vertex in vertices:
        graph.add_node(f"V:{vertex.name}", color=f"vertex:{vertex.color}")
    for prop in propagators:
        pnode = f"P:{prop.name}"
        graph.add_node(pnode, color=f"propagator:{prop.color}")
        for side, vertex_name, halfedge_color in (
            ("L", prop.left_vertex, prop.left_halfedge),
            ("R", prop.right_vertex, prop.right_halfedge),
        ):
            hnode = f"H:{prop.name}:{side}"
            graph.add_node(hnode, color=f"halfedge:{halfedge_color}")
            graph.add_edge(f"V:{vertex_name}", hnode)
            graph.add_edge(hnode, pnode)
    return graph


def automorphism_order(graph: nx.Graph) -> int:
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph, graph, node_match=categorical_node_match("color", None)
    )
    return sum(1 for _ in matcher.isomorphisms_iter())


def bprop(name: str, left: str, right: str) -> Propagator:
    return Propagator(name, "B", left, "B", right, "B")


def fprop(name: str, source: str, target: str) -> Propagator:
    return Propagator(name, "F", source, "Fout", target, "Fin")


def topologies() -> dict[str, tuple[list[Vertex], list[Propagator]]]:
    return {
        "G20_B4_BARE": (
            [Vertex("a", "V4_bare")],
            [bprop("e1", "a", "a"), bprop("e2", "a", "a")],
        ),
        "G20_B33_MIX": (
            [Vertex("a", "V3_dressed"), Vertex("b", "V3_bare")],
            [bprop(f"e{i}", "a", "b") for i in range(3)],
        ),
        "G20_F3_MIX": (
            [Vertex("a", "U_dressed"), Vertex("b", "U_bare")],
            [bprop("boson", "a", "b"), fprop("f1", "a", "b"), fprop("f2", "b", "a")],
        ),
        "G30_B44_MIX": (
            [Vertex("a", "V4_dressed"), Vertex("b", "V4_bare")],
            [bprop(f"e{i}", "a", "b") for i in range(4)],
        ),
        "G30_B334": (
            [Vertex("a", "V3_dressed"), Vertex("b", "V3_dressed"), Vertex("c", "V4_bare")],
            [
                bprop("ab", "a", "b"),
                bprop("ac1", "a", "c"),
                bprop("ac2", "a", "c"),
                bprop("bc1", "b", "c"),
                bprop("bc2", "b", "c"),
            ],
        ),
        "G2I_B33": (
            [Vertex("a", "V3_dressed"), Vertex("b", "V3_dressed")],
            [bprop(f"e{i}", "a", "b") for i in range(3)],
        ),
        "G2I_F3": (
            [Vertex("a", "U_dressed"), Vertex("b", "U_dressed")],
            [bprop("boson", "a", "b"), fprop("f1", "a", "b"), fprop("f2", "b", "a")],
        ),
        "G3I_B44": (
            [Vertex("a", "V4_dressed"), Vertex("b", "V4_dressed")],
            [bprop(f"e{i}", "a", "b") for i in range(4)],
        ),
        "G3I_B3333": (
            [Vertex(name, "V3_dressed") for name in "abcd"],
            [bprop(x + y, x, y) for index, x in enumerate("abcd") for y in "abcd"[index + 1 :]],
        ),
        "G3I_FFFB": (
            [Vertex("x", "V3_dressed")] + [Vertex(name, "U_dressed") for name in "abc"],
            [
                fprop("fab", "a", "b"),
                fprop("fbc", "b", "c"),
                fprop("fca", "c", "a"),
                bprop("ba", "x", "a"),
                bprop("bb", "x", "b"),
                bprop("bc", "x", "c"),
            ],
        ),
        "G3I_FFFF": (
            [Vertex(name, "U_dressed") for name in "abcd"],
            [
                fprop("fab", "a", "b"),
                fprop("fbc", "b", "c"),
                fprop("fcd", "c", "d"),
                fprop("fda", "d", "a"),
                bprop("ac", "a", "c"),
                bprop("bd", "b", "d"),
            ],
        ),
    }


LEDGER_MAGNITUDES = {
    "G20_B4_BARE": 1 / 8,
    "G20_B33_MIX": 1 / 6,
    "G20_F3_MIX": 1.0,
    "G30_B44_MIX": 1 / 24,
    "G30_B334": 1 / 8,
    "G2I_B33": 1 / 12,
    "G2I_F3": 1 / 2,
    "G3I_B44": 1 / 48,
    "G3I_B3333": 1 / 24,
    "G3I_FFFB": 1 / 3,
    "G3I_FFFF": 1 / 4,
}


def run() -> dict:
    rows = []
    for identifier, (vertices, propagators) in topologies().items():
        order = automorphism_order(incidence_graph(vertices, propagators))
        predicted = 1.0 / order
        ledger = LEDGER_MAGNITUDES[identifier]
        rows.append(
            {
                "id": identifier,
                "automorphism_order": order,
                "predicted_coefficient_magnitude": predicted,
                "ledger_coefficient_magnitude": ledger,
                "relative_difference": abs(predicted - ledger) / ledger,
                "magnitude_match": abs(predicted - ledger) < 1.0e-15,
            }
        )
    all_match = all(row["magnitude_match"] for row in rows)
    return {
        "evidence_class": "INDEPENDENT_RECOMPUTATION",
        "method": "coloured half-edge incidence graph automorphisms",
        "rows": rows,
        "all_magnitudes_match": all_match,
        "phase_and_sign_status": (
            "Powers of i and the closed-Grassmann-loop sign are not fixed by automorphism counting; "
            "they remain source-convention checks against the nPI functional."
        ),
    }


def write_results(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result = run()
    (output_dir / "threepi_combinatorics_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    answer = write_results(args.output_dir)
    print(json.dumps(answer, indent=2))
    raise SystemExit(0 if answer["all_magnitudes_match"] else 2)
