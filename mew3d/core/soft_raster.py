"""Pure-PyTorch drop-in replacement for Hunyuan3D-Paint's `custom_rasterizer` extension.

The upstream package is a compiled CUDA extension, and the prebuilt Windows wheels are
each built for a narrow set of GPU architectures - on an unlisted card every kernel fails
with "no kernel image is available for execution on the device". This module reimplements
the two functions the paint pipeline actually uses (`rasterize` and `interpolate`) with
plain tensor ops, so texturing runs on any CUDA GPU (and on CPU) with no wheel to match.

Semantics are ported from the reference kernel (rasterizer_gpu.cu):
  screen_x = (x/w * 0.5 + 0.5) * (W - 1) + 0.5      pixel centres at (px+0.5, py+0.5)
  screen_y = (0.5 + 0.5 * y/w) * (H - 1) + 0.5      coverage: all barycentrics in [0, 1]
  screen_z = z/w * 0.49999 + 0.5                    depth key: trunc(z * 2**18)
Nearest fragment wins, ties broken by lower face index (the reference packs both into one
int64 token and takes an atomicMin; we reproduce the token exactly and scatter-reduce it).
Returned barycentrics are perspective-corrected, as upstream.
"""

import torch

MAXINT = 2147483647
_SENTINEL = MAXINT * MAXINT + (MAXINT - 1)  # matches the reference z-buffer initialiser
_PAIR_BUDGET = 2_000_000  # (face, pixel) candidates per chunk; caps peak memory


def _to_screen(pos, width: int, height: int):
    w = pos[:, 3]
    w = torch.where(w.abs() < 1e-12, torch.full_like(w, 1e-12), w)
    sx = (pos[:, 0] / w * 0.5 + 0.5) * (width - 1) + 0.5
    sy = (0.5 + 0.5 * pos[:, 1] / w) * (height - 1) + 0.5
    sz = pos[:, 2] / w * 0.49999 + 0.5
    return sx, sy, sz, w


def _signed_area2(ax, ay, bx, by, cx, cy):
    """Reference calculateSignedArea2(a, b, c)."""
    return (cx - ax) * (by - ay) - (bx - ax) * (cy - ay)


def _barycentric(ax, ay, bx, by, cx, cy, px, py):
    """Reference calculateBarycentricCoordinate; degenerate triangles return -1 (never inside)."""
    area = _signed_area2(ax, ay, bx, by, cx, cy)
    beta_t = _signed_area2(ax, ay, px, py, cx, cy)
    gamma_t = _signed_area2(ax, ay, bx, by, px, py)
    degenerate = area == 0
    inv = 1.0 / torch.where(degenerate, torch.ones_like(area), area)
    beta = beta_t * inv
    gamma = gamma_t * inv
    alpha = 1.0 - beta - gamma
    neg = torch.full_like(area, -1.0)
    return (
        torch.where(degenerate, neg, alpha),
        torch.where(degenerate, neg, beta),
        torch.where(degenerate, neg, gamma),
    )


def _chunk_bounds(counts, budget: int):
    """Yield (start, end) face ranges whose candidate-pair totals stay under `budget`."""
    n = int(counts.numel())
    if n == 0:
        return
    cum = torch.cumsum(counts, 0)
    start, base = 0, 0
    while start < n:
        limit = torch.tensor(base + budget, device=cum.device, dtype=cum.dtype)
        end = int(torch.searchsorted(cum, limit, right=True).item())
        end = max(end, start + 1)  # always make progress, even for one huge triangle
        yield start, end
        base = int(cum[end - 1].item())
        start = end


def rasterize(pos, tri, resolution, clamp_depth=torch.zeros(0), use_depth_prior=0):
    """Rasterise clip-space triangles.

    pos: (1, V, 4) or (V, 4) clip coords. tri: (F, 3) indices. resolution: (H, W).
    Returns findices (H, W) int32 - 0 is background, otherwise face index + 1 - and
    barycentric (H, W, 3) float32.
    """
    if pos.dim() == 3:
        pos = pos[0]
    height, width = int(resolution[0]), int(resolution[1])
    device = pos.device
    pos = pos.float()
    faces = tri.long()

    sx, sy, sz, wc = _to_screen(pos, width, height)
    fx = sx[faces]  # (F, 3)
    fy = sy[faces]
    fz = sz[faces]

    raw_xmin, raw_xmax = fx.min(dim=1).values, fx.max(dim=1).values
    raw_ymin, raw_ymax = fy.min(dim=1).values, fy.max(dim=1).values
    onscreen = (raw_xmax >= 0) & (raw_xmin <= width - 1) & \
               (raw_ymax >= 0) & (raw_ymin <= height - 1)

    xmin = raw_xmin.floor().clamp(0, width - 1).long()
    xmax = raw_xmax.floor().clamp(0, width - 1).long()
    ymin = raw_ymin.floor().clamp(0, height - 1).long()
    ymax = raw_ymax.floor().clamp(0, height - 1).long()

    box_w = (xmax - xmin + 1).clamp(min=0)
    box_h = (ymax - ymin + 1).clamp(min=0)
    counts = torch.where(onscreen, box_w * box_h, torch.zeros_like(box_w))

    keep = (counts > 0).nonzero(as_tuple=True)[0]
    best = torch.full((height * width,), _SENTINEL, dtype=torch.int64, device=device)
    if keep.numel() == 0:
        return (torch.zeros((height, width), dtype=torch.int32, device=device),
                torch.zeros((height, width, 3), dtype=torch.float32, device=device))

    kept_counts = counts[keep]
    for start, end in _chunk_bounds(kept_counts, _PAIR_BUDGET):
        fidx = keep[start:end]
        c = counts[fidx]
        total = int(c.sum().item())
        if total == 0:
            continue
        rep = torch.repeat_interleave(fidx, c)
        offsets = torch.cumsum(c, 0) - c
        local = torch.arange(total, device=device) - torch.repeat_interleave(offsets, c)
        bw = torch.repeat_interleave(box_w[fidx], c)
        px = xmin[rep] + local % bw
        py = ymin[rep] + local // bw

        vx = px.float() + 0.5
        vy = py.float() + 0.5
        alpha, beta, gamma = _barycentric(
            fx[rep, 0], fy[rep, 0], fx[rep, 1], fy[rep, 1], fx[rep, 2], fy[rep, 2], vx, vy
        )
        inside = ((alpha >= 0) & (alpha <= 1) & (beta >= 0) & (beta <= 1)
                  & (gamma >= 0) & (gamma <= 1))
        if not bool(inside.any()):
            continue

        depth = alpha * fz[rep, 0] + beta * fz[rep, 1] + gamma * fz[rep, 2]
        # reference packs trunc(depth * 2**18) and the 1-based face id into one sortable key
        zq = (depth * float(2 << 17)).trunc().clamp(min=0).to(torch.int64)
        token = zq * MAXINT + (rep + 1)
        pixel = py * width + px
        best.scatter_reduce_(0, pixel[inside], token[inside], reduce="amin")

    f = best % MAXINT
    findices = torch.where(f == MAXINT - 1, torch.zeros_like(f), f)

    barycentric = torch.zeros((height * width, 3), dtype=torch.float32, device=device)
    hit = (findices > 0).nonzero(as_tuple=True)[0]
    if hit.numel() > 0:
        face = findices[hit] - 1
        vx = (hit % width).float() + 0.5
        vy = torch.div(hit, width, rounding_mode="floor").float() + 0.5
        alpha, beta, gamma = _barycentric(
            fx[face, 0], fy[face, 0], fx[face, 1], fy[face, 1],
            fx[face, 2], fy[face, 2], vx, vy,
        )
        # perspective correction, exactly as upstream: divide by clip w, then renormalise
        tri_w = wc[faces[face]]
        b = torch.stack([alpha, beta, gamma], dim=1) / tri_w
        barycentric[hit] = b / b.sum(dim=1, keepdim=True).clamp(min=1e-20)

    return (findices.to(torch.int32).view(height, width),
            barycentric.view(height, width, 3))


def interpolate(col, findices, barycentric, tri):
    """Barycentric attribute interpolation (identical to the upstream pure-torch helper)."""
    f = findices - 1 + (findices == 0)
    vcol = col[0, tri.long()[f.long()]]
    result = barycentric.view(*barycentric.shape, 1) * vcol
    result = torch.sum(result, axis=-2)
    return result.view(1, *result.shape)


_PROBE = """
import torch, custom_rasterizer as cr
pos = torch.tensor([[[-1.,-1.,0.,1.],[1.,-1.,0.,1.],[-1.,1.,0.,1.]]], device='cuda')
tri = torch.tensor([[0,1,2]], dtype=torch.int32, device='cuda')
f, _ = cr.rasterize(pos, tri, (32, 32))
torch.cuda.synchronize()
raise SystemExit(0 if bool((f > 0).any()) else 1)
"""

_native_cache = None


def _native_works() -> bool:
    """Probe the compiled extension in a SUBPROCESS.

    A failing CUDA kernel poisons the whole CUDA context, so probing in-process would
    break every later GPU call in this run even after we fall back. Isolating it in a
    child process keeps our context clean whatever the outcome.
    """
    global _native_cache
    if _native_cache is not None:
        return _native_cache

    import subprocess
    import sys

    try:
        import custom_rasterizer as cr  # noqa: F401

        if getattr(sys.modules["custom_rasterizer"], "_MEW3D_SHIM", False):
            _native_cache = True
            return True
    except Exception:
        _native_cache = False
        return False

    try:
        done = subprocess.run(
            [sys.executable, "-c", _PROBE], capture_output=True, timeout=180
        )
        _native_cache = done.returncode == 0
    except Exception:
        _native_cache = False
    return _native_cache


def ensure_rasterizer(log=None) -> str:
    """Make `custom_rasterizer` importable and functional; returns the backend in use.

    Prefers the compiled extension when it genuinely runs on this GPU, otherwise installs
    this pure-PyTorch implementation under the same module name.
    """
    import sys
    import types

    if _native_works():
        if log:
            log("rasterizer: native custom_rasterizer extension")
        return "native"

    shim = types.ModuleType("custom_rasterizer")
    shim.rasterize = rasterize
    shim.interpolate = interpolate
    shim._MEW3D_SHIM = True
    sys.modules["custom_rasterizer"] = shim
    if log:
        log("rasterizer: compiled extension unusable on this GPU - "
            "using the pure-PyTorch fallback")
    return "pure-torch"
