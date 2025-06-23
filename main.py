from shared_models import SupportTicket, AgentOutput, Sentiment, Priority, Department, CustomerTier
from agents.sentiment_agent import SentimentAgent
from agents.priority_agent import PriorityAgent
from agents.router_agent import RouterAgent
import json

def process_ticket(ticket: SupportTicket) -> AgentOutput:
    """Orchestrates the agents to process a single support ticket."""
    sentiment_agent = SentimentAgent()
    priority_agent = PriorityAgent()
    router_agent = RouterAgent()

    # 1. Sentiment Analysis
    # Call the run method of the SentimentAgent
    sentiment_output = sentiment_agent.run(ticket)

    # 2. Priority Assignment
    # Call the run method of the PriorityAgent
    priority_output = priority_agent.run(ticket, sentiment_output.sentiment)

    # 3. Ticket Routing
    # Call the run method of the RouterAgent
    routing_output = router_agent.run(ticket, sentiment_output.sentiment, priority_output.priority)

    # Combine results into a single AgentOutput
    return AgentOutput(
        sentiment=sentiment_output.sentiment,
        priority=priority_output.priority,
        routed_to_department=routing_output.routed_to_department,
        summary=routing_output.summary,
        reasoning=f"Sentiment Reason: {sentiment_output.reasoning}\nPriority Reason: {priority_output.reasoning}\nRouting Reason: {routing_output.reasoning}"
    )

