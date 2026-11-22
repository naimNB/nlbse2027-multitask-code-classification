# Investigating Imbalance-Aware Multitask Code Classification with CodeBERT

**Working paper draft — not submission ready**

**Author:** Md Naim Babu  
**Affiliation:** Department of Computer Science and Engineering, Pundra University of Science & Technology, Bogura, Bangladesh

## Abstract

Multitask code classification aims to identify software weaknesses and self-admitted technical debt (SATD) from source-code functions. The two tasks have different label prevalence: in the analyzed 214,586-example training dataset, technical-debt positives comprise only about 1.65%. We study CodeBERT fine-tuning with standard and positively weighted binary cross-entropy under restricted optimization budgets. On a 30,655-example public evaluation split with fixed 0.5 thresholds and locally standardized 256-token inference, the independently initialized weighted-loss 15,000-step run (E9-Fresh), with a pilot-selected checkpoint at 13,000 steps, achieves F1 of 0.8550 for weakness identification and 0.7111 for technical debt (mean F1 0.7830). A released baseline checkpoint evaluated under the same local protocol achieves mean F1 0.7952. We also investigate threshold sensitivity and shared-file generalization limitations. These observations describe preliminary empirical trade-offs; we do **not** claim an improvement over the released baseline or official hidden-test performance.

## 1. Introduction

Detecting both potential weaknesses and self-admitted maintenance debt from source-code functions is challenging, especially when the prevalence of the latter label is low. We study whether positive-class weighting and longer fine-tuning budgets yield useful task-wise changes while retaining a common CodeBERT encoder. This work reports an empirical analysis rather than a novel architecture.

## 2. Experimental methodology

We use `microsoft/codebert-base` with two binary output logits, corresponding to weakness detection and MAT/SATD. Weighted configurations apply `BCEWithLogitsLoss` with positive weights [1,10]. The recorded E3 run used 2,000 optimizer steps. E5 allowed up to 6,000 steps, with a checkpoint selected at step 4,000 based on mean F1 over 5,000 internal pilot examples. E8 used the same positive-class weighting with 1,000-step warmup and linear decay across 10,000 steps; the pilot-selected checkpoint was at step 10,000. E9-Fresh ran up to 15,000 steps with 1,500-step warmup and linear decay; the pilot-selected checkpoint was at 13,000 steps. These experiments are not a fully controlled causal ablation. Our local public-split evaluation uses a fixed 0.5 decision threshold for each task and truncates to at most 256 tokens. The E9 run configuration records dataset-split fingerprints and dependency versions; however, its upstream dataset revision and complete train/validation row identifiers were not pinned.

**Evaluation terminology:** The Hugging Face split named `test` (30,655 labeled rows) is the competition's **public validation** set. The organizer retains a separate 61,311-row hidden test. Our reported E3–E9 results use 256-token local evaluation; the organizer reference baseline notebook uses 512 tokens and different batching/precision. Its published ~0.910 baseline Mean F1 is not directly comparable with our separate 256-token baseline checkpoint evaluation of 0.7952 without reconciliation. A T4 reference-style 512-token run is pending and documented at `docs/OFFICIAL_EVALUATION.md`.

## 3. Results

| Checkpoint | Weakness F1 | Debt F1 | Mean F1 |
|---|---:|---:|---:|
| Released baseline | **0.8760** | **0.7143** | **0.7952** |
| E3, weighted BCE, 2,000 steps | 0.7834 | 0.6872 | 0.7353 |
| E5, weighted BCE, best step 4,000 | 0.8192 | 0.6933 | 0.7563 |
| E8, weighted BCE + schedule, 10,000 steps | 0.8504 | 0.6995 | 0.7750 |
| **E9-Fresh, weighted BCE + schedule, best step 13,000** | **0.8550** | **0.7111** | **0.7830** |

All values are from the **same local evaluation procedure** on the 30,655-example public split, not competition hidden-test scores. The E9 column was independently replicated from the uploaded Hugging Face model in a fresh Kaggle session. The organizers' separate README reports a baseline mean F1 near 0.910, unlike our local baseline checkpoint evaluation of 0.7952; that discrepancy has not been reconciled and neither number should be confused with an E9 hidden-test result. E9 improved over E3, E5 and E8 but did not surpass the released baseline. Its clean internal holdout reached vulnerability F1 0.8455 and debt F1 0.7075 (mean F1 0.7765); that set is within-project and not an independent unseen-project evaluation. E8's clean internal holdout on 16,420 rows reached vulnerability F1 0.8435 and debt F1 0.6970 (mean F1 0.7703), but this within-project set cannot establish generalization to unseen projects.

An E3 internal duplicate-filtered holdout yielded weakness F1 0.7794, debt F1 0.6925 and mean F1 0.7360. In a small unseen-file subset (854 rows, only 18 debt positives), debt F1 fell to 0.2857. This is a diagnostic rather than a conclusive generalization result.

Figure 1 (pilot F1 progression): [SVG figure](../figures/e9_pilot_f1.svg). Figure 2 (E9 public-split confusion matrices): [SVG figure](../figures/e9_public_confusion_matrices.svg). These are descriptive figures; they do not represent hidden-test results.

### 3.1 Reference-style 512-token evaluation (new, separate protocol)

On Colab Tesla T4, the independently hosted E9 checkpoint was evaluated on the same 30,655 public-validation rows using max length 512, global padding to length 512, batch size 600, FP16 autocast, 10 repeated inference passes and fixed thresholds 0.5. It achieved vulnerability precision 0.9309258870, recall 0.8822124950, F1 **0.9059148023**; SATD precision 0.9828850856, recall 0.7960396040, F1 **0.8796498906**; **mean F1 0.8927823465**. Confusion matrices: vulnerability [[19945,658],[1184,8868]], SATD [[30143,7],[103,402]]. Local reference formula score: 0.7098832194, with synchronized average runtime 240.0944 s and profiler-counted GFLOPs 2,666,509.7132. This is a *public-validation, local reference-style measurement*, not the organizer hidden-test or official ranking. It changes length, padding, batching and precision simultaneously versus the historical 256-token table; improvements cannot be attributed to sequence length alone. The organizer-reported baseline mean F1 (~0.910) requires a matched T4 run before direct model ranking.

## 4. Discussion and threats to validity

The E9 experiment uses 120,000 distinct training examples sampled in one fixed randomized pass from 193,072 internal training rows, with a pilot-selected checkpoint. The experiments use partial training budgets, largely single-run results, and pilot-based checkpoint selection. Differences in initialization and example ordering limit causal interpretation of cross-run comparisons. Exact code hashes do not overlap between training and validation in the reported audit, but the internal splits share all 15 projects and many source-file identities. The public split was inspected during model development, and so must not be described as untouched final evaluation. The low prevalence and limited positive counts complicate confidence in subset estimates. Official hidden-test evaluation and computational-efficiency scoring remain unreported.

## 5. Conclusion

On the 512-token reference-style public-validation protocol, E9-Fresh obtains mean F1 0.8928. Under the separate historical 256-token local protocol, the 15,000-step E9-Fresh run has the highest mean F1 among our tested checkpoints, while debt performance remains constrained by recall. The released baseline performs better overall. Future work includes matched-seed ablation studies, file/project-disjoint evaluation and calibration assessment.

## Model artifact

The participant reports a successful upload of the E9 selected checkpoint to [Hugging Face](https://huggingface.co/naimNB/nlbse2027-e9-codebert), commit `33031d7072989699bd27a25284b60d81b396b26b`. Unauthenticated download and basic CUDA inference were verified in a new Kaggle notebook (two-logit output); the hosted checkpoint was then independently re-evaluated on all 30,655 public examples and exactly matched the archived vulnerability and SATD P/R/F1 metrics and confusion matrices. An organizer-compatible inference wrapper remains pending. Include the link in the submission manuscript only with these qualifications until verification completes.

## References (to complete)

1. NLBSE 2027 Multitask Code Classification official repository: https://github.com/nlbse2027/code-comment-classification
2. Released baseline model: https://huggingface.co/NLBSE/nlbse27-code-comment-classification-baseline
3. Feng et al., CodeBERT: A Pre-Trained Model for Programming and Natural Languages (2020): https://arxiv.org/abs/2002.08155

**Before submission:** confirm NLBSE page limits/template, add proper scholarly citations and artifact links, and reconcile terminology with official competition rules.
