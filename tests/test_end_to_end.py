import pytest
from pathlib import Path
from main import process_ticket
from shared_models import SupportTicket, Sentiment, Priority, Department, CustomerTier
from evaluation.evaluator import Evaluator # To use the evaluator for reporting
import json

# Define your ground truth expected outputs
EXPECTED_OUTPUTS = {
    "SUP-001": {"sentiment": Sentiment.URGENT, "priority": Priority.CRITICAL, "routed_to_department": Department.TECHNICAL_SUPPORT},
    "SUP-002": {"sentiment": Sentiment.NEUTRAL, "priority": Priority.LOW, "routed_to_department": Department.TECHNICAL_SUPPORT},
    "SUP-003": {"sentiment": Sentiment.POSITIVE, "priority": Priority.MEDIUM, "routed_to_department": Department.FEATURE_REQUEST},
    "SUP-004": {"sentiment": Sentiment.NEGATIVE, "priority": Priority.HIGH, "routed_to_department": Department.TECHNICAL_SUPPORT},
    "SUP-005": {"sentiment": Sentiment.URGENT, "priority": Priority.CRITICAL, "routed_to_department": Department.SECURITY}
}

@pytest.fixture(scope="module")
def test_tickets():
    """Provides a list of SupportTicket objects for testing."""
    test_data = [
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
    return [SupportTicket(**data) for data in test_data]


@pytest.mark.parametrize("ticket_id", EXPECTED_OUTPUTS.keys())
def test_ticket_processing_accuracy(ticket_id, test_tickets):
    """
    Tests the end-to-end processing of a single ticket against expected outputs.
    """
    ticket = next(t for t in test_tickets if t.ticket_id == ticket_id)
    expected = EXPECTED_OUTPUTS[ticket_id]

    print(f"\nTesting Ticket: {ticket.ticket_id}")
    try:
        agent_output = process_ticket(ticket)
        print(f"  Agent Sentiment: {agent_output.sentiment.value}, Expected: {expected['sentiment'].value}")
        print(f"  Agent Priority: {agent_output.priority.value}, Expected: {expected['priority'].value}")
        print(f"  Agent Department: {agent_output.routed_to_department.value}, Expected: {expected['routed_to_department'].value}")

        assert agent_output.sentiment == expected["sentiment"], f"Sentiment mismatch for {ticket_id}. Got {agent_output.sentiment.value}, expected {expected['sentiment'].value}"
        assert agent_output.priority == expected["priority"], f"Priority mismatch for {ticket_id}. Got {agent_output.priority.value}, expected {expected['priority'].value}"
        assert agent_output.routed_to_department == expected["routed_to_department"], f"Routing mismatch for {ticket_id}. Got {agent_output.routed_to_department.value}, expected {expected['routed_to_department'].value}"

    except Exception as e:
        pytest.fail(f"Error processing ticket {ticket_id}: {e}")

# This part can be used to generate a full evaluation report after all tests run
# You can uncomment and adapt if you want a separate report besides pytest's own output.
def test_full_evaluation_report(test_tickets):
    """
    Runs all test cases and generates a combined evaluation report.
    This test serves as an aggregation step and doesn't perform assertions itself.
    """
    processed_results = {}
    for ticket in test_tickets:
        try:
            agent_output = process_ticket(ticket)
            processed_results[ticket.ticket_id] = agent_output.model_dump()
        except Exception as e:
            processed_results[ticket.ticket_id] = {"error": str(e), "message": ticket.message}
            print(f"Error processing ticket {ticket.ticket_id} for evaluation: {e}")

    evaluator = Evaluator()
    evaluator.evaluate(processed_results, EXPECTED_OUTPUTS)

    # Optional: Save the detailed results from the evaluator if desired
    with open("evaluation_report.json", "w") as f:
        json.dump(evaluator.detailed_results, f, indent=4)