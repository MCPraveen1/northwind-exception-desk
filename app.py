import gradio as gr

from session import TriageSession


session = TriageSession()


def process_report(report, shipment_value, customer_tier):
    result = session.process(
        report=report,
        shipment_value=float(shipment_value),
        customer_tier=customer_tier,
    )

    compensation = result["compensation"]["compensation"]

    steps = [
        f"1. Classified as: {result['category']}",
        f"2. Compensation calculated: ${compensation:.2f}",
        f"3. Escalation decision: "
        f"{'Escalate' if result['should_escalate'] else 'Auto-resolve'}",
        f"4. Outcome: {result['outcome']}",
    ]

    log = "\n".join(
        [
            f"Case {len(session.exceptions)}",
            f"Category: {result['category']}",
            f"Compensation: ${compensation:.2f}",
            f"Outcome: {result['outcome']}",
            "-" * 40,
        ]
    )

    return (
        result["outcome"],
        "\n".join(steps),
        result["message"],
        build_log(),
    )


def build_log():
    if not session.exceptions:
        return "No exceptions processed yet."

    entries = []

    for index, result in enumerate(session.exceptions, start=1):
        compensation = result["compensation"]["compensation"]

        entries.append(
            f"Case {index}\n"
            f"Category: {result['category']}\n"
            f"Compensation: ${compensation:.2f}\n"
            f"Outcome: {result['outcome']}\n"
            f"Escalated: "
            f"{'Yes' if result['should_escalate'] else 'No'}\n"
            + "-" * 40
        )

    return "\n".join(entries)


def get_summary():
    summary = session.get_summary()

    if summary["total_cases"] == 0:
        return "No exceptions have been processed yet."

    return (
        f"Daily Triage Summary\n\n"
        f"Total cases: {summary['total_cases']}\n"
        f"Total compensation: "
        f"${summary['total_compensation']:.2f}\n"
        f"Escalation rate: "
        f"{summary['escalation_rate']:.2f}%\n"
        f"Costliest category: "
        f"{summary['costliest_category']}"
    )


with gr.Blocks(title="Northwind Shipment Exception Desk") as app:

    gr.Markdown(
        """
        # Northwind Logistics
        ## Shipment Exception Desk

        Submit a shipment exception for automated triage.
        """
    )

    with gr.Row():

        with gr.Column():

            report = gr.Textbox(
                label="Exception Report",
                placeholder="Describe what happened to the shipment...",
                lines=5,
            )

            shipment_value = gr.Number(
                label="Shipment Value ($)",
                value=1000,
                minimum=0,
            )

            customer_tier = gr.Dropdown(
                choices=["standard", "premium"],
                value="standard",
                label="Customer Tier",
            )

            submit_button = gr.Button(
                "Process Exception",
                variant="primary",
            )

        with gr.Column():

            outcome = gr.Textbox(
                label="Outcome",
            )

            steps = gr.Textbox(
                label="Processing Steps",
                lines=6,
            )

            message = gr.Textbox(
                label="Generated Message",
                lines=12,
            )

    gr.Markdown("## Daily Triage Log")

    daily_log = gr.Textbox(
        label="Processed Exceptions",
        lines=12,
        interactive=False,
    )

    gr.Markdown("## Daily Summary")

    summary_button = gr.Button("Get Daily Summary")

    summary = gr.Textbox(
        label="Summary",
        lines=6,
        interactive=False,
    )

    submit_button.click(
        fn=process_report,
        inputs=[
            report,
            shipment_value,
            customer_tier,
        ],
        outputs=[
            outcome,
            steps,
            message,
            daily_log,
        ],
    )

    summary_button.click(
        fn=get_summary,
        inputs=[],
        outputs=summary,
    )


if __name__ == "__main__":
    app.launch(share=True)