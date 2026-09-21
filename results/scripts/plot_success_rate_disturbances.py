#!/usr/bin/env python3
"""Plot simulated task success rate under each disturbance type.

Style matches the paper's own counterfactual plots
(icra2026_yubi-real2sim/figs/plots/plot_all_policy_success_significance.py,
plot_cup_success_significance.py): the first policy encountered (the
shared/generalist checkpoint) is blue, the second (the task-specific
checkpoint) is amber, white-edged bars, and 95% Wilson-interval error bars.
Only sim results are plotted -- disturbances were only applied in
simulation, so there is no per-disturbance real measurement to show.

One figure is produced per CSV found in
results/data/success_rate_disturbances/. Each CSV is one (scene, task)
pair; drop in a new <scene>_<task>.csv to get a new figure with no script
changes.

CSV schema (results/data/success_rate_disturbances/<scene>_<task>.csv):
    disturbance,domain,policy,success_rate,num_trials,successes

    disturbance    name of the disturbance / perturbation type
    domain         expected to be "sim" (see ingest_policy_success.py)
    policy         policy id (e.g. "pi_1", "pi_2"); first-seen policy is
                   blue, second is amber
    success_rate   fraction in [0, 1]
    num_trials     number of trials the rate is computed from
    successes      number of successful trials (for the Wilson interval)

A CSV with no data rows is skipped.
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from style import (
    RIG_NAMES,
    POLICY_COLORS,
    ERROR_BAR_COLOR,
    apply_icra_style,
    savefig,
    style_axes,
    wilson_interval,
)

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "success_rate_disturbances"
DEFAULT_FIGURE_DIR = Path(__file__).resolve().parents[1] / "figures" / "success_rate_disturbances"


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return [r for r in csv.DictReader(f) if r["domain"] == "sim"]


def plot(rows, scene, task, output_path):
    disturbances = list(dict.fromkeys(r["disturbance"] for r in rows))
    policies = list(dict.fromkeys(r["policy"] for r in rows))
    policy_color = {p: POLICY_COLORS[min(i, len(POLICY_COLORS) - 1)] for i, p in enumerate(policies)}
    lookup = {(r["disturbance"], r["policy"]): r for r in rows}

    apply_icra_style()
    fig, ax = plt.subplots(figsize=(max(4.3, 0.62 * len(disturbances) + 1.6), 3.1))
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.28, top=0.82)

    x = range(len(disturbances))
    width = 0.8 / len(policies)
    for i, policy in enumerate(policies):
        offset = -0.4 + width / 2 + i * width
        present = [lookup.get((d, policy)) for d in disturbances]
        positions = [j + offset for j, r in enumerate(present) if r is not None]
        present = [r for r in present if r is not None]
        values = [100 * float(r["success_rate"]) for r in present]
        intervals = [wilson_interval(int(r["successes"]), int(r["num_trials"])) for r in present]
        errors = [
            [max(0.0, v - 100 * lo) for v, (lo, _) in zip(values, intervals)],
            [max(0.0, 100 * hi - v) for v, (_, hi) in zip(values, intervals)],
        ]
        ax.bar(
            positions, values, width, color=policy_color[policy], edgecolor="white",
            linewidth=0.4, zorder=2,
        )
        ax.errorbar(
            positions, values, yerr=errors, fmt="none", ecolor=ERROR_BAR_COLOR,
            elinewidth=0.6, capsize=2, capthick=0.6, zorder=3,
        )

    ax.set_xticks(list(x), disturbances, rotation=28, ha="right")
    ax.set_xlim(-0.5, len(disturbances) - 0.5)
    ax.set_ylim(0, 110)
    ax.set_yticks([0, 25, 50, 75, 100])
    style_axes(ax, ylabel="Sim success rate (%)")
    ax.set_title(f"{RIG_NAMES.get(scene, scene)} / {task}", loc="left", fontsize=9, pad=4)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=policy_color[p], label=p) for p in policies
    ]
    fig.legend(
        handles=handles, loc="upper left", bbox_to_anchor=(0.02, 1.0), ncol=len(policies),
        frameon=False, fontsize=8,
    )

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
            print(f"No sim data rows in {csv_path}; skipping.")
            continue
        scene, task = csv_path.stem.split("_", 1)
        plot(rows, scene, task, args.figure_dir / f"{csv_path.stem}.png")


if __name__ == "__main__":
    main()
