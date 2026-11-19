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
- [ ] Export E7 notebook and actual run outputs (training completed on Kaggle; notebook/checkpoint not yet copied to repository).
- [ ] Exact dataset revision, dataset split indices or reproducible row IDs, hash/label conflict policy.
- [ ] Per-model predictions and metrics artifacts, checked against public split.
- [ ] A controlled same-seed comparison or plainly documented limitations.
- [ ] Official inference entrypoint, efficiency measurement, organizer format and paper template verification.
- [ ] Paper review, correct author name and affiliation, citations, and final PDF.

## Integrity and privacy

Never commit raw datasets, Kaggle tokens, credentials, `.env` secrets, or 500MB model weights. Do not claim that a checkpoint is reproducible or publicly downloadable unless it has been actually uploaded and tested. Published GitHub notebooks should have no private paths or secrets.
