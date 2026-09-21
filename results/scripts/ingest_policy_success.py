#!/usr/bin/env python3
"""Convert the raw per-trial policy success CSV into the per-scene /
per-(scene,task) CSVs that plot_success_rate_overall.py and
plot_success_rate_disturbances.py consume.

Raw input schema (one row per scene x task x domain x policy x condition):
    condition,scene,task,domain,policy,checkpoint,successes,trials,
    success_rate_percent,ci95_lower_percent,ci95_upper_percent

    condition   "Clean" (no disturbance) or a disturbance name
    domain      "real" or "sim"
    policy      policy id (e.g. "pi_1", "pi_2")

Output:
    results/data/success_rate_overall/<scene>.csv
        rows where condition == "Clean", one file per scene, both domains
        schema: task,domain,policy,success_rate,num_trials,successes

    results/data/success_rate_disturbances/<scene>_<task>.csv
        rows where condition != "Clean" AND domain == "sim", one file per
        (scene, task). Real trials were only run under the Clean condition
        (the raw log repeats the Clean real result under every disturbance
        row as a reference, not as a re-measurement), so real is reported
        once in success_rate_overall/ and omitted here to avoid implying it
        was re-measured per disturbance -- this matches how the paper's own
        plot_all_policy_success_significance.py reports this data (sim only,
        y-axis labelled "Sim success rate").
        schema: disturbance,domain,policy,success_rate,num_trials,successes

Re-running this script overwrites the generated CSVs; it does not touch
results/figures/ -- run the plot_*.py scripts (or generate_all.sh)
afterwards to redraw the figures.
"""

import argparse
import csv
from pathlib import Path

DEFAULT_INPUT = (
    Path.home() / "icra2026_yubi-real2sim" / "docs" / "experiments" / "policy_success_all_conditions.csv"
)
REPO_ROOT = Path(__file__).resolve().parents[2]
OVERALL_DIR = REPO_ROOT / "results" / "data" / "success_rate_overall"
DISTURBANCES_DIR = REPO_ROOT / "results" / "data" / "success_rate_disturbances"


def load_rows(csv_path):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def to_row(r):
    return {
        "domain": r["domain"],
        "policy": r["policy"],
        "success_rate": int(r["successes"]) / int(r["trials"]),
        "num_trials": r["trials"],
        "successes": r["successes"],
    }


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=DEFAULT_INPUT, type=Path)
    args = parser.parse_args()

    raw_rows = load_rows(args.input)
    scenes = list(dict.fromkeys(r["scene"] for r in raw_rows))

    for scene in scenes:
        scene_rows = [r for r in raw_rows if r["scene"] == scene and r["condition"] == "Clean"]
        out_rows = [{"task": r["task"], **to_row(r)} for r in scene_rows]
        write_csv(
            OVERALL_DIR / f"{scene}.csv",
            ["task", "domain", "policy", "success_rate", "num_trials", "successes"],
            out_rows,
        )

    scene_tasks = list(dict.fromkeys((r["scene"], r["task"]) for r in raw_rows))

    for scene, task in scene_tasks:
        rows = [
            r
            for r in raw_rows
            if r["scene"] == scene
            and r["task"] == task
            and r["condition"] != "Clean"
            and r["domain"] == "sim"
        ]
        out_rows = [{"disturbance": r["condition"], **to_row(r)} for r in rows]
        write_csv(
            DISTURBANCES_DIR / f"{scene}_{task}.csv",
            ["disturbance", "domain", "policy", "success_rate", "num_trials", "successes"],
            out_rows,
        )


if __name__ == "__main__":
    main()
