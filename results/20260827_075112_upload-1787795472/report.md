# Mew3D Run Report - 20260827_075112_upload-1787795472

- **Date:** 2026-08-27 07:54:17
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787795472.jpg
- **Analyst read:** robot figure (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_075112_upload-1787795472\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 1,195,844 | Vertices: 597,916 | Watertight: False | Components: 13
- Attempt 1 LLM opinion: The mesh quality is high, but it is not watertight and contains degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `07:51:13` **Analyst** [status] started
- `07:51:15` **Analyst** [decision] subject 'robot figure' (character, complexity medium) - Ensure to capture the smooth surfaces and simple shapes for accurate reconstruction.
- `07:51:15` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `07:51:15` **Analyst** [status] done
- `07:51:15` **Preprocessor** [status] started
- `07:51:18` **Preprocessor** [artifact] user image copied to run folder
- `07:51:19` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `07:51:19` **Preprocessor** [status] done
- `07:51:19` **MeshGen** [status] started
- `07:52:22` **MeshGen** [artifact] hunyuan clay previews saved
- `07:52:22` **MeshGen** [status] done
- `07:52:22` **Judge** [status] started
- `07:52:27` **Judge** [decision] score 0.89 - PASS
- `07:52:27` **Judge** [status] done
- `07:52:27` **TextureSmith** [status] started
- `07:54:15` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `07:54:15` **TextureSmith** [artifact] textured previews saved
- `07:54:15` **TextureSmith** [status] done
- `07:54:15` **Exporter** [status] started
- `07:54:17` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
