#!/usr/bin/env bash
# Regenerate every figure in results/figures/ from the CSVs in results/data/.
# A CSV with no data rows leaves its figure's placeholder untouched.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

python3 plot_success_rate_overall.py
python3 plot_success_rate_disturbances.py
python3 plot_disturbance_highlights.py
python3 plot_mae.py
python3 plot_crossscore.py
python3 plot_novel_view_metrics.py
