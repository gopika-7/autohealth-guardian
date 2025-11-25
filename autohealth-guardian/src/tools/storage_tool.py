import json
from pathlib import Path
from datetime import datetime


class StorageTool:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._write({})

    def _read(self):
        try:
            return json.loads(self.db_path.read_text())
        except Exception:
            return {}

    def _write(self, obj):
        self.db_path.write_text(json.dumps(obj, indent=2))

    def append_telemetry(self, user_id, record):
        db = self._read()
        db.setdefault(user_id, {}).setdefault("telemetry", []).append(record)
        self._write(db)

    def get_last_n_days(self, user_id, n=7):
        db = self._read()
        data = db.get(user_id, {}).get("telemetry", [])
        return data[-n:]

    def append_advice_history(self, user_id, advice):
        db = self._read()
        db.setdefault(user_id, {}).setdefault("advice_history", []).append({**advice, "ts": datetime.utcnow().isoformat()})
        self._write(db)

    def append_notification(self, user_id, notification_payload):
        db = self._read()
        db.setdefault(user_id, {}).setdefault("notifications", []).append(notification_payload)
        self._write(db)

    def get_user_profile(self, user_id):
        db = self._read()
        return db.get(user_id, {}).get("profile", {})

    def update_user_profile(self, user_id, profile):
        db = self._read()
        db.setdefault(user_id, {})["profile"] = profile
        self._write(db)
        return profile
