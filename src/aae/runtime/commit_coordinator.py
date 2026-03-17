class CommitCoordinator:
    def __init__(self, event_bus):
        """Rule 1 & 5: Central coordinator for valid result promotion."""
        self.event_bus = event_bus

    def publish_promotion(self, task_id, repo_id, agent_id, payload):
        """Emits event signaling valid and approved repair candidate."""
        return self.event_bus.publish(
            "candidate_promoted",
            task_id,
            repo_id,
            agent_id,
            payload
        )

    def verify_success(self, task_id, repo_id, evaluation):
        """Hooks for root agent final approval before PR creation."""
        # Optional check: If reward < 0, maybe retry or reject promotion
        return evaluation.get("success", False)
