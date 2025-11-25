"""Monitoring Agent: normalize telemetry and persist to storage."""
from datetime import datetime


class MonitoringAgent:
    def __init__(self, storage):
        self.storage = storage

    def process(self, user_id, telemetry: dict):
        record = {
            "ts": datetime.utcnow().isoformat(),
            "steps": int(telemetry.get("steps", 0)),
            "water_ml": int(telemetry.get("water_ml", 0)),
            "sleep_hours": float(telemetry.get("sleep_hours", 0)),
            "screen_minutes": int(telemetry.get("screen_minutes", 0)),
        }
        self.storage.append_telemetry(user_id, record)
        return record
