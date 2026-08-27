# Mew3D Run Report - 20260827_183407_upload-1787834047

- **Date:** 2026-08-27 18:37:09
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787834047.jpg
- **Analyst read:** cartoon bee (creature, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_183407_upload-1787834047\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 906,788 | Vertices: 453,388 | Watertight: False | Components: 8
- Attempt 1 LLM opinion: The mesh exhibits a high quality with minor geometric issues.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `18:34:07` **Analyst** [status] started
- `18:34:08` **Analyst** [decision] subject 'cartoon bee' (creature, complexity medium) - Ensure to capture the fluffy texture and the transparent wings for a more realistic reconstruction.
- `18:34:08` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `18:34:08` **Analyst** [status] done
- `18:34:08` **Preprocessor** [status] started
- `18:34:09` **Preprocessor** [artifact] user image copied to run folder
- `18:34:11` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:34:11` **Preprocessor** [status] done
- `18:34:11` **Gatekeeper** [status] started
- `18:34:12` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `18:34:12` **Gatekeeper** [status] done
- `18:34:12` **MeshGen** [status] started
- `18:35:04` **MeshGen** [artifact] hunyuan clay previews saved
- `18:35:04` **MeshGen** [status] done
- `18:35:04` **Judge** [status] started
- `18:35:08` **Judge** [decision] score 0.89 - PASS
- `18:35:08` **Judge** [status] done
- `18:35:08` **TextureSmith** [status] started
- `18:37:08` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `18:37:08` **TextureSmith** [artifact] textured previews saved
- `18:37:08` **TextureSmith** [status] done
- `18:37:08` **Exporter** [status] started
- `18:37:09` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
