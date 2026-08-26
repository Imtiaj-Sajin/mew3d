"""MeshGen agent: single image -> 3D mesh via TripoSR, plus NeRF-rendered turntable previews."""

import sys

from .base import Agent
from ..config import TRIPOSR_DIR, TRIPOSR_MODEL_ID


class MeshGenAgent(Agent):
    name = "MeshGen"
    icon = "🧊"
    description = "reconstructs a 3D mesh from the processed image (TripoSR)"

    def _load_model(self):
        if str(TRIPOSR_DIR) not in sys.path:
            sys.path.insert(0, str(TRIPOSR_DIR))

        def loader():
            from tsr.system import TSR

            model = TSR.from_pretrained(
                TRIPOSR_MODEL_ID, config_name="config.yaml", weight_name="model.ckpt"
            )
            model.renderer.set_chunk_size(self.cfg.chunk_size)
            model.to("cuda")
            return model

        return self.models.acquire("triposr", loader)

    def execute(self):
        import numpy as np
        import torch

        image = self.ctx.state["processed_image"]
        mc_res = self.cfg.adjustments.get("mc_resolution", self.cfg.mc_resolution)

        self.log("loading TripoSR (first run downloads ~1.6GB)")
        model = self._load_model()

        self.progress("encoding image into scene codes")
        with torch.no_grad():
            scene_codes = model([image], device="cuda")

        preview_paths = []
        if self.cfg.n_preview_views > 0:
            self.progress(f"rendering {self.cfg.n_preview_views} preview views")
            renders = model.render(
                scene_codes, n_views=self.cfg.n_preview_views, return_type="pil"
            )[0]
            for i, im in enumerate(renders):
                p = self.ctx.path("output", f"preview_{i:02d}.png")
                im.save(p)
                preview_paths.append(str(p))
            self.artifact(f"{len(renders)} preview renders saved", preview_paths[0])
            try:
                import imageio

                gif_path = self.ctx.path("output", "turntable.gif")
                imageio.mimsave(gif_path, [np.array(im) for im in renders], duration=0.35, loop=0)
                self.artifact("turntable gif saved", gif_path)
            except Exception as e:
                self.log(f"gif skipped: {e}")

        self.progress(f"extracting mesh (marching cubes @ {mc_res}^3)")
        mesh = model.extract_mesh(scene_codes, has_vertex_color=True, resolution=mc_res)[0]
        self.log(f"mesh extracted: {len(mesh.vertices):,} vertices, {len(mesh.faces):,} faces")

        self.ctx.state["mesh"] = mesh
        self.ctx.state["mc_resolution_used"] = mc_res
        self.ctx.state["preview_paths"] = preview_paths
        return mesh
