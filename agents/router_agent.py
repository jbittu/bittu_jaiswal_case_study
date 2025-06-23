from agents.base_agent import BaseAgent
from shared_models import SupportTicket, Sentiment, Priority, Department, RoutingOutput

class RouterAgent(BaseAgent):
    def route_ticket(self, ticket: SupportTicket, sentiment: Sentiment, priority: Priority) -> RoutingOutput:
        department_list = ', '.join([d.value for d in Department])
        prompt = f"""
        Route the following customer support ticket to the most appropriate department.
        Consider the subject, message content, assigned sentiment, and priority.
        Possible departments: {department_list}.

        Guidelines:
        - 'Technical Support': API errors, software bugs, login issues, technical queries.
        - 'Billing': Questions about invoices, payments, subscriptions.
        - 'Feature Request': Suggestions for new features or enhancements.
        - 'Sales': Inquiries about new products, upgrades, or partnerships.
        - 'Security': Reported vulnerabilities, suspicious activity (especially if sentiment is 'urgent').
        - 'Urgent Response Team': For 'critical' priority tickets, especially involving security or major outages impacting enterprise clients. Route critical security issues here.
        - 'General Inquiry': For anything that doesn't fit the above categories.

        Ticket ID: {ticket.ticket_id}
        Customer Tier: {ticket.customer_tier.value}
        Subject: {ticket.subject}
        Message: {ticket.message}
        Detected Sentiment: {sentiment.value}
        Assigned Priority: {priority.value}

        Provide your routing decision in JSON format, including the department, a brief summary of the ticket and recommended action, and the reasoning for the routing decision.
        """
        return self._generate_content(prompt, RoutingOutput)