# Mew3D Run Report - 20260827_090503_upload-1787799903

- **Date:** 2026-08-27 09:07:01
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787799903.jpg
- **Analyst read:** jacket (clothing, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_090503_upload-1787799903\input\user_image.png`

## Quality verdict
- **Score:** 0.88 (PASS)
- Attempts: 1
- Faces: 75,512 | Vertices: 37,762 | Watertight: True | Components: 3
- Attempt 1 LLM opinion: The mesh quality is high with a watertight structure but has a few degenerate faces and multiple components.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted triposr mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `09:05:03` **Analyst** [status] started
- `09:05:04` **Analyst** [decision] subject 'jacket' (clothing, complexity medium) - Ensure the jacket is well-lit and avoid cropping any parts to capture its full shape.
- `09:05:04` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `09:05:04` **Analyst** [status] done
- `09:05:04` **Preprocessor** [status] started
- `09:05:05` **Preprocessor** [artifact] user image copied to run folder
- `09:05:11` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `09:05:11` **Preprocessor** [status] done
- `09:05:11` **MeshGen** [status] started
- `09:05:23` **MeshGen** [artifact] triposr turntable gif saved
- `09:05:25` **MeshGen** [status] done
- `09:05:25` **Judge** [status] started
- `09:05:30` **Judge** [decision] score 0.88 - PASS
- `09:05:30` **Judge** [status] done
- `09:05:30` **TextureSmith** [status] started
- `09:07:01` **TextureSmith** [artifact] textured GLB exported (triposr mesh)
- `09:07:01` **TextureSmith** [artifact] textured previews saved
- `09:07:01` **TextureSmith** [status] done
- `09:07:01` **Exporter** [status] started
- `09:07:01` **Exporter** [artifact] [triposr] OBJ + GLB exported
