-- Healthcare Analytics Schema (SQL Server / PostgreSQL compatible)
-- Portfolio: Tiger Analytics Lead Data Scientist - mock healthcare dataset

-- Reference tables
CREATE TABLE facility_types (
    facility_type_id   VARCHAR(10) PRIMARY KEY,
    facility_type_name VARCHAR(100) NOT NULL
);

CREATE TABLE specialties (
    specialty_id   VARCHAR(10) PRIMARY KEY,
    specialty_name VARCHAR(100) NOT NULL
);

CREATE TABLE icd_codes (
    icd_code    VARCHAR(10) PRIMARY KEY,
    description VARCHAR(500),
    chapter     VARCHAR(50)
);

CREATE TABLE cpt_codes (
    cpt_code    VARCHAR(15) PRIMARY KEY,
    description VARCHAR(500),
    category    VARCHAR(50)
);

CREATE TABLE ndc_codes (
    ndc_code    VARCHAR(20) PRIMARY KEY,
    description VARCHAR(500),
    drug_class  VARCHAR(100)
);

-- Organizations
CREATE TABLE organizations (
    organization_id   VARCHAR(20) PRIMARY KEY,
    organization_name VARCHAR(200) NOT NULL,
    parent_id        VARCHAR(20) REFERENCES organizations(organization_id)
);

CREATE TABLE payers (
    payer_id   VARCHAR(20) PRIMARY KEY,
    payer_name VARCHAR(200) NOT NULL,
    payer_type VARCHAR(50)  -- commercial, medicare, medicaid, other
);

CREATE TABLE facilities (
    facility_id       VARCHAR(20) PRIMARY KEY,
    facility_name     VARCHAR(200) NOT NULL,
    facility_type_id  VARCHAR(10) NOT NULL REFERENCES facility_types(facility_type_id),
    organization_id   VARCHAR(20) REFERENCES organizations(organization_id),
    address_line1     VARCHAR(200),
    city              VARCHAR(100),
    state             VARCHAR(2),
    zip               VARCHAR(10)
);

CREATE TABLE providers (
    provider_id   VARCHAR(20) PRIMARY KEY,
    provider_name VARCHAR(200) NOT NULL,
    specialty_id  VARCHAR(10) NOT NULL REFERENCES specialties(specialty_id),
    facility_id   VARCHAR(20) REFERENCES facilities(facility_id),
    npi           VARCHAR(15)
);

-- Core clinical
CREATE TABLE patients (
    patient_id    VARCHAR(20) PRIMARY KEY,
    date_of_birth DATE NOT NULL,
    gender        VARCHAR(10),
    race          VARCHAR(50),
    ethnicity     VARCHAR(50),
    zip           VARCHAR(10),
    payer_id      VARCHAR(20) REFERENCES payers(payer_id),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE encounters (
    encounter_id   VARCHAR(20) PRIMARY KEY,
    patient_id     VARCHAR(20) NOT NULL REFERENCES patients(patient_id),
    facility_id    VARCHAR(20) NOT NULL REFERENCES facilities(facility_id),
    provider_id    VARCHAR(20) REFERENCES providers(provider_id),
    encounter_type VARCHAR(50) NOT NULL,  -- inpatient, outpatient, emergency, etc.
    admit_date     TIMESTAMP NOT NULL,
    discharge_date TIMESTAMP,
    status         VARCHAR(20),  -- completed, in_progress, cancelled
    payer_id       VARCHAR(20) REFERENCES payers(payer_id)
);

CREATE TABLE diagnoses (
    diagnosis_id  VARCHAR(20) PRIMARY KEY,
    encounter_id  VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    icd_code     VARCHAR(10) NOT NULL REFERENCES icd_codes(icd_code),
    is_primary    SMALLINT DEFAULT 0,
    sequence_num  INT
);

CREATE TABLE procedures (
    procedure_id  VARCHAR(20) PRIMARY KEY,
    encounter_id  VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    cpt_code      VARCHAR(15) NOT NULL REFERENCES cpt_codes(cpt_code),
    procedure_date TIMESTAMP,
    quantity      INT DEFAULT 1
);

CREATE TABLE medications (
    medication_id   VARCHAR(20) PRIMARY KEY,
    encounter_id   VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    ndc_code       VARCHAR(20) NOT NULL REFERENCES ndc_codes(ndc_code),
    order_date     TIMESTAMP,
    quantity       DECIMAL(12,4),
    dose_unit      VARCHAR(20)
);

CREATE TABLE labs (
    lab_id        VARCHAR(20) PRIMARY KEY,
    encounter_id  VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    patient_id    VARCHAR(20) NOT NULL REFERENCES patients(patient_id),
    lab_code      VARCHAR(20) NOT NULL,
    lab_name      VARCHAR(200),
    result_value  VARCHAR(100),
    result_num    DECIMAL(18,4),
    result_unit   VARCHAR(20),
    result_date   TIMESTAMP NOT NULL
);

CREATE TABLE vitals (
    vital_id      VARCHAR(20) PRIMARY KEY,
    encounter_id  VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    patient_id    VARCHAR(20) NOT NULL REFERENCES patients(patient_id),
    vital_type    VARCHAR(50) NOT NULL,  -- bp_systolic, bp_diastolic, heart_rate, temp, etc.
    vital_value   DECIMAL(10,2),
    recorded_at   TIMESTAMP NOT NULL
);

-- Utilization / finance
CREATE TABLE claims (
    claim_id      VARCHAR(20) PRIMARY KEY,
    encounter_id  VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    patient_id    VARCHAR(20) NOT NULL REFERENCES patients(patient_id),
    payer_id      VARCHAR(20) NOT NULL REFERENCES payers(payer_id),
    claim_type    VARCHAR(50),  -- professional, institutional
    total_charge  DECIMAL(14,2),
    total_paid    DECIMAL(14,2),
    claim_status  VARCHAR(20),
    submitted_date DATE,
    paid_date     DATE
);

CREATE TABLE claim_lines (
    claim_line_id VARCHAR(20) PRIMARY KEY,
    claim_id      VARCHAR(20) NOT NULL REFERENCES claims(claim_id),
    line_num      INT NOT NULL,
    cpt_code      VARCHAR(15) REFERENCES cpt_codes(cpt_code),
    charge_amt    DECIMAL(14,2),
    paid_amt      DECIMAL(14,2),
    units         INT DEFAULT 1
);

CREATE TABLE utilization_events (
    event_id      VARCHAR(20) PRIMARY KEY,
    encounter_id  VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    patient_id    VARCHAR(20) NOT NULL REFERENCES patients(patient_id),
    event_type    VARCHAR(50) NOT NULL,
    event_date    TIMESTAMP NOT NULL,
    quantity      INT DEFAULT 1
);

-- Outcomes / risk (ML targets)
CREATE TABLE readmissions (
    readmission_id   VARCHAR(20) PRIMARY KEY,
    encounter_id     VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    patient_id       VARCHAR(20) NOT NULL REFERENCES patients(patient_id),
    index_discharge  TIMESTAMP NOT NULL,
    readmit_date     TIMESTAMP NOT NULL,
    days_to_readmit  INT NOT NULL,
    is_30_day        SMALLINT NOT NULL  -- 1 if days_to_readmit <= 30
);

CREATE TABLE adverse_events (
    adverse_event_id VARCHAR(20) PRIMARY KEY,
    encounter_id     VARCHAR(20) NOT NULL REFERENCES encounters(encounter_id),
    patient_id       VARCHAR(20) NOT NULL REFERENCES patients(patient_id),
    event_type       VARCHAR(100) NOT NULL,
    event_date       TIMESTAMP NOT NULL,
    severity         VARCHAR(20)
);

CREATE TABLE risk_scores (
    risk_score_id VARCHAR(20) PRIMARY KEY,
    patient_id    VARCHAR(20) NOT NULL REFERENCES patients(patient_id),
    score_date    DATE NOT NULL,
    risk_model    VARCHAR(100) NOT NULL,
    score_value   DECIMAL(8,4),
    risk_tier     VARCHAR(20)  -- low, medium, high
);

-- Indexes for common queries and joins
CREATE INDEX idx_encounters_patient ON encounters(patient_id);
CREATE INDEX idx_encounters_dates ON encounters(admit_date, discharge_date);
CREATE INDEX idx_diagnoses_encounter ON diagnoses(encounter_id);
CREATE INDEX idx_claims_encounter ON claims(encounter_id);
CREATE INDEX idx_labs_patient_date ON labs(patient_id, result_date);
CREATE INDEX idx_readmissions_patient ON readmissions(patient_id);
