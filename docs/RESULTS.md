# Results summary

Summary of typical outputs when running the portfolio on **demo data** (`config/demo.yaml`: 1k patients, 5k encounters). Exact numbers vary with random seed and data; run the notebooks or scripts for your own metrics.

## Readmission model (binary classification)

- **Target**: 30-day readmission (binary).
- **Model**: Random Forest (default or GridSearchCV-tuned).
- **Typical test ROC-AUC**: ~0.85–0.92 (depends on class balance and features).
- **Average precision (PR-AUC)**: Often much lower than ROC when readmissions are rare (e.g. order 0.05–0.15 on small demo sets)—more informative than ROC alone for ranking rare events.
- **Note**: With demo data, the positive class is small; precision/recall for the readmit class at 0.5 threshold may be low. Full-scale data improves stability; use **threshold tuning** or **average precision** as the scoring metric when optimizing for the positive class.
- **Temporal split** (`python src/python/readmission_model.py --split temporal`): trains on earlier discharges and tests on the latest chunk—closer to deployment; on synthetic data metrics often track near the random split.
- **Recall@10%** and **top-decile lift**: CLI/notebook report what fraction of all readmits fall in the top-decile risk bucket and how concentrated readmits are vs baseline prevalence.

## PMPM time series

- **Target**: Per-member-per-month cost (pmpm_paid) from claims.
- **Models**: SARIMA(1,0,1), Holt-Winters, optional Prophet.
- **Metrics**: RMSE and MAPE on held-out test months (e.g. last 20% of months).
- **Typical range**: MAPE often in the teens to low twenties on synthetic data; RMSE depends on scale of pmpm_paid.

## Clustering and anomaly detection

- **Clustering**: KMeans (k=4) on encounter-level features; segments by LOS, age, diag count, total paid.
- **Anomaly**: Isolation Forest (5% contamination); flags outlier encounters for review.

## Reproducibility

To reproduce (or improve on) these results:

1. `python src/python/generate_healthcare_data.py --config config/demo.yaml`
2. Run `readmission_model.py`, `time_series_forecast.py`, or the notebooks.
3. For full-scale metrics, use default config (no `--config`) and run again (longer).
