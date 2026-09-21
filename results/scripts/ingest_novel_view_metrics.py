#!/usr/bin/env python3
"""Convert the paper's full-reference test-set scores into
results/data/novel_view_metrics.csv.

Raw input schema (one row per scene x condition):
    robot,condition,views,psnr_db,ssim,lpips_alex

Output schema:
    condition,scene,views,PSNR,SSIM,LPIPS

Condition names are rewritten to the ones the success-rate and MAE figures
use, and rows are ordered the same way, so every figure in this repo shares
one x-axis.
"""

import argparse
import csv
from pathlib import Path

DEFAULT_INPUT = (
    Path.home() / "icra2026_yubi-real2sim" / "docs" / "experiments"
    / "test_full_reference_20260917" / "scores_30_scenes.csv"
)
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "novel_view_metrics.csv"

CONDITIONS = {
    "Clear": "Clean",
    "Hole54": "hole_54",
    "Hole90": "hole_90",
    "FloaterLow8": "float_low8",
    "FloaterMid8": "float_mid8",
    "FloaterHigh8": "float_high8",
    "TableGeometryS1": "tablegeo_s1",
    "CentralPinhole": "fov_center",
    "Contiguous30": "pinhole_adjacent_remove_30",
    "ViewCountRandom30": "pinhole_random_remove_30",
}
SCENES = ["Duo", "Flat", "G2"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=DEFAULT_INPUT, type=Path)
    args = parser.parse_args()

    with open(args.input, newline="") as f:
        raw = list(csv.DictReader(f))
    unknown = {r["condition"] for r in raw} - set(CONDITIONS)
    if unknown:
        raise ValueError(f"Unmapped conditions: {sorted(unknown)}")

    order = list(CONDITIONS)
    raw.sort(key=lambda r: (order.index(r["condition"]),
                            SCENES.index(r["robot"]) if r["robot"] in SCENES else len(SCENES)))
    rows = [{"condition": CONDITIONS[r["condition"]], "scene": r["robot"], "views": r["views"],
             "PSNR": r["psnr_db"], "SSIM": r["ssim"], "LPIPS": r["lpips_alex"]} for r in raw]
    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUTPUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
