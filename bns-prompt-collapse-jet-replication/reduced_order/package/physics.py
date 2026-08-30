"""Reduced-order physical state model for a prompt-collapse BNS merger remnant.

This is not a numerical-relativity GRMHD solver.  It is a physics-informed
surrogate calibrated to the timing and integral quantities reported by
Hayashi et al., Phys. Rev. Lett. 134, 211407 (2025).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Dict

G_SI = 6.67430e-11
C_SI = 299_792_458.0
M_SUN_KG = 1.98847e30


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def sigmoid(x: float) -> float:
    if x >= 0.0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def smoothstep(x: float) -> float:
    x = clamp(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def normalized_exponential_decay(
    t: float,
    start_time: float,
    end_time: float,
    initial_value: float,
    final_value: float,
    tau: float,
) -> float:
    """Exponential decay constrained to hit both requested endpoint values."""
    if t <= start_time:
        return initial_value
    if t >= end_time:
        return final_value
    u = t - start_time
    u_end = end_time - start_time
    e = math.exp(-u / tau)
    e_end = math.exp(-u_end / tau)
    fraction = (e - e_end) / (1.0 - e_end)
    return final_value + (initial_value - final_value) * fraction


def normalized_exponential_growth(
    t: float,
    start_time: float,
    end_time: float,
    initial_value: float,
    final_value: float,
    tau: float,
) -> float:
    """Exponential growth constrained to hit both requested endpoint values."""
    if t <= start_time:
        return initial_value
    if t >= end_time:
        return final_value
    u = t - start_time
    u_end = end_time - start_time
    numerator = 1.0 - math.exp(-u / tau)
    denominator = 1.0 - math.exp(-u_end / tau)
    return initial_value + (final_value - initial_value) * numerator / denominator


@dataclass(frozen=True)
class RemnantParameters:
    neutron_star_1_mass_msun: float = 1.25
    neutron_star_2_mass_msun: float = 1.65
    total_mass_msun: float = 2.90
    black_hole_mass_msun: float = 2.77
    black_hole_dimensionless_spin: float = 0.76
    initial_disk_mass_msun: float = 6.2e-2
    final_disk_mass_msun: float = 1.6e-3
    dynamical_ejecta_mass_msun: float = 1.6e-3
    final_post_merger_ejecta_mass_msun: float = 4.7e-3
    initial_maximum_magnetic_field_gauss: float = 1.0e15
    target_poynting_luminosity_erg_s: float = 1.0e49
    target_neutrino_luminosity_erg_s: float = 1.0e53
    simulation_end_s: float = 1.39864

    @property
    def gravitational_radius_km(self) -> float:
        return (
            G_SI
            * self.black_hole_mass_msun
            * M_SUN_KG
            / (C_SI * C_SI)
            / 1000.0
        )

    @property
    def horizon_radius_km(self) -> float:
        a = self.black_hole_dimensionless_spin
        return self.gravitational_radius_km * (1.0 + math.sqrt(1.0 - a * a))

    @property
    def horizon_angular_frequency_rad_s(self) -> float:
        # Kerr horizon angular frequency, Omega_H = a*c/(2*r_+), with a dimensionless.
        return (
            self.black_hole_dimensionless_spin
            * C_SI
            / (2.0 * self.horizon_radius_km * 1000.0)
        )


@dataclass(frozen=True)
class RemnantState:
    time_s: float
    disk_mass_msun: float
    dynamical_ejecta_mass_msun: float
    post_merger_ejecta_mass_msun: float
    total_ejecta_mass_msun: float
    magnetic_to_internal_energy_ratio: float
    neutrino_luminosity_erg_s: float
    north_jet_luminosity_erg_s: float
    south_jet_luminosity_erg_s: float
    north_jet_strength: float
    south_jet_strength: float
    jet_half_opening_angle_deg: float
    black_hole_horizon_radius_km: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


class ReducedOrderRemnant:
    """Integral-quantity surrogate for disk, ejecta, neutrinos and jets."""

    def __init__(self, parameters: RemnantParameters | None = None) -> None:
        self.p = parameters or RemnantParameters()

    def disk_mass(self, t: float) -> float:
        # The paper reports the steep decline beginning near 0.1 s.
        return normalized_exponential_decay(
            t=t,
            start_time=0.08,
            end_time=self.p.simulation_end_s,
            initial_value=self.p.initial_disk_mass_msun,
            final_value=self.p.final_disk_mass_msun,
            tau=0.22,
        )

    def post_merger_ejecta_mass(self, t: float) -> float:
        # Turbulent-viscous ejection starts growing after ~0.1 s and is clearly
        # established by ~0.4 s.  This smooth curve is normalized to the reported
        # final 4.7e-3 Msun.
        return normalized_exponential_growth(
            t=t,
            start_time=0.10,
            end_time=self.p.simulation_end_s,
            initial_value=0.0,
            final_value=self.p.final_post_merger_ejecta_mass_msun,
            tau=0.42,
        )

    def magnetic_energy_fraction(self, t: float) -> float:
        # MRI amplification saturates at approximately one percent of internal
        # energy around 0.1 s in the supplemental material.
        return 0.01 * sigmoid((t - 0.075) / 0.015)

    def neutrino_luminosity(self, t: float) -> float:
        prompt = self.p.target_neutrino_luminosity_erg_s * math.exp(-t / 0.16)
        mri_reheating_peak = 3.0e52 * math.exp(-0.5 * ((t - 0.10) / 0.028) ** 2)
        late_floor = 2.0e49 * math.exp(-t / 0.65)
        return prompt + mri_reheating_peak + late_floor

    @staticmethod
    def _jet_strength(t: float, plateau_time: float, rise_width: float) -> float:
        rise = sigmoid((t - plateau_time) / rise_width)
        # The reported luminosity begins declining after roughly one second.
        decline = 1.0 if t <= 1.0 else math.exp(-(t - 1.0) / 0.55)
        return rise * decline

    def north_jet_strength(self, t: float) -> float:
        # North reaches ~1e49 erg/s near 0.30 s.
        return self._jet_strength(t, plateau_time=0.30, rise_width=0.034)

    def south_jet_strength(self, t: float) -> float:
        # South reaches ~1e49 erg/s near 0.13 s.
        return self._jet_strength(t, plateau_time=0.13, rise_width=0.022)

    @staticmethod
    def jet_opening_angle_deg(t: float) -> float:
        # Supplemental material: less than 6 degrees before 1 s, about 9 degrees
        # at 1.4 s.  The visual line bundle includes a wider turbulent sheath.
        if t <= 1.0:
            return 5.5
        return 5.5 + 3.5 * smoothstep((t - 1.0) / 0.4)

    def state_at(self, t: float) -> RemnantState:
        t = clamp(t, 0.0, self.p.simulation_end_s)
        post = self.post_merger_ejecta_mass(t)
        north = self.north_jet_strength(t)
        south = self.south_jet_strength(t)
        return RemnantState(
            time_s=t,
            disk_mass_msun=self.disk_mass(t),
            dynamical_ejecta_mass_msun=self.p.dynamical_ejecta_mass_msun,
            post_merger_ejecta_mass_msun=post,
            total_ejecta_mass_msun=self.p.dynamical_ejecta_mass_msun + post,
            magnetic_to_internal_energy_ratio=self.magnetic_energy_fraction(t),
            neutrino_luminosity_erg_s=self.neutrino_luminosity(t),
            north_jet_luminosity_erg_s=(
                self.p.target_poynting_luminosity_erg_s * north
            ),
            south_jet_luminosity_erg_s=(
                self.p.target_poynting_luminosity_erg_s * south
            ),
            north_jet_strength=north,
            south_jet_strength=south,
            jet_half_opening_angle_deg=self.jet_opening_angle_deg(t),
            black_hole_horizon_radius_km=self.p.horizon_radius_km,
        )
