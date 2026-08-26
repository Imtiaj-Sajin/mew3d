"""Prefetch all model weights into the local cache (resumable; rerun if interrupted)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mew3d.config import setup_environment  # noqa: E402

setup_environment()

from huggingface_hub import snapshot_download  # noqa: E402


def fetch(repo_id: str, allow_patterns=None) -> None:
    print(f"--> {repo_id}", flush=True)
    snapshot_download(repo_id, allow_patterns=allow_patterns)
    print(f"OK  {repo_id}", flush=True)


# sd-turbo: fp16 weights + configs/tokenizer only (skip fp32 + safety checker extras)
fetch(
    "stabilityai/sd-turbo",
    allow_patterns=[
        "*.json", "*.txt", "**/*.json", "**/*.txt",
        "**/*.fp16.safetensors", "tokenizer/*", "scheduler/*",
    ],
)
fetch("stabilityai/TripoSR", allow_patterns=["config.yaml", "model.ckpt"])
# Hunyuan3D-Paint texture stage (delight + multiview diffusion, used by --texture)
fetch(
    "tencent/Hunyuan3D-2",
    allow_patterns=["hunyuan3d-delight-v2-0/*", "hunyuan3d-paint-v2-0/*"],
)
# Hunyuan3D-2mini: turbo shape DiT + turbo VAE (used by --mesh-model hunyuan/both)
fetch(
    "tencent/Hunyuan3D-2mini",
    allow_patterns=[
        "hunyuan3d-dit-v2-mini-turbo/*",
        "hunyuan3d-vae-v2-mini-turbo/*",
        "*.json", "*.yaml",
    ],
)
# DINO image tokenizer used inside TripoSR
fetch("facebook/dino-vitb16")

# u2net for rembg
print("--> u2net (rembg)", flush=True)
import rembg  # noqa: E402

rembg.new_session("u2net")
print("OK  u2net", flush=True)

print("ALL MODELS PREFETCHED", flush=True)
