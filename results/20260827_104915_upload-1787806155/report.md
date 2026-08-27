# Mew3D Run Report - 20260827_104915_upload-1787806155

- **Date:** 2026-08-27 10:51:39
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787806155.jpg
- **Analyst read:** camera (prop, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_104915_upload-1787806155\input\user_image.png`

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 647,136 | Vertices: 323,560 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh quality is high with a watertight structure and a strong heuristic score, but the presence of degenerate faces is a concern.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:49:15` **Analyst** [status] started
- `10:49:16` **Analyst** [decision] subject 'camera' (prop, complexity medium) - Ensure to capture the details of the lens and buttons for accurate reconstruction.
- `10:49:16` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:49:16` **Analyst** [status] done
- `10:49:16` **Preprocessor** [status] started
- `10:49:16` **Preprocessor** [artifact] user image copied to run folder
- `10:49:18` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:49:18` **Preprocessor** [status] done
- `10:49:18` **MeshGen** [status] started
- `10:50:02` **MeshGen** [artifact] hunyuan clay previews saved
- `10:50:02` **MeshGen** [status] done
- `10:50:02` **Judge** [status] started
- `10:50:06` **Judge** [decision] score 0.92 - PASS
- `10:50:06` **Judge** [status] done
- `10:50:06` **TextureSmith** [status] started
- `10:51:38` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:51:38` **TextureSmith** [artifact] textured previews saved
- `10:51:38` **TextureSmith** [status] done
- `10:51:38` **Exporter** [status] started
- `10:51:39` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
