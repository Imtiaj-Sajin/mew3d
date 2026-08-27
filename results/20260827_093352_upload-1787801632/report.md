# Mew3D Run Report - 20260827_093352_upload-1787801632

- **Date:** 2026-08-27 09:36:19
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787801632.png
- **Analyst read:** Pikachu (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_093352_upload-1787801632\input\user_image.png`

## Quality verdict
- **Score:** 0.93 (PASS)
- Attempts: 1
- Faces: 765,512 | Vertices: 382,752 | Watertight: False | Components: 11
- Attempt 1 LLM opinion: The mesh shows good detail but has concerns regarding watertightness and the presence of degenerate faces.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `09:33:52` **Analyst** [status] started
- `09:33:54` **Analyst** [decision] subject 'Pikachu' (character, complexity medium) - Ensure to capture the character's distinct features and colors accurately.
- `09:33:54` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `09:33:54` **Analyst** [status] done
- `09:33:54` **Preprocessor** [status] started
- `09:33:54` **Preprocessor** [artifact] user image copied to run folder
- `09:33:56` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `09:33:56` **Preprocessor** [status] done
- `09:33:56` **MeshGen** [status] started
- `09:34:42` **MeshGen** [artifact] hunyuan clay previews saved
- `09:34:42` **MeshGen** [status] done
- `09:34:42` **Judge** [status] started
- `09:34:47` **Judge** [decision] score 0.93 - PASS
- `09:34:47` **Judge** [status] done
- `09:34:47` **TextureSmith** [status] started
- `09:36:18` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `09:36:18` **TextureSmith** [artifact] textured previews saved
- `09:36:18` **TextureSmith** [status] done
- `09:36:18` **Exporter** [status] started
- `09:36:19` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
