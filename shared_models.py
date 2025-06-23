from pydantic import BaseModel, Field
from enum import Enum

class CustomerTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class SupportTicket(BaseModel):
    ticket_id: str
    customer_tier: CustomerTier
    subject: str
    message: str
    previous_tickets: int
    monthly_revenue: float
    account_age_days: int

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    URGENT = "urgent" # For critically negative/urgent messages

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Department(str, Enum):
    TECHNICAL_SUPPORT = "Technical Support"
    BILLING = "Billing"
    FEATURE_REQUEST = "Feature Request"
    SALES = "Sales"
    SECURITY = "Security"
    GENERAL_INQUIRY = "General Inquiry"
    URGENT_RESPONSE_TEAM = "Urgent Response Team"

# Agent-specific output models (can also be in respective agent files if preferred)
class SentimentAnalysisOutput(BaseModel):
    sentiment: Sentiment
    reasoning: str = Field(description="Explanation for the determined sentiment.")

class PriorityAssignmentOutput(BaseModel):
    priority: Priority
    reasoning: str = Field(description="Explanation for the assigned priority.")

class RoutingOutput(BaseModel):
    routed_to_department: Department
    summary: str = Field(description="A brief summary of the ticket and recommended action.")
    reasoning: str = Field(description="Explanation for the routing decision.")

# Combined output model for the entire processing flow
class AgentOutput(BaseModel):
    sentiment: Sentiment
    priority: Priority
    routed_to_department: Department
    summary: str = Field(description="A brief summary of the ticket and recommended action.")
    reasoning: str = Field(description="Comprehensive explanation for the assigned sentiment, priority, and routing.")