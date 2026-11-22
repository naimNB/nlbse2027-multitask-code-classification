# Figures and evaluation protocols

This folder includes two **distinct** types of plots. Do not relabel historical results as 512-token metrics.

| File | What it represents |
|---|---|
| [e9_pilot_f1.svg](e9_pilot_f1.svg) | E9-Fresh **internal 5,000-row pilot validation** F1 by optimization step; checkpoint selected at step 13,000. |
| [e9_public_confusion_matrices.svg](e9_public_confusion_matrices.svg) | Historical **256-token** public-validation confusion matrices (30,655 labeled rows). |
| [e9_512_confusion_matrices.svg](e9_512_confusion_matrices.svg) | **512-token**, matched-protocol E9 public-validation confusion matrices. |
| [matched_512_model_comparison.svg](matched_512_model_comparison.svg) | Matched **512-token** F1 comparison, E9 versus released baseline; visual axis starts at **0.84**. |

Confusion matrices list actual labels as **rows** (negative, positive) and model predictions as **columns** (negative, positive).

**Verified 512-token E9 counts:**
- Vulnerability: `[[19945,658],[1184,8868]]`
- SATD: `[[30143,7],[103,402]]`

**Verified 512-token released-baseline counts:**
- Vulnerability: `[[20031,572],[650,9402]]`
- SATD: `[[30141,9],[100,405]]`

**Source of truth:** [E9 T4 metrics](../results/e9/colab_t4_reference_style_512_metrics.json) and [matched baseline T4 metrics](../results/baseline/colab_t4_matched_512_metrics.json). The 512-token runs use Tesla T4, 512-token global padding, batch 600, FP16 autocast and 10 repeated forward passes; they are **local public-validation measurements**, not organizer hidden-test scores.

The standalone competition paper's LaTeX archive contains separate publication-sized PDF/PNG figures. These GitHub SVGs are lightweight browser-viewable documentation assets.
