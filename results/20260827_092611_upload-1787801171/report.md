# Mew3D Run Report - 20260827_092611_upload-1787801171

- **Date:** 2026-08-27 09:29:14
- **Mode:** image23d
- **Image input:** G:\codes\mew3d\uploads\upload_1787801171.jpg
- **Analyst read:** dragon (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_092611_upload-1787801171\input\user_image.png`

## Backend comparison

| backend | score | faces | components | vision issue |
|---|---|---|---|---|
| triposr | 0.88 | 123,746 | 5 | Some details are less defined in certain views. |
| hunyuan **(winner)** | 0.89 | 1,168,504 | 38 | Some details are less defined in certain views. |

## Quality verdict
- **Score:** 0.89 (PASS)
- Attempts: 1
- Faces: 1,168,504 | Vertices: 584,398 | Watertight: False | Components: 38
- Attempt 1 LLM opinion: The mesh quality is high overall, but significant concerns regarding watertightness and the presence of degenerate faces remain.

## Texture
- **Textured mesh:** `output/mesh_textured.glb` (painted hunyuan mesh via Hunyuan3D-Paint)

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `09:26:11` **Analyst** [status] started
- `09:26:12` **Analyst** [decision] subject 'dragon' (character, complexity medium) - Ensure to capture the details of the facial features and scales for a more dynamic reconstruction.
- `09:26:12` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `09:26:12` **Analyst** [status] done
- `09:26:12` **Preprocessor** [status] started
- `09:26:13` **Preprocessor** [artifact] user image copied to run folder
- `09:26:15` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `09:26:15` **Preprocessor** [status] done
- `09:26:15` **MeshGen** [status] started
- `09:26:26` **MeshGen** [artifact] triposr turntable gif saved
- `09:27:22` **MeshGen** [artifact] hunyuan clay previews saved
- `09:27:22` **MeshGen** [status] done
- `09:27:22` **Judge** [status] started
- `09:27:30` **Judge** [decision] backend comparison: hunyuan 0.89 | triposr 0.88 -> winner: hunyuan
- `09:27:30` **Judge** [decision] score 0.89 - PASS
- `09:27:30` **Judge** [status] done
- `09:27:30` **TextureSmith** [status] started
- `09:29:12` **TextureSmith** [artifact] textured GLB exported (hunyuan mesh)
- `09:29:12` **TextureSmith** [artifact] textured previews saved
- `09:29:12` **TextureSmith** [status] done
- `09:29:12` **Exporter** [status] started
- `09:29:13` **Exporter** [artifact] [triposr] OBJ + GLB exported
- `09:29:14` **Exporter** [artifact] [hunyuan] OBJ + GLB exported <- WINNER
