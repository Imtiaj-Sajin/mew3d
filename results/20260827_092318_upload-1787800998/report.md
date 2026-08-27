# Mew3D Run Report - 20260827_092318_upload-1787800998

- **Date:** 2026-08-27 09:25:49
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787800998.jpg
- **Analyst read:** pixelated cat (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_092318_upload-1787800998\input\user_image.png`

## Quality verdict
- **Score:** 0.73 (PASS)
- Attempts: 1
- Faces: 486,288 | Vertices: 243,150 | Watertight: False | Components: 1
- Attempt 1 concern: sliver-shaped bounding box (ratio 35.81)
- Attempt 1 LLM opinion: The mesh has a good number of vertices and faces, but the non-watertight nature raises concerns for usability.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `09:23:18` **Analyst** [status] started
- `09:23:19` **Analyst** [decision] subject 'pixelated cat' (character, complexity medium) - Ensure to capture the pixelated texture and vibrant background for an authentic retro look.
- `09:23:19` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `09:23:19` **Analyst** [status] done
- `09:23:19` **Preprocessor** [status] started
- `09:23:20` **Preprocessor** [artifact] user image copied to run folder
- `09:23:22` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `09:23:22` **Preprocessor** [status] done
- `09:23:22` **MeshGen** [status] started
- `09:24:03` **MeshGen** [artifact] hunyuan clay previews saved
- `09:24:03` **MeshGen** [status] done
- `09:24:03` **Judge** [status] started
- `09:24:06` **Judge** [decision] score 0.73 - PASS
- `09:24:06` **Judge** [status] done
- `09:24:06` **TextureSmith** [status] started
- `09:25:49` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `09:25:49` **TextureSmith** [artifact] textured previews saved
- `09:25:49` **TextureSmith** [status] done
- `09:25:49` **Exporter** [status] started
- `09:25:49` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
