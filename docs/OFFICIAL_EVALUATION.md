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

The organizer's own README reports baseline mean F1 of approximately **0.910**. A released-baseline checkpoint evaluated locally at **256 tokens** gave **0.795157**. A matched **512-token T4** evaluation of that checkpoint has now measured **0.9101860726**, aligning with the organizer's reported score. The protocols differ in token length, padding, batching, and precision, whose individual effects were not isolated. Do not report 0.795157 as the organizer's published baseline score.

## Next procedure

1. Open [E9 Colab T4 reference-style notebook](../notebooks/E9_Colab_T4_reference_style_evaluation.ipynb) in Google Colab with a T4 GPU and run top-to-bottom. Save its JSON output.
2. Matched released-baseline 512-token evaluation is **completed** (see recorded JSON); rerun it only for reproducibility.
3. Document the actual batch size, GPU, elapsed time, profiler-counted GFLOPs, fixed thresholds, and 512-token public-validation metrics.
4. Use 512-token results only after measurement; do not fabricate them or silently replace the 256-token table.
5. Confirm the competition submission form and produce a non-anonymous 2–4-page ICSE-formatted PDF with a model, code and reproduction links.
6. The final competition ranking requires the organizer's **hidden test**; no local validation score is an official leaderboard score.

Do not undertake additional parameter tuning on the labeled public split without recording that it has informed model selection.

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
