-- Monthly PMPM summary (PostgreSQL). Same logic as monthly_pmpm_summary.sql (SQL Server).
SELECT
    date_trunc('month', (c.submitted_date)::date)::date AS service_month,
    SUM(c.total_paid)    AS total_paid,
    SUM(c.total_charge)  AS total_charge,
    COUNT(DISTINCT c.patient_id) AS member_count,
    COUNT(c.claim_id)    AS claim_count,
    SUM(c.total_paid)::float / NULLIF(COUNT(DISTINCT c.patient_id), 0) AS pmpm_paid,
    SUM(c.total_charge)::float / NULLIF(COUNT(DISTINCT c.patient_id), 0) AS pmpm_charge
FROM claims c
WHERE c.claim_status = 'paid'
GROUP BY date_trunc('month', (c.submitted_date)::date)
ORDER BY service_month;
