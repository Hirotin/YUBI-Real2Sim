#!/usr/bin/env python3
"""Plot task success rate: real robot vs. clean simulation.

CSV schema (results/data/success_rate_overall.csv):
    task,condition,success_rate,num_trials

    task           name of the manipulation task
    condition      e.g. "Real" or "Sim (Clean)"
    success_rate   fraction in [0, 1]
    num_trials     number of trials the rate is computed from (optional)

If the CSV has no data rows yet, the existing placeholder figure is left
untouched.
"""

import argparse
import csv
from pathlib import Path

import numpy as np

from style import assign_colors, bar_value_labels, legend, new_figure, savefig, style_axes

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "data" / "success_rate_overall.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "figures" / "success_rate_overall.png"


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def plot(rows, output_path):
    tasks = list(dict.fromkeys(r["task"] for r in rows))
    conditions = list(dict.fromkeys(r["condition"] for r in rows))
    colors = assign_colors(conditions)

    values = {c: [None] * len(tasks) for c in conditions}
    for r in rows:
        values[r["condition"]][tasks.index(r["task"])] = float(r["success_rate"]) * 100

    fig, ax = new_figure(figsize=(max(6, 1.4 * len(tasks) + 2), 4.5))
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
    style_axes(ax, ylabel="Success rate (%)", title="Task Success Rate: Real vs. Clean Sim")
    legend(ax, ncol=len(conditions))
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
