#!/usr/bin/env python3
"""Plot task success rate: real robot vs. clean simulation.

Style matches the paper's own Fig. 1 (icra2026_yubi-real2sim/figs/plots/
plot_policy_success.py): real = gray, sim = blue, and the first policy
encountered is drawn at reduced opacity so both policies read as the same
domain color family. Error bars are 95% Wilson intervals.

One figure is produced, with one panel per CSV found in
results/data/success_rate_overall/, laid out left to right as in Fig. 1.
Each CSV is one scene; drop in a new <scene>.csv to get a new panel with no
script changes.

CSV schema (results/data/success_rate_overall/<scene>.csv):
    task,domain,policy,success_rate,num_trials,successes

    task           name of the manipulation task
    domain         "real" or "sim"
    policy         policy id (e.g. "pi_1", "pi_2"); first-seen policy is
                   drawn at reduced opacity, second at full opacity
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
from matplotlib.patches import Patch

from style import (
    RIG_NAMES,
    REAL_COLOR,
    SIM_COLOR,
    POLICY_ALPHAS,
    ERROR_BAR_COLOR,
    apply_icra_style,
    savefig,
    style_axes,
    wilson_interval,
)

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "success_rate_overall"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "figures" / "success_rate_overall.png"

DOMAIN_COLOR = {"real": REAL_COLOR, "sim": SIM_COLOR}


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def draw_panel(ax, rows, scene, domains, policies, policy_alpha):
    tasks = list(dict.fromkeys(r["task"] for r in rows))
    lookup = {(r["task"], r["domain"], r["policy"]): r for r in rows}
    groups = [(d, p) for d in domains for p in policies]
    group_width = 0.8 / len(groups)
    offsets = [-0.4 + group_width / 2 + i * group_width for i in range(len(groups))]

    for (domain, policy), offset in zip(groups, offsets):
        rows_for_series = [lookup.get((task, domain, policy)) for task in tasks]
        positions = [i + offset for i, r in enumerate(rows_for_series) if r is not None]
        present = [r for r in rows_for_series if r is not None]
        values = [100 * float(r["success_rate"]) for r in present]
        intervals = [wilson_interval(int(r["successes"]), int(r["num_trials"])) for r in present]
        errors = [
            [max(0.0, v - 100 * lo) for v, (lo, _) in zip(values, intervals)],
            [max(0.0, 100 * hi - v) for v, (_, hi) in zip(values, intervals)],
        ]
        ax.bar(positions, values, width=0.155, color=DOMAIN_COLOR.get(domain, "#4a4a4a"),
               alpha=policy_alpha[policy], linewidth=0, zorder=2)
        ax.errorbar(positions, values, yerr=errors, fmt="none", ecolor=ERROR_BAR_COLOR,
                    elinewidth=0.65, capsize=2, capthick=0.65, zorder=3)

    ax.set_xticks(range(len(tasks)), tasks)
    ax.set_xlim(-0.52, len(tasks) - 0.48)
    ax.set_ylim(0, 110)
    ax.set_yticks([0, 25, 50, 75, 100])
    style_axes(ax)
    ax.set_title(RIG_NAMES.get(scene, scene), fontsize=8.5, pad=4)


def plot(scenes, output_path):
    """scenes: list of (scene name, rows), drawn left to right as in Fig. 1."""
    all_rows = [r for _, rows in scenes for r in rows]
    domains = list(dict.fromkeys(r["domain"] for r in all_rows))
    policies = list(dict.fromkeys(r["policy"] for r in all_rows))
    policy_alpha = {p: POLICY_ALPHAS[min(i, len(POLICY_ALPHAS) - 1)] for i, p in enumerate(policies)}

    apply_icra_style()
    fig, axes = plt.subplots(1, len(scenes), figsize=(2.39 * len(scenes), 2.31),
                             sharey=True, squeeze=False)
    fig.subplots_adjust(left=0.52 / (2.39 * len(scenes)), right=0.992, bottom=0.1, top=0.8,
                        wspace=0.13)
    for ax, (scene, rows) in zip(axes[0], scenes):
        draw_panel(ax, rows, scene, domains, policies, policy_alpha)
    axes[0][0].set_ylabel("Task success rate (%)")

    handles = [
        Patch(facecolor=DOMAIN_COLOR.get(d, "#4a4a4a"), alpha=policy_alpha[p], label=f"{d.title()} {p}")
        for d in domains for p in policies
    ]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 1.01), ncol=len(handles),
               frameon=False, fontsize=8.5, handlelength=1.5, columnspacing=1.6, handletextpad=0.55)
    savefig(fig, output_path)
    print(f"Wrote figure: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    args = parser.parse_args()

    scenes = [(p.stem, load_rows(p)) for p in sorted(args.data_dir.glob("*.csv"))]
    scenes = [(scene, rows) for scene, rows in scenes if rows]
    if not scenes:
        print(f"No CSVs with data in {args.data_dir}; nothing to do.")
        return
    plot(scenes, args.output)


if __name__ == "__main__":
    main()
