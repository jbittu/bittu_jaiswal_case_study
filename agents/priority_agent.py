from .base_agent import BaseAgent
from shared_models import SupportTicket, Sentiment, PriorityAssignmentOutput

class PriorityAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def run(self, ticket: SupportTicket, sentiment: Sentiment) -> PriorityAssignmentOutput:
        return self.assign_priority(ticket, sentiment)

    def assign_priority(self, ticket: SupportTicket, sentiment: Sentiment) -> PriorityAssignmentOutput:
        prompt = f"""
Assign a priority to the following support ticket using ONLY one of these values: "low", "medium", "high", "urgent", "critical".

Guidelines:
- "critical": Assign for any complete service outage, inability to log in, security vulnerability, or major data loss, regardless of customer tier or revenue.
- "urgent": Immediate attention needed, but not at the highest severity.
- "high": Significant but not urgent or critical.
- "medium": Moderate importance.
- "low": Minor, routine, or feature requests for free tier users.

Ticket Data:
- Ticket ID: {ticket.ticket_id}
- Customer Tier: {ticket.customer_tier.value}
- Subject: {ticket.subject}
- Message: {ticket.message}
- Previous Tickets: {ticket.previous_tickets}
- Monthly Revenue: ${ticket.monthly_revenue:.2f}
- Account Age: {ticket.account_age_days} days
- Determined Sentiment: {sentiment.value}

Respond ONLY in this JSON format, strictly matching the PriorityAssignmentOutput schema:
{{
  "priority": "priority_value",
  "reasoning": "Your detailed reasoning here."
}}
"""
        return self._generate_content(prompt, PriorityAssignmentOutput)
