# Mew3D Run Report - 20260827_191636_upload-1787836596

- **Date:** 2026-08-27 19:19:35
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787836596.jpg
- **Analyst read:** dragon (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_191636_upload-1787836596\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 971,530 | Vertices: 485,797 | Watertight: False | Components: 28
- Attempt 1 LLM opinion: The mesh quality is high but lacks watertightness, which is a significant concern.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `19:16:36` **Analyst** [status] started
- `19:16:38` **Analyst** [decision] subject 'dragon' (character, complexity medium) - Ensure to capture the details of the wings and facial features for a more accurate reconstruction.
- `19:16:38` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `19:16:38` **Analyst** [status] done
- `19:16:38` **Preprocessor** [status] started
- `19:16:39` **Preprocessor** [artifact] user image copied to run folder
- `19:16:41` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `19:16:41` **Preprocessor** [status] done
- `19:16:41` **Gatekeeper** [status] started
- `19:16:44` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `19:16:44` **Gatekeeper** [status] done
- `19:16:44` **MeshGen** [status] started
- `19:17:38` **MeshGen** [artifact] hunyuan clay previews saved
- `19:17:38` **MeshGen** [status] done
- `19:17:38` **Judge** [status] started
- `19:17:43` **Judge** [decision] score 0.89 - PASS
- `19:17:43` **Judge** [status] done
- `19:17:43` **TextureSmith** [status] started
- `19:19:34` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `19:19:34` **TextureSmith** [artifact] textured previews saved
- `19:19:34` **TextureSmith** [status] done
- `19:19:34` **Exporter** [status] started
- `19:19:35` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
