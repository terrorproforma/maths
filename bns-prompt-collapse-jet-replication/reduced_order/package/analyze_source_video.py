#!/usr/bin/env python3
"""Extract reproducible screen-space measurements from the supplied source MP4.

The simulation timestamp is read from a supplied timeline CSV.  This avoids an
OCR dependency in normal use; the exact timestamps from the user's 431-frame
clip are distributed as source_timeline.csv.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Dict, Tuple

import cv2
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter


def phase_for_time(ms: float, frame: int) -> Tuple[str, str]:
    if 130 <= frame <= 142:
        return (
            "editorial hold at 74.40 ms",
            "The physical state is frozen for 13 frames while the playback rate changes.",
        )
    if ms < 20.0:
        return (
            "prompt-collapse aftermath",
            "The apparent horizon already exists; a compact hot torus and the innermost ejecta dominate.",
        )
    if ms < 40.0:
        return (
            "disk circularisation and dynamical ejecta",
            "The asymmetric tidal/shock ejecta expands while the remnant disk winds the seed magnetic field.",
        )
    if ms < 100.0:
        return (
            "MRI growth and alpha-Omega dynamo",
            "The low-density envelope expands and the disk magnetic energy approaches saturation.",
        )
    if ms < 130.0:
        return (
            "disk-wide MRI resolution",
            "MRI-driven turbulence is established across the disk; polar magnetic pressure is building.",
        )
    if ms < 200.0:
        return (
            "southern magnetosphere and jet launch",
            "A magnetically dominated southern funnel becomes visible first; the northern side remains weaker.",
        )
    if ms < 300.0:
        return (
            "asymmetric bipolar jet growth",
            "The southern helical bundle is mature while the northern Poynting outflow catches up.",
        )
    if ms < 400.0:
        return (
            "Blandford-Znajek bipolar outflow",
            "Both polar bundles are established and the jet is collimated by the surrounding gas pressure.",
        )
    if ms < 440.0:
        return (
            "onset of post-merger mass ejection",
            "MRI-driven viscous heating expands the disk and begins launching the broad post-merger wind.",
        )
    if ms < 600.0:
        return (
            "mature jet plus disk wind",
            "The movie now evolves on a fixed spacetime background; the broad density shell and polar jet coexist.",
        )
    if ms < 1000.0:
        return (
            "wind-dominated secular evolution",
            "Mass ejection overtakes accretion, neutrino cooling fades and the low-density shell continues expanding.",
        )
    return (
        "late jet weakening and funnel widening",
        "The Poynting luminosity declines after about one second and the magnetosphere opens toward roughly nine degrees.",
    )


def measure_frame(frame_bgr: np.ndarray) -> Dict[str, float]:
    height, width = frame_bgr.shape[:2]
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    yy, xx = np.mgrid[:height, :width]

    # Exclude the two color bars, timestamp, scale bar and coordinate triad.
    roi = (xx < 409) & (yy > 35) & (yy < height - 10)
    roi &= ~((xx < 118) & (yy < 193))
    roi &= ~((xx < 125) & (yy > 392))

    # Density contours use the blue-green-yellow-red map.  A small opening and
    # blur suppresses the much thinner magnetic-field filaments.
    density_mask = roi & (s > 42) & (v > 22) & (h < 138)
    density_u8 = np.uint8(density_mask) * 255
    density_u8 = cv2.morphologyEx(
        density_u8, cv2.MORPH_OPEN, np.ones((3, 3), dtype=np.uint8)
    )
    density_u8 = cv2.morphologyEx(
        density_u8, cv2.MORPH_CLOSE, np.ones((5, 5), dtype=np.uint8)
    )
    density_probability = gaussian_filter((density_u8 > 0).astype(np.float32), 3.0)
    blob = density_probability > 0.08
    blob &= roi

    center_x = width / 2.0
    center_y = height / 2.0
    y_blob, x_blob = np.nonzero(blob)
    if len(x_blob) == 0:
        centroid_x = centroid_y = radial_95 = radial_99 = 0.0
        x_extent = y_extent = 0.0
        left_right_asymmetry = 0.0
    else:
        centroid_x = float(x_blob.mean())
        centroid_y = float(y_blob.mean())
        radius = np.hypot(x_blob - center_x, y_blob - center_y)
        radial_95 = float(np.percentile(radius, 95.0))
        radial_99 = float(np.percentile(radius, 99.0))
        x_extent = float(x_blob.max() - x_blob.min() + 1)
        y_extent = float(y_blob.max() - y_blob.min() + 1)
        left = np.count_nonzero(x_blob < center_x)
        right = np.count_nonzero(x_blob >= center_x)
        left_right_asymmetry = float((right - left) / max(right + left, 1))

    # The robust jet proxy uses magenta pixels in the central 220-pixel strip.
    # It deliberately ignores green field lines; the proxy is therefore a lower
    # bound on visible field-line extent rather than a physical jet boundary.
    magenta = (
        roi
        & (s > 68)
        & (v > 48)
        & (h >= 138)
        & (xx > 145)
        & (xx < 365)
    )
    y_mag, x_mag = np.nonzero(magenta)
    north_px = south_px = magenta_pixels = 0.0
    if len(y_mag):
        north_candidates = y_mag[y_mag < center_y - 15]
        south_candidates = y_mag[y_mag > center_y + 15]
        if len(north_candidates):
            north_px = float(center_y - np.min(north_candidates))
        if len(south_candidates):
            south_px = float(np.max(south_candidates) - center_y)
        magenta_pixels = float(len(y_mag))

    # Calibrate approximate screen scale from the displayed 500-km ruler.  Its
    # measured diagonal is approximately 78 pixels in the source frames.
    km_per_pixel = 500.0 / 78.0
    return {
        "density_coloured_pixels": float(np.count_nonzero(density_mask)),
        "density_blob_pixels": float(np.count_nonzero(blob)),
        "density_centroid_x_px": centroid_x,
        "density_centroid_y_px": centroid_y,
        "density_r95_px": radial_95,
        "density_r99_px": radial_99,
        "density_r95_screen_km": radial_95 * km_per_pixel,
        "density_r99_screen_km": radial_99 * km_per_pixel,
        "density_x_extent_px": x_extent,
        "density_y_extent_px": y_extent,
        "right_minus_left_density_fraction": left_right_asymmetry,
        "north_magenta_jet_extent_px": north_px,
        "south_magenta_jet_extent_px": south_px,
        "north_magenta_jet_extent_screen_km": north_px * km_per_pixel,
        "south_magenta_jet_extent_screen_km": south_px * km_per_pixel,
        "magenta_jet_pixels": magenta_pixels,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument(
        "--timeline",
        type=Path,
        default=Path(__file__).with_name("source_timeline.csv"),
    )
    parser.add_argument("--output", type=Path, default=Path("frame_by_frame_analysis.csv"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    timeline = pd.read_csv(args.timeline)
    if "sim_time_ms" not in timeline.columns:
        raise ValueError("Timeline requires sim_time_ms")

    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open {args.video}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count != len(timeline):
        raise ValueError(
            f"Video has {frame_count} frames but timeline has {len(timeline)} rows"
        )

    rows = []
    previous_sim_ms = None
    previous_metrics = None
    for index in range(frame_count):
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError(f"Decode failed at frame {index}")
        sim_ms = float(timeline.iloc[index]["sim_time_ms"])
        metrics = measure_frame(frame)
        phase, interpretation = phase_for_time(sim_ms, index)
        if previous_sim_ms is None:
            delta_sim_ms = 0.0
            physical_seconds_per_video_second = 0.0
            density_trend = "baseline"
            jet_trend = "baseline"
        else:
            delta_sim_ms = sim_ms - previous_sim_ms
            physical_seconds_per_video_second = delta_sim_ms * fps / 1000.0
            density_change = metrics["density_blob_pixels"] - previous_metrics["density_blob_pixels"]
            if density_change > 250.0:
                density_trend = "visible density area expanding"
            elif density_change < -250.0:
                density_trend = "visible density area contracting/thinning"
            else:
                density_trend = "visible density area approximately steady"
            jet_change = metrics["magenta_jet_pixels"] - previous_metrics["magenta_jet_pixels"]
            if jet_change > 35.0:
                jet_trend = "magenta magnetized structure strengthening"
            elif jet_change < -35.0:
                jet_trend = "magenta magnetized structure weakening/reorienting"
            else:
                jet_trend = "magenta magnetized structure approximately steady"

        row = {
            "frame": index,
            "video_time_s": index / fps,
            "sim_time_ms": sim_ms,
            "delta_sim_time_ms": delta_sim_ms,
            "physical_seconds_per_video_second": physical_seconds_per_video_second,
            "slow_motion_factor": (
                1.0 / physical_seconds_per_video_second
                if physical_seconds_per_video_second > 0.0
                else float("inf")
            ),
            "phase": phase,
            "frame_interpretation": interpretation,
            "density_trend_from_previous_frame": density_trend,
            "jet_trend_from_previous_frame": jet_trend,
            **metrics,
        }
        rows.append(row)
        previous_sim_ms = sim_ms
        previous_metrics = metrics

    capture.release()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output, index=False)
    print(f"Wrote {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
