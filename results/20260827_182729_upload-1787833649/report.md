# Mew3D Run Report - 20260827_182729_upload-1787833649

- **Date:** 2026-08-27 18:30:22
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787833649.jpg
- **Analyst read:** Stitch (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_182729_upload-1787833649\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 1,058,600 | Vertices: 529,522 | Watertight: False | Components: 25
- Attempt 1 LLM opinion: The mesh quality is generally high, but the presence of multiple components and non-watertight geometry raises concerns.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `18:27:29` **Analyst** [status] started
- `18:27:30` **Analyst** [decision] subject 'Stitch' (character, complexity medium) - Ensure to capture the character's unique features and expressions for accurate reconstruction.
- `18:27:30` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `18:27:30` **Analyst** [status] done
- `18:27:30` **Preprocessor** [status] started
- `18:27:31` **Preprocessor** [artifact] user image copied to run folder
- `18:27:32` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:27:32` **Preprocessor** [status] done
- `18:27:32` **Gatekeeper** [status] started
- `18:27:33` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `18:27:33` **Gatekeeper** [status] done
- `18:27:33` **MeshGen** [status] started
- `18:28:29` **MeshGen** [artifact] hunyuan clay previews saved
- `18:28:29` **MeshGen** [status] done
- `18:28:29` **Judge** [status] started
- `18:28:33` **Judge** [decision] score 0.89 - PASS
- `18:28:33` **Judge** [status] done
- `18:28:33` **TextureSmith** [status] started
- `18:30:20` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `18:30:21` **TextureSmith** [artifact] textured previews saved
- `18:30:21` **TextureSmith** [status] done
- `18:30:21` **Exporter** [status] started
- `18:30:22` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
