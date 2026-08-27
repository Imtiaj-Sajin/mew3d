# Mew3D Run Report - 20260827_090143_upload-1787799703

- **Date:** 2026-08-27 09:04:16
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787799703.jpg
- **Analyst read:** jacket (clothing, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_090143_upload-1787799703\input\user_image.png`

## Quality verdict
- **Score:** 0.73 (PASS)
- Attempts: 1
- Faces: 517,384 | Vertices: 258,687 | Watertight: False | Components: 6
- Attempt 1 concern: sliver-shaped bounding box (ratio 7.22)
- Attempt 1 LLM opinion: The mesh shows good geometric complexity but is not watertight and has degenerate faces, which may affect its usability.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `09:01:43` **Analyst** [status] started
- `09:01:45` **Analyst** [decision] subject 'jacket' (clothing, complexity medium) - Ensure the jacket is well-lit and avoid cropping any parts to capture its full shape.
- `09:01:45` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `09:01:45` **Analyst** [status] done
- `09:01:45` **Preprocessor** [status] started
- `09:01:46` **Preprocessor** [artifact] user image copied to run folder
- `09:01:51` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `09:01:51` **Preprocessor** [status] done
- `09:01:51` **MeshGen** [status] started
- `09:02:32` **MeshGen** [artifact] hunyuan clay previews saved
- `09:02:32` **MeshGen** [status] done
- `09:02:32` **Judge** [status] started
- `09:02:38` **Judge** [decision] score 0.73 - PASS
- `09:02:38` **Judge** [status] done
- `09:02:38` **TextureSmith** [status] started
- `09:04:15` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `09:04:15` **TextureSmith** [artifact] textured previews saved
- `09:04:15` **TextureSmith** [status] done
- `09:04:15` **Exporter** [status] started
- `09:04:16` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
