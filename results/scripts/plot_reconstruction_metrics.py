#!/usr/bin/env python3
"""Plot reconstruction quality metrics (MAE, CrossScore) per scene.

CSV schema (results/data/reconstruction_metrics.csv):
    scene,MAE,CrossScore

MAE and CrossScore live on different scales, so each metric gets its own
panel (small multiples) rather than a shared/dual axis.

If the CSV has no data rows yet, the existing placeholder figure is left
untouched.
"""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt

from style import SEQUENTIAL_BLUE, SURFACE, bar_value_labels, savefig, style_axes

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "data" / "reconstruction_metrics.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "figures" / "reconstruction_metrics.png"

METRICS = ["MAE", "CrossScore"]


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def plot(rows, output_path):
    scenes = [r["scene"] for r in rows]

    fig, axes = plt.subplots(
        1, len(METRICS), figsize=(max(6, 1.3 * len(scenes) * len(METRICS)), 4.5), dpi=200
    )
    fig.patch.set_facecolor(SURFACE)

    for ax, metric in zip(axes, METRICS):
        ax.set_facecolor(SURFACE)
        heights = [float(r[metric]) for r in rows]
        bars = ax.bar(scenes, heights, color=SEQUENTIAL_BLUE, zorder=3)
        bar_value_labels(ax, bars, fmt="{:.3f}")
        ax.set_xticks(range(len(scenes)))
        ax.set_xticklabels(scenes, rotation=15, ha="right")
        style_axes(ax, ylabel=metric, title=metric)

    fig.suptitle("Reconstruction Quality", x=0.02, ha="left", fontsize=12, color="#0b0b0b")
    savefig(fig, output_path)
    print(f"Wrote figure: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default=DEFAULT_CSV, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    args = parser.parse_args()

    rows = load_rows(args.csv)
    if not rows:
        print(f"No data rows in {args.csv}; keeping existing placeholder at {args.output}.")
        return
    plot(rows, args.output)


if __name__ == "__main__":
    main()
