"""Reporting Agent: aggregate data and create a weekly PDF report."""
from tools.pdf_tool import PDFTool
from statistics import mean


class ReportingAgent:
    def __init__(self, storage):
        self.storage = storage
        self.pdf = PDFTool()

    def generate_weekly_report(self, user_id):
        data = self.storage.get_last_n_days(user_id, n=7)
        if not data:
            # generate empty report
            return self.pdf.generate_weekly_report(user_id, {})
        agg = {
            "avg_sleep": mean([d.get("sleep_hours", 0) for d in data]),
            "avg_water": mean([d.get("water_ml", 0) for d in data]),
            "avg_steps": mean([d.get("steps", 0) for d in data]),
        }
        return self.pdf.generate_weekly_report(user_id, agg)
