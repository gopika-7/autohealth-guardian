"""Memory Agent (wrapper over storage) — for clarity in architecture demos."""
class MemoryAgent:
    def __init__(self, storage):
        self.storage = storage

    def get_user_profile(self, user_id):
        return self.storage.get_user_profile(user_id)

    def update_profile(self, user_id, profile):
        return self.storage.update_user_profile(user_id, profile)
