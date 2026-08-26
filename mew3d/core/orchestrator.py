"""The central agent: routes work to specialist agents, runs the judge/retry loop."""

from ..agents.analyst import AnalystAgent
from ..agents.exporter import ExporterAgent
from ..agents.image_gen import ImageGenAgent
from ..agents.judge import JudgeAgent
from ..agents.mesh_gen import MeshGenAgent
from ..agents.preprocessor import PreprocessorAgent
from ..agents.prompt_smith import PromptSmithAgent
from ..llm.client import LLMClient
from .model_manager import ModelManager


class Orchestrator:
    name = "Orchestrator"

    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.cfg = ctx.cfg
        self.bus = ctx.bus
        self.models = ModelManager(self.bus)
        self.llm = LLMClient(self.bus, enabled=self.cfg.use_llm)

        deps = (ctx, self.models, self.llm)
        self.analyst = AnalystAgent(*deps)
        self.prompt_smith = PromptSmithAgent(*deps)
        self.image_gen = ImageGenAgent(*deps)
        self.preprocessor = PreprocessorAgent(*deps)
        self.mesh_gen = MeshGenAgent(*deps)
        self.judge = JudgeAgent(*deps)
        self.exporter = ExporterAgent(*deps)

    def emit(self, message: str, **data) -> None:
        self.bus.emit(self.name, "log", message, **data)

    def run(self) -> dict:
        cfg = self.cfg
        self.emit(f"run {self.ctx.run_id} starting (mode: {cfg.mode}, "
                  f"LLM: {'on' if self.llm.usable else 'heuristic fallback'})")

        self.analyst.run()

        text_mode = cfg.mode == "text23d"
        if text_mode:
            self.prompt_smith.run()

        if cfg.mesh_model == "both" and cfg.max_retries:
            self.emit("compare mode: retries disabled (one clean pass per backend)")
            cfg.max_retries = 0

        max_attempts = 1 + max(0, cfg.max_retries)
        images_generated = False
        verdict = None

        for attempt in range(1, max_attempts + 1):
            if attempt > 1:
                self.emit(f"--- retry: attempt {attempt}/{max_attempts} "
                          f"with adjustments {cfg.adjustments} ---")

            if text_mode and (not images_generated or cfg.adjustments.get("regenerate_images")):
                self.image_gen.run()
                images_generated = True
                cfg.adjustments.pop("regenerate_images", None)

            self.preprocessor.run()
            self.mesh_gen.run()
            verdict = self.judge.run(attempt=attempt, attempts_left=max_attempts - attempt)

            if verdict["passed"]:
                break
            if attempt < max_attempts:
                cfg.adjustments.update(verdict["adjustments"])

        outputs = self.exporter.run()
        self.models.release_all()
        self.emit(
            f"run complete - score {verdict['score']:.2f} after "
            f"{verdict['attempt']} attempt(s); outputs in {self.ctx.path('output')}"
        )
        return {"verdict": verdict, "outputs": outputs}
