"""
Readmission prediction script (runnable without notebook).
Builds features from data/raw, trains RandomForest, prints metrics.
Run from repo root: python src/python/readmission_model.py
    python src/python/readmission_model.py --split temporal
"""
from __future__ import annotations

import argparse
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, classification_report
from sklearn.model_selection import train_test_split

from readmission_evaluation import (
    print_ranking_metrics,
    safe_roc_auc,
    temporal_train_test_split,
)
from readmission_features import load_and_feature

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "raw"


def parse_args():
    p = argparse.ArgumentParser(description="Train readmission model on data/raw CSVs.")
    p.add_argument(
        "--split",
        choices=("random", "temporal"),
        default="random",
        help="random=stratified shuffle split; temporal=hold out last discharge dates",
    )
    p.add_argument(
        "--test-size",
        type=float,
        default=0.25,
        help="Fraction held out for test (temporal: last fraction by discharge date)",
    )
    return p.parse_args()


def main():
    args = parse_args()
    X, y, _feature_cols, discharge_date = load_and_feature(DATA_DIR)

    if args.split == "temporal":
        X_train, X_test, y_train, y_test = temporal_train_test_split(
            X, y, discharge_date, test_size=args.test_size
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=42, stratify=y
        )

    print(f"Split: {args.split} (test_size={args.test_size})")
    print(f"Train n={len(y_train)}, test n={len(y_test)}; test readmit rate={y_test.mean():.4f}")

    clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    print(
        classification_report(
            y_test, y_pred, target_names=["No readmit", "Readmit 30d"], zero_division=0
        )
    )
    print("ROC-AUC:", round(safe_roc_auc(y_test, y_prob), 4))
    ap = average_precision_score(y_test, y_prob) if y_test.sum() > 0 else float("nan")
    print("Average precision (PR-AUC):", round(ap, 4))
    print_ranking_metrics(y_test, y_prob)


if __name__ == "__main__":
    main()
