"""Project paths, environment setup, and generation configuration."""

import os
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
MODELS_DIR = PROJECT_ROOT / "models"
THIRD_PARTY_DIR = PROJECT_ROOT / "third_party"
TRIPOSR_DIR = THIRD_PARTY_DIR / "TripoSR"


def setup_environment() -> None:
    """Route all model caches onto this drive and load .env. Call before importing torch/diffusers."""
    os.environ.setdefault("HF_HOME", str(MODELS_DIR / "hf"))
    os.environ.setdefault("U2NET_HOME", str(MODELS_DIR / "u2net"))
    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
    try:
        from dotenv import load_dotenv

        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass


IMAGE_MODEL_IDS = {
    "sd-turbo": "stabilityai/sd-turbo",
    "sdxl-turbo": "stabilityai/sdxl-turbo",
}

TRIPOSR_MODEL_ID = "stabilityai/TripoSR"


@dataclass
class GenerationConfig:
    # inputs
    text: str | None = None
    image: str | None = None
    run_name: str | None = None

    # text -> image stage
    image_model: str = "sd-turbo"
    num_candidates: int = 3
    image_size: int = 512
    image_steps: int = 4
    seed: int | None = None

    # preprocessing
    foreground_ratio: float = 0.85

    hosted_image_size: int = 1024  # hosted FLUX handles 1024 comfortably
    screen_input: bool = True      # run the input guardrail before anything loads
    interactive: bool = False      # agents may pause and ask the operator (web UI only)

    # 3D stage
    mesh_model: str = "triposr"  # triposr | hunyuan | both
    mc_resolution: int = 256
    chunk_size: int = 8192
    n_preview_views: int = 4
    hunyuan_steps: int = 5  # turbo model is distilled for ~5 steps
    hunyuan_octree: int = 380
    # None = auto (texture when a hunyuan mesh is produced); CLI --texture/--no-texture
    texture: bool | None = None

    @property
    def texture_enabled(self) -> bool:
        if self.texture is not None:
            return self.texture
        return self.mesh_model in ("hunyuan", "both")

    # orchestration
    max_retries: int = 1
    judge_threshold: float = 0.55
    use_llm: bool = True
    plain_ui: bool = False

    # filled at runtime by the orchestrator/judge between attempts
    adjustments: dict = field(default_factory=dict)

    @property
    def mode(self) -> str:
        if self.image and self.text:
            return "hybrid"
        if self.image:
            return "image23d"
        return "text23d"
