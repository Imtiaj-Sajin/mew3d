# Mew3D Run Report - 20260827_091846_upload-1787800726

- **Date:** 2026-08-27 09:22:45
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787800726.jpg
- **Analyst read:** pixel character (character, complexity low)
- Selected candidate: `G:\codes\mew3d\results\20260827_091846_upload-1787800726\input\user_image.png`

## Quality verdict
- **Score:** 0.14 (below threshold, best effort)
- Attempts: 2
- Faces: 2,368 | Vertices: 1,198 | Watertight: True | Components: 7
- Attempt 1 concern: very low face count (1720)
- Attempt 1 concern: fragmented: 5 pieces, main piece only 68% of faces
- Attempt 1 concern: sliver-shaped bounding box (ratio 12.56)
- Attempt 1 LLM opinion: The mesh quality is poor and requires significant improvement.
- Attempt 2 concern: low face count (2368)
- Attempt 2 concern: fragmented: 7 pieces, main piece only 55% of faces
- Attempt 2 concern: sliver-shaped bounding box (ratio 8.67)
- Attempt 2 LLM opinion: The mesh shows significant issues with geometry quality and component integrity.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `09:18:46` **Analyst** [status] started
- `09:18:47` **Analyst** [decision] subject 'pixel character' (character, complexity low) - Ensure to capture the pixelated style and maintain the simplicity of the character.
- `09:18:47` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `09:18:47` **Analyst** [status] done
- `09:18:47` **Preprocessor** [status] started
- `09:18:48` **Preprocessor** [artifact] user image copied to run folder
- `09:18:49` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `09:18:49` **Preprocessor** [status] done
- `09:18:49` **MeshGen** [status] started
- `09:20:18` **MeshGen** [artifact] hunyuan clay previews saved
- `09:20:18` **MeshGen** [status] done
- `09:20:18` **Judge** [status] started
- `09:20:22` **Judge** [decision] score 0.02 < 0.55 - requesting retry with {'foreground_ratio': 0.75, 'mc_resolution': 320}
- `09:20:22` **Judge** [status] done
- `09:20:22` **Preprocessor** [status] started
- `09:20:23` **Preprocessor** [artifact] processed input ready (foreground ratio 0.75)
- `09:20:23` **Preprocessor** [status] done
- `09:20:23` **MeshGen** [status] started
- `09:21:26` **MeshGen** [artifact] hunyuan clay previews saved
- `09:21:26` **MeshGen** [status] done
- `09:21:26` **Judge** [status] started
- `09:21:29` **Judge** [decision] score 0.14 - accepting best effort (no retries left)
- `09:21:29` **Judge** [status] done
- `09:21:29` **TextureSmith** [status] started
- `09:22:44` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `09:22:45` **TextureSmith** [artifact] textured previews saved
- `09:22:45` **TextureSmith** [status] done
- `09:22:45` **Exporter** [status] started
- `09:22:45` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
