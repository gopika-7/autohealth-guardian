"""Advice Agent: map risk events to advice and reminders."""
class AdviceAgent:
    def __init__(self, storage):
        self.storage = storage

    def generate(self, user_id, risk_events):
        adv = []
        for e in risk_events:
            if e["type"] == "sleep_deficit":
                adv.append({"type": "advice", "text": "Try a 30-min screen-free wind-down before bed."})
                adv.append({"type": "reminder", "text": "Start sleep wind-down - dim lights & relax.", "when": "21:00"})
            if e["type"] == "hydration_low":
                adv.append({"type": "advice", "text": "Aim to drink +300ml today."})
                adv.append({"type": "reminder", "text": "Drink 200ml water now", "repeat_minutes": 120})
            if e["type"] == "low_activity":
                adv.append({"type": "advice", "text": "Try a 10-min walk after lunch."})
                adv.append({"type": "reminder", "text": "10-min walk", "delay_minutes": 60})
        for a in adv:
            # persist advice + timestamp
            self.storage.append_advice_history(user_id, a)
        return adv
