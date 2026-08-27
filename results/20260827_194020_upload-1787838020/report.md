# Mew3D Run Report - 20260827_194020_upload-1787838020

- **Date:** 2026-08-27 19:42:57
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787838020.jpg
- **Analyst read:** bird (creature, complexity low)
- Selected candidate: `G:\codes\mew3d\results\20260827_194020_upload-1787838020\input\user_image.png`

## Quality verdict
- **Score:** 0.93 (PASS)
- Attempts: 1
- Faces: 705,708 | Vertices: 352,852 | Watertight: False | Components: 9
- Attempt 1 LLM opinion: The mesh shows good quality overall but has significant concerns regarding watertightness and degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `19:40:20` **Analyst** [status] started
- `19:40:22` **Analyst** [decision] subject 'bird' (creature, complexity low) - Ensure the bird's features are well-defined and avoid any busy backgrounds.
- `19:40:22` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `19:40:22` **Analyst** [status] done
- `19:40:22` **Preprocessor** [status] started
- `19:40:22` **Preprocessor** [artifact] user image copied to run folder
- `19:40:24` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `19:40:24` **Preprocessor** [status] done
- `19:40:24` **Gatekeeper** [status] started
- `19:40:26` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `19:40:26` **Gatekeeper** [status] done
- `19:40:26` **MeshGen** [status] started
- `19:41:12` **MeshGen** [artifact] hunyuan clay previews saved
- `19:41:12` **MeshGen** [status] done
- `19:41:12` **Judge** [status] started
- `19:41:16` **Judge** [decision] score 0.93 - PASS
- `19:41:16` **Judge** [status] done
- `19:41:16` **TextureSmith** [status] started
- `19:42:56` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `19:42:56` **TextureSmith** [artifact] textured previews saved
- `19:42:56` **TextureSmith** [status] done
- `19:42:56` **Exporter** [status] started
- `19:42:57` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
