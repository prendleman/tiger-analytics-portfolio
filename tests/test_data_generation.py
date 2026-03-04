"""Tests for data generation: run with demo config and check outputs exist and have rows."""
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "raw"
CONFIG_DEMO = REPO_ROOT / "config" / "demo.yaml"


@pytest.fixture(scope="module")
def generate_demo_data():
    """Run generator with demo config once per test module."""
    if not CONFIG_DEMO.exists():
        pytest.skip("config/demo.yaml not found")
    subprocess.run(
        [sys.executable, "src/python/generate_healthcare_data.py", "--config", "config/demo.yaml"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        timeout=120,
    )


def test_raw_dir_exists():
    assert DATA_DIR.exists(), "data/raw should exist"


def test_required_csvs_exist_after_generation(generate_demo_data):
    required = ["patients.csv", "encounters.csv", "claims.csv", "diagnoses.csv", "readmissions.csv"]
    for name in required:
        path = DATA_DIR / name
        assert path.exists(), f"Expected {name} after generation"


def test_patients_has_rows(generate_demo_data):
    import pandas as pd
    df = pd.read_csv(DATA_DIR / "patients.csv")
    assert len(df) >= 100, "Demo config should produce at least 100 patients"
    assert "patient_id" in df.columns and "date_of_birth" in df.columns


def test_encounters_reference_patients(generate_demo_data):
    import pandas as pd
    patients = set(pd.read_csv(DATA_DIR / "patients.csv")["patient_id"])
    encounters = pd.read_csv(DATA_DIR / "encounters.csv")
    assert encounters["patient_id"].isin(patients).all(), "All encounter patient_ids should exist in patients"
