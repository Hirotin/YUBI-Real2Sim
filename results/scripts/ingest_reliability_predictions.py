#!/usr/bin/env python3
"""Copy the out-of-fold reliability predictions behind Table II of the paper
into results/data/reliability_predictions.csv.

Input schema (kept unchanged; one row per method x target x held-out scene x variant):
    method,target,heldout_scene,variant,quality,label,prediction,correct,fit_status

    target       Cup / Tape / Pen / All-three
    label        H: 1 = the sim ranking of the two policies disagrees with the
                 real ranking (or ties in sim), 0 = agrees
    prediction   predicted H for the held-out scene
    fit_status   balanced_accuracy_threshold, or training_class_constant when
                 the training labels contained a single class
"""

import argparse
import shutil
from pathlib import Path

DEFAULT_INPUT = (
    Path.home() / "icra2026_yubi-real2sim" / "docs" / "experiments"
    / "main_test_baselines_20260917" / "predictions.csv"
)
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "reliability_predictions.csv"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=DEFAULT_INPUT, type=Path)
    args = parser.parse_args()
    shutil.copyfile(args.input, OUTPUT)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
