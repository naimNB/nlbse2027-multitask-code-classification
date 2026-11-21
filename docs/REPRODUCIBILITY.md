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
- E9-Fresh: 15,000 training steps from pretrained CodeBERT (NOT a resume of E8), 1,500 warmup steps, best step 13,000 by pilot mean F1. Public evaluation (30,655 rows): vulnerability F1 0.8549545743, debt F1 0.7110552764, mean F1 0.7830049253; thresholds [0.5,0.5], max length 256, observed inference wall time 441.88 s. Metadata and notebook are now published; model weights still require public artifact hosting and a load test.
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
- [ ] Publish and independently load-test an accessible E9 best-model checkpoint (weights currently backed up locally, not hosted publicly).
- [ ] Preserve original E9 metadata ZIP and 15-step history, and publish or attach these as supplementary evidence.
- [ ] Capture exact source-dataset revision and confirm split membership against saved fingerprints.
- [ ] Archive optimizer resume state separately only if later training continuation is necessary.
- [ ] Export E8 notebook, pilot/holdout/public metrics JSON, run config and best checkpoint (large model files to external hosting).
- [ ] Export E7 notebook and actual run outputs (training completed on Kaggle; notebook/checkpoint not yet copied to repository).
- [ ] Exact dataset revision, dataset split indices or reproducible row IDs, hash/label conflict policy.
- [ ] Per-model predictions and metrics artifacts, checked against public split.
- [ ] A controlled same-seed comparison or plainly documented limitations.
- [ ] Official inference entrypoint, efficiency measurement, organizer format and paper template verification.
- [ ] Paper review, correct author name and affiliation, citations, and final PDF.

## Integrity and privacy

Never commit raw datasets, Kaggle tokens, credentials, `.env` secrets, or 500MB model weights. Do not claim that a checkpoint is reproducible or publicly downloadable unless it has been actually uploaded and tested. Published GitHub notebooks should have no private paths or secrets.

## E9 captured environment and split fingerprints

From the uploaded E9 `run_config.json`: Python notebook environment with PyTorch `2.11.0+cu130`, Transformers `5.20.2`, Datasets `4.8.5`, scikit-learn `1.6.1`, NumPy `2.1.3`, and pandas `2.3.3`. Seed 42; training used a fixed random permutation without replacement, 15,000 batches of eight (120,000 distinct training rows). Training split SHA-256 fingerprint: `3cddf4a4a6931c5675b9c1f6c6769eafec0de0e5afd1f0ba25c18f79f1d7f4f2`; pilot: `563363315b571ed7da81dd91c03bff117eefafde84ed48ff2054648b5d9bd09b`. The original source dataset revision was **not pinned** in the notebook, so identical checksums are necessary but cannot alone establish exact reproducibility in a future different environment.
