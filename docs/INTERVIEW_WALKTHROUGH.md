# Interview walkthrough (5 minutes)

Use this outline when walking a hiring manager or technical interviewer through the repo.

1. **Data and scope** — Synthetic healthcare data (encounters, claims, diagnoses, labs) generated with a config-driven pipeline. Same domain threads through SQL, Python/R models, and pipeline examples so the story stays coherent.

2. **Readmission use case** — Binary label = 30-day readmission. Features are encounter-level (LOS, age, diagnosis count, labs, encounter type). Feature code is centralized in `readmission_features.py` so the CLI, notebook, and any app stay aligned.

3. **Splits and leakage** — Random stratified split is the default for a quick baseline. **Temporal split** (`--split temporal`) orders by **discharge date** and holds out the most recent encounters—closer to production and avoids “future” discharges in training when dates matter. Discuss what you’d add for real data (e.g. eligibility, rolling features).

4. **Metrics that match imbalance** — Readmits are rare: **ROC-AUC** can look fine while default **precision** is poor. The repo reports **average precision (PR-AUC)**, **recall@10%** (share of all readmits captured in the top-decile-risk bucket), **top-decile prevalence vs overall (lift)**, and **threshold** choices (max F1, illustrative FN/FP costs). Connect that to how the business would prioritize interventions.

5. **What you’d do next with a client** — Real PHI/claims integration, cohort definitions aligned to the payer, calibration and monitoring, fairness review, and deployment (Airflow/Databricks patterns are sketched in `pipelines/`). Be clear this repo is a **portfolio**, not validated for clinical or payment decisions.
