# Pipelines & MLOps

- **`run_pipeline.py`** — Single script to run data generation, readmission model, and time series forecast in sequence. Use as a scheduled job or as the basis for Airflow/Databricks steps.
- **`dag_airflow_example.py`** — Example Airflow DAG (BashOperators). Set `REPO_ROOT` and add to your DAGs folder.
- **Spark:** `src/python/spark_claims_agg.py` — PySpark job to aggregate claims by month; writes parquet to `data/processed/claims_by_month/`.

Optional dependencies: `apache-airflow` (for the DAG), `pyspark` (for the Spark job).
