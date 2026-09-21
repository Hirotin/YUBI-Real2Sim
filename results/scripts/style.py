"""Shared plotting style for the results figures.

Matches the house style used by the ICRA 2026 paper's own figure scripts
(icra2026_yubi-real2sim/figs/plots/*.py): DejaVu Serif, thin hairline
spines/gridlines, and the same color roles --

    Real vs. Sim panels (Fig. 1, plot_policy_success.py):
        real = REAL_COLOR (#4a4a4a), sim = SIM_COLOR (#1d4ed8);
        the first policy encountered is drawn at POLICY_ALPHAS[0] (0.42),
        the second at POLICY_ALPHAS[1] (1.0).

    Within-sim policy comparisons under disturbance
    (plot_all_policy_success_significance.py / plot_cup_success_significance.py):
        the first policy is POLICY_COLORS[0] (#2563eb, the shared/generalist
        checkpoint), the second is POLICY_COLORS[1] (#f59e0b, the
        task-specific checkpoint).

    Per-scene panels (Fig. 3, plot_viewcount_quality_nvs.py):
        SCENE_COLORS keyed by scene name (Duo/Flat/G2).
"""

import math

import matplotlib.pyplot as plt

REAL_COLOR = "#4a4a4a"
SIM_COLOR = "#1d4ed8"
POLICY_ALPHAS = (0.42, 1.0)
POLICY_COLORS = ("#2563eb", "#f59e0b")
SCENE_COLORS = {"Duo": "#3366b3", "Flat": "#db7326", "G2": "#40945a"}
RIG_NAMES = {"Duo": "FR3 Duo", "Flat": "FR3 Flat", "G2": "G2"}

GRID_COLOR = "#DDE2E7"
SPINE_COLOR = "#666666"
ERROR_BAR_COLOR = "#333333"
INK_PRIMARY = "#1a1a1a"
INK_SECONDARY = "#444444"


def apply_icra_style(base_size=8):
    """Match the rcParams every figure script in the paper repo sets."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": base_size,
            "mathtext.fontset": "dejavuserif",
            "axes.labelsize": base_size + 0.5,
            "xtick.labelsize": base_size,
            "ytick.labelsize": base_size - 0.5,
            "axes.linewidth": 0.65,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def wilson_interval(successes, trials, z=1.959963984540054):
    """Two-sided 95% Wilson binomial interval, as used throughout the paper's
    own significance plots."""
    if trials <= 0:
        return 0.0, 0.0
    p = successes / trials
    den = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / den
    half = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / den
    return max(0.0, center - half), min(1.0, center + half)


def style_axes(ax, ylabel=None, grid_axis="y"):
    ax.grid(axis=grid_axis, color=GRID_COLOR, linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["bottom"].set_color(SPINE_COLOR)
    ax.spines["left"].set_color(SPINE_COLOR)
    ax.tick_params(axis="x", length=0, pad=4)
    ax.tick_params(axis="y", length=3, color=SPINE_COLOR)
    if ylabel:
        ax.set_ylabel(ylabel)


def savefig(fig, output_png_path):
    """Write both the PNG (for the README) and a vector PDF (for the paper),
    mirroring how every figure script in the paper repo saves its output."""
    output_png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_png_path.with_suffix(".pdf"),
        metadata={"Title": output_png_path.stem, "Author": "", "CreationDate": None, "ModDate": None},
    )
    fig.savefig(output_png_path, dpi=300)
    plt.close(fig)


def fisher_two_sided(a, n1, b, n2):
    """Two-sided Fisher exact p for [[a, n1-a], [b, n2-b]], as in the paper's
    significance plots."""
    total = a + b
    lo, hi = max(0, total - n2), min(n1, total)

    def prob(x):
        return math.comb(n1, x) * math.comb(n2, total - x) / math.comb(n1 + n2, total)

    observed = prob(a)
    return min(1.0, sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= observed + 1e-15))


def p_label(p):
    if p < 0.001:
        return "p<.001 ***"
    if p < 0.01:
        return f"p={p:.3f} **"
    if p < 0.05:
        return f"p={p:.3f} *"
    return f"p={p:.3f} n.s."
