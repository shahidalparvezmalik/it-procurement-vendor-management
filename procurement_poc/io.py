"""CSV input validation and report generation."""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Iterable, Mapping

from .assessment import assess_contract

REQUIRED_COLUMNS = {
    "contract_id", "supplier_name", "category", "stage", "annual_value_eur",
    "renewal_date", "sla_target_pct", "sla_actual_pct", "on_time_delivery_pct",
    "quality_pass_pct", "open_major_issues",
}


def load_contracts(path: str | Path, as_of: date) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("input CSV must include a header row")
        missing = sorted(REQUIRED_COLUMNS.difference(reader.fieldnames))
        if missing:
            raise ValueError(f"input CSV is missing required columns: {', '.join(missing)}")
        records = [dict(row) for row in reader]
    if not records:
        raise ValueError("input CSV contains no contract records")

    seen: set[str] = set()
    for line, record in enumerate(records, start=2):
        try:
            assessed = assess_contract(record, as_of)
        except ValueError as exc:
            raise ValueError(f"invalid record on CSV line {line}: {exc}") from exc
        key = str(assessed["contract_id"])
        if key in seen:
            raise ValueError(f"duplicate contract_id on CSV line {line}: {key}")
        seen.add(key)
    return records


def write_reports(records: Iterable[Mapping[str, str]], output_dir: str | Path,
                  as_of: date) -> dict[str, Path]:
    results = [assess_contract(row, as_of) for row in records]
    if not results:
        raise ValueError("at least one contract record is required")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    scorecard_path = out / "supplier_scorecards.csv"
    renewal_path = out / "contract_renewal_flags.csv"
    summary_path = out / "management_summary.json"
    review_path = out / "human_review_template.csv"
    fields = [
        "contract_id", "supplier_name", "category", "stage", "annual_value_eur",
        "renewal_date", "days_to_renewal", "sla_target_pct", "sla_actual_pct",
        "on_time_delivery_pct", "quality_pass_pct", "open_major_issues",
        "performance_score", "performance_status", "sla_below_target",
        "review_reasons", "human_review_required", "action_executed",
    ]

    def write_csv(path: Path, rows: list[Mapping[str, object]], columns: list[str]) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                clean = dict(row)
                if "review_reasons" in clean and isinstance(clean["review_reasons"], list):
                    clean["review_reasons"] = "; ".join(clean["review_reasons"])
                if "human_review_required" in clean:
                    clean["human_review_required"] = str(clean["human_review_required"]).lower()
                if "action_executed" in clean:
                    clean["action_executed"] = str(clean["action_executed"]).lower()
                if "sla_below_target" in clean and isinstance(clean["sla_below_target"], bool):
                    clean["sla_below_target"] = str(clean["sla_below_target"]).lower()
                writer.writerow(clean)

    write_csv(scorecard_path, results, fields)
    flagged = [row for row in results if row["review_reasons"]]
    write_csv(renewal_path, flagged, fields)

    stages = Counter(str(row["stage"]) for row in results)
    due_soon = sum(1 for row in results if row["days_to_renewal"] != "" and 0 <= int(row["days_to_renewal"]) <= 90)
    overdue = sum(1 for row in results if row["days_to_renewal"] != "" and int(row["days_to_renewal"]) < 0)
    scored = [row for row in results if row["performance_score"] != ""]
    summary = {
        "assessment_date": as_of.isoformat(),
        "synthetic_demo": True,
        "assessment_method": "transparent_rules_baseline",
        "contracts_assessed": len(results),
        "distinct_suppliers": len({str(row["supplier_name"]) for row in results}),
        "contracts_by_stage": dict(sorted(stages.items())),
        "renewals_due_within_90_days": due_soon,
        "renewal_dates_passed": overdue,
        "contracts_flagged_for_review": len(flagged),
        "supplier_records_scored": len(scored),
        "human_review_required": len(results),
        "actions_executed": 0,
        "synthetic_annual_value_total_eur": round(sum(float(row["annual_value_eur"]) for row in results), 2),
        "limitations": [
            "Supplier metrics and values are fictional and not procurement evidence.",
            "The weighted score is a transparent review aid, not a calibrated supplier rating.",
            "Renewal flags prompt human review and do not make sourcing, renewal, or payment decisions.",
        ],
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    review_rows = [
        {"contract_id": row["contract_id"], "reviewer": "", "decision": "", "notes": "", "reviewed_at": ""}
        for row in results
    ]
    write_csv(review_path, review_rows, ["contract_id", "reviewer", "decision", "notes", "reviewed_at"])
    return {"scorecards": scorecard_path, "renewal_flags": renewal_path,
            "summary": summary_path, "review_template": review_path}
