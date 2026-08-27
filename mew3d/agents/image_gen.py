"""ImageGen agent: text -> candidate images.

Prefers hosted FLUX (much cleaner single-object framing than the local turbo models) and
falls back to the local pipeline when the network or quota is unavailable. Each candidate
uses a distinct prompt variation and its own seed, so retries explore genuinely different
interpretations instead of re-rolling the same picture.
"""

from .base import Agent
from ..config import IMAGE_MODEL_IDS
from ..core.imagegen import (
    ImageProviderError, generate_hf, generate_local, hf_available,
    load_local_pipeline, provider_order, random_seed,
)


class ImageGenAgent(Agent):
    name = "ImageGen"
    icon = "🎨"
    description = "generates candidate images from the enhanced prompt"

    def _local_pipeline(self):
        model_id = IMAGE_MODEL_IDS[self.cfg.image_model]
        self.log(f"loading local {self.cfg.image_model}")
        return self.models.acquire(
            f"t2i:{model_id}",
            lambda: load_local_pipeline(model_id, self.cfg.image_model == "sdxl-turbo"),
        )

    def execute(self):
        enhanced = self.ctx.state["enhanced_prompt"]
        variants = enhanced.get("variants") or [enhanced["prompt"]]
        negative = enhanced["negative_prompt"]
        n = max(1, self.cfg.num_candidates)

        base_seed = self.cfg.adjustments.get("seed", self.cfg.seed)
        if base_seed is None:
            base_seed = random_seed()

        order = [p for p in provider_order() if p != "huggingface" or hf_available()]
        if not order:
            order = ["local"]

        paths, used, pipe = [], None, None
        for i in range(n):
            seed = base_seed + i * 977  # spread seeds so candidates differ meaningfully
            prompt = variants[i % len(variants)]
            self.progress(f"generating candidate {i + 1}/{n} (seed {seed})",
                          current=i + 1, total=n)

            image, error = None, None
            for provider in order:
                try:
                    if provider == "huggingface":
                        image = generate_hf(prompt, seed, self.cfg.hosted_image_size, negative)
                    else:
                        pipe = pipe or self._local_pipeline()
                        image = generate_local(pipe, prompt, negative, seed,
                                               self.cfg.image_steps, self.cfg.image_size)
                    if used != provider:
                        used = provider
                        self.log(f"image provider: {provider}")
                    break
                except (ImageProviderError, Exception) as e:  # noqa: B014 - want any failure
                    error = e
                    self.log(f"{provider} unavailable ({type(e).__name__}: "
                             f"{str(e)[:90]}) - trying next provider")
            if image is None:
                raise RuntimeError(f"all image providers failed: {error}")

            path = self.ctx.path("intermediate", f"candidate_{i:02d}_seed{seed}.png")
            image.save(path)
            self.artifact(f"candidate {i + 1} saved", path)
            paths.append(str(path))

        self.ctx.state["candidate_images"] = paths
        self.ctx.state["image_seed"] = base_seed
        self.ctx.state["image_provider"] = used
        return paths
