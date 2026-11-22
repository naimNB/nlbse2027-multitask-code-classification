---
language:
- en
base_model: microsoft/codebert-base
tags:
- code-classification
- multi-label-classification
- codebert
- vulnerability-detection
- self-admitted-technical-debt
datasets:
- NLBSE/nlbse27-code-comment-classification
model-index:
- name: NLBSE 2027 E9-Fresh CodeBERT
  results: []
---

# NLBSE 2027 — E9-Fresh CodeBERT (Vulnerability + SATD)

An **independent participant-trained model** for the NLBSE 2027 Multitask Code Classification Tool Competition. It predicts two labels from a source-code function: **vulnerability/weakness** (output index 0) and **self-admitted technical debt (SATD/MAT)** (output index 1).

**This is not an official organizer model**, and the scores below are **local public-split evaluations**, not a hidden-test or official leaderboard result.

## Model details

- Architecture: `microsoft/codebert-base` shared encoder with two independent sequence-classification logits.
- Input: dataset `Function` field (formatted source-code function, including any comments).
- Model head output order: `[vulnerability, SATD]`.
- Inference: sigmoid on each logit, fixed thresholds `[0.5, 0.5]`.
- Maximum input length for reported metrics: **256 tokens**.
- Fine-tuning: weighted binary cross-entropy with positive-class weights `[1.0, 10.0]`, batch size 8, peak learning rate `2e-5`, weight decay `0.01`, linear learning-rate decay and 1,500 warmup steps.
- Training: fresh pretrained CodeBERT initialization, 15,000 optimization steps, checkpoint **selected at step 13,000 using internal pilot validation**. This run is **not** a continuation of E8.

## Reference-style evaluation on Colab Tesla T4: 512 tokens

A new independently executed reference-style evaluation of this **same, already-trained checkpoint** on all 30,655 labeled public-validation functions used global padding, maximum input length 512, batch size 600, FP16 autocast, 10 repeated forward passes and fixed sigmoid thresholds of 0.5.

| Task | Precision | Recall | F1 |
|---|---:|---:|---:|
| Vulnerability | 0.9309258870 | 0.8822124950 | 0.9059148023 |
| SATD | 0.9828850856 | 0.7960396040 | 0.8796498906 |
| **Mean F1** | — | — | **0.8927823465** |

Confusion matrices: vulnerability `[[19945,658],[1184,8868]]`; SATD `[[30143,7],[103,402]]`. Average 10-repeat synchronized inference time: **240.0944 seconds**; average profiler-counted GFLOPs: **2,666,509.7132**; **local reference-formula score 0.7098832194**. This is **not an official hidden-test result or organizer efficiency ranking**. The reported official baseline Mean F1 (~0.910) has not yet been reproduced under matched settings. [Full experimental JSON](https://github.com/naimNB/nlbse2027-multitask-code-classification/blob/main/results/e9/colab_t4_reference_style_512_metrics.json).

**The 256-token results below are from a different local protocol, not a direct matched baseline comparison.** No retraining occurred between these evaluations. Changes to input length, padding, batch size and precision occurred together, so the cause of the score gap cannot be isolated.

## Evaluation: public split (30,655 examples)

The historical 256-token evaluation was run with the open [evaluation script](https://github.com/naimNB/nlbse2027-multitask-code-classification/blob/main/scripts/evaluate_public.py), `max_length=256` and both thresholds set to `0.5`.

| Task | Precision | Recall | F1 |
|---|---:|---:|---:|
| Vulnerability | 0.9113738739 | 0.8051134103 | 0.8549545743 |
| SATD | 0.9725085911 | 0.5603960396 | 0.7110552764 |
| **Mean F1** | — | — | **0.7830049253** |

Confusion matrices (rows actual negative/positive, columns predicted negative/positive):
- Vulnerability: `[[19816,787],[1959,8093]]`
- SATD: `[[30142,8],[222,283]]`

The hosted model was re-downloaded on a **new Kaggle GPU notebook without Hugging Face authentication** and reproduced all recorded public-split task precision, recall, F1 and confusion-matrix counts **exactly**. Measured local evaluation time in that session was **457.19 s**; this is **not** the official time/GFLOPs benchmark.

## Example usage

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_id = "naimNB/nlbse2027-e9-codebert"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id).eval()

code = "int f(int x) { // FIXME: handle edge cases\n return x; }"
inputs = tokenizer(code, max_length=256, truncation=True, return_tensors="pt")

with torch.inference_mode():
    logits = model(**inputs).logits
    probabilities = torch.sigmoid(logits)
    predictions = (probabilities >= 0.5).int()

print("Probability [vulnerability, SATD]:", probabilities.tolist())
print("Predictions:", predictions.tolist())
```

## Reproducibility

- [Training notebook](https://github.com/naimNB/nlbse2027-multitask-code-classification/blob/main/notebooks/E9_fresh_15k_codebert.ipynb)
- [Evaluation script](https://github.com/naimNB/nlbse2027-multitask-code-classification/blob/main/scripts/evaluate_public.py)
- [Run configuration](https://github.com/naimNB/nlbse2027-multitask-code-classification/blob/main/results/e9/run_config.json)
- [Recorded metrics](https://github.com/naimNB/nlbse2027-multitask-code-classification/tree/main/results/e9)
- [Research repository](https://github.com/naimNB/nlbse2027-multitask-code-classification)

## Limitations and responsible use

- This is an experimental research classifier, **not** a production security audit system or substitute for expert code review.
- SATD recall is approximately **0.5604** on the public evaluation split; it misses a substantial fraction of positive SATD functions.
- Training and internal validation contain shared projects and source-file identifiers. Generalization to unseen projects remains unproven.
- The public split was consulted during development; it is not an untouched test.
- The experiment is single-seed. Full independent retraining and the competition's hidden-test and efficiency evaluation have **not** been verified.
- A separate published organizer baseline score is not directly reconciled with the locally re-evaluated baseline checkpoint; cross-protocol rankings should be treated cautiously.

## Attribution

- Dataset/competition: [NLBSE 2027 tool competition](https://github.com/nlbse2027/code-comment-classification)
- Pretrained architecture: [CodeBERT](https://arxiv.org/abs/2002.08155)

Author: **Md Naim Babu**, Department of Computer Science and Engineering, Pundra University of Science & Technology, Bangladesh.
