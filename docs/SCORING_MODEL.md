# Scoring model and review rules

This demo calculates an illustrative score only when all four performance fields are present:

```text
0.40 × SLA actual % + 0.35 × on-time delivery % + 0.25 × quality pass %
```

The result is rounded to one decimal place. The stated SLA target is evaluated separately; a strong blended score does not hide a missed target.

## Performance status

- **review:** SLA actual is below target, score is below 80, or at least three major issues are open.
- **watch:** score is below 92 or one or more major issues are open, unless a review condition applies.
- **on_track:** none of those conditions is triggered.
- **not_scored:** a pipeline record has no performance metrics.

## Renewal flags

- A date already passed prompts the user to verify the contract's actual status.
- A date from the assessment day through 90 days prompts a human renewal review.
- These calendar flags do not recommend renewing, terminating, or contacting a supplier.

All rows require human review. The program reports the score and reasons separately and always sets `action_executed` to false. The score is not statistically calibrated, an SLA policy, an award ranking, or a financial valuation. Validate definitions, thresholds, data quality, and evaluation cases with the relevant procurement, finance, legal, and service owners before considering any real use.
