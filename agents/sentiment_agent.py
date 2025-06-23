from .base_agent import BaseAgent
from shared_models import SupportTicket, SentimentAnalysisOutput

class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def run(self, ticket: SupportTicket) -> SentimentAnalysisOutput:
        return self.analyze_sentiment(ticket)

    def analyze_sentiment(self, ticket: SupportTicket) -> SentimentAnalysisOutput:
        prompt = f"""
Analyze the sentiment of the following support ticket and provide a concise reasoning.
The sentiment must be exactly one of: "positive", "neutral", "negative", "urgent".

Definitions (in order of precedence):
- "urgent": ONLY IF the ticket describes a critical issue requiring immediate attention (e.g., complete outage, inability to log in, security vulnerability, major data loss, or business interruption). This takes precedence over all other categories.
- "negative": Only if the customer expresses dissatisfaction, frustration, disappointment, or complains emotionally about a non-critical issue.
- "positive": The customer expresses satisfaction, gratitude, compliments, or provides constructive feedback and feature suggestions that indicate engagement.
  **Any feature request, even if written in a neutral or factual tone, should be classified as "positive".**
  Example: "We need bulk export functionality for our quarterly reports. Currently exporting one by one is too slow." → "positive"
- "neutral": For minor, factual bug reports or observations with no emotional language, even if a problem is reported, and it is NOT a feature request.

Use only the above values. Do not invent new categories or synonyms.

Ticket Data:
- Ticket ID: {ticket.ticket_id}
- Customer Tier: {ticket.customer_tier.value}
- Subject: {ticket.subject}
- Message: {ticket.message}
- Previous Tickets: {ticket.previous_tickets}
- Monthly Revenue: ${ticket.monthly_revenue:.2f}
- Account Age: {ticket.account_age_days} days

Respond ONLY in this JSON format, strictly matching the SentimentAnalysisOutput schema:
{{
  "sentiment": "sentiment_value",
  "reasoning": "Your detailed reasoning here."
}}
"""
        return self._generate_content(prompt, SentimentAnalysisOutput)
