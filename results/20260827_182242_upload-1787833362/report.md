# Mew3D Run Report - 20260827_182242_upload-1787833362

- **Date:** 2026-08-27 18:25:24
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787833362.png
- **Analyst read:** scooter (vehicle, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_182242_upload-1787833362\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 601,590 | Vertices: 300,687 | Watertight: False | Components: 7
- Attempt 2 LLM opinion: The mesh quality is generally high but concerns about watertightness and the presence of degenerate faces need to be addressed.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `18:22:42` **Analyst** [status] started
- `18:22:43` **Analyst** [decision] subject 'scooter' (vehicle, complexity medium) - Ensure to capture different angles for a comprehensive reconstruction.
- `18:22:43` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `18:22:43` **Analyst** [status] done
- `18:22:43` **Preprocessor** [status] started
- `18:22:44` **Preprocessor** [artifact] user image copied to run folder
- `18:22:46` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:22:46` **Preprocessor** [status] done
- `18:22:46` **Gatekeeper** [status] started
- `18:22:47` **Gatekeeper** [decision] stopping before the GPU: multiple_objects. Retrying preprocessing with {'largest_component_only': True} instead of reconstructing bad input
- `18:22:47` **Gatekeeper** [status] done
- `18:22:47` **Preprocessor** [status] started
- `18:22:48` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:22:48` **Preprocessor** [status] done
- `18:22:48` **Gatekeeper** [status] started
- `18:22:50` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `18:22:50` **Gatekeeper** [status] done
- `18:22:50` **MeshGen** [status] started
- `18:23:35` **MeshGen** [artifact] hunyuan clay previews saved
- `18:23:35` **MeshGen** [status] done
- `18:23:35` **Judge** [status] started
- `18:23:39` **Judge** [decision] score 0.89 - PASS
- `18:23:39` **Judge** [status] done
- `18:23:39` **TextureSmith** [status] started
- `18:25:23` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `18:25:23` **TextureSmith** [artifact] textured previews saved
- `18:25:23` **TextureSmith** [status] done
- `18:25:23` **Exporter** [status] started
- `18:25:24` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
