# Mew3D Run Report - 20260827_102726_upload-1787804846

- **Date:** 2026-08-27 10:30:53
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787804846.jpg
- **Analyst read:** character (character, complexity high)
- Selected candidate: `G:\codes\mew3d\results\20260827_102726_upload-1787804846\input\user_image.png`

## Quality verdict
- **Score:** 0.193 (below threshold, best effort)
- Attempts: 2
- Faces: 984,555 | Vertices: 492,377 | Watertight: False | Components: 56
- Attempt 1 concern: fragmented: 79 pieces, main piece only 29% of faces
- Attempt 1 concern: source image foreground was fragmented
- Attempt 1 LLM opinion: The mesh quality is acceptable but requires improvements in watertightness and component reduction.
- Attempt 2 concern: fragmented: 56 pieces, main piece only 29% of faces
- Attempt 2 concern: source image foreground was fragmented
- Attempt 2 LLM opinion: The mesh quality is subpar due to multiple concerns, particularly the lack of watertightness and a high number of components.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:27:26` **Analyst** [status] started
- `10:27:29` **Analyst** [decision] subject 'character' (character, complexity high) - Ensure to capture the details of the clothing and armor for accurate reconstruction.
- `10:27:29` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:27:29` **Analyst** [status] done
- `10:27:29` **Preprocessor** [status] started
- `10:27:29` **Preprocessor** [artifact] user image copied to run folder
- `10:27:31` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:27:31` **Preprocessor** [status] done
- `10:27:31` **MeshGen** [status] started
- `10:28:23` **MeshGen** [artifact] hunyuan clay previews saved
- `10:28:23` **MeshGen** [status] done
- `10:28:23` **Judge** [status] started
- `10:28:28` **Judge** [decision] score 0.19 < 0.55 - requesting retry with {'foreground_ratio': 0.75, 'mc_resolution': 320}
- `10:28:28` **Judge** [status] done
- `10:28:28` **Preprocessor** [status] started
- `10:28:30` **Preprocessor** [artifact] processed input ready (foreground ratio 0.75)
- `10:28:30` **Preprocessor** [status] done
- `10:28:30` **MeshGen** [status] started
- `10:28:56` **MeshGen** [artifact] hunyuan clay previews saved
- `10:28:56` **MeshGen** [status] done
- `10:28:56` **Judge** [status] started
- `10:29:04` **Judge** [decision] score 0.19 - accepting best effort (no retries left)
- `10:29:04` **Judge** [status] done
- `10:29:04` **TextureSmith** [status] started
- `10:30:52` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:30:52` **TextureSmith** [artifact] textured previews saved
- `10:30:52` **TextureSmith** [status] done
- `10:30:52` **Exporter** [status] started
- `10:30:53` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
