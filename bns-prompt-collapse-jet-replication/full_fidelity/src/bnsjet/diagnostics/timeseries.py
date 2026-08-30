"""Strict CSV time-series loading and window statistics."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import numpy.typing as npt


def load_numeric_csv(path: str | Path) -> dict[str, npt.NDArray[np.float64]]:
    """Load a headered CSV whose data columns are all numeric."""

    source = Path(path).expanduser().resolve()
    with source.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {source}")
        columns: dict[str, list[float]] = {name: [] for name in reader.fieldnames}
        for row_number, row in enumerate(reader, start=2):
            for name in reader.fieldnames:
                raw = row.get(name)
                try:
                    value = float(raw) if raw is not None else float("nan")
                except ValueError as exc:
                    raise ValueError(f"Non-numeric value at {source}:{row_number}, column {name}") from exc
                columns[name].append(value)
    return {name: np.asarray(values, dtype=np.float64) for name, values in columns.items()}


def window_summary(
    time: npt.ArrayLike,
    values: npt.ArrayLike,
    start: float,
    stop: float,
) -> dict[str, float]:
    """Return count, mean, standard deviation and quantiles in a time window."""

    times = np.asarray(time, dtype=np.float64)
    samples = np.asarray(values, dtype=np.float64)
    if times.shape != samples.shape:
        raise ValueError("time and values must have the same shape")
    selected = (times >= start) & (times <= stop) & np.isfinite(samples)
    window = samples[selected]
    if window.size == 0:
        raise ValueError("Requested window contains no finite samples")
    return {
        "count": float(window.size),
        "mean": float(np.mean(window)),
        "std": float(np.std(window)),
        "q05": float(np.quantile(window, 0.05)),
        "q50": float(np.quantile(window, 0.50)),
        "q95": float(np.quantile(window, 0.95)),
    }
