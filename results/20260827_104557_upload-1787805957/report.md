# Mew3D Run Report - 20260827_104557_upload-1787805957

- **Date:** 2026-08-27 10:48:35
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787805957.jpg
- **Analyst read:** headphones (prop, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_104557_upload-1787805957\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 949,894 | Vertices: 474,937 | Watertight: False | Components: 6
- Attempt 1 LLM opinion: The mesh is complex and well-detailed, but it is not watertight and has a significant number of degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:45:57` **Analyst** [status] started
- `10:45:58` **Analyst** [decision] subject 'headphones' (prop, complexity medium) - Ensure to capture the texture of the ear cushions and the details of the headband for a realistic reconstruction.
- `10:45:58` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:45:58` **Analyst** [status] done
- `10:45:58` **Preprocessor** [status] started
- `10:45:58` **Preprocessor** [artifact] user image copied to run folder
- `10:46:00` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:46:00` **Preprocessor** [status] done
- `10:46:00` **MeshGen** [status] started
- `10:46:49` **MeshGen** [artifact] hunyuan clay previews saved
- `10:46:49` **MeshGen** [status] done
- `10:46:49` **Judge** [status] started
- `10:46:54` **Judge** [decision] score 0.89 - PASS
- `10:46:54` **Judge** [status] done
- `10:46:54` **TextureSmith** [status] started
- `10:48:33` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:48:34` **TextureSmith** [artifact] textured previews saved
- `10:48:34` **TextureSmith** [status] done
- `10:48:34` **Exporter** [status] started
- `10:48:35` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
