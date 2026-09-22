#!/usr/bin/env python3
"""Supplementary analysis of Table II: constant baselines, label layout, and
the Tape error decomposition, all recomputed from the out-of-fold prediction
log (results/data/reliability_predictions.csv).

Writes
    results/figures/reliability_labels.png   Fig. S1: (a) ranking-disagreement
        labels per scene/task/variant, (b) Tape class support per held-out scene
and fills two README tables between markers:
    <!-- table-s1:start --> ... <!-- table-s1:end -->   accuracy incl. constant predictors
    <!-- table-s2:start --> ... <!-- table-s2:end -->   Tape TP/FN/FP/TN and pooled balanced accuracy

Nothing is refit: predictions are read as logged, constants follow from the labels.
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from style import INK_SECONDARY, RIG_NAMES, SPINE_COLOR, apply_icra_style, savefig

RESULTS = Path(__file__).resolve().parents[1]
DEFAULT_CSV = RESULTS / "data" / "reliability_predictions.csv"
EXTRA_CSV = RESULTS / "data" / "reliability_predictions_crossscore.csv"
DEFAULT_OUTPUT = RESULTS / "figures" / "reliability_labels.png"
README = RESULTS.parent / "README.md"

SCENES = ["Duo", "Flat", "G2"]
TASKS = ["Cup", "Tape", "Pen"]
VARIANTS = [("Hole54", "Hole 54°"), ("Hole90", "Hole 90°"), ("CentralPinhole", "Central\npinhole"),
            ("Contiguous30", "Adjacent\n30%"), ("Random30", "Random\n30%")]
METHODS = [("NVS-SQA Test", "NVS-SQA / Test"), ("NVS-SQA OBS", "NVS-SQA / OBS"),
           ("PSNR Test", "PSNR / Test"), ("SSIM Test", "SSIM / Test"), ("LPIPS Test", "LPIPS / Test")]
# computed here with the same protocol, not part of Table II
EXTRA_METHODS = [("CrossScore Test", "CrossScore / Test \u2020"),
                 ("CrossScore OBS-TableII", "CrossScore / OBS \u2020")]
DISAGREE = "#b91c1c"


def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def labels_of(rows):
    return {(r["target"], r["heldout_scene"], r["variant"]): int(r["label"]) for r in rows}


def table_s1(rows):
    labels = labels_of(rows)
    targets = TASKS + ["All-three"]
    per_target = {t: [v for (tt, _, _), v in labels.items() if tt == t] for t in targets}

    def line(name, correct):
        total = sum(correct[t] for t in TASKS)
        n = sum(len(per_target[t]) for t in TASKS)
        cells = [f"{correct[t]}/{len(per_target[t])}" for t in TASKS]
        cells.append(f"{total}/{n} ({100 * total / n:.1f}%)")
        cells.append(f"{correct['All-three']}/{len(per_target['All-three'])}")
        return f"| {name} | " + " | ".join(cells) + " |"

    out = ["| Method / view | Cup | Tape | Pen | Total | All-three |", "|---|---:|---:|---:|---:|---:|"]
    out.append(line("Always reliable ($\\widehat{H}=0$)", {t: per_target[t].count(0) for t in targets}))
    out.append(line("Always unreliable ($\\widehat{H}=1$)", {t: per_target[t].count(1) for t in targets}))
    for key, name in METHODS + EXTRA_METHODS:
        if not any(r["method"] == key for r in rows):
            continue
        correct = {t: sum(int(r["correct"]) for r in rows if r["method"] == key and r["target"] == t)
                   for t in targets}
        out.append(line(name, correct))
    return "\n".join(out)


def table_s2(rows):
    tape = {k: v for k, v in labels_of(rows).items() if k[0] == "Tape"}
    pos, neg = list(tape.values()).count(1), list(tape.values()).count(0)

    def line(name, tp, fn, fp, tn):
        ba = 0.5 * (tp / (tp + fn) + tn / (tn + fp))
        return f"| {name} | {tp} | {fn} | {fp} | {tn} | {100 * ba:.1f}% |"

    out = ["| Method / view | TP ↑ | FN ↓ | FP ↓ | TN ↑ | Balanced accuracy ↑ |",
           "|---|---:|---:|---:|---:|---:|"]
    out.append(line("Always reliable", 0, pos, 0, neg))
    out.append(line("Always unreliable", pos, 0, neg, 0))
    for key, name in METHODS + EXTRA_METHODS:
        sel = [(int(r["label"]), int(r["prediction"])) for r in rows
               if r["method"] == key and r["target"] == "Tape"]
        if not sel:
            continue
        out.append(line(name, sel.count((1, 1)), sel.count((1, 0)), sel.count((0, 1)), sel.count((0, 0))))
    return "\n".join(out)


def fill(text, marker, body):
    start, end = f"<!-- {marker}:start -->", f"<!-- {marker}:end -->"
    if start not in text or end not in text:
        print(f"No {start} marker in {README}; table not written.")
        return text
    a, b = text.index(start) + len(start), text.index(end)
    return text[:a] + "\n" + body + "\n" + text[b:]


def plot(rows, output_path):
    labels = labels_of(rows)
    tape_fit = {r["heldout_scene"]: r["fit_status"] for r in rows if r["target"] == "Tape"}

    apply_icra_style()
    fig = plt.figure(figsize=(7.16, 3.7))
    ax = fig.add_axes([0.125, 0.04, 0.36, 0.7])
    bx = fig.add_axes([0.55, 0.04, 0.44, 0.7])

    # (a) label matrix
    order = [(s, t) for s in SCENES for t in TASKS]
    for i, (scene, task) in enumerate(order):
        for j, (variant, _) in enumerate(VARIANTS):
            h = labels[(task, scene, variant)]
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=DISAGREE if h else "white", alpha=0.85 if h else 1,
                                   edgecolor="#c9cdd2", linewidth=0.5))
            ax.text(j + 0.5, i + 0.5, str(h), ha="center", va="center", fontsize=8,
                    color="white" if h else "#777777", fontweight="bold" if h else "normal")
    for k in range(1, len(SCENES)):
        ax.axhline(k * len(TASKS), color=SPINE_COLOR, linewidth=1.1)
    ax.set_xlim(0, len(VARIANTS))
    ax.set_ylim(len(order), 0)
    ax.set_xticks([j + 0.5 for j in range(len(VARIANTS))], [name for _, name in VARIANTS], fontsize=7)
    ax.xaxis.tick_top()
    ax.set_yticks([i + 0.5 for i in range(len(order))],
                  [f"{RIG_NAMES.get(s, s)} / {t}" for s, t in order], fontsize=7.4)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)
    fig.text(0.01, 0.985, "(a) Ranking-disagreement labels", fontsize=8.5, ha="left", va="top")
    fig.text(0.01, 0.925, "0: observed ranking agreement,  1: disagreement", fontsize=7,
             ha="left", va="top", color=INK_SECONDARY)

    # (b) Tape class support per held-out scene
    bx.set_xlim(0, 10)
    bx.set_ylim(0, 10)
    bx.axis("off")
    fig.text(0.55, 0.985, "(b) Tape class support per held-out scene", fontsize=8.5, ha="left", va="top")
    fig.text(0.55, 0.925, "R: ranking agreement,  U: disagreement", fontsize=7, ha="left", va="top",
             color=INK_SECONDARY)
    for x, head in ((0.1, "Held out"), (2.3, "Train R / U"), (4.9, "Test R / U"), (7.2, "Prediction rule")):
        bx.text(x, 9.4, head, fontsize=7.4, color=INK_SECONDARY, va="center")
    bx.plot([0, 10], [8.95, 8.95], color=SPINE_COLOR, linewidth=0.6)
    single = None
    for i, scene in enumerate(SCENES):
        y = 8.2 - 1.25 * i
        train = [labels[("Tape", s, v)] for s in SCENES if s != scene for v, _ in VARIANTS]
        test = [labels[("Tape", scene, v)] for v, _ in VARIANTS]
        constant = tape_fit[scene] == "training_class_constant"
        weight = "bold" if constant else "normal"
        bx.text(0.1, y, RIG_NAMES.get(scene, scene), fontsize=8, va="center", fontweight=weight)
        bx.text(2.3, y, f"{train.count(0)} / {train.count(1)}", fontsize=8, va="center", fontweight=weight)
        bx.annotate("", xy=(4.7, y), xytext=(3.9, y), arrowprops=dict(arrowstyle="->", lw=0.7, color=SPINE_COLOR))
        bx.text(4.9, y, f"{test.count(0)} / {test.count(1)}", fontsize=8, va="center", fontweight=weight)
        bx.text(7.2, y, "single class:\nalways R" if constant else "threshold from\nboth classes",
                fontsize=6.8, va="center", fontweight=weight, color=DISAGREE if constant else "#1a1a1a")
        if constant:
            single = scene
            bx.add_patch(Rectangle((-0.1, y - 0.58), 10.1, 1.16, fill=False, edgecolor=DISAGREE, linewidth=0.9))
    if single:
        truth = [labels[("Tape", single, v)] for v, _ in VARIANTS]
        preds = {tuple(int(r["prediction"]) for v, _ in VARIANTS for r in rows
                       if r["method"] == key and r["target"] == "Tape"
                       and r["heldout_scene"] == single and r["variant"] == v)
                 for key, _ in METHODS + EXTRA_METHODS if any(r["method"] == key for r in rows)}
        pred = list(next(iter(preds))) if len(preds) == 1 else None
        bx.text(0.1, 3.6, f"{RIG_NAMES.get(single, single)} labels", fontsize=7.6, va="center")
        bx.text(5.6, 3.6, str(truth), fontsize=8, va="center", family="DejaVu Sans Mono")
        bx.text(0.1, 2.7, "Predictions, all methods" if pred else "Predictions differ by method",
                fontsize=7.6, va="center")
        if pred:
            bx.text(5.6, 2.7, str(pred), fontsize=8, va="center", family="DejaVu Sans Mono")
            hits = sum(1 for t, p in zip(truth, pred) if t == 1 and p == 1)
            bx.text(0.1, 1.8, "Disagreements detected", fontsize=7.6, va="center")
            bx.text(5.6, 1.8, f"{hits}/{truth.count(1)}", fontsize=8, va="center", color=DISAGREE,
                    fontweight="bold")
        bx.text(0.1, 0.6, "Test labels are shown for retrospective analysis only;\nthey are not used for fitting.",
                fontsize=6.2, va="center", color=INK_SECONDARY)

    savefig(fig, output_path)
    print(f"Wrote figure: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", default=DEFAULT_CSV, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    args = parser.parse_args()

    if not args.csv.exists() or not load_rows(args.csv):
        print(f"No prediction log at {args.csv}; nothing to do.")
        return
    rows = load_rows(args.csv)
    if EXTRA_CSV.exists():
        rows += load_rows(EXTRA_CSV)
    plot(rows, args.output)
    text = fill(fill(README.read_text(), "table-s1", table_s1(rows)), "table-s2", table_s2(rows))
    README.write_text(text)
    print(f"Updated Table S1 / S2 in {README}")


if __name__ == "__main__":
    main()
