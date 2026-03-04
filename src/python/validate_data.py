"""
Validate generated healthcare data: referential integrity and row-count checks.
Run from repo root: python src/python/validate_data.py [--data-dir data/raw]
"""
import argparse
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default="data/raw", help="Path to CSVs")
    args = parser.parse_args()
    data_dir = REPO_ROOT / args.data_dir
    if not data_dir.exists():
        print(f"Data dir not found: {data_dir}")
        return 1
    errors = []

    # Load key tables
    patients = pd.read_csv(data_dir / "patients.csv")
    encounters = pd.read_csv(data_dir / "encounters.csv")
    claims = pd.read_csv(data_dir / "claims.csv")
    patient_ids = set(patients["patient_id"])
    encounter_ids = set(encounters["encounter_id"])

    # FK: encounters.patient_id -> patients
    bad = encounters[~encounters["patient_id"].isin(patient_ids)]
    if len(bad) > 0:
        errors.append(f"encounters: {len(bad)} rows with missing patient_id")
    # FK: claims.encounter_id -> encounters
    bad = claims[~claims["encounter_id"].isin(encounter_ids)]
    if len(bad) > 0:
        errors.append(f"claims: {len(bad)} rows with missing encounter_id")
    # FK: claims.patient_id -> patients
    bad = claims[~claims["patient_id"].isin(patient_ids)]
    if len(bad) > 0:
        errors.append(f"claims: {len(bad)} rows with missing patient_id")

    # Row count sanity
    if len(patients) == 0:
        errors.append("patients: no rows")
    if len(encounters) == 0:
        errors.append("encounters: no rows")
    if len(encounters) > 0 and len(encounters) > 20 * len(patients):
        errors.append("encounters/patients ratio very high (check scale)")

    if errors:
        print("Validation FAILED:")
        for e in errors:
            print("  -", e)
        return 1
    print("Validation passed: referential integrity and row-count checks OK.")
    print(f"  patients: {len(patients):,}  encounters: {len(encounters):,}  claims: {len(claims):,}")
    return 0


if __name__ == "__main__":
    exit(main())
