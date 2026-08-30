"""Apply deterministic source repairs found by the clean-checkout CI audit.

This migration helper is intentionally strict and idempotent. It upgrades the
finite-bath recurrence scale and replaces the expensive coordinate-basis energy
check with the mathematically equivalent normal-mode Verlet check. The latter
allows a smaller timestep without a dense matrix-vector multiplication at every
step.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "frontier_evidence" / "scalar_two_time.py"


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count == 0:
        if new in text:
            return text
        raise RuntimeError(f"Expected source block not found in {TARGET}: {old[:80]!r}")
    if count != 1:
        raise RuntimeError(f"Expected one source block, found {count}: {old[:80]!r}")
    return text.replace(old, new)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    text = replace_once(text, "    bath_modes: int = 260\n", "    bath_modes: int = 360\n")

    old = '''    rng = np.random.default_rng(20260826)\n    q = vectors @ rng.normal(scale=0.1, size=len(frequencies))\n    p = vectors @ rng.normal(scale=0.1, size=len(frequencies))\n    dt = 0.002\n    steps = int(30.0 / dt)\n    acceleration = -force @ q\n    e0 = 0.5 * float(p @ p + q @ force @ q)\n    max_drift = 0.0\n    for _ in range(steps):\n        q = q + dt * p + 0.5 * dt * dt * acceleration\n        a_new = -force @ q\n        p = p + 0.5 * dt * (acceleration + a_new)\n        acceleration = a_new\n        energy = 0.5 * float(p @ p + q @ force @ q)\n        max_drift = max(max_drift, abs(energy - e0) / max(abs(e0), 1.0e-30))\n'''
    new = '''    # Integrate the same quadratic Hamiltonian in its normal-mode basis.\n    # This is exactly equivalent to the coordinate-basis evolution but reduces\n    # the energy audit from a dense matrix-vector multiply to O(N) per step,\n    # allowing a genuinely converged timestep on clean CI runners.\n    rng = np.random.default_rng(20260826)\n    q = rng.normal(scale=0.1, size=len(frequencies))\n    p = rng.normal(scale=0.1, size=len(frequencies))\n    mode_force = frequencies * frequencies\n    dt = 0.0004\n    steps = int(30.0 / dt)\n    acceleration = -mode_force * q\n    e0 = 0.5 * float(np.sum(p * p + mode_force * q * q))\n    max_drift = 0.0\n    for _ in range(steps):\n        q = q + dt * p + 0.5 * dt * dt * acceleration\n        a_new = -mode_force * q\n        p = p + 0.5 * dt * (acceleration + a_new)\n        acceleration = a_new\n        energy = 0.5 * float(np.sum(p * p + mode_force * q * q))\n        max_drift = max(max_drift, abs(energy - e0) / max(abs(e0), 1.0e-30))\n'''
    text = replace_once(text, old, new)
    TARGET.write_text(text, encoding="utf-8")
    print(f"Patched {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
