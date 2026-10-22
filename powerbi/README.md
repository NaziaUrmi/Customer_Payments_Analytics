# Power BI phase (later)

Power BI Desktop is not currently available, so this phase can wait. For now, use Python/Matplotlib charts and CSV summary outputs.

When Power BI Desktop becomes available:
1. Import validated customer, invoice, and payment tables.
2. Create one-to-many relationships from Customers to Invoices and Invoices to Payments.
3. Aggregate payments by invoice before calculating invoice-level balances to avoid double-counting.
4. Create measures only after KPI definitions and reporting date are agreed.
5. Suggested pages: Executive Overview; Aging & Collections; Customer/Region Drilldown; Data Quality.
6. Validate totals against SQL and Python before publishing screenshots.

Suggested visuals: KPI cards, monthly trend, aging-bucket bar chart, segment/region matrix, and a detail table with drill-through.
