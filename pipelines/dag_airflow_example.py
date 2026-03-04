"""
Example Airflow DAG for the healthcare analytics pipeline.
Drop this into your Airflow DAGs folder and set REPO_ROOT (or edit path below).
Requires: pip install apache-airflow
Tasks: generate_data -> readmission_model -> time_series_forecast
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

# Set this to the absolute path of the tiger-analytics-portfolio repo on the Airflow worker.
REPO_ROOT = "/path/to/tiger-analytics-portfolio"

with DAG(
    dag_id="healthcare_analytics_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@weekly",
    catchup=False,
    tags=["healthcare", "ml", "forecasting"],
) as dag:
    generate_data = BashOperator(
        task_id="generate_healthcare_data",
        bash_command=f"cd {REPO_ROOT} && python src/python/generate_healthcare_data.py",
    )
    readmission_model = BashOperator(
        task_id="readmission_model",
        bash_command=f"cd {REPO_ROOT} && python src/python/readmission_model.py",
    )
    time_series_forecast = BashOperator(
        task_id="time_series_forecast",
        bash_command=f"cd {REPO_ROOT} && python src/python/time_series_forecast.py",
    )
    generate_data >> readmission_model >> time_series_forecast
