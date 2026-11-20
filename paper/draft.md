# Investigating Imbalance-Aware Multitask Code Classification with CodeBERT

**Working paper draft — not submission ready**

**Author:** Md Naim Babu  
**Affiliation:** Department of Computer Science and Engineering, Pundra University of Science & Technology, Bogura, Bangladesh

## Abstract

Multitask code classification aims to identify software weaknesses and self-admitted technical debt (SATD) from source-code functions. The two tasks have different label prevalence: in the analyzed 214,586-example training dataset, technical-debt positives comprise only about 1.65%. We study CodeBERT fine-tuning with standard and positively weighted binary cross-entropy under restricted optimization budgets. On a 30,655-example public evaluation split with fixed 0.5 thresholds and locally standardized 256-token inference, the weighted-loss 10,000-step checkpoint (E8), with linear warmup and learning-rate decay, achieves F1 of 0.8504 for weakness identification and 0.6995 for technical debt (mean F1 0.7750). A released baseline checkpoint evaluated under the same local protocol achieves mean F1 0.7952. We also investigate threshold sensitivity and shared-file generalization limitations. These observations describe preliminary empirical trade-offs; we do **not** claim an improvement over the released baseline or official hidden-test performance.

## 1. Introduction

Detecting both potential weaknesses and self-admitted maintenance debt from source-code functions is challenging, especially when the prevalence of the latter label is low. We study whether positive-class weighting and longer fine-tuning budgets yield useful task-wise changes while retaining a common CodeBERT encoder. This work reports an empirical analysis rather than a novel architecture.

## 2. Experimental methodology

We use `microsoft/codebert-base` with two binary output logits, corresponding to weakness detection and MAT/SATD. Weighted configurations apply `BCEWithLogitsLoss` with positive weights [1,10]. The recorded E3 run used 2,000 optimizer steps. E5 allowed up to 6,000 steps, with a checkpoint selected at step 4,000 based on mean F1 over 5,000 internal pilot examples. E8 used the same positive-class weighting with 1,000-step warmup and linear decay across 10,000 steps; the pilot-selected checkpoint was at step 10,000. These experiments are not a fully controlled causal ablation. Our local public-split evaluation uses a fixed 0.5 decision threshold for each task and truncates to at most 256 tokens. Exact historical split indices and dependency revisions remain to be exported from Kaggle.

## 3. Results

| Checkpoint | Weakness F1 | Debt F1 | Mean F1 |
|---|---:|---:|---:|
| Released baseline | **0.8760** | **0.7143** | **0.7952** |
| E3, weighted BCE, 2,000 steps | 0.7834 | 0.6872 | 0.7353 |
| E5, weighted BCE, best step 4,000 | 0.8192 | 0.6933 | 0.7563 |
| **E8, weighted BCE + schedule, 10,000 steps** | **0.8504** | **0.6995** | **0.7750** |

All values are from the **same local evaluation procedure** on the 30,655-example public split, not competition hidden-test scores. E8 improved over E3 and E5 but did not surpass the released baseline. E8's clean internal holdout on 16,420 rows reached vulnerability F1 0.8435 and debt F1 0.6970 (mean F1 0.7703), but this within-project set cannot establish generalization to unseen projects.

An E3 internal duplicate-filtered holdout yielded weakness F1 0.7794, debt F1 0.6925 and mean F1 0.7360. In a small unseen-file subset (854 rows, only 18 debt positives), debt F1 fell to 0.2857. This is a diagnostic rather than a conclusive generalization result.

## 4. Discussion and threats to validity

The experiments use small training budgets relative to the source dataset, largely single-run results, and pilot-based checkpoint selection. Differences in initialization and example ordering limit causal interpretation of cross-run comparisons. Exact code hashes do not overlap between training and validation in the reported audit, but the internal splits share all 15 projects and many source-file identities. The public split was inspected during model development, and so must not be described as untouched final evaluation. The low prevalence and limited positive counts complicate confidence in subset estimates. Official hidden-test evaluation and computational-efficiency scoring remain unreported.

## 5. Conclusion

Under the local protocol, the 10,000-step weighted scheduled run has the highest mean F1 among our tested checkpoints, while debt performance remains constrained by recall. The released baseline performs better overall. Future work includes matched-seed ablation studies, file/project-disjoint evaluation and calibration assessment.

## References (to complete)

1. NLBSE 2027 Multitask Code Classification official repository: https://github.com/nlbse2027/code-comment-classification
2. Released baseline model: https://huggingface.co/NLBSE/nlbse27-code-comment-classification-baseline
3. Feng et al., CodeBERT: A Pre-Trained Model for Programming and Natural Languages (2020): https://arxiv.org/abs/2002.08155

**Before submission:** confirm NLBSE page limits/template, add proper scholarly citations and artifact links, and reconcile terminology with official competition rules.
