"""Reminder Agent: schedules notifications via NotificationTool (synchronous demo)."""
from datetime import datetime, timedelta


class ReminderAgent:
    def __init__(self, notification_tool, storage):
        self.notification_tool = notification_tool
        self.storage = storage

    def schedule(self, user_id, reminder):
        # Compute scheduled time for demo purposes
        when = reminder.get("when")
        if when:
            scheduled_time = when
        elif reminder.get("delay_minutes"):
            scheduled_time = (datetime.utcnow() + timedelta(minutes=reminder["delay_minutes"])).isoformat()
        else:
            scheduled_time = datetime.utcnow().isoformat()
        payload = self.notification_tool.send_notification(
            user_id, channel="in-app", message=reminder.get("text"), schedule_time=scheduled_time
        )
        self.storage.append_notification(user_id, payload)
        return payload
