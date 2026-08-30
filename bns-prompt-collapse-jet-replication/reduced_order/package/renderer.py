"""Fast OpenCV renderer for the reduced-order BNS-remnant surrogate."""
from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import Iterable, Tuple

import cv2
import numpy as np
from scipy.ndimage import gaussian_filter

from physics import ReducedOrderRemnant, RemnantState, sigmoid


@dataclass(frozen=True)
class RenderConfig:
    width: int = 512
    height: int = 514
    view_half_extent_km: float = 1650.0
    azimuth_deg: float = -23.0
    inclination_deg: float = 12.0
    seed: int = 241010958
    disk_particles: int = 24_000
    dynamical_ejecta_particles: int = 42_000
    wind_particles: int = 34_000
    gaussian_sigma_px: float = 2.2


class ParticleInitialConditions:
    """Deterministic Monte Carlo samples used by every rendered frame."""

    def __init__(self, config: RenderConfig) -> None:
        self.cfg = config
        rng = np.random.default_rng(config.seed)

        # Remnant disk / torus samples.
        n = config.disk_particles
        self.disk_phi0 = rng.uniform(0.0, 2.0 * np.pi, n)
        self.disk_r0 = np.clip(rng.normal(72.0, 28.0, n), 16.0, 175.0)
        self.disk_z0 = rng.normal(0.0, 15.0, n)
        self.disk_phase1 = rng.uniform(0.0, 2.0 * np.pi, n)
        self.disk_phase2 = rng.uniform(0.0, 2.0 * np.pi, n)
        self.disk_weight = np.exp(-0.5 * ((self.disk_r0 - 68.0) / 36.0) ** 2)

        # Dynamical ejecta.  Most visible mass is slow enough to remain within
        # the 1000-km-scale rendering domain; a sparse fast tail leaves the view.
        n = config.dynamical_ejecta_particles
        mixture = rng.random(n)
        speed = np.empty(n)
        slow = mixture < 0.89
        medium = (mixture >= 0.89) & (mixture < 0.992)
        fast = mixture >= 0.992
        speed[slow] = rng.lognormal(mean=np.log(2_000.0), sigma=0.40, size=slow.sum())
        speed[medium] = rng.lognormal(mean=np.log(8_000.0), sigma=0.42, size=medium.sum())
        speed[fast] = rng.uniform(35_000.0, 210_000.0, fast.sum())
        self.dyn_speed_km_s = np.clip(speed, 350.0, 210_000.0)

        # Equatorially concentrated ejecta, with an m=1 asymmetry reflecting the
        # unequal 1.25+1.65 Msun binary.
        self.dyn_phi = rng.vonmises(mu=0.45, kappa=0.42, size=n)
        self.dyn_costheta = np.clip(rng.normal(0.0, 0.24, n), -0.88, 0.88)
        self.dyn_launch_radius = rng.uniform(28.0, 90.0, n)
        self.dyn_weight = np.exp(-self.dyn_speed_km_s / 9_000.0)
        self.dyn_turbulence = rng.uniform(0.0, 2.0 * np.pi, n)

        # Broad post-merger wind, launched continuously after 0.1 s.
        n = config.wind_particles
        q = rng.uniform(0.0, 1.0, n)
        # Bias launch times toward the first several hundred ms, while retaining
        # material launched throughout the movie.
        self.wind_launch_s = 0.10 + 1.25 * q ** 1.7
        self.wind_speed_km_s = np.clip(
            rng.lognormal(mean=np.log(1_600.0), sigma=0.45, size=n),
            280.0,
            6_500.0,
        )
        self.wind_phi = rng.uniform(0.0, 2.0 * np.pi, n)
        self.wind_costheta = rng.uniform(-0.93, 0.93, n)
        self.wind_weight = rng.lognormal(mean=0.0, sigma=0.35, size=n)
        self.wind_turbulence = rng.uniform(0.0, 2.0 * np.pi, n)

        # Persistent random phases for field-line bundles.
        self.field_phases = rng.uniform(0.0, 2.0 * np.pi, 30)
        self.field_offsets = rng.normal(0.0, 1.0, (30, 3))


class SurrogateRenderer:
    def __init__(
        self,
        model: ReducedOrderRemnant | None = None,
        config: RenderConfig | None = None,
    ) -> None:
        self.model = model or ReducedOrderRemnant()
        self.cfg = config or RenderConfig()
        self.ic = ParticleInitialConditions(self.cfg)
        self._rotation = self._camera_rotation()
        self._density_bar = self._make_density_bar()
        self._magnetization_bar = self._make_magnetization_bar()

    def _camera_rotation(self) -> np.ndarray:
        az = math.radians(self.cfg.azimuth_deg)
        inc = math.radians(self.cfg.inclination_deg)
        rz = np.array(
            [
                [math.cos(az), -math.sin(az), 0.0],
                [math.sin(az), math.cos(az), 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )
        # Rotate about x so that the disk is viewed slightly from above while the
        # spin axis remains almost vertical on screen.
        rx = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, math.cos(inc), -math.sin(inc)],
                [0.0, math.sin(inc), math.cos(inc)],
            ],
            dtype=np.float64,
        )
        return rx @ rz

    def project(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        xyz = np.vstack((x, y, z))
        rotated = self._rotation @ xyz
        screen_x = rotated[0]
        screen_y = rotated[2]
        depth = rotated[1]
        scale_x = (self.cfg.width - 1) / (2.0 * self.cfg.view_half_extent_km)
        scale_y = (self.cfg.height - 1) / (2.0 * self.cfg.view_half_extent_km)
        u = self.cfg.width * 0.5 + screen_x * scale_x
        v = self.cfg.height * 0.5 - screen_y * scale_y
        return u, v, depth

    def _disk_coordinates(self, t: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        ic = self.ic
        # Kepler-like differential rotation.  The coefficient is softened so that
        # the animation does not alias at 30 fps while retaining turbulent winding.
        omega = 42.0 * (72.0 / np.maximum(ic.disk_r0, 18.0)) ** 1.5
        phi = ic.disk_phi0 + omega * t
        expansion = 1.0 + 0.62 * (1.0 - np.exp(-max(t - 0.06, 0.0) / 0.38))
        radial_turbulence = 1.0 + 0.10 * np.sin(3.0 * phi + ic.disk_phase1 + 13.0 * t)
        r = ic.disk_r0 * expansion * radial_turbulence
        scale_height = 1.0 + 1.7 * (1.0 - np.exp(-max(t - 0.08, 0.0) / 0.34))
        z = (
            ic.disk_z0 * scale_height
            + 9.0 * np.sin(2.0 * phi + ic.disk_phase2) * sigmoid((t - 0.07) / 0.025)
        )
        x = r * np.cos(phi)
        y = r * np.sin(phi)
        state = self.model.state_at(t)
        mass_ratio = state.disk_mass_msun / self.model.p.initial_disk_mass_msun
        weight = ic.disk_weight * (0.20 + 0.80 * mass_ratio)
        return x, y, z, weight

    def _dynamical_ejecta_coordinates(self, t: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        ic = self.ic
        sin_theta = np.sqrt(np.maximum(0.0, 1.0 - ic.dyn_costheta ** 2))
        radius = ic.dyn_launch_radius + ic.dyn_speed_km_s * t
        # Weak angular corrugation creates the filamentary, non-axisymmetric shell.
        corrugation = 1.0 + 0.055 * np.sin(5.0 * ic.dyn_phi + ic.dyn_turbulence + 19.0 * t)
        radius = radius * corrugation
        x = radius * sin_theta * np.cos(ic.dyn_phi)
        y = radius * sin_theta * np.sin(ic.dyn_phi)
        z = radius * ic.dyn_costheta
        # Homologous dilution.  Fast particles fade rapidly once sparse, so the
        # visible 1e5 g/cm^3 contour remains near the central ~1000 km.
        dilution = 1.0 / (1.0 + (t / 0.045) ** 2.35)
        velocity_fade = np.exp(-np.maximum(radius - 1_550.0, 0.0) / 420.0)
        weight = ic.dyn_weight * dilution * velocity_fade
        return x, y, z, weight

    def _wind_coordinates(self, t: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        ic = self.ic
        age = t - ic.wind_launch_s
        active = age > 0.0
        if not np.any(active):
            empty = np.empty(0, dtype=np.float64)
            return empty, empty, empty, empty
        age = age[active]
        costheta = ic.wind_costheta[active]
        sin_theta = np.sqrt(np.maximum(0.0, 1.0 - costheta ** 2))
        phi = ic.wind_phi[active] + 0.13 * np.sin(7.0 * age + ic.wind_turbulence[active])
        radius = 70.0 + ic.wind_speed_km_s[active] * age
        x = radius * sin_theta * np.cos(phi)
        y = radius * sin_theta * np.sin(phi)
        z = radius * costheta
        dilution = 1.0 / (1.0 + (age / 0.22) ** 2.0)
        edge_fade = np.exp(-np.maximum(radius - 1_600.0, 0.0) / 450.0)
        weight = ic.wind_weight[active] * dilution * edge_fade
        return x, y, z, weight

    def _histogram(self, u: np.ndarray, v: np.ndarray, weight: np.ndarray) -> np.ndarray:
        valid = (
            (u >= 0.0)
            & (u < self.cfg.width)
            & (v >= 0.0)
            & (v < self.cfg.height)
            & np.isfinite(weight)
            & (weight > 0.0)
        )
        if not np.any(valid):
            return np.zeros((self.cfg.height, self.cfg.width), dtype=np.float32)
        hist, _, _ = np.histogram2d(
            v[valid],
            u[valid],
            bins=(self.cfg.height, self.cfg.width),
            range=((0.0, float(self.cfg.height)), (0.0, float(self.cfg.width))),
            weights=weight[valid],
        )
        return hist.astype(np.float32)

    @staticmethod
    def _normalize_component(field: np.ndarray, peak_density: float) -> np.ndarray:
        if not np.any(field > 0.0):
            return field
        reference = np.percentile(field[field > 0.0], 99.7)
        if reference <= 0.0:
            return field
        return np.clip(field / reference, 0.0, 1.8) * peak_density

    def _density_field(self, t: float, state: RemnantState) -> np.ndarray:
        xd, yd, zd, wd = self._disk_coordinates(t)
        ud, vd, _ = self.project(xd, yd, zd)
        disk = self._histogram(ud, vd, wd)
        disk = gaussian_filter(disk, sigma=self.cfg.gaussian_sigma_px)
        disk_peak = 1.0e10 * (0.25 + 0.75 * state.disk_mass_msun / self.model.p.initial_disk_mass_msun)
        disk = self._normalize_component(disk, disk_peak)

        xe, ye, ze, we = self._dynamical_ejecta_coordinates(t)
        ue, ve, _ = self.project(xe, ye, ze)
        ejecta = self._histogram(ue, ve, we)
        ejecta = gaussian_filter(ejecta, sigma=self.cfg.gaussian_sigma_px * 1.35)
        ejecta_peak = 2.2e7 / (1.0 + (t / 0.075) ** 1.1)
        ejecta = self._normalize_component(ejecta, ejecta_peak)

        xw, yw, zw, ww = self._wind_coordinates(t)
        uw, vw, _ = self.project(xw, yw, zw)
        wind = self._histogram(uw, vw, ww)
        wind = gaussian_filter(wind, sigma=self.cfg.gaussian_sigma_px * 1.55)
        wind_fraction = state.post_merger_ejecta_mass_msun / max(
            self.model.p.final_post_merger_ejecta_mass_msun, 1.0e-30
        )
        wind_peak = 1.5e7 * max(wind_fraction, 0.05)
        wind = self._normalize_component(wind, wind_peak)

        # Screen-space surrogate for the nested, optically thin density contours
        # used in the published 3-D visualization.  It represents the projected
        # low-density cocoon and expanding ejecta shell; the particle components
        # above still carry the asymmetry and filamentary structure.
        yy, xx = np.mgrid[: self.cfg.height, : self.cfg.width]
        km_per_px_x = 2.0 * self.cfg.view_half_extent_km / (self.cfg.width - 1)
        km_per_px_y = 2.0 * self.cfg.view_half_extent_km / (self.cfg.height - 1)
        x_km = (xx - self.cfg.width * 0.5) * km_per_px_x
        y_km = (self.cfg.height * 0.5 - yy) * km_per_px_y
        angle = np.arctan2(y_km, x_km)

        early_shift = 42.0 * math.exp(-t / 0.055)
        x_shell = x_km - early_shift * math.cos(18.0 * t)
        y_shell = y_km - 0.45 * early_shift * math.sin(15.0 * t)
        radius = np.hypot(x_shell, y_shell)
        angle_shifted = np.arctan2(y_shell, x_shell)

        shell_radius = (
            105.0
            + 1_430.0 * sigmoid((t - 0.024) / 0.0043)
            + 120.0 * min(1.0, max(0.0, (t - 0.35) / 1.05))
        )
        angular_corrugation = (
            1.0
            + 0.080 * np.sin(5.0 * angle_shifted + 17.0 * t)
            + 0.045 * np.sin(11.0 * angle_shifted - 9.0 * t)
        )
        target_radius = shell_radius * angular_corrugation
        shell_width = 42.0 + 78.0 * (1.0 - math.exp(-t / 0.16))
        shell_amplitude = 1.6e6 / (1.0 + (t / 0.16) ** 1.45) + 1.2e5
        shell = shell_amplitude * np.exp(-0.5 * ((radius - target_radius) / shell_width) ** 2)

        # A diffuse interior prevents the shell from looking like a single line
        # and creates the nested blue/green translucent layers seen after jet launch.
        interior_scale = max(150.0, 0.78 * shell_radius)
        interior_amplitude = (
            4.2e6 * math.exp(-0.5 * (t / 0.105) ** 2)
            + 1.4e5 / (1.0 + (t / 0.45) ** 1.2)
        )
        interior = (
            interior_amplitude
            * np.exp(-0.5 * (radius / interior_scale) ** 3.0)
            * (0.78 + 0.22 * np.sin(3.0 * angle_shifted + 5.0 * t) ** 2)
        )

        # MRI-driven post-merger wind produces a slower inner cocoon beginning
        # near 0.1 s.
        wind_cocoon_strength = sigmoid((t - 0.12) / 0.045)
        wind_radius = 180.0 + 520.0 * (1.0 - math.exp(-max(t - 0.10, 0.0) / 0.32))
        wind_width = 90.0 + 75.0 * min(1.0, t / 0.8)
        wind_cocoon = (
            3.8e6
            * wind_cocoon_strength
            * np.exp(-0.5 * ((radius - wind_radius) / wind_width) ** 2)
            * (0.82 + 0.18 * np.cos(4.0 * angle + 8.0 * t) ** 2)
        )

        return disk + ejecta + wind + shell.astype(np.float32) + interior.astype(np.float32) + wind_cocoon.astype(np.float32)

    @staticmethod
    def _make_density_bar() -> np.ndarray:
        gradient = np.arange(255, -1, -1, dtype=np.uint8).reshape(-1, 1)
        return cv2.applyColorMap(gradient, cv2.COLORMAP_TURBO)

    @staticmethod
    def _make_magnetization_bar() -> np.ndarray:
        bar = np.zeros((256, 1, 3), dtype=np.uint8)
        low = np.array([155.0, 155.0, 155.0])
        high = np.array([250.0, 20.0, 245.0])
        for row in range(256):
            q = 1.0 - row / 255.0
            # BGR interpolation from grey at sigma=0.1 to magenta at sigma=10.
            bar[row, 0] = np.clip((1.0 - q) * low + q * high, 0.0, 255.0)
        return bar

    def _render_density(self, canvas: np.ndarray, rho: np.ndarray) -> None:
        positive = rho > 1.0e5
        if not np.any(positive):
            return
        log_rho = np.zeros_like(rho, dtype=np.float32)
        log_rho[positive] = np.log10(rho[positive])
        normalized = np.clip((log_rho - 5.0) / 5.0, 0.0, 1.0)
        indexed = np.uint8(np.rint(normalized * 255.0))
        colors = cv2.applyColorMap(indexed, cv2.COLORMAP_TURBO)
        # Opacity rises with density but remains translucent to mimic nested
        # volume contours rather than an opaque heat map.
        alpha = np.clip(0.025 + 0.58 * normalized ** 1.35, 0.0, 0.66)
        alpha[~positive] = 0.0
        alpha3 = alpha[..., None]
        canvas[:] = np.uint8(
            np.clip(canvas.astype(np.float32) * (1.0 - alpha3) + colors.astype(np.float32) * alpha3, 0.0, 255.0)
        )

        # A few isodensity edges make the shell and torus legible.
        for level, value in ((5.25, 55), (6.25, 80), (7.25, 105), (8.25, 125), (9.25, 145)):
            mask = np.uint8(log_rho >= level) * 255
            edge = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
            edge_alpha = (edge.astype(np.float32) / 255.0) * 0.20
            edge_alpha3 = edge_alpha[..., None]
            pale = np.full_like(canvas, value, dtype=np.uint8)
            canvas[:] = np.uint8(
                np.clip(canvas.astype(np.float32) * (1.0 - edge_alpha3) + pale.astype(np.float32) * edge_alpha3, 0.0, 255.0)
            )

    def _jet_length_km(self, t: float, hemisphere: str) -> float:
        if hemisphere == "south":
            field_onset = 0.095
            tau = 0.065
        else:
            field_onset = 0.145
            tau = 0.082
        if t <= field_onset:
            return 0.0
        return 1_720.0 * (1.0 - math.exp(-(t - field_onset) / tau))

    def _draw_field_bundle(self, canvas: np.ndarray, t: float, state: RemnantState, hemisphere: str) -> None:
        sign = 1.0 if hemisphere == "north" else -1.0
        strength = state.north_jet_strength if hemisphere == "north" else state.south_jet_strength
        # Permit faint pre-plateau field lines; luminosity reaches its quoted value later.
        visual_strength = max(strength, sigmoid((t - (0.145 if hemisphere == "north" else 0.095)) / 0.020) * 0.28)
        length = self._jet_length_km(t, hemisphere)
        if length < 15.0 or visual_strength < 0.015:
            return

        n_lines = 24
        n_points = 185
        base_opening = math.radians(state.jet_half_opening_angle_deg)
        for line_index in range(n_lines):
            q = (line_index + 0.5) / n_lines
            phase0 = self.ic.field_phases[line_index]
            offset = self.ic.field_offsets[line_index]
            z_abs = np.linspace(12.0, length * (0.90 + 0.13 * math.sin(phase0)), n_points)
            z = sign * z_abs
            sheath = 0.28 + 0.82 * q
            radius = (
                9.0
                + z_abs * math.tan(base_opening) * sheath
                + 14.0 * np.sin(z_abs / 115.0 + phase0 + 4.0 * t)
            )
            twist = phase0 + sign * (z_abs / 72.0 + 27.0 * t) + 0.25 * np.sin(z_abs / 53.0 + phase0)
            x = radius * np.cos(twist) + 4.0 * offset[0]
            y = radius * np.sin(twist) + 4.0 * offset[1]
            # Mild kink instability / turbulent wandering.
            x += (5.0 + 18.0 * q) * np.sin(z_abs / 230.0 + phase0 + 2.1 * t)
            y += (5.0 + 15.0 * q) * np.cos(z_abs / 195.0 + 1.7 * phase0 - 1.8 * t)
            u, v, _ = self.project(x, y, z)
            points = np.column_stack((u, v)).astype(np.int32)
            valid = (
                (points[:, 0] >= -40)
                & (points[:, 0] < self.cfg.width + 40)
                & (points[:, 1] >= -40)
                & (points[:, 1] < self.cfg.height + 40)
            )
            points = points[valid]
            if len(points) < 2:
                continue
            # Alternate cyan/green and magenta filaments around a pink core.
            if line_index % 4 == 0:
                color = (175, 235, 45)  # BGR, green-cyan
            elif line_index % 4 == 1:
                color = (205, 125, 255)
            elif line_index % 4 == 2:
                color = (120, 220, 120)
            else:
                color = (240, 55, 245)
            line_thickness = 1 if q > 0.28 else 2
            overlay = canvas.copy()
            cv2.polylines(overlay, [points], False, color, line_thickness, cv2.LINE_AA)
            alpha = 0.20 + 0.65 * min(1.0, visual_strength)
            cv2.addWeighted(overlay, alpha, canvas, 1.0 - alpha, 0.0, dst=canvas)

        # Bright Poynting-dominated spine and a turbulent terminal cap.
        z_abs = np.linspace(10.0, length, 150)
        z = sign * z_abs
        radius = 5.0 + 8.0 * np.sin(z_abs / 95.0 + 21.0 * t)
        x = radius * np.cos(z_abs / 48.0 + 10.0 * t)
        y = radius * np.sin(z_abs / 48.0 + 10.0 * t)
        u, v, _ = self.project(x, y, z)
        pts = np.column_stack((u, v)).astype(np.int32)
        overlay = canvas.copy()
        cv2.polylines(overlay, [pts], False, (244, 55, 248), 2, cv2.LINE_AA)
        cv2.addWeighted(overlay, 0.30 + 0.55 * min(1.0, visual_strength), canvas, 0.70 - 0.55 * min(1.0, visual_strength), 0.0, dst=canvas)

        endpoint = np.array([x[-1], y[-1], z[-1]], dtype=np.float64)
        ue, ve, _ = self.project(endpoint[0:1], endpoint[1:2], endpoint[2:3])
        cap_radius = int(4 + 12 * min(1.0, visual_strength))
        cap_overlay = canvas.copy()
        cv2.ellipse(
            cap_overlay,
            (int(ue[0]), int(ve[0])),
            (cap_radius, max(4, cap_radius // 2)),
            0.0,
            0.0,
            360.0,
            (225, 80, 245),
            -1,
            cv2.LINE_AA,
        )
        cv2.addWeighted(cap_overlay, 0.32, canvas, 0.68, 0.0, dst=canvas)

    def _draw_equatorial_magnetic_loops(self, canvas: np.ndarray, t: float, state: RemnantState) -> None:
        amplitude = min(1.0, state.magnetic_to_internal_energy_ratio / 0.01)
        if amplitude < 0.03:
            return
        for i in range(12):
            phase = self.ic.field_phases[i]
            phi = np.linspace(0.0, 2.0 * np.pi, 160)
            radius = 78.0 + 7.0 * i + 9.0 * np.sin(3.0 * phi + phase + 8.0 * t)
            x = radius * np.cos(phi + 9.0 * t)
            y = radius * np.sin(phi + 9.0 * t)
            z = (8.0 + 2.5 * i) * np.sin(2.0 * phi + phase)
            u, v, _ = self.project(x, y, z)
            pts = np.column_stack((u, v)).astype(np.int32)
            overlay = canvas.copy()
            color = (175, 230, 55) if i % 2 == 0 else (230, 90, 240)
            cv2.polylines(overlay, [pts], True, color, 1, cv2.LINE_AA)
            cv2.addWeighted(overlay, 0.10 + 0.26 * amplitude, canvas, 0.90 - 0.26 * amplitude, 0.0, dst=canvas)

    @staticmethod
    def _put_rotated_text(
        canvas: np.ndarray,
        text: str,
        center: Tuple[int, int],
        font_scale: float = 0.42,
        thickness: int = 1,
    ) -> None:
        (tw, th), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        pad = 4
        tile = np.zeros((th + baseline + 2 * pad, tw + 2 * pad, 3), dtype=np.uint8)
        cv2.putText(
            tile,
            text,
            (pad, th + pad),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (240, 240, 240),
            thickness,
            cv2.LINE_AA,
        )
        tile = cv2.rotate(tile, cv2.ROTATE_90_COUNTERCLOCKWISE)
        h, w = tile.shape[:2]
        x0 = center[0] - w // 2
        y0 = center[1] - h // 2
        x1 = x0 + w
        y1 = y0 + h
        if x0 < 0 or y0 < 0 or x1 > canvas.shape[1] or y1 > canvas.shape[0]:
            return
        mask = np.any(tile > 0, axis=2)
        roi = canvas[y0:y1, x0:x1]
        roi[mask] = tile[mask]

    def _draw_overlays(self, canvas: np.ndarray, sim_time_s: float) -> None:
        cv2.putText(
            canvas,
            f"{sim_time_s * 1000.0:.2f} ms",
            (7, 19),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.50,
            (245, 245, 245),
            1,
            cv2.LINE_AA,
        )

        # 500-km diagonal scale bar.
        km_per_px = 2.0 * self.cfg.view_half_extent_km / (self.cfg.width - 1)
        length_px = int(round(500.0 / km_per_px))
        x0, y0 = 20, 122
        x1, y1 = x0 + int(0.86 * length_px), y0 + int(0.50 * length_px)
        cv2.line(canvas, (x0, y0), (x1, y1), (235, 235, 235), 1, cv2.LINE_AA)
        # Orthogonal end caps.
        cv2.line(canvas, (x0 - 2, y0 + 4), (x0 + 2, y0 - 4), (235, 235, 235), 1, cv2.LINE_AA)
        cv2.line(canvas, (x1 - 2, y1 + 4), (x1 + 2, y1 - 4), (235, 235, 235), 1, cv2.LINE_AA)
        cv2.putText(canvas, "500 km", (24, y0 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.39, (235, 235, 235), 1, cv2.LINE_AA)

        # Magnetization color bar, logarithmic sigma=b^2/(4*pi*rho), 1e-1..1e1.
        mag_bar = cv2.resize(self._magnetization_bar, (20, 171), interpolation=cv2.INTER_LINEAR)
        canvas[7:178, 421:441] = mag_bar
        for y, label in ((12, "1.0e+1"), (92, "1.0"), (176, "1.0e-1")):
            cv2.putText(canvas, label, (450, y), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (230, 230, 230), 1, cv2.LINE_AA)
        self._put_rotated_text(canvas, "b^2 / 4pi rho", (505, 95), 0.34, 1)

        # Density color bar, 1e5..1e10 g/cm^3.
        density_bar = cv2.resize(self._density_bar, (20, 170), interpolation=cv2.INTER_LINEAR)
        canvas[337:507, 414:434] = density_bar
        density_ticks = (
            (342, "1.0e+10"),
            (375, "1.0e+9"),
            (408, "1.0e+8"),
            (441, "1.0e+7"),
            (474, "1.0e+6"),
            (507, "1.0e+5"),
        )
        for y, label in density_ticks:
            cv2.putText(canvas, label, (443, y), cv2.FONT_HERSHEY_SIMPLEX, 0.31, (230, 230, 230), 1, cv2.LINE_AA)
        self._put_rotated_text(canvas, "rho [g cm^-3]", (505, 420), 0.34, 1)

        # Small xyz triad at lower left.
        origin = (66, 465)
        cv2.arrowedLine(canvas, origin, (42, 486), (40, 40, 245), 1, cv2.LINE_AA, tipLength=0.22)
        cv2.arrowedLine(canvas, origin, (91, 486), (70, 225, 225), 1, cv2.LINE_AA, tipLength=0.22)
        cv2.arrowedLine(canvas, origin, (68, 425), (70, 245, 70), 1, cv2.LINE_AA, tipLength=0.15)
        cv2.putText(canvas, "x", (35, 495), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (80, 80, 250), 1, cv2.LINE_AA)
        cv2.putText(canvas, "y", (92, 495), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (90, 235, 235), 1, cv2.LINE_AA)
        cv2.putText(canvas, "z", (68, 423), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (90, 250, 90), 1, cv2.LINE_AA)

    def render_frame(self, sim_time_s: float) -> Tuple[np.ndarray, RemnantState]:
        state = self.model.state_at(sim_time_s)
        canvas = np.zeros((self.cfg.height, self.cfg.width, 3), dtype=np.uint8)
        rho = self._density_field(sim_time_s, state)
        self._render_density(canvas, rho)

        # Apparent horizon: only several pixels at this 1000-km-scale view.
        center_u, center_v, _ = self.project(
            np.array([0.0]), np.array([0.0]), np.array([0.0])
        )
        horizon_px = max(
            2,
            int(
                round(
                    state.black_hole_horizon_radius_km
                    * (self.cfg.width - 1)
                    / (2.0 * self.cfg.view_half_extent_km)
                )
            ),
        )
        cv2.circle(canvas, (int(center_u[0]), int(center_v[0])), horizon_px + 1, (95, 95, 95), -1, cv2.LINE_AA)
        cv2.circle(canvas, (int(center_u[0]), int(center_v[0])), horizon_px, (0, 0, 0), -1, cv2.LINE_AA)

        self._draw_equatorial_magnetic_loops(canvas, sim_time_s, state)
        self._draw_field_bundle(canvas, sim_time_s, state, "south")
        self._draw_field_bundle(canvas, sim_time_s, state, "north")
        self._draw_overlays(canvas, sim_time_s)
        return canvas, state
