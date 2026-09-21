#!/usr/bin/env python3
"""Highlight the (Clean, disturbance) pairs where a disturbance changes the
simulated policy comparison.

For every (scene, task, disturbance), the sim pi_1-vs-pi_2 comparison is
tested with a two-sided Fisher exact test (alpha = 0.05) under Clean and
under the disturbance. Three figures are written:

    significance_lost.png     significant under Clean, not under the disturbance
    significance_gained.png   not significant under Clean, significant under the disturbance
    rank_reversed.png         the sign of (pi_1 - pi_2) flips

Inputs are the same CSVs the other success-rate figures use
(results/data/success_rate_overall/<scene>.csv for Clean sim,
results/data/success_rate_disturbances/<scene>_<task>.csv), so nothing extra
needs to be supplied. A category with no pairs writes no figure.
"""

import argparse
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from style import (
    ERROR_BAR_COLOR,
    POLICY_COLORS,
    RIG_NAMES,
    apply_icra_style,
    fisher_two_sided,
    p_label,
    savefig,
    style_axes,
    wilson_interval,
)

RESULTS = Path(__file__).resolve().parents[1]
OVERALL_DIR = RESULTS / "data" / "success_rate_overall"
DISTURBANCES_DIR = RESULTS / "data" / "success_rate_disturbances"
DEFAULT_FIGURE_DIR = RESULTS / "figures" / "success_rate_disturbances_highlights"

ALPHA = 0.05
NCOLS = 4
TITLES = {
    "rank_reversed": "Policy ranking reversed",
    "significance_lost": "From significant to not significant",
    "significance_gained": "From not significant to significant",
}


def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def counts(rows):
    return {r["policy"]: (int(r["successes"]), int(r["num_trials"])) for r in rows}


def collect_pairs():
    pairs = {key: [] for key in TITLES}
    for csv_path in sorted(DISTURBANCES_DIR.glob("*.csv")):
        scene, task = csv_path.stem.split("_", 1)
        overall = OVERALL_DIR / f"{scene}.csv"
        if not overall.exists():
            continue
        clean = counts(r for r in load_rows(overall) if r["task"] == task and r["domain"] == "sim")
        rows = [r for r in load_rows(csv_path) if r["domain"] == "sim"]
        policies = list(clean)
        if len(policies) != 2:
            continue
        a, b = policies
        p_clean = fisher_two_sided(*clean[a], *clean[b])
        diff_clean = clean[a][0] / clean[a][1] - clean[b][0] / clean[b][1]
        for disturbance in dict.fromkeys(r["disturbance"] for r in rows):
            dist = counts(r for r in rows if r["disturbance"] == disturbance)
            if a not in dist or b not in dist:
                continue
            p_dist = fisher_two_sided(*dist[a], *dist[b])
            diff_dist = dist[a][0] / dist[a][1] - dist[b][0] / dist[b][1]
            pair = {"scene": scene, "task": task, "disturbance": disturbance,
                    "policies": policies, "clean": clean, "dist": dist,
                    "p_clean": p_clean, "p_dist": p_dist}
            if p_clean < ALPHA <= p_dist:
                pairs["significance_lost"].append(pair)
            if p_dist < ALPHA <= p_clean:
                pairs["significance_gained"].append(pair)
            if diff_clean * diff_dist < 0:
                pairs["rank_reversed"].append(pair)
    return pairs


def draw_panel(ax, pair):
    width = 0.36
    for g, (key, p) in enumerate((("clean", pair["p_clean"]), ("dist", pair["p_dist"]))):
        tops = []
        for j, policy in enumerate(pair["policies"]):
            k, n = pair[key][policy]
            h = 100 * k / n
            lo, hi = wilson_interval(k, n)
            x = g + (j - 0.5) * width
            ax.bar(x, h, width, color=POLICY_COLORS[j], edgecolor="white", linewidth=0.4, zorder=2)
            ax.errorbar([x], [h], yerr=[[max(0.0, h - 100 * lo)], [max(0.0, 100 * hi - h)]],
                        fmt="none", ecolor=ERROR_BAR_COLOR, elinewidth=0.6, capsize=1.8,
                        capthick=0.6, zorder=3)
            tops.append(100 * hi)
        y = min(112, max(tops) + 6)
        ax.plot([g - width * 0.6, g - width * 0.6, g + width * 0.6, g + width * 0.6],
                [y - 2, y, y, y - 2], color=ERROR_BAR_COLOR, lw=0.55)
        ax.text(g, y + 1.5, p_label(p), ha="center", va="bottom", fontsize=5.6,
                fontweight="bold" if p < ALPHA else "normal")
    ax.set_xticks([0, 1], ["Clean", pair["disturbance"].replace("_remove_", "\nremove ")
                           .replace("pinhole_", "pinhole ")])
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, 128)
    ax.set_yticks([0, 25, 50, 75, 100])
    style_axes(ax)
    ax.tick_params(axis="x", labelsize=6.2)
    ax.set_title(f"{RIG_NAMES.get(pair['scene'], pair['scene'])} / {pair['task']}",
                 loc="left", fontsize=7.4, pad=3)


def plot(key, pairs, output_path):
    apply_icra_style(base_size=7)
    ncols = min(NCOLS, len(pairs))
    nrows = math.ceil(len(pairs) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(1.79 * ncols, 1.85 * nrows + 0.55),
                             sharey=True, squeeze=False)
    top = 1 - 0.55 / (1.85 * nrows + 0.55)
    fig.subplots_adjust(left=0.42 / (1.79 * ncols) + 0.02, right=0.99,
                        bottom=0.30 / (1.85 * nrows + 0.55) + 0.03, top=top,
                        wspace=0.12, hspace=0.62)
    for ax, pair in zip(axes.flat, pairs):
        draw_panel(ax, pair)
    for ax in axes.flat[len(pairs):]:
        ax.set_visible(False)
    for row in axes:
        row[0].set_ylabel("Sim success rate (%)")
    handles = [plt.Rectangle((0, 0), 1, 1, color=POLICY_COLORS[j], label=policy)
               for j, policy in enumerate(pairs[0]["policies"])]
    fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.995, 1.0), ncol=2,
               frameon=False, fontsize=7)
    fig.text(0.01, 1 - 0.13 / (1.85 * nrows + 0.55), f"{TITLES[key]} ({len(pairs)})",
             ha="left", va="top", fontsize=8)
    savefig(fig, output_path)
    print(f"Wrote figure: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure-dir", default=DEFAULT_FIGURE_DIR, type=Path)
    args = parser.parse_args()
    for key, pairs in collect_pairs().items():
        if not pairs:
            print(f"No pairs for {key}; nothing to draw.")
            continue
        plot(key, pairs, args.figure_dir / f"{key}.png")


if __name__ == "__main__":
    main()
