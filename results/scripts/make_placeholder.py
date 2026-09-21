#!/usr/bin/env python3
"""Generate a placeholder figure for a results chart that has no data yet.

Used once per figure to seed results/figures/*.png before the corresponding
CSV in results/data/ has been filled in. The real plot_*.py script for that
figure overwrites the placeholder in place once the CSV has data.

Only covers the still-single-CSV figures (reconstruction_metrics,
novel_view_metrics). success_rate_overall/ and success_rate_disturbances/
are glob-based directories of per-scene (or per-scene/task) CSVs -- an empty
directory there just means the corresponding plot_*.py script has nothing to
draw yet, so no placeholder image is needed.
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from style import BASELINE, INK_MUTED, INK_SECONDARY, SURFACE


def make_placeholder(title, csv_path, output_path, figsize=(7, 4.5)):
    fig, ax = plt.subplots(figsize=figsize, dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.add_patch(
        plt.Rectangle(
            (0.02, 0.02),
            0.96,
            0.96,
            transform=ax.transAxes,
            fill=False,
            edgecolor=BASELINE,
            linewidth=1.5,
            linestyle=(0, (6, 4)),
        )
    )
    ax.text(
        0.5,
        0.58,
        title,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=13,
        color=INK_SECONDARY,
    )
    ax.text(
        0.5,
        0.42,
        f"Add data to {csv_path} and re-run this figure's plot script",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=9,
        color=INK_MUTED,
    )

    fig.tight_layout()
    fig.savefig(output_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote placeholder: {output_path}")


PLACEHOLDERS = [
    (
        "Reconstruction Quality (MAE / CrossScore)",
        "results/data/reconstruction_metrics.csv",
        "results/figures/reconstruction_metrics.png",
    ),
    (
        "Novel View Synthesis Quality (PSNR / SSIM / LPIPS)",
        "results/data/novel_view_metrics.csv",
        "results/figures/novel_view_metrics.png",
    ),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[2],
        type=Path,
        help="Repository root (default: auto-detected)",
    )
    args = parser.parse_args()

    for title, csv_rel, out_rel in PLACEHOLDERS:
        make_placeholder(title, csv_rel, args.repo_root / out_rel)


if __name__ == "__main__":
    main()
