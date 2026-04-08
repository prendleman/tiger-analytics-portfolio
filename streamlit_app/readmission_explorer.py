"""
Interactive readmission exploration. Run from repo root:
  pip install -r requirements-app.txt
  streamlit run streamlit_app/readmission_explorer.py
"""
from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, classification_report
from sklearn.model_selection import train_test_split

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "raw"
sys.path.insert(0, str(REPO_ROOT / "src" / "python"))

from readmission_evaluation import (  # noqa: E402
    print_ranking_metrics,
    recall_at_top_fraction,
    safe_roc_auc,
    temporal_train_test_split,
    top_decile_prevalence_lift,
)
from readmission_features import load_and_feature  # noqa: E402


def main():
    st.set_page_config(page_title="Readmission explorer", layout="wide")
    st.title("30-day readmission — portfolio explorer")
    st.caption("Synthetic data only. Uses `readmission_features` + RandomForest.")

    if not (DATA_DIR / "patients.csv").exists():
        st.error(f"No data in `{DATA_DIR}`. Run: `python src/python/generate_healthcare_data.py --config config/demo.yaml`")
        st.stop()

    split = st.sidebar.selectbox("Train/test split", ("random", "temporal"), index=0)
    test_size = st.sidebar.slider("Test fraction", 0.15, 0.4, 0.25, 0.05)
    n_est = st.sidebar.slider("n_estimators", 50, 200, 100, 25)
    max_depth = st.sidebar.slider("max_depth", 4, 16, 8, 1)

    X, y, feature_cols, discharge = load_and_feature(DATA_DIR)

    if split == "temporal":
        X_train, X_test, y_train, y_test = temporal_train_test_split(
            X, y, discharge, test_size=test_size
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

    clf = RandomForestClassifier(
        n_estimators=n_est, max_depth=max_depth, random_state=42
    )
    clf.fit(X_train, y_train)
    y_prob = clf.predict_proba(X_test)[:, 1]
    y_pred = clf.predict(X_test)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Test rows", len(y_test))
    c2.metric("Readmit rate (test)", f"{y_test.mean():.3f}")
    roc = safe_roc_auc(y_test, y_prob)
    c3.metric("ROC-AUC", f"{roc:.3f}" if np.isfinite(roc) else "N/A")
    ap = average_precision_score(y_test, y_prob) if y_test.sum() > 0 else float("nan")
    c4.metric("Avg precision", f"{ap:.3f}" if np.isfinite(ap) else "N/A")

    st.subheader("Classification report")
    st.text(
        classification_report(
            y_test, y_pred, target_names=["No readmit", "Readmit 30d"], zero_division=0
        )
    )

    r10 = recall_at_top_fraction(y_test, y_prob, 0.1)
    prev_top, prev_all, lift = top_decile_prevalence_lift(y_test, y_prob)
    st.subheader("Ranking / imbalance")
    st.write(
        {
            "Recall@10% (of all readmits)": round(r10, 4) if np.isfinite(r10) else None,
            "Prevalence top decile": round(prev_top, 4),
            "Overall prevalence": round(prev_all, 4),
            "Lift (top decile / overall)": round(lift, 2) if np.isfinite(lift) else None,
        }
    )

    imp = pd.Series(clf.feature_importances_, index=feature_cols).sort_values(ascending=False)
    st.subheader("Feature importance")
    st.bar_chart(imp.head(12))

    with st.expander("Raw ranking metrics (same as CLI)"):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_ranking_metrics(y_test, y_prob)
        st.code(buf.getvalue())


if __name__ == "__main__":
    main()
