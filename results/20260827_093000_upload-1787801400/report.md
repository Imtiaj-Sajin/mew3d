# Mew3D Run Report - 20260827_093000_upload-1787801400

- **Date:** 2026-08-27 09:32:37
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787801400.png
- **Analyst read:** cartoon monster (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_093000_upload-1787801400\input\user_image.png`

## Backend comparison

| backend | score | faces | components | vision issue |
|---|---|---|---|---|
| triposr **(winner)** | 0.92 | 131,926 | 9 | Minor discrepancies in proportions |
| hunyuan | 0.89 | 768,356 | 4 | Minor details missing |

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 131,926 | Vertices: 65,981 | Watertight: True | Components: 9
- Attempt 1 LLM opinion: The mesh exhibits a good balance of complexity and quality, but the presence of degenerate faces is concerning.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted triposr mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `09:30:00` **Analyst** [status] started
- `09:30:02` **Analyst** [decision] subject 'cartoon monster' (character, complexity medium) - Ensure to capture the texture details of the fur and the character's facial features for a more lifelike representation.
- `09:30:02` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `09:30:02` **Analyst** [status] done
- `09:30:02` **Preprocessor** [status] started
- `09:30:03` **Preprocessor** [artifact] user image copied to run folder
- `09:30:05` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `09:30:05` **Preprocessor** [status] done
- `09:30:05` **MeshGen** [status] started
- `09:30:16` **MeshGen** [artifact] triposr turntable gif saved
- `09:31:04` **MeshGen** [artifact] hunyuan clay previews saved
- `09:31:04` **MeshGen** [status] done
- `09:31:04` **Judge** [status] started
- `09:31:12` **Judge** [decision] backend comparison: triposr 0.92 | hunyuan 0.89 -> winner: triposr
- `09:31:12` **Judge** [decision] score 0.92 - PASS
- `09:31:12` **Judge** [status] done
- `09:31:12` **TextureSmith** [status] started
- `09:32:36` **TextureSmith** [artifact] textured GLB exported (triposr mesh)
- `09:32:36` **TextureSmith** [artifact] textured previews saved
- `09:32:36` **TextureSmith** [status] done
- `09:32:36` **Exporter** [status] started
- `09:32:36` **Exporter** [artifact] [triposr] OBJ + GLB exported <- WINNER
- `09:32:37` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
