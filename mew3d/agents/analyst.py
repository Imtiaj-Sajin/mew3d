"""Analyst agent: inspects the request, judges feasibility, and plans the pipeline."""

from pathlib import Path

from .base import Agent

ANALYST_SYSTEM = """You are the intake analyst of a local 3D-generation studio.
Given a user's request (text prompt, image, or both), assess it for single-object 3D
reconstruction. Reply with JSON:
{"subject": "<short name of the object>",
 "category": "<creature|character|vehicle|furniture|food|prop|architecture|abstract|other>",
 "single_object": true/false,
 "complexity": "<low|medium|high>",
 "advice": "<one sentence of advice for the downstream image/3D generation agents>"}
Scenes with many objects reconstruct poorly - if the request describes a scene, set
single_object=false and advise focusing on the main subject."""

ANALYST_VISION_SYSTEM = """You are the intake analyst of a local 3D-generation studio.
Look at the user's image and identify what should be reconstructed in 3D. Reply with JSON:
{"subject": "<short name of the main object you see>",
 "category": "<creature|character|vehicle|furniture|food|prop|architecture|abstract|other>",
 "single_object": true/false,
 "complexity": "<low|medium|high>",
 "advice": "<one sentence of advice for the downstream reconstruction agents, e.g. about
 framing, cut-off parts, or busy background>"}"""


class AnalystAgent(Agent):
    name = "Analyst"
    icon = "🔎"
    description = "judges the input and plans the pipeline"

    def execute(self):
        cfg = self.cfg
        mode = cfg.mode
        self.log(f"input mode: {mode}"
                 + (f" | text: {cfg.text!r}" if cfg.text else "")
                 + (f" | image: {Path(cfg.image).name}" if cfg.image else ""))

        if mode == "text23d":
            pipeline = ["PromptSmith", "ImageGen", "Preprocessor", "MeshGen", "Judge", "Exporter"]
        else:
            # with an input image, TripoSR consumes the image; text (if any) informs the judge
            pipeline = ["Preprocessor", "MeshGen", "Judge", "Exporter"]

        analysis = {"mode": mode, "pipeline": pipeline}

        described = cfg.text or (Path(cfg.image).stem.replace("_", " ") if cfg.image else "")
        if cfg.image:
            # identify the subject by LOOKING at the image, not from the filename
            hint = f" The user also says it is: {cfg.text!r}." if cfg.text else ""
            llm_view = self.llm.chat_json_vision(
                self.name, ANALYST_VISION_SYSTEM,
                f"Identify the main object in this image for 3D reconstruction.{hint}",
                cfg.image,
            )
        else:
            llm_view = self.llm.chat_json(
                self.name, ANALYST_SYSTEM,
                f"Request: {described!r}. Input mode: {mode}.",
            )
        if llm_view:
            analysis.update(llm_view)
            self.decision(
                f"subject '{llm_view.get('subject')}' ({llm_view.get('category')}, "
                f"complexity {llm_view.get('complexity')}) - {llm_view.get('advice')}",
            )
            if llm_view.get("single_object") is False:
                self.log("warning: request looks like a multi-object scene; "
                         "reconstruction will focus on the dominant subject")
        else:
            analysis["subject"] = described or "object"
            self.log("LLM not available - using heuristic analysis")

        self.decision("pipeline plan: " + " -> ".join(pipeline), pipeline=pipeline)
        self.ctx.state["analysis"] = analysis
        self.ctx.save_json("logs/analysis.json", analysis)
        return analysis
