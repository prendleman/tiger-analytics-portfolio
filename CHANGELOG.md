# Changelog

## [Unreleased]

(No unreleased changes.)

## 2024-03 (beef-up #2)

- Data validation script (`src/python/validate_data.py`)
- CI: GitHub Actions workflow (`.github/workflows/tests.yml`) — generate demo data, validate, run models, pytest
- Model card for readmission model (`docs/MODEL_CARD.md`)
- PostgreSQL variant of monthly PMPM SQL (`sql/monthly_pmpm_summary_pg.sql`)

## 2024-03 (beef-up #1)

- **Config**: `config/config.yaml`, `config/demo.yaml`; generator supports `--config`
- **Demo**: One-command `scripts/run_demo.py` (generate demo data + readmission + time series)
- **Tests**: Pytest for data generation and readmission model smoke test
- **SQL**: `sql/monthly_pmpm_summary.sql` (SQL Server)
- **Docs**: `docs/DESIGN.md` (data flow, design decisions), expanded README (quick start, architecture)
- **License**: MIT

## Initial

- Healthcare mock schema and data generator (patients, encounters, claims, diagnoses, labs, vitals, readmissions, etc.)
- Readmission prediction (Random Forest, GridSearchCV), time series/PMPM (SARIMA, Prophet, exponential smoothing), clustering and anomaly detection
- Python and R notebooks and scripts; SQL feature and reporting queries
- Pipeline orchestration (`pipelines/run_pipeline.py`), Airflow DAG example, PySpark claims aggregation
