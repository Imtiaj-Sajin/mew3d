"""Per-run workspace: results folder, structured logging, and a shared blackboard for agents."""

import json
import re
import time
from pathlib import Path

from ..config import RESULTS_DIR, GenerationConfig
from .events import Event, EventBus


def _slugify(text: str, max_len: int = 32) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len] or "run"


class RunContext:
    """Owns the results/<run_id>/ folder, the event bus, and the inter-agent blackboard."""

    def __init__(self, cfg: GenerationConfig) -> None:
        self.cfg = cfg
        label = cfg.run_name or cfg.text or (Path(cfg.image).stem if cfg.image else "run")
        self.run_id = time.strftime("%Y%m%d_%H%M%S") + "_" + _slugify(label)
        self.dir = RESULTS_DIR / self.run_id
        for sub in ("input", "intermediate", "output", "logs"):
            (self.dir / sub).mkdir(parents=True, exist_ok=True)

        self.bus = EventBus()
        self.state: dict = {}  # blackboard: agents read/write intermediate results here
        self.events: list[Event] = []

        self._events_file = open(self.dir / "logs" / "events.jsonl", "a", encoding="utf-8")
        self._log_file = open(self.dir / "logs" / "run.log", "a", encoding="utf-8")
        self.bus.subscribe(self._record)

    def _record(self, event: Event) -> None:
        self.events.append(event)
        payload = {
            "ts": event.ts,
            "time": time.strftime("%H:%M:%S", time.localtime(event.ts)),
            "agent": event.agent,
            "type": event.type,
            "message": event.message,
            "data": _jsonable(event.data),
        }
        self._events_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self._events_file.flush()
        self._log_file.write(
            f"[{payload['time']}] {event.agent:<12} {event.type:<9} {event.message}\n"
        )
        self._log_file.flush()

    def path(self, *parts: str) -> Path:
        return self.dir.joinpath(*parts)

    def save_json(self, relpath: str, obj) -> Path:
        p = self.path(relpath)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(_jsonable(obj), indent=2, ensure_ascii=False), encoding="utf-8")
        return p

    def close(self) -> None:
        self._events_file.close()
        self._log_file.close()


def _jsonable(obj):
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    if hasattr(obj, "item"):  # numpy scalars
        return obj.item()
    return str(obj)
