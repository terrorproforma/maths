from __future__ import annotations
import numpy as np


def scalar_transverse_basis(p: np.ndarray, q: np.ndarray, u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    q2 = float(np.dot(q, q))
    t1 = q2*p - float(np.dot(p, q))*q
    t2 = q2*u - float(np.dot(u, q))*q
    n1 = max(float(np.dot(t1, t1)), 1.0e-30)
    t2 = t2 - float(np.dot(t2, t1))/n1*t1
    return t1, t2


def solve_separable_form_factors(kernel: np.ndarray, source: np.ndarray) -> np.ndarray:
    if kernel.shape[0] != kernel.shape[1] or kernel.shape[0] != source.shape[0]:
        raise ValueError("incompatible separable BSE dimensions")
    return np.linalg.solve(np.eye(kernel.shape[0])-kernel, source)


def sti_residual(q: np.ndarray, vertex: list[np.ndarray], rhs: np.ndarray) -> float:
    lhs = sum(q[mu]*vertex[mu] for mu in range(4))
    return float(np.linalg.norm(lhs-rhs)/max(np.linalg.norm(rhs), 1.0e-30))
