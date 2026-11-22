# NLBSE 2027 — Multitask Code Classification submission readiness

**Current state:** model and model card are public, E9 and released baseline have been evaluated on 30,655 public-validation rows in matched local T4 conditions. **Competition form has not been submitted.**

## Authoritative competition instructions

- Official tool competition: https://nlbse2027.github.io/tools/
- Official ICSE-hosted competition description: https://conf.researchr.org/home/icse-2027/nlbse-2027
- **Specific competition submission form:** https://forms.gle/yx2CcKLYYBSjWoiJ8
- Competition paper/tool deadline: **27 November 2026, Anywhere on Earth (AoE)**.
- Manuscript: **2–4 pages including references**, follow ICSE 2027 formatting. Competition papers do **not** need to be double-blind.
- Distinguish from the **regular workshop** submission path (HotCRP and anonymization), which is not the tool competition's submission route.

Organizers require the paper to describe model architecture, preprocessing, training and tuning, validation results, and open-source implementation plus reproducibility instructions. Acceptance considers correctness, reliable reporting, and reproducibility, not merely achieving higher F1 than the released baseline.

## Validated research evidence

- [x] Participant Hugging Face model: https://huggingface.co/naimNB/nlbse2027-e9-codebert
- [x] Public model card updated with matched baseline comparison: commit `f5df3b8bdab84a086d4c23311dd71eb051ef4452`.
- [x] Training notebook: [E9 standalone training](../notebooks/E9_fresh_15k_codebert.ipynb).
- [x] Evaluation script: [scripts/evaluate_public.py](../scripts/evaluate_public.py).
- [x] E9 hosted checkpoint independently re-downloaded in Kaggle without authentication; public-validation F1 metrics and both confusion matrices reproduced exactly under the historical 256-token protocol.
- [x] [E9 Colab T4 512-token public-validation JSON](../results/e9/colab_t4_reference_style_512_metrics.json).
- [x] [Released-baseline matched Colab T4 512-token JSON](../results/baseline/colab_t4_matched_512_metrics.json).
- [x] Both measured with T4, 512-token global padding, FP16 autocast, batch 600, sigmoid thresholds 0.5, 10 repeats and explicit CUDA synchronization.

## Matched public-validation results (30,655 examples)

| Measurement | E9-Fresh | Released baseline |
|---|---:|---:|
| Vulnerability F1 | 0.9059148023 | 0.9389793269 |
| SATD F1 | 0.8796498906 | 0.8813928183 |
| Mean F1 | 0.8927823465 | 0.9101860726 |
| Avg synchronized inference time (s) | 240.0944 | 196.8109 |
| Avg profiler-counted GFLOPs | 2666509.7132 | 2666509.7132 |
| Local reference-formula score | 0.7098832194 | 0.7289821579 |

These are **not hidden-test results or official rankings**. Separate runs cannot establish precise causal conclusions about runtime. The historical 256-token F1=0.7830049253 is a different protocol, not a degradation of model weights.

## Still required before submitting

- [x] Re-review the IEEE manuscript source and rendered 4-page PDF for title, author, all sections, citations, figures and matched result data. The author has indicated the prior layout looks acceptable; the subsequent metric-table/citation revision still requires the author's quick final look.
- [x] Ensure the main results comparison prominently uses the matched **512-token** E9 and baseline scores above, with task precision, recall and F1, macro averages, and local efficiency metrics.
- [x] **Figure protocol audit for IEEE paper:** 512-token E9 confusion matrices and matched 512-token E9/baseline F1 comparison were redrawn from verified metrics. Training/pilot plots remain correctly labeled separately. The editable reviewed Overleaf source and PDF are prepared for author review; those files are not yet uploaded to this GitHub repository.
- [x] New E9 512-token confusion matrix documented and stored in [figures/e9_512_confusion_matrices.svg](../figures/e9_512_confusion_matrices.svg): vulnerability `[[19945,658],[1184,8868]]`; SATD `[[30143,7],[103,402]]`. Baseline matrices: vulnerability `[[20031,572],[650,9402]]`, SATD `[[30141,9],[100,405]]`. Label axes actual/predicted and row order negative/positive.
- [x] Separate the internal pilot validation (checkpoint selection), labeled public-validation (HF `test`) and organizer-hidden test (never accessed) throughout the polished README, results and protocol guide.
- [x] Compile and visually inspect the revised 4-page IEEE PDF: all four figures included, correct 512-token labels, captions, two results tables and no overfull-box warnings. Author must still inspect the final Overleaf render after any edit.
- [x] Format source with IEEE `\\documentclass[10pt,conference]{IEEEtran}` (no `compsoc`), reviewed PDF length 4 pages including references, author/affiliation shown, cited work and clickable GitHub/HF links. Final author approval before actual submission remains required.
- [x] Provide published model loading, a functional inference CLI at [scripts/predict.py](../scripts/predict.py) and a completed [512-token Colab reference-style notebook](../notebooks/E9_Colab_T4_reference_style_evaluation.ipynb). This establishes executable documentation, **not** an organizer-provided hidden-test inference contract or official runtime validation.
- [ ] Open the official Google Form and verify any form-specific fields/attachments. Upload the actual finished PDF and required links **only after reviewing the filled form**.
- [ ] Retain submission confirmation/email/receipt.

**Do not claim a submission has been completed until the official form confirms it.**

## 23 November 2026 final PDF review revision

The editable IEEEtran source and reviewed 4-page PDF have been regenerated after final verification of the official competition instructions. Improvements: the main matched-512-token results table now includes precision and recall for each task and their two-task arithmetic means (required in the organizer's reference instructions), the organizer-provided full NLBSE competition citation was added, and the PDF title and author metadata are populated. PDF dimensions are US Letter, title 24 pt, body from the unmodified 10 pt IEEEtran conference layout, with embedded Nimbus Roman (Times-compatible), **not** Microsoft's Times New Roman. Four figures remain correctly placed, linked code/model URLs are active and no page-boundary text clipping was detected. The final artifact is prepared in the conversation as a reviewed Overleaf ZIP and PDF; it is **not automatically in this GitHub repo or the official submission system**.

**Submission is still pending.** The official Google Form must receive the final approved PDF and required fields, and the user must save a confirmation/receipt. The form structure was not accessible in this review; do not guess its fields.

## 23 November 2026 manuscript QA

A new Overleaf-ready IEEE project and compiled 4-page PDF were generated in the active conversation. The revised Fig. 3 contains **512-token** E9 confusion matrices; Fig. 4 contains the **matched 512-token** E9 vs baseline F1 comparison. Fig. 1 is the *pilot validation* F1 progression and Fig. 2 is *logged training loss*. The original **256-token** checkpoint comparison remains separately identified as Table I; the matched **512-token** result is Table II. The PDF is still **unsubmitted**; the author must upload the approved final PDF using the tool competition's Google Form and retain its confirmation receipt.

## Repository polish (23 November 2026)

- [x] Submission-focused README with the **512-token matched** result displayed first, not the historical 256-token table.
- [x] Single-function/file/JSONL inference CLI and documented commands.
- [x] Lightweight JSON and confusion-matrix integrity tests.
- [x] GitHub Actions continuous verification (syntax, tests and CLI smoke checks).
- [x] Correctly labeled 512-token SVG plots and separate historical 256-token figure documentation.
- [x] CITATION.cff citation metadata and paper/README.md clarify manuscript status.
- [ ] A license has **not** been selected or applied; the author should decide whether to publish the code under a suitable open-source license. Do not silently assume or grant legal reuse rights.

**Form submission has not been verified in GitHub.** Keep the original submitted PDF and confirmation receipt separately.
