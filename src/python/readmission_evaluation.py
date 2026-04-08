"""
Metrics and splits for readmission models: temporal validation, recall@k, lift, thresholds.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve, roc_auc_score


def temporal_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    discharge_date: pd.Series,
    test_size: float = 0.25,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Sort by discharge date and hold out the last test_size fraction of rows.
    Avoids training on future discharges and testing on the past (no time leakage).
    """
    if not (len(X) == len(y) == len(discharge_date)):
        raise ValueError("X, y, and discharge_date must have the same length")
    df = X.copy()
    df["_y"] = y.values
    df["_d"] = pd.to_datetime(discharge_date.values)
    df = df.sort_values("_d", kind="mergesort")
    n = len(df)
    cut = max(1, int(n * (1 - test_size)))
    train = df.iloc[:cut]
    test = df.iloc[cut:]
    feature_cols = [c for c in df.columns if c not in ("_y", "_d")]
    X_train = train[feature_cols]
    X_test = test[feature_cols]
    y_train = train["_y"]
    y_test = test["_y"]
    return X_train, X_test, y_train, y_test


def recall_at_top_fraction(y_true, y_prob, top_fraction: float = 0.1) -> float:
    """Share of all positive cases that fall in the highest-risk top_fraction of scores."""
    y = np.asarray(y_true).astype(int)
    p = np.asarray(y_prob, dtype=float)
    pos = int(y.sum())
    if pos == 0:
        return float("nan")
    n = len(y)
    k = max(1, int(np.ceil(n * top_fraction)))
    order = np.argsort(-p)
    topk = y[order[:k]]
    return float(topk.sum() / pos)


def top_decile_prevalence_lift(y_true, y_prob) -> tuple[float, float, float]:
    """
    Returns (prevalence in top decile, overall prevalence, ratio).
    Ratio = (prevalence in top decile) / (overall prevalence); random model = ~1.0.
    """
    y = np.asarray(y_true).astype(int)
    p = np.asarray(y_prob, dtype=float)
    n = len(y)
    k = max(1, n // 10)
    order = np.argsort(-p)
    top_prev = float(y[order[:k]].mean())
    overall = float(y.mean()) if n else 0.0
    ratio = top_prev / overall if overall > 0 else float("nan")
    return top_prev, overall, ratio


def best_f1_threshold(y_true, y_prob) -> tuple[float, float]:
    """Threshold on predicted probability that maximizes F1 for the positive class."""
    y = np.asarray(y_true).astype(int)
    p = np.asarray(y_prob, dtype=float)
    prec, rec, thresh = precision_recall_curve(y, p)
    # precision_recall_curve: last precision/rec are 1,0 with no threshold
    p0, r0 = prec[:-1], rec[:-1]
    denom = p0 + r0
    f1 = np.divide(
        2 * p0 * r0, denom, out=np.zeros_like(denom, dtype=float), where=denom > 0
    )
    idx = int(np.nanargmax(f1))
    return float(thresh[idx]), float(f1[idx])


def best_cost_threshold(
    y_true, y_prob, cost_fn: float = 5.0, cost_fp: float = 1.0, n_grid: int = 101
) -> tuple[float, float]:
    """
    Threshold minimizing expected cost: FN * cost_fn + FP * cost_fp (illustrative defaults).
    """
    y = np.asarray(y_true).astype(int)
    p = np.asarray(y_prob, dtype=float)
    best_t, best_cost = 0.5, float("inf")
    for t in np.linspace(0, 1, n_grid):
        pred = (p >= t).astype(int)
        fn = int(((pred == 0) & (y == 1)).sum())
        fp = int(((pred == 1) & (y == 0)).sum())
        c = fn * cost_fn + fp * cost_fp
        if c < best_cost:
            best_cost = float(c)
            best_t = float(t)
    return best_t, best_cost


def safe_roc_auc(y_true, y_prob) -> float:
    try:
        return float(roc_auc_score(y_true, y_prob))
    except ValueError:
        return float("nan")


def print_ranking_metrics(y_test, y_prob, label: str = "") -> None:
    """Log recall@10%, decile prevalence lift, best F1 threshold, illustrative cost threshold."""
    prefix = f"{label}: " if label else ""
    r10 = recall_at_top_fraction(y_test, y_prob, 0.10)
    prev_top, prev_all, lift = top_decile_prevalence_lift(y_test, y_prob)
    t_f1, f1 = best_f1_threshold(y_test, y_prob)
    t_cost, cost = best_cost_threshold(y_test, y_prob, cost_fn=5.0, cost_fp=1.0)
    print(f"{prefix}Recall@10% (capture of all readmits in top decile risk): {round(r10, 4)}")
    print(
        f"{prefix}Top-decile prevalence: {round(prev_top, 4)} "
        f"(overall {round(prev_all, 4)}, lift ratio {round(lift, 2)}x)"
    )
    print(f"{prefix}Best F1 threshold (prob): {round(t_f1, 4)} (F1={round(f1, 4)})")
    print(
        f"{prefix}Illustrative cost-min threshold (FN=5x, FP=1x): "
        f"t={round(t_cost, 4)}, cost={round(cost, 1)}"
    )
