"""Smoke test: readmission model runs and returns metrics."""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(
    not (REPO_ROOT / "data" / "raw" / "patients.csv").exists(),
    reason="Generate data first (e.g. python src/python/generate_healthcare_data.py --config config/demo.yaml)",
)
def test_readmission_model_runs():
    """Run readmission model script and check it exits 0."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "src/python/readmission_model.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, f"readmission_model.py failed: {result.stderr}"
