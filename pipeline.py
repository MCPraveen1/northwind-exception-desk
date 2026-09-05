import re

from chains import (
    classify_chain,
    escalate_chain,
    draft_email_chain,
)

from tools import (
    calculate_delay_compensation,
    calculate_damage_compensation,
    calculate_lost_compensation,
)


STANDARD_ESCALATION_THRESHOLD = 500
PREMIUM_ESCALATION_THRESHOLD = 250


def extract_days_late(report: str) -> int:
    """Extract the number of days a shipment was delayed."""

    patterns = [
        r"(\d+)\s+days?\s+late",
        r"late\s+by\s+(\d+)\s+days?",
    ]

    for pattern in patterns:
        match = re.search(pattern, report.lower())

        if match:
            return int(match.group(1))

    return 0


def process_exception(
    report: str,
    shipment_value: float,
    customer_tier: str,
) -> dict:

    # 1. Classify
    category = classify_chain.invoke(
        {"report": report}
    ).strip().lower()

    # 2. Calculate compensation
    if category == "delayed":

        days_late = extract_days_late(report)

        compensation = calculate_delay_compensation(
            shipment_value,
            days_late,
        )

    elif category == "damaged":

        compensation = calculate_damage_compensation(
            shipment_value,
        )

    elif category == "lost":

        compensation = calculate_lost_compensation(
            shipment_value,
        )

    else:

        category = "unknown"

        compensation = {
            "category": "unknown",
            "shipment_value": shipment_value,
            "compensation": 0,
            "reason": "Unable to classify the exception.",
        }

    compensation_amount = compensation["compensation"]

    # 3. Decide escalation
    customer_tier = customer_tier.strip().lower()

    if category == "unknown":
        should_escalate = True
        escalation_reason = "Exception could not be classified."

    else:
        threshold = (
            PREMIUM_ESCALATION_THRESHOLD
            if customer_tier == "premium"
            else STANDARD_ESCALATION_THRESHOLD
        )

        should_escalate = compensation_amount > threshold

        if should_escalate:
            escalation_reason = (
                f"Compensation of ${compensation_amount:.2f} "
                f"exceeds the ${threshold} threshold."
            )
        else:
            escalation_reason = (
                f"Compensation of ${compensation_amount:.2f} "
                f"is within the ${threshold} threshold."
            )

    # 4. Draft the appropriate message
    if should_escalate:

        message = escalate_chain.invoke(
            {
                "category": category,
                "shipment_value": shipment_value,
                "compensation": compensation_amount,
                "customer_tier": customer_tier,
                "report": report,
            }
        ).strip()

        outcome = "escalated"

    else:

        message = draft_email_chain.invoke(
            {
                "category": category,
                "shipment_value": shipment_value,
                "compensation": compensation_amount,
                "customer_tier": customer_tier,
                "report": report,
            }
        ).strip()

        outcome = "auto-resolved"

    return {
        "report": report,
        "category": category,
        "customer_tier": customer_tier,
        "compensation": compensation,
        "should_escalate": should_escalate,
        "escalation_reason": escalation_reason,
        "outcome": outcome,
        "message": message,
    }