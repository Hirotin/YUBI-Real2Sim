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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

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


# disturbance types, by condition-name prefix; Clean/artifact/view-reduction
# keep the colors the paper's counterfactual figure gives them
FAMILIES = [("Clean", "Clean"), ("hole", "Hole"), ("float", "Floater"), ("tablegeo", "Warping"),
            ("fov", "View reduction"), ("pinhole", "View reduction")]
FAMILY_COLORS = {"Clean": "#1d4ed8", "Hole": "#b91c1c", "Floater": "#d97706",
                 "Warping": "#7c3aed", "View reduction": "#4a4a4a"}
MARKERS = ["o", "s", "^", "D", "v"]
# ticks that would otherwise collide; anything not listed keeps its derived label
SHORT_LABELS = {"hole_54": "54\u00b0", "hole_90": "90\u00b0", "float_low8": "low",
                "float_mid8": "mid", "float_high8": "high", "fov_center": "center",
                "pinhole_adjacent_remove_30": "adj.", "pinhole_random_remove_30": "rand."}


def family(condition):
    for prefix, name in FAMILIES:
        if condition.startswith(prefix):
            return name
    return "Other"


def short_label(condition):
    """The disturbance type is already in the color legend, so the tick only
    carries what tells conditions of one type apart."""
    for prefix, _ in FAMILIES:
        if condition.startswith(prefix):
            rest = condition[len(prefix):].strip("_").replace("_remove_", " ").replace("_", " ")
            return SHORT_LABELS.get(condition, rest)
    return condition


def draw_condition_traces(ax, conditions, scenes, lookup):
    """Conditions run across, the value runs up. Markers are colored by
    disturbance type and shaped by scene; a faint trace follows each scene
    across the conditions, and each scene's Clean value is carried across as a
    dotted reference so every disturbed point reads as a difference from it.

    lookup maps (condition, scene) -> value.
    """
    # one slot per condition, with a gap between disturbance types
    slots, x, last = {}, 0.0, None
    for condition in conditions:
        if last is not None and family(condition) != last:
            x += 0.6
        slots[condition] = x
        last, x = family(condition), x + 1

    reference = next((c for c in conditions if family(c) == "Clean"), None)
    for scene in scenes:
        if reference and (reference, scene) in lookup:
            ax.axhline(lookup[(reference, scene)], color=FAMILY_COLORS["Clean"], linewidth=0.7,
                       linestyle=(0, (2, 2)), alpha=0.6, zorder=1)
    for scene in scenes:
        points = [(slots[c], lookup[(c, scene)]) for c in conditions if (c, scene) in lookup]
        ax.plot(*zip(*points), color="#9aa0a6", linewidth=0.6, alpha=0.7, zorder=1)
    for condition in conditions:
        colour = FAMILY_COLORS.get(family(condition), REAL_COLOR)
        for i, scene in enumerate(scenes):
            if (condition, scene) in lookup:
                ax.plot([slots[condition]], [lookup[(condition, scene)]], MARKERS[i % len(MARKERS)],
                        color=colour, markersize=5.6, markeredgecolor="white",
                        markeredgewidth=0.5, zorder=3)
    ax.set_xticks([slots[c] for c in conditions], [short_label(c) for c in conditions])
    ax.set_xlim(-0.7, max(slots.values()) + 0.7)


def condition_legends(fig, conditions, scenes, x=0.55, y_scene=1.0, y_family=0.93):
    scene_handles = [Line2D([], [], color="#4a4a4a", marker=MARKERS[i % len(MARKERS)],
                            linestyle="None", markersize=5.2, label=RIG_NAMES.get(s, s))
                     for i, s in enumerate(scenes)]
    present = list(dict.fromkeys(family(c) for c in conditions))
    family_handles = [Patch(facecolor=FAMILY_COLORS.get(f, REAL_COLOR), label=f) for f in present]
    fig.legend(handles=scene_handles, loc="upper center", bbox_to_anchor=(x, y_scene),
               ncol=len(scene_handles), frameon=False, fontsize=8, handletextpad=0.3,
               columnspacing=1.4)
    fig.legend(handles=family_handles, loc="upper center", bbox_to_anchor=(x, y_family),
               ncol=len(family_handles), frameon=False, fontsize=7.4, handlelength=1.3,
               handletextpad=0.4, columnspacing=1.1)
