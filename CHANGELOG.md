# Changelog

## [Unreleased]

(No unreleased changes.)

## 2024-03 (beef-up #5)

- **SECURITY.md** — Portfolio context, no production use, how to report issues.
- **CITATION.cff** — Citation file for the repo (authors, URL, date).
- **docs/RESULTS.md** — One-page results summary (typical AUC, MAPE, etc. on demo data).
- **.editorconfig** — Indentation and line endings for Python, YAML, Markdown, JSON.
- **CI** — Optional dependency audit step (`pip-audit`; non-blocking).

## 2024-03 (beef-up #4)

- **Makefile** — targets: `install`, `data-demo`, `data-full`, `demo`, `validate`, `test`, `pipeline`, `export-notebooks`.
- **README badges** — GitHub Actions (tests) and MIT License.
- **docs/README.md** — documentation index (methodology, design, model cards, troubleshooting).
- **docs/MODEL_CARD_TIMESERIES.md** — model card for PMPM time series (SARIMA, Prophet, evaluation).
- **tests/test_time_series_forecast.py** — smoke test that time_series_forecast.py runs.

## 2024-03 (beef-up #3)

- Overview notebook (`notebooks/python/00_overview.ipynb`) — intro and links to all Python notebooks.
- Export notebooks to HTML (`scripts/export_notebooks.py`) — static HTML in `docs/notebooks/` for viewing without Jupyter.
- R readmission model (`src/r/readmission_model_r.R`) — logistic regression for 30-day readmission; optional pROC for AUC.
- **TROUBLESHOOTING.md** — common issues (paths, missing modules, R, Prophet).
- **CONTRIBUTING.md** — how to run, test, and suggest changes.

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
