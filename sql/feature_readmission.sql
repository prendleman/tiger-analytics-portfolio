-- Feature table for readmission prediction (encounter-level)
-- Joins: encounters, patients, diagnoses (count), labs (agg), readmissions (target)
-- Run against a database loaded with the healthcare schema and data.

WITH encounter_los AS (
    SELECT
        encounter_id,
        patient_id,
        facility_id,
        provider_id,
        encounter_type,
        admit_date,
        discharge_date,
        payer_id,
        DATEDIFF(day, admit_date, discharge_date) AS los_days
    FROM encounters
    WHERE status = 'completed'
),
diag_counts AS (
    SELECT encounter_id, COUNT(*) AS diag_count
    FROM diagnoses
    GROUP BY encounter_id
),
lab_agg AS (
    SELECT
        encounter_id,
        AVG(result_num) AS lab_mean,
        COUNT(*) AS lab_count
    FROM labs
    GROUP BY encounter_id
),
readmit_flag AS (
    SELECT encounter_id, 1 AS readmit_30
    FROM readmissions
    WHERE is_30_day = 1
)
SELECT
    e.encounter_id,
    e.patient_id,
    e.encounter_type,
    e.los_days,
    e.admit_date,
    DATEDIFF(year, p.date_of_birth, e.admit_date) AS age,
    p.gender,
    p.payer_id,
    ISNULL(d.diag_count, 0) AS diag_count,
    ISNULL(l.lab_mean, 0) AS lab_mean,
    ISNULL(l.lab_count, 0) AS lab_count,
    ISNULL(r.readmit_30, 0) AS readmit_30
FROM encounter_los e
JOIN patients p ON p.patient_id = e.patient_id
LEFT JOIN diag_counts d ON d.encounter_id = e.encounter_id
LEFT JOIN lab_agg l ON l.encounter_id = e.encounter_id
LEFT JOIN readmit_flag r ON r.encounter_id = e.encounter_id;
