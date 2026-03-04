-- Monthly PMPM (per member per month) summary for forecasting and reporting.
-- Feeds time series models (SARIMA, Prophet). Compatible with claims table.
SELECT
    DATEADD(month, DATEDIFF(month, 0, CAST(c.submitted_date AS date)), 0) AS service_month,
    SUM(c.total_paid)    AS total_paid,
    SUM(c.total_charge)  AS total_charge,
    COUNT(DISTINCT c.patient_id) AS member_count,
    COUNT(c.claim_id)    AS claim_count,
    SUM(c.total_paid) * 1.0 / NULLIF(COUNT(DISTINCT c.patient_id), 0) AS pmpm_paid,
    SUM(c.total_charge) * 1.0 / NULLIF(COUNT(DISTINCT c.patient_id), 0) AS pmpm_charge
FROM claims c
WHERE c.claim_status = 'paid'
GROUP BY DATEADD(month, DATEDIFF(month, 0, CAST(c.submitted_date AS date)), 0)
ORDER BY service_month;
