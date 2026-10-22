"""Generate reproducible synthetic customer, invoice, and payment CSV files."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SEED = 20261022

def main():
    rng = np.random.default_rng(SEED)
    RAW.mkdir(parents=True, exist_ok=True)

    n_customers = 1000
    customer_ids = [f"C{i:05d}" for i in range(1, n_customers + 1)]
    segments = rng.choice(["Small Business", "Mid-Market", "Enterprise"], n_customers, p=[0.55, 0.30, 0.15])
    regions = rng.choice(["DACH", "Western Europe", "Nordics", "Southern Europe"], n_customers, p=[0.45, 0.25, 0.15, 0.15])
    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "customer_name": [f"Customer {i:04d}" for i in range(1, n_customers + 1)],
        "segment": segments,
        "region": regions,
        "customer_since": pd.to_datetime(rng.integers(pd.Timestamp("2018-01-01").value // 10**9,
                                                        pd.Timestamp("2025-12-31").value // 10**9,
                                                        n_customers), unit="s").date.astype(str),
        "payment_terms_days": rng.choice([14, 30, 45, 60], n_customers, p=[0.10, 0.60, 0.20, 0.10])
    })

    n_invoices = 5000
    invoice_ids = [f"INV{i:06d}" for i in range(1, n_invoices + 1)]
    cust_idx = rng.integers(0, n_customers, n_invoices)
    invoice_dates = pd.to_datetime(rng.integers(pd.Timestamp("2024-01-01").value // 10**9,
                                                 pd.Timestamp("2026-09-30").value // 10**9,
                                                 n_invoices), unit="s").normalize()
    amounts = np.round(np.exp(rng.normal(np.log(850), 0.8, n_invoices)), 2)
    # Simulated invoice status is descriptive source data, not used as the only source of payment truth.
    invoices = pd.DataFrame({
        "invoice_id": invoice_ids,
        "customer_id": np.array(customer_ids)[cust_idx],
        "invoice_date": invoice_dates.date.astype(str),
        "due_date": (invoice_dates + pd.to_timedelta(np.array(customers["payment_terms_days"])[cust_idx], unit="D")).date.astype(str),
        "invoice_amount": amounts,
        "currency": "EUR",
        "invoice_category": rng.choice(["Subscription", "Professional Services", "Hardware", "Support"], n_invoices, p=[0.45, 0.25, 0.15, 0.15]),
        "source_status": rng.choice(["Open", "Partially Paid", "Paid", "Cancelled"], n_invoices, p=[0.22, 0.13, 0.62, 0.03])
    })

    payment_rows = []
    payment_counter = 1
    for row in invoices.itertuples(index=False):
        status = row.source_status
        if status == "Cancelled":
            continue
        if status == "Open":
            continue
        invoice_amount = float(row.invoice_amount)
        if status == "Paid":
            paid_fraction = 1.0
        else:
            paid_fraction = float(rng.uniform(0.15, 0.80))
        amount_to_pay = round(invoice_amount * paid_fraction, 2)
        n_parts = int(rng.choice([1, 2, 3], p=[0.72, 0.23, 0.05]))
        remaining = amount_to_pay
        due = pd.Timestamp(row.due_date)
        inv_date = pd.Timestamp(row.invoice_date)
        for part in range(n_parts):
            if part == n_parts - 1:
                part_amount = round(remaining, 2)
            else:
                part_amount = round(amount_to_pay / n_parts, 2)
                remaining -= part_amount
            delay = int(rng.normal(12, 24))
            pay_date = max(inv_date, due + pd.Timedelta(days=delay + part * int(rng.integers(1, 8))))
            # Keep payments inside a plausible generated reporting window.
            pay_date = min(pay_date, pd.Timestamp("2026-10-15"))
            payment_rows.append({
                "payment_id": f"PAY{payment_counter:07d}",
                "invoice_id": row.invoice_id,
                "payment_date": pay_date.date().isoformat(),
                "payment_amount": part_amount,
                "payment_method": rng.choice(["Bank Transfer", "Direct Debit", "Card"], p=[0.70, 0.20, 0.10])
            })
            payment_counter += 1

    payments = pd.DataFrame(payment_rows)

    # Insert a small set of intentional raw-data issues for data-quality practice.
    issue_rows = []
    # Duplicate one customer row (a second copy of the same key).
    customers = pd.concat([customers, customers.iloc[[17]]], ignore_index=True)
    issue_rows.append({"table_name":"customers","record_key":customers.iloc[-1]["customer_id"],"issue_type":"duplicate_key","description":"One customer row duplicated intentionally."})
    # Missing segment.
    customers.loc[customers["customer_id"] == "C00042", "segment"] = np.nan
    issue_rows.append({"table_name":"customers","record_key":"C00042","issue_type":"missing_value","description":"Customer segment intentionally missing."})
    # Unexpected region label.
    customers.loc[customers["customer_id"] == "C00077", "region"] = "DACH "
    issue_rows.append({"table_name":"customers","record_key":"C00077","issue_type":"inconsistent_category","description":"Region has trailing whitespace intentionally."})
    # Invalid invoice amount.
    invoices.loc[invoices["invoice_id"] == "INV000123", "invoice_amount"] = -125.00
    issue_rows.append({"table_name":"invoices","record_key":"INV000123","issue_type":"invalid_range","description":"Invoice amount is negative intentionally."})
    # Payment references a nonexistent invoice.
    if not payments.empty:
        payments.loc[len(payments)] = {
            "payment_id": f"PAY{payment_counter:07d}",
            "invoice_id": "INV999999",
            "payment_date": "2026-09-15",
            "payment_amount": 99.99,
            "payment_method": "Bank Transfer"
        }
        issue_rows.append({"table_name":"payments","record_key":f"PAY{payment_counter:07d}","issue_type":"orphan_foreign_key","description":"Payment references an invoice that does not exist."})

    customers.to_csv(RAW / "customers.csv", index=False)
    invoices.to_csv(RAW / "invoices.csv", index=False)
    payments.to_csv(RAW / "payments.csv", index=False)
    pd.DataFrame(issue_rows).to_csv(RAW / "data_quality_issues.csv", index=False)
    print(f"Generated synthetic data in {RAW}")
    print(f"customers={len(customers):,}; invoices={len(invoices):,}; payments={len(payments):,}")
    print("Intentional data-quality issues are documented in data_quality_issues.csv.")

if __name__ == "__main__":
    main()
