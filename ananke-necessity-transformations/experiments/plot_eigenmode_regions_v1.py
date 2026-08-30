"""Plot the noisy eigenvalue disk against selected Karpelevič boundaries."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ananke import boundary_points


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "results" / "noisy_qubit_v1.json"
OUTPUT_PATH = ROOT / "results" / "eigenmode_regions_v1.png"


def main() -> None:
    result = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    eigenmode = result["x_eigenmode_bootstrap"]
    centre = complex(*eigenmode["point_estimate"])
    radius = float(eigenmode["confidence_disk_radius"])
    exact = complex(*result["exact_reference"]["x_mode"])

    figure, axis = plt.subplots(figsize=(8, 7))
    angles = np.linspace(0.0, 2.0 * np.pi, 1_440, endpoint=True)
    for order in (8, 15, 16):
        points = boundary_points(order, angles)
        axis.plot(points.real, points.imag, label=fr"$\Theta_{{{order}}}$")

    disk_angles = np.linspace(0.0, 2.0 * np.pi, 720)
    disk = centre + radius * np.exp(1j * disk_angles)
    disk_line = axis.plot(
        disk.real,
        disk.imag,
        linewidth=2.0,
        label="99% bootstrap disk",
    )[0]
    axis.fill(disk.real, disk.imag, alpha=0.12, color=disk_line.get_color())
    axis.scatter(
        [centre.real],
        [centre.imag],
        marker="x",
        s=80,
        label="Extracted mode",
    )
    axis.scatter(
        [exact.real],
        [exact.imag],
        marker="+",
        s=100,
        label="Exact reference",
    )

    axis.set_aspect("equal", adjustable="box")
    axis.set_xlim(0.70, 0.79)
    axis.set_ylim(0.62, 0.71)
    axis.set_xlabel("Real part")
    axis.set_ylabel("Imaginary part")
    axis.set_title("ANANKE v1: invariant mode versus finite stochastic regions")
    axis.grid(True, alpha=0.25)
    axis.legend(loc="best")
    figure.tight_layout()
    figure.savefig(OUTPUT_PATH, dpi=180)
    plt.close(figure)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
