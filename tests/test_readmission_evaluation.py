"""Tests for readmission ranking / temporal helpers (no data files required)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "python"))

from readmission_evaluation import (  # noqa: E402
    recall_at_top_fraction,
    temporal_train_test_split,
    top_decile_prevalence_lift,
)


def test_recall_at_top_fraction_perfect_ranking():
    y = pd.Series([1, 0, 1, 0, 1])
    p = np.array([0.9, 0.1, 0.8, 0.2, 0.7])
    # Top 60% -> k=3, covers the three highest scores (all positives)
    r = recall_at_top_fraction(y, p, top_fraction=0.6)
    assert r == 1.0


def test_temporal_split_order():
    X = pd.DataFrame({"a": [1, 2, 3, 4]})
    y = pd.Series([0, 1, 0, 1])
    d = pd.Series(pd.date_range("2020-01-01", periods=4, freq="D"))
    X_train, X_test, y_train, y_test = temporal_train_test_split(X, y, d, test_size=0.25)
    assert len(X_test) == 1
    assert X_test["a"].iloc[0] == 4


def test_top_decile_lift_random_scores():
    np.random.seed(0)
    n = 1000
    y = pd.Series((np.random.rand(n) > 0.95).astype(int))
    p = np.random.rand(n)
    prev_top, prev_all, lift = top_decile_prevalence_lift(y, p)
    assert 0 <= prev_top <= 1
    assert prev_all == y.mean()
    if prev_all > 0:
        assert lift == pytest.approx(prev_top / prev_all, rel=1e-9)
