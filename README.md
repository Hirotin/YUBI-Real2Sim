# ICRA 2027 Real2Sim — Supplementary Results

## 1. Task Success Rate under Disturbances

Sim pi_1 vs. pi_2, two-sided Fisher exact test (alpha = 0.05), Clean vs. each disturbance. The full per-scene results are in Section 5.

### 1.1 Policy ranking reversed

![Rank reversed](results/figures/success_rate_disturbances_highlights/rank_reversed.png)

### 1.2 From significant to not significant

![Significance lost](results/figures/success_rate_disturbances_highlights/significance_lost.png)

### 1.3 From not significant to significant

![Significance gained](results/figures/success_rate_disturbances_highlights/significance_gained.png)

## 2. Sim-to-Real MAE

Mean absolute error between simulated and real success rates, in percentage points. For scene $s$ and condition $c$, the 6 cells (3 tasks $t$ × 2 policies $\pi$) are averaged with equal weight:

```math
\mathrm{MAE}(s, c) = \frac{1}{6} \sum_{t,\,\pi} \left| \, 100 \cdot \frac{k^{\mathrm{sim}}_{s,c,t,\pi}}{80} \; - \; 100 \cdot \frac{k^{\mathrm{real}}_{s,t,\pi}}{20} \, \right|
```

where $k^{\mathrm{sim}}$ is the number of successes out of 80 simulated trials under condition $c$, and $k^{\mathrm{real}}$ is the number of successes out of 20 real trials. Real trials were run under Clean only, so the same real value is used for every condition.

![Sim-to-real MAE per scene and condition](results/figures/mae.png)

Values: [`results/data/mae.csv`](results/data/mae.csv)

## 3. CrossScore

CrossScore per scene and condition, on the held-out Test views (mean over test views; the same views as Section 4) and on the OBS views (mean of the right and left OBS cameras). Higher is better.

![CrossScore on Test and OBS views](results/figures/crossscore_lines.png)

<!-- crossscore-table:start -->
| Condition | Test FR3 Duo | Test FR3 Flat | Test G2 | OBS FR3 Duo | OBS FR3 Flat | OBS G2 |
|---|---:|---:|---:|---:|---:|---:|
| Clean | 0.897 | 0.862 | 0.874 | 0.778 | 0.824 | 0.828 |
| hole_54 | 0.722 | 0.740 | 0.822 | 0.781 | 0.829 | 0.802 |
| hole_90 | 0.508 | 0.523 | 0.592 | 0.631 | 0.745 | 0.827 |
| float_low8 | 0.889 | 0.854 | 0.872 | 0.766 | 0.800 | 0.818 |
| float_mid8 | 0.890 | 0.851 | 0.868 | 0.777 | 0.829 | 0.736 |
| float_high8 | 0.887 | 0.849 | 0.867 | 0.783 | 0.790 | 0.788 |
| tablegeo_s1 | 0.888 | 0.853 | 0.872 | 0.778 | 0.815 | 0.839 |
| fov_center | 0.689 | 0.672 | 0.797 | 0.584 | 0.697 | 0.810 |
| pinhole_adjacent_remove_30 | 0.601 | 0.569 | 0.703 | 0.536 | 0.617 | 0.607 |
| pinhole_random_remove_30 | 0.643 | 0.615 | 0.765 | 0.551 | 0.677 | 0.784 |
<!-- crossscore-table:end -->

Values: [`results/data/crossscore.csv`](results/data/crossscore.csv)

## 4. Novel View Synthesis Quality (Test Set: PSNR / SSIM / LPIPS)

Full-reference scores on the held-out test views, per scene and condition.

![Novel view synthesis quality: PSNR, SSIM, LPIPS](results/figures/nvs_lines.png)

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

## 5. Task Success Rate under Disturbances: All Results

Success rate of pi_1 and pi_2 per scene and task: the real result and the Clean sim result at the left as the reference, then sim under every disturbance (the pairs highlighted in Section 1 are drawn from these).

### 5.1 FR3 Duo

![Task success rate under disturbances — Duo / Cup](results/figures/success_rate_disturbances/Duo_Cup.png)

![Task success rate under disturbances — Duo / Pen](results/figures/success_rate_disturbances/Duo_Pen.png)

![Task success rate under disturbances — Duo / Tape](results/figures/success_rate_disturbances/Duo_Tape.png)

### 5.2 FR3 Flat

![Task success rate under disturbances — Flat / Cup](results/figures/success_rate_disturbances/Flat_Cup.png)

![Task success rate under disturbances — Flat / Pen](results/figures/success_rate_disturbances/Flat_Pen.png)

![Task success rate under disturbances — Flat / Tape](results/figures/success_rate_disturbances/Flat_Tape.png)

### 5.3 G2

![Task success rate under disturbances — G2 / Cup](results/figures/success_rate_disturbances/G2_Cup.png)

![Task success rate under disturbances — G2 / Pen](results/figures/success_rate_disturbances/G2_Pen.png)

![Task success rate under disturbances — G2 / Tape](results/figures/success_rate_disturbances/G2_Tape.png)

## 6. Supplementary Analysis of Table II: Constant Baselines and Fold-wise Class Support

This section supplements Table II and Sec. V-E of the main paper with constant-prediction baselines, the distribution of ranking-disagreement labels across scenes, and a class-wise analysis of Tape predictions. The evaluated conditions and the quality-based predictions are unchanged: every number below is recomputed from the out-of-fold prediction log behind Table II ([`results/data/reliability_predictions.csv`](results/data/reliability_predictions.csv)), without refitting.

The label is the same as in the main paper: $H=0$ when the observed ranking of the two policies in simulation agrees with the real ranking, and $H=1$ when it disagrees or the two policies tie in simulation. $H$ describes the ranking of the two policies, not the success or failure of individual robot trials.

### 6.1 Table S1: Extended comparison with constant-prediction baselines

*Always reliable* predicts $\widehat{H}=0$ for every condition and *Always unreliable* predicts $\widehat{H}=1$; neither uses a quality score or a fitted threshold.

<!-- table-s1:start -->
| Method / view | Cup | Tape | Pen | Total | All-three |
|---|---:|---:|---:|---:|---:|
| Always reliable ($\widehat{H}=0$) | 8/15 | 12/15 | 15/15 | 35/45 (77.8%) | 6/15 |
| Always unreliable ($\widehat{H}=1$) | 7/15 | 3/15 | 0/15 | 10/45 (22.2%) | 9/15 |
| NVS-SQA / Test | 7/15 | 8/15 | 15/15 | 30/45 (66.7%) | 13/15 |
| NVS-SQA / OBS | 12/15 | 2/15 | 15/15 | 29/45 (64.4%) | 7/15 |
| PSNR / Test | 8/15 | 8/15 | 15/15 | 31/45 (68.9%) | 9/15 |
| SSIM / Test | 8/15 | 9/15 | 15/15 | 32/45 (71.1%) | 7/15 |
| LPIPS / Test | 8/15 | 5/15 | 15/15 | 28/45 (62.2%) | 10/15 |
| CrossScore / Test † | 7/15 | 8/15 | 15/15 | 30/45 (66.7%) | 4/15 |
| CrossScore / OBS † | 6/15 | 3/15 | 15/15 | 24/45 (53.3%) | 8/15 |
| CrossScore / OBS (Table II views) † | 5/15 | 6/15 | 15/15 | 26/45 (57.8%) | 9/15 |
<!-- table-s1:end -->

**Table S1. Extended comparison corresponding to Table II of the main paper.** Entries are correct/total classification decisions on the same matched conditions. The five quality-based rows of Table II are reproduced without modification. Rows marked † are not in Table II: they apply the identical protocol (scene-held-out threshold maximizing balanced accuracy, single-class fallback, threshold refit per target) to the CrossScore values of Section 3, with CrossScore / Test on the held-out test views and CrossScore / OBS on the OBS views of Section 3 (right/left OBS cameras). CrossScore / OBS (Table II views) is CrossScore evaluated on exactly the OBS images that Table II's NVS-SQA / OBS used: the policy-observation frames of one hole_54 rollout per scene (38 frames for Duo and G2, 19 for Flat, two wrist cameras each, MuJoCo foreground composited over the re-rendered 3DGS background); the NVS-SQA scores of those same images reproduce Table II's OBS column exactly, so this row is the like-for-like comparison with NVS-SQA / OBS. The classifier used here reproduces all 300 logged Table II predictions exactly. Both constant predictors are reported without fitting to quality scores or target-scene labels. "Total" pools the 45 task-level decisions; "All-three" evaluates the separate binary target of whether all three task rankings agree with real evaluation, so for that column *Always unreliable* means "at least one task ranking disagrees", not "all three disagree". As in the main paper, All-three predictions come from a threshold fitted to the All-three labels, not from combining the three task-level predictions.

The SSIM result of 32/45 in Sec. V-E is the highest pooled task-level accuracy among the quality-based methods listed in Table II. The expanded comparison shows that the always-reliable predictor achieves 35/45. Thus, the reported SSIM accuracy does not demonstrate an improvement over this constant predictor on the evaluated conditions. In the pooled counts the gap sits entirely in Tape:

```math
\underbrace{8-8}_{\mathrm{Cup}} + \underbrace{9-12}_{\mathrm{Tape}} + \underbrace{15-15}_{\mathrm{Pen}} = -3
```

Equal Cup counts do not imply identical individual Cup predictions. Separately, the All-three result of NVS-SQA / Test (13/15) exceeds both constant predictors (6/15 and 9/15); that result stands on its own, although 13/15 on three scenes does not by itself establish general reliability of scene acceptance.

### 6.2 Fig. S1: Label layout and Tape class support

![Ranking-disagreement labels and Tape class support](results/figures/reliability_labels.png)

**Fig. S1. Ranking-disagreement labels and Tape class support across held-out scenes.** (a) Labels for the 15 matched scene variants, with $H=1$ denoting disagreement with the observed real ranking. Cup has 8 agreements and 7 disagreements, Tape 12 and 3, Pen 15 and 0, which gives the constant-predictor rows of Table S1. (b) Tape training and test class counts for each held-out scene. All three Tape disagreements occur in G2. When G2 is held out, the training labels are all $H=0$, so the single-class fallback in Sec. IV-B predicts $H=0$ for every G2 variant. Test labels are displayed only for retrospective analysis and are not used for fitting.

The point is not that quality metrics are inherently uninformative for Tape. With this label layout and the single-class fallback, the quality score is never used in the one fold that contains Tape disagreements. Under the current protocol the Tape accuracy of any quality-based method is therefore at most 12/15, because the three G2 disagreements are always missed, and the always-reliable predictor attains that bound.

### 6.3 Table S2: Tape error decomposition

Ranking disagreement ($H=1$) is the positive class: TP is a disagreement flagged as one, FN a missed disagreement, FP a false alarm on an agreement-labeled condition, and TN a correctly passed agreement.

<!-- table-s2:start -->
| Method / view | TP ↑ | FN ↓ | FP ↓ | TN ↑ | Balanced accuracy ↑ |
|---|---:|---:|---:|---:|---:|
| Always reliable | 0 | 3 | 0 | 12 | 50.0% |
| Always unreliable | 3 | 0 | 12 | 0 | 50.0% |
| NVS-SQA / Test | 0 | 3 | 4 | 8 | 33.3% |
| NVS-SQA / OBS | 0 | 3 | 10 | 2 | 8.3% |
| PSNR / Test | 0 | 3 | 4 | 8 | 33.3% |
| SSIM / Test | 0 | 3 | 3 | 9 | 37.5% |
| LPIPS / Test | 0 | 3 | 7 | 5 | 20.8% |
| CrossScore / Test † | 0 | 3 | 4 | 8 | 33.3% |
| CrossScore / OBS † | 0 | 3 | 9 | 3 | 12.5% |
| CrossScore / OBS (Table II views) † | 0 | 3 | 6 | 6 | 25.0% |
<!-- table-s2:end -->

**Table S2. Tape classification errors pooled across the three held-out-scene folds.** The evaluated set contains three disagreements and twelve agreements. Balanced accuracy is computed from the pooled out-of-fold confusion counts, not averaged over single-class test folds:

```math
\mathrm{BA} = \frac{1}{2}\left(\frac{TP}{TP+FN} + \frac{TN}{TN+FP}\right), \qquad \mathrm{BA}_{\mathrm{Tape,\,SSIM}} = \frac{1}{2}\left(\frac{0}{3} + \frac{9}{12}\right) = 37.5\%
```

All quality-based methods, including both CrossScore views, miss the three Tape disagreements in the G2 fold. Their Tape accuracy differences therefore arise from false alarms on agreement-labeled conditions, rather than differences in disagreement detection. For SSIM, the 9/15 result consists of nine true negatives, three false positives, and three false negatives. Pen contains no disagreement, so disagreement recall and two-class balanced accuracy are undefined (N/A) there; its 15/15 is not evidence of disagreement detection.

---
