# Phase 1 beginner exercises

Complete these after running `python src/generate_data.py`.

## Exercise 1 — Learn the files
1. Open each CSV and identify what one row represents.
2. Write down the primary key and foreign key for each table.
3. Use Python to print each file's row count and column names.

Starter:
```python
import pandas as pd
customers = pd.read_csv("data/raw/customers.csv")
print(customers.shape)
print(customers.columns.tolist())
print(customers.head())
```

## Exercise 2 — Inspect types and missing values
Run `customers.info()` and `customers.isna().sum()`. Repeat for invoices and payments.
- Which columns have missing values?
- Which date columns should be parsed as dates?
- Why are IDs strings rather than numbers?

## Exercise 3 — Check keys and relationships
- Find duplicate customer IDs.
- Count payments whose invoice ID is absent from invoices.
- Count invoices whose customer ID is absent from customers.
- Do not delete anything until you explain the proposed treatment.

## Exercise 4 — Check numeric validity
- Find invoice amounts <= 0.
- Find payment amounts <= 0.
- Inspect the minimum, maximum, median, and 95th percentile of invoice amounts.
- Are outliers always errors? Explain.

## Exercise 5 — Create a quality summary
Run:
```bash
python src/clean_data.py
```
Open `data/processed/data_quality_report.csv` and explain each check in your own words. Compare the report to `data/raw/data_quality_issues.csv`, but do not treat the issue register as a substitute for validation.

## Exercise 6 — Write your first business question
In your own words, answer:
- What does “overdue” mean?
- Which date should be used as the reporting date?
- How should cancelled invoices be treated?
- How should overpayments, refunds, and partial payments be handled?
Document assumptions before calculating KPIs.

## Exercise 7 — Reflection
Create a file `reports/phase1_notes.md` with:
- three things you learned;
- three data-quality risks;
- two questions you would ask a finance stakeholder;
- one rule you would not apply without business approval.

## Success criteria
- You can explain all three data tables.
- You can run the generator and quality report from the terminal.
- You can identify at least the intentional issues and explain why each matters.
- You have not claimed any business improvement or predictive result.
