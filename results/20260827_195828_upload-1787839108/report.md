# Mew3D Run Report - 20260827_195828_upload-1787839108

- **Date:** 2026-08-27 20:01:25
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787839108.jpg
- **Analyst read:** wizard character (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_195828_upload-1787839108\input\user_image.png`

## Quality verdict
- **Score:** 0.93 (PASS)
- Attempts: 1
- Faces: 975,636 | Vertices: 487,822 | Watertight: False | Components: 12
- Attempt 1 LLM opinion: The mesh of the wizard character demonstrates a high level of detail but exhibits significant issues with watertightness and component fragmentation.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `19:58:28` **Analyst** [status] started
- `19:58:30` **Analyst** [decision] subject 'wizard character' (character, complexity medium) - Ensure to capture the details of the wizard's robe and the glowing torch for a more dynamic reconstruction.
- `19:58:30` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `19:58:30` **Analyst** [status] done
- `19:58:30` **Preprocessor** [status] started
- `19:58:31` **Preprocessor** [artifact] user image copied to run folder
- `19:58:33` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `19:58:33` **Preprocessor** [status] done
- `19:58:33` **Gatekeeper** [status] started
- `19:58:34` **Gatekeeper** [decision] prepared image looks reconstructable - handing to MeshGen
- `19:58:34` **Gatekeeper** [status] done
- `19:58:34` **MeshGen** [status] started
- `19:59:29` **MeshGen** [artifact] hunyuan clay previews saved
- `19:59:29` **MeshGen** [status] done
- `19:59:29` **Judge** [status] started
- `19:59:34` **Judge** [decision] score 0.93 - PASS
- `19:59:34` **Judge** [status] done
- `19:59:34` **TextureSmith** [status] started
- `20:01:23` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `20:01:23` **TextureSmith** [artifact] textured previews saved
- `20:01:23` **TextureSmith** [status] done
- `20:01:23` **Exporter** [status] started
- `20:01:25` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
