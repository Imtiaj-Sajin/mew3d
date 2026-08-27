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
        results = self.ctx.state.get("mesh_results") or [
            {"backend": self.cfg.mesh_model, "mesh": self.ctx.state["mesh"],
             "previews": self.ctx.state.get("preview_paths", [])}
        ]
        judged = [self._judge_one(r) for r in results]

        if len(judged) > 1:
            ranking = sorted(judged, key=lambda j: j["score"], reverse=True)
            self.decision(
                "backend comparison: "
                + " | ".join(f"{j['backend']} {j['score']:.2f}" for j in ranking)
                + f" -> winner: {ranking[0]['backend']}",
            )
            best = ranking[0]
        else:
            best = judged[0]

        score, issues = best["score"], best["issues"]
        metrics, llm_view, vision_view = best["metrics"], best["llm_view"], best["vision_view"]
        self.ctx.state["winning_backend"] = best["backend"]
        passed = score >= self.cfg.judge_threshold

        # A low score is a judgement call, not a fact - show the operator the actual mesh
        # and let them look before we spend another few minutes redoing it.
        if not passed and getattr(self.cfg, "interactive", False):
            reasons = "; ".join(issues) or "it does not look like the requested subject"
            vision_note = (vision_view or {}).get("issue")
            # export the mesh now so it can be rotated in the viewer before deciding
            glb = None
            try:
                glb_path = self.ctx.path("output", f"review_attempt{attempt}.glb")
                best["mesh"].export(glb_path)
                glb = str(glb_path)
                self.artifact("mesh available for review", glb_path)
            except Exception as e:
                self.log(f"could not export a reviewable mesh: {e}")
            choice = self.ctx.ask(
                self.name,
                f"I scored this {score:.2f} (pass mark {self.cfg.judge_threshold}). "
                f"Concerns: {reasons}"
                + (f". Vision check: {vision_note}" if vision_note else "")
                + ". Rotate it and see what you think.",
                options=(
                    [{"value": "retry", "label": "Try again", "primary": True},
                     {"value": "keep", "label": "Keep this one"}]
                    if attempts_left > 0 else
                    [{"value": "keep", "label": "Keep it", "primary": True}]
                ),
                default="retry" if attempts_left > 0 else "keep",
                images=best.get("previews", [])[:3],
                model=glb,
            )
            if choice == "keep":
                passed = True
                self.decision(f"you accepted the {score:.2f} result - keeping it")

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
            "backend": best["backend"],
            "score": score,
            "passed": passed,
            "metrics": metrics,
            "issues": issues,
            "llm_opinion": (llm_view or {}).get("verdict"),
            "vision_opinion": vision_view,
            "adjustments": adjustments,
            "comparison": [
                {"backend": j["backend"], "score": j["score"], "issues": j["issues"],
                 "metrics": j["metrics"], "vision_opinion": j["vision_view"]}
                for j in judged
            ],
        }
        self.ctx.state.setdefault("verdicts", []).append(verdict)
        self.ctx.save_json(f"logs/judge_attempt_{attempt}.json", verdict)
        return verdict

    def _judge_one(self, result: dict) -> dict:
        """Score one backend's mesh: geometry heuristics + LLM + vision check."""
        backend, mesh, previews = result["backend"], result["mesh"], result["previews"]
        metrics = self._metrics(mesh)
        score, issues = self._score(metrics, self.ctx.state.get("candidate_scores"))
        self.log(
            f"[{backend}] {metrics['faces']:,} faces, {metrics['components']} components, "
            f"watertight={metrics['watertight']}, extent ratio {metrics['extent_ratio']}"
        )
        for issue in issues:
            self.log(f"[{backend}] concern: {issue}")

        llm_view = self.llm.chat_json(
            self.name, JUDGE_SYSTEM,
            f"Backend: {backend}. Metrics: {metrics}. Heuristic score {score} (threshold "
            f"{self.cfg.judge_threshold}). Subject: "
            f"{self.ctx.state.get('analysis', {}).get('subject', 'unknown')!r}.",
        )
        if llm_view and llm_view.get("verdict"):
            self.log(f"[{backend}] LLM second opinion: {llm_view['verdict']}")

        vision_view, score = self._vision_check(score, previews, backend)
        return {"backend": backend, "score": score, "issues": issues, "mesh": mesh,
                "previews": previews, "metrics": metrics, "llm_view": llm_view,
                "vision_view": vision_view}

    def _vision_check(self, score: float, previews: list, backend: str) -> tuple[dict | None, float]:
        """Show a preview render to the vision LLM; semantic failure slashes the score."""
        from ..llm.client import VISION_MESH_SYSTEM

        if not self.llm.usable or not previews:
            return None, score
        subject = self.ctx.state.get("analysis", {}).get("subject", "object")
        images = []
        src = self.ctx.state.get("processed_image_path")
        if src:
            images.append(src)
        images.extend(previews[:3])
        view = self.llm.chat_json_vision(
            self.name, VISION_MESH_SYSTEM,
            f"Subject: {subject!r}. First image is the source photo; the rest are views "
            "of the reconstruction. Judge shape fidelity only.",
            images,
        )
        if not view:
            return None, score
        if view.get("looks_like_subject") is False or view.get("is_flat_or_blob") is True:
            score = round(score * 0.35, 3)
            self.log(f"[{backend}] vision check FAILED: "
                     f"{view.get('issue', 'does not look like subject')} "
                     f"- score slashed to {score}")
        else:
            vlm = max(0.0, min(1.0, float(view.get("score", 5)) / 10.0))
            score = round(0.6 * score + 0.4 * vlm, 3)
            self.log(f"[{backend}] vision check: looks like {subject!r}, "
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
