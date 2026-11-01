import csv
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from procurement_poc.assessment import assess_contract
from procurement_poc.io import load_contracts, write_reports

AS_OF = date(2026, 10, 26)


def contract(**overrides):
    row = {
        "contract_id": "C-TEST",
        "supplier_name": "Synthetic Supplier",
        "category": "Support",
        "stage": "active",
        "annual_value_eur": "10000",
        "renewal_date": "2027-04-01",
        "sla_target_pct": "99",
        "sla_actual_pct": "99.5",
        "on_time_delivery_pct": "96",
        "quality_pass_pct": "98",
        "open_major_issues": "0",
    }
    row.update(overrides)
    return row


class AssessmentTests(unittest.TestCase):
    def test_good_performance_is_transparent_and_requires_review(self):
        result = assess_contract(contract(), AS_OF)
        self.assertEqual(result["performance_score"], 97.9)
        self.assertEqual(result["performance_status"], "on_track")
        self.assertTrue(result["human_review_required"])
        self.assertFalse(result["action_executed"])

    def test_renewal_within_90_days_is_flagged(self):
        result = assess_contract(contract(renewal_date="2026-11-30"), AS_OF)
        self.assertEqual(result["days_to_renewal"], 35)
        self.assertIn("renewal is within 90 days; begin human review", result["review_reasons"])

    def test_missed_sla_target_is_flagged_even_if_weighted_score_is_high(self):
        result = assess_contract(contract(sla_actual_pct="98.9"), AS_OF)
        self.assertTrue(result["sla_below_target"])
        self.assertIn("reported SLA is below the stated target", result["review_reasons"])
        self.assertEqual(result["performance_status"], "review")

    def test_expired_renewal_date_is_flagged_for_status_check(self):
        result = assess_contract(contract(renewal_date="2026-09-30"), AS_OF)
        self.assertEqual(result["days_to_renewal"], -26)
        self.assertIn("renewal date has passed; verify contract status", result["review_reasons"])

    def test_pipeline_record_without_metrics_is_not_scored(self):
        row = contract(stage="tender", renewal_date="", sla_target_pct="", sla_actual_pct="",
                       on_time_delivery_pct="", quality_pass_pct="")
        result = assess_contract(row, AS_OF)
        self.assertEqual(result["performance_status"], "not_scored")
        self.assertEqual(result["performance_score"], "")

    def test_partial_performance_metrics_are_rejected(self):
        row = contract(on_time_delivery_pct="")
        with self.assertRaisesRegex(ValueError, "all supplied or all blank"):
            assess_contract(row, AS_OF)

    def test_percentage_above_100_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "at most 100"):
            assess_contract(contract(quality_pass_pct="101"), AS_OF)

    def test_bundled_dataset_has_expected_review_only_outputs(self):
        root = Path(__file__).resolve().parents[1]
        records = load_contracts(root / "data" / "contracts.csv", AS_OF)
        self.assertEqual(len(records), 8)
        with tempfile.TemporaryDirectory() as directory:
            paths = write_reports(records, directory, AS_OF)
            with paths["summary"].open(encoding="utf-8") as handle:
                summary = json.load(handle)
            with paths["scorecards"].open(encoding="utf-8", newline="") as handle:
                scorecards = list(csv.DictReader(handle))
            with paths["renewal_flags"].open(encoding="utf-8", newline="") as handle:
                flagged = list(csv.DictReader(handle))
        self.assertEqual(summary["contracts_assessed"], 8)
        self.assertEqual(summary["distinct_suppliers"], 8)
        self.assertEqual(summary["renewals_due_within_90_days"], 2)
        self.assertEqual(summary["renewal_dates_passed"], 1)
        self.assertEqual(summary["human_review_required"], 8)
        self.assertEqual(summary["actions_executed"], 0)
        self.assertEqual(len(scorecards), 8)
        self.assertEqual(len(flagged), summary["contracts_flagged_for_review"])
        self.assertTrue(all(row["action_executed"] == "false" for row in scorecards))

    def test_loader_rejects_duplicate_contract_ids(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contracts.csv"
            rows = [contract(), contract(supplier_name="Another Synthetic Supplier")]
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "duplicate contract_id"):
                load_contracts(path, AS_OF)


if __name__ == "__main__":
    unittest.main()
