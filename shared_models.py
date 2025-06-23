from pydantic import BaseModel, Field
from enum import Enum



class Sentiment(Enum):
    """Represents the sentiment of a support ticket."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    URGENT = "urgent"

class Priority(Enum):
    """Represents the priority level of a support ticket."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class Department(Enum):
    """Represents the department a ticket can be routed to."""
    TECHNICAL = "Technical"
    BILLING = "Billing"
    SALES = "Sales"
    CUSTOMER_SUPPORT = "Customer_Support"
    ACCOUNT_MANAGEMENT = "Account_Management"
    SECURITY = "Security"
    TECHNICAL_SUPPORT = "Technical_Support"
    FEATURE_REQUEST = "Feature_Request" 

class CustomerTier(Enum):
    """Represents the customer's service tier."""
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class SupportTicket(BaseModel):
    """Represents the structure of an incoming customer support ticket."""
    ticket_id: str
    customer_tier: CustomerTier
    subject: str
    message: str
    previous_tickets: int
    monthly_revenue: float
    account_age_days: int


class SentimentAnalysisOutput(BaseModel):
    """Output structure for the Sentiment Agent."""
    sentiment: Sentiment
    reasoning: str = Field(description="Detailed reasoning for the sentiment analysis.")

class PriorityAssignmentOutput(BaseModel):
    """Output structure for the Priority Agent."""
    priority: Priority
    reasoning: str = Field(description="Detailed reasoning for the priority assignment.")

class TicketRoutingOutput(BaseModel):
    """Output structure for the Router Agent."""
    routed_to_department: Department
    summary: str = Field(description="A brief summary of the ticket for the receiving department.")
    reasoning: str = Field(description="Detailed reasoning for the routing decision.")


class AgentOutput(BaseModel):
    """Combines the outputs from all agents into a single comprehensive result."""
    sentiment: Sentiment
    priority: Priority
    routed_to_department: Department
    summary: str
    reasoning: str