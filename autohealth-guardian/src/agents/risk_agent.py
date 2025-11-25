"""Risk Agent: heuristics + small trend analysis for demo."""
from statistics import mean


class RiskAgent:
    def __init__(self, storage):
        self.storage = storage

    def analyze(self, user_id):
        last7 = self.storage.get_last_n_days(user_id, n=7)
        events = []
        if not last7:
            return events
        avg_sleep = mean([d.get("sleep_hours", 0) for d in last7])
        avg_water = mean([d.get("water_ml", 0) for d in last7])
        avg_steps = mean([d.get("steps", 0) for d in last7])
        if avg_sleep < 6:
            events.append({"type": "sleep_deficit", "score": 1, "msg": f"avg_sleep={avg_sleep:.1f}"})
        if avg_water < 1500:
            events.append({"type": "hydration_low", "score": 1, "msg": f"avg_water={avg_water:.0f}ml"})
        if avg_steps < 3000:
            events.append({"type": "low_activity", "score": 1, "msg": f"avg_steps={avg_steps:.0f}"})
        return events
