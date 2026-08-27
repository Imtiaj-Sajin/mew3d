# Mew3D Run Report - 20260827_103933_upload-1787805573

- **Date:** 2026-08-27 10:41:57
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787805573.png
- **Analyst read:** car (vehicle, complexity high)
- Selected candidate: `G:\codes\mew3d\results\20260827_103933_upload-1787805573\input\user_image.png`

## Quality verdict
- **Score:** 0.85 (PASS)
- Attempts: 1
- Faces: 568,456 | Vertices: 284,229 | Watertight: False | Components: 2
- Attempt 1 LLM opinion: The mesh quality is high, but it is not watertight and has some degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:39:33` **Analyst** [status] started
- `10:39:35` **Analyst** [decision] subject 'car' (vehicle, complexity high) - Ensure to capture the sleek design and unique color accents for accurate reconstruction.
- `10:39:35` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:39:35` **Analyst** [status] done
- `10:39:35` **Preprocessor** [status] started
- `10:39:36` **Preprocessor** [artifact] user image copied to run folder
- `10:39:37` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:39:37` **Preprocessor** [status] done
- `10:39:37` **MeshGen** [status] started
- `10:40:19` **MeshGen** [artifact] hunyuan clay previews saved
- `10:40:19` **MeshGen** [status] done
- `10:40:19` **Judge** [status] started
- `10:40:23` **Judge** [decision] score 0.85 - PASS
- `10:40:23` **Judge** [status] done
- `10:40:23` **TextureSmith** [status] started
- `10:41:56` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:41:56` **TextureSmith** [artifact] textured previews saved
- `10:41:56` **TextureSmith** [status] done
- `10:41:56` **Exporter** [status] started
- `10:41:57` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
