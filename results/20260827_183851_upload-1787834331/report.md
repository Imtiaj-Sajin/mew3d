# Mew3D Run Report - 20260827_183851_upload-1787834331

- **Date:** 2026-08-27 18:41:41
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787834331.jpg
- **Analyst read:** Hello Kitty (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_183851_upload-1787834331\input\user_image.png`

## Quality verdict
- **Score:** 0.96 (PASS)
- Attempts: 1
- Faces: 964,164 | Vertices: 482,082 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh of Hello Kitty is well-constructed and meets quality standards, although the presence of degenerate faces is a minor concern.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `18:38:51` **Analyst** [status] started
- `18:38:53` **Analyst** [decision] subject 'Hello Kitty' (character, complexity medium) - Ensure to capture the details of the bow and facial features for accurate reconstruction.
- `18:38:53` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `18:38:53` **Analyst** [status] done
- `18:38:53` **Preprocessor** [status] started
- `18:38:53` **Preprocessor** [artifact] user image copied to run folder
- `18:38:55` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:38:55` **Preprocessor** [status] done
- `18:38:55` **Gatekeeper** [status] started
- `18:38:57` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `18:38:57` **Gatekeeper** [status] done
- `18:38:57` **MeshGen** [status] started
- `18:39:50` **MeshGen** [artifact] hunyuan clay previews saved
- `18:39:50` **MeshGen** [status] done
- `18:39:50` **Judge** [status] started
- `18:39:54` **Judge** [decision] score 0.96 - PASS
- `18:39:54` **Judge** [status] done
- `18:39:54` **TextureSmith** [status] started
- `18:41:39` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `18:41:39` **TextureSmith** [artifact] textured previews saved
- `18:41:39` **TextureSmith** [status] done
- `18:41:39` **Exporter** [status] started
- `18:41:41` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
