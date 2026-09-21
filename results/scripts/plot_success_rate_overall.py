#!/usr/bin/env python3
"""Plot task success rate: real robot vs. clean simulation.

One figure is produced per CSV found in results/data/success_rate_overall/.
Each CSV is one scene; drop in a new <scene>.csv to get a new figure with no
script changes.

CSV schema (results/data/success_rate_overall/<scene>.csv):
    task,condition,success_rate,num_trials

    task           name of the manipulation task
    condition      series label, e.g. "Real (pi_1)" / "Sim (pi_2)"
    success_rate   fraction in [0, 1]
    num_trials     number of trials the rate is computed from (optional)

A CSV with no data rows is skipped.
"""

import argparse
import csv
from pathlib import Path

import numpy as np

from style import assign_colors, bar_value_labels, legend, new_figure, savefig, style_axes

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "success_rate_overall"
DEFAULT_FIGURE_DIR = Path(__file__).resolve().parents[1] / "figures" / "success_rate_overall"


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def plot(rows, scene, output_path):
    tasks = list(dict.fromkeys(r["task"] for r in rows))
    conditions = list(dict.fromkeys(r["condition"] for r in rows))
    colors = assign_colors(conditions)

    values = {c: [None] * len(tasks) for c in conditions}
    for r in rows:
        values[r["condition"]][tasks.index(r["task"])] = float(r["success_rate"]) * 100

    fig, ax = new_figure(figsize=(max(6, 1.7 * len(tasks) + 2), 4.5))
    x = np.arange(len(tasks))
    width = 0.8 / len(conditions)

    for i, cond in enumerate(conditions):
        offsets = x - 0.4 + width / 2 + i * width
        heights = [v if v is not None else 0 for v in values[cond]]
        bars = ax.bar(offsets, heights, width=width, label=cond, color=colors[cond], zorder=3)
        bar_value_labels(ax, bars)

    ax.set_xticks(x)
    ax.set_xticklabels(tasks)
    ax.set_ylim(0, 100)
    style_axes(ax, ylabel="Success rate (%)", title=f"Task Success Rate: Real vs. Clean Sim — {scene}")
    legend(ax, ncol=len(conditions))
    savefig(fig, output_path)
    print(f"Wrote figure: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR, type=Path)
    parser.add_argument("--figure-dir", default=DEFAULT_FIGURE_DIR, type=Path)
    args = parser.parse_args()

    csv_paths = sorted(args.data_dir.glob("*.csv"))
    if not csv_paths:
        print(f"No CSVs found in {args.data_dir}; nothing to do.")
        return

    args.figure_dir.mkdir(parents=True, exist_ok=True)
    for csv_path in csv_paths:
        rows = load_rows(csv_path)
        if not rows:
            print(f"No data rows in {csv_path}; skipping.")
            continue
        scene = csv_path.stem
        plot(rows, scene, args.figure_dir / f"{scene}.png")


if __name__ == "__main__":
    main()
