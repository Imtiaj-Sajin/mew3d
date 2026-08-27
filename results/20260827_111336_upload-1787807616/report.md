# Mew3D Run Report - 20260827_111336_upload-1787807616

- **Date:** 2026-08-27 11:16:09
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787807616.jpg
- **Analyst read:** letter G (abstract, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_111336_upload-1787807616\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 758,324 | Vertices: 379,162 | Watertight: False | Components: 5
- Attempt 1 LLM opinion: The mesh is of high quality but not watertight, which may affect its usability.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `11:13:36` **Analyst** [status] started
- `11:13:37` **Analyst** [decision] subject 'letter G' (abstract, complexity medium) - Ensure to capture the gradient and translucency of the material for a realistic effect.
- `11:13:37` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `11:13:37` **Analyst** [status] done
- `11:13:37` **Preprocessor** [status] started
- `11:13:38` **Preprocessor** [artifact] user image copied to run folder
- `11:13:39` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `11:13:39` **Preprocessor** [status] done
- `11:13:39` **MeshGen** [status] started
- `11:14:26` **MeshGen** [artifact] hunyuan clay previews saved
- `11:14:26` **MeshGen** [status] done
- `11:14:26` **Judge** [status] started
- `11:14:29` **Judge** [decision] score 0.89 - PASS
- `11:14:29` **Judge** [status] done
- `11:14:29` **TextureSmith** [status] started
- `11:16:08` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `11:16:08` **TextureSmith** [artifact] textured previews saved
- `11:16:08` **TextureSmith** [status] done
- `11:16:08` **Exporter** [status] started
- `11:16:09` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
