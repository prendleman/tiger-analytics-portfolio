"""Smoke test: time series forecast script runs and exits 0."""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(
    not (REPO_ROOT / "data" / "raw" / "claims.csv").exists(),
    reason="Generate data first (e.g. python src/python/generate_healthcare_data.py --config config/demo.yaml)",
)
def test_time_series_forecast_runs():
    """Run time_series_forecast.py and check it exits 0."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "src/python/time_series_forecast.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert result.returncode == 0, f"time_series_forecast.py failed: {result.stderr}"
