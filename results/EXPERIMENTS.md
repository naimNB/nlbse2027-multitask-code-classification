# Recorded experiments (as of 21 November 2026)

**Do not mix pilot, holdout and public-split scores when ranking models.** The recorded experiments were mostly single-seed runs; E0–E3, E5, E7, E8 and E9 do not constitute a fully controlled ablation.

## Public split — 30,655 rows, 256 tokens, thresholds [0.5, 0.5]

| Model | Weakness P | Weakness R | Weakness F1 | Debt P | Debt R | Debt F1 | Mean F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Official released baseline | 0.9325 | 0.8260 | 0.8760 | 0.9727 | 0.5644 | 0.7143 | 0.7952 |
| E3 weighted BCE, 2,000 steps | 0.8495 | 0.7268 | 0.7834 | 0.9745 | 0.5307 | 0.6872 | 0.7353 |
| E5 weighted BCE, best at step 4,000 | 0.8509 | 0.7898 | 0.8192 | 0.9926 | 0.5327 | 0.6933 | 0.7563 |
| E8 weighted BCE + scheduler, 10,000 steps | 0.9014 | 0.8049 | 0.8504 | 0.9652 | 0.5485 | 0.6995 | 0.7750 |
| **E9-Fresh weighted BCE + scheduler, best step 13,000** | **0.9114** | **0.8051** | **0.8550** | **0.9725** | **0.5604** | **0.7111** | **0.7830** |

Timing in the local earlier evaluation: released baseline ~414.16 seconds and E3 ~417.77 seconds for the public split. No same-procedure E5 timing measurement is recorded. E8 wall-clock inference from model loading excluded and timed inference was 486.06 seconds on its Kaggle session, which is not necessarily hardware-comparable. These timings are not the organizer's official runtime/GFLOPs ranking.

## Training and pilot experiments

| Experiment | Configuration | Pilot weakness F1 | Pilot debt F1 | Pilot mean F1 | Note |
|---|---|---:|---:|---:|---|
| E0 | Standard BCE, 500 steps | 0.7241 | 0.0000 | 0.3620 | Fixed 0.5 threshold |
| E1 | Weighted BCE [1,10], 500 steps | 0.6851 | 0.0000 | 0.3425 | Fixed 0.5 threshold |
| E2 | Standard BCE, 2,000 steps | 0.7745 | 0.0000 | 0.3873 | Fixed 0.5 threshold |
| E3 | Weighted BCE [1,10], 2,000 steps | 0.7814 | 0.6080 | 0.6947 | Fixed 0.5 threshold |
| E5 | Weighted BCE [1,10], 6,000 max steps; best checkpoint 4,000 | 0.8176 | 0.6080 | 0.7128 | Fixed 0.5 threshold |
| E6 | Post-hoc threshold search on E5 pilot | 0.8200 | 0.6080 | 0.7140 | Thresholds [0.43, 0.99]; exploratory only |
| E7 | Weighted BCE [1,10], 6,000 steps; linear learning-rate decay; best at step 6,000 | 0.8188 | 0.6080 | 0.7134 | Pilot only; public split not yet evaluated |
| **E8** | Weighted BCE [1,10], 10,000 steps; linear schedule, 1,000 warmup steps | **0.8399** | **0.6142** | **0.7270** | Best at 10,000; public split evaluated |
| **E9-Fresh** | Weighted BCE [1,10], 15,000 steps; linear scheduler, 1,500 warmup steps | **0.8502** | **0.6615** | **0.7559** | Best at 13,000; public split evaluated |

### Pilot threshold analyses

- E0 best tested debt threshold 0.020: debt F1 0.0842.
- E1 best tested debt threshold 0.041: debt F1 0.0896.
- E2 best tested debt threshold 0.164: debt F1 0.4677.
- These values were selected **on the same pilot split** and are not independent evaluation results.
- E6's debt threshold 0.99 was a tie among many thresholds at the same F1; it was not evidence of superior calibration. Default 0.5 is preferable until a cleaner validation study.

## E5 checkpoint selection

| Step | Weakness F1 | Debt F1 | Mean F1 |
|---:|---:|---:|---:|
| 1,000 | 0.7442 | 0.0000 | 0.3721 |
| 2,000 | 0.7813 | 0.6032 | 0.6922 |
| 3,000 | 0.8034 | 0.6032 | 0.7033 |
| **4,000** | **0.8176** | **0.6080** | **0.7128** |
| 5,000 | 0.8162 | 0.6032 | 0.7097 |
| 6,000 | 0.8223 | 0.6032 | 0.7127 |

## E7 scheduler run (pilot validation only)

| Step | Learning rate | Weakness F1 | Debt F1 | Mean F1 |
|---:|---:|---:|---:|---:|
| 1,000 | 1.85e-5 | 0.6859 | 0.0000 | 0.3430 |
| 2,000 | 1.48e-5 | 0.7724 | 0.6080 | 0.6902 |
| 3,000 | 1.11e-5 | 0.8057 | 0.6080 | 0.7068 |
| 4,000 | 7.41e-6 | 0.8046 | 0.6080 | 0.7063 |
| 5,000 | 3.70e-6 | 0.8127 | 0.6080 | 0.7104 |
| **6,000** | **0** | **0.8188** | **0.6080** | **0.7134** |

Elapsed training time: **45.87 minutes**. Pilot mean F1 E7 minus E5: **+0.00061**. Precision and recall at E7 best pilot checkpoint: weakness P=0.86785 / R=0.77494, debt P=1.0 / R=0.43678. An apparent 0.0006-point F1 advantage on the pilot does not establish a meaningful scheduler benefit. The same pilot selected checkpoints for both runs.

**E7 public-split metrics have not been supplied or verified.**

## E8 training and internal evaluation (20 November 2026)

E8 completed 10,000 steps in approximately **86.54 minutes**. The best checkpoint according to pilot mean F1 was saved at **step 10,000**. Reported configuration: weighted BCE `[1, 10]`, 2e-5 peak learning rate, 1,000 warmup steps, linear decay, 256-token truncation, batch size 8. As with earlier experiments, precise hyperparameter/config versioning should be checked against the actual saved `run_config.json`.

### E8 validation checkpoints

| Step | Vulnerability F1 | Debt F1 | Mean F1 |
|---:|---:|---:|---:|
| 1,000 | 0.6751 | 0.0000 | 0.3375 |
| 2,000 | 0.7567 | 0.6032 | 0.6799 |
| 3,000 | 0.7630 | 0.6080 | 0.6855 |
| 4,000 | 0.8032 | 0.6080 | 0.7056 |
| 5,000 | 0.8116 | 0.6032 | 0.7074 |
| 6,000 | 0.8309 | 0.6154 | 0.7231 |
| 7,000 | 0.8332 | 0.6080 | 0.7206 |
| 8,000 | 0.8344 | 0.6000 | 0.7172 |
| 9,000 | 0.8385 | 0.6142 | 0.7264 |
| **10,000** | **0.8399** | **0.6142** | **0.7270** |

### E8 clean internal holdout (16,420 samples)

The reported split was `internal_holdout_excluding_exact_pilot_code_hashes`. The evaluation remains **within-project** and includes many previously seen source files. It is not a blind project-disjoint test.

| Task | Precision | Recall | F1 | Confusion matrix [[TN, FP], [FN, TP]] |
|---|---:|---:|---:|---|
| Vulnerability | 0.88985 | 0.80170 | **0.84348** | [[10483,536],[1071,4330]] |
| Technical Debt | 0.98710 | 0.53873 | **0.69704** | [[16134,2],[131,153]] |
| **Mean** | — | — | **0.77026** | — |

The recorded E3 clean-holdout mean F1 was 0.7360. E8's 0.77026 is **0.0343 higher on nominally comparable internal holdout conditions**; exact dataset revision and row membership must still be audited.

**E8 public split result:** 30,655 rows, thresholds [0.5,0.5], max length 256: vulnerability P 0.90140, R 0.80491, F1 0.85043, confusion [[19718,885],[1961,8091]]; debt P 0.96516, R 0.54851, F1 0.69949, confusion [[30140,10],[228,277]]. Mean F1 **0.7749629467**, compared with the released baseline 0.795157 under the recorded local protocol. E8 was the strongest *participant-trained* checkpoint prior to E9 but still trails the released baseline by ~0.0202. This public split has informed model decisions; do not claim a blind test.

Artifacts remain in Kaggle, including `E8_results_metadata.zip`, best checkpoint and resume state; the repository does not yet host those files.

## E9-Fresh training and holdout results (21 November 2026)

E9-Fresh trained independently from `microsoft/codebert-base`; this is **not** a resumed E8 run. Training ended at 15,000 steps, with checkpoint at **13,000** chosen by internal pilot Mean F1. The fixed evaluation thresholds are [0.5,0.5] with 256-token truncation.

| Pilot task | F1 at selected step 13,000 |
|---|---:|
| Vulnerability | 0.850163 |
| Technical Debt | 0.661538 |
| **Mean F1** | **0.755851** |

| Clean internal holdout task (16,420 rows) | Precision | Recall | F1 | Confusion matrix [[TN, FP], [FN, TP]] |
|---|---:|---:|---:|---|
| Vulnerability | 0.900251 | 0.797075 | **0.845527** | [[10542,477],[1096,4305]] |
| Technical Debt | 0.993631 | 0.549296 | **0.707483** | [[16135,1],[128,156]] |
| **Mean** | — | — | **0.776505** | — |

Compared with E8's recorded clean holdout mean F1 of 0.770259, E9 is higher by about **0.00625** on nominally comparable within-project splits. Split identity and seed controls should be verified before treating this as a strictly paired experiment. **E9 public-split result:** 30,655 rows, 256-token evaluation, fixed thresholds [0.5,0.5]. Vulnerability P=0.9113738739, R=0.8051134103, F1=0.8549545743, confusion [[19816,787],[1959,8093]]. Debt P=0.9725085911, R=0.5603960396, F1=0.7110552764, confusion [[30142,8],[222,283]]. **Mean F1=0.7830049253.** Inference time=441.8847 seconds in the reported Kaggle session, not a controlled speed comparison. The released baseline's local mean F1 was 0.795157, approximately 0.01215 higher. The public split influenced development discussions; this is not a blind final evaluation.

## E3 internal generalization diagnostics (NOT the public split)

| Slice | Rows | Weakness F1 | Debt F1 | Mean F1 |
|---|---:|---:|---:|---:|
| Original internal holdout | 16,452 | 0.7794 | 0.6939 | 0.7366 |
| After pilot-overlap hash filtering | 16,420 | 0.7794 | 0.6925 | 0.7360 |
| Unseen-file subset of clean holdout | 854 | 0.7949 | 0.2857 | 0.5403 |

The unseen-file slice has only **18 actual debt positives**; its debt F1 is statistically unstable.

## Leakage audit

- Exact `Function` SHA-256 hashes: Train↔Pilot 0; Train↔Holdout 0; Pilot↔Holdout **30 unique hashes**, corresponding to **32 excluded holdout rows**.
- Same `Projectname` seen in all splits: **15 projects**.
- Shared unique `(Projectname, Filepath)` keys: Train↔Pilot 3,894; Train↔Holdout 9,919; Pilot↔Holdout 1,985.
- The clean holdout is **not unseen-project or unseen-file** evaluation. No near-duplicate audit or multiple-seed reproducibility verification has been completed.

## Interpretation

E9 improved on E8, E5 and E3 in the recorded 30,655-sample public evaluation but **did not beat** the released CodeBERT checkpoint. Weighted-loss benefits should not be presented as causally established across runs without matched initialization/sampling and multiple seeds.
