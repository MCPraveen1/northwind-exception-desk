from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm import model


# ---------------------------------------------------------
# Classification chain
# ---------------------------------------------------------

classify_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You classify shipment exception reports.

Classify the report into exactly ONE of these categories:
- delayed
- damaged
- lost
- unknown

Return ONLY the category name.
If the report is unclear, garbled, or does not clearly describe
a delayed, damaged, or lost shipment, return unknown.""",
        ),
        (
            "human",
            "{report}",
        ),
    ]
)

classify_chain = classify_prompt | model | StrOutputParser()

# ---------------------------------------------------------
# Escalation chain
# ---------------------------------------------------------

escalate_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a logistics operations manager assistant.

Draft a concise internal escalation note for a manager.
Include:
- Exception category
- Shipment value
- Compensation amount
- Customer tier
- Why the case requires human review

Do not address the customer directly.""",
        ),
        (
            "human",
            """Category: {category}
Shipment value: ${shipment_value}
Compensation: ${compensation}
Customer tier: {customer_tier}
Report: {report}""",
        ),
    ]
)

escalate_chain = escalate_prompt | model | StrOutputParser()


# ---------------------------------------------------------
# Customer email chain
# ---------------------------------------------------------

draft_email_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a customer service assistant for a logistics company.

Draft a concise, professional customer-facing email about a shipment
exception that has been automatically resolved.

Mention:
- What happened
- The compensation amount
- That the case has been resolved

Do not mention internal escalation rules or internal processes.""",
        ),
        (
            "human",
            """Category: {category}
Shipment value: ${shipment_value}
Compensation: ${compensation}
Customer tier: {customer_tier}
Report: {report}""",
        ),
    ]
)

draft_email_chain = draft_email_prompt | model | StrOutputParser()