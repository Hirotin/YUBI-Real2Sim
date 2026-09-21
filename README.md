# ICRA 2027 Real2Sim — Supplementary Results

## 1. Task Success Rate: Real Robot vs. Clean Sim

![Task success rate: real vs. clean sim](results/figures/success_rate_overall.png)

## 2. Task Success Rate under Disturbances

Sim pi_1 vs. pi_2, two-sided Fisher exact test (alpha = 0.05), Clean vs. each disturbance.

### 2.1 Policy ranking reversed

![Rank reversed](results/figures/success_rate_disturbances_highlights/rank_reversed.png)

### 2.2 From significant to not significant

![Significance lost](results/figures/success_rate_disturbances_highlights/significance_lost.png)

### 2.3 From not significant to significant

![Significance gained](results/figures/success_rate_disturbances_highlights/significance_gained.png)

### 2.4 All results: Duo

![Task success rate under disturbances — Duo / Cup](results/figures/success_rate_disturbances/Duo_Cup.png)

![Task success rate under disturbances — Duo / Pen](results/figures/success_rate_disturbances/Duo_Pen.png)

![Task success rate under disturbances — Duo / Tape](results/figures/success_rate_disturbances/Duo_Tape.png)

### 2.5 All results: Flat

![Task success rate under disturbances — Flat / Cup](results/figures/success_rate_disturbances/Flat_Cup.png)

![Task success rate under disturbances — Flat / Pen](results/figures/success_rate_disturbances/Flat_Pen.png)

![Task success rate under disturbances — Flat / Tape](results/figures/success_rate_disturbances/Flat_Tape.png)

### 2.6 All results: G2

![Task success rate under disturbances — G2 / Cup](results/figures/success_rate_disturbances/G2_Cup.png)

![Task success rate under disturbances — G2 / Pen](results/figures/success_rate_disturbances/G2_Pen.png)

![Task success rate under disturbances — G2 / Tape](results/figures/success_rate_disturbances/G2_Tape.png)

## 3. Reconstruction Quality (MAE / CrossScore)

![Reconstruction quality: MAE and CrossScore](results/figures/reconstruction_metrics.png)

## 4. Novel View Synthesis Quality (Test Set: PSNR / SSIM / LPIPS)

![Novel view synthesis quality: PSNR, SSIM, LPIPS](results/figures/novel_view_metrics.png)

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
