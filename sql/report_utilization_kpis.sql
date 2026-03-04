-- Utilization and cost KPIs by facility and payer
-- Reporting/BI-style aggregations from encounters and claims.

SELECT
    f.facility_name,
    f.facility_type_id,
    pt.payer_type,
    COUNT(DISTINCT e.encounter_id) AS encounter_count,
    COUNT(DISTINCT e.patient_id) AS patient_count,
    SUM(CASE WHEN e.encounter_type = 'inpatient' THEN 1 ELSE 0 END) AS inpatient_count,
    AVG(DATEDIFF(day, e.admit_date, e.discharge_date)) AS avg_los_days,
    SUM(c.total_charge) AS total_charge,
    SUM(c.total_paid) AS total_paid,
    AVG(c.total_paid) AS avg_paid_per_claim
FROM encounters e
JOIN facilities f ON f.facility_id = e.facility_id
JOIN payers pt ON pt.payer_id = e.payer_id
LEFT JOIN claims c ON c.encounter_id = e.encounter_id
WHERE e.status = 'completed'
GROUP BY f.facility_name, f.facility_type_id, pt.payer_type
ORDER BY encounter_count DESC;
