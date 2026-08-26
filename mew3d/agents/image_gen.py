"""ImageGen agent: text -> candidate images via SD-Turbo / SDXL-Turbo (fits 8GB VRAM)."""

import random

from .base import Agent
from ..config import IMAGE_MODEL_IDS


class ImageGenAgent(Agent):
    name = "ImageGen"
    icon = "🎨"
    description = "generates candidate images from the enhanced prompt"

    def _load_pipeline(self):
        import torch
        from diffusers import AutoPipelineForText2Image

        model_id = IMAGE_MODEL_IDS[self.cfg.image_model]

        def loader():
            try:
                pipe = AutoPipelineForText2Image.from_pretrained(
                    model_id, torch_dtype=torch.float16, variant="fp16",
                    safety_checker=None,
                )
            except (OSError, ValueError):
                pipe = AutoPipelineForText2Image.from_pretrained(
                    model_id, torch_dtype=torch.float16, safety_checker=None,
                )
            pipe.set_progress_bar_config(disable=True)
            if self.cfg.image_model == "sdxl-turbo":
                pipe.enable_model_cpu_offload()  # sdxl is tight on 8GB
            else:
                pipe.to("cuda")
            return pipe

        return self.models.acquire(f"t2i:{model_id}", loader)

    def execute(self):
        import torch

        enhanced = self.ctx.state["enhanced_prompt"]
        n = max(1, self.cfg.num_candidates)
        base_seed = self.cfg.adjustments.get("seed", self.cfg.seed)
        if base_seed is None:
            base_seed = random.randint(0, 2**31 - 1)

        self.log(f"loading {self.cfg.image_model} (first run downloads the model)")
        pipe = self._load_pipeline()

        paths = []
        for i in range(n):
            seed = base_seed + i
            self.progress(f"generating candidate {i + 1}/{n} (seed {seed})",
                          current=i + 1, total=n)
            generator = torch.Generator("cuda").manual_seed(seed)
            image = pipe(
                prompt=enhanced["prompt"],
                negative_prompt=enhanced["negative_prompt"],
                num_inference_steps=self.cfg.image_steps,
                guidance_scale=0.0,  # turbo models are distilled for CFG-free sampling
                height=self.cfg.image_size,
                width=self.cfg.image_size,
                generator=generator,
            ).images[0]
            path = self.ctx.path("intermediate", f"candidate_{i:02d}_seed{seed}.png")
            image.save(path)
            self.artifact(f"candidate {i + 1} saved", path)
            paths.append(str(path))

        self.ctx.state["candidate_images"] = paths
        self.ctx.state["image_seed"] = base_seed
        return paths
