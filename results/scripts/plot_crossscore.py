#!/usr/bin/env python3
"""Plot CrossScore per scene and condition, on the held-out Test views and on
the OBS views, in the same line form as the MAE and NVS figures.

CSV schema (results/data/crossscore.csv):
    condition,scene,CrossScore_Test,CrossScore_Test_sd,CrossScore_OBS,CrossScore_OBS_R,CrossScore_OBS_L,test_views

The values are also written into the README as a table, between the
<!-- crossscore-table:start --> and <!-- crossscore-table:end --> markers.

If the CSV has no data rows yet, nothing is written.
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from style import (
    RIG_NAMES,
    apply_icra_style,
    condition_legends,
    draw_condition_traces,
    savefig,
    style_axes,
)

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "data" / "crossscore.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "figures" / "crossscore_lines.png"
README = Path(__file__).resolve().parents[2] / "README.md"

PANELS = [("CrossScore_Test", "CrossScore, Test views ↑"), ("CrossScore_OBS", "CrossScore, OBS views ↑")]


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def plot(rows, output_path):
    conditions = list(dict.fromkeys(r["condition"] for r in rows))
    scenes = list(dict.fromkeys(r["scene"] for r in rows))

    apply_icra_style()
    height = 1.9 * len(PANELS) + 0.85
    fig, axes = plt.subplots(len(PANELS), 1, figsize=(5.2, height), sharex=True)
    fig.subplots_adjust(left=0.115, right=0.985, bottom=0.35 / height, top=1 - 0.75 / height,
                        hspace=0.16)
    low = min(float(r[k]) for r in rows for k, _ in PANELS)
    high = max(float(r[k]) for r in rows for k, _ in PANELS)
    pad = 0.08 * (high - low)
    for ax, (column, label) in zip(axes, PANELS):
        lookup = {(r["condition"], r["scene"]): float(r[column]) for r in rows}
        draw_condition_traces(ax, conditions, scenes, lookup)
        ax.set_ylim(low - pad, high + pad)
        style_axes(ax, ylabel=label)
    condition_legends(fig, conditions, scenes, y_scene=1.0, y_family=1 - 0.33 / height)
    savefig(fig, output_path)
    print(f"Wrote figure: {output_path}")


def readme_table(rows):
    conditions = list(dict.fromkeys(r["condition"] for r in rows))
    scenes = list(dict.fromkeys(r["scene"] for r in rows))
    lookup = {(r["condition"], r["scene"]): r for r in rows}
    head = ["Condition"] + [f"{view} {RIG_NAMES.get(s, s)}" for view in ("Test", "OBS") for s in scenes]
    lines = ["| " + " | ".join(head) + " |", "|---|" + "---:|" * (len(head) - 1)]
    for c in conditions:
        cells = []
        for column in ("CrossScore_Test", "CrossScore_OBS"):
            cells += [f"{float(lookup[(c, s)][column]):.3f}" if (c, s) in lookup else "" for s in scenes]
        lines.append(f"| {c} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def update_readme(rows):
    text = README.read_text()
    start, end = "<!-- crossscore-table:start -->", "<!-- crossscore-table:end -->"
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
