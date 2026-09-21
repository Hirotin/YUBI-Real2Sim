# ICRA 2027 Real2Sim — Supplementary Results

## Task Success Rate: Real Robot vs. Clean Sim

![Task success rate: real vs. clean sim](results/figures/success_rate_overall.png)

- CSV: [`results/data/success_rate_overall.csv`](results/data/success_rate_overall.csv)
- Script: [`results/scripts/plot_success_rate_overall.py`](results/scripts/plot_success_rate_overall.py)

## Task Success Rate under Disturbances

![Task success rate under disturbances](results/figures/success_rate_disturbances.png)

- CSV: [`results/data/success_rate_disturbances.csv`](results/data/success_rate_disturbances.csv)
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

Each figure above is generated from its CSV. To update a result, fill in the
corresponding CSV under `results/data/` and run:

```bash
pip install -r results/scripts/requirements.txt
bash results/scripts/generate_all.sh
```
