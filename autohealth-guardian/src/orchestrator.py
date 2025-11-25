from pathlib import Path
from agents.monitoring_agent import MonitoringAgent
from agents.risk_agent import RiskAgent
from agents.advice_agent import AdviceAgent
from agents.reminder_agent import ReminderAgent
from agents.reporting_agent import ReportingAgent
from tools.storage_tool import StorageTool
from tools.notification_tool import NotificationTool

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

STORAGE = StorageTool(db_path=DATA_DIR / "memory.json")
NOTIFY = NotificationTool(log_path=DATA_DIR / "notifications.log")


class Orchestrator:
    def __init__(self):
        self.monitor = MonitoringAgent(storage=STORAGE)
        self.risk = RiskAgent(storage=STORAGE)
        self.advice = AdviceAgent(storage=STORAGE)
        self.reminder = ReminderAgent(notification_tool=NOTIFY, storage=STORAGE)
        self.reporting = ReportingAgent(storage=STORAGE)

    def ingest(self, user_id, telemetry):
        """Process a single telemetry dict for a user and return actions."""
        normalized = self.monitor.process(user_id, telemetry)
        risk_events = self.risk.analyze(user_id)
        advice = self.advice.generate(user_id, risk_events)
        scheduled = []
        for a in advice:
            if a.get("type") == "reminder":
                scheduled.append(self.reminder.schedule(user_id, a))
        return {
            "normalized": normalized,
            "risk": risk_events,
            "advice": advice,
            "scheduled": scheduled,
        }

    def generate_weekly_report(self, user_id):
        return self.reporting.generate_weekly_report(user_id)


if __name__ == "__main__":
    orch = Orchestrator()
    sample = {
        "steps": 1200,
        "water_ml": 400,
        "sleep_hours": 5.5,
        "screen_minutes": 260,
    }
    out = orch.ingest("user_1", sample)
    print("--- ORCHESTRATOR OUTPUT ---")
    print(out)
    print("--- GENERATING WEEKLY REPORT ---")
    report_path = orch.generate_weekly_report("user_1")
    print("Report saved to:", report_path)
