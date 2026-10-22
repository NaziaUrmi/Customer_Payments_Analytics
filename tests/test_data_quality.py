"""Basic tests for the generated raw data. Run generator before tests."""
from pathlib import Path
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

class TestGeneratedData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.customers = pd.read_csv(RAW / "customers.csv", dtype={"customer_id": "string"})
        cls.invoices = pd.read_csv(RAW / "invoices.csv", dtype={"invoice_id": "string", "customer_id": "string"})
        cls.payments = pd.read_csv(RAW / "payments.csv", dtype={"payment_id": "string", "invoice_id": "string"})

    def test_expected_scale(self):
        self.assertGreaterEqual(len(self.customers), 1000)
        self.assertEqual(len(self.invoices), 5000)
        self.assertGreater(len(self.payments), 1000)

    def test_invoice_ids_are_unique(self):
        self.assertTrue(self.invoices["invoice_id"].is_unique)

    def test_payment_ids_are_unique(self):
        self.assertTrue(self.payments["payment_id"].is_unique)

    def test_known_duplicate_customer_is_present_in_raw_data(self):
        self.assertFalse(self.customers["customer_id"].is_unique)

    def test_known_orphan_payment_is_present(self):
        self.assertGreater((~self.payments["invoice_id"].isin(self.invoices["invoice_id"])).sum(), 0)

if __name__ == "__main__":
    unittest.main()
