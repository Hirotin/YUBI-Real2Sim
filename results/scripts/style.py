"""Shared plotting style for the results figures.

Palette and chart chrome follow a validated categorical order (fixed hue
sequence, never re-cycled) so that colors stay consistent and
colorblind-distinguishable across every figure in this directory.
"""

import matplotlib.pyplot as plt

# Fixed categorical hue order (light-surface variant). Assign colors to
# series in first-seen order -- never re-sort or cycle per chart.
CATEGORICAL = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

SEQUENTIAL_BLUE = "#2a78d6"

SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

FONT_FAMILY = "sans-serif"


def assign_colors(labels):
    """Map each distinct label to a fixed categorical color, in the order
    the labels were first encountered."""
    seen = []
    for label in labels:
        if label not in seen:
            seen.append(label)
    if len(seen) > len(CATEGORICAL):
        raise ValueError(
            f"{len(seen)} series requested but only {len(CATEGORICAL)} "
            "categorical colors are defined; fold extra series into "
            "'Other' or split into small multiples."
        )
    return {label: CATEGORICAL[i] for i, label in enumerate(seen)}


def new_figure(figsize=(7, 4.5)):
    fig, ax = plt.subplots(figsize=figsize, dpi=200)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    return fig, ax


def style_axes(ax, ylabel=None, title=None):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.yaxis.grid(True, color=GRIDLINE, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", colors=INK_SECONDARY, length=0)
    ax.tick_params(axis="y", colors=INK_MUTED, length=0)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK_SECONDARY, fontsize=10)
    if title:
        ax.set_title(title, color=INK_PRIMARY, fontsize=12, pad=12, loc="left")


def bar_value_labels(ax, bars, fmt="{:.1f}"):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            fmt.format(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            color=INK_SECONDARY,
        )


def legend(ax, **kwargs):
    leg = ax.legend(
        frameon=False,
        loc=kwargs.pop("loc", "upper center"),
        bbox_to_anchor=kwargs.pop("bbox_to_anchor", (0.5, 1.18)),
        ncol=kwargs.pop("ncol", 4),
        fontsize=9,
        labelcolor=INK_SECONDARY,
        **kwargs,
    )
    return leg


def savefig(fig, output_path):
    fig.tight_layout()
    fig.savefig(output_path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
