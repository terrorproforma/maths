#!/usr/bin/env python3
"""Generate deterministic summary figures for TP-01 v1.1."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def add_box(ax, x, y, w, h, text, fontsize=9, linewidth=1.2):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.015,rounding_size=0.015",
        facecolor="white", edgecolor="black", linewidth=linewidth,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)
    return box


def arrow(ax, start, end, text=None, fontsize=8, linestyle="-"):
    arr = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12,
                          linewidth=1.1, linestyle=linestyle, color="black")
    ax.add_patch(arr)
    if text:
        mx = (start[0] + end[0]) / 2
        my = (start[1] + end[1]) / 2
        ax.text(mx, my + 0.025, text, ha="center", va="bottom", fontsize=fontsize)


def make_descent_map(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(11.8, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(ax, 0.035, 0.72, 0.22, 0.15,
            "6D relative Chern-Weil\n$\\int P_3(\\mathcal{F}^3)$", fontsize=10)
    add_box(ax, 0.345, 0.72, 0.22, 0.15,
            "5D transgression\n$T_5(A,\\bar{A})$", fontsize=10)
    add_box(ax, 0.655, 0.72, 0.22, 0.15,
            "5D AdS CS gravity\n$\\bar{A}=0$", fontsize=10)
    arrow(ax, (0.255, 0.795), (0.345, 0.795), "exact")
    arrow(ax, (0.565, 0.795), (0.655, 0.795), "exact")

    add_box(ax, 0.19, 0.41, 0.22, 0.15,
            "4D full zero-mode action\n$\\int\\langle\\phi F\\wedge F\\rangle$", fontsize=9.5)
    add_box(ax, 0.49, 0.41, 0.20, 0.15,
            "Fixed holonomy /\ncompensator sector", fontsize=9.5)
    add_box(ax, 0.78, 0.41, 0.19, 0.15,
            "MacDowell-Mansouri\n$\\to$ EC+$\\Lambda$+Euler", fontsize=9.5)
    arrow(ax, (0.455, 0.72), (0.30, 0.56), "exact")
    arrow(ax, (0.41, 0.485), (0.49, 0.485), "restrict")
    arrow(ax, (0.69, 0.485), (0.78, 0.485), "exact")

    add_box(ax, 0.16, 0.09, 0.25, 0.17,
            "Vary all zero modes\nextra $F\\wedge F=0$ equation\n13 local modes", fontsize=9.3)
    add_box(ax, 0.49, 0.09, 0.20, 0.17,
            "Correct local\nsymplectic pullback", fontsize=9.3)
    add_box(ax, 0.78, 0.09, 0.19, 0.17,
            "NOT a dynamical /\nBRST reduction", fontsize=9.3)
    arrow(ax, (0.30, 0.41), (0.285, 0.26), "vary")
    arrow(ax, (0.59, 0.41), (0.59, 0.26), "pullback")
    arrow(ax, (0.69, 0.175), (0.78, 0.175), "not invariant")

    ax.text(0.5, 0.965,
            "TP-01 v1.1: exact action genealogy survives; spectrum-preserving reduction does not",
            ha="center", va="top", fontsize=14)
    fig.savefig(out / "descent_obstruction_map.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def make_orbit_summary(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    add_box(ax, 0.05, 0.66, 0.26, 0.18,
            "$\\mathfrak{so}(4,2)$ adjoint\n15 dimensions", fontsize=11)
    add_box(ax, 0.42, 0.70, 0.23, 0.14,
            "orbit of $J_{54}$\n8 directions", fontsize=10)
    add_box(ax, 0.72, 0.70, 0.23, 0.14,
            "centralizer\n7 directions", fontsize=10)
    arrow(ax, (0.31, 0.75), (0.42, 0.77))
    arrow(ax, (0.31, 0.75), (0.72, 0.77))

    add_box(ax, 0.05, 0.27, 0.26, 0.18,
            "$SO(3,2)$ vector ansatz\n5 components", fontsize=11)
    add_box(ax, 0.42, 0.31, 0.23, 0.14,
            "orientation orbit\n4 directions", fontsize=10)
    add_box(ax, 0.72, 0.31, 0.23, 0.14,
            "norm / conjugacy datum\n1 physical direction", fontsize=10)
    arrow(ax, (0.31, 0.36), (0.42, 0.38))
    arrow(ax, (0.31, 0.36), (0.72, 0.38))

    ax.text(0.5, 0.94, "Gauge orbit versus physical holonomy data", ha="center", va="top", fontsize=14)
    ax.text(0.5, 0.08,
            "$\\mathrm{tr}_{\\mathbf{6}} W=4+2\\cosh(L_y v)$ is conjugacy invariant: changing $v$ changes the sector.",
            ha="center", va="center", fontsize=10)

    fig.tight_layout()
    fig.savefig(out / "holonomy_orbit_summary.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    out = args.root.resolve() / "figures"
    out.mkdir(parents=True, exist_ok=True)
    make_descent_map(out)
    make_orbit_summary(out)


if __name__ == "__main__":
    main()
