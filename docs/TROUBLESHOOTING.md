# Troubleshooting

## Module not found (statsmodels, sklearn, etc.)

Install dependencies from repo root:

```bash
pip install -r requirements.txt
```

If you use a virtual environment, activate it first.

## Path or "file not found" errors

Run all commands from the **repo root** (the folder that contains `data/`, `src/`, `notebooks/`). For example:

```bash
cd tiger-analytics-portfolio
python src/python/readmission_model.py
```

Not from `src/python/` or `notebooks/python/`.

## No data in data/raw/

Generate data first:

```bash
python src/python/generate_healthcare_data.py --config config/demo.yaml
```

Or use the one-command demo (generates then runs models):

```bash
python scripts/run_demo.py
```

## R: "Rscript not found" or R errors

R is optional. The portfolio runs with Python only. If you want to run R:

- Install [R](https://cran.r-project.org/) and add it to your PATH.
- From repo root: `Rscript src/r/healthcare_eda.R`
- For R Markdown: open `notebooks/r/healthcare_eda.Rmd` in RStudio and knit.

## Pytest fails (e.g. "no module named 'src'")

Run pytest from repo root:

```bash
pytest tests/ -v
```

The tests run the data generator with demo config (they may overwrite existing files in `data/raw/`).

## Pipeline or Airflow DAG: path issues

In `pipelines/dag_airflow_example.py`, set `REPO_ROOT` to the **absolute** path of the repo on the machine where Airflow runs (e.g. `/opt/airflow/repos/tiger-analytics-portfolio`).

## Prophet (time series notebook)

The Prophet cell in the time series notebook is optional. If you see "Prophet not installed", either:

- Run `pip install prophet` to add it, or
- Ignore that cell; SARIMA and exponential smoothing already demonstrate time series forecasting.
