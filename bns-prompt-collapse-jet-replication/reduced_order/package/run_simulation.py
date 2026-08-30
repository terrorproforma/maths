#!/usr/bin/env python3
"""Render the reduced-order replication as MP4 and write its state history."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import List

import cv2
import numpy as np
import pandas as pd

from physics import ReducedOrderRemnant
from renderer import RenderConfig, SurrogateRenderer


def load_timeline(path: Path) -> np.ndarray:
    table = pd.read_csv(path)
    if "sim_time_ms" not in table.columns:
        raise ValueError(f"{path} must contain a sim_time_ms column")
    values = table["sim_time_ms"].to_numpy(dtype=np.float64) / 1000.0
    if len(values) < 2 or np.any(~np.isfinite(values)) or np.any(np.diff(values) < 0.0):
        raise ValueError("Timeline must contain at least two finite, non-decreasing times")
    return values


def decimate_timeline(times: np.ndarray, frame_count: int | None) -> np.ndarray:
    if frame_count is None or frame_count >= len(times):
        return times
    if frame_count < 2:
        raise ValueError("--frames must be at least 2")
    indices = np.rint(np.linspace(0, len(times) - 1, frame_count)).astype(int)
    return times[indices]


def encode_h264(intermediate_path: Path, output_path: Path, fps: float) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        intermediate_path.replace(output_path)
        print("ffmpeg was not found; retained the OpenCV MPEG-4 file instead of H.264.")
        return
    command = [
        ffmpeg,
        "-y",
        "-loglevel",
        "error",
        "-i",
        str(intermediate_path),
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-r",
        f"{fps:g}",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    subprocess.run(command, check=True)
    intermediate_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render a physics-informed, reduced-order visual surrogate of the "
            "Hayashi et al. prompt-collapse BNS black-hole/jet simulation."
        )
    )
    parser.add_argument(
        "--timeline",
        type=Path,
        default=Path(__file__).with_name("source_timeline.csv"),
        help="CSV with sim_time_ms values; defaults to the 431-frame source timeline.",
    )
    parser.add_argument("--output", type=Path, default=Path("surrogate_replication.mp4"))
    parser.add_argument("--state-csv", type=Path, default=Path("surrogate_state_history.csv"))
    parser.add_argument("--fps", type=float, default=30.0)
    parser.add_argument(
        "--frames",
        type=int,
        default=None,
        help="Optionally decimate to this many frames for a faster preview.",
    )
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=514)
    parser.add_argument("--disk-particles", type=int, default=24_000)
    parser.add_argument("--ejecta-particles", type=int, default=42_000)
    parser.add_argument("--wind-particles", type=int, default=34_000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.fps <= 0.0:
        raise ValueError("--fps must be positive")
    for name in ("width", "height", "disk_particles", "ejecta_particles", "wind_particles"):
        if getattr(args, name) <= 0:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")

    timeline = decimate_timeline(load_timeline(args.timeline), args.frames)
    config = RenderConfig(
        width=args.width,
        height=args.height,
        disk_particles=args.disk_particles,
        dynamical_ejecta_particles=args.ejecta_particles,
        wind_particles=args.wind_particles,
    )
    renderer = SurrogateRenderer(model=ReducedOrderRemnant(), config=config)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.state_csv.parent.mkdir(parents=True, exist_ok=True)
    intermediate = args.output.with_name(args.output.stem + ".opencv.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        str(intermediate),
        fourcc,
        args.fps,
        (config.width, config.height),
    )
    if not writer.isOpened():
        raise RuntimeError(f"Could not open video writer for {intermediate}")

    state_rows: List[dict] = []
    try:
        total = len(timeline)
        for index, t in enumerate(timeline):
            frame, state = renderer.render_frame(float(t))
            writer.write(frame)
            row = {"frame": index, "video_time_s": index / args.fps, **state.to_dict()}
            state_rows.append(row)
            if index == 0 or (index + 1) % max(1, total // 20) == 0 or index + 1 == total:
                print(f"Rendered {index + 1:4d}/{total} frames ({100.0 * (index + 1) / total:5.1f}%)", flush=True)
    finally:
        writer.release()

    encode_h264(intermediate, args.output, args.fps)
    pd.DataFrame(state_rows).to_csv(args.state_csv, index=False)
    print(f"Wrote video: {args.output}")
    print(f"Wrote state history: {args.state_csv}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
