# Mew3D Run Report - 20260827_080022_upload-1787796022

- **Date:** 2026-08-27 08:03:13
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787796022.jpg
- **Analyst read:** computer monitor (prop, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_080022_upload-1787796022\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 995,828 | Vertices: 497,916 | Watertight: False | Components: 7
- Attempt 1 LLM opinion: The mesh quality is high but lacks watertightness and has multiple components.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `08:00:22` **Analyst** [status] started
- `08:00:23` **Analyst** [decision] subject 'computer monitor' (prop, complexity medium) - Ensure to capture the details of the monitor's screen and the mouse for accurate reconstruction.
- `08:00:23` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `08:00:23` **Analyst** [status] done
- `08:00:23` **Preprocessor** [status] started
- `08:00:24` **Preprocessor** [artifact] user image copied to run folder
- `08:00:26` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `08:00:26` **Preprocessor** [status] done
- `08:00:26` **MeshGen** [status] started
- `08:01:21` **MeshGen** [artifact] hunyuan clay previews saved
- `08:01:21` **MeshGen** [status] done
- `08:01:21` **Judge** [status] started
- `08:01:25` **Judge** [decision] score 0.89 - PASS
- `08:01:25` **Judge** [status] done
- `08:01:25` **TextureSmith** [status] started
- `08:03:11` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `08:03:11` **TextureSmith** [artifact] textured previews saved
- `08:03:11` **TextureSmith** [status] done
- `08:03:11` **Exporter** [status] started
- `08:03:13` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
