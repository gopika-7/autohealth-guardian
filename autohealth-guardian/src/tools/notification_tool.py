from datetime import datetime
import uuid
import json


class NotificationTool:
    def __init__(self, log_path=None):
        self.log_path = log_path

    def send_notification(self, user_id, channel, message, schedule_time=None):
        nid = str(uuid.uuid4())
        payload = {
            "id": nid,
            "user_id": user_id,
            "channel": channel,
            "message": message,
            "scheduled_at": schedule_time or datetime.utcnow().isoformat(),
        }
        line = json.dumps(payload)
        if self.log_path:
            with open(self.log_path, "a") as f:
                f.write(line + "\n")
        else:
            print("[NOTIFY]", line)
        return payload

    def cancel(self, nid):
        # demo: no-op / log
        if self.log_path:
            with open(self.log_path, "a") as f:
                f.write(json.dumps({"cancel": nid}) + "\n")
        return True
