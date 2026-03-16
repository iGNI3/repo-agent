from threading import Lock
from datetime import datetime

class StateManager:
    """
    Thread-safe global state manager for agent orchestration.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(StateManager, cls).__new__(cls)
                cls._instance._state = {
                    "current_task": None,
                    "plan": [],
                    "history": [],
                    "files_touched": set(),
                    "status": "idle",
                    "start_time": datetime.now()
                }
            return cls._instance

    def set(self, key, value):
        with self._lock:
            self._state[key] = value

    def get(self, key, default=None):
        with self._lock:
            return self._state.get(key, default)

    def append(self, key, value):
        with self._lock:
            if key in self._state and isinstance(self._state[key], list):
                self._state[key].append(value)
            else:
                self._state[key] = [value]

    def get_all(self):
        with self._lock:
            return self._state.copy()
