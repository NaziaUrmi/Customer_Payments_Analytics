# Data dictionary

All values are synthetic. IDs are fictional. Amounts are EUR.

## customers.csv

| Column | Type | Meaning | Quality considerations |
|---|---|---|---|
| customer_id | string | Customer business key | Intended unique and non-null |
| customer_name | string | Fictional customer label | Not a real person's name |
| segment | category | Small Business, Mid-Market, Enterprise | Missing value intentionally inserted |
| region | category | Sales region | Trailing whitespace intentionally inserted for one value |
| customer_since | date | Customer start date | Check parsing and valid range |
| payment_terms_days | integer | Contracted payment terms | Expected positive value from 14, 30, 45, 60 |

## invoices.csv

| Column | Type | Meaning | Quality considerations |
|---|---|---|---|
| invoice_id | string | Invoice business key | Intended unique and non-null |
| customer_id | string | Customer reference | Must match customers |
| invoice_date | date | Invoice issue date | Must parse as date |
| due_date | date | Contractual due date | Usually invoice date + payment terms |
| invoice_amount | decimal | Invoice face value | A negative amount is intentionally inserted |
| currency | string | Currency code | EUR in this dataset |
| invoice_category | category | Subscription, services, hardware, support | Review category consistency |
| source_status | category | Open, Partially Paid, Paid, Cancelled | Treat as source label, not definitive payment truth |

## payments.csv

| Column | Type | Meaning | Quality considerations |
|---|---|---|---|
| payment_id | string | Payment transaction key | Intended unique |
| invoice_id | string | Invoice reference | One invoice may have multiple payments; one orphan reference intentionally inserted |
| payment_date | date | Payment transaction date | Must parse as date |
| payment_amount | decimal | Payment amount | Check non-positive values and overpayment behavior |
| payment_method | category | Bank Transfer, Direct Debit, Card | Validate categories |

## Important modeling note

The `source_status` field is generated as a simplified source-system label. The payment ledger is a separate transaction table and may not reconcile perfectly with the status label in every case. In later phases, use actual transaction totals and a documented business rule to derive balances. Investigate discrepancies instead of assuming the source status is correct.
