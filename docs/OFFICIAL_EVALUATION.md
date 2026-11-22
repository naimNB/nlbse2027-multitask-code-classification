# NLBSE 2027 Multitask Code Classification: official-reference evaluation

## Official sources

- [Tool-competition rules](https://nlbse2027.github.io/tools/)
- [Organizer challenge/instructions notebook](https://colab.research.google.com/drive/1b_EiXx5woyCrDntwbljfi-BwS9Dwvhoa)
- [Organizer CodeBERT reference baseline notebook](https://colab.research.google.com/drive/1q1fGPpU7uxaK1mUVHa3b2xJOtEwhWwLG)
- [Organizer task repository](https://github.com/nlbse2027/code-comment-classification)
- [Participant T4 evaluation notebook](../notebooks/E9_Colab_T4_reference_style_evaluation.ipynb)

## Dataset naming

The HF dataset named `NLBSE/nlbse27-code-comment-classification` exposes:
- `train`: **214,586** labeled functions;
- `test`: **30,655** labeled functions. Despite the HF split name, competition materials describe this as the **public validation** partition;
- organizer-hidden test: **61,311** functions, unavailable for participant evaluation.

The model input is the `Function` field, containing the normalized source-code function with any included comments. One model must output two binary labels in `[weakness/vulnerability, MAT/SATD]` order. The organizer explicitly permits fine-tuning a pretrained model on the public training split.

## Organizer reference baseline notebook: concrete settings

The publicly accessible `CodeBERT_baseline.ipynb` notebook, linked from the organizer instructions, uses:
- model `NLBSE/nlbse27-code-comment-classification-baseline`;
- `RobertaTokenizer`, `RobertaForSequenceClassification`;
- **512-token** maximum input length (with **global** padding in one tokenization call);
- **batch_size=600** in a DataLoader;
- **repetitions=10** of each forward pass inside `torch.profiler.profile(with_flops=True)`;
- `torch.cuda.amp.autocast()` for mixed precision;
- probability sigmoid and 0.5 threshold;
- average time as the sum of per-batch elapsed times divided by 10, and profiler-counted operation total divided by 10;
- scoring constants `max_avg_runtime=1000` and `max_avg_flops=3000000`.

The organizer challenge notebook specifies **Colab T4** for runtime comparison and the following weighted score:

```python
score = (
    0.6 * mean_f1
    + 0.2 * max((1000 - avg_runtime) / 1000, 0)
    + 0.2 * max((3000000 - avg_gflops) / 3000000, 0)
)
```

Note: the reference calls the profiler total 'GFLOPS' although the formula computes **billions of floating-point operations**, not **floating-point operations per second**.

The reference notebook lacks explicit CUDA synchronization around its clock measurements and may run out of T4 memory at batch size 600. Our standalone notebook adds synchronization and automatically falls back to smaller batches when the initial memory probe fails. Thus its timing and derived score are **local reference-style estimates, not an official ranking**.

## Historical local E9 metrics use a different protocol

Earlier E9 public evaluations used `max_length=256`, dynamic per-batch padding, batch size 16, no mixed precision requirement, and a single (not repeated) pass. Hosted E9 metrics exactly replicated:

| Task | Precision | Recall | F1 |
|---|---:|---:|---:|
| Vulnerability | 0.9113738739 | 0.8051134103 | 0.8549545743 |
| SATD | 0.9725085911 | 0.5603960396 | 0.7110552764 |
| Mean | — | — | **0.7830049253** |

These are legitimate local **public-validation** metrics. They do not directly provide the reference's 512-token F1 or efficiency score.

The organizer's own README reports a baseline mean F1 of approximately **0.910**, while our earlier local evaluation of the released baseline checkpoint at **256 tokens** gave **0.795157**. Their **512-token** tokenizer/batching/precision setup differs substantially. This is a plausible explanation for the discrepancy but remains **unconfirmed** until the released baseline is evaluated under matched conditions. Do not report 0.795157 as the organizer's published baseline score.

## Next procedure

1. Open [E9 Colab T4 reference-style notebook](../notebooks/E9_Colab_T4_reference_style_evaluation.ipynb) in Google Colab with a T4 GPU and run top-to-bottom. Save its JSON output.
2. If possible, copy the notebook, change `MODEL_ID` to `NLBSE/nlbse27-code-comment-classification-baseline`, and repeat using **exactly the same** settings.
3. Document the actual batch size, GPU, elapsed time, profiler-counted GFLOPs, fixed thresholds, and 512-token public-validation metrics.
4. Use 512-token results only after measurement; do not fabricate them or silently replace the 256-token table.
5. Confirm the competition submission form and produce a non-anonymous 2–4-page ICSE-formatted PDF with a model, code and reproduction links.
6. The final competition ranking requires the organizer's **hidden test**; no local validation score is an official leaderboard score.

Do not undertake additional parameter tuning on the labeled public split without recording that it has informed model selection.
