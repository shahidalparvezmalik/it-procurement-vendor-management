"""Transparent, deterministic review flags for synthetic contract records."""

from __future__ import annotations

from datetime import date, datetime
from typing import Mapping

STAGES = {"planning", "tender", "evaluation", "awarded", "active", "renewal_review", "closed"}
METRIC_FIELDS = ("sla_target_pct", "sla_actual_pct", "on_time_delivery_pct", "quality_pass_pct")


def _number(value: object, field: str, *, minimum: float = 0, maximum: float | None = None) -> float:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a number") from exc
    if number < minimum or (maximum is not None and number > maximum):
        bounds = f"at least {minimum}" + (f" and at most {maximum}" if maximum is not None else "")
        raise ValueError(f"{field} must be {bounds}")
    return number


def assess_contract(record: Mapping[str, str], as_of: date) -> dict[str, object]:
    """Assess one synthetic contract; suggestions always require human review."""
    contract_id = str(record.get("contract_id", "")).strip()
    supplier = str(record.get("supplier_name", "")).strip()
    category = str(record.get("category", "")).strip()
    stage = str(record.get("stage", "")).strip().lower()
    if not contract_id or not supplier or not category:
        raise ValueError("contract_id, supplier_name, and category are required")
    if stage not in STAGES:
        raise ValueError(f"stage must be one of: {', '.join(sorted(STAGES))}")

    annual_value = _number(record.get("annual_value_eur", ""), "annual_value_eur")
    try:
        major_issues = int(str(record.get("open_major_issues", "")).strip())
        if major_issues < 0:
            raise ValueError
    except ValueError as exc:
        raise ValueError("open_major_issues must be a non-negative integer") from exc

    renewal_raw = str(record.get("renewal_date", "")).strip()
    try:
        renewal = date.fromisoformat(renewal_raw) if renewal_raw else None
    except ValueError as exc:
        raise ValueError("renewal_date must be YYYY-MM-DD or blank") from exc
    days_to_renewal = (renewal - as_of).days if renewal else None

    present = [str(record.get(field, "")).strip() != "" for field in METRIC_FIELDS]
    if any(present) and not all(present):
        raise ValueError("performance metrics must be all supplied or all blank")
    if stage in {"active", "renewal_review", "closed"} and not all(present):
        raise ValueError(f"performance metrics are required for stage {stage}")

    reasons: list[str] = []
    if renewal and days_to_renewal is not None:
        if days_to_renewal < 0:
            reasons.append("renewal date has passed; verify contract status")
        elif days_to_renewal <= 90:
            reasons.append("renewal is within 90 days; begin human review")

    if all(present):
        metrics = {
            field: _number(record[field], field, maximum=100)
            for field in METRIC_FIELDS
        }
        score = round(
            0.40 * metrics["sla_actual_pct"]
            + 0.35 * _number(record["on_time_delivery_pct"], "on_time_delivery_pct", maximum=100)
            + 0.25 * _number(record["quality_pass_pct"], "quality_pass_pct", maximum=100),
            1,
        )
        sla_missed = metrics["sla_actual_pct"] < metrics["sla_target_pct"]
        if sla_missed:
            reasons.append("reported SLA is below the stated target")
        if score < 80:
            reasons.append("illustrative performance score is below 80")
        if major_issues >= 3:
            reasons.append("three or more open major issues; review evidence")
        performance_status = "review" if sla_missed or score < 80 or major_issues >= 3 else (
            "watch" if score < 92 or major_issues > 0 else "on_track"
        )
    else:
        score = None
        sla_missed = None
        performance_status = "not_scored"

    return {
        "contract_id": contract_id,
        "supplier_name": supplier,
        "category": category,
        "stage": stage,
        "annual_value_eur": round(annual_value, 2),
        "renewal_date": renewal.isoformat() if renewal else "",
        "days_to_renewal": days_to_renewal if days_to_renewal is not None else "",
        "sla_target_pct": record.get("sla_target_pct", ""),
        "sla_actual_pct": record.get("sla_actual_pct", ""),
        "on_time_delivery_pct": record.get("on_time_delivery_pct", ""),
        "quality_pass_pct": record.get("quality_pass_pct", ""),
        "open_major_issues": major_issues,
        "performance_score": score if score is not None else "",
        "performance_status": performance_status,
        "sla_below_target": sla_missed if sla_missed is not None else "",
        "review_reasons": reasons,
        "human_review_required": True,
        "action_executed": False,
    }
