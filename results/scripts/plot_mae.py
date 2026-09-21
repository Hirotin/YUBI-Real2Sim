#!/usr/bin/env python3
"""Plot the sim-to-real success-rate MAE per scene and condition.

Same definition as the paper (icra2026_yubi-real2sim/docs/experiments/
mae_paper_20260921/calculate.py), in percentage points:

    MAE(scene, condition) = mean over (task, policy) cells of
        |100 * sim_successes / sim_trials  -  100 * real_successes / real_trials|

Real is always the Clean real measurement (disturbances exist only in sim);
every cell is weighted equally. Computed from the CSVs the success-rate
figures already use (results/data/success_rate_overall/<scene>.csv and
results/data/success_rate_disturbances/<scene>_<task>.csv), so no extra
input is needed. The values are also written to results/data/mae.csv.
"""

import argparse
import csv
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from style import REAL_COLOR, RIG_NAMES, SCENE_COLORS, apply_icra_style, savefig, style_axes

RESULTS = Path(__file__).resolve().parents[1]
OVERALL_DIR = RESULTS / "data" / "success_rate_overall"
DISTURBANCES_DIR = RESULTS / "data" / "success_rate_disturbances"
DEFAULT_TABLE = RESULTS / "data" / "mae.csv"
DEFAULT_OUTPUT = RESULTS / "figures" / "mae.png"


def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def percent(row):
    return Fraction(100 * int(row["successes"]), int(row["num_trials"]))


def compute():
    """Return [{condition, scene, n_policy_cells, mae_pp}], Clean first."""
    summary = []
    for overall in sorted(OVERALL_DIR.glob("*.csv")):
        scene = overall.stem
        rows = load_rows(overall)
        real = {(r["task"], r["policy"]): percent(r) for r in rows if r["domain"] == "real"}
        sim = {"Clean": {(r["task"], r["policy"]): percent(r) for r in rows if r["domain"] == "sim"}}
        for path in sorted(DISTURBANCES_DIR.glob(f"{scene}_*.csv")):
            task = path.stem.split("_", 1)[1]
            for r in load_rows(path):
                if r["domain"] == "sim":
                    sim.setdefault(r["disturbance"], {})[(task, r["policy"])] = percent(r)
        for condition, cells in sim.items():
            errors = [abs(value - real[cell]) for cell, value in cells.items() if cell in real]
            if errors:
                summary.append({"condition": condition, "scene": scene,
                                "n_policy_cells": len(errors),
                                "mae_pp": float(sum(errors) / len(errors))})
    return summary


def plot(summary, output_path):
    conditions = list(dict.fromkeys(r["condition"] for r in summary))
    scenes = list(dict.fromkeys(r["scene"] for r in summary))
    lookup = {(r["condition"], r["scene"]): r["mae_pp"] for r in summary}

    apply_icra_style()
    fig, ax = plt.subplots(figsize=(7.16, 2.9))
    fig.subplots_adjust(left=0.075, right=0.992, bottom=0.27, top=0.88)
    width = 0.8 / len(scenes)
    for i, scene in enumerate(scenes):
        xs = [j - 0.4 + width / 2 + i * width for j, c in enumerate(conditions) if (c, scene) in lookup]
        ys = [lookup[(c, scene)] for c in conditions if (c, scene) in lookup]
        ax.bar(xs, ys, width, color=SCENE_COLORS.get(scene, REAL_COLOR), edgecolor="white",
               linewidth=0.4, label=RIG_NAMES.get(scene, scene), zorder=2)
        for x, y in zip(xs, ys):
            ax.text(x, y + 0.8, f"{y:.1f}", ha="center", va="bottom", fontsize=5.6, rotation=90)
    labels = [c.replace("_remove_", " ").replace("pinhole_", "pinhole ") for c in conditions]
    ax.set_xticks(range(len(conditions)), labels, rotation=28, ha="right")
    ax.set_xlim(-0.55, len(conditions) - 0.45)
    ax.set_ylim(0, max(r["mae_pp"] for r in summary) * 1.22)
    style_axes(ax, ylabel="Sim-to-real MAE (pp) ↓")
    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=len(scenes), frameon=False,
               fontsize=8.5, handlelength=1.5, columnspacing=1.6)
    savefig(fig, output_path)
    print(f"Wrote figure: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", default=DEFAULT_TABLE, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    args = parser.parse_args()

    summary = compute()
    if not summary:
        print("No success-rate CSVs with both real and sim rows; nothing to do.")
        return
    conditions = list(dict.fromkeys(r["condition"] for r in summary))
    summary.sort(key=lambda r: conditions.index(r["condition"]))
    with open(args.table, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    print(f"Wrote {args.table} ({len(summary)} rows)")
    plot(summary, args.output)


if __name__ == "__main__":
    main()
