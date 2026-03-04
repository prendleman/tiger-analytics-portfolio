# Model card: PMPM time series forecasting

## Overview

- **Task**: Forecast per-member-per-month (PMPM) cost (or utilization) from historical claims.
- **Models**: SARIMA(1,0,1), Holt-Winters exponential smoothing, optional Prophet. Train/test split; evaluation with RMSE and MAPE.
- **Data**: Monthly aggregates from claims (total_paid, member_count, pmpm_paid) in `data/raw/claims.csv`.

## Intended use

- **Purpose**: Portfolio demonstration of time series and PMPM forecasting for healthcare. Not for production planning or rate-setting.
- **Users**: Recruiters and technical reviewers. Out-of-scope: real membership/eligibility, production deployment.

## Training data

- **Source**: Claims aggregated by service month; member count = distinct patient_id per month. Production PMPM typically uses eligibility/membership tables.
- **Train/test**: 80/20 temporal split; metrics on held-out test period.

## Evaluation

- **Metrics**: RMSE, MAPE (and optionally back-testing over multiple origins if implemented).
- **Limitations**: Single split; no formal back-test or hyperparameter search in the default notebook/script.

## Ethical considerations and limitations

- Data is synthetic. Do not use for reimbursement, pricing, or policy decisions.
- No formal bias or fairness assessment.

## Reproducibility

- `python src/python/time_series_forecast.py` (from repo root).
- Notebook: `notebooks/python/time_series_pmpm_forecasting.ipynb`.
