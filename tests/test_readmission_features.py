"""Unit tests for readmission feature pipeline."""
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "raw"


@pytest.mark.skipif(
    not (DATA_DIR / "patients.csv").exists(),
    reason="Generate data first (e.g. generate_healthcare_data.py --config config/demo.yaml)",
)
def test_load_and_feature_schema():
    import sys

    sys.path.insert(0, str(REPO_ROOT / "src" / "python"))
    from readmission_features import load_and_feature

    X, y, cols, dd = load_and_feature(DATA_DIR)
    assert len(X) == len(y) == len(dd)
    assert len(cols) == X.shape[1]
    assert set(y.unique()) <= {0, 1}
    assert not X.isna().any().any()
    assert X.shape[0] > 0
