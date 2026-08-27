"""MeshGen agent: single image -> 3D mesh via pluggable backends.

Backends:
  triposr - fast (419M), vertex-colored output, NeRF preview renders
  hunyuan - Hunyuan3D-2mini turbo (better geometry, untextured clay output)
  both    - run every backend on the same input so the Judge can compare them
"""

import sys

from .base import Agent
from ..config import TRIPOSR_DIR, TRIPOSR_MODEL_ID
from ..core.meshview import render_clay_views

HUNYUAN_MODEL_ID = "tencent/Hunyuan3D-2mini"
HUNYUAN_SUBFOLDER = "hunyuan3d-dit-v2-mini-turbo"


class MeshGenAgent(Agent):
    name = "MeshGen"
    icon = "🧊"
    description = "reconstructs 3D meshes from the processed image"

    def execute(self):
        backends = (
            ["triposr", "hunyuan"]
            if self.cfg.mesh_model == "both"
            else [self.cfg.mesh_model]
        )
        results = []
        for backend in backends:
            self.log(f"backend: {backend}")
            run = getattr(self, f"_run_{backend}")
            mesh, previews = run()
            self.log(
                f"{backend}: {len(mesh.vertices):,} vertices, {len(mesh.faces):,} faces"
            )
            results.append({"backend": backend, "mesh": mesh, "previews": previews})

        self.ctx.state["mesh_results"] = results
        # single-backend runs keep the original keys so the retry loop stays unchanged
        self.ctx.state["mesh"] = results[0]["mesh"]
        self.ctx.state["preview_paths"] = results[0]["previews"]
        return results

    # -- TripoSR --------------------------------------------------------------
    def _load_triposr(self):
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

    def _run_triposr(self):
        import numpy as np
        import torch

        image = self.ctx.state["processed_image"]
        mc_res = self.cfg.adjustments.get("mc_resolution", self.cfg.mc_resolution)

        model = self._load_triposr()
        self.progress("triposr: encoding image into scene codes")
        with torch.no_grad():
            scene_codes = model([image], device="cuda")

        preview_paths = []
        if self.cfg.n_preview_views > 0:
            self.progress(f"triposr: rendering {self.cfg.n_preview_views} preview views")
            renders = model.render(
                scene_codes, n_views=self.cfg.n_preview_views, return_type="pil"
            )[0]
            for i, im in enumerate(renders):
                p = self.ctx.path("output", f"triposr_preview_{i:02d}.png")
                im.save(p)
                preview_paths.append(str(p))
            try:
                import imageio

                gif_path = self.ctx.path("output", "triposr_turntable.gif")
                imageio.mimsave(
                    gif_path, [np.array(im) for im in renders], duration=0.35, loop=0
                )
                self.artifact("triposr turntable gif saved", gif_path)
            except Exception as e:
                self.log(f"gif skipped: {e}")

        self.progress(f"triposr: extracting mesh (marching cubes @ {mc_res}^3)")
        mesh = model.extract_mesh(scene_codes, has_vertex_color=True, resolution=mc_res)[0]
        self.ctx.state["mc_resolution_used"] = mc_res
        return mesh, preview_paths

    # -- Hunyuan3D-2mini ------------------------------------------------------
    def _load_hunyuan(self):
        def loader():
            from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

            return Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
                HUNYUAN_MODEL_ID, subfolder=HUNYUAN_SUBFOLDER, use_safetensors=True
            )

        return self.models.acquire("hunyuan3d", loader)

    def _set_flashvdm(self, pipe, enabled: bool) -> None:
        try:
            pipe.enable_flashvdm(enabled=enabled, mc_algo="mc" if enabled else None)
        except Exception as e:
            self.log(f"flashvdm toggle ({enabled}) unavailable: {e}")

    def _run_hunyuan(self):
        import torch

        # hunyuan expects the RGBA cutout (transparent background), not the gray composite
        image = self.ctx.state["foreground_rgba"].convert("RGBA")

        self.log("loading Hunyuan3D-2mini (first run downloads the model)")
        pipe = self._load_hunyuan()
        seed = self.ctx.state.get("image_seed") or self.cfg.seed or 2025

        # FlashVDM is fast but crashes on sparse/thin volumes (empty reduction dim);
        # degrade to the plain decoder at lower resolution rather than failing the run.
        ladder = [
            (self.cfg.hunyuan_octree, True),
            (self.cfg.hunyuan_octree, False),
            (256, False),
        ]
        mesh, last_error = None, None
        for octree, flash in ladder:
            self._set_flashvdm(pipe, flash)
            self.progress(
                f"hunyuan: flow-matching diffusion (octree {octree}, "
                f"flashvdm {'on' if flash else 'off'})"
            )
            try:
                result = pipe(
                    image=image,
                    num_inference_steps=self.cfg.hunyuan_steps,
                    guidance_scale=5.0,  # turbo-distilled models use low guidance
                    octree_resolution=octree,
                    generator=torch.Generator().manual_seed(seed),
                )[0]
            except Exception as e:
                last_error = e
                self.log(f"hunyuan decode failed ({type(e).__name__}: {e}) - degrading")
                continue
            candidate = result[0] if isinstance(result, list) else result
            if candidate is not None and len(getattr(candidate, "faces", [])) > 0:
                mesh = candidate
                break
            self.log("hunyuan returned an empty mesh - degrading")

        if mesh is None:
            raise RuntimeError(
                f"Hunyuan3D produced no mesh after {len(ladder)} attempts"
                + (f" (last error: {type(last_error).__name__}: {last_error})" if last_error else "")
            )

        preview_paths = []
        if self.cfg.n_preview_views > 0:
            self.progress("hunyuan: rendering clay preview views")
            out_paths = [
                self.ctx.path("output", f"hunyuan_preview_{i:02d}.png")
                for i in range(self.cfg.n_preview_views)
            ]
            preview_paths = render_clay_views(mesh, out_paths, up="y")
            self.artifact("hunyuan clay previews saved", preview_paths[0])
        return mesh, preview_paths
