"""Exporter agent: writes final meshes and the human-readable run report."""

import time

from .base import Agent


class ExporterAgent(Agent):
    name = "Exporter"
    icon = "📦"
    description = "exports the mesh and writes the run report"

    def execute(self):
        mesh = self.ctx.state["mesh"]

        obj_path = self.ctx.path("output", "mesh.obj")
        glb_path = self.ctx.path("output", "mesh.glb")
        mesh.export(obj_path)
        self.artifact("OBJ exported", obj_path)
        mesh.export(glb_path)
        self.artifact("GLB exported (vertex colors included)", glb_path)

        report_path = self.ctx.path("report.md")
        report_path.write_text(self._report(), encoding="utf-8")
        self.artifact("run report written", report_path)
        return {"obj": str(obj_path), "glb": str(glb_path), "report": str(report_path)}

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
