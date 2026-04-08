"""
Readmission prediction script (runnable without notebook).
Builds features from data/raw, trains RandomForest, prints metrics.
Run from repo root: python src/python/readmission_model.py
"""
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

from readmission_features import load_and_feature

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "raw"


def main():
    X, y, _ = load_and_feature(DATA_DIR)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    print(
        classification_report(
            y_test, y_pred, target_names=["No readmit", "Readmit 30d"], zero_division=0
        )
    )
    print("ROC-AUC:", round(roc_auc_score(y_test, y_prob), 4))
    print("Average precision (PR-AUC):", round(average_precision_score(y_test, y_prob), 4))


if __name__ == "__main__":
    main()
