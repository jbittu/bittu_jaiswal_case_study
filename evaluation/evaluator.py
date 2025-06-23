from shared_models import Sentiment, Priority, Department

class Evaluator:
    def __init__(self):
        self.metrics = {
            "correct_routing": {"correct": 0, "total": 0},
            "priority_accuracy": {"correct": 0, "total": 0},
            "sentiment_alignment": {"correct": 0, "total": 0}
        }
        self.detailed_results = {}

    def evaluate(self, agent_results: dict, expected_results: dict):
        print("--- Running Evaluation ---")
        for ticket_id, agent_output_data in agent_results.items():
            if "error" in agent_output_data:
                print(f"⚠️ Skipping evaluation for {ticket_id} due to error: {agent_output_data['error']}")
                continue

            expected = expected_results.get(ticket_id)
            if not expected:
                print(f"⚠️ Warning: No expected output for ticket {ticket_id}. Skipping.")
                continue

            try:
                agent_sentiment = Sentiment(agent_output_data.get('sentiment'))
                agent_priority = Priority(agent_output_data.get('priority'))
                agent_department = Department(agent_output_data.get('routed_to_department'))
            except Exception as e:
                print(f"⚠️ Enum conversion failed for {ticket_id}: {e}")
                continue

            # Metric 1: Correct Routing
            if agent_department == expected["routed_to_department"]:
                self.metrics["correct_routing"]["correct"] += 1
            self.metrics["correct_routing"]["total"] += 1

            # Metric 2: Priority Accuracy
            if agent_priority == expected["priority"]:
                self.metrics["priority_accuracy"]["correct"] += 1
            self.metrics["priority_accuracy"]["total"] += 1

            # Metric 3: Sentiment Alignment
            if agent_sentiment == expected["sentiment"]:
                self.metrics["sentiment_alignment"]["correct"] += 1
            self.metrics["sentiment_alignment"]["total"] += 1

            self.detailed_results[ticket_id] = {
                "agent_output": {
                    "sentiment": agent_sentiment.value,
                    "priority": agent_priority.value,
                    "routed_to_department": agent_department.value,
                    "summary": agent_output_data.get("summary"),
                    "reasoning": agent_output_data.get("reasoning")
                },
                "expected_output": {
                    "sentiment": expected["sentiment"].value,
                    "priority": expected["priority"].value,
                    "routed_to_department": expected["routed_to_department"].value
                },
                "routing_correct": agent_department == expected["routed_to_department"],
                "priority_correct": agent_priority == expected["priority"],
                "sentiment_correct": agent_sentiment == expected["sentiment"]
            }

        self._print_summary()
        self._print_detailed_results()

    def _print_summary(self):
        print("\n--- Summary Metrics ---")
        for metric_name, data in self.metrics.items():
            if data["total"] > 0:
                accuracy = (data["correct"] / data["total"]) * 100
                print(f"{metric_name.replace('_', ' ').title()}: {accuracy:.2f}% ({data['correct']}/{data['total']})")
            else:
                print(f"{metric_name.replace('_', ' ').title()}: No data")

    def _print_detailed_results(self):
        print("\n--- Detailed Test Case Results ---")
        for ticket_id, details in self.detailed_results.items():
            print(f"\nTicket ID: {ticket_id}")
            print(f"   Agent Routing: {details['agent_output']['routed_to_department']} (Correct: {details['routing_correct']})")
            print(f"   Expected Routing: {details['expected_output']['routed_to_department']}")
            print(f"   Agent Priority: {details['agent_output']['priority']} (Correct: {details['priority_correct']})")
            print(f"   Expected Priority: {details['expected_output']['priority']}")
            print(f"   Agent Sentiment: {details['agent_output']['sentiment']} (Correct: {details['sentiment_correct']})")
            print(f"   Expected Sentiment: {details['expected_output']['sentiment']}")
            print(f"   Agent Summary: {details['agent_output']['summary']}")
            print(f"   Agent Reasoning: {details['agent_output']['reasoning']}")
