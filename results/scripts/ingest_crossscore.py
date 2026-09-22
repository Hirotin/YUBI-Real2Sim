#!/usr/bin/env python3
"""Convert the CrossScore export into results/data/crossscore.csv.

Raw input schema (one row per scene x condition):
    rig,condition,obs_R,obs_L,obs_mean,obs_current5_mean,
    test_crossscore,test_crossscore_sd,test_views,test_psnr_person_free,test_psnr_all

Output schema:
    condition,scene,CrossScore_Test,CrossScore_Test_sd,CrossScore_OBS,CrossScore_OBS_R,CrossScore_OBS_L,test_views

    CrossScore_Test   mean over the held-out Test views (test_crossscore)
    CrossScore_OBS    mean over the OBS views (obs_mean, the mean of the R/L cameras)

Conditions are renamed to the ones every other figure uses (clean -> Clean)
and rows are ordered the same way. The PSNR columns of the export are not
copied: the README's PSNR comes from the full-reference test-set scores.
"""

import argparse
import csv
from pathlib import Path

DEFAULT_INPUT = Path.home() / "Downloads" / "obs_and_test_crossscore.csv"
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "crossscore.csv"
CONDITIONS = ["Clean", "hole_54", "hole_90", "float_low8", "float_mid8", "float_high8",
              "tablegeo_s1", "fov_center", "pinhole_adjacent_remove_30", "pinhole_random_remove_30"]
SCENES = ["Duo", "Flat", "G2"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=DEFAULT_INPUT, type=Path)
    args = parser.parse_args()

    with open(args.input, newline="") as f:
        raw = list(csv.DictReader(f))
    rows = [{"condition": "Clean" if r["condition"] == "clean" else r["condition"], "scene": r["rig"],
             "CrossScore_Test": r["test_crossscore"], "CrossScore_Test_sd": r["test_crossscore_sd"],
             "CrossScore_OBS": r["obs_mean"], "CrossScore_OBS_R": r["obs_R"], "CrossScore_OBS_L": r["obs_L"],
             "test_views": r["test_views"]} for r in raw]
    unknown = {r["condition"] for r in rows} - set(CONDITIONS)
    if unknown:
        raise ValueError(f"Unmapped conditions: {sorted(unknown)}")
    rows.sort(key=lambda r: (CONDITIONS.index(r["condition"]),
                             SCENES.index(r["scene"]) if r["scene"] in SCENES else len(SCENES)))
    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUTPUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
