# Proposed operating model

This document describes review points for the portfolio demo. It is not an approved procurement policy.

## Roles

| Role | Example responsibility |
|---|---|
| Procurement / vendor manager | Maintain approved sourcing records, assess supplier evidence, and coordinate contract reviews. |
| Service owner | Define service requirements, criticality, and operational impact. |
| Finance | Validate commercial data and delegated budget authority. |
| Legal / contract owner | Confirm contract terms, notice periods, renewal clauses, and obligations. |
| Security / data protection | Review supplier access, data handling, security evidence, and required controls. |
| Approver | Make renewal, sourcing, or payment decisions under organizational authority. |

## Demo workflow

1. Load a fictional CSV of contract stage, metrics, and renewal date.
2. Validate record structure, numeric ranges, dates, and unique IDs.
3. Calculate a transparent weighted score where synthetic performance fields exist.
4. Flag dates and performance conditions that warrant review.
5. Generate scorecards, a management summary, and an empty review template.
6. A human reviews the source data and makes any decision outside the program.

## Controls and limits

- The repository contains synthetic records only. Do not add real contracts, vendor names, prices, performance records, or personal data.
- The demo does not read a contract, contact suppliers, rank bids, approve purchases, renew/terminate contracts, or submit payments.
- A reported metric must be confirmed against an approved source before any real decision.
- Renewal deadlines, service criticality, security and legal obligations require the appropriate owner; a score cannot replace that judgment.
- Every score and flag remains a human-review prompt. The output template does not imply that a review took place.

Before operational use, define authorized data sources, privacy and retention rules, procurement controls, score validation, approval routes, audit requirements, and escalation for incomplete or conflicting evidence. No operational benefits or supplier outcomes are claimed by this demonstration.
