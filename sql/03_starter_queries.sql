/*
Starter SQL exercises. Adapt table names to your staging/final schema.
Do not run all business KPIs until data quality issues are investigated.
*/
USE CustomerPaymentsAnalytics;
GO

-- 1. Count rows in each table.
SELECT COUNT(*) AS customer_count FROM dbo.Customers;
SELECT COUNT(*) AS invoice_count FROM dbo.Invoices;
SELECT COUNT(*) AS payment_count FROM dbo.Payments;

-- 2. Check for duplicate customer keys in staging data.
-- SELECT customer_id, COUNT(*) AS row_count
-- FROM dbo.Customers_Staging
-- GROUP BY customer_id
-- HAVING COUNT(*) > 1;

-- 3. Find invoices with invalid/non-positive amounts.
SELECT invoice_id, invoice_amount
FROM dbo.Invoices
WHERE invoice_amount <= 0;

-- 4. Monthly invoiced amount (confirm how cancellations should be treated).
SELECT YEAR(invoice_date) AS invoice_year,
       MONTH(invoice_date) AS invoice_month,
       SUM(invoice_amount) AS invoiced_amount
FROM dbo.Invoices
WHERE source_status <> 'Cancelled'
GROUP BY YEAR(invoice_date), MONTH(invoice_date)
ORDER BY invoice_year, invoice_month;

-- 5. Payment totals per invoice. Aggregate payments before joining to invoices
-- to avoid duplicating invoice_amount when an invoice has multiple payments.
WITH PaymentTotals AS (
    SELECT invoice_id, SUM(payment_amount) AS amount_paid
    FROM dbo.Payments
    GROUP BY invoice_id
)
SELECT i.invoice_id, i.invoice_amount,
       COALESCE(p.amount_paid, 0) AS amount_paid,
       i.invoice_amount - COALESCE(p.amount_paid, 0) AS raw_balance
FROM dbo.Invoices AS i
LEFT JOIN PaymentTotals AS p ON p.invoice_id = i.invoice_id;

-- Exercises:
-- A. Find the top 10 customers by outstanding balance.
-- B. Create aging buckets: not due, 1-30, 31-60, 61-90, 90+ days overdue.
-- C. Rank customers by total overdue balance using DENSE_RANK().
-- D. Compare monthly payment cash-in with monthly invoiced amount; explain why
--    these are different metrics and should not be treated as equivalent.
