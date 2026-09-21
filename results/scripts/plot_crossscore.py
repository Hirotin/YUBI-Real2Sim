#!/usr/bin/env python3
"""Plot CrossScore per scene.

CSV schema (results/data/crossscore.csv):
    scene,CrossScore

Bars are colored per
scene with the same palette as the paper's Fig. 3 (Duo/Flat/G2), so a scene
carries the same color across every figure in this repo.

If the CSV has no data rows yet, the existing placeholder figure is left
untouched.
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from style import REAL_COLOR, SCENE_COLORS, apply_icra_style, savefig, style_axes

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "data" / "crossscore.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "figures" / "crossscore.png"

METRICS = ["CrossScore"]


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def plot(rows, output_path):
    scenes = [r["scene"] for r in rows]
    colors = [SCENE_COLORS.get(s, REAL_COLOR) for s in scenes]

    apply_icra_style()
    fig, axes = plt.subplots(1, len(METRICS), figsize=(3.5, 2.62), squeeze=False)
    axes = axes[0]
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.12, top=0.93)

    for ax, metric in zip(axes, METRICS):
        heights = [float(r[metric]) for r in rows]
        bars = ax.bar(scenes, heights, color=colors, zorder=2)
        for bar, h in zip(bars, heights):
            ax.annotate(
                f"{h:.3f}", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3),
                textcoords="offset points", ha="center", va="bottom", fontsize=7,
            )
        style_axes(ax, ylabel=metric)

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
