# Mew3D Run Report - 20260827_101132_upload-1787803892

- **Date:** 2026-08-27 10:14:06
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787803892.jpg
- **Analyst read:** character (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_101132_upload-1787803892\input\user_image.png`

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 791,020 | Vertices: 395,510 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh quality is satisfactory with a high heuristic score, but the presence of degenerate faces is a concern.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:11:32` **Analyst** [status] started
- `10:11:35` **Analyst** [decision] subject 'character' (character, complexity medium) - Ensure to capture the character's facial expressions and clothing texture for a more realistic reconstruction.
- `10:11:35` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:11:35` **Analyst** [status] done
- `10:11:35` **Preprocessor** [status] started
- `10:11:36` **Preprocessor** [artifact] user image copied to run folder
- `10:11:39` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:11:39` **Preprocessor** [status] done
- `10:11:39` **MeshGen** [status] started
- `10:12:25` **MeshGen** [artifact] hunyuan clay previews saved
- `10:12:25` **MeshGen** [status] done
- `10:12:25` **Judge** [status] started
- `10:12:31` **Judge** [decision] score 0.92 - PASS
- `10:12:31` **Judge** [status] done
- `10:12:31` **TextureSmith** [status] started
- `10:14:05` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:14:05` **TextureSmith** [artifact] textured previews saved
- `10:14:05` **TextureSmith** [status] done
- `10:14:05` **Exporter** [status] started
- `10:14:06` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
