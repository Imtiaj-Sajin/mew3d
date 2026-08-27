# Mew3D Run Report - 20260827_181511_upload-1787832911

- **Date:** 2026-08-27 18:18:25
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787832911.jpg
- **Analyst read:** scooter (vehicle, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_181511_upload-1787832911\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 711,346 | Vertices: 355,759 | Watertight: False | Components: 40
- Attempt 1 LLM opinion: The mesh quality is high but has significant concerns due to non-watertightness and a high number of components.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `18:15:11` **Analyst** [status] started
- `18:15:12` **Analyst** [decision] subject 'scooter' (vehicle, complexity medium) - Ensure to capture the details of the scooter's design and features for accurate reconstruction.
- `18:15:12` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `18:15:12` **Analyst** [status] done
- `18:15:12` **Preprocessor** [status] started
- `18:15:14` **Preprocessor** [artifact] user image copied to run folder
- `18:15:18` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:15:18` **Preprocessor** [status] done
- `18:15:18` **Gatekeeper** [status] started
- `18:15:19` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `18:15:19` **Gatekeeper** [status] done
- `18:15:19` **MeshGen** [status] started
- `18:16:27` **MeshGen** [artifact] hunyuan clay previews saved
- `18:16:27` **MeshGen** [status] done
- `18:16:27` **Judge** [status] started
- `18:16:33` **Judge** [decision] score 0.89 - PASS
- `18:16:33` **Judge** [status] done
- `18:16:33` **TextureSmith** [status] started
- `18:18:23` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `18:18:24` **TextureSmith** [artifact] textured previews saved
- `18:18:24` **TextureSmith** [status] done
- `18:18:24` **Exporter** [status] started
- `18:18:25` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
