#!/usr/bin/env python3
"""Render a deterministic density/magnetisation slice from a contract HDF5 snapshot."""

from __future__ import annotations

import argparse
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np

from bnsjet.field_contract import validate_field_snapshot


def central_index(coordinates: np.ndarray) -> int:
    return int(np.argmin(np.abs(coordinates)))


def robust_limits(values: np.ndarray, low: float, high: float) -> tuple[float, float]:
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        raise ValueError("Cannot determine limits from an empty/non-finite field")
    lower, upper = np.quantile(finite, [low, high])
    if not upper > lower:
        upper = lower + max(abs(lower), 1.0) * 1.0e-12
    return float(lower), float(upper)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--plane", choices=("xz", "yz", "xy"), default="xz")
    parser.add_argument("--dpi", type=int, default=180)
    arguments = parser.parse_args()

    validate_field_snapshot(arguments.snapshot)
    with h5py.File(arguments.snapshot, "r") as handle:
        x = np.asarray(handle["/coordinates/x"], dtype=float)
        y = np.asarray(handle["/coordinates/y"], dtype=float)
        z = np.asarray(handle["/coordinates/z"], dtype=float)
        rho = np.asarray(handle["/fields/rho"], dtype=float)
        b_squared = np.asarray(handle["/fields/b_squared"], dtype=float)
        time_s = float(np.asarray(handle["/meta/time_s"]))

    sigma = b_squared / np.maximum(rho, np.finfo(float).tiny)
    if arguments.plane == "xz":
        index = central_index(y)
        density_slice = rho[:, index, :].T
        sigma_slice = sigma[:, index, :].T
        horizontal, vertical = x, z
        labels = ("x", "z")
    elif arguments.plane == "yz":
        index = central_index(x)
        density_slice = rho[index, :, :].T
        sigma_slice = sigma[index, :, :].T
        horizontal, vertical = y, z
        labels = ("y", "z")
    else:
        index = central_index(z)
        density_slice = rho[:, :, index].T
        sigma_slice = sigma[:, :, index].T
        horizontal, vertical = x, y
        labels = ("x", "y")

    log_density = np.log10(np.maximum(density_slice, np.finfo(float).tiny))
    density_low, density_high = robust_limits(log_density, 0.01, 0.995)
    sigma_low, sigma_high = robust_limits(np.log10(np.maximum(sigma_slice, 1.0e-20)), 0.5, 0.995)

    figure, axis = plt.subplots(figsize=(8, 8), constrained_layout=True)
    extent = [horizontal.min(), horizontal.max(), vertical.min(), vertical.max()]
    image = axis.imshow(
        log_density,
        origin="lower",
        extent=extent,
        vmin=density_low,
        vmax=density_high,
        interpolation="bilinear",
        aspect="equal",
    )
    magnetised = np.ma.masked_less_equal(np.log10(np.maximum(sigma_slice, 1.0e-20)), sigma_low)
    axis.contour(
        horizontal,
        vertical,
        magnetised,
        levels=np.linspace(sigma_low, sigma_high, 6),
        linewidths=0.6,
    )
    axis.set_xlabel(labels[0])
    axis.set_ylabel(labels[1])
    axis.set_title(f"t - t_merger = {time_s * 1.0e3:.2f} ms")
    colorbar = figure.colorbar(image, ax=axis)
    colorbar.set_label("log10(rest-mass density)")

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(arguments.output, dpi=arguments.dpi)
    plt.close(figure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
