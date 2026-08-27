# Mew3D Run Report - 20260827_193307_upload-1787837587

- **Date:** 2026-08-27 19:35:57
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787837587.jpg
- **Analyst read:** young man (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_193307_upload-1787837587\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 899,332 | Vertices: 450,048 | Watertight: False | Components: 41
- Attempt 1 LLM opinion: The mesh exhibits good complexity but has significant concerns regarding watertightness and component fragmentation.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `19:33:07` **Analyst** [status] started
- `19:33:08` **Analyst** [decision] subject 'young man' (character, complexity medium) - Ensure to capture the facial features and hairstyle details for accurate reconstruction.
- `19:33:08` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `19:33:08` **Analyst** [status] done
- `19:33:08` **Preprocessor** [status] started
- `19:33:09` **Preprocessor** [artifact] user image copied to run folder
- `19:33:11` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `19:33:11` **Preprocessor** [status] done
- `19:33:11` **Gatekeeper** [status] started
- `19:33:14` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `19:33:14` **Gatekeeper** [status] done
- `19:33:14` **MeshGen** [status] started
- `19:34:08` **MeshGen** [artifact] hunyuan clay previews saved
- `19:34:08` **MeshGen** [status] done
- `19:34:08` **Judge** [status] started
- `19:34:13` **Judge** [decision] score 0.89 - PASS
- `19:34:13` **Judge** [status] done
- `19:34:13` **TextureSmith** [status] started
- `19:35:55` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `19:35:55` **TextureSmith** [artifact] textured previews saved
- `19:35:55` **TextureSmith** [status] done
- `19:35:55` **Exporter** [status] started
- `19:35:57` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
