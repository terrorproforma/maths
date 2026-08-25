from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from scipy.interpolate import RegularGridInterpolator

@dataclass
class MatchedKernel:
    k: np.ndarray
    omega: np.ndarray
    im_pi: np.ndarray
    re_pi: np.ndarray
    noise: np.ndarray
    qstar: np.ndarray
    by_qstar: np.ndarray

    @classmethod
    def load(cls, path: str | Path) -> "MatchedKernel":
        raw = np.load(path)
        return cls(
            k=raw["match_k_over_T"],
            omega=raw["match_omega_over_T"],
            im_pi=raw["match_ImPi_total_over_T2"],
            re_pi=raw["match_RePi_total_over_T2"],
            noise=raw["match_KMS_noise_over_T2"],
            qstar=raw["match_qstar_over_T"],
            by_qstar=raw["match_ImPi_total_by_qstar_over_T2"],
        )

    def interpolator(self, component: str = "im") -> RegularGridInterpolator:
        values = {"im": self.im_pi, "re": self.re_pi, "noise": self.noise}[component]
        return RegularGridInterpolator((self.k, self.omega), values, bounds_error=False, fill_value=None)

    def factorization_spread(self, signal_floor: float = 1.0e-9) -> float:
        reference = self.by_qstar[len(self.qstar)//2]
        spread = np.max(np.abs(self.by_qstar-reference[None, :, :]), axis=0)
        mask = np.abs(reference) > signal_floor
        if not np.any(mask):
            return 0.0
        return float(np.max(spread[mask]/np.abs(reference[mask])))
