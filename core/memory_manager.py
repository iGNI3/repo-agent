import json
import os

class MemoryManager:
    def __init__(self, history_path):
        self.history_path = history_path
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_path):
            with open(self.history_path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def add_turn(self, role, content):
        self.history.append({"role": role, "content": content})
        self.save_history()

    def save_history(self):
        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        with open(self.history_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2)

    def get_context(self, limit=10):
        """Returns the last N turns of history."""
        return self.history[-limit:]
