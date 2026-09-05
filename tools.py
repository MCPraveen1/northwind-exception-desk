def calculate_delay_compensation(
    shipment_value: float,
    days_late: int
) -> dict:
    """
    Calculate compensation for a delayed shipment.

    Policy:
    - $25 per day late
    - Maximum compensation is 25% of shipment value
    """

    base_compensation = days_late * 25
    maximum_compensation = shipment_value * 0.25

    compensation = min(base_compensation, maximum_compensation)

    return {
        "category": "delayed",
        "shipment_value": shipment_value,
        "days_late": days_late,
        "compensation": round(compensation, 2),
        "reason": f"${25} per day for {days_late} day(s) late",
    }
def calculate_damage_compensation(shipment_value: float) -> dict:
    """
    Calculate compensation for a damaged shipment.

    Policy:
    - Compensation is 30% of shipment value
    - Maximum compensation is $1,000
    """

    base_compensation = shipment_value * 0.30
    maximum_compensation = 1000

    compensation = min(base_compensation, maximum_compensation)

    return {
        "category": "damaged",
        "shipment_value": shipment_value,
        "compensation": round(compensation, 2),
        "reason": "30% of shipment value",
    }
def calculate_lost_compensation(shipment_value: float) -> dict:
    """
    Calculate compensation for a lost shipment.

    Policy:
    - Compensation is 100% of shipment value
    - Maximum compensation is $2,000
    """

    base_compensation = shipment_value
    maximum_compensation = 2000

    compensation = min(base_compensation, maximum_compensation)

    return {
        "category": "lost",
        "shipment_value": shipment_value,
        "compensation": round(compensation, 2),
        "reason": "100% of shipment value",
    }

