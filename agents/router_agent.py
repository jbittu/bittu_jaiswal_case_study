from .base_agent import BaseAgent
from shared_models import SupportTicket, Sentiment, Priority, TicketRoutingOutput

class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def run(self, ticket: SupportTicket, sentiment: Sentiment, priority: Priority) -> TicketRoutingOutput:
        return self.route_ticket(ticket, sentiment, priority)

    def route_ticket(self, ticket: SupportTicket, sentiment: Sentiment, priority: Priority) -> TicketRoutingOutput:
        prompt = f"""
Route the following support ticket to the most appropriate department.
Choose ONLY from: "Technical", "Billing", "Sales", "Customer_Support", "Account_Management", "Security", "Technical_Support", "Feature_Request".

Guidelines:
- "Technical_Support": For technical issues, bugs, API errors, outages, or anything requiring engineering intervention.
- "Technical": For general technical queries (if not a support issue).
- "Billing": Invoices, payments, subscriptions, refunds.
- "Sales": New features, upgrades, demos, pre-sales.
- "Customer_Support": How-to, account updates (non-billing), minor issues.
- "Account_Management": Enterprise/high-revenue customer relationship management.
- "Security": Security vulnerabilities, breaches, or suspicious activity.
- "Feature_Request": Explicit feature requests.

Ticket Data:
- Ticket ID: {ticket.ticket_id}
- Customer Tier: {ticket.customer_tier.value}
- Subject: {ticket.subject}
- Message: {ticket.message}
- Previous Tickets: {ticket.previous_tickets}
- Monthly Revenue: ${ticket.monthly_revenue:.2f}
- Account Age: {ticket.account_age_days} days
- Sentiment: {sentiment.value}
- Priority: {priority.value}

Respond ONLY in this JSON format, strictly matching the TicketRoutingOutput schema:
{{
  "routed_to_department": "department_name",
  "summary": "A brief summary of the ticket and why it was routed this way.",
  "reasoning": "Detailed reasoning for the routing decision."
}}
"""
        return self._generate_content(prompt, TicketRoutingOutput)
