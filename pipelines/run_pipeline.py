"""
Orchestration script: run data generation, readmission model, and time series forecast in sequence.
Designed to be run as a single job or as separate steps (e.g. Airflow tasks, Databricks jobs).
Usage from repo root:
  python pipelines/run_pipeline.py
  python pipelines/run_pipeline.py --skip-data   # use existing data/raw
"""
import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(cmd_desc: str, cmd: list) -> bool:
    print(f"[Pipeline] {cmd_desc}...")
    try:
        r = subprocess.run(cmd, cwd=REPO_ROOT)
        if r.returncode != 0:
            print(f"[Pipeline] {cmd_desc} — failed (exit {r.returncode}).")
            return False
        print(f"[Pipeline] {cmd_desc} — done.")
        return True
    except Exception as e:
        print(f"[Pipeline] {cmd_desc} — failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run healthcare analytics pipeline")
    parser.add_argument("--skip-data", action="store_true", help="Skip data generation; use existing data/raw")
    args = parser.parse_args()

    if not args.skip_data:
        if not run("Data generation", [sys.executable, "src/python/generate_healthcare_data.py"]):
            sys.exit(1)
    if not run("Readmission model", [sys.executable, "src/python/readmission_model.py"]):
        sys.exit(1)
    if not run("Time series (PMPM) forecast", [sys.executable, "src/python/time_series_forecast.py"]):
        sys.exit(1)
    print("[Pipeline] All steps completed.")


if __name__ == "__main__":
    main()
