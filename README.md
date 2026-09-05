# Northwind Logistics — Shipment Exception Desk

An AI-powered shipment exception triage system built with **Python, LangChain, Groq, and Gradio**.

The application classifies shipment exception reports, calculates compensation using deterministic business rules, decides whether a case can be automatically resolved or requires human review, and generates the appropriate message.

## Demo

The application provides a Gradio interface for submitting shipment exceptions and viewing:

- Classification
- Compensation calculation
- Escalation decision
- Generated customer or internal message
- Daily triage log
- Daily summary

## Architecture

```text
Shipment Exception Report
          |
          v
   LLM Classification
          |
          v
  Compensation Calculator
          |
          v
   Escalation Decision
       /        \
      /          \
Auto-resolve    Escalate
    |              |
    v              v
Customer Email   Internal Note
          \        /
           \      /
            v    v
        Triage Session
              |
              v
       Daily Summary