"""Exporter agent: writes final meshes and the human-readable run report."""

import time

from .base import Agent


class ExporterAgent(Agent):
    name = "Exporter"
    icon = "📦"
    description = "exports the mesh and writes the run report"

    def execute(self):
        results = self.ctx.state.get("mesh_results") or [
            {"backend": self.cfg.mesh_model, "mesh": self.ctx.state["mesh"]}
        ]
        multi = len(results) > 1
        winner = self.ctx.state.get("winning_backend")
        exported = {}
        for r in results:
            prefix = f"{r['backend']}_" if multi else ""
            obj_path = self.ctx.path("output", f"{prefix}mesh.obj")
            glb_path = self.ctx.path("output", f"{prefix}mesh.glb")
            r["mesh"].export(obj_path)
            r["mesh"].export(glb_path)
            tag = " <- WINNER" if multi and r["backend"] == winner else ""
            self.artifact(f"[{r['backend']}] OBJ + GLB exported{tag}", glb_path)
            exported[r["backend"]] = {"obj": str(obj_path), "glb": str(glb_path)}

        primary = exported.get(winner) or next(iter(exported.values()))
        report_path = self.ctx.path("report.md")
        report_path.write_text(self._report(), encoding="utf-8")
        self.artifact("run report written", report_path)
        return {"obj": primary["obj"], "glb": primary["glb"],
                "report": str(report_path), "all": exported}

    def _report(self) -> str:
        cfg, state = self.cfg, self.ctx.state
        analysis = state.get("analysis", {})
        verdicts = state.get("verdicts", [])
        final = verdicts[-1] if verdicts else {}
        prompt = state.get("enhanced_prompt")

        lines = [
            f"# Mew3D Run Report - {self.ctx.run_id}",
            "",
            f"- **Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **Mode:** {cfg.mode}",
        ]
        if cfg.text:
            lines.append(f"- **Text input:** {cfg.text}")
        if cfg.image:
            lines.append(f"- **Image input:** {cfg.image}")
        if analysis.get("subject"):
            lines.append(
                f"- **Analyst read:** {analysis.get('subject')} "
                f"({analysis.get('category', 'n/a')}, complexity {analysis.get('complexity', 'n/a')})"
            )
        if prompt:
            lines += [
                "",
                "## Prompt enhancement",
                f"- Original: `{prompt['original']}`",
                f"- Enhanced: `{prompt['prompt']}`",
                f"- Negative: `{prompt['negative_prompt']}`",
            ]
        if state.get("selected_candidate"):
            lines.append(f"- Selected candidate: `{state['selected_candidate']}`")

        comparison = final.get("comparison") or []
        if len(comparison) > 1:
            lines += ["", "## Backend comparison", "",
                      "| backend | score | faces | components | vision issue |",
                      "|---|---|---|---|---|"]
            winner = state.get("winning_backend")
            for j in comparison:
                m = j.get("metrics", {})
                mark = " **(winner)**" if j["backend"] == winner else ""
                vision_issue = (j.get("vision_opinion") or {}).get("issue", "-")
                lines.append(
                    f"| {j['backend']}{mark} | {j['score']} | {m.get('faces', 0):,} "
                    f"| {m.get('components', '-')} | {vision_issue} |"
                )

        if final:
            m = final.get("metrics", {})
            lines += [
                "",
                "## Quality verdict",
                f"- **Score:** {final.get('score')} "
                f"({'PASS' if final.get('passed') else 'below threshold, best effort'})",
                f"- Attempts: {len(verdicts)}",
                f"- Faces: {m.get('faces'):,} | Vertices: {m.get('vertices'):,} | "
                f"Watertight: {m.get('watertight')} | Components: {m.get('components')}",
            ]
            for v in verdicts:
                for issue in v.get("issues", []):
                    lines.append(f"- Attempt {v['attempt']} concern: {issue}")
                if v.get("llm_opinion"):
                    lines.append(f"- Attempt {v['attempt']} LLM opinion: {v['llm_opinion']}")

        if state.get("textured_glb"):
            lines += [
                "",
                "## Texture",
                f"- **Textured mesh:** `output/mesh_textured.glb` "
                f"(painted {state.get('textured_backend')} mesh via Hunyuan3D-Paint)",
            ]

        lines += [
            "",
            "## Outputs",
            "- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)",
            "- `output/preview_*.png`, `output/turntable.gif`",
            "- `intermediate/` - candidates and processed inputs",
            "- `logs/events.jsonl` - every agent action, timestamped",
            "",
            "## Agent timeline",
        ]
        for ev in self.ctx.events:
            if ev.type in ("status", "decision", "artifact"):
                t = time.strftime("%H:%M:%S", time.localtime(ev.ts))
                lines.append(f"- `{t}` **{ev.agent}** [{ev.type}] {ev.message}")
        return "\n".join(lines) + "\n"
