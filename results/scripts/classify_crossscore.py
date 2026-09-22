#!/usr/bin/env python3
"""Run the Table II reliability classifier on CrossScore.

Same protocol as the paper's per-task threshold classifier
(icra2026_yubi-real2sim/docs/experiments/all_task_classification/analyze.py,
reused unchanged by main_test_baselines_20260917/analyze.py for Table II):
for each target (Cup / Tape / Pen / All-three) and each held-out scene, a
threshold on the quality score is chosen on the other two scenes' 10
conditions to maximize balanced accuracy (ties: higher sensitivity, then the
smaller oriented threshold), and H=1 is predicted when the held-out score
falls below it. If the training labels contain one class, that class is
predicted. CrossScore is higher-is-better (direction = +1).

Inputs
    results/data/crossscore.csv               CrossScore_Test / CrossScore_OBS per scene x condition
    results/data/crossscore_obs_table2.csv    CrossScore on exactly the OBS images Table II's NVS-SQA OBS
                                              used (ABCI-Q cf_eval_final/outputs; the NVS-SQA values of
                                              those images reproduce Table II's OBS scores exactly)
    results/data/reliability_predictions.csv  labels of the 15 matched conditions (Table II log)
Output
    results/data/reliability_predictions_crossscore.csv   same schema as the Table II log,
        methods "CrossScore Test", "CrossScore OBS", "CrossScore OBS-TableII"
"""

import argparse
import csv
import math
from fractions import Fraction
from pathlib import Path

RESULTS = Path(__file__).resolve().parents[1]
SCORES = RESULTS / "data" / "crossscore.csv"
LABELS = RESULTS / "data" / "reliability_predictions.csv"
OBS_TABLE2 = RESULTS / "data" / "crossscore_obs_table2.csv"
OUTPUT = RESULTS / "data" / "reliability_predictions_crossscore.csv"

VARIANT_TO_CONDITION = {"Hole54": "hole_54", "Hole90": "hole_90", "CentralPinhole": "fov_center",
                        "Contiguous30": "pinhole_adjacent_remove_30", "Random30": "pinhole_random_remove_30"}
METHODS = [("CrossScore Test", "CrossScore_Test"), ("CrossScore OBS", "CrossScore_OBS")]
TARGETS = ["Cup", "Tape", "Pen", "All-three"]
SCENES = ["Duo", "Flat", "G2"]


def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def confusion(rows):
    return {k: sum((r["label"], r["prediction"]) == pair for r in rows)
            for k, pair in [("TP", (1, 1)), ("FN", (1, 0)), ("TN", (0, 0)), ("FP", (0, 1))]}


def fit(train, direction):
    labels = {r["label"] for r in train}
    if len(labels) == 1:
        return None, next(iter(labels)), "training_class_constant"
    vals = sorted({direction * r["quality"] for r in train})
    thresholds = [vals[0]] + [(a + b) / 2 for a, b in zip(vals[:-1], vals[1:])] + [math.nextafter(vals[-1], math.inf)]
    choices = []
    for t in thresholds:
        c = confusion([dict(r, prediction=int(direction * r["quality"] < t)) for r in train])
        sens = Fraction(c["TP"], c["TP"] + c["FN"])
        spec = Fraction(c["TN"], c["TN"] + c["FP"])
        choices.append(((sens + spec) / 2, sens, -t, t))
    _, _, _, t = max(choices)
    return t, None, "balanced_accuracy_threshold"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", default=SCORES, type=Path)
    parser.add_argument("--labels", default=LABELS, type=Path)
    parser.add_argument("--output", default=OUTPUT, type=Path)
    args = parser.parse_args()

    scores = {(r["scene"], r["condition"]): r for r in load_rows(args.scores)}
    labels = {(r["target"], r["heldout_scene"], r["variant"]): int(r["label"]) for r in load_rows(args.labels)}
    variants = list(VARIANT_TO_CONDITION)
    missing = [(s, c) for s in SCENES for c in VARIANT_TO_CONDITION.values() if (s, c) not in scores]
    if missing:
        raise SystemExit(f"CrossScore missing for {missing}")

    quality = {}
    for method, column in METHODS:
        for s in SCENES:
            for v in variants:
                quality[(method, s, v)] = float(scores[(s, VARIANT_TO_CONDITION[v])][column])
    methods = [m for m, _ in METHODS]
    if OBS_TABLE2.exists():
        for r in load_rows(OBS_TABLE2):
            quality[("CrossScore OBS-TableII", r["scene"], r["variant"])] = float(r["crossscore_obs"])
        if all(("CrossScore OBS-TableII", s, v) in quality for s in SCENES for v in variants):
            methods.append("CrossScore OBS-TableII")

    predictions = []
    for method in methods:
        for target in TARGETS:
            rows = [{"scene": s, "variant": v, "label": labels[(target, s, v)],
                     "quality": quality[(method, s, v)]} for s in SCENES for v in variants]
            for scene in SCENES:
                train = [r for r in rows if r["scene"] != scene]
                test = [r for r in rows if r["scene"] == scene]
                threshold, constant, status = fit(train, 1)
                for r in test:
                    pred = constant if constant is not None else int(r["quality"] < threshold)
                    predictions.append({"method": method, "target": target, "heldout_scene": scene,
                                        "variant": r["variant"], "quality": r["quality"], "label": r["label"],
                                        "prediction": pred, "correct": int(pred == r["label"]),
                                        "fit_status": status})
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)
    print(f"Wrote {args.output} ({len(predictions)} rows)")
    for method in methods:
        counts = {t: sum(r["correct"] for r in predictions if r["method"] == method and r["target"] == t)
                  for t in TARGETS}
        print(method, counts, "total", sum(counts[t] for t in TARGETS[:3]))


if __name__ == "__main__":
    main()
