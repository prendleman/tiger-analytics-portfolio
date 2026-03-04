# Executive summary

**One-page overview for stakeholders and non-technical reviewers.**

## What this project is

A **healthcare analytics portfolio** that shows end-to-end data science: synthetic claims and clinical data, predictive models (readmission risk, cost forecasting), and reporting/SQL. It is built to demonstrate skills for analytics consulting and healthcare/life sciences roles—**not** for production or clinical use.

## What we built

| Deliverable | Purpose |
|-------------|--------|
| **Synthetic healthcare data** | Patients, encounters, diagnoses, procedures, medications, labs, claims—with configurable size (demo vs. full scale). |
| **30-day readmission model** | Binary classification (Random Forest) to flag encounters at higher risk of readmission; supports prioritization and outreach. |
| **PMPM time series** | Per-member-per-month cost forecasting (SARIMA, exponential smoothing) for budgeting and trend reporting. |
| **Clustering & anomaly detection** | Segment encounters and flag outliers for review (e.g. unusual LOS or cost). |
| **SQL and reporting** | Feature tables for ML, monthly PMPM summaries, utilization KPIs—ready to plug into a warehouse or BI tool. |
| **Pipelines** | Orchestration script plus Airflow/Spark-style examples for scheduled runs in a production-like setup. |

## Key takeaways (on demo data)

- **Readmission**: Model achieves strong discrimination (e.g. AUC ~0.85–0.92 on demo data); with more data and tuning, precision/recall for the positive class can be improved.
- **PMPM**: Forecasts give a baseline trend and MAPE in a typical range for synthetic data; useful for capacity and cost planning discussions.
- **Data quality**: Validation checks referential integrity and row counts so downstream models and reports run on consistent data.

## Limitations

- **Data**: 100% synthetic (Faker + pandas). No real PHI or claims; results are illustrative only.
- **Models**: Not validated on real populations; not for clinical or reimbursement decisions.
- **Scope**: Portfolio demonstration—not a deployed product (no auth, no API, no SLAs).

## Next steps (if this were a real engagement)

1. **Data**: Replace synthetic data with de-identified production data; align schema and definitions with client.
2. **Readmission**: Add more features (e.g. social determinants, prior utilization); calibrate thresholds with clinical/business input.
3. **PMPM**: Incorporate seasonality and program changes; refresh forecasts on a cadence (e.g. monthly).
4. **Operationalize**: Deploy pipelines (Airflow/Databricks), add monitoring, and document handoff to analytics/engineering.

---

*For technical details, see [methodology.md](methodology.md), [DESIGN.md](DESIGN.md), and [README.md](README.md) (docs index).*
