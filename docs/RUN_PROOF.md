# Local run proof

Verified locally on 2026-10-26 from both the source folder and the extracted ZIP bundle.

Commands run in each location:

```text
python -m unittest discover -v
python -m compileall -q procurement_poc tests
python -m procurement_poc.cli --input data/contracts.csv --output-dir <temporary-report-dir> --as-of 2026-10-26
```

Both runs passed. The test suite reported **9 tests, OK**. `compileall` exited 0.

The CLI reported:

```text
Contracts assessed: 8
Assessment method: transparent rules baseline (not an AI model)
Human review required: yes; no procurement actions are executed
```

The generated management summary was checked programmatically:

```json
{
  "assessment_date": "2026-10-26",
  "synthetic_demo": true,
  "assessment_method": "transparent_rules_baseline",
  "contracts_assessed": 8,
  "distinct_suppliers": 8,
  "contracts_by_stage": {
    "active": 4,
    "evaluation": 1,
    "planning": 1,
    "renewal_review": 1,
    "tender": 1
  },
  "renewals_due_within_90_days": 2,
  "renewal_dates_passed": 1,
  "contracts_flagged_for_review": 4,
  "supplier_records_scored": 5,
  "human_review_required": 8,
  "actions_executed": 0,
  "synthetic_annual_value_total_eur": 158500.0
}
```

All values are produced from the eight fictional CSV rows. They are not actual supplier outcomes, performance claims, budgets, savings, or procurement recommendations. The 21-file ZIP archive was extracted and passed the same tests, compile check, and CLI run; its banner PNG is 1672×941. The repository was created on GitHub on 2026-11-01 and the workflow file is present at `.github/workflows/tests.yml`; its first remote Actions run has not yet been verified.
