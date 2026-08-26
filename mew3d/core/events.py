"""Event bus every agent publishes to; the live UI and the run logger subscribe."""

import threading
import time
from dataclasses import dataclass, field


@dataclass
class Event:
    ts: float
    agent: str
    type: str  # status | log | progress | decision | artifact | metric | error
    message: str
    data: dict = field(default_factory=dict)


class EventBus:
    def __init__(self) -> None:
        self._subscribers: list = []
        self._lock = threading.Lock()

    def subscribe(self, fn) -> None:
        self._subscribers.append(fn)

    def emit(self, agent: str, type: str, message: str, **data) -> Event:
        event = Event(time.time(), agent, type, message, data)
        with self._lock:
            for fn in self._subscribers:
                try:
                    fn(event)
                except Exception:
                    pass  # a broken subscriber must never kill the pipeline
        return event
