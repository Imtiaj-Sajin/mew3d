"""The central agent: routes work to specialist agents, runs the judge/retry loop."""

from ..agents.analyst import AnalystAgent
from ..agents.exporter import ExporterAgent
from ..agents.guardian import GatekeeperAgent, screen_request
from ..agents.image_gen import ImageGenAgent
from ..agents.judge import JudgeAgent
from ..agents.mesh_gen import MeshGenAgent
from ..agents.preprocessor import PreprocessorAgent
from ..agents.prompt_smith import PromptSmithAgent
from ..agents.texture_smith import TextureSmithAgent
from ..llm.client import LLMClient
from .model_manager import ModelManager


class BadInputError(RuntimeError):
    """The request cannot produce a useful model - stop instead of burning GPU time."""


class RequestRejected(RuntimeError):
    """The request was refused by the input guardrail."""


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
        self.gatekeeper = GatekeeperAgent(*deps)
        self.mesh_gen = MeshGenAgent(*deps)
        self.judge = JudgeAgent(*deps)
        self.texture_smith = TextureSmithAgent(*deps)
        self.exporter = ExporterAgent(*deps)

    def emit(self, message: str, **data) -> None:
        self.bus.emit(self.name, "log", message, **data)

    def run(self) -> dict:
        cfg = self.cfg
        self.emit(f"run {self.ctx.run_id} starting (mode: {cfg.mode}, "
                  f"LLM: {'on' if self.llm.usable else 'heuristic fallback'})")

        if cfg.text and cfg.screen_input:
            self.bus.emit("Guardian", "status", "started", state="running", icon="🛡️")
            screen = screen_request(cfg.text, self.llm)
            self.ctx.save_json("logs/screening.json", screen)
            if not screen["allowed"]:
                self.bus.emit("Guardian", "decision",
                              f"request refused ({screen['category']}): {screen['reason']}")
                self.bus.emit("Guardian", "status", "done", state="done")
                raise RequestRejected(screen["reason"])
            self.bus.emit("Guardian", "log",
                          "request screened - safe and buildable"
                          + (" (screening degraded)" if screen.get("degraded") else ""))
            self.bus.emit("Guardian", "status", "done", state="done")

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

            # last cheap checkpoint: never spend GPU minutes on input that cannot work
            gate = self.gatekeeper.run(attempt=attempt,
                                       attempts_left=max_attempts - attempt)
            if not gate["proceed"]:
                if gate.get("fatal"):
                    raise BadInputError(
                        f"{gate['problem']}: "
                        + ((gate.get("vision") or {}).get("advice")
                           or "the prepared image cannot produce a useful model")
                    )
                cfg.adjustments.update(gate["recovery"])
                continue  # re-run preprocessing with a different strategy

            self.mesh_gen.run()
            verdict = self.judge.run(attempt=attempt, attempts_left=max_attempts - attempt)

            if verdict["passed"]:
                break
            if attempt < max_attempts:
                cfg.adjustments.update(verdict["adjustments"])

        if verdict is None:
            # every attempt was stopped at the gate before reconstruction
            raise BadInputError(
                "the prepared image never reached a state worth reconstructing - "
                "try a clearer prompt, or an image where the whole object is visible"
            )

        if self.cfg.texture_enabled:
            try:
                self.texture_smith.run()
            except Exception as e:
                # a failed paint must never cost us the mesh - ship clay and say so
                self.emit(f"texture stage failed ({type(e).__name__}: {e}) - "
                          "exporting untextured mesh")

        outputs = self.exporter.run()
        if self.ctx.state.get("textured_glb"):
            outputs["textured_glb"] = self.ctx.state["textured_glb"]
        self.models.release_all()
        self.emit(
            f"run complete - score {verdict['score']:.2f} after "
            f"{verdict['attempt']} attempt(s); outputs in {self.ctx.path('output')}"
        )
        return {"verdict": verdict, "outputs": outputs}
