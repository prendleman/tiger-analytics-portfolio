"""
Generate healthcare mock dataset with referential integrity.
Uses Faker + pandas. Outputs CSVs to data/raw/.
Run from repo root: python src/python/generate_healthcare_data.py
"""
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

Faker.seed(42)
random.seed(42)
np.random.seed(42)

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "data" / "raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Config: scaled for portfolio (50k patients, 200k encounters; adjust if needed)
CONFIG = {
    "n_patients": 50_000,
    "n_encounters": 200_000,
    "n_labs_per_enc": 5,
    "n_claim_lines_per_claim": 8,
    "date_start": "2020-01-01",
    "date_end": "2024-12-31",
}
FAKE = Faker()


def write_csv(name: str, df: pd.DataFrame) -> None:
    path = OUT_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"  {path.name}: {len(df):,} rows")


def generate_reference_tables() -> dict:
    """Reference tables with fixed IDs for joins."""
    facility_types = pd.DataFrame([
        {"facility_type_id": "HOSP", "facility_type_name": "Hospital"},
        {"facility_type_id": "CLIN", "facility_type_name": "Clinic"},
        {"facility_type_id": "ER", "facility_type_name": "Emergency"},
        {"facility_type_id": "SNF", "facility_type_name": "Skilled Nursing"},
    ])
    specialties = pd.DataFrame([
        {"specialty_id": "IM", "specialty_name": "Internal Medicine"},
        {"specialty_id": "CARD", "specialty_name": "Cardiology"},
        {"specialty_id": "ORTH", "specialty_name": "Orthopedics"},
        {"specialty_id": "PULM", "specialty_name": "Pulmonology"},
        {"specialty_id": "PCP", "specialty_name": "Primary Care"},
        {"specialty_id": "SURG", "specialty_name": "General Surgery"},
        {"specialty_id": "PEDS", "specialty_name": "Pediatrics"},
        {"specialty_id": "PSY", "specialty_name": "Psychiatry"},
    ])
    # Sample ICD-10 (chapter-level variety)
    icd_list = [
        ("I10", "Essential hypertension", "Circulatory"),
        ("E11", "Type 2 diabetes", "Endocrine"),
        ("J44", "COPD", "Respiratory"),
        ("M17", "Knee osteoarthritis", "Musculoskeletal"),
        ("F32", "Depressive episode", "Mental"),
        ("K21", "GERD", "Digestive"),
        ("J18", "Pneumonia", "Respiratory"),
        ("I25", "Chronic ischemic heart disease", "Circulatory"),
        ("N18", "CKD", "Genitourinary"),
        ("G47", "Sleep disorders", "Nervous"),
    ]
    icd_codes = pd.DataFrame([
        {"icd_code": c[0], "description": c[1], "chapter": c[2]} for c in icd_list
    ])
    # Expand with more codes for variety
    for i in range(40):
        icd_codes = pd.concat([icd_codes, pd.DataFrame([{
            "icd_code": f"Z{i:02d}9", "description": f"Condition {i}", "chapter": "Other"
        }])], ignore_index=True)
    cpt_codes = pd.DataFrame([
        {"cpt_code": "99213", "description": "Office visit level 3", "category": "E&M"},
        {"cpt_code": "99214", "description": "Office visit level 4", "category": "E&M"},
        {"cpt_code": "99223", "description": "Hospital visit high", "category": "E&M"},
        {"cpt_code": "99285", "description": "ED visit high", "category": "E&M"},
        {"cpt_code": "80053", "description": "Comprehensive metabolic panel", "category": "Lab"},
        {"cpt_code": "85025", "description": "CBC", "category": "Lab"},
        {"cpt_code": "93000", "description": "EKG", "category": "Cardiology"},
        {"cpt_code": "71046", "description": "Chest X-ray", "category": "Radiology"},
        {"cpt_code": "36415", "description": "Venipuncture", "category": "Lab"},
        {"cpt_code": "99231", "description": "Subsequent hospital care", "category": "E&M"},
    ])
    ndc_codes = pd.DataFrame([
        {"ndc_code": "0002-3227-01", "description": "Metformin 500mg", "drug_class": "Antidiabetic"},
        {"ndc_code": "0002-3228-01", "description": "Lisinopril 10mg", "drug_class": "ACE inhibitor"},
        {"ndc_code": "0002-3229-01", "description": "Amlodipine 5mg", "drug_class": "CCB"},
        {"ndc_code": "0002-3230-01", "description": "Omeprazole 20mg", "drug_class": "PPI"},
        {"ndc_code": "0002-3231-01", "description": "Sertraline 50mg", "drug_class": "SSRI"},
        {"ndc_code": "0002-3232-01", "description": "Albuterol inhaler", "drug_class": "Bronchodilator"},
        {"ndc_code": "0002-3233-01", "description": "Insulin glargine", "drug_class": "Insulin"},
        {"ndc_code": "0002-3234-01", "description": "Atorvastatin 20mg", "drug_class": "Statin"},
    ])
    write_csv("facility_types", facility_types)
    write_csv("specialties", specialties)
    write_csv("icd_codes", icd_codes)
    write_csv("cpt_codes", cpt_codes)
    write_csv("ndc_codes", ndc_codes)
    return {
        "facility_types": facility_types,
        "specialties": specialties,
        "icd_codes": icd_codes,
        "cpt_codes": cpt_codes,
        "ndc_codes": ndc_codes,
    }


def generate_organizations(refs: dict) -> dict:
    orgs = pd.DataFrame([
        {"organization_id": "ORG1", "organization_name": "Metro Health System", "parent_id": None},
        {"organization_id": "ORG2", "organization_name": "Regional Care Network", "parent_id": None},
    ])
    payers = pd.DataFrame([
        {"payer_id": "PAY1", "payer_name": "Commercial A", "payer_type": "commercial"},
        {"payer_id": "PAY2", "payer_name": "Medicare", "payer_type": "medicare"},
        {"payer_id": "PAY3", "payer_name": "Medicaid", "payer_type": "medicaid"},
        {"payer_id": "PAY4", "payer_name": "Commercial B", "payer_type": "commercial"},
    ])
    ft = refs["facility_types"]
    facilities = pd.DataFrame([
        {"facility_id": "F1", "facility_name": "Metro General", "facility_type_id": "HOSP", "organization_id": "ORG1", "city": "Chicago", "state": "IL", "zip": "60601"},
        {"facility_id": "F2", "facility_name": "Metro Clinic North", "facility_type_id": "CLIN", "organization_id": "ORG1", "city": "Chicago", "state": "IL", "zip": "60614"},
        {"facility_id": "F3", "facility_name": "Regional ER", "facility_type_id": "ER", "organization_id": "ORG2", "city": "Evanston", "state": "IL", "zip": "60201"},
        {"facility_id": "F4", "facility_name": "Metro SNF", "facility_type_id": "SNF", "organization_id": "ORG1", "city": "Chicago", "state": "IL", "zip": "60607"},
    ])
    specs = refs["specialties"]
    providers = pd.DataFrame([
        {"provider_id": f"PRV{i}", "provider_name": FAKE.name(), "specialty_id": specs.sample(1).iloc[0]["specialty_id"], "facility_id": facilities.sample(1).iloc[0]["facility_id"], "npi": str(1000000000 + i)}
        for i in range(1, 51)
    ])
    write_csv("organizations", orgs)
    write_csv("payers", payers)
    write_csv("facilities", facilities)
    write_csv("providers", providers)
    return {"organizations": orgs, "payers": payers, "facilities": facilities, "providers": providers}


def generate_patients(orgs: dict) -> pd.DataFrame:
    payers = orgs["payers"]
    n = CONFIG["n_patients"]
    start = pd.to_datetime(CONFIG["date_start"])
    end = pd.to_datetime(CONFIG["date_end"])
    dob_start = end - pd.DateOffset(years=90)
    dob_end = end - pd.DateOffset(years=18)
    patients = pd.DataFrame({
        "patient_id": [f"P{i:08d}" for i in range(1, n + 1)],
        "date_of_birth": pd.to_datetime([FAKE.date_between(dob_start, dob_end) for _ in range(n)]),
        "gender": random.choices(["M", "F", "O"], weights=[0.49, 0.50, 0.01], k=n),
        "race": random.choices(["White", "Black", "Asian", "Other", "Unknown"], k=n),
        "ethnicity": random.choices(["Non-Hispanic", "Hispanic", "Unknown"], k=n),
        "zip": [FAKE.zipcode() for _ in range(n)],
        "payer_id": payers.sample(n, replace=True)["payer_id"].values,
        "created_at": pd.to_datetime([FAKE.date_between(start, end) for _ in range(n)]),
    })
    write_csv("patients", patients)
    return patients


def generate_encounters(patients: pd.DataFrame, orgs: dict) -> pd.DataFrame:
    facilities = orgs["facilities"]
    providers = orgs["providers"]
    payers = orgs["payers"]
    n = CONFIG["n_encounters"]
    start = pd.to_datetime(CONFIG["date_start"])
    end = pd.to_datetime(CONFIG["date_end"])
    enc_types = ["inpatient", "outpatient", "outpatient", "emergency", "outpatient"]
    patient_ids = patients.sample(min(n, len(patients)), replace=True)["patient_id"].values
    encounters = []
    for i in range(n):
        admit = FAKE.date_time_between(start, end)
        enc_type = random.choice(enc_types)
        if enc_type == "inpatient":
            los_days = max(1, int(np.random.lognormal(2, 1.2)))
            discharge = admit + timedelta(days=los_days)
        else:
            discharge = admit + timedelta(hours=random.randint(1, 12))
        encounters.append({
            "encounter_id": f"E{i+1:010d}",
            "patient_id": patient_ids[i % len(patient_ids)],
            "facility_id": facilities.sample(1).iloc[0]["facility_id"],
            "provider_id": providers.sample(1).iloc[0]["provider_id"],
            "encounter_type": enc_type,
            "admit_date": admit,
            "discharge_date": discharge,
            "status": "completed",
            "payer_id": payers.sample(1).iloc[0]["payer_id"],
        })
    enc_df = pd.DataFrame(encounters)
    write_csv("encounters", enc_df)
    return enc_df


def generate_diagnoses_procedures_meds(encounters: pd.DataFrame, refs: dict) -> None:
    icd = refs["icd_codes"]
    cpt = refs["cpt_codes"]
    ndc = refs["ndc_codes"]
    diag_rows, proc_rows, med_rows = [], [], []
    diag_id, proc_id, med_id = 0, 0, 0
    for _, row in encounters.iterrows():
        eid = row["encounter_id"]
        n_diag = random.randint(1, 5)
        for s in range(n_diag):
            diag_id += 1
            diag_rows.append({
                "diagnosis_id": f"D{diag_id}",
                "encounter_id": eid,
                "icd_code": icd.sample(1).iloc[0]["icd_code"],
                "is_primary": 1 if s == 0 else 0,
                "sequence_num": s + 1,
            })
        n_proc = random.randint(0, 4)
        for s in range(n_proc):
            proc_id += 1
            proc_rows.append({
                "procedure_id": f"PR{proc_id}",
                "encounter_id": eid,
                "cpt_code": cpt.sample(1).iloc[0]["cpt_code"],
                "procedure_date": row["admit_date"],
                "quantity": random.randint(1, 2),
            })
        n_med = random.randint(0, 6)
        for s in range(n_med):
            med_id += 1
            med_rows.append({
                "medication_id": f"M{med_id}",
                "encounter_id": eid,
                "ndc_code": ndc.sample(1).iloc[0]["ndc_code"],
                "order_date": row["admit_date"],
                "quantity": round(random.uniform(1, 30), 2),
                "dose_unit": "mg",
            })
    write_csv("diagnoses", pd.DataFrame(diag_rows))
    write_csv("procedures", pd.DataFrame(proc_rows))
    write_csv("medications", pd.DataFrame(med_rows))


def generate_labs(encounters: pd.DataFrame) -> None:
    n_per_enc = CONFIG["n_labs_per_enc"]
    lab_codes = ["80053", "85025", "83036", "84443", "83540"]
    lab_names = ["CMP", "CBC", "HbA1c", "TSH", "Iron"]
    rows = []
    lid = 0
    for _, row in encounters.iterrows():
        for k in range(n_per_enc):
            lid += 1
            code = random.choice(lab_codes)
            name = lab_names[lab_codes.index(code)] if code in lab_codes else "Lab"
            val = round(random.gauss(100, 25), 2)
            rows.append({
                "lab_id": f"L{lid}",
                "encounter_id": row["encounter_id"],
                "patient_id": row["patient_id"],
                "lab_code": code,
                "lab_name": name,
                "result_value": str(val),
                "result_num": val,
                "result_unit": "mg/dL",
                "result_date": row["admit_date"],
            })
    write_csv("labs", pd.DataFrame(rows))


def generate_vitals(encounters: pd.DataFrame) -> None:
    vital_types = ["bp_systolic", "bp_diastolic", "heart_rate", "temp", "respiratory_rate"]
    rows = []
    vid = 0
    for _, row in encounters.iterrows():
        for vt in vital_types:
            vid += 1
            if vt == "bp_systolic":
                v = random.randint(100, 160)
            elif vt == "bp_diastolic":
                v = random.randint(60, 100)
            elif vt == "heart_rate":
                v = random.randint(55, 110)
            elif vt == "temp":
                v = round(random.uniform(96.5, 99.5), 1)
            else:
                v = random.randint(12, 22)
            rows.append({
                "vital_id": f"V{vid}",
                "encounter_id": row["encounter_id"],
                "patient_id": row["patient_id"],
                "vital_type": vt,
                "vital_value": v,
                "recorded_at": row["admit_date"],
            })
    write_csv("vitals", pd.DataFrame(rows))


def generate_claims(encounters: pd.DataFrame, refs: dict) -> None:
    cpt = refs["cpt_codes"]
    claim_rows = []
    line_rows = []
    line_id = 0
    for cidx, (_, row) in enumerate(encounters.iterrows(), start=1):
        total_charge = round(random.uniform(200, 50000), 2)
        total_paid = round(total_charge * random.uniform(0.5, 0.95), 2)
        ddate = row["discharge_date"]
        ddate_date = ddate.date() if hasattr(ddate, "date") else ddate
        claim_rows.append({
            "claim_id": f"C{cidx:08d}",
            "encounter_id": row["encounter_id"],
            "patient_id": row["patient_id"],
            "payer_id": row["payer_id"],
            "claim_type": "institutional" if row["encounter_type"] == "inpatient" else "professional",
            "total_charge": total_charge,
            "total_paid": total_paid,
            "claim_status": "paid",
            "submitted_date": ddate_date,
            "paid_date": (ddate + timedelta(days=random.randint(14, 60))).date() if hasattr(ddate, "date") else None,
        })
        n_lines = CONFIG["n_claim_lines_per_claim"]
        for ln in range(n_lines):
            line_id += 1
            chg = round(total_charge / n_lines * random.uniform(0.8, 1.2), 2)
            line_rows.append({
                "claim_line_id": f"CL{line_id}",
                "claim_id": f"C{cidx:08d}",
                "line_num": ln + 1,
                "cpt_code": cpt.sample(1).iloc[0]["cpt_code"],
                "charge_amt": chg,
                "paid_amt": round(chg * random.uniform(0.5, 1), 2),
                "units": random.randint(1, 3),
            })
    write_csv("claims", pd.DataFrame(claim_rows))
    write_csv("claim_lines", pd.DataFrame(line_rows))


def generate_utilization_events(encounters: pd.DataFrame) -> None:
    event_types = ["lab", "imaging", "medication", "procedure", "consult"]
    rows = []
    ueid = 0
    for _, row in encounters.iterrows():
        for _ in range(random.randint(1, 5)):
            ueid += 1
            rows.append({
                "event_id": f"UE{ueid}",
                "encounter_id": row["encounter_id"],
                "patient_id": row["patient_id"],
                "event_type": random.choice(event_types),
                "event_date": row["admit_date"],
                "quantity": random.randint(1, 3),
            })
    write_csv("utilization_events", pd.DataFrame(rows))


def generate_adverse_events(encounters: pd.DataFrame) -> None:
    event_types = ["fall", "medication_error", "infection", "pressure_ulcer", "other"]
    rows = []
    aeid = 0
    for _, row in encounters.sample(frac=0.02).iterrows():
        aeid += 1
        rows.append({
            "adverse_event_id": f"AE{aeid}",
            "encounter_id": row["encounter_id"],
            "patient_id": row["patient_id"],
            "event_type": random.choice(event_types),
            "event_date": row["admit_date"],
            "severity": random.choice(["low", "medium", "high"]),
        })
    write_csv("adverse_events", pd.DataFrame(rows))


def generate_readmissions(encounters: pd.DataFrame) -> None:
    inpatient = encounters[encounters["encounter_type"] == "inpatient"].copy()
    inpatient = inpatient.sort_values("discharge_date")
    readmit_rows = []
    rid = 0
    for pid in inpatient["patient_id"].unique()[:5000]:
        pat_encs = inpatient[inpatient["patient_id"] == pid].sort_values("discharge_date")
        for i in range(len(pat_encs) - 1):
            d1 = pat_encs.iloc[i]["discharge_date"]
            d2 = pat_encs.iloc[i + 1]["admit_date"]
            days = (d2 - d1).days if hasattr(d2 - d1, "days") else int((d2 - d1).total_seconds() / 86400)
            if 1 <= days <= 90:
                rid += 1
                readmit_rows.append({
                    "readmission_id": f"RM{rid}",
                    "encounter_id": pat_encs.iloc[i]["encounter_id"],
                    "patient_id": pid,
                    "index_discharge": d1,
                    "readmit_date": d2,
                    "days_to_readmit": days,
                    "is_30_day": 1 if days <= 30 else 0,
                })
    write_csv("readmissions", pd.DataFrame(readmit_rows))


def generate_risk_scores(patients: pd.DataFrame) -> None:
    start = pd.to_datetime(CONFIG["date_start"])
    end = pd.to_datetime(CONFIG["date_end"])
    rows = []
    for i, pid in enumerate(patients["patient_id"]):
        if i % 3 == 0:
            rows.append({
                "risk_score_id": f"RS{i+1}",
                "patient_id": pid,
                "score_date": FAKE.date_between(start, end),
                "risk_model": "readmission_risk_v1",
                "score_value": round(random.uniform(0.05, 0.65), 4),
                "risk_tier": random.choice(["low", "medium", "high"]),
            })
    write_csv("risk_scores", pd.DataFrame(rows))


def main():
    print("Generating reference tables...")
    refs = generate_reference_tables()
    print("Generating organizations...")
    orgs = generate_organizations(refs)
    print("Generating patients...")
    patients = generate_patients(orgs)
    print("Generating encounters...")
    encounters = generate_encounters(patients, orgs)
    print("Generating diagnoses, procedures, medications...")
    generate_diagnoses_procedures_meds(encounters, refs)
    print("Generating labs...")
    generate_labs(encounters)
    print("Generating vitals...")
    generate_vitals(encounters)
    print("Generating claims and claim_lines...")
    generate_claims(encounters, refs)
    print("Generating utilization_events and adverse_events...")
    generate_utilization_events(encounters)
    generate_adverse_events(encounters)
    print("Generating readmissions...")
    generate_readmissions(encounters)
    print("Generating risk_scores...")
    generate_risk_scores(patients)
    print("Done. Output in", OUT_DIR)


if __name__ == "__main__":
    main()
