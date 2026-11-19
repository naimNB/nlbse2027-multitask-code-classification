# Recorded experiments (as of 20 November 2026)

**Do not mix pilot, holdout and public-split scores when ranking models.** The recorded experiments were mostly single-seed runs; E0–E3 and E5 do not constitute a fully controlled ablation.

## Public split — 30,655 rows, 256 tokens, thresholds [0.5, 0.5]

| Model | Weakness P | Weakness R | Weakness F1 | Debt P | Debt R | Debt F1 | Mean F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Official released baseline | 0.9325 | 0.8260 | 0.8760 | 0.9727 | 0.5644 | 0.7143 | 0.7952 |
| E3 weighted BCE, 2,000 steps | 0.8495 | 0.7268 | 0.7834 | 0.9745 | 0.5307 | 0.6872 | 0.7353 |
| E5 weighted BCE, best at step 4,000 | 0.8509 | 0.7898 | 0.8192 | 0.9926 | 0.5327 | 0.6933 | 0.7563 |

Timing in the local earlier evaluation: released baseline ~414.16 seconds and E3 ~417.77 seconds for the public split. No same-procedure E5 timing measurement is recorded. These timings are not the organizer's official runtime/GFLOPs ranking.

## Training and pilot experiments

| Experiment | Configuration | Pilot weakness F1 | Pilot debt F1 | Pilot mean F1 | Note |
|---|---|---:|---:|---:|---|
| E0 | Standard BCE, 500 steps | 0.7241 | 0.0000 | 0.3620 | Fixed 0.5 threshold |
| E1 | Weighted BCE [1,10], 500 steps | 0.6851 | 0.0000 | 0.3425 | Fixed 0.5 threshold |
| E2 | Standard BCE, 2,000 steps | 0.7745 | 0.0000 | 0.3873 | Fixed 0.5 threshold |
| E3 | Weighted BCE [1,10], 2,000 steps | 0.7814 | 0.6080 | 0.6947 | Fixed 0.5 threshold |
| E5 | Weighted BCE [1,10], 6,000 max steps; best checkpoint 4,000 | 0.8176 | 0.6080 | 0.7128 | Fixed 0.5 threshold |
| E6 | Post-hoc threshold search on E5 pilot | 0.8200 | 0.6080 | 0.7140 | Thresholds [0.43, 0.99]; exploratory only |
| E7 | Linear warmup/decay candidate | — | — | — | No reported run/result yet |

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

E5 improved on E3 in the recorded 30,655-sample public evaluation but **did not beat** the released CodeBERT checkpoint. Weighted-loss benefits should not be presented as causally established across runs without matched initialization/sampling and multiple seeds.
