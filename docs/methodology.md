# Methodology: Healthcare Mock Data & Readmission Model

## Data

- **Source**: Synthetically generated healthcare dataset (see `data/schema/` and `src/python/generate_healthcare_data.py`).
- **Scope**: Patients, encounters (inpatient/outpatient/emergency), diagnoses (ICD), procedures (CPT), medications (NDC), labs, vitals, claims, claim lines, readmissions, risk scores, and reference tables.
- **Assumptions**: Data is mock only; distributions (LOS, readmission rates, costs) are plausible but not calibrated to real benchmarks. No PHI; demographics and identifiers are synthetic (Faker).

## Time series & PMPM forecasting (Python)

- **Notebook**: `notebooks/python/time_series_pmpm_forecasting.ipynb`.
- **PMPM**: Claims aggregated to service month; member count and total paid/charge; PMPM (per member per month) cost series.
- **Models**: SARIMA(1,0,1) and Holt-Winters exponential smoothing; train/test split; evaluation with RMSE and MAPE.
- **Stack**: pandas, statsmodels. Production use would add back-testing, hyperparameter tuning, and pipeline automation (e.g. Airflow, Databricks).

## Clustering & anomaly detection (Python)

- **Notebook**: `notebooks/python/clustering_anomaly_detection.ipynb`.
- **Clustering**: KMeans (k=4) on encounter-level features: LOS, age, diagnosis count, total paid. Segments encounters by utilization/acuity for reporting or targeting.
- **Anomaly detection**: Isolation Forest (contamination=5%) on the same scaled features; flags outlier encounters (e.g. unusual cost or LOS) for review.

## Readmission prediction (Python)

- **Target**: Binary `readmit_30` — whether an encounter had a 30-day readmission (from `readmissions.is_30_day`).
- **Unit of analysis**: One row per encounter (index encounter).
- **Features**: Length of stay, age at admission, diagnosis count per encounter, lab summary (mean result, count), encounter type (dummies).
- **Model**: Random Forest (scikit-learn); train/test split 75/25, stratified.
- **Limitations**: No temporal leak (target uses only readmissions table); no prior utilization or comorbidity indices in this version. Model is for portfolio demonstration, not clinical use.

## R analytics

- **Purpose**: Descriptive analytics and visualization (encounter mix, LOS distribution, claims by type, readmission counts).
- **Output**: R Markdown HTML report and/or R script summary; supports stakeholder-style communication.

## SQL

- **feature_readmission.sql**: Builds encounter-level feature table with LOS, age, diag count, lab agg, and readmit flag for modeling or BI.
- **report_utilization_kpis.sql**: Aggregates encounters and claims by facility and payer (counts, LOS, charges, payments).

## Reproducibility

- Generate data: `python src/python/generate_healthcare_data.py` (config in script).
- Python model: `python src/python/readmission_model.py` or run `notebooks/python/readmission_prediction.ipynb`.
- R: `Rscript src/r/healthcare_eda.R` or knit `notebooks/r/healthcare_eda.Rmd`.
- SQL: Run against a database populated with `data/schema/ddl.sql` and the CSVs (via ETL or bulk load).
