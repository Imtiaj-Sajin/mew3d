# Mew3D Run Report - 20260827_192930_upload-1787837370

- **Date:** 2026-08-27 19:32:01
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787837370.jpg
- **Analyst read:** pink bunny character (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_192930_upload-1787837370\input\user_image.png`

## Quality verdict
- **Score:** 0.93 (PASS)
- Attempts: 1
- Faces: 575,352 | Vertices: 287,676 | Watertight: False | Components: 5
- Attempt 1 LLM opinion: The mesh quality is high, but it is not watertight and contains several degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `19:29:30` **Analyst** [status] started
- `19:29:35` **Analyst** [decision] subject 'pink bunny character' (character, complexity medium) - Ensure to capture the character's facial features and fluffy texture for a more realistic 3D model.
- `19:29:35` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `19:29:35` **Analyst** [status] done
- `19:29:35` **Preprocessor** [status] started
- `19:29:36` **Preprocessor** [artifact] user image copied to run folder
- `19:29:38` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `19:29:38` **Preprocessor** [status] done
- `19:29:38` **Gatekeeper** [status] started
- `19:29:39` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `19:29:39` **Gatekeeper** [status] done
- `19:29:39` **MeshGen** [status] started
- `19:30:23` **MeshGen** [artifact] hunyuan clay previews saved
- `19:30:23` **MeshGen** [status] done
- `19:30:23` **Judge** [status] started
- `19:30:27` **Judge** [decision] score 0.93 - PASS
- `19:30:27` **Judge** [status] done
- `19:30:27` **TextureSmith** [status] started
- `19:32:00` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `19:32:00` **TextureSmith** [artifact] textured previews saved
- `19:32:00` **TextureSmith** [status] done
- `19:32:00` **Exporter** [status] started
- `19:32:01` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
