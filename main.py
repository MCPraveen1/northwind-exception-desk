from session import TriageSession


session = TriageSession()


tests = [
    {
        "report": "My package is 3 days late and still hasn't arrived.",
        "shipment_value": 1000,
        "customer_tier": "standard",
    },
    {
        "report": "The package arrived with a cracked screen.",
        "shipment_value": 1000,
        "customer_tier": "standard",
    },
    {
        "report": "The shipment was lost in transit.",
        "shipment_value": 5000,
        "customer_tier": "standard",
    },
]


for test in tests:
    result = session.process(**test)

    print("=" * 60)
    print("Category:", result["category"])
    print("Compensation:", result["compensation"]["compensation"])
    print("Outcome:", result["outcome"])


print("=" * 60)
print("DAILY SUMMARY")
print(session.get_summary())