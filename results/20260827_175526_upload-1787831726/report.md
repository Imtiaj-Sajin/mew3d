# Mew3D Run Report - 20260827_175526_upload-1787831726

- **Date:** 2026-08-27 17:58:23
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787831726.jpg
- **Analyst read:** cute dinosaur figure (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_175526_upload-1787831726\input\user_image.png`

## Quality verdict
- **Score:** 0.93 (PASS)
- Attempts: 1
- Faces: 831,012 | Vertices: 415,562 | Watertight: False | Components: 7
- Attempt 1 LLM opinion: The mesh exhibits strong geometric fidelity but has concerns regarding watertightness and the presence of degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `17:55:26` **Analyst** [status] started
- `17:55:28` **Analyst** [decision] subject 'cute dinosaur figure' (character, complexity medium) - Ensure to capture the smooth textures and rounded features for a more accurate representation.
- `17:55:28` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `17:55:28` **Analyst** [status] done
- `17:55:28` **Preprocessor** [status] started
- `17:55:30` **Preprocessor** [artifact] user image copied to run folder
- `17:55:32` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `17:55:32` **Preprocessor** [status] done
- `17:55:32` **Gatekeeper** [status] started
- `17:55:34` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `17:55:34` **Gatekeeper** [status] done
- `17:55:34` **MeshGen** [status] started
- `17:56:31` **MeshGen** [artifact] hunyuan clay previews saved
- `17:56:31` **MeshGen** [status] done
- `17:56:31` **Judge** [status] started
- `17:56:35` **Judge** [decision] score 0.93 - PASS
- `17:56:35` **Judge** [status] done
- `17:56:35` **TextureSmith** [status] started
- `17:58:22` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `17:58:22` **TextureSmith** [artifact] textured previews saved
- `17:58:22` **TextureSmith** [status] done
- `17:58:22` **Exporter** [status] started
- `17:58:23` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
