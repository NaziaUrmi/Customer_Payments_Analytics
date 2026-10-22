# Loading CSVs into SQL Server

The raw data intentionally includes a duplicate customer key and an orphan payment reference. A table with primary/foreign-key constraints may reject those rows. This is expected and is part of the exercise.

Recommended learning approach:
1. Import raw CSVs into staging tables with permissive columns (no primary/foreign-key constraints).
2. Run quality checks in `03_starter_queries.sql`.
3. Document how each issue will be resolved.
4. Load only validated records into `dbo.Customers`, `dbo.Invoices`, and `dbo.Payments`.

In SSMS, you can use **Tasks → Import Flat File** or the Import Data wizard. Import customers first, then invoices, then payments. If you are using SQL Server Developer/Express on your local computer, check the local server instance name and permissions.

Do not use `BULK INSERT` with a guessed file path: SQL Server reads files from the server machine and requires appropriate permissions. For a beginner, the SSMS import wizard is usually simpler.

Before importing into constrained final tables:
- resolve the duplicate `customer_id`;
- decide how to handle missing segment and normalize category values;
- investigate the negative invoice amount;
- reject/quarantine the orphan payment;
- verify row counts and financial totals.
