#!/usr/bin/env python3
"""Plot novel-view synthesis quality on the test set (PSNR, SSIM, LPIPS) per
scene and condition.

CSV schema (results/data/novel_view_metrics.csv):
    condition,scene,views,PSNR,SSIM,LPIPS

Each metric lives on its own scale, so each gets its own panel rather than a
shared/dual axis; the panels share the condition axis. Scenes use the same
palette as the paper's Fig. 3 (Duo/Flat/G2).

The same values are written into the README as a table, between the
<!-- nvs-table:start --> and <!-- nvs-table:end --> markers.

If the CSV has no data rows yet, nothing is written.
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from style import REAL_COLOR, RIG_NAMES, SCENE_COLORS, apply_icra_style, savefig, style_axes

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "data" / "novel_view_metrics.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "figures" / "nvs_metrics.png"

README = Path(__file__).resolve().parents[2] / "README.md"

METRICS = [("PSNR", "PSNR (dB) ↑", "{:.1f}"), ("SSIM", "SSIM ↑", "{:.2f}"),
           ("LPIPS", "LPIPS ↓", "{:.2f}")]


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def plot(rows, output_path):
    conditions = list(dict.fromkeys(r["condition"] for r in rows))
    scenes = list(dict.fromkeys(r["scene"] for r in rows))
    lookup = {(r["condition"], r["scene"]): r for r in rows}

    apply_icra_style()
    fig, axes = plt.subplots(len(METRICS), 1, figsize=(7.16, 1.75 * len(METRICS) + 0.9), sharex=True)
    fig.subplots_adjust(left=0.085, right=0.992, bottom=0.13, top=0.95, hspace=0.22)
    width = 0.8 / len(scenes)
    for ax, (metric, label, fmt) in zip(axes, METRICS):
        top = 0.0
        for i, scene in enumerate(scenes):
            present = [(j, float(lookup[(c, scene)][metric])) for j, c in enumerate(conditions)
                       if (c, scene) in lookup]
            xs = [j - 0.4 + width / 2 + i * width for j, _ in present]
            ys = [y for _, y in present]
            ax.bar(xs, ys, width, color=SCENE_COLORS.get(scene, REAL_COLOR), edgecolor="white",
                   linewidth=0.4, label=RIG_NAMES.get(scene, scene), zorder=2)
            top = max([top] + ys)
            for x, y in zip(xs, ys):
                ax.annotate(fmt.format(y), (x, y), xytext=(0, 1.5), textcoords="offset points",
                            ha="center", va="bottom", fontsize=5.4, rotation=90)
        ax.set_ylim(0, top * 1.28)
        ax.set_xlim(-0.55, len(conditions) - 0.45)
        style_axes(ax, ylabel=label)
    labels = [c.replace("_remove_", " ").replace("pinhole_", "pinhole ") for c in conditions]
    axes[-1].set_xticks(range(len(conditions)), labels, rotation=28, ha="right")
    handles, names = axes[0].get_legend_handles_labels()
    fig.legend(handles, names, loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=len(scenes),
               frameon=False, fontsize=8.5, handlelength=1.5, columnspacing=1.6)
    savefig(fig, output_path)
    print(f"Wrote figure: {output_path}")


def readme_table(rows):
    conditions = list(dict.fromkeys(r["condition"] for r in rows))
    scenes = list(dict.fromkeys(r["scene"] for r in rows))
    lookup = {(r["condition"], r["scene"]): r for r in rows}
    head = ["Condition"] + [f"{m} {RIG_NAMES.get(s, s)}" for m, _, _ in METRICS for s in scenes]
    lines = ["| " + " | ".join(head) + " |", "|---|" + "---:|" * (len(head) - 1)]
    for c in conditions:
        cells = [f"{float(lookup[(c, s)][m]):.{2 if m == 'PSNR' else 3}f}" if (c, s) in lookup else ""
                 for m, _, _ in METRICS for s in scenes]
        lines.append(f"| {c} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def update_readme(rows):
    text = README.read_text()
    start, end = "<!-- nvs-table:start -->", "<!-- nvs-table:end -->"
    if start not in text or end not in text:
        print(f"No {start} marker in {README}; table not written.")
        return
    a, b = text.index(start) + len(start), text.index(end)
    README.write_text(text[:a] + "\n" + readme_table(rows) + "\n" + text[b:])
    print(f"Updated table in {README}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default=DEFAULT_CSV, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    args = parser.parse_args()

    rows = load_rows(args.csv)
    if not rows:
        print(f"No data rows in {args.csv}; nothing to do.")
        return
    plot(rows, args.output)
    update_readme(rows)


if __name__ == "__main__":
    main()
