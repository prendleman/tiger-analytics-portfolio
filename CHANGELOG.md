# Changelog

## [Unreleased]

(No unreleased changes.)

## 2024-03 (Release 9)

- **Readmission evaluation** — `readmission_evaluation.py`: temporal split by discharge date, recall@10%, top-decile prevalence lift, best F1 threshold, illustrative cost-based threshold.
- **CLI** — `readmission_model.py --split temporal|random`, `--test-size`; ranking metrics printed after PR-AUC.
- **Tests** — `test_readmission_features.py`, `test_readmission_evaluation.py`.
- **Streamlit** — `streamlit_app/readmission_explorer.py` + `requirements-app.txt` (optional install).
- **GitHub Pages** — workflow `notebooks-pages.yml` exports notebooks + `write_notebooks_index.py`; enable Pages → GitHub Actions in repo settings.
- **`pyproject.toml`** — pytest/ruff/black metadata; **`make lock`** for pip-compile.
- **Docs** — `docs/INTERVIEW_WALKTHROUGH.md`.

## 2024-03 (Release 8)

- **Readmission**: `src/python/readmission_features.py` — shared feature/label pipeline for the CLI and notebook (single source of truth).
- **Metrics**: Script and notebook report **average precision (PR-AUC)**; notebook adds ROC and precision–recall plots and notes on imbalance; `classification_report(..., zero_division=0)` to avoid noisy warnings.
- **Docs**: MODEL_CARD and RESULTS updated for PR-AUC and threshold/scoring guidance; README JD table mentions average precision.

## 2024-03 (Release 7)

- **Pre-commit** — `.pre-commit-config.yaml`: Black, Ruff (with --fix), trailing-whitespace, end-of-file-fixer, check-yaml, check-merge-conflict. Optional: `pip install pre-commit && pre-commit install`.
- **Pinned dependencies** — `requirements.in` is the source; `requirements.txt` is generated with `pip-compile` for reproducible installs. CONTRIBUTING and README updated.
- **CI Docker** — New workflow job: build the Docker image and run the demo in the container on every push/PR.

## 2024-03 (Release 6)

- **Docker** — `Dockerfile` and `.dockerignore` for one-command reproducible run: `docker build -t tiger-portfolio .` then `docker run --rm tiger-portfolio` runs the full demo.
- **docs/EXECUTIVE_SUMMARY.md** — One-page stakeholder summary: what we built, key takeaways, limitations, next steps (for client/PM-style communication).

## 2024-03 (Release 5)

- **SECURITY.md** — Portfolio context, no production use, how to report issues.
- **CITATION.cff** — Citation file for the repo (authors, URL, date).
- **docs/RESULTS.md** — One-page results summary (typical AUC, MAPE, etc. on demo data).
- **.editorconfig** — Indentation and line endings for Python, YAML, Markdown, JSON.
- **CI** — Optional dependency audit step (`pip-audit`; non-blocking).

## 2024-03 (Release 4)

- **Makefile** — targets: `install`, `data-demo`, `data-full`, `demo`, `validate`, `test`, `pipeline`, `export-notebooks`.
- **README badges** — GitHub Actions (tests) and MIT License.
- **docs/README.md** — documentation index (methodology, design, model cards, troubleshooting).
- **docs/MODEL_CARD_TIMESERIES.md** — model card for PMPM time series (SARIMA, Prophet, evaluation).
- **tests/test_time_series_forecast.py** — smoke test that time_series_forecast.py runs.

## 2024-03 (Release 3)

- Overview notebook (`notebooks/python/00_overview.ipynb`) — intro and links to all Python notebooks.
- Export notebooks to HTML (`scripts/export_notebooks.py`) — static HTML in `docs/notebooks/` for viewing without Jupyter.
- R readmission model (`src/r/readmission_model_r.R`) — logistic regression for 30-day readmission; optional pROC for AUC.
- **TROUBLESHOOTING.md** — common issues (paths, missing modules, R, Prophet).
- **CONTRIBUTING.md** — how to run, test, and suggest changes.

## 2024-03 (Release 2)

- Data validation script (`src/python/validate_data.py`)
- CI: GitHub Actions workflow (`.github/workflows/tests.yml`) — generate demo data, validate, run models, pytest
- Model card for readmission model (`docs/MODEL_CARD.md`)
- PostgreSQL variant of monthly PMPM SQL (`sql/monthly_pmpm_summary_pg.sql`)

## 2024-03 (Release 1)

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
