# ICRA 2027 Real2Sim — Supplementary Results

## 1. Task Success Rate: Real Robot vs. Clean Sim

![Task success rate: real vs. clean sim](results/figures/success_rate_overall.png?v=ebb906de)

## 2. Task Success Rate under Disturbances

Sim pi_1 vs. pi_2, two-sided Fisher exact test (alpha = 0.05), Clean vs. each disturbance.

### 2.1 Policy ranking reversed

![Rank reversed](results/figures/success_rate_disturbances_highlights/rank_reversed.png?v=57ca485f)

### 2.2 From significant to not significant

![Significance lost](results/figures/success_rate_disturbances_highlights/significance_lost.png?v=892b19d5)

### 2.3 From not significant to significant

![Significance gained](results/figures/success_rate_disturbances_highlights/significance_gained.png?v=745a975f)

### 2.4 All results: Duo

![Task success rate under disturbances — Duo / Cup](results/figures/success_rate_disturbances/Duo_Cup.png?v=3fbfd21d)

![Task success rate under disturbances — Duo / Pen](results/figures/success_rate_disturbances/Duo_Pen.png?v=d88f936e)

![Task success rate under disturbances — Duo / Tape](results/figures/success_rate_disturbances/Duo_Tape.png?v=4f5f5e4c)

### 2.5 All results: Flat

![Task success rate under disturbances — Flat / Cup](results/figures/success_rate_disturbances/Flat_Cup.png?v=def4d562)

![Task success rate under disturbances — Flat / Pen](results/figures/success_rate_disturbances/Flat_Pen.png?v=7784613a)

![Task success rate under disturbances — Flat / Tape](results/figures/success_rate_disturbances/Flat_Tape.png?v=99d19850)

### 2.6 All results: G2

![Task success rate under disturbances — G2 / Cup](results/figures/success_rate_disturbances/G2_Cup.png?v=af3d8989)

![Task success rate under disturbances — G2 / Pen](results/figures/success_rate_disturbances/G2_Pen.png?v=1e01191d)

![Task success rate under disturbances — G2 / Tape](results/figures/success_rate_disturbances/G2_Tape.png?v=58abb8a7)

## 3. Sim-to-Real MAE

Mean absolute error between simulated and real success rates, in percentage points. For scene $s$ and condition $c$, the 6 cells (3 tasks $t$ × 2 policies $\pi$) are averaged with equal weight:

```math
\mathrm{MAE}(s, c) = \frac{1}{6} \sum_{t,\,\pi} \left| \, 100 \cdot \frac{k^{\mathrm{sim}}_{s,c,t,\pi}}{80} \; - \; 100 \cdot \frac{k^{\mathrm{real}}_{s,t,\pi}}{20} \, \right|
```

where $k^{\mathrm{sim}}$ is the number of successes out of 80 simulated trials under condition $c$, and $k^{\mathrm{real}}$ is the number of successes out of 20 real trials. Real trials were run under Clean only, so the same real value is used for every condition.

![Sim-to-real MAE per scene and condition](results/figures/mae.png?v=96ad6854)

Values: [`results/data/mae.csv`](results/data/mae.csv)

## 4. CrossScore

![CrossScore](results/figures/crossscore.png?v=1c12324c)

## 5. Novel View Synthesis Quality (Test Set: PSNR / SSIM / LPIPS)

Full-reference scores on the held-out test views, per scene and condition.

![Novel view synthesis quality: PSNR, SSIM, LPIPS](results/figures/nvs_metrics.png?v=63b6e4a7)

PSNR in dB (↑), SSIM (↑), LPIPS (↓).

<!-- nvs-table:start -->
| Condition | PSNR FR3 Duo | PSNR FR3 Flat | PSNR G2 | SSIM FR3 Duo | SSIM FR3 Flat | SSIM G2 | LPIPS FR3 Duo | LPIPS FR3 Flat | LPIPS G2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Clean | 18.55 | 18.13 | 16.52 | 0.738 | 0.716 | 0.718 | 0.227 | 0.230 | 0.276 |
| hole_54 | 13.90 | 14.57 | 14.36 | 0.582 | 0.594 | 0.642 | 0.387 | 0.352 | 0.357 |
| hole_90 | 9.63 | 10.21 | 10.85 | 0.377 | 0.394 | 0.488 | 0.615 | 0.578 | 0.554 |
| float_low8 | 18.33 | 18.10 | 16.35 | 0.730 | 0.711 | 0.712 | 0.242 | 0.240 | 0.291 |
| float_mid8 | 18.40 | 18.16 | 16.39 | 0.731 | 0.713 | 0.713 | 0.242 | 0.239 | 0.292 |
| float_high8 | 18.50 | 18.16 | 16.38 | 0.733 | 0.712 | 0.712 | 0.240 | 0.240 | 0.290 |
| tablegeo_s1 | 18.17 | 17.78 | 16.41 | 0.719 | 0.700 | 0.708 | 0.236 | 0.237 | 0.284 |
| fov_center | 15.46 | 15.42 | 14.90 | 0.585 | 0.547 | 0.638 | 0.336 | 0.351 | 0.341 |
| pinhole_adjacent_remove_30 | 14.91 | 14.79 | 13.72 | 0.527 | 0.476 | 0.549 | 0.384 | 0.407 | 0.406 |
| pinhole_random_remove_30 | 15.46 | 15.08 | 14.58 | 0.578 | 0.529 | 0.617 | 0.349 | 0.372 | 0.354 |
<!-- nvs-table:end -->

Values: [`results/data/novel_view_metrics.csv`](results/data/novel_view_metrics.csv)

---

Colors and fonts follow the ICRA 2026 paper's own figure scripts
(`icra2026_yubi-real2sim/figs/plots/*.py`): DejaVu Serif, real = gray /
sim = blue with policy encoded as opacity (Fig. 1 style) for the overall
chart, and policy-colored blue/amber bars for the sim-only disturbance
chart (matching the paper's counterfactual significance plots). Each
`plot_*.py` script also writes a vector `.pdf` next to its `.png`, ready to
drop into the paper.

Each figure above is generated from CSVs. `success_rate_overall/` and
`success_rate_disturbances/` pick up every CSV file found in their
directory (one panel per scene, and one figure per scene/task pair, respectively) — drop
in a new CSV there to get a new figure with no script changes. To update a
result, add/edit the relevant CSV(s) and run:

```bash
pip install -r results/scripts/requirements.txt
bash results/scripts/generate_all.sh
```

`results/scripts/ingest_policy_success.py` converts the raw per-trial policy
success log into the `success_rate_overall/` and `success_rate_disturbances/`
CSVs above:

```bash
python3 results/scripts/ingest_policy_success.py --input <path/to/policy_success_all_conditions.csv>
bash results/scripts/generate_all.sh
```
