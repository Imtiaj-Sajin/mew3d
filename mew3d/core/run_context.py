"""Per-run workspace: results folder, structured logging, and a shared blackboard for agents."""

import json
import re
import threading
import time
import uuid
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

        # interactive question channel: agents can pause and ask the operator
        self.pending_question: dict | None = None
        self._answered = threading.Event()
        self._answer: str | None = None

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

    # -- interactive questions -------------------------------------------------
    def ask(self, agent: str, text: str, options: list[dict], default: str,
            images: list | None = None, model: str | None = None,
            timeout: float = 240.0) -> str:
        """Pause and ask the operator a question; returns the chosen option value.

        Non-interactive runs (CLI, cron) take `default` immediately, and an unanswered
        question falls back to it after `timeout` so a run can never hang forever.
        """
        if not getattr(self.cfg, "interactive", False):
            return default

        question = {
            "id": uuid.uuid4().hex[:12],
            "agent": agent,
            "text": text,
            "options": options,
            "default": default,
            "images": [self.rel_url(p) for p in (images or []) if p],
            "model": self.rel_url(model) if model else None,
            "asked_at": time.time(),
            "timeout": timeout,
        }
        self.pending_question = question
        self._answer = None
        self._answered.clear()
        self.bus.emit(agent, "question", text, **question)

        answered = self._answered.wait(timeout)
        choice = self._answer if answered and self._answer else default
        self.pending_question = None
        self.bus.emit(
            agent, "decision",
            f"you chose: {choice}" if answered
            else f"no answer within {int(timeout)}s - continuing with '{default}'",
            choice=choice, answered=bool(answered),
        )
        return choice

    def answer(self, question_id: str, choice: str) -> bool:
        q = self.pending_question
        if not q or q["id"] != question_id:
            return False
        self._answer = choice
        self._answered.set()
        return True

    def rel_url(self, path) -> str:
        """Path under this run's folder -> a /files/ URL the web UI can load."""
        try:
            return "/files/" + str(Path(path).resolve().relative_to(
                self.dir.parent.resolve())).replace("\\", "/")
        except (ValueError, OSError):
            return str(path)

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
