# Mew3D Run Report - 20260827_100839_upload-1787803719

- **Date:** 2026-08-27 10:10:58
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787803719.jpg
- **Analyst read:** stylized doll (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_100839_upload-1787803719\input\user_image.png`

## Quality verdict
- **Score:** 0.96 (PASS)
- Attempts: 1
- Faces: 576,768 | Vertices: 288,386 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh is well-constructed with a high heuristic score, but the presence of degenerate faces raises some concerns.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `10:08:39` **Analyst** [status] started
- `10:08:40` **Analyst** [decision] subject 'stylized doll' (character, complexity medium) - Ensure to capture the smooth surfaces and simple shapes for accurate reconstruction.
- `10:08:40` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `10:08:40` **Analyst** [status] done
- `10:08:40` **Preprocessor** [status] started
- `10:08:41` **Preprocessor** [artifact] user image copied to run folder
- `10:08:43` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `10:08:43` **Preprocessor** [status] done
- `10:08:43` **MeshGen** [status] started
- `10:09:26` **MeshGen** [artifact] hunyuan clay previews saved
- `10:09:26` **MeshGen** [status] done
- `10:09:26` **Judge** [status] started
- `10:09:29` **Judge** [decision] score 0.96 - PASS
- `10:09:29` **Judge** [status] done
- `10:09:29` **TextureSmith** [status] started
- `10:10:57` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `10:10:57` **TextureSmith** [artifact] textured previews saved
- `10:10:57` **TextureSmith** [status] done
- `10:10:57` **Exporter** [status] started
- `10:10:58` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
