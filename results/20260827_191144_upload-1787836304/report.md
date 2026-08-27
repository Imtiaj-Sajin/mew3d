# Mew3D Run Report - 20260827_191144_upload-1787836304

- **Date:** 2026-08-27 19:14:59
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787836304.jpg
- **Analyst read:** Batman figure (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_191144_upload-1787836304\input\user_image.png`

## Quality verdict
- **Score:** 0.96 (PASS)
- Attempts: 1
- Faces: 635,384 | Vertices: 317,692 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh is well-constructed with a high heuristic score, but the presence of degenerate faces needs attention.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `19:11:46` **Analyst** [status] started
- `19:11:48` **Analyst** [decision] subject 'Batman figure' (character, complexity medium) - Ensure to capture the details of the costume and facial expression for accurate reconstruction.
- `19:11:48` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `19:11:48` **Analyst** [status] done
- `19:11:48` **Preprocessor** [status] started
- `19:11:51` **Preprocessor** [artifact] user image copied to run folder
- `19:11:53` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `19:11:53` **Preprocessor** [status] done
- `19:11:53` **Gatekeeper** [status] started
- `19:11:54` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `19:11:54` **Gatekeeper** [status] done
- `19:11:54` **MeshGen** [status] started
- `19:12:48` **MeshGen** [artifact] hunyuan clay previews saved
- `19:12:48` **MeshGen** [status] done
- `19:12:48` **Judge** [status] started
- `19:12:52` **Judge** [decision] score 0.96 - PASS
- `19:12:52` **Judge** [status] done
- `19:12:52` **TextureSmith** [status] started
- `19:14:57` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `19:14:58` **TextureSmith** [artifact] textured previews saved
- `19:14:58` **TextureSmith** [status] done
- `19:14:58` **Exporter** [status] started
- `19:14:59` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
