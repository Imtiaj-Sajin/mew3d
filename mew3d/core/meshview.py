"""Clay-style mesh preview renders with numpy + matplotlib (no OpenGL needed).

Orthographic painter's-algorithm rendering shaded by face normals - grayscale
"clay" views that are ideal for judging geometry regardless of texturing.
"""

import numpy as np


def _rotation(azimuth_deg: float, elevation_deg: float, up: str) -> np.ndarray:
    az, el = np.radians(azimuth_deg), np.radians(elevation_deg)
    ca, sa, ce, se = np.cos(az), np.sin(az), np.cos(el), np.sin(el)
    rot_az_z = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    rot_az_y = np.array([[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]])
    rot_el_x = np.array([[1, 0, 0], [0, ce, -se], [0, se, ce]])
    return rot_el_x @ (rot_az_z if up == "z" else rot_az_y)


def render_clay_views(
    mesh, out_paths: list, up: str = "y", elevation_deg: float = -15.0, size: int = 384
) -> list:
    """Render len(out_paths) evenly spaced turntable views; returns written paths."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection

    verts = np.asarray(mesh.vertices, dtype=np.float64)
    faces = np.asarray(mesh.faces)
    center = (verts.max(0) + verts.min(0)) / 2
    scale = max(np.linalg.norm(verts - center, axis=1).max(), 1e-9)
    verts = (verts - center) / scale

    written = []
    n = len(out_paths)
    for i, path in enumerate(out_paths):
        rot = _rotation(360.0 * i / n, elevation_deg, up)
        v = verts @ rot.T
        tri = v[faces]  # (F, 3, 3)
        # screen: x right, y up; z toward the viewer
        depth = tri[:, :, 2].mean(axis=1)
        order = np.argsort(depth)  # back-to-front
        normals = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        norm_len = np.linalg.norm(normals, axis=1, keepdims=True)
        normals = normals / np.maximum(norm_len, 1e-12)
        light = np.array([0.3, 0.4, 0.87])
        shade = 0.25 + 0.75 * np.clip(normals @ light, 0, 1)

        fig, ax = plt.subplots(figsize=(size / 96, size / 96), dpi=96)
        polys = PolyCollection(
            tri[order][:, :, :2],
            facecolors=plt.cm.gray(shade[order] * 0.85 + 0.1),
            edgecolors="none",
        )
        ax.add_collection(polys)
        ax.set_xlim(-1.05, 1.05)
        ax.set_ylim(-1.05, 1.05)
        ax.set_aspect("equal")
        ax.axis("off")
        fig.patch.set_facecolor("white")
        fig.savefig(path, bbox_inches="tight", pad_inches=0.05, facecolor="white")
        plt.close(fig)
        written.append(str(path))
    return written
