"""
Readmission prediction script (runnable without notebook).
Builds features from data/raw, trains RandomForest, prints metrics.
Run from repo root: python src/python/readmission_model.py
"""
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "raw"


def load_and_feature():
    patients = pd.read_csv(DATA_DIR / "patients.csv")
    encounters = pd.read_csv(DATA_DIR / "encounters.csv", parse_dates=["admit_date", "discharge_date"])
    diagnoses = pd.read_csv(DATA_DIR / "diagnoses.csv")
    labs = pd.read_csv(DATA_DIR / "labs.csv", parse_dates=["result_date"])
    readmissions = pd.read_csv(DATA_DIR / "readmissions.csv")

    enc_with_readmit = set(readmissions[readmissions["is_30_day"] == 1]["encounter_id"])
    encounters["readmit_30"] = encounters["encounter_id"].isin(enc_with_readmit).astype(int)
    encounters["los_days"] = (
        (encounters["discharge_date"] - encounters["admit_date"]).dt.total_seconds() / 86400
    ).clip(lower=0)
    encounters["admit_date_d"] = pd.to_datetime(encounters["admit_date"])
    patients["date_of_birth"] = pd.to_datetime(patients["date_of_birth"])
    encounters = encounters.merge(
        patients[["patient_id", "date_of_birth", "gender", "payer_id"]], on="patient_id", how="left"
    )
    encounters["age"] = (
        (encounters["admit_date_d"] - encounters["date_of_birth"]).dt.days / 365.25
    ).clip(0, 120)
    diag_count = diagnoses.groupby("encounter_id").size().reset_index(name="diag_count")
    encounters = encounters.merge(diag_count, on="encounter_id", how="left")
    encounters["diag_count"] = encounters["diag_count"].fillna(0).astype(int)
    lab_agg = labs.groupby("encounter_id")["result_num"].agg(["mean", "count"]).reset_index()
    lab_agg.columns = ["encounter_id", "lab_mean", "lab_count"]
    encounters = encounters.merge(lab_agg, on="encounter_id", how="left")
    encounters["lab_mean"] = encounters["lab_mean"].fillna(encounters["lab_mean"].median())
    encounters["lab_count"] = encounters["lab_count"].fillna(0).astype(int)
    encounters = pd.get_dummies(encounters, columns=["encounter_type"], prefix="enc")
    feature_cols = ["los_days", "age", "diag_count", "lab_mean", "lab_count"] + [
        c for c in encounters.columns if c.startswith("enc_")
    ]
    X = encounters[feature_cols].fillna(0)
    y = encounters["readmit_30"]
    return X, y


def main():
    X, y = load_and_feature()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, y_pred, target_names=["No readmit", "Readmit 30d"]))
    print("ROC-AUC:", round(roc_auc_score(y_test, y_prob), 4))


if __name__ == "__main__":
    main()
