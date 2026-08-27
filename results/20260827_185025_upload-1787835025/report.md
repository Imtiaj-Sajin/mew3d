# Mew3D Run Report - 20260827_185025_upload-1787835025

- **Date:** 2026-08-27 18:53:09
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787835025.jpg
- **Analyst read:** crab (creature, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_185025_upload-1787835025\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 768,436 | Vertices: 384,219 | Watertight: False | Components: 2
- Attempt 1 LLM opinion: The mesh exhibits high detail but is not watertight, which is a significant issue.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `18:50:25` **Analyst** [status] started
- `18:50:29` **Analyst** [decision] subject 'crab' (creature, complexity medium) - Ensure the limbs and facial features are well-defined for a playful appearance.
- `18:50:29` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `18:50:29` **Analyst** [status] done
- `18:50:29` **Preprocessor** [status] started
- `18:50:30` **Preprocessor** [artifact] user image copied to run folder
- `18:50:31` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:50:31` **Preprocessor** [status] done
- `18:50:31` **Gatekeeper** [status] started
- `18:50:33` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `18:50:33` **Gatekeeper** [status] done
- `18:50:33` **MeshGen** [status] started
- `18:51:22` **MeshGen** [artifact] hunyuan clay previews saved
- `18:51:22` **MeshGen** [status] done
- `18:51:22` **Judge** [status] started
- `18:51:26` **Judge** [decision] score 0.89 - PASS
- `18:51:26` **Judge** [status] done
- `18:51:26` **TextureSmith** [status] started
- `18:53:07` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `18:53:08` **TextureSmith** [artifact] textured previews saved
- `18:53:08` **TextureSmith** [status] done
- `18:53:08` **Exporter** [status] started
- `18:53:09` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
