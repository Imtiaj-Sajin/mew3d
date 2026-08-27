# Mew3D Run Report - 20260827_103158_upload-1787805118

- **Date:** 2026-08-27 10:34:33
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787805118.jpg
- **Analyst read:** character (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_103158_upload-1787805118\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 582,428 | Vertices: 291,222 | Watertight: False | Components: 3
- Attempt 1 LLM opinion: The mesh is of high quality but has issues with watertightness and degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:31:58` **Analyst** [status] started
- `10:31:59` **Analyst** [decision] subject 'character' (character, complexity medium) - Ensure to capture the distinct geometric shapes and colors of the character for accurate reconstruction.
- `10:31:59` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:31:59` **Analyst** [status] done
- `10:31:59` **Preprocessor** [status] started
- `10:32:00` **Preprocessor** [artifact] user image copied to run folder
- `10:32:02` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:32:02` **Preprocessor** [status] done
- `10:32:02` **MeshGen** [status] started
- `10:32:44` **MeshGen** [artifact] hunyuan clay previews saved
- `10:32:44` **MeshGen** [status] done
- `10:32:44` **Judge** [status] started
- `10:32:48` **Judge** [decision] score 0.89 - PASS
- `10:32:48` **Judge** [status] done
- `10:32:48` **TextureSmith** [status] started
- `10:34:32` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:34:32` **TextureSmith** [artifact] textured previews saved
- `10:34:32` **TextureSmith** [status] done
- `10:34:32` **Exporter** [status] started
- `10:34:33` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
