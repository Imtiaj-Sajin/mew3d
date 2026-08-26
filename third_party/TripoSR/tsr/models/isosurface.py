from typing import Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from skimage import measure


class IsosurfaceHelper(nn.Module):
    points_range: Tuple[float, float] = (0, 1)

    @property
    def grid_vertices(self) -> torch.FloatTensor:
        raise NotImplementedError


class MarchingCubeHelper(IsosurfaceHelper):
    """Marching cubes via scikit-image (pure Python wheels; no CUDA build needed).

    Drop-in replacement for the original torchmcubes-based implementation:
    skimage returns vertices already in (dim0, dim1, dim2) == (x, y, z) grid order,
    so the [2, 1, 0] axis flip from the original code is not needed.
    """

    def __init__(self, resolution: int) -> None:
        super().__init__()
        self.resolution = resolution
        self._grid_vertices: Optional[torch.FloatTensor] = None

    @property
    def grid_vertices(self) -> torch.FloatTensor:
        if self._grid_vertices is None:
            # keep the vertices on CPU so that we can support very large resolution
            x, y, z = (
                torch.linspace(*self.points_range, self.resolution),
                torch.linspace(*self.points_range, self.resolution),
                torch.linspace(*self.points_range, self.resolution),
            )
            x, y, z = torch.meshgrid(x, y, z, indexing="ij")
            verts = torch.cat(
                [x.reshape(-1, 1), y.reshape(-1, 1), z.reshape(-1, 1)], dim=-1
            ).reshape(-1, 3)
            self._grid_vertices = verts
        return self._grid_vertices

    def forward(
        self,
        level: torch.FloatTensor,
    ) -> Tuple[torch.FloatTensor, torch.LongTensor]:
        # inside becomes positive, matching skimage's "object > background" convention
        volume = (
            -level.view(self.resolution, self.resolution, self.resolution)
            .detach()
            .cpu()
            .numpy()
            .astype(np.float32)
        )
        verts, faces, _, _ = measure.marching_cubes(
            volume, level=0.0, gradient_direction="descent"
        )
        v_pos = torch.from_numpy(verts.copy()).float() / (self.resolution - 1.0)
        # skimage winds faces opposite to torchmcubes; flip so normals point outward
        t_pos_idx = torch.from_numpy(faces[:, ::-1].astype(np.int64).copy())
        return v_pos.to(level.device), t_pos_idx.to(level.device)
