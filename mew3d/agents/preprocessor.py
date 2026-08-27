"""Preprocessor agent: background removal, candidate scoring/selection, TripoSR framing.

Output convention matches TripoSR's reference pipeline: RGBA foreground resized so the
object fills `foreground_ratio` of a square canvas, composited over 50% gray.
"""

import numpy as np
from PIL import Image

from .base import Agent


def remove_background(image: Image.Image, session) -> Image.Image:
    import rembg

    return rembg.remove(image, session=session)


def resize_foreground(image: Image.Image, ratio: float) -> Image.Image:
    """Crop to the alpha bounding box and pad so the object occupies `ratio` of the frame."""
    arr = np.array(image)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 10)
    if len(ys) == 0:
        return image  # nothing detected; let the judge complain downstream
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    fg = arr[y0:y1, x0:x1]
    size = int(max(fg.shape[0], fg.shape[1]) / ratio)
    canvas = np.zeros((size, size, 4), dtype=np.uint8)
    oy = (size - fg.shape[0]) // 2
    ox = (size - fg.shape[1]) // 2
    canvas[oy:oy + fg.shape[0], ox:ox + fg.shape[1]] = fg
    return Image.fromarray(canvas)


def composite_gray(image: Image.Image) -> Image.Image:
    arr = np.array(image).astype(np.float32) / 255.0
    rgb = arr[:, :, :3] * arr[:, :, 3:4] + 0.5 * (1 - arr[:, :, 3:4])
    return Image.fromarray((rgb * 255.0).astype(np.uint8))


def score_candidate(rgba: Image.Image) -> dict:
    """Heuristic quality score for picking the best candidate image."""
    arr = np.array(rgba)
    alpha = arr[:, :, 3].astype(np.float32) / 255.0
    coverage = float(alpha.mean())
    # sharpness proxy: variance of the luminance gradient inside the foreground
    lum = arr[:, :, :3].astype(np.float32).mean(axis=2)
    gy, gx = np.gradient(lum)
    grad = np.sqrt(gx**2 + gy**2)
    sharpness = float((grad * (alpha > 0.5)).mean())
    # ideal coverage ~0.35: big enough to have detail, small enough to be one object
    coverage_score = max(0.0, 1.0 - abs(coverage - 0.35) / 0.35)
    sharpness_score = min(1.0, sharpness / 12.0)
    # fragmentation: how much of the alpha mass sits in the largest connected blob
    from scipy import ndimage  # scipy ships with skimage's dependency tree

    labels, n = ndimage.label(alpha > 0.5)
    if n > 0:
        sizes = ndimage.sum(alpha > 0.5, labels, range(1, n + 1))
        blob_score = float(sizes.max() / max(1.0, sizes.sum()))
    else:
        blob_score = 0.0
    # Frame-edge contact. Which edge matters: a bust, a standing figure or anything
    # resting on the ground legitimately fills the bottom edge, so only contact at the
    # top and sides really means the subject is clipped.
    edges = {
        "top": float((alpha[0, :] > 0.5).mean()),
        "bottom": float((alpha[-1, :] > 0.5).mean()),
        "left": float((alpha[:, 0] > 0.5).mean()),
        "right": float((alpha[:, -1] > 0.5).mean()),
    }
    border_contact = float(np.mean(list(edges.values())))
    clipping = max(edges["top"], edges["left"], edges["right"])
    border_score = max(0.0, 1.0 - clipping * 3.0)
    total = (
        0.3 * coverage_score
        + 0.1 * sharpness_score
        + 0.25 * blob_score
        + 0.35 * border_score
    )
    return {
        "coverage": round(coverage, 3),
        "coverage_score": round(coverage_score, 3),
        "sharpness_score": round(sharpness_score, 3),
        "blob_score": round(blob_score, 3),
        "border_contact": round(border_contact, 3),
        "edge_top": round(edges["top"], 3),
        "edge_bottom": round(edges["bottom"], 3),
        "edge_sides": round(max(edges["left"], edges["right"]), 3),
        "clipping": round(clipping, 3),
        "border_score": round(border_score, 3),
        "total": round(total, 3),
    }


class PreprocessorAgent(Agent):
    name = "Preprocessor"
    icon = "🪄"
    description = "removes backgrounds, scores candidates, frames the object"

    def _vision_review(self, scored: list) -> list:
        """Blend heuristic scores with a vision-LLM critique of each candidate image."""
        from ..llm.client import VISION_CANDIDATE_SYSTEM

        if not self.llm.usable:
            return scored
        subject = self.ctx.state.get("analysis", {}).get("subject", self.cfg.text or "object")
        reviewed = []
        for src, rgba, scores in scored:
            view = self.llm.chat_json_vision(
                self.name, VISION_CANDIDATE_SYSTEM,
                f"Requested subject: {subject!r}. Judge this image.", src,
            )
            if not view:
                reviewed.append((src, rgba, scores))
                continue
            vlm = max(0.0, min(1.0, float(view.get("score", 5)) / 10.0))
            blended = 0.5 * scores["total"] + 0.5 * vlm
            if view.get("complete_object") is False or view.get("single_object") is False:
                blended *= 0.3  # cut-off or multi-object images are near-useless for 3D
            scores = {**scores, "vlm_score": round(vlm, 2),
                      "vlm_issue": view.get("issue", "none"),
                      "total": round(blended, 3)}
            self.log(f"vision critic: {view.get('issue', 'none')} "
                     f"(vlm {vlm * 10:.0f}/10 -> blended {scores['total']:.2f})",
                     source=src, **{k: v for k, v in view.items() if k != "issue"})
            reviewed.append((src, rgba, scores))
        return reviewed

    def _session(self, model: str = "u2net"):
        """Cache one rembg session per model - the Gatekeeper can ask for a different one."""
        import rembg

        cache = getattr(self, "_rembg_sessions", None)
        if cache is None:
            cache = self._rembg_sessions = {}
        if model not in cache:
            self.log(f"loading background-removal model ({model})")
            cache[model] = rembg.new_session(model)
        return cache[model]

    @staticmethod
    def _keep_largest_component(rgba: Image.Image) -> Image.Image:
        """Drop everything but the biggest blob - used when several objects survive."""
        from scipy import ndimage

        arr = np.array(rgba)
        mask = arr[:, :, 3] > 128
        labels, n = ndimage.label(mask)
        if n <= 1:
            return rgba
        sizes = ndimage.sum(mask, labels, range(1, n + 1))
        keep = int(np.argmax(sizes)) + 1
        arr[:, :, 3] = np.where(labels == keep, arr[:, :, 3], 0)
        return Image.fromarray(arr)

    def execute(self):
        cfg = self.cfg
        ratio = cfg.adjustments.get("foreground_ratio", cfg.foreground_ratio)
        rembg_model = cfg.adjustments.get("rembg_model", "u2net")
        largest_only = cfg.adjustments.get("largest_component_only", False)
        session = self._session(rembg_model)

        if cfg.mode == "text23d":
            sources = self.ctx.state["candidate_images"]
        else:
            src = self.ctx.path("input", "user_image.png")
            if not src.exists():
                Image.open(cfg.image).convert("RGB").save(src)
                self.artifact("user image copied to run folder", src)
            sources = [str(src)]

        skip = set(self.ctx.state.get("rejected_candidates", []))
        scored = []
        for i, src in enumerate(sources):
            if src in skip:
                continue
            self.progress(f"removing background {i + 1}/{len(sources)}",
                          current=i + 1, total=len(sources))
            rgba = remove_background(Image.open(src).convert("RGB"), session)
            if largest_only:
                rgba = self._keep_largest_component(rgba)
            scores = score_candidate(rgba)
            scored.append((src, rgba, scores))
            self.log(f"candidate {i + 1} scored {scores['total']:.2f} "
                     f"(coverage {scores['coverage']:.2f}, blob {scores['blob_score']:.2f}, "
                     f"edge-cut {scores['border_contact']:.2f})",
                     source=src, **scores)

        if not scored:
            raise RuntimeError("no usable candidate images left after rejections")

        scored = self._vision_review(scored)
        scored.sort(key=lambda t: t[2]["total"], reverse=True)
        best_src, best_rgba, best_scores = scored[0]
        if len(scored) > 1:
            self.decision(
                f"selected best candidate (score {best_scores['total']:.2f}): {best_src}",
                scores=[{"source": s, **sc} for s, _, sc in scored],
            )
        if best_scores["total"] < 0.4:
            self.log("warning: even the best candidate scores poorly - "
                     "the judge will likely order a retry")

        framed = resize_foreground(best_rgba, ratio)
        processed = composite_gray(framed)
        rgba_path = self.ctx.path("intermediate", "foreground_rgba.png")
        framed.save(rgba_path)
        out_path = self.ctx.path("intermediate", "processed_input.png")
        processed.save(out_path)
        self.artifact(f"processed input ready (foreground ratio {ratio})", out_path)

        self.ctx.state["selected_candidate"] = best_src
        self.ctx.state["candidate_scores"] = best_scores
        self.ctx.state["processed_image"] = processed
        self.ctx.state["processed_image_path"] = str(out_path)
        self.ctx.state["foreground_rgba"] = framed
        self.ctx.state["foreground_rgba_path"] = str(rgba_path)
        return processed
