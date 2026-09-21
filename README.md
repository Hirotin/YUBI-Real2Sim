# ICRA 2027 Real2Sim — Supplementary Results

## Task Success Rate: Real Robot vs. Clean Sim

### Duo

![Task success rate: real vs. clean sim — Duo](results/figures/success_rate_overall/Duo.png)

### Flat

![Task success rate: real vs. clean sim — Flat](results/figures/success_rate_overall/Flat.png)

### G2

![Task success rate: real vs. clean sim — G2](results/figures/success_rate_overall/G2.png)

- CSVs: [`results/data/success_rate_overall/`](results/data/success_rate_overall)
- Script: [`results/scripts/plot_success_rate_overall.py`](results/scripts/plot_success_rate_overall.py)

## Task Success Rate under Disturbances

### Duo

![Task success rate under disturbances — Duo / Cup](results/figures/success_rate_disturbances/Duo_Cup.png)

![Task success rate under disturbances — Duo / Pen](results/figures/success_rate_disturbances/Duo_Pen.png)

![Task success rate under disturbances — Duo / Tape](results/figures/success_rate_disturbances/Duo_Tape.png)

### Flat

![Task success rate under disturbances — Flat / Cup](results/figures/success_rate_disturbances/Flat_Cup.png)

![Task success rate under disturbances — Flat / Pen](results/figures/success_rate_disturbances/Flat_Pen.png)

![Task success rate under disturbances — Flat / Tape](results/figures/success_rate_disturbances/Flat_Tape.png)

### G2

![Task success rate under disturbances — G2 / Cup](results/figures/success_rate_disturbances/G2_Cup.png)

![Task success rate under disturbances — G2 / Pen](results/figures/success_rate_disturbances/G2_Pen.png)

![Task success rate under disturbances — G2 / Tape](results/figures/success_rate_disturbances/G2_Tape.png)

- CSVs: [`results/data/success_rate_disturbances/`](results/data/success_rate_disturbances)
- Script: [`results/scripts/plot_success_rate_disturbances.py`](results/scripts/plot_success_rate_disturbances.py)

## Reconstruction Quality (MAE / CrossScore)

![Reconstruction quality: MAE and CrossScore](results/figures/reconstruction_metrics.png)

- CSV: [`results/data/reconstruction_metrics.csv`](results/data/reconstruction_metrics.csv)
- Script: [`results/scripts/plot_reconstruction_metrics.py`](results/scripts/plot_reconstruction_metrics.py)

## Novel View Synthesis Quality (Test Set: PSNR / SSIM / LPIPS)

![Novel view synthesis quality: PSNR, SSIM, LPIPS](results/figures/novel_view_metrics.png)

- CSV: [`results/data/novel_view_metrics.csv`](results/data/novel_view_metrics.csv)
- Script: [`results/scripts/plot_novel_view_metrics.py`](results/scripts/plot_novel_view_metrics.py)

---

Colors and fonts follow the ICRA 2026 paper's own figure scripts
(`icra2026_yubi-real2sim/figs/plots/*.py`): DejaVu Serif, real = gray /
sim = blue with policy encoded as opacity (Fig. 1 style) for the overall
chart, and policy-colored blue/amber bars for the sim-only disturbance
chart (matching the paper's counterfactual significance plots). Each
`plot_*.py` script also writes a vector `.pdf` next to its `.png`, ready to
drop into the paper.

Each figure above is generated from CSVs. `success_rate_overall/` and
`success_rate_disturbances/` produce one figure per CSV file found in their
directory (one per scene, and one per scene/task pair, respectively) — drop
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
