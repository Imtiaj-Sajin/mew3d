# Mew3D Run Report - 20260827_105723_upload-1787806643

- **Date:** 2026-08-27 11:00:03
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787806643.png
- **Analyst read:** game controller (prop, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_105723_upload-1787806643\input\user_image.png`

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 990,396 | Vertices: 495,200 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh quality is high with a solid structure, but the presence of degenerate faces is a concern.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:57:23` **Analyst** [status] started
- `10:57:24` **Analyst** [decision] subject 'game controller' (prop, complexity medium) - Ensure to capture the details of the buttons and texture of the grips for accurate reconstruction.
- `10:57:24` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:57:24` **Analyst** [status] done
- `10:57:24` **Preprocessor** [status] started
- `10:57:25` **Preprocessor** [artifact] user image copied to run folder
- `10:57:26` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:57:26` **Preprocessor** [status] done
- `10:57:26` **MeshGen** [status] started
- `10:58:17` **MeshGen** [artifact] hunyuan clay previews saved
- `10:58:17` **MeshGen** [status] done
- `10:58:17` **Judge** [status] started
- `10:58:21` **Judge** [decision] score 0.92 - PASS
- `10:58:21` **Judge** [status] done
- `10:58:21` **TextureSmith** [status] started
- `11:00:02` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `11:00:02` **TextureSmith** [artifact] textured previews saved
- `11:00:02` **TextureSmith** [status] done
- `11:00:02` **Exporter** [status] started
- `11:00:03` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
