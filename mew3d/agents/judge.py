"""Judge agent: scores the reconstructed mesh, decides pass / retry, proposes adjustments."""

import numpy as np

from .base import Agent

JUDGE_SYSTEM = """You are the quality judge of a 3D generation studio. You receive geometric
metrics of a mesh reconstructed from a single image. Give a short verdict. Reply with JSON:
{"verdict": "<one sentence assessment>", "concerns": ["<concern>", ...]}"""


class JudgeAgent(Agent):
    name = "Judge"
    icon = "⚖️"
    description = "scores mesh quality and decides whether to retry"

    def _metrics(self, mesh) -> dict:
        extents = mesh.extents if len(mesh.vertices) else np.zeros(3)
        try:
            components = mesh.split(only_watertight=False)
            comp_faces = sorted((len(c.faces) for c in components), reverse=True)
            largest_frac = comp_faces[0] / max(1, len(mesh.faces)) if comp_faces else 0.0
            n_components = len(components)
        except Exception:
            n_components, largest_frac = 1, 1.0
        degenerate = int((mesh.area_faces < 1e-10).sum()) if len(mesh.faces) else 0
        return {
            "vertices": len(mesh.vertices),
            "faces": len(mesh.faces),
            "watertight": bool(mesh.is_watertight),
            "components": n_components,
            "largest_component_fraction": round(float(largest_frac), 3),
            "extents": [round(float(e), 3) for e in extents],
            "extent_ratio": round(float(extents.max() / max(extents.min(), 1e-6)), 2),
            "degenerate_faces": degenerate,
        }

    def _score(self, m: dict, image_scores: dict | None) -> tuple[float, list[str]]:
        score, issues = 1.0, []
        if m["faces"] < 2000:
            score -= 0.5
            issues.append(f"very low face count ({m['faces']})")
        elif m["faces"] < 10000:
            score -= 0.15
            issues.append(f"low face count ({m['faces']})")
        if m["largest_component_fraction"] < 0.85 and m["components"] > 3:
            score -= 0.25
            issues.append(
                f"fragmented: {m['components']} pieces, main piece only "
                f"{m['largest_component_fraction'] * 100:.0f}% of faces"
            )
        if m["extent_ratio"] > 6:
            score -= 0.2
            issues.append(f"sliver-shaped bounding box (ratio {m['extent_ratio']})")
        if not m["watertight"]:
            score -= 0.05  # common for marching cubes output; mild penalty
        if m["degenerate_faces"] > 0.03 * max(1, m["faces"]):
            score -= 0.1
            issues.append("many degenerate faces")
        if image_scores and image_scores.get("blob_score", 1.0) < 0.75:
            score -= 0.15
            issues.append("source image foreground was fragmented")
        return max(0.0, round(score, 3)), issues

    def execute(self, attempt: int, attempts_left: int):
        mesh = self.ctx.state["mesh"]
        metrics = self._metrics(mesh)
        score, issues = self._score(metrics, self.ctx.state.get("candidate_scores"))
        passed = score >= self.cfg.judge_threshold

        self.log(
            f"mesh metrics: {metrics['faces']:,} faces, {metrics['components']} components, "
            f"watertight={metrics['watertight']}, extent ratio {metrics['extent_ratio']}"
        )
        for issue in issues:
            self.log(f"concern: {issue}")

        llm_view = self.llm.chat_json(
            self.name, JUDGE_SYSTEM,
            f"Metrics: {metrics}. Heuristic score {score} (threshold "
            f"{self.cfg.judge_threshold}). Subject: "
            f"{self.ctx.state.get('analysis', {}).get('subject', 'unknown')!r}.",
        )
        if llm_view and llm_view.get("verdict"):
            self.log(f"LLM second opinion: {llm_view['verdict']}")

        # geometric metrics can't see semantics - a vision check on the render can
        vision_view, score = self._vision_check(score)
        passed = score >= self.cfg.judge_threshold

        adjustments = {}
        if not passed and attempts_left > 0:
            adjustments = self._plan_retry(issues)
            self.decision(
                f"score {score:.2f} < {self.cfg.judge_threshold} - requesting retry "
                f"with {adjustments}", score=score, adjustments=adjustments,
            )
        else:
            self.decision(
                f"score {score:.2f} - {'PASS' if passed else 'accepting best effort (no retries left)'}",
                score=score,
            )

        verdict = {
            "attempt": attempt,
            "score": score,
            "passed": passed,
            "metrics": metrics,
            "issues": issues,
            "llm_opinion": (llm_view or {}).get("verdict"),
            "vision_opinion": vision_view,
            "adjustments": adjustments,
        }
        self.ctx.state.setdefault("verdicts", []).append(verdict)
        self.ctx.save_json(f"logs/judge_attempt_{attempt}.json", verdict)
        return verdict

    def _vision_check(self, score: float) -> tuple[dict | None, float]:
        """Show a preview render to the vision LLM; semantic failure slashes the score."""
        from ..llm.client import VISION_MESH_SYSTEM

        previews = self.ctx.state.get("preview_paths") or []
        if not self.llm.usable or not previews:
            return None, score
        subject = self.ctx.state.get("analysis", {}).get("subject", "object")
        view = self.llm.chat_json_vision(
            self.name, VISION_MESH_SYSTEM,
            f"Requested subject: {subject!r}. Judge this render of the reconstruction.",
            previews[0],
        )
        if not view:
            return None, score
        if view.get("looks_like_subject") is False or view.get("is_flat_or_blob") is True:
            score = round(score * 0.35, 3)
            self.log(f"vision check FAILED: {view.get('issue', 'does not look like subject')} "
                     f"- score slashed to {score}")
        else:
            vlm = max(0.0, min(1.0, float(view.get("score", 5)) / 10.0))
            score = round(0.6 * score + 0.4 * vlm, 3)
            self.log(f"vision check: looks like {subject!r}, "
                     f"{view.get('score', '?')}/10 ({view.get('issue', 'none')})")
        return view, score

    def _plan_retry(self, issues: list[str]) -> dict:
        """Choose what to change for the next attempt based on what went wrong."""
        adj = dict(self.cfg.adjustments)
        if self.cfg.mode == "text23d":
            candidates = self.ctx.state.get("candidate_images", [])
            selected = self.ctx.state.get("selected_candidate")
            rejected = self.ctx.state.setdefault("rejected_candidates", [])
            if selected and selected not in rejected:
                rejected.append(selected)
            if len(rejected) >= len(candidates):
                # all candidates burned: regenerate with a fresh seed
                adj["seed"] = self.ctx.state.get("image_seed", 0) + 1000
                self.ctx.state["rejected_candidates"] = []
                adj["regenerate_images"] = True
                self.log("all candidates exhausted - will regenerate images with a new seed")
            else:
                adj["regenerate_images"] = False
                self.log("will retry with the next-best candidate image")
        else:
            # user image: reframe smaller and extract at higher resolution
            current = adj.get("foreground_ratio", self.cfg.foreground_ratio)
            adj["foreground_ratio"] = round(max(0.6, current - 0.1), 2)
        # more marching-cubes resolution helps thin/fragmented geometry on any retry
        adj["mc_resolution"] = min(320, int(adj.get("mc_resolution", self.cfg.mc_resolution) * 1.25))
        return adj
