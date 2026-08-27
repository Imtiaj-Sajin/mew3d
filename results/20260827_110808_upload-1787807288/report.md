# Mew3D Run Report - 20260827_110808_upload-1787807288

- **Date:** 2026-08-27 11:10:30
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787807288.jpg
- **Analyst read:** cute creature (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_110808_upload-1787807288\input\user_image.png`

## Quality verdict
- **Score:** 0.93 (PASS)
- Attempts: 1
- Faces: 734,032 | Vertices: 367,016 | Watertight: False | Components: 3
- Attempt 1 LLM opinion: The mesh quality is high, but it is not watertight and has a significant number of degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `11:08:08` **Analyst** [status] started
- `11:08:09` **Analyst** [decision] subject 'cute creature' (character, complexity medium) - Ensure to capture the smooth surface and rounded features for a more appealing 3D model.
- `11:08:09` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `11:08:09` **Analyst** [status] done
- `11:08:09` **Preprocessor** [status] started
- `11:08:10` **Preprocessor** [artifact] user image copied to run folder
- `11:08:11` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `11:08:11` **Preprocessor** [status] done
- `11:08:11` **MeshGen** [status] started
- `11:08:57` **MeshGen** [artifact] hunyuan clay previews saved
- `11:08:57` **MeshGen** [status] done
- `11:08:57` **Judge** [status] started
- `11:09:00` **Judge** [decision] score 0.93 - PASS
- `11:09:00` **Judge** [status] done
- `11:09:00` **TextureSmith** [status] started
- `11:10:29` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `11:10:29` **TextureSmith** [artifact] textured previews saved
- `11:10:29` **TextureSmith** [status] done
- `11:10:29` **Exporter** [status] started
- `11:10:30` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
