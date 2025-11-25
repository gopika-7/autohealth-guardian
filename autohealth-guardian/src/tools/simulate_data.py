"""Generate simulated telemetry CSV and/or push into storage."""
import argparse
import random
from pathlib import Path
from src.tools.storage_tool import StorageTool
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def simulate(user_id: str, days: int = 14, out_db: Path = DATA_DIR / "memory.json"):
    storage = StorageTool(db_path=out_db)
    today = datetime.utcnow().date()
    for i in range(days):
        d = today - timedelta(days=(days - 1 - i))
        record = {
            "ts": datetime.combine(d, datetime.min.time()).isoformat(),
            "steps": random.randint(1000, 9000),
            "water_ml": random.randint(800, 2500),
            "sleep_hours": round(random.uniform(4.0, 8.5), 1),
            "screen_minutes": random.randint(120, 420),
        }
        storage.append_telemetry(user_id, record)
    print(f"Simulated {days} days for {user_id} -> {out_db}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--user", default="user_1")
    p.add_argument("--days", type=int, default=14)
    args = p.parse_args()
    simulate(args.user, args.days)
