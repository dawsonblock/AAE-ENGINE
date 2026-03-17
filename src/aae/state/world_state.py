class WorldState:
    def __init__(self):
        self._state = {
            "last_execution": None,
            "last_evaluation": None,
            "agent_tree": {},
        }

    def apply(self, event):
        event_type = event.get("type") or event.get("event_type")
        payload = event.get("payload", {})

        if event_type == "execution_completed":
            self._state["last_execution"] = payload
        elif event_type == "evaluation_completed":
            self._state["last_evaluation"] = payload
        elif event_type in {"supervisor_spawned", "worker_spawned"}:
            self._state["agent_tree"][event.get("agent_id", "unknown")] = {
                "parent_agent_id": event.get("parent_agent_id"),
                "payload": payload,
            }

    def snapshot(self):
        return copy.deepcopy(self._state)
