"""TextureSmith agent: paints the reconstructed mesh with Hunyuan3D-Paint.

Runs strictly AFTER mesh generation - the ModelManager evicts the shape model first,
so the full 8GB GPU is available. The paint pipeline (delight + multiview diffusion)
runs fp16 with model CPU offload, streaming weights from system RAM per step.
"""

from .base import Agent

PAINT_MODEL_ID = "tencent/Hunyuan3D-2"
MAX_PAINT_FACES = 40000  # UV unwrap + baking choke far above this


class TextureSmithAgent(Agent):
    name = "TextureSmith"
    icon = "🖌️"
    description = "paints the mesh with diffusion textures (Hunyuan3D-Paint)"

    def _load_pipeline(self):
        def loader():
            # must happen before hy3dgen imports the (possibly unusable) CUDA extension
            from ..core.soft_raster import ensure_rasterizer

            ensure_rasterizer(self.log)

            from hy3dgen.texgen import Hunyuan3DPaintPipeline

            pipe = Hunyuan3DPaintPipeline.from_pretrained(PAINT_MODEL_ID)
            try:
                pipe.enable_model_cpu_offload()
                self.log("cpu offload enabled - weights stream from RAM per step")
            except Exception as e:
                self.log(f"cpu offload unavailable ({e}) - running fully on GPU")
            return pipe

        return self.models.acquire("hunyuan-paint", loader)

    def _pick_mesh(self):
        """Texture the winning backend's mesh (falls back to the primary one)."""
        results = self.ctx.state.get("mesh_results", [])
        winner = self.ctx.state.get("winning_backend")
        for r in results:
            if r["backend"] == winner:
                return r["backend"], r["mesh"]
        if results:
            return results[0]["backend"], results[0]["mesh"]
        return self.cfg.mesh_model, self.ctx.state["mesh"]

    def _paint_remote(self, mesh, image, glb_path, backend) -> bool:
        """Try a remote texture server. Returns True only if it produced the GLB.

        Any failure - no URL, unreachable, timeout, bad response - returns False so the
        caller paints locally instead. A remote outage must never cost the run.
        """
        from ..core.remote_texture import check, paint_remote, texture_url

        url = texture_url()
        if not url:
            return False

        self.progress("checking the remote texture server")
        health = check(url)
        if not health:
            self.log(f"remote texture server unreachable ({url}) - painting locally")
            return False
        if health.get("busy"):
            self.log("remote texture server is busy with another job - painting locally")
            return False

        self.log(f"remote texture server ready on {health.get('gpu', 'unknown GPU')}")
        mesh_tmp = self.ctx.path("intermediate", "for_texturing.glb")
        image_tmp = self.ctx.path("intermediate", "texture_source.png")
        try:
            mesh.export(mesh_tmp)
            image.save(image_tmp)
            self.progress(f"painting {backend} mesh remotely "
                          f"({len(mesh.faces):,} faces uploaded)")
            took = paint_remote(url, mesh_tmp, image_tmp, glb_path)
            self.decision(f"textured remotely in {took:.0f}s "
                          f"(no local GPU time spent on painting)")
            return True
        except Exception as e:
            self.log(f"remote texturing failed ({type(e).__name__}: {str(e)[:100]}) "
                     "- falling back to local")
            return False

    def execute(self):
        backend, mesh = self._pick_mesh()

        if len(mesh.faces) > MAX_PAINT_FACES:
            self.progress(
                f"simplifying mesh for texturing: {len(mesh.faces):,} -> ~{MAX_PAINT_FACES:,} faces"
            )
            from hy3dgen.shapegen import DegenerateFaceRemover, FaceReducer, FloaterRemover

            mesh = FloaterRemover()(mesh)
            mesh = DegenerateFaceRemover()(mesh)
            mesh = FaceReducer()(mesh, max_facenum=MAX_PAINT_FACES)
            self.log(f"simplified to {len(mesh.faces):,} faces")

        image = self.ctx.state["foreground_rgba"].convert("RGBA")
        glb_path = self.ctx.path("output", "mesh_textured.glb")

        if self._paint_remote(mesh, image, glb_path, backend):
            self.ctx.state["texture_where"] = "remote"
        else:
            self.log("loading Hunyuan3D-Paint (first run downloads ~6GB)")
            pipe = self._load_pipeline()
            self.progress(
                f"painting {backend} mesh locally (multiview diffusion + baking, "
                "takes minutes)"
            )
            textured = pipe(mesh, image=image)
            textured.export(glb_path)
            self.ctx.state["texture_where"] = "local"

        self.artifact(f"textured GLB exported ({backend} mesh)", glb_path)

        self.ctx.state["textured_mesh"] = textured
        self.ctx.state["textured_glb"] = str(glb_path)
        self.ctx.state["textured_backend"] = backend

        # turntable previews of the actual textured result
        try:
            from ..core.meshview import render_textured_views

            paths = [self.ctx.path("output", f"textured_preview_{i:02d}.png") for i in range(4)]
            shots = render_textured_views(glb_path, paths)
            self.artifact("textured previews saved", shots[0])
            self.ctx.state["textured_previews"] = shots
        except Exception as e:
            self.log(f"textured previews skipped: {e}")
        return str(glb_path)
