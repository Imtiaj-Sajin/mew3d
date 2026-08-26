"""Base class all Mew3D agents share: event emission, timing, status lifecycle."""

import time


class Agent:
    name = "agent"
    icon = "🤖"
    description = ""

    def __init__(self, ctx, models, llm) -> None:
        self.ctx = ctx            # RunContext (blackboard + results folder)
        self.cfg = ctx.cfg        # GenerationConfig
        self.bus = ctx.bus
        self.models = models      # ModelManager
        self.llm = llm            # LLMClient

    # -- convenience emitters -------------------------------------------------
    def log(self, message: str, **data) -> None:
        self.bus.emit(self.name, "log", message, **data)

    def decision(self, message: str, **data) -> None:
        self.bus.emit(self.name, "decision", message, **data)

    def artifact(self, message: str, path) -> None:
        self.bus.emit(self.name, "artifact", message, path=str(path))

    def progress(self, message: str, **data) -> None:
        self.bus.emit(self.name, "progress", message, **data)

    # -- lifecycle ------------------------------------------------------------
    def run(self, **kwargs):
        self.bus.emit(self.name, "status", "started", state="running", icon=self.icon)
        t0 = time.time()
        try:
            result = self.execute(**kwargs)
        except Exception as e:
            self.bus.emit(
                self.name, "status", f"failed: {e}", state="failed",
                elapsed=round(time.time() - t0, 1),
            )
            raise
        self.bus.emit(
            self.name, "status", "done", state="done",
            elapsed=round(time.time() - t0, 1),
        )
        return result

    def execute(self, **kwargs):
        raise NotImplementedError
