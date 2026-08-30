from __future__ import annotations
import numpy as np


def separable_ladder(chi0: np.ndarray, kernel: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Solve chi=chi0/(1-K chi0) and return chi, vertex, equation residual."""
    if kernel.ndim == 1:
        kernel = kernel[:, None]
    vertex = 1.0/(1.0-kernel*chi0)
    chi = chi0*vertex
    residual = vertex-1.0-kernel*chi0*vertex
    return chi, vertex, float(np.max(np.abs(residual)))
