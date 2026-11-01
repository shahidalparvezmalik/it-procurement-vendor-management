# Input and output data dictionary

All rows in `data/contracts.csv` are fabricated. Supplier names, contract identifiers, metrics, dates, and EUR values are illustrative only.

## Input fields

| Field | Meaning |
|---|---|
| `contract_id` | Unique fictional contract/record ID. |
| `supplier_name` | Fictional supplier label. |
| `category` | Synthetic procurement category. |
| `stage` | `planning`, `tender`, `evaluation`, `awarded`, `active`, `renewal_review`, or `closed`. |
| `annual_value_eur` | Fictional annual value, not an approved budget or quote. |
| `renewal_date` | ISO date (`YYYY-MM-DD`), or blank when not applicable. |
| `sla_target_pct` | Declared synthetic SLA target from 0 to 100. |
| `sla_actual_pct` | Synthetic actual SLA measure from 0 to 100. |
| `on_time_delivery_pct` | Synthetic on-time delivery rate from 0 to 100. |
| `quality_pass_pct` | Synthetic quality pass rate from 0 to 100. |
| `open_major_issues` | Non-negative integer count of fictional open major issues. |

Performance fields must be either all present or all blank. Active, renewal-review, and closed records require all four metrics. Pipeline stages may omit them and will be marked `not_scored`.

The loader rejects missing columns, empty input, duplicate contract IDs, invalid lifecycle stages, invalid numeric fields, out-of-range percentages, partial metric sets, and invalid renewal dates.

## Outputs

- `supplier_scorecards.csv` — one transparent score/status row per input record, including reasons and mandatory human-review/action flags.
- `contract_renewal_flags.csv` — rows with any date or performance review reasons.
- `management_summary.json` — stage counts, suppliers, renewal/review counts, and totals of synthetic annual values.
- `human_review_template.csv` — blank fields for a reviewer to complete separately.

Use only fictional records in this repository. Reports copy source input values and should not be treated as operational records.
