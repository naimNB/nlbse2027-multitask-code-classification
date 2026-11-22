# Tool competition manuscript

The manuscript is authored by **Md Naim Babu** and is prepared as a **4-page IEEEtran conference PDF** for the **NLBSE 2027 Code Comment Classification Tool Competition**.

**Canonical paper title:** _Imbalance-Aware CodeBERT for Joint Vulnerability and Self-Admitted Technical Debt Classification_

**Author affiliation:** Department of Computer Science and Engineering, Pundra University of Science & Technology, Bogura, Bangladesh.  
**Contact:** naim.cse2004@gmail.com

The submission PDF and its Overleaf archive are provided directly to the competition form. **They are not part of this GitHub repository**, and this repository is not a record of submission or acceptance.

- The old [draft.md](draft.md) captures early study notes and a **historical 256-token evaluation**; **do not use it as the final paper or its current abstract**.
- The final manuscript uses the matched **512-token Colab T4 comparison**, as recorded in the [E9 metrics](../results/e9/colab_t4_reference_style_512_metrics.json) and [released-baseline metrics](../results/baseline/colab_t4_matched_512_metrics.json).
- Updated figures: [512-token confusion matrices](../figures/e9_512_confusion_matrices.svg) and [matched F1 comparison](../figures/matched_512_model_comparison.svg).
- The model is [published separately on Hugging Face](https://huggingface.co/naimNB/nlbse2027-e9-codebert).
- [Submission checklist](../docs/SUBMISSION_CHECKLIST.md) and [reference-style protocol](../docs/OFFICIAL_EVALUATION.md).

**Scientific scope:** local public-validation Mean F1 **0.8927823465** (E9) versus **0.9101860726** (baseline) with matched 512-token settings. These are **not** the hidden-test result or official competition ranking. Neither paper acceptance nor form submission is asserted here.
