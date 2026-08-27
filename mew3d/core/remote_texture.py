"""Client for an optional remote texture server (see scripts/colab_texture_server.ipynb).

Texturing is the slowest stage on an 8GB card, because the paint model does not fit in
VRAM and streams its weights from system RAM. A 16GB machine (a free Colab T4, say) runs
the same stage several times faster. Mesh generation stays local either way - it is quick
here and not worth the upload.

Everything is best-effort: an unset URL, an unreachable server, or a failed request all
fall through to local texturing rather than failing the run.
"""

import os
import time


def texture_url() -> str | None:
    url = (os.getenv("MEW3D_TEXTURE_URL") or "").strip().strip('"').rstrip("/")
    return url or None


def check(url: str, timeout: float = 8.0) -> dict | None:
    """Ping the server. Returns its health payload, or None if it is not usable."""
    import requests

    try:
        r = requests.get(f"{url}/health", timeout=timeout)
        if r.status_code != 200:
            return None
        info = r.json()
        return info if info.get("service") == "mew3d-texture" else None
    except Exception:
        return None


def paint_remote(url: str, mesh_path, image_path, out_path, timeout: float = 900.0) -> float:
    """Send a mesh + its source image, save the textured GLB. Returns seconds taken."""
    import requests

    started = time.time()
    with open(mesh_path, "rb") as mesh_f, open(image_path, "rb") as image_f:
        response = requests.post(
            f"{url}/texture",
            files={
                "mesh": ("mesh.glb", mesh_f, "model/gltf-binary"),
                "image": ("image.png", image_f, "image/png"),
            },
            timeout=timeout,
        )
    response.raise_for_status()
    body = response.content
    if len(body) < 1024 or not body[:4] == b"glTF":
        raise RuntimeError(f"server did not return a GLB ({len(body)} bytes)")
    with open(out_path, "wb") as out:
        out.write(body)
    return time.time() - started
