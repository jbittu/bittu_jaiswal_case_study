# Multi-Agent System Architecture: Customer Support Ticket Analyzer

## 1. System Overview

This system is designed to automate the analysis and routing of customer support tickets using a pipeline of specialized AI agents. The primary goal is to efficiently direct tickets to the correct department with an appropriate priority, improving response times and customer satisfaction.

## 2. Agent Breakdown and Roles

The system comprises three distinct agents, each with a specific role and perspective:

### 2.1. Sentiment Agent
* **Role:** To determine the emotional tone and urgency of the customer's message.
* **Perspective:** Focuses primarily on linguistic cues, keywords, and overall sentiment expressed in the `subject` and `message`, but also considers other ticket data (like the customer's tier or account age) to infer the overall urgency or criticality implied.
* **Input:** The full `SupportTicket` object.
* **Output:** `SentimentAnalysisOutput` (containing `sentiment` - e.g., positive, neutral, negative, urgent - and `reasoning`).
* **Rationale:** Separating sentiment analysis allows for a highly specialized agent capable of nuanced emotional detection, which is critical for understanding the customer's state and the immediate impact of their issue.

### 2.2. Priority Agent
* **Role:** To assess the business impact and urgency of the ticket.
* **Perspective:** Combines the detected sentiment with all relevant customer-specific data (tier, previous tickets, revenue, account age) to assign a business priority.
* **Input:** The full `SupportTicket` (all fields) and the `sentiment` from the Sentiment Agent.
* **Output:** `PriorityAssignmentOutput` (containing `priority` - e.g., low, medium, high, critical - and `reasoning`).
* **Rationale:** This agent ensures that high-value customers or critical business issues are prioritized, even if the initial message sentiment isn't overtly "urgent." It brings a business-centric view to the ticket.

### 2.3. Router Agent
* **Role:** To determine the most appropriate department or team for the ticket.
* **Perspective:** Synthesizes all available information (original ticket details, derived sentiment, and assigned priority) to make an informed routing decision.
* **Input:** The full `SupportTicket` (all fields), the `sentiment` from the Sentiment Agent, and the `priority` from the Priority Agent.
* **Output:** `TicketRoutingOutput` (containing `routed_to_department`, a `summary` of the ticket and recommended action, and `reasoning` for the routing decision).
* **Rationale:** This agent acts as the orchestrator, taking the specialized insights from the previous agents and mapping them to actionable routing. It's designed to consider all facets before making the final decision, mimicking a human dispatcher who reviews various inputs.

## 3. Inter-Agent Communication

Agents communicate sequentially by passing structured Pydantic models. The output of one agent serves as a direct input to the next, creating a clear and traceable flow of information:

`SupportTicket` -> `SentimentAgent` -> `SentimentAnalysisOutput` -> `PriorityAgent` -> `PriorityAssignmentOutput` -> `RouterAgent` -> `TicketRoutingOutput`

The `main.py` script orchestrates this flow, ensuring that each agent receives the necessary context from its predecessors.

## 4. Why Multiple Agents?

This multi-agent architecture was chosen over a single, monolithic agent for several key reasons:

* **Specialization and Focus:** Each agent can be fine-tuned for a specific task (sentiment, priority, routing) without diluting its focus. This leads to more accurate and reliable individual outputs. For example, the Sentiment Agent doesn't need to understand routing rules, only emotional tone.
* **Modularity and Maintainability:** Agents are independent units. Changes to priority calculation do not necessitate changes to sentiment analysis or routing logic. This simplifies development, debugging, and future updates.
* **Improved Accuracy through Iteration:** By breaking down the complex task of ticket analysis into smaller, more manageable sub-problems, the system can achieve higher overall accuracy. Each agent refines the understanding of the ticket before passing it on.
* **Clearer Reasoning and Debugging:** Each agent provides its own reasoning for its specific output. This makes the overall decision-making process more transparent and easier to debug if an incorrect routing occurs. We can pinpoint which agent made an erroneous judgment.
* **Scalability:** In a larger system, different agents could potentially run on different services or be scaled independently based on their computational demands. (While not implemented in this prototype, it's a future benefit).

## 5. Handling Agent Discrepancies (Considered)

In this sequential pipeline, direct "discrepancies" between agents are less likely in terms of conflicting primary outputs, as each agent builds upon the previous one. However, the Router Agent is designed to synthesize all information.

The primary concern in this setup is the **propagation of errors**: if an upstream agent (e.g., Sentiment Agent) makes an incorrect classification, this error will be passed to downstream agents (Priority, Router), potentially leading to a cascading incorrect decision.

**Mitigation:** This was addressed through rigorous, iterative prompt engineering for each agent. By focusing on making each agent's individual output as accurate and robust as possible, the likelihood of errors propagating was significantly reduced, as evidenced by all test cases now passing.

**Future Considerations for More Complex Discrepancies:**
While not implemented in this prototype, in more advanced multi-agent systems, potential strategies for handling true "agent opinions" or conflicts could include:
* **Consensus Mechanisms:** If multiple agents perform the *same* task (e.g., two sentiment agents), their outputs could be compared, and a majority vote or weighted average could determine the final decision.
* **Arbitration Agent:** A dedicated higher-level agent could be introduced to review and resolve conflicting outputs from specialized agents, acting as an arbiter.
* **Confidence Scores:** Agents could be designed to output a confidence score alongside their prediction, allowing the orchestrator or subsequent agents to weigh inputs based on their certainty.