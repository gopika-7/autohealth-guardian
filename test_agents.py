"""Very small unit tests for the demo agents (pytest)."""
from pathlib import Path
from tools.storage_tool import StorageTool
from agents.monitoring_agent import MonitoringAgent

def test_monitoring_appends(tmp_path):
    db = tmp_path / "memory.json"
    storage = StorageTool(db_path=db)
    m = MonitoringAgent(storage=storage)
    r = m.process("u1", {"steps": 1000, "water_ml": 500, "sleep_hours": 6})
    assert r["steps"] == 1000
    data = storage.get_last_n_days("u1", n=1)
    assert len(data) == 1
