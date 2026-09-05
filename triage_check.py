from pipeline import process_exception


TEST_CASES = [
    {
        "name": "Mild delay",
        "report": "My package is 2 days late.",
        "shipment_value": 1000,
        "customer_tier": "standard",
        "expected_outcome": "auto-resolved",
    },
    {
        "name": "High-value loss",
        "report": "The shipment was lost in transit.",
        "shipment_value": 5000,
        "customer_tier": "standard",
        "expected_outcome": "escalated",
    },
    {
        "name": "Minor damage",
        "report": "The package arrived with a cracked screen.",
        "shipment_value": 500,
        "customer_tier": "standard",
        "expected_outcome": "auto-resolved",
    },
    {
        "name": "Garbled report",
        "report": "asdf qwerty 12345",
        "shipment_value": 100,
        "customer_tier": "standard",
        "expected_outcome": "escalated",
    },
]


def run_checks():
    passed = 0

    for test in TEST_CASES:
        result = process_exception(
            report=test["report"],
            shipment_value=test["shipment_value"],
            customer_tier=test["customer_tier"],
        )

        actual = result["outcome"]
        expected = test["expected_outcome"]

        if actual == expected:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"

        print(
            f"{status}: {test['name']} "
            f"(expected={expected}, actual={actual})"
        )

    print()
    print(f"{passed}/{len(TEST_CASES)} checks passed")

    return passed == len(TEST_CASES)


if __name__ == "__main__":
    success = run_checks()

    if not success:
        raise SystemExit(1)