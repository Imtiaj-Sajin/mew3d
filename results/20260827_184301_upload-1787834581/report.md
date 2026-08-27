# Mew3D Run Report - 20260827_184301_upload-1787834581

- **Date:** 2026-08-27 18:45:41
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787834581.jpg
- **Analyst read:** Minion (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_184301_upload-1787834581\input\user_image.png`

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 725,564 | Vertices: 362,781 | Watertight: False | Components: 3
- Attempt 1 LLM opinion: The mesh quality is high but has concerns regarding watertightness and degeneracy.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `18:43:01` **Analyst** [status] started
- `18:43:03` **Analyst** [decision] subject 'Minion' (character, complexity medium) - Ensure to capture the character's distinctive features and avoid a busy background.
- `18:43:03` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `18:43:03` **Analyst** [status] done
- `18:43:03` **Preprocessor** [status] started
- `18:43:03` **Preprocessor** [artifact] user image copied to run folder
- `18:43:06` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `18:43:06` **Preprocessor** [status] done
- `18:43:06` **Gatekeeper** [status] started
- `18:43:07` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `18:43:07` **Gatekeeper** [status] done
- `18:43:07` **MeshGen** [status] started
- `18:43:57` **MeshGen** [artifact] hunyuan clay previews saved
- `18:43:57` **MeshGen** [status] done
- `18:43:57` **Judge** [status] started
- `18:44:01` **Judge** [decision] score 0.89 - PASS
- `18:44:01` **Judge** [status] done
- `18:44:01` **TextureSmith** [status] started
- `18:45:40` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `18:45:40` **TextureSmith** [artifact] textured previews saved
- `18:45:40` **TextureSmith** [status] done
- `18:45:40` **Exporter** [status] started
- `18:45:41` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
