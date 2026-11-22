# Reproducibility and submission checklist

## Data

- Source: https://huggingface.co/datasets/NLBSE/nlbse27-code-comment-classification
- Dataset columns: `Projectname`, `Filepath`, `Function`, `Label`.
- Label order: weakness/vulnerability (index 0), developer-admitted technical debt / MAT (index 1).
- Original train: 214,586 rows; original public test: 30,655 rows.
- Historical internal train: 193,072 rows. Pilot validation: 5,000 rows.
- Historical split used group-aware exact-code hashes and label stratification. **Exact source code, dataset revision, saved split indices and split filenames must be exported from the Kaggle runs before claiming exact reproduction.**
- Do not recreate E3/E5 splits with a different library revision and assume identical rows. Compare stored indices/hashes and row counts.

## Model and evaluation

- Encoder: `microsoft/codebert-base`.
- Two logits, `problem_type='multi_label_classification'`.
- E3/E5 weighted loss: `torch.nn.BCEWithLogitsLoss(pos_weight=tensor([1., 10.]))`.
- E3: 2,000 steps; E5: 6,000 maximum and checkpoint chosen at 4,000.
- Reported learning rate: 2e-5; weight decay: 0.01; batch size: 8; maximum length: 256. Verify these with saved run configs.
- E7: weighted BCE with linear learning-rate warmup/decay; 6,000 steps completed, best checkpoint at step 6,000; pilot mean F1 0.7134. Public-split evaluation pending. Training duration 45.87 minutes. Verify actual warmup settings using the saved run configuration.
- E8: 10,000 training steps, 1,000 linear warmup steps, peak LR 2e-5, weighted BCE [1,10], best step 10,000 on pilot. E8 local public mean F1 0.7749629467 (vulnerability F1 0.8504309439, debt F1 0.6994949495); 30,655 samples, 486.06-second inference wall time, and fixed [0.5,0.5] thresholds. Kaggle artifact export still pending.
- E9-Fresh: 15,000 training steps from pretrained CodeBERT (NOT a resume of E8), 1,500 warmup steps, best step 13,000 by pilot mean F1. Public evaluation (30,655 rows): vulnerability F1 0.8549545743, debt F1 0.7110552764, mean F1 0.7830049253; thresholds [0.5,0.5], max length 256, observed inference wall time 441.88 s. Metadata and notebook are now published; model weights are hosted publicly and independently load-tested.
- Local public-set comparison: 256-token truncation, batch size 16 at inference, sigmoid threshold 0.5 for both tasks.
- Report binary precision, recall, F1 separately for each label; mean F1 = arithmetic mean of the two task F1 scores.
- The organizer may require a different inference wrapper and resource scoring. Match the official competition contract before submission.

## Run evaluation

```bash
python scripts/evaluate_public.py --model-dir /path/to/best_model
# or evaluate the released baseline checkpoint:
python scripts/evaluate_public.py --model-dir NLBSE/nlbse27-code-comment-classification-baseline
```

Kaggle's GPU PyTorch is typically sufficient; do not overwrite it blindly with a CPU-only build.

## Artifacts still to export from Kaggle

- [ ] E3 and E5 complete notebook exports, with outputs carefully scrubbed and organized.
- [ ] E5 best checkpoint, tokenizer and `run_config.json` (host large files outside Git).
- [x] Publish cleaned E9-Fresh training notebook, run configuration including split fingerprints, pilot metrics, clean holdout metrics and public-split metrics in GitHub.
- [x] Upload E9 best checkpoint to Hugging Face: https://huggingface.co/naimNB/nlbse2027-e9-codebert (commit 33031d7072989699bd27a25284b60d81b396b26b).
- [x] Publish E9 Hugging Face model card, including evaluation, limitations and sample inference code (commit 6331998768f9112f440ca029429640281f4df1b8).
- [x] Updated the public Hugging Face model card with the matched 512-token T4 baseline comparison (user-confirmed upload commit [`f5df3b8bdab84a086d4c23311dd71eb051ef4452`](https://huggingface.co/naimNB/nlbse2027-e9-codebert/commit/f5df3b8bdab84a086d4c23311dd71eb051ef4452)).

- [x] Independently load-test uploaded checkpoint from Hugging Face on a new Kaggle notebook with no HF token: CUDA inference succeeded, logits shape (1,2), and sigmoid probabilities were produced.
- [x] Re-run public-split evaluation from the hosted checkpoint in a fresh Kaggle notebook: 30,655 samples, fixed [0.5,0.5], max length 256, both task P/R/F1 and confusion matrices identical to recorded E9 outputs; elapsed time 457.1878 s (not controlled benchmarking).
- [ ] Preserve original E9 metadata ZIP and 15-step history, and publish or attach these as supplementary evidence.
- [ ] Capture exact source-dataset revision and confirm split membership against saved fingerprints.
- [ ] Archive optimizer resume state separately only if later training continuation is necessary.
- [ ] Export E8 notebook, pilot/holdout/public metrics JSON, run config and best checkpoint (large model files to external hosting).
- [ ] Export E7 notebook and actual run outputs (training completed on Kaggle; notebook/checkpoint not yet copied to repository).
- [ ] Exact dataset revision, dataset split indices or reproducible row IDs, hash/label conflict policy.
- [ ] Per-model predictions and metrics artifacts, checked against public split.
- [ ] A controlled same-seed comparison or plainly documented limitations.
- [x] Report local Colab T4 512-token reference-style public-validation metrics and profiler/timing estimate: see [512-token metrics](../results/e9/colab_t4_reference_style_512_metrics.json).
- [ ] Organizer-compatible inference wrapper and true organizer hidden-test efficiency/score verification (the local T4 score is not official).
- [x] Independently evaluate the released baseline under the same 512-token Colab T4 settings: Mean F1 0.9101860726, matching the organizers' reported ~0.910. JSON: [matched baseline metrics](../results/baseline/colab_t4_matched_512_metrics.json).
- [ ] Paper review, correct author name and affiliation, citations, and final PDF.

## Integrity and privacy

Never commit raw datasets, Kaggle tokens, credentials, `.env` secrets, or 500MB model weights. Do not claim that a checkpoint is reproducible or publicly downloadable unless it has been actually uploaded and tested. Published GitHub notebooks should have no private paths or secrets.

## E9 captured environment and split fingerprints

From the uploaded E9 `run_config.json`: Python notebook environment with PyTorch `2.11.0+cu130`, Transformers `5.20.2`, Datasets `4.8.5`, scikit-learn `1.6.1`, NumPy `2.1.3`, and pandas `2.3.3`. Seed 42; training used a fixed random permutation without replacement, 15,000 batches of eight (120,000 distinct training rows). Training split SHA-256 fingerprint: `3cddf4a4a6931c5675b9c1f6c6769eafec0de0e5afd1f0ba25c18f79f1d7f4f2`; pilot: `563363315b571ed7da81dd91c03bff117eefafde84ed48ff2054648b5d9bd09b`. The original source dataset revision was **not pinned** in the notebook, so identical checksums are necessary but cannot alone establish exact reproducibility in a future different environment.

## Hosted E9 checkpoint replication (22 November 2026)

The participant independently evaluated the public Hugging Face model [`naimNB/nlbse2027-e9-codebert`](https://huggingface.co/naimNB/nlbse2027-e9-codebert) using `scripts/evaluate_public.py` in a new Kaggle GPU notebook **without a Hugging Face access token**. The hosted checkpoint downloaded successfully and produced **bit-for-bit identical reported task metrics and confusion matrices** to the prior local-checkpoint public evaluation on 30,655 examples at max length 256 and thresholds `[0.5, 0.5]`:

| Task | Precision | Recall | F1 | Confusion matrix |
|---|---:|---:|---:|---|
| Vulnerability | 0.9113738739 | 0.8051134103 | 0.8549545743 | `[[19816,787],[1959,8093]]` |
| SATD | 0.9725085911 | 0.5603960396 | 0.7110552764 | `[[30142,8],[222,283]]` |
| **Mean** | — | — | **0.7830049253** | — |

Original local-checkpoint inference wall time: **441.8847 s**. Hosted-checkpoint inference wall time: **457.1878 s**. These are different sessions and do not establish a controlled speed comparison or official compute ranking. This confirms checkpoint portability and **evaluation replication**, not full training reproducibility, blind generalization or organizer hidden-test performance.

The competition organizer's README also reports a **different baseline evaluation score** (mean F1 approximately 0.910); our earlier locally evaluated baseline checkpoint gave 0.7952. The protocols/processing underlying that discrepancy have not been reconciled, so do not present the locally evaluated baseline score as the organizers' official score.

## E9 reference-style 512-token evaluation (Colab Tesla T4; 23 Nov 2026)

The participant executed the [reference-style T4 notebook](../notebooks/E9_Colab_T4_reference_style_evaluation.ipynb) on **all 30,655 labeled public-validation rows** using the publicly uploaded E9 model. Configuration: max_length=512, globally padded length 512, batch=600 (no OOM fallback), fp16 autocast, 10 repeated inference passes, thresholds [0.5,0.5], CUDA synchronization added for elapsed-time measurement.

| Task | Precision | Recall | F1 | Confusion matrix [[TN,FP],[FN,TP]] |
|---|---:|---:|---:|---|
| Vulnerability | 0.9309258870 | 0.8822124950 | **0.9059148023** | [[19945,658],[1184,8868]] |
| Technical debt / SATD | 0.9828850856 | 0.7960396040 | **0.8796498906** | [[30143,7],[103,402]] |
| **Mean** | — | — | **0.8927823465** | — |

**Local reference-formula efficiency estimate (not official):** 10 repeated passes took 2,400.9437 seconds total; reported average full-public-set runtime = **240.0944 seconds**; average profiler-counted operation total = **2,666,509.7132 GFLOPs**; combined local score = **0.7098832194**. The reference notebook's timer lacks explicit CUDA synchronization whereas ours synchronizes; do not treat this as an identical official measurement. Profiler-reported GFLOPs is an operation count, not throughput.

For contrast, the **same E9 checkpoint** had 256-token dynamic-batch-padding, non-fp16 local public-validation mean F1 **0.7830049253**. The new protocol raises mean F1 by about 0.1098 (vulnerability +0.0510, SATD +0.1686), but length, padding, batching and precision changed together. It does not isolate the benefit of 512-token truncation. No new training occurred. The competition's baseline README reports a separate mean F1 around 0.910; a **matched baseline run with this same T4 notebook is still pending**. The labeled public split is not the 61,311-example organizer hidden test.

JSON evidence: [E9 T4 512-token metrics](../results/e9/colab_t4_reference_style_512_metrics.json). Do not mix 512-token F1 with the old 256-token E3/E5/E8 baseline table as if settings were matched.

## Matched 512-token comparison: E9 versus released baseline (23 November 2026)

Both checkpoints were run in **separate Colab Tesla T4 executions** using the same reference-style script and settings: `max_length=512`, global padding to 512, batch size 600, FP16 autocast, 10 repeated forward passes, sigmoid thresholds [0.5,0.5], and explicit CUDA synchronization. Each run used all **30,655 public-validation rows**; neither is hidden-test evaluation.

| Measurement | E9-Fresh | Released baseline |
|---|---:|---:|
| Vulnerability precision | 0.9309258870 | 0.9426508923 |
| Vulnerability recall | 0.8822124950 | 0.9353362515 |
| **Vulnerability F1** | **0.9059148023** | **0.9389793269** |
| SATD precision | 0.9828850856 | 0.9782608696 |
| SATD recall | 0.7960396040 | 0.8019801980 |
| **SATD F1** | **0.8796498906** | **0.8813928183** |
| **Mean F1** | **0.8927823465** | **0.9101860726** |
| Average runtime per public split | 240.0944 s | 196.8109 s |
| Avg profiler-counted GFLOPs | 2,666,509.7132 | 2,666,509.7132 |
| **Local reference-formula score** | **0.7098832194** | **0.7289821579** |

Baseline confusion matrices: vulnerability `[[20031,572],[650,9402]]`; SATD `[[30141,9],[100,405]]`. E9 matrices: vulnerability `[[19945,658],[1184,8868]]`; SATD `[[30143,7],[103,402]]`.

The baseline exceeds E9 by **0.0174037 mean-F1 points** and **0.0190989 local combined-score points**. Nearly all of the mean-F1 difference comes from the vulnerability task (F1 gap **0.0330645**); the SATD F1 gap is **0.0017429**. The organizer README baseline mean F1 (~0.910) is now reproduced using a matched local 512-token protocol, explaining why its figure differed from an earlier **256-token** local baseline run (0.7952). Input length, padding, batch size and mixed precision all differed between the old and new protocols, so this is not an isolated sequence-length ablation.

Average run time is **43.28 s lower for baseline** in these two executions, but executions were separate rather than interleaved; do not interpret this as a controlled or official efficiency ranking. The added CUDA synchronization differs from the organizer's reference notebook. Both local combined scores are estimates and **not hidden-test or organizer leaderboard scores**.

Evidence: [E9 JSON](../results/e9/colab_t4_reference_style_512_metrics.json), [baseline JSON](../results/baseline/colab_t4_matched_512_metrics.json). The published baseline score discrepancy is reconciled at the level of the same measured mean F1, not by establishing an exclusive causal explanation for earlier protocol differences.
