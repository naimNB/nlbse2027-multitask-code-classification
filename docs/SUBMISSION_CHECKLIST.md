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

- [ ] Open the 4-page Overleaf IEEE manuscript and review every section and bibliography entry.
- [ ] Ensure the main results comparison prominently uses the matched **512-token** E9 and baseline scores above.
- [ ] **Figure protocol audit:** previously prepared confusion matrices and model-comparison figure were generated at **256 tokens**. Either redraw them for 512 tokens using the correct matrices below, or explicitly retain and caption them as historical 256-token diagnostics. Do **not** label them as 512-token matrices.
- [ ] For a new E9 512-token confusion matrix: vulnerability `[[19945,658],[1184,8868]]`; SATD `[[30143,7],[103,402]]`. Baseline matrices: vulnerability `[[20031,572],[650,9402]]`, SATD `[[30141,9],[100,405]]`. Label axes actual/predicted and row order negative/positive.
- [ ] Distinguish internal pilot validation (used for checkpoint selection), labeled public-validation (HF `test`), and organizer-hidden test (never accessed).
- [ ] Ensure figures are legible at final PDF column width, captions accurately describe datasets/protocols, and all text/tables stay within margins.
- [ ] Check IEEE `\\documentclass[10pt,conference]{IEEEtran}` (no `compsoc` options), final PDF length 2–4 pages **including references**, non-anonymous author details, proper citations and accessible GitHub/HF links.
- [ ] Confirm that the submitted code/notebook can run the **512-token** evaluation using the public checkpoint; the stored matched Colab notebook is provided, but a one-command inference entrypoint suitable for organizers should be reviewed against their full instructions.
- [ ] Open the official Google Form and verify any form-specific fields/attachments. Upload the actual finished PDF and required links **only after reviewing the filled form**.
- [ ] Retain submission confirmation/email/receipt.

**Do not claim a submission has been completed until the official form confirms it.**
