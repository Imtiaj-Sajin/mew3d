# Mew3D Run Report - 20260827_122819_upload-1787812099

- **Date:** 2026-08-27 12:31:46
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787812099.png
- **Analyst read:** game controller (prop, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_122819_upload-1787812099\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 584,280 | Vertices: 292,140 | Watertight: False | Components: 3
- Attempt 1 LLM opinion: The mesh is of high quality with a good heuristic score, but it is not watertight and has a few degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `12:28:19` **Analyst** [status] started
- `12:28:21` **Analyst** [decision] subject 'game controller' (prop, complexity medium) - Ensure to capture the details of the buttons and texture for accurate reconstruction.
- `12:28:21` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `12:28:21` **Analyst** [status] done
- `12:28:21` **Preprocessor** [status] started
- `12:28:23` **Preprocessor** [artifact] user image copied to run folder
- `12:28:25` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `12:28:25` **Preprocessor** [status] done
- `12:28:25` **MeshGen** [status] started
- `12:29:41` **MeshGen** [artifact] hunyuan clay previews saved
- `12:29:41` **MeshGen** [status] done
- `12:29:41` **Judge** [status] started
- `12:29:46` **Judge** [decision] score 0.89 - PASS
- `12:29:46` **Judge** [status] done
- `12:29:46` **TextureSmith** [status] started
- `12:31:45` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `12:31:45` **TextureSmith** [artifact] textured previews saved
- `12:31:45` **TextureSmith** [status] done
- `12:31:45` **Exporter** [status] started
- `12:31:46` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
