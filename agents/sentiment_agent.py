from agents.base_agent import BaseAgent
from shared_models import SupportTicket, Sentiment, SentimentAnalysisOutput

class SentimentAgent(BaseAgent):
    def analyze_sentiment(self, ticket: SupportTicket) -> SentimentAnalysisOutput:
        prompt = f"""
        Analyze the sentiment of the following customer support ticket.
        Consider the subject and message content.
        Possible sentiments: {', '.join([s.value for s in Sentiment])}.
        If the message implies immediate action is needed due to severity or critical issue, classify as 'urgent'.

        Ticket ID: {ticket.ticket_id}
        Subject: {ticket.subject}
        Message: {ticket.message}

        Provide your analysis in JSON format, including the sentiment and a brief reasoning.
        """
        return self._generate_content(prompt, SentimentAnalysisOutput)