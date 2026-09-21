#!/usr/bin/env python3
"""Plot simulated task success rate under each disturbance type.

Style matches the paper's own counterfactual plots
(icra2026_yubi-real2sim/figs/plots/plot_all_policy_success_significance.py,
plot_cup_success_significance.py): the first policy encountered (the
shared/generalist checkpoint) is blue, the second (the task-specific
checkpoint) is amber, white-edged bars, and 95% Wilson-interval error bars.
Disturbances were only applied in simulation, so the disturbance groups are
sim only; the real result and the Clean sim result (read from
results/data/success_rate_overall/<scene>.csv) sit at the left as the
reference, real in gray as in Fig. 1.

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
from matplotlib.patches import Patch

from style import (
    ERROR_BAR_COLOR,
    POLICY_ALPHAS,
    POLICY_COLORS,
    REAL_COLOR,
    RIG_NAMES,
    SPINE_COLOR,
    apply_icra_style,
    savefig,
    style_axes,
    wilson_interval,
)

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "success_rate_disturbances"
OVERALL_DIR = Path(__file__).resolve().parents[1] / "data" / "success_rate_overall"
DEFAULT_FIGURE_DIR = Path(__file__).resolve().parents[1] / "figures" / "success_rate_disturbances"


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def draw_group(ax, x, rows_by_policy, policies, colors, alphas):
    width = 0.8 / len(policies)
    for i, policy in enumerate(policies):
        r = rows_by_policy.get(policy)
        if r is None:
            continue
        pos = x - 0.4 + width / 2 + i * width
        value = 100 * float(r["success_rate"])
        lo, hi = wilson_interval(int(r["successes"]), int(r["num_trials"]))
        ax.bar([pos], [value], width, color=colors[i], alpha=alphas[i], edgecolor="white",
               linewidth=0.4, zorder=2)
        ax.errorbar([pos], [value], yerr=[[max(0.0, value - 100 * lo)], [max(0.0, 100 * hi - value)]],
                    fmt="none", ecolor=ERROR_BAR_COLOR, elinewidth=0.6, capsize=2, capthick=0.6,
                    zorder=3)


def plot(rows, clean_rows, scene, task, output_path):
    """Real and Clean sim sit at the left as the reference, then one group per
    disturbance (sim only)."""
    sim = [r for r in rows if r["domain"] == "sim"]
    disturbances = list(dict.fromkeys(r["disturbance"] for r in sim))
    policies = list(dict.fromkeys(r["policy"] for r in sim))
    n = len(policies)
    sim_colors = [POLICY_COLORS[min(i, len(POLICY_COLORS) - 1)] for i in range(n)]
    real_alphas = [POLICY_ALPHAS[min(i, len(POLICY_ALPHAS) - 1)] for i in range(n)]

    reference = [(label, {r["policy"]: r for r in clean_rows if r["domain"] == domain})
                 for label, domain in (("Real", "real"), ("Clean", "sim"))]
    reference = [(label, by_policy) for label, by_policy in reference if by_policy]
    gap = 0.5 if reference else 0.0

    apply_icra_style()
    groups = len(reference) + len(disturbances)
    fig, ax = plt.subplots(figsize=(max(4.3, 0.62 * groups + 1.6), 3.1))
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.28, top=0.82)

    ticks, labels = [], []
    for j, (label, by_policy) in enumerate(reference):
        real = label == "Real"
        draw_group(ax, j, by_policy, policies, [REAL_COLOR] * n if real else sim_colors,
                   real_alphas if real else [1.0] * n)
        ticks.append(j)
        labels.append(label)
    if reference:
        ax.axvline(len(reference) - 0.5 + gap / 2, color=SPINE_COLOR, linewidth=0.6,
                   linestyle=(0, (3, 2)), zorder=1)
    for j, disturbance in enumerate(disturbances):
        x = len(reference) + gap + j
        draw_group(ax, x, {r["policy"]: r for r in sim if r["disturbance"] == disturbance},
                   policies, sim_colors, [1.0] * n)
        ticks.append(x)
        labels.append(disturbance.replace("_remove_", " ").replace("pinhole_", "pinhole "))

    ax.set_xticks(ticks, labels, rotation=28, ha="right")
    ax.set_xlim(-0.5, ticks[-1] + 0.5)
    ax.set_ylim(0, 110)
    ax.set_yticks([0, 25, 50, 75, 100])
    style_axes(ax, ylabel="Success rate (%)")
    ax.set_title(f"{RIG_NAMES.get(scene, scene)} / {task}", loc="left", fontsize=9, pad=4)

    handles = []
    if any(label == "Real" for label, _ in reference):
        handles += [Patch(facecolor=REAL_COLOR, alpha=real_alphas[i], label=f"Real {p}")
                    for i, p in enumerate(policies)]
    handles += [Patch(facecolor=sim_colors[i], label=f"Sim {p}") for i, p in enumerate(policies)]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.02, 1.0), ncol=len(handles),
               frameon=False, fontsize=8, handlelength=1.5, columnspacing=1.4, handletextpad=0.5)

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
        if not any(r["domain"] == "sim" for r in rows):
            print(f"No sim data rows in {csv_path}; skipping.")
            continue
        scene, task = csv_path.stem.split("_", 1)
        overall = OVERALL_DIR / f"{scene}.csv"
        clean_rows = [r for r in load_rows(overall) if r["task"] == task] if overall.exists() else []
        plot(rows, clean_rows, scene, task, args.figure_dir / f"{csv_path.stem}.png")


if __name__ == "__main__":
    main()
