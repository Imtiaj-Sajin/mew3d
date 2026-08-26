# Mew3D Run Report - 20260827_002232_face-man

- **Date:** 2026-08-27 00:23:58
- **Mode:** image23d
- **Image input:** D:\Downloads\face man.jpg
- **Analyst read:** male character (character, complexity medium)
- Selected candidate: `G:\codes\mew3d\results\20260827_002232_face-man\input\user_image.png`

## Backend comparison

| backend | score | faces | components | vision issue |
|---|---|---|---|---|
| triposr **(winner)** | 0.92 | 116,428 | 1 | Minor inaccuracies in hair volume |
| hunyuan | 0.89 | 899,332 | 41 | Minor inaccuracies in hair detail |

## Quality verdict
- **Score:** 0.92 (PASS)
- Attempts: 1
- Faces: 116,428 | Vertices: 58,216 | Watertight: True | Components: 1
- Attempt 1 LLM opinion: The mesh quality is high with a solid structure and good geometric metrics.

## Outputs
- `output/mesh.obj`, `output/mesh.glb` (vertex-colored)
- `output/preview_*.png`, `output/turntable.gif`
- `intermediate/` - candidates and processed inputs
- `logs/events.jsonl` - every agent action, timestamped

## Agent timeline
- `00:22:33` **Analyst** [status] started
- `00:22:35` **Analyst** [decision] subject 'male character' (character, complexity medium) - Ensure to capture the facial features and hairstyle details for accurate reconstruction.
- `00:22:35` **Analyst** [decision] pipeline plan: Preprocessor -> MeshGen -> Judge -> Exporter
- `00:22:35` **Analyst** [status] done
- `00:22:35` **Preprocessor** [status] started
- `00:22:37` **Preprocessor** [artifact] user image copied to run folder
- `00:22:39` **Preprocessor** [artifact] processed input ready (foreground ratio 0.85)
- `00:22:39` **Preprocessor** [status] done
- `00:22:39` **MeshGen** [status] started
- `00:22:52` **MeshGen** [artifact] triposr turntable gif saved
- `00:23:47` **MeshGen** [artifact] hunyuan clay previews saved
- `00:23:47` **MeshGen** [status] done
- `00:23:47` **Judge** [status] started
- `00:23:57` **Judge** [decision] backend comparison: triposr 0.92 | hunyuan 0.89 -> winner: triposr
- `00:23:57` **Judge** [decision] score 0.92 - PASS
- `00:23:57` **Judge** [status] done
- `00:23:57` **Exporter** [status] started
- `00:23:57` **Exporter** [artifact] [triposr] OBJ + GLB exported <- WINNER
- `00:23:58` **Exporter** [artifact] [hunyuan] OBJ + GLB exported
