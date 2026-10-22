"""Starter cleaner: report quality issues and write conservative processed copies."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    customers = pd.read_csv(RAW / "customers.csv", dtype={"customer_id": "string"})
    invoices = pd.read_csv(RAW / "invoices.csv", dtype={"invoice_id": "string", "customer_id": "string"})
    payments = pd.read_csv(RAW / "payments.csv", dtype={"payment_id": "string", "invoice_id": "string"})

    report = []
    def add(table, check, count, note):
        report.append({"table": table, "check": check, "issue_count": int(count), "note": note})

    add("customers", "duplicate customer_id rows", customers.duplicated("customer_id", keep=False).sum(),
        "Inspect duplicate rows; do not automatically discard if attributes differ.")
    add("customers", "missing segment", customers["segment"].isna().sum(),
        "Keep missing values visible until a documented imputation/business rule is agreed.")
    add("customers", "region whitespace", customers["region"].astype("string").str.strip().ne(customers["region"].astype("string")).sum(),
        "Whitespace can be normalized, but retain a record of the transformation.")
    add("invoices", "non-positive invoice_amount", invoices["invoice_amount"].le(0).sum(),
        "Investigate; do not assume a negative value is valid or invalid without business context.")
    add("invoices", "missing customer reference", invoices["customer_id"].isna().sum(),
        "Check referential integrity against customers.")
    add("payments", "non-positive payment_amount", payments["payment_amount"].le(0).sum(),
        "Investigate refunds/adjustments separately if present.")
    add("payments", "orphan invoice reference", (~payments["invoice_id"].isin(invoices["invoice_id"])).sum(),
        "Payment invoice_id does not exist in invoices.")

    # Conservative normalization: trim text whitespace only. Keep other issues for analyst review.
    customers["region"] = customers["region"].astype("string").str.strip()
    customers.to_csv(OUT / "customers_review.csv", index=False)
    invoices.to_csv(OUT / "invoices_review.csv", index=False)
    payments.to_csv(OUT / "payments_review.csv", index=False)
    pd.DataFrame(report).to_csv(OUT / "data_quality_report.csv", index=False)
    print(pd.DataFrame(report).to_string(index=False))
    print(f"\nWrote review copies and report to {OUT}")
    print("These are review outputs, not fully certified clean data. Resolve flagged issues with documented rules.")

if __name__ == "__main__":
    main()
