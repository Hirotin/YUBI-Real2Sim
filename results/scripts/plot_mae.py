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
from matplotlib.lines import Line2D

from style import REAL_COLOR, RIG_NAMES, apply_icra_style, savefig, style_axes

RESULTS = Path(__file__).resolve().parents[1]
OVERALL_DIR = RESULTS / "data" / "success_rate_overall"
DISTURBANCES_DIR = RESULTS / "data" / "success_rate_disturbances"
DEFAULT_TABLE = RESULTS / "data" / "mae.csv"
DEFAULT_OUTPUT = RESULTS / "figures" / "mae.png"

# disturbance types, by condition-name prefix; Clean/artifact/view-reduction
# keep the colors the paper's counterfactual figure gives them
FAMILIES = [("Clean", "Clean"), ("hole", "Hole"), ("float", "Floater"), ("tablegeo", "Warping"),
            ("fov", "View reduction"), ("pinhole", "View reduction")]
FAMILY_COLORS = {"Clean": "#1d4ed8", "Hole": "#b91c1c", "Floater": "#d97706",
                 "Warping": "#7c3aed", "View reduction": "#4a4a4a"}
MARKERS = ["o", "s", "^", "D", "v"]


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


def family(condition):
    for prefix, name in FAMILIES:
        if condition.startswith(prefix):
            return name
    return "Other"


def plot(summary, output_path):
    """Conditions run down the page, MAE runs across it. Each condition is one
    line spanning its scenes, colored by disturbance type; each scene has its
    own marker and a faint trace so it can be followed down the conditions."""
    conditions = list(dict.fromkeys(r["condition"] for r in summary))
    scenes = list(dict.fromkeys(r["scene"] for r in summary))
    lookup = {(r["condition"], r["scene"]): r["mae_pp"] for r in summary}

    # one slot per condition, with a gap between disturbance types
    slots, y, last = {}, 0.0, None
    for condition in conditions:
        if last is not None and family(condition) != last:
            y += 0.6
        slots[condition] = y
        last, y = family(condition), y + 1

    apply_icra_style()
    fig, ax = plt.subplots(figsize=(5.2, 3.9))
    fig.subplots_adjust(left=0.245, right=0.975, bottom=0.115, top=0.84)

    for i, scene in enumerate(scenes):
        points = [(lookup[(c, scene)], slots[c]) for c in conditions if (c, scene) in lookup]
        ax.plot(*zip(*points), color="#9aa0a6", linewidth=0.6, alpha=0.7, zorder=1)
    for condition in conditions:
        colour = FAMILY_COLORS.get(family(condition), REAL_COLOR)
        values = [lookup[(condition, s)] for s in scenes if (condition, s) in lookup]
        ax.plot([min(values), max(values)], [slots[condition]] * 2, color=colour, linewidth=1.4,
                alpha=0.55, zorder=2, solid_capstyle="butt")
        for i, scene in enumerate(scenes):
            if (condition, scene) in lookup:
                ax.plot([lookup[(condition, scene)]], [slots[condition]], MARKERS[i % len(MARKERS)],
                        color=colour, markersize=5.6, markeredgecolor="white",
                        markeredgewidth=0.5, zorder=3)

    ax.set_yticks([slots[c] for c in conditions],
                  [c.replace("_remove_", " ").replace("pinhole_", "pinhole ") for c in conditions])
    ax.set_ylim(max(slots.values()) + 0.8, -0.8)
    ax.set_xlim(0, max(r["mae_pp"] for r in summary) * 1.06)
    ax.set_xlabel("Sim-to-real MAE (pp) \u2193", labelpad=3)
    style_axes(ax, grid_axis="x")
    ax.tick_params(axis="y", length=0, pad=4)
    ax.tick_params(axis="x", length=3, color="#666666")

    scene_handles = [Line2D([], [], color="#4a4a4a", marker=MARKERS[i % len(MARKERS)],
                            linestyle="None", markersize=5.2, label=RIG_NAMES.get(s, s))
                     for i, s in enumerate(scenes)]
    present = list(dict.fromkeys(family(c) for c in conditions))
    family_handles = [Line2D([], [], color=FAMILY_COLORS.get(f, REAL_COLOR), linewidth=2.2, label=f)
                      for f in present]
    fig.legend(handles=scene_handles, loc="upper center", bbox_to_anchor=(0.6, 1.0),
               ncol=len(scene_handles), frameon=False, fontsize=8, handletextpad=0.3,
               columnspacing=1.4)
    fig.legend(handles=family_handles, loc="upper center", bbox_to_anchor=(0.6, 0.94),
               ncol=len(family_handles), frameon=False, fontsize=7.4, handlelength=1.3,
               handletextpad=0.4, columnspacing=1.1)
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
