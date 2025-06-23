import pytest
import json
from main import process_ticket
from shared_models import SupportTicket, Sentiment, Priority, Department
from evaluation.evaluator import Evaluator

EXPECTED_OUTPUTS = {
    "SUP-001": {"sentiment": Sentiment.URGENT, "priority": Priority.CRITICAL, "routed_to_department": Department.TECHNICAL_SUPPORT},
    "SUP-002": {"sentiment": Sentiment.NEUTRAL, "priority": Priority.LOW, "routed_to_department": Department.TECHNICAL_SUPPORT},
    "SUP-003": {"sentiment": Sentiment.POSITIVE, "priority": Priority.MEDIUM, "routed_to_department": Department.FEATURE_REQUEST},
    "SUP-004": {"sentiment": Sentiment.NEGATIVE, "priority": Priority.HIGH, "routed_to_department": Department.TECHNICAL_SUPPORT},
    "SUP-005": {"sentiment": Sentiment.URGENT, "priority": Priority.CRITICAL, "routed_to_department": Department.SECURITY}
}

@pytest.fixture(scope="module")
def test_tickets():
    data = [
        {
            "ticket_id": "SUP-001",
            "customer_tier": "free",
            "subject": "This product is completely broken!!!",
            "message": "Nothing works! I can't even log in. This is the worst software I've ever used. I'm leaving.",
            "previous_tickets": 0,
            "monthly_revenue": 0,
            "account_age_days": 2
        },
        {
            "ticket_id": "SUP-002",
            "customer_tier": "enterprise",
            "subject": "Minor UI issue with dashboard",
            "message": "Hi team, just noticed the dashboard numbers are slightly misaligned on mobile view.",
            "previous_tickets": 15,
            "monthly_revenue": 25000,
            "account_age_days": 730
        },
        {
            "ticket_id": "SUP-003",
            "customer_tier": "premium",
            "subject": "Feature Request: Bulk export",
            "message": "We need bulk export functionality for our quarterly reports. Currently exporting one by one is too slow.",
            "previous_tickets": 5,
            "monthly_revenue": 5000,
            "account_age_days": 400
        },
        {
            "ticket_id": "SUP-004",
            "customer_tier": "premium",
            "subject": "API rate limits unclear",
            "message": "Getting rate limited but documentation says we should have 1000 requests/hour. We are hitting limits much faster.",
            "previous_tickets": 8,
            "monthly_revenue": 3000,
            "account_age_days": 180
        },
        {
            "ticket_id": "SUP-005",
            "customer_tier": "enterprise",
            "subject": "Urgent: Security vulnerability?",
            "message": "Our security team flagged that your API responses include internal server paths in error messages, which is a potential information disclosure vulnerability.",
            "previous_tickets": 20,
            "monthly_revenue": 50000,
            "account_age_days": 900
        }
    ]
    return [SupportTicket(**d) for d in data]

@pytest.mark.parametrize("ticket_id", EXPECTED_OUTPUTS.keys())
def test_ticket_processing_accuracy(ticket_id, test_tickets):
    ticket = next(t for t in test_tickets if t.ticket_id == ticket_id)
    expected = EXPECTED_OUTPUTS[ticket_id]
    try:
        agent_output = process_ticket(ticket)
        assert agent_output.sentiment == expected["sentiment"], f"Sentiment mismatch for {ticket_id}"
        assert agent_output.priority == expected["priority"], f"Priority mismatch for {ticket_id}"
        assert agent_output.routed_to_department == expected["routed_to_department"], f"Routing mismatch for {ticket_id}"
    except Exception as e:
        pytest.fail(f"Error processing ticket {ticket_id}: {e}")

def test_full_evaluation_report(test_tickets):
    processed_results = {}

    print("\n--- Begin Full Evaluation ---")
    for ticket in test_tickets:
        try:
            agent_output = process_ticket(ticket)
            model_data = agent_output.model_dump()
            print(f" Processed {ticket.ticket_id}")
            processed_results[ticket.ticket_id] = model_data
        except Exception as e:
            print(f" Error processing {ticket.ticket_id}: {e}")
            processed_results[ticket.ticket_id] = {"error": str(e), "message": ticket.message}

    print(f"\n Total tickets processed: {len(processed_results)}")
    print(f" Tickets: {list(processed_results.keys())}")

    evaluator = Evaluator()
    evaluator.evaluate(processed_results, EXPECTED_OUTPUTS)

    with open("evaluation_report.json", "w") as f:
        json.dump(evaluator.detailed_results, f, indent=4)
    print("\n evaluation_report.json saved successfully.")
