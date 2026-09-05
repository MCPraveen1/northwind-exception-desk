from pipeline import process_exception


class TriageSession:
    def __init__(self):
        self.exceptions = []

    def process(
        self,
        report: str,
        shipment_value: float,
        customer_tier: str,
    ) -> dict:

        result = process_exception(
            report=report,
            shipment_value=shipment_value,
            customer_tier=customer_tier,
        )

        self.exceptions.append(result)

        return result

    def get_summary(self) -> dict:
        total_cases = len(self.exceptions)

        if total_cases == 0:
            return {
                "total_cases": 0,
                "total_compensation": 0,
                "escalation_rate": 0,
                "costliest_category": None,
            }

        total_compensation = sum(
            result["compensation"]["compensation"]
            for result in self.exceptions
        )

        escalated_cases = sum(
            1
            for result in self.exceptions
            if result["should_escalate"]
        )

        escalation_rate = (
            escalated_cases / total_cases
        ) * 100

        category_totals = {}

        for result in self.exceptions:
            category = result["category"]
            amount = result["compensation"]["compensation"]

            category_totals[category] = (
                category_totals.get(category, 0) + amount
            )

        costliest_category = max(
            category_totals,
            key=category_totals.get,
        )

        return {
            "total_cases": total_cases,
            "total_compensation": total_compensation,
            "escalation_rate": escalation_rate,
            "costliest_category": costliest_category,
        }