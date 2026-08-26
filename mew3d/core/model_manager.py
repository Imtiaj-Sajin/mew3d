"""VRAM-aware model registry: only one heavy model lives on the 8GB GPU at a time."""

import gc


class ModelManager:
    def __init__(self, bus) -> None:
        self.bus = bus
        self._loaded: dict = {}

    def acquire(self, key: str, loader):
        """Return the model for `key`, loading it via `loader()` after evicting everything else."""
        if key in self._loaded:
            return self._loaded[key]
        if self._loaded:
            self.release_all()
        self.bus.emit("vram", "log", f"loading model: {key}")
        model = loader()
        self._loaded[key] = model
        self._report(f"after loading {key}")
        return model

    def release_all(self) -> None:
        if not self._loaded:
            return
        names = list(self._loaded)
        self._loaded.clear()
        gc.collect()
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass
        self.bus.emit("vram", "log", f"released models: {', '.join(names)}")

    def _report(self, note: str) -> None:
        try:
            import torch

            if torch.cuda.is_available():
                used = torch.cuda.memory_allocated() / 1e9
                total = torch.cuda.get_device_properties(0).total_memory / 1e9
                self.bus.emit(
                    "vram", "metric", f"VRAM {used:.1f}/{total:.1f} GB ({note})",
                    used_gb=round(used, 2), total_gb=round(total, 2),
                )
        except ImportError:
            pass
