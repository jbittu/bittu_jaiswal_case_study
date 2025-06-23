from agents.base_agent import BaseAgent
from shared_models import SupportTicket, Sentiment, Priority, PriorityAssignmentOutput

class PriorityAgent(BaseAgent):
    def assign_priority(self, ticket: SupportTicket, sentiment: Sentiment) -> PriorityAssignmentOutput:
        prompt = f"""
        Assign a priority level to the following customer support ticket.
        Consider the customer tier, previous tickets, monthly revenue, account age, and the determined sentiment.
        Possible priorities: {', '.join([p.value for p in Priority])}.

        Guidelines:
        - 'critical' for enterprise customers with urgent issues (sentiment 'urgent'), or high revenue impact when combined with negative/urgent sentiment.
        - 'high' for premium/enterprise customers with significant issues, or high previous tickets.
        - 'medium' for general issues, premium customers with minor issues.
        - 'low' for free tier customers, feature requests, or very minor issues.

        Ticket ID: {ticket.ticket_id}
        Customer Tier: {ticket.customer_tier.value}
        Subject: {ticket.subject}
        Message: {ticket.message}
        Previous Tickets: {ticket.previous_tickets}
        Monthly Revenue: ${ticket.monthly_revenue}
        Account Age (days): {ticket.account_age_days}
        Detected Sentiment: {sentiment.value}

        Provide your analysis in JSON format, including the priority and a brief reasoning.
        """
        return self._generate_content(prompt, PriorityAssignmentOutput)