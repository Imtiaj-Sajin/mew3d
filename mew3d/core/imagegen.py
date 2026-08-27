"""Text-to-image providers.

Hosted FLUX (via Hugging Face inference providers) produces far cleaner single-object
images than the local turbo models, so it is tried first; the local pipeline stays as an
offline fallback so a dead network or spent quota never blocks a run.
"""

import io
import os
import random


class ImageProviderError(RuntimeError):
    pass


def provider_order() -> list[str]:
    raw = os.getenv("AI_IMAGE_PROVIDER_ORDER", "huggingface,local")
    order = [p.strip().lower() for p in raw.split(",") if p.strip()]
    return order or ["huggingface", "local"]


def hf_available() -> bool:
    return bool((os.getenv("HF_API_KEY") or "").strip().strip('"'))


def generate_hf(prompt: str, seed: int, size: int = 1024, negative: str | None = None):
    """One image from a hosted model. Raises ImageProviderError on any failure."""
    from huggingface_hub import InferenceClient

    key = (os.getenv("HF_API_KEY") or "").strip().strip('"')
    if not key:
        raise ImageProviderError("HF_API_KEY not set")
    model = (os.getenv("HF_IMAGE_MODEL") or "black-forest-labs/FLUX.1-schnell").strip().strip('"')
    provider = (os.getenv("HF_IMAGE_PROVIDER") or "auto").strip().strip('"')

    client = InferenceClient(provider=provider, api_key=key, timeout=120)
    kwargs = {"model": model, "width": size, "height": size}
    # FLUX-schnell is CFG-distilled and rejects negative prompts on some providers;
    # seed support also varies, so both are best-effort.
    attempts = [
        {**kwargs, "seed": seed},
        kwargs,
    ]
    last = None
    for attempt in attempts:
        try:
            return client.text_to_image(prompt, **attempt)
        except Exception as e:
            last = e
    raise ImageProviderError(f"{type(last).__name__}: {last}")


def load_local_pipeline(model_id: str, cpu_offload: bool):
    import torch
    from diffusers import AutoPipelineForText2Image

    try:
        pipe = AutoPipelineForText2Image.from_pretrained(
            model_id, torch_dtype=torch.float16, variant="fp16", safety_checker=None,
        )
    except (OSError, ValueError):
        pipe = AutoPipelineForText2Image.from_pretrained(
            model_id, torch_dtype=torch.float16, safety_checker=None,
        )
    pipe.set_progress_bar_config(disable=True)
    if cpu_offload:
        pipe.enable_model_cpu_offload()
    else:
        pipe.to("cuda")
    return pipe


def generate_local(pipe, prompt: str, negative: str, seed: int, steps: int, size: int):
    import torch

    generator = torch.Generator("cuda").manual_seed(seed)
    return pipe(
        prompt=prompt, negative_prompt=negative, num_inference_steps=steps,
        guidance_scale=0.0, height=size, width=size, generator=generator,
    ).images[0]


def random_seed() -> int:
    return random.randint(0, 2**31 - 1)
